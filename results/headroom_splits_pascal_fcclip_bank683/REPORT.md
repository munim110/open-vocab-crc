# Repeated-split calibrated sets from the headroom probe

2000 Pascal Context validation images (development data; 0 without a source-labelled sampled pixel excluded), 59 source labels, 500 random splits per design; thresholds by image-level CRC on the calibration part, everything reported on the rest. Projective arms calibrate once at the source labels. Nothing is fitted; the confirmation reserve is untouched.

## 200 calibration / 1800 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +399 |
|---|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 9.61 | 1.17 | 34.8 | 2.06 [1.82, 2.36] | 2.47 [2.10, 2.94] | 3.31 [2.69, 4.14] | 6.12 [4.67, 8.06] |
| catseg_native_source | 9.58 | 1.14 | 32.6 | 2.00 [1.72, 2.28] |  |  |  |
| catseg_native_frozen_full | 15.82 | 1.62 | 100.0 |  |  |  | 2.96 [2.30, 3.72] |
| catseg_native_replay_full | 9.60 | 1.16 | 32.0 |  |  |  | 5.58 [4.25, 7.30] |

## 200 calibration / 1800 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +399 |
|---|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 4.57 | 0.80 | 27.8 | 3.30 [2.72, 3.97] | 4.60 [3.54, 5.83] | 7.24 [5.25, 9.57] | 15.38 [10.65, 20.91] |
| catseg_native_source | 4.59 | 0.80 | 28.2 | 3.32 [2.67, 4.23] |  |  |  |
| catseg_native_frozen_full | 8.06 | 1.27 | 99.8 |  |  |  | 7.06 [4.88, 10.47] |
| catseg_native_replay_full | 4.57 | 0.80 | 27.6 |  |  |  | 14.32 [9.88, 21.01] |

## 1000 calibration / 1000 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +399 |
|---|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 9.86 | 0.71 | 40.6 | 2.01 [1.92, 2.11] | 2.39 [2.25, 2.54] | 3.17 [2.94, 3.42] | 5.80 [5.28, 6.39] |
| catseg_native_source | 9.86 | 0.73 | 40.6 | 1.95 [1.85, 2.04] |  |  |  |
| catseg_native_frozen_full | 16.22 | 0.96 | 100.0 |  |  |  | 2.82 [2.59, 3.05] |
| catseg_native_replay_full | 9.86 | 0.74 | 40.2 |  |  |  | 5.30 [4.87, 5.80] |

## 1000 calibration / 1000 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +399 |
|---|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 4.87 | 0.53 | 38.6 | 3.14 [2.95, 3.36] | 4.28 [3.95, 4.67] | 6.65 [6.00, 7.42] | 13.99 [12.41, 15.84] |
| catseg_native_source | 4.88 | 0.52 | 36.0 | 3.13 [2.90, 3.36] |  |  |  |
| catseg_native_frozen_full | 8.55 | 0.71 | 100.0 |  |  |  | 6.37 [5.56, 7.15] |
| catseg_native_replay_full | 4.87 | 0.51 | 40.2 |  |  |  | 12.77 [11.29, 14.39] |

Brackets are the 2.5-97.5% range of the evaluation mean across splits (splits overlap, so this is spread, not a confidence interval). CRC controls the mean risk over splits; individual splits may exceed alpha. catseg_native_frozen_full reuses the threshold calibrated under the source vocabulary after all labels are added; catseg_native_replay_full recalibrates under the full vocabulary. Stored scores are float16 logits clamped to [-30, 30].