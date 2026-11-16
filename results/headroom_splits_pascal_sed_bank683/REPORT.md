# Repeated-split calibrated sets from the headroom probe

2000 Pascal Context validation images (development data; 0 without a source-labelled sampled pixel excluded), 59 source labels, 500 random splits per design; thresholds by image-level CRC on the calibration part, everything reported on the rest. Projective arms calibrate once at the source labels. Nothing is fitted; the confirmation reserve is untouched.

## 200 calibration / 1800 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +399 |
|---|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 9.60 | 1.20 | 36.4 | 1.70 [1.53, 1.89] | 1.79 [1.60, 2.00] | 2.05 [1.80, 2.33] | 2.89 [2.43, 3.41] |
| catseg_native_source | 9.64 | 1.17 | 35.4 | 1.55 [1.38, 1.75] |  |  |  |
| catseg_native_frozen_full | 4.53 | 0.65 | 0.0 |  |  |  | 4.94 [4.10, 5.97] |
| catseg_native_replay_full | 9.62 | 1.16 | 35.4 |  |  |  | 2.75 [2.29, 3.26] |

## 200 calibration / 1800 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +399 |
|---|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 4.63 | 0.86 | 33.8 | 2.41 [2.11, 2.83] | 2.59 [2.24, 3.09] | 3.14 [2.65, 3.85] | 5.04 [4.06, 6.46] |
| catseg_native_source | 4.62 | 0.79 | 28.4 | 2.28 [1.98, 2.66] |  |  |  |
| catseg_native_frozen_full | 1.95 | 0.37 | 0.0 |  |  |  | 8.91 [7.18, 11.22] |
| catseg_native_replay_full | 4.61 | 0.85 | 32.6 |  |  |  | 4.90 [3.94, 6.32] |

## 1000 calibration / 1000 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +399 |
|---|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 9.85 | 0.69 | 41.2 | 1.67 [1.61, 1.73] | 1.76 [1.69, 1.82] | 2.01 [1.92, 2.09] | 2.80 [2.64, 2.95] |
| catseg_native_source | 9.85 | 0.70 | 40.8 | 1.53 [1.47, 1.58] |  |  |  |
| catseg_native_frozen_full | 4.62 | 0.42 | 0.0 |  |  |  | 4.80 [4.54, 5.08] |
| catseg_native_replay_full | 9.83 | 0.72 | 42.6 |  |  |  | 2.68 [2.51, 2.83] |

## 1000 calibration / 1000 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +399 |
|---|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 4.86 | 0.50 | 36.0 | 2.33 [2.23, 2.46] | 2.50 [2.39, 2.63] | 3.01 [2.86, 3.20] | 4.77 [4.45, 5.14] |
| catseg_native_source | 4.87 | 0.50 | 38.2 | 2.20 [2.10, 2.31] |  |  |  |
| catseg_native_frozen_full | 2.05 | 0.27 | 0.0 |  |  |  | 8.45 [7.90, 9.10] |
| catseg_native_replay_full | 4.86 | 0.52 | 42.0 |  |  |  | 4.63 [4.30, 4.99] |

Brackets are the 2.5-97.5% range of the evaluation mean across splits (splits overlap, so this is spread, not a confidence interval). CRC controls the mean risk over splits; individual splits may exceed alpha. catseg_native_frozen_full reuses the threshold calibrated under the source vocabulary after all labels are added; catseg_native_replay_full recalibrates under the full vocabulary. Stored scores are float16 logits clamped to [-30, 30].