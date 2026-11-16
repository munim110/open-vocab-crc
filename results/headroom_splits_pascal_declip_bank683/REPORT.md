# Repeated-split calibrated sets from the headroom probe

2000 Pascal Context validation images (development data; 0 without a source-labelled sampled pixel excluded), 59 source labels, 500 random splits per design; thresholds by image-level CRC on the calibration part, everything reported on the rest. Projective arms calibrate once at the source labels. Nothing is fitted; the confirmation reserve is untouched.

## 200 calibration / 1800 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +399 |
|---|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 9.62 | 1.21 | 35.0 | 1.53 [1.39, 1.67] | 1.65 [1.49, 1.81] | 1.84 [1.63, 2.05] | 2.48 [2.12, 2.83] |
| catseg_native_source | 9.63 | 1.14 | 36.6 | 1.39 [1.27, 1.55] |  |  |  |
| catseg_native_frozen_full | 14.44 | 1.28 | 100.0 |  |  |  | 1.53 [1.35, 1.78] |
| catseg_native_replay_full | 9.61 | 1.16 | 35.6 |  |  |  | 2.15 [1.81, 2.54] |

## 200 calibration / 1800 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +399 |
|---|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 4.59 | 0.85 | 28.2 | 2.07 [1.82, 2.37] | 2.29 [1.98, 2.65] | 2.71 [2.29, 3.21] | 4.08 [3.27, 5.10] |
| catseg_native_source | 4.58 | 0.79 | 28.0 | 1.96 [1.71, 2.27] |  |  |  |
| catseg_native_frozen_full | 7.95 | 1.16 | 99.8 |  |  |  | 2.50 [2.05, 3.05] |
| catseg_native_replay_full | 4.58 | 0.83 | 32.0 |  |  |  | 3.82 [3.06, 4.97] |

## 1000 calibration / 1000 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +399 |
|---|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 9.83 | 0.74 | 39.8 | 1.51 [1.46, 1.56] | 1.62 [1.57, 1.68] | 1.81 [1.73, 1.88] | 2.42 [2.30, 2.54] |
| catseg_native_source | 9.86 | 0.71 | 42.0 | 1.37 [1.33, 1.41] |  |  |  |
| catseg_native_frozen_full | 14.69 | 0.80 | 100.0 |  |  |  | 1.50 [1.44, 1.56] |
| catseg_native_replay_full | 9.84 | 0.71 | 39.2 |  |  |  | 2.09 [1.98, 2.20] |

## 1000 calibration / 1000 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +399 |
|---|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 4.87 | 0.53 | 40.4 | 2.00 [1.92, 2.09] | 2.21 [2.11, 2.31] | 2.59 [2.45, 2.73] | 3.85 [3.59, 4.13] |
| catseg_native_source | 4.88 | 0.52 | 42.0 | 1.89 [1.80, 1.98] |  |  |  |
| catseg_native_frozen_full | 8.43 | 0.68 | 100.0 |  |  |  | 2.36 [2.21, 2.54] |
| catseg_native_replay_full | 4.88 | 0.53 | 40.4 |  |  |  | 3.58 [3.33, 3.87] |

Brackets are the 2.5-97.5% range of the evaluation mean across splits (splits overlap, so this is spread, not a confidence interval). CRC controls the mean risk over splits; individual splits may exceed alpha. catseg_native_frozen_full reuses the threshold calibrated under the source vocabulary after all labels are added; catseg_native_replay_full recalibrates under the full vocabulary. Stored scores are float16 logits clamped to [-30, 30].