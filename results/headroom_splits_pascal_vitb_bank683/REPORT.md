# Repeated-split calibrated sets from the headroom probe

2000 Pascal Context validation images (development data; 0 without a source-labelled sampled pixel excluded), 59 source labels, 500 random splits per design; thresholds by image-level CRC on the calibration part, everything reported on the rest. Projective arms calibrate once at the source labels. Nothing is fitted; the confirmation reserve is untouched.

## 200 calibration / 1800 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +399 |
|---|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 9.60 | 1.18 | 32.4 | 1.69 [1.53, 1.87] | 1.82 [1.63, 2.02] | 2.08 [1.82, 2.35] | 2.90 [2.44, 3.41] |
| catseg_native_source | 9.62 | 1.14 | 37.2 | 1.52 [1.37, 1.71] |  |  |  |
| catseg_native_frozen_full | 14.83 | 1.41 | 100.0 |  |  |  | 1.69 [1.45, 2.00] |
| catseg_native_replay_full | 9.63 | 1.14 | 38.4 |  |  |  | 2.61 [2.16, 3.14] |

## 200 calibration / 1800 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +399 |
|---|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 4.59 | 0.85 | 30.4 | 2.39 [2.07, 2.79] | 2.66 [2.28, 3.16] | 3.26 [2.71, 4.02] | 5.28 [4.13, 6.92] |
| catseg_native_source | 4.59 | 0.80 | 30.8 | 2.27 [1.96, 2.65] |  |  |  |
| catseg_native_frozen_full | 7.97 | 1.14 | 99.4 |  |  |  | 3.13 [2.49, 3.93] |
| catseg_native_replay_full | 4.59 | 0.81 | 29.8 |  |  |  | 4.99 [3.98, 6.52] |

## 1000 calibration / 1000 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +399 |
|---|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 9.83 | 0.72 | 41.6 | 1.67 [1.61, 1.73] | 1.79 [1.72, 1.86] | 2.04 [1.95, 2.13] | 2.82 [2.66, 2.98] |
| catseg_native_source | 9.87 | 0.71 | 40.2 | 1.49 [1.44, 1.55] |  |  |  |
| catseg_native_frozen_full | 15.17 | 0.84 | 100.0 |  |  |  | 1.63 [1.55, 1.73] |
| catseg_native_replay_full | 9.87 | 0.72 | 46.2 |  |  |  | 2.52 [2.36, 2.69] |

## 1000 calibration / 1000 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +399 |
|---|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 4.86 | 0.53 | 37.6 | 2.30 [2.20, 2.41] | 2.55 [2.42, 2.68] | 3.11 [2.92, 3.30] | 4.95 [4.54, 5.36] |
| catseg_native_source | 4.88 | 0.53 | 41.4 | 2.19 [2.08, 2.30] |  |  |  |
| catseg_native_frozen_full | 8.39 | 0.68 | 100.0 |  |  |  | 2.94 [2.71, 3.18] |
| catseg_native_replay_full | 4.88 | 0.52 | 42.2 |  |  |  | 4.66 [4.32, 5.05] |

Brackets are the 2.5-97.5% range of the evaluation mean across splits (splits overlap, so this is spread, not a confidence interval). CRC controls the mean risk over splits; individual splits may exceed alpha. catseg_native_frozen_full reuses the threshold calibrated under the source vocabulary after all labels are added; catseg_native_replay_full recalibrates under the full vocabulary. Stored scores are float16 logits clamped to [-30, 30].