import tensorflow as tf
from tensorflow.keras import layers, models

FS_TARGET        = 30
SEGMENT_DURATION = 9.6
WINDOW_SAMPLES   = int(SEGMENT_DURATION * FS_TARGET)   # 288
N_CHANNELS_IN    = 3
N_FILTERS        = 8


def _channel_encoder(channel_input, name, n_out):
    x = channel_input
    for kernel, stage in zip([150, 75, 50], [1, 2, 3]):
        x = layers.SeparableConv1D(n_out, kernel, padding='same', name=f"{name}_conv{stage}")(x)
        x = layers.LayerNormalization(name=f"{name}_norm{stage}")(x)
        x = layers.ReLU(name=f"{name}_relu{stage}")(x)
        x = layers.MaxPooling1D(2, name=f"{name}_pool{stage}")(x)
        x = layers.Dropout(0.1, name=f"{name}_drop{stage}")(x)
    return x


def build_late_fusion_dual_task(input_len=WINDOW_SAMPLES, n_in=N_CHANNELS_IN, n_out=N_FILTERS):
    inputs = layers.Input(shape=(input_len, n_in), name="input_3ch")

    bw = layers.Lambda(lambda x: x[:, :, 0:1], name="extract_BW")(inputs)
    am = layers.Lambda(lambda x: x[:, :, 1:2], name="extract_AM")(inputs)
    fm = layers.Lambda(lambda x: x[:, :, 2:3], name="extract_FM")(inputs)

    bw_feat = _channel_encoder(bw, "BW", n_out)
    am_feat = _channel_encoder(am, "AM", n_out)
    fm_feat = _channel_encoder(fm, "FM", n_out)

    fused = layers.Concatenate(axis=-1, name="late_fusion")([bw_feat, am_feat, fm_feat])

    shared = layers.Conv1D(n_out * 2, 7, padding='same', name="shared_conv1")(fused)
    shared = layers.LayerNormalization(name="shared_norm1")(shared)
    shared = layers.ReLU(name="shared_relu1")(shared)
    shared = layers.Dropout(0.15, name="shared_drop1")(shared)
    shared = layers.Conv1D(n_out, 3, padding='same', name="shared_conv2")(shared)
    shared = layers.LayerNormalization(name="shared_norm2")(shared)
    shared = layers.ReLU(name="shared_relu2")(shared)

    # Waveform decoder
    wav = layers.UpSampling1D(2, name="waveform_up1")(shared)
    wav = layers.SeparableConv1D(n_out, 50,  padding='same', name="waveform_conv1")(wav)
    wav = layers.LayerNormalization(name="waveform_norm1")(wav)
    wav = layers.ReLU(name="waveform_relu1")(wav)
    wav = layers.UpSampling1D(2, name="waveform_up2")(wav)
    wav = layers.SeparableConv1D(n_out, 75,  padding='same', name="waveform_conv2")(wav)
    wav = layers.LayerNormalization(name="waveform_norm2")(wav)
    wav = layers.ReLU(name="waveform_relu2")(wav)
    wav = layers.UpSampling1D(2, name="waveform_up3")(wav)
    wav = layers.SeparableConv1D(n_out, 150, padding='same', name="waveform_conv3")(wav)
    wav = layers.LayerNormalization(name="waveform_norm3")(wav)
    wav = layers.ReLU(name="waveform_relu3")(wav)
    waveform_output = layers.Conv1D(1, 1, padding='same', activation='linear', name="waveform")(wav)

    # RR decoder
    rr = layers.GlobalAveragePooling1D(name="rr_gap")(shared)
    rr = layers.Dense(32, activation='relu', name="rr_dense1")(rr)
    rr = layers.Dropout(0.3, name="rr_drop1")(rr)
    rr = layers.Dense(16, activation='relu', name="rr_dense2")(rr)
    rr = layers.Dropout(0.2, name="rr_drop2")(rr)
    rr_output = layers.Dense(1, activation='sigmoid', name="rr")(rr)

    model = models.Model(inputs=inputs, outputs=[waveform_output, rr_output],
                         name="LateFusion_DualTask")
    return model


TRAIN_CONFIG = {
    "optimizer"          : "Adam",
    "learning_rate"      : 1e-3,
    "clipnorm"           : 1.0,
    "loss"               : "Huber(delta=0.1)",
    "loss_weights"       : {"waveform": 1.0, "rr": 1.0},
    "epochs"             : 100,
    "batch_size"         : 32,
    "early_stop_patience": 15,
    "lr_reduce_factor"   : 0.5,
    "lr_reduce_patience" : 7,
    "min_lr"             : 1e-7,
    "finetune_lr"        : 1e-3,
    "finetune_epochs"    : 100,
}
