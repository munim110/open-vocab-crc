# Repeated-split calibrated sets from the headroom probe

2000 ADE validation images (development data; 0 without a source-labelled sampled pixel excluded), 150 source labels, 500 random splits per design; thresholds by image-level CRC on the calibration part, everything reported on the rest. Projective arms calibrate once at the source labels. Nothing is fitted; the confirmation reserve is untouched.

## 200 calibration / 1800 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 9.45 | 1.02 | 30.0 | 2.56 [2.28, 2.92] | 2.95 [2.60, 3.39] | 3.50 [3.04, 4.09] | 4.99 [4.23, 5.98] | 5.33 [4.50, 6.43] |
| catseg_native_source | 9.50 | 0.98 | 30.0 | 1.97 [1.74, 2.24] |  |  |  |  |
| catseg_native_frozen_full | 14.71 | 1.24 | 100.0 |  |  |  |  | 2.25 [1.94, 2.63] |
| catseg_native_replay_full | 9.50 | 1.10 | 31.0 |  |  |  |  | 3.68 [2.97, 4.70] |

## 200 calibration / 1800 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 4.49 | 0.72 | 26.0 | 4.09 [3.52, 4.79] | 4.88 [4.14, 5.78] | 6.15 [5.13, 7.41] | 9.52 [7.76, 11.71] | 10.43 [8.43, 12.94] |
| catseg_native_source | 4.51 | 0.73 | 25.6 | 3.54 [2.83, 4.35] |  |  |  |  |
| catseg_native_frozen_full | 7.81 | 1.06 | 100.0 |  |  |  |  | 4.64 [3.50, 5.99] |
| catseg_native_replay_full | 4.51 | 0.81 | 27.2 |  |  |  |  | 8.81 [6.20, 12.84] |

## 1000 calibration / 1000 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 9.86 | 0.65 | 40.2 | 2.48 [2.38, 2.59] | 2.84 [2.72, 2.97] | 3.36 [3.20, 3.53] | 4.76 [4.49, 5.05] | 5.08 [4.78, 5.39] |
| catseg_native_source | 9.91 | 0.64 | 40.8 | 1.91 [1.82, 1.99] |  |  |  |  |
| catseg_native_frozen_full | 15.23 | 0.80 | 100.0 |  |  |  |  | 2.16 [2.05, 2.28] |
| catseg_native_replay_full | 9.91 | 0.67 | 42.6 |  |  |  |  | 3.47 [3.23, 3.74] |

## 1000 calibration / 1000 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 4.89 | 0.46 | 40.6 | 3.87 [3.66, 4.07] | 4.59 [4.33, 4.85] | 5.75 [5.39, 6.12] | 8.83 [8.22, 9.47] | 9.64 [8.95, 10.38] |
| catseg_native_source | 4.89 | 0.48 | 39.6 | 3.28 [3.04, 3.54] |  |  |  |  |
| catseg_native_frozen_full | 8.38 | 0.65 | 100.0 |  |  |  |  | 4.21 [3.82, 4.63] |
| catseg_native_replay_full | 4.90 | 0.49 | 41.4 |  |  |  |  | 7.81 [7.03, 8.70] |

Brackets are the 2.5-97.5% range of the evaluation mean across splits (splits overlap, so this is spread, not a confidence interval). CRC controls the mean risk over splits; individual splits may exceed alpha. catseg_native_frozen_full reuses the threshold calibrated under the source vocabulary after all labels are added; catseg_native_replay_full recalibrates under the full vocabulary. Stored scores are float16 logits clamped to [-30, 30].