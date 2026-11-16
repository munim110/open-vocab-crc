# Repeated-split calibrated sets from the headroom probe

2000 ADE validation images (development data; 0 without a source-labelled sampled pixel excluded), 150 source labels, 500 random splits per design; thresholds by image-level CRC on the calibration part, everything reported on the rest. Projective arms calibrate once at the source labels. Nothing is fitted; the confirmation reserve is untouched.

## 200 calibration / 1800 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 9.48 | 1.05 | 33.0 | 3.26 [2.79, 3.85] | 3.81 [3.21, 4.57] | 4.58 [3.78, 5.62] | 6.92 [5.56, 8.69] | 7.44 [5.94, 9.39] |
| catseg_native_source | 9.50 | 1.02 | 32.2 | 2.99 [2.58, 3.49] |  |  |  |  |
| catseg_native_frozen_full | 10.78 | 1.02 | 75.2 |  |  |  |  | 4.81 [3.98, 5.85] |
| catseg_native_replay_full | 9.51 | 1.07 | 34.2 |  |  |  |  | 5.62 [4.45, 7.12] |

## 200 calibration / 1800 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 4.49 | 0.72 | 23.6 | 6.16 [4.91, 7.48] | 7.58 [5.94, 9.33] | 9.88 [7.53, 12.40] | 16.13 [12.01, 20.57] | 17.83 [13.14, 22.92] |
| catseg_native_source | 4.48 | 0.72 | 23.6 | 5.62 [4.47, 6.94] |  |  |  |  |
| catseg_native_frozen_full | 5.74 | 0.71 | 84.2 |  |  |  |  | 10.77 [8.06, 14.01] |
| catseg_native_replay_full | 4.49 | 0.75 | 23.8 |  |  |  |  | 15.23 [10.25, 21.42] |

## 1000 calibration / 1000 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 9.87 | 0.64 | 43.0 | 3.13 [2.96, 3.31] | 3.64 [3.44, 3.87] | 4.36 [4.09, 4.66] | 6.54 [6.07, 7.04] | 7.01 [6.49, 7.56] |
| catseg_native_source | 9.87 | 0.62 | 40.2 | 2.88 [2.74, 3.02] |  |  |  |  |
| catseg_native_frozen_full | 11.15 | 0.64 | 96.8 |  |  |  |  | 4.59 [4.31, 4.87] |
| catseg_native_replay_full | 9.88 | 0.65 | 38.8 |  |  |  |  | 5.31 [4.93, 5.68] |

## 1000 calibration / 1000 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 4.88 | 0.48 | 40.8 | 5.72 [5.28, 6.19] | 7.00 [6.42, 7.61] | 9.05 [8.21, 9.90] | 14.66 [13.20, 16.15] | 16.15 [14.51, 17.85] |
| catseg_native_source | 4.89 | 0.48 | 40.2 | 5.17 [4.78, 5.61] |  |  |  |  |
| catseg_native_frozen_full | 6.14 | 0.50 | 98.6 |  |  |  |  | 9.68 [8.76, 10.72] |
| catseg_native_replay_full | 4.89 | 0.49 | 40.4 |  |  |  |  | 13.23 [11.64, 15.16] |

Brackets are the 2.5-97.5% range of the evaluation mean across splits (splits overlap, so this is spread, not a confidence interval). CRC controls the mean risk over splits; individual splits may exceed alpha. catseg_native_frozen_full reuses the threshold calibrated under the source vocabulary after all labels are added; catseg_native_replay_full recalibrates under the full vocabulary. Stored scores are float16 logits clamped to [-30, 30].