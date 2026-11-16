# Repeated-split calibrated sets from the headroom probe

2000 Pascal Context validation images (development data; 0 without a source-labelled sampled pixel excluded), 59 source labels, 500 random splits per design; thresholds by image-level CRC on the calibration part, everything reported on the rest. Projective arms calibrate once at the source labels. Nothing is fitted; the confirmation reserve is untouched.

## 200 calibration / 1800 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +399 |
|---|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 9.65 | 1.20 | 37.6 | 1.53 [1.40, 1.66] | 1.63 [1.48, 1.78] | 1.81 [1.62, 2.00] | 2.38 [2.07, 2.71] |
| catseg_native_source | 9.64 | 1.11 | 37.4 | 1.38 [1.27, 1.52] |  |  |  |
| catseg_native_frozen_full | 14.76 | 1.32 | 100.0 |  |  |  | 1.52 [1.35, 1.73] |
| catseg_native_replay_full | 9.63 | 1.14 | 38.8 |  |  |  | 2.12 [1.79, 2.46] |

## 200 calibration / 1800 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +399 |
|---|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 4.60 | 0.84 | 32.2 | 2.06 [1.84, 2.36] | 2.24 [1.98, 2.60] | 2.63 [2.28, 3.13] | 3.87 [3.20, 4.84] |
| catseg_native_source | 4.58 | 0.80 | 29.0 | 1.94 [1.71, 2.21] |  |  |  |
| catseg_native_frozen_full | 8.06 | 1.14 | 99.6 |  |  |  | 2.42 [2.04, 2.89] |
| catseg_native_replay_full | 4.58 | 0.81 | 29.2 |  |  |  | 3.60 [2.92, 4.60] |

## 1000 calibration / 1000 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +399 |
|---|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 9.82 | 0.73 | 40.4 | 1.51 [1.46, 1.56] | 1.61 [1.55, 1.66] | 1.78 [1.72, 1.85] | 2.34 [2.23, 2.44] |
| catseg_native_source | 9.85 | 0.70 | 38.8 | 1.37 [1.33, 1.41] |  |  |  |
| catseg_native_frozen_full | 15.03 | 0.81 | 100.0 |  |  |  | 1.49 [1.42, 1.55] |
| catseg_native_replay_full | 9.86 | 0.72 | 43.2 |  |  |  | 2.07 [1.96, 2.17] |

## 1000 calibration / 1000 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +399 |
|---|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 4.87 | 0.51 | 39.2 | 2.00 [1.91, 2.08] | 2.16 [2.07, 2.27] | 2.53 [2.40, 2.66] | 3.66 [3.43, 3.92] |
| catseg_native_source | 4.88 | 0.51 | 40.8 | 1.87 [1.80, 1.95] |  |  |  |
| catseg_native_frozen_full | 8.54 | 0.67 | 100.0 |  |  |  | 2.30 [2.17, 2.44] |
| catseg_native_replay_full | 4.88 | 0.50 | 41.6 |  |  |  | 3.38 [3.15, 3.61] |

Brackets are the 2.5-97.5% range of the evaluation mean across splits (splits overlap, so this is spread, not a confidence interval). CRC controls the mean risk over splits; individual splits may exceed alpha. catseg_native_frozen_full reuses the threshold calibrated under the source vocabulary after all labels are added; catseg_native_replay_full recalibrates under the full vocabulary. Stored scores are float16 logits clamped to [-30, 30].