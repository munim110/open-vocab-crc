# Repeated-split calibrated sets from the headroom probe

2000 ADE validation images (development data; 0 without a source-labelled sampled pixel excluded), 150 source labels, 500 random splits per design; thresholds by image-level CRC on the calibration part, everything reported on the rest. Projective arms calibrate once at the source labels. Nothing is fitted; the confirmation reserve is untouched.

## 200 calibration / 1800 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 9.43 | 1.06 | 28.6 | 4.01 [3.28, 4.95] | 5.10 [4.14, 6.34] | 6.54 [5.21, 8.26] | 10.44 [8.11, 13.47] | 11.61 [8.94, 15.12] |
| catseg_native_source | 9.48 | 1.03 | 29.2 | 3.39 [2.75, 4.11] |  |  |  |  |
| catseg_native_frozen_full | 13.25 | 1.40 | 99.8 |  |  |  |  | 5.53 [4.27, 6.97] |
| catseg_native_replay_full | 9.45 | 1.12 | 28.0 |  |  |  |  | 8.88 [6.55, 11.93] |

## 200 calibration / 1800 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 4.50 | 0.76 | 26.6 | 10.27 [6.88, 16.33] | 13.25 [8.86, 21.07] | 18.20 [11.86, 29.54] | 31.63 [19.95, 52.87] | 36.57 [22.66, 62.14] |
| catseg_native_source | 4.51 | 0.77 | 25.8 | 8.89 [5.66, 13.02] |  |  |  |  |
| catseg_native_frozen_full | 6.22 | 1.09 | 90.2 |  |  |  |  | 17.68 [10.25, 27.84] |
| catseg_native_replay_full | 4.52 | 0.80 | 27.4 |  |  |  |  | 31.15 [17.59, 50.53] |

## 1000 calibration / 1000 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 9.86 | 0.61 | 35.0 | 3.80 [3.55, 4.02] | 4.83 [4.50, 5.12] | 6.16 [5.70, 6.58] | 9.77 [9.01, 10.51] | 10.83 [9.98, 11.68] |
| catseg_native_source | 9.85 | 0.61 | 37.2 | 3.22 [3.03, 3.42] |  |  |  |  |
| catseg_native_frozen_full | 13.76 | 0.76 | 100.0 |  |  |  |  | 5.19 [4.81, 5.56] |
| catseg_native_replay_full | 9.87 | 0.64 | 41.4 |  |  |  |  | 8.18 [7.47, 8.94] |

## 1000 calibration / 1000 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 4.87 | 0.49 | 37.4 | 8.69 [7.71, 10.03] | 11.20 [9.93, 12.92] | 15.24 [13.35, 17.74] | 26.14 [22.74, 30.73] | 29.99 [25.98, 35.45] |
| catseg_native_source | 4.88 | 0.45 | 35.0 | 7.60 [6.63, 8.65] |  |  |  |  |
| catseg_native_frozen_full | 6.76 | 0.61 | 99.8 |  |  |  |  | 14.53 [12.31, 16.99] |
| catseg_native_replay_full | 4.89 | 0.49 | 40.2 |  |  |  |  | 25.65 [21.26, 30.26] |

Brackets are the 2.5-97.5% range of the evaluation mean across splits (splits overlap, so this is spread, not a confidence interval). CRC controls the mean risk over splits; individual splits may exceed alpha. catseg_native_frozen_full reuses the threshold calibrated under the source vocabulary after all labels are added; catseg_native_replay_full recalibrates under the full vocabulary. Stored scores are float16 logits clamped to [-30, 30].