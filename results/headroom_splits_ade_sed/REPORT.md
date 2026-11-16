# Repeated-split calibrated sets from the headroom probe

2000 ADE validation images (development data; 0 without a source-labelled sampled pixel excluded), 150 source labels, 500 random splits per design; thresholds by image-level CRC on the calibration part, everything reported on the rest. Projective arms calibrate once at the source labels. Nothing is fitted; the confirmation reserve is untouched.

## 200 calibration / 1800 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| sclip_fixed_source | 9.42 | 0.78 | 19.6 | 26.09 [22.79, 29.76] | 33.82 [29.61, 38.52] | 47.82 [41.78, 54.56] | 87.97 [76.29, 101.00] | 103.96 [89.80, 119.84] |
| catseg_anchored | 9.46 | 1.06 | 31.0 | 3.06 [2.64, 3.67] | 3.66 [3.12, 4.45] | 4.58 [3.82, 5.72] | 6.83 [5.58, 8.73] | 7.38 [6.01, 9.49] |
| catseg_native_source | 9.50 | 1.04 | 31.8 | 2.32 [1.99, 2.76] |  |  |  |  |
| catseg_native_frozen_full | 6.87 | 0.63 | 0.0 |  |  |  |  | 9.39 [7.46, 12.08] |
| catseg_native_replay_full | 9.49 | 1.13 | 34.0 |  |  |  |  | 5.72 [4.29, 7.99] |

## 200 calibration / 1800 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| sclip_fixed_source | 4.46 | 0.51 | 14.4 | 45.88 [40.27, 51.59] | 59.07 [51.91, 66.35] | 84.27 [73.86, 94.86] | 159.59 [138.92, 180.72] | 192.40 [166.68, 218.84] |
| catseg_anchored | 4.47 | 0.78 | 25.4 | 5.95 [4.55, 8.54] | 7.58 [5.65, 11.19] | 10.45 [7.50, 16.00] | 16.88 [11.77, 26.59] | 18.61 [12.87, 29.64] |
| catseg_native_source | 4.51 | 0.79 | 25.6 | 5.40 [3.75, 7.85] |  |  |  |  |
| catseg_native_frozen_full | 3.49 | 0.59 | 0.2 |  |  |  |  | 29.58 [18.41, 46.60] |
| catseg_native_replay_full | 4.50 | 0.81 | 26.6 |  |  |  |  | 19.55 [11.70, 32.17] |

## 1000 calibration / 1000 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| sclip_fixed_source | 9.85 | 0.50 | 41.8 | 24.99 [23.91, 26.21] | 32.43 [31.06, 33.99] | 45.83 [43.83, 48.08] | 84.12 [80.08, 88.46] | 99.28 [94.36, 104.62] |
| catseg_anchored | 9.85 | 0.67 | 41.6 | 2.94 [2.79, 3.10] | 3.50 [3.31, 3.72] | 4.35 [4.07, 4.65] | 6.45 [5.98, 6.95] | 6.96 [6.45, 7.52] |
| catseg_native_source | 9.88 | 0.66 | 38.2 | 2.22 [2.11, 2.36] |  |  |  |  |
| catseg_native_frozen_full | 7.10 | 0.49 | 0.0 |  |  |  |  | 8.80 [8.09, 9.60] |
| catseg_native_replay_full | 9.89 | 0.71 | 43.4 |  |  |  |  | 5.28 [4.79, 5.80] |

## 1000 calibration / 1000 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| sclip_fixed_source | 4.87 | 0.34 | 28.0 | 43.35 [41.34, 45.39] | 55.84 [53.27, 58.45] | 79.58 [75.85, 83.34] | 150.24 [142.89, 157.45] | 180.72 [171.62, 189.71] |
| catseg_anchored | 4.87 | 0.51 | 37.0 | 5.29 [4.83, 5.79] | 6.67 [6.04, 7.35] | 9.05 [8.10, 10.12] | 14.45 [12.80, 16.33] | 15.86 [14.03, 17.97] |
| catseg_native_source | 4.89 | 0.50 | 39.2 | 4.71 [4.17, 5.28] |  |  |  |  |
| catseg_native_frozen_full | 3.78 | 0.40 | 0.2 |  |  |  |  | 24.84 [21.13, 28.86] |
| catseg_native_replay_full | 4.89 | 0.52 | 40.4 |  |  |  |  | 16.19 [13.59, 18.88] |

Brackets are the 2.5-97.5% range of the evaluation mean across splits (splits overlap, so this is spread, not a confidence interval). CRC controls the mean risk over splits; individual splits may exceed alpha. catseg_native_frozen_full reuses the threshold calibrated under the source vocabulary after all labels are added; catseg_native_replay_full recalibrates under the full vocabulary. Stored scores are float16 logits clamped to [-30, 30].