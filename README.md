**Minh Nhut Ho¹, Kien Trong Nguyen¹**

¹ Posts and Telecommunications Institute of Technology, Ho Chi Minh City, Vietnam  


## Datasets

This study uses two publicly available benchmark datasets. Both are segmented into non-overlapping 9.6-second windows, and data partitioning is performed at the subject level (5 subjects held out for testing per dataset).

### CapnoBase

- **Source:** W. Karlen, *CapnoBase IEEE TBME Respiratory Rate Benchmark*, 2021. [https://doi.org/10.5683/SP2/NLB8IT](https://doi.org/10.5683/SP2/NLB8IT)
- **Subjects:** 42 (29 pediatric, 13 adult), recorded during elective surgery
- **Signals:** PPG and capnography (end-tidal CO₂), sampled at 300 Hz
- **Recording duration:** 8 min per subject
- **Respiratory rate range:** 5–48 brpm (mean 15.1, median 11.7)
- **Train/Test split:** 37 / 5

### BIDMC
- **Source:** Pimentel et al., *Towards a Robust Estimation of Respiratory Rate from Pulse Oximeters*, IEEE Trans. Biomed. Eng., 64(8), 2017. [https://physionet.org/content/bidmc/1.0.0/](https://physionet.org/content/bidmc/1.0.0/)
- **Subjects:** 53 adult ICU patients; 1 excluded (bidmc_13, >75% missing annotations) → 52 used
- **Signals:** PPG and impedance pneumography, sampled at 125 Hz
- **Recording duration:** 8 min per subject
- **Respiratory rate range:** 5–34 brpm (mean 17.7, median 18.0)
- **Train/Test split:** 47 / 5

### Test set subjects

| Dataset    | Test subject IDs |
|:-----------|:-----------------|
| CapnoBase  | `['0330', '0331', '0332', '0333', 0370']` |
| BIDMC      | `['49', '50', '51', '52', '53']` |
