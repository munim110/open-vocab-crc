# Repeated-split calibrated sets from the headroom probe

2000 ADE validation images (development data; 0 without a source-labelled sampled pixel excluded), 150 source labels, 500 random splits per design; thresholds by image-level CRC on the calibration part, everything reported on the rest. Projective arms calibrate once at the source labels. Nothing is fitted; the confirmation reserve is untouched.

## 200 calibration / 1800 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 9.48 | 1.12 | 32.8 | 2.25 [1.97, 2.60] | 2.62 [2.27, 3.06] | 3.06 [2.60, 3.63] | 4.38 [3.62, 5.35] | 4.59 [3.78, 5.62] |
| catseg_native_source | 9.52 | 1.03 | 31.6 | 1.90 [1.67, 2.17] |  |  |  |  |
| catseg_native_frozen_full | 14.22 | 1.30 | 100.0 |  |  |  |  | 2.26 [1.89, 2.72] |
| catseg_native_replay_full | 9.53 | 1.13 | 33.4 |  |  |  |  | 3.58 [2.84, 4.53] |

## 200 calibration / 1800 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 4.50 | 0.76 | 24.6 | 3.82 [3.11, 4.84] | 4.61 [3.71, 5.93] | 5.77 [4.51, 7.63] | 9.11 [6.89, 12.51] | 9.76 [7.30, 13.56] |
| catseg_native_source | 4.52 | 0.74 | 25.4 | 3.35 [2.69, 4.19] |  |  |  |  |
| catseg_native_frozen_full | 7.38 | 1.07 | 99.4 |  |  |  |  | 4.83 [3.59, 6.46] |
| catseg_native_replay_full | 4.52 | 0.79 | 24.6 |  |  |  |  | 8.61 [6.06, 12.22] |

## 1000 calibration / 1000 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 9.87 | 0.71 | 42.2 | 2.18 [2.08, 2.28] | 2.53 [2.40, 2.66] | 2.94 [2.78, 3.10] | 4.19 [3.91, 4.45] | 4.38 [4.08, 4.66] |
| catseg_native_source | 9.88 | 0.65 | 41.4 | 1.84 [1.76, 1.92] |  |  |  |  |
| catseg_native_frozen_full | 14.70 | 0.78 | 100.0 |  |  |  |  | 2.17 [2.04, 2.29] |
| catseg_native_replay_full | 9.89 | 0.66 | 40.6 |  |  |  |  | 3.39 [3.14, 3.63] |

## 1000 calibration / 1000 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 4.89 | 0.49 | 37.6 | 3.54 [3.29, 3.81] | 4.25 [3.94, 4.60] | 5.26 [4.83, 5.73] | 8.19 [7.43, 9.02] | 8.74 [7.89, 9.64] |
| catseg_native_source | 4.89 | 0.47 | 38.6 | 3.10 [2.88, 3.32] |  |  |  |  |
| catseg_native_frozen_full | 7.95 | 0.62 | 100.0 |  |  |  |  | 4.35 [3.93, 4.77] |
| catseg_native_replay_full | 4.90 | 0.50 | 41.2 |  |  |  |  | 7.64 [6.82, 8.57] |

Brackets are the 2.5-97.5% range of the evaluation mean across splits (splits overlap, so this is spread, not a confidence interval). CRC controls the mean risk over splits; individual splits may exceed alpha. catseg_native_frozen_full reuses the threshold calibrated under the source vocabulary after all labels are added; catseg_native_replay_full recalibrates under the full vocabulary. Stored scores are float16 logits clamped to [-30, 30].