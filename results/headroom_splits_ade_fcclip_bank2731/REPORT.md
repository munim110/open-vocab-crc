# Repeated-split calibrated sets from the headroom probe

2000 ADE validation images (development data; 0 without a source-labelled sampled pixel excluded), 150 source labels, 500 random splits per design; thresholds by image-level CRC on the calibration part, everything reported on the rest. Projective arms calibrate once at the source labels. Nothing is fitted; the confirmation reserve is untouched.

## 200 calibration / 1800 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 9.44 | 1.06 | 29.8 | 4.09 [3.32, 5.02] | 5.18 [4.17, 6.39] | 6.58 [5.19, 8.25] | 10.42 [8.02, 13.36] | 11.56 [8.81, 14.94] |
| catseg_native_source | 9.48 | 1.03 | 29.2 | 3.39 [2.75, 4.11] |  |  |  |  |
| catseg_native_frozen_full | 13.25 | 1.40 | 99.8 |  |  |  |  | 5.53 [4.27, 6.97] |
| catseg_native_replay_full | 9.45 | 1.12 | 28.0 |  |  |  |  | 8.88 [6.55, 11.93] |

## 200 calibration / 1800 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 4.51 | 0.76 | 25.2 | 10.51 [7.00, 16.64] | 13.46 [8.93, 21.34] | 18.34 [11.85, 29.71] | 31.53 [19.73, 52.56] | 36.34 [22.35, 61.56] |
| catseg_native_source | 4.51 | 0.77 | 25.8 | 8.89 [5.66, 13.02] |  |  |  |  |
| catseg_native_frozen_full | 6.22 | 1.09 | 90.2 |  |  |  |  | 17.68 [10.25, 27.84] |
| catseg_native_replay_full | 4.52 | 0.80 | 27.4 |  |  |  |  | 31.15 [17.59, 50.53] |

## 1000 calibration / 1000 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 9.87 | 0.61 | 40.0 | 3.85 [3.61, 4.10] | 4.87 [4.56, 5.20] | 6.15 [5.71, 6.63] | 9.69 [8.95, 10.50] | 10.71 [9.88, 11.65] |
| catseg_native_source | 9.85 | 0.61 | 37.2 | 3.22 [3.03, 3.42] |  |  |  |  |
| catseg_native_frozen_full | 13.76 | 0.76 | 100.0 |  |  |  |  | 5.19 [4.81, 5.56] |
| catseg_native_replay_full | 9.87 | 0.64 | 41.4 |  |  |  |  | 8.18 [7.47, 8.94] |

## 1000 calibration / 1000 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 4.87 | 0.49 | 38.0 | 8.90 [7.64, 10.50] | 11.39 [9.77, 13.42] | 15.36 [13.04, 18.28] | 26.06 [21.91, 31.42] | 29.82 [24.91, 36.20] |
| catseg_native_source | 4.88 | 0.45 | 35.0 | 7.60 [6.63, 8.65] |  |  |  |  |
| catseg_native_frozen_full | 6.76 | 0.61 | 99.8 |  |  |  |  | 14.53 [12.31, 16.99] |
| catseg_native_replay_full | 4.89 | 0.49 | 40.2 |  |  |  |  | 25.65 [21.26, 30.26] |

Brackets are the 2.5-97.5% range of the evaluation mean across splits (splits overlap, so this is spread, not a confidence interval). CRC controls the mean risk over splits; individual splits may exceed alpha. catseg_native_frozen_full reuses the threshold calibrated under the source vocabulary after all labels are added; catseg_native_replay_full recalibrates under the full vocabulary. Stored scores are float16 logits clamped to [-30, 30].