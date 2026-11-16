# Repeated-split calibrated sets from the headroom probe

2000 ADE validation images (development data; 0 without a source-labelled sampled pixel excluded), 150 source labels, 500 random splits per design; thresholds by image-level CRC on the calibration part, everything reported on the rest. Projective arms calibrate once at the source labels. Nothing is fitted; the confirmation reserve is untouched.

## 200 calibration / 1800 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 9.48 | 1.03 | 33.4 | 3.33 [2.82, 3.99] | 3.77 [3.15, 4.57] | 4.46 [3.65, 5.53] | 6.20 [4.90, 7.93] | 6.55 [5.14, 8.43] |
| catseg_native_source | 9.50 | 1.04 | 32.4 | 3.15 [2.71, 3.74] |  |  |  |  |
| catseg_native_frozen_full | 12.47 | 1.16 | 99.0 |  |  |  |  | 4.20 [3.51, 5.14] |
| catseg_native_replay_full | 9.51 | 1.10 | 33.2 |  |  |  |  | 5.80 [4.55, 7.40] |

## 200 calibration / 1800 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 4.47 | 0.74 | 24.0 | 6.54 [5.12, 8.34] | 7.72 [5.96, 9.97] | 9.87 [7.41, 13.02] | 15.19 [11.05, 20.53] | 16.49 [11.87, 22.51] |
| catseg_native_source | 4.49 | 0.74 | 22.8 | 6.04 [4.70, 7.77] |  |  |  |  |
| catseg_native_frozen_full | 6.57 | 0.92 | 97.0 |  |  |  |  | 9.10 [6.75, 12.27] |
| catseg_native_replay_full | 4.49 | 0.77 | 25.0 |  |  |  |  | 15.04 [10.16, 22.74] |

## 1000 calibration / 1000 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 9.87 | 0.64 | 43.6 | 3.19 [3.01, 3.38] | 3.60 [3.38, 3.83] | 4.24 [3.95, 4.54] | 5.83 [5.38, 6.32] | 6.15 [5.67, 6.67] |
| catseg_native_source | 9.88 | 0.66 | 39.4 | 3.03 [2.87, 3.20] |  |  |  |  |
| catseg_native_frozen_full | 12.91 | 0.73 | 100.0 |  |  |  |  | 4.01 [3.76, 4.27] |
| catseg_native_replay_full | 9.89 | 0.68 | 40.4 |  |  |  |  | 5.47 [5.07, 5.91] |

## 1000 calibration / 1000 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 4.89 | 0.49 | 37.8 | 5.98 [5.49, 6.51] | 7.03 [6.41, 7.68] | 8.90 [8.02, 9.84] | 13.53 [12.07, 15.13] | 14.63 [12.99, 16.41] |
| catseg_native_source | 4.89 | 0.49 | 39.4 | 5.52 [5.10, 6.00] |  |  |  |  |
| catseg_native_frozen_full | 7.07 | 0.59 | 100.0 |  |  |  |  | 8.17 [7.42, 9.00] |
| catseg_native_replay_full | 4.89 | 0.50 | 41.2 |  |  |  |  | 12.88 [11.37, 14.69] |

Brackets are the 2.5-97.5% range of the evaluation mean across splits (splits overlap, so this is spread, not a confidence interval). CRC controls the mean risk over splits; individual splits may exceed alpha. catseg_native_frozen_full reuses the threshold calibrated under the source vocabulary after all labels are added; catseg_native_replay_full recalibrates under the full vocabulary. Stored scores are float16 logits clamped to [-30, 30].