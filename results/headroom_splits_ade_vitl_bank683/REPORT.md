# Repeated-split calibrated sets from the headroom probe

2000 ADE validation images (development data; 0 without a source-labelled sampled pixel excluded), 150 source labels, 500 random splits per design; thresholds by image-level CRC on the calibration part, everything reported on the rest. Projective arms calibrate once at the source labels. Nothing is fitted; the confirmation reserve is untouched.

## 200 calibration / 1800 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 9.47 | 1.07 | 30.8 | 2.32 [2.04, 2.67] | 2.64 [2.29, 3.06] | 3.09 [2.63, 3.63] | 4.25 [3.53, 5.14] | 4.48 [3.70, 5.44] |
| catseg_native_source | 9.50 | 0.98 | 30.0 | 1.97 [1.74, 2.24] |  |  |  |  |
| catseg_native_frozen_full | 14.71 | 1.24 | 100.0 |  |  |  |  | 2.25 [1.94, 2.63] |
| catseg_native_replay_full | 9.50 | 1.10 | 31.0 |  |  |  |  | 3.68 [2.97, 4.70] |

## 200 calibration / 1800 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 4.49 | 0.76 | 26.2 | 3.96 [3.24, 4.93] | 4.68 [3.77, 5.91] | 5.84 [4.58, 7.55] | 8.91 [6.74, 11.92] | 9.68 [7.22, 13.13] |
| catseg_native_source | 4.51 | 0.73 | 25.6 | 3.54 [2.83, 4.35] |  |  |  |  |
| catseg_native_frozen_full | 7.81 | 1.06 | 100.0 |  |  |  |  | 4.64 [3.50, 5.99] |
| catseg_native_replay_full | 4.51 | 0.81 | 27.2 |  |  |  |  | 8.81 [6.20, 12.84] |

## 1000 calibration / 1000 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 9.90 | 0.68 | 42.0 | 2.25 [2.15, 2.36] | 2.55 [2.43, 2.68] | 2.97 [2.81, 3.13] | 4.06 [3.81, 4.32] | 4.27 [4.01, 4.55] |
| catseg_native_source | 9.91 | 0.64 | 40.8 | 1.91 [1.82, 1.99] |  |  |  |  |
| catseg_native_frozen_full | 15.23 | 0.80 | 100.0 |  |  |  |  | 2.16 [2.05, 2.28] |
| catseg_native_replay_full | 9.91 | 0.67 | 42.6 |  |  |  |  | 3.47 [3.23, 3.74] |

## 1000 calibration / 1000 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 4.89 | 0.49 | 41.4 | 3.66 [3.40, 3.95] | 4.30 [3.98, 4.65] | 5.31 [4.87, 5.80] | 7.99 [7.23, 8.84] | 8.63 [7.78, 9.60] |
| catseg_native_source | 4.89 | 0.48 | 39.6 | 3.28 [3.04, 3.54] |  |  |  |  |
| catseg_native_frozen_full | 8.38 | 0.65 | 100.0 |  |  |  |  | 4.21 [3.82, 4.63] |
| catseg_native_replay_full | 4.90 | 0.49 | 41.4 |  |  |  |  | 7.81 [7.03, 8.70] |

Brackets are the 2.5-97.5% range of the evaluation mean across splits (splits overlap, so this is spread, not a confidence interval). CRC controls the mean risk over splits; individual splits may exceed alpha. catseg_native_frozen_full reuses the threshold calibrated under the source vocabulary after all labels are added; catseg_native_replay_full recalibrates under the full vocabulary. Stored scores are float16 logits clamped to [-30, 30].