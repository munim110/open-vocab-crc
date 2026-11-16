# Repeated-split calibrated sets from the headroom probe

2000 ADE validation images (development data; 0 without a source-labelled sampled pixel excluded), 150 source labels, 500 random splits per design; thresholds by image-level CRC on the calibration part, everything reported on the rest. Projective arms calibrate once at the source labels. Nothing is fitted; the confirmation reserve is untouched.

## 200 calibration / 1800 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 9.45 | 1.00 | 29.6 | 4.34 [3.47, 5.31] | 5.67 [4.50, 6.97] | 7.58 [5.88, 9.49] | 12.80 [9.64, 16.36] | 14.55 [10.85, 18.76] |
| catseg_native_source | 9.48 | 1.03 | 29.2 | 3.39 [2.75, 4.11] |  |  |  |  |
| catseg_native_frozen_full | 13.25 | 1.40 | 99.8 |  |  |  |  | 5.53 [4.27, 6.97] |
| catseg_native_replay_full | 9.45 | 1.12 | 28.0 |  |  |  |  | 8.88 [6.55, 11.93] |

## 200 calibration / 1800 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 4.51 | 0.75 | 25.4 | 10.65 [7.52, 15.29] | 14.03 [9.90, 20.12] | 19.94 [13.80, 29.01] | 36.44 [24.55, 54.18] | 42.99 [28.56, 64.66] |
| catseg_native_source | 4.51 | 0.77 | 25.8 | 8.89 [5.66, 13.02] |  |  |  |  |
| catseg_native_frozen_full | 6.22 | 1.09 | 90.2 |  |  |  |  | 17.68 [10.25, 27.84] |
| catseg_native_replay_full | 4.52 | 0.80 | 27.4 |  |  |  |  | 31.15 [17.59, 50.53] |

## 1000 calibration / 1000 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 9.87 | 0.61 | 41.2 | 4.11 [3.82, 4.42] | 5.36 [4.96, 5.78] | 7.13 [6.53, 7.79] | 11.96 [10.87, 13.14] | 13.56 [12.26, 14.92] |
| catseg_native_source | 9.85 | 0.61 | 37.2 | 3.22 [3.03, 3.42] |  |  |  |  |
| catseg_native_frozen_full | 13.76 | 0.76 | 100.0 |  |  |  |  | 5.19 [4.81, 5.56] |
| catseg_native_replay_full | 9.87 | 0.64 | 41.4 |  |  |  |  | 8.18 [7.47, 8.94] |

## 1000 calibration / 1000 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 4.86 | 0.48 | 37.6 | 9.37 [8.32, 10.75] | 12.35 [10.96, 14.20] | 17.46 [15.37, 20.28] | 31.60 [27.53, 37.06] | 37.08 [32.18, 43.71] |
| catseg_native_source | 4.88 | 0.45 | 35.0 | 7.60 [6.63, 8.65] |  |  |  |  |
| catseg_native_frozen_full | 6.76 | 0.61 | 99.8 |  |  |  |  | 14.53 [12.31, 16.99] |
| catseg_native_replay_full | 4.89 | 0.49 | 40.2 |  |  |  |  | 25.65 [21.26, 30.26] |

Brackets are the 2.5-97.5% range of the evaluation mean across splits (splits overlap, so this is spread, not a confidence interval). CRC controls the mean risk over splits; individual splits may exceed alpha. catseg_native_frozen_full reuses the threshold calibrated under the source vocabulary after all labels are added; catseg_native_replay_full recalibrates under the full vocabulary. Stored scores are float16 logits clamped to [-30, 30].