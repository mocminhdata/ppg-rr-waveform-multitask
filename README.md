# ppg-rr-waveform-multitask
# A Late Fusion Multi-Task Learning for Respiratory Waveform and Rate Estimation from Photoplethysmography

**Nhut Minh Ho¹, Kien Trong Nguyen¹***

¹ Posts and Telecommunications Institute of Technology, Ho Chi Minh City, Vietnam  
\* ntkien@ptit.edu.vn

## Abstract

Continuous respiratory monitoring enables early detection of physiological deterioration, yet conventional capnography remains impractical for prolonged use. Photoplethysmography (PPG) offers a non-invasive alternative that encodes respiratory information through baseline wander (respiratory-induced intensity variation; RIIV), amplitude modulation (respiratory-induced amplitude variation; RIAV), and frequency modulation (respiratory-induced frequency variation; RIFV) of the pulsatile waveform. Although prior work has used these modulations as inputs to deep learning models for respiratory rate estimation, existing approaches are limited to single-task architectures and have not jointly addressed waveform reconstruction. We propose a late fusion multi-task framework in which dedicated encoder branches independently process each modulation before fusion, and dual decoders simultaneously reconstruct the respiratory waveform and estimate the respiratory rate. Five training strategies (i.e., single dataset, combined, and bidirectional transfer learning) were crossed with two ground truth filtering conditions, yielding 10 experimental conditions evaluated on the CapnoBase and BIDMC benchmarks. Under the best-performing transfer learning configuration with bandpass-filtered ground truth, the model achieved respiratory rate MAE of 2.27 bpm (r = 0.819) on CapnoBase and 1.33 bpm (r = 0.417) on BIDMC, with waveform reconstruction MAE of 19.00% (r = 0.662) and 20.90% (r = 0.591) on the corresponding datasets. Combined training, in which data from both datasets were pooled, degraded both waveform and rate performance. These results demonstrate that multi-task learning can jointly deliver respiratory waveform and rate from short PPG windows while highlighting the importance of matching training strategy to reference signal characteristics.
