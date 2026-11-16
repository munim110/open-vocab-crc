# Repeated-split calibrated sets from the headroom probe

2000 ADE validation images (development data; 0 without a source-labelled sampled pixel excluded), 150 source labels, 500 random splits per design; thresholds by image-level CRC on the calibration part, everything reported on the rest. Projective arms calibrate once at the source labels. Nothing is fitted; the confirmation reserve is untouched.

## 200 calibration / 1800 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| sclip_fixed_source | 9.42 | 0.78 | 19.6 | 26.09 [22.79, 29.76] | 33.82 [29.61, 38.52] | 47.82 [41.78, 54.56] | 87.97 [76.29, 101.00] | 103.96 [89.80, 119.84] |
| catseg_anchored | 9.46 | 1.06 | 31.0 | 3.06 [2.64, 3.67] | 3.66 [3.12, 4.45] | 4.58 [3.82, 5.72] | 6.83 [5.58, 8.73] | 7.38 [6.01, 9.49] |
| catseg_native_source | 9.50 | 1.05 | 31.6 | 2.42 [2.05, 2.96] |  |  |  |  |
| catseg_native_frozen_full | 12.34 | 1.22 | 97.4 |  |  |  |  | 3.79 [3.03, 4.90] |
| catseg_native_replay_full | 9.52 | 1.18 | 34.0 |  |  |  |  | 5.66 [4.12, 8.32] |

## 200 calibration / 1800 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| sclip_fixed_source | 4.46 | 0.51 | 14.4 | 45.88 [40.27, 51.59] | 59.07 [51.91, 66.35] | 84.27 [73.86, 94.86] | 159.59 [138.92, 180.72] | 192.40 [166.68, 218.84] |
| catseg_anchored | 4.47 | 0.78 | 25.4 | 5.95 [4.55, 8.54] | 7.58 [5.65, 11.19] | 10.45 [7.50, 16.00] | 16.88 [11.77, 26.59] | 18.61 [12.87, 29.64] |
| catseg_native_source | 4.50 | 0.80 | 27.4 | 6.07 [4.01, 10.91] |  |  |  |  |
| catseg_native_frozen_full | 6.51 | 0.91 | 94.8 |  |  |  |  | 11.36 [7.22, 20.18] |
| catseg_native_replay_full | 3.58 | 2.25 | 29.4 |  |  |  |  | 248.27 [12.33, 845.00] |

## 1000 calibration / 1000 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| sclip_fixed_source | 9.85 | 0.50 | 41.8 | 24.99 [23.91, 26.21] | 32.43 [31.06, 33.99] | 45.83 [43.83, 48.08] | 84.12 [80.08, 88.46] | 99.28 [94.36, 104.62] |
| catseg_anchored | 9.85 | 0.67 | 41.6 | 2.94 [2.79, 3.10] | 3.50 [3.31, 3.72] | 4.35 [4.07, 4.65] | 6.45 [5.98, 6.95] | 6.96 [6.45, 7.52] |
| catseg_native_source | 9.87 | 0.67 | 40.0 | 2.31 [2.18, 2.46] |  |  |  |  |
| catseg_native_frozen_full | 12.80 | 0.75 | 100.0 |  |  |  |  | 3.55 [3.29, 3.85] |
| catseg_native_replay_full | 9.88 | 0.72 | 40.8 |  |  |  |  | 5.20 [4.65, 5.78] |

## 1000 calibration / 1000 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| sclip_fixed_source | 4.87 | 0.34 | 28.0 | 43.35 [41.34, 45.39] | 55.84 [53.27, 58.45] | 79.58 [75.85, 83.34] | 150.24 [142.89, 157.45] | 180.72 [171.62, 189.71] |
| catseg_anchored | 4.87 | 0.51 | 37.0 | 5.29 [4.83, 5.79] | 6.67 [6.04, 7.35] | 9.05 [8.10, 10.12] | 14.45 [12.80, 16.33] | 15.86 [14.03, 17.97] |
| catseg_native_source | 4.89 | 0.50 | 40.4 | 4.98 [4.40, 5.65] |  |  |  |  |
| catseg_native_frozen_full | 6.96 | 0.58 | 100.0 |  |  |  |  | 9.30 [8.09, 10.73] |
| catseg_native_replay_full | 4.88 | 0.60 | 39.2 |  |  |  |  | 23.29 [15.12, 33.15] |

Brackets are the 2.5-97.5% range of the evaluation mean across splits (splits overlap, so this is spread, not a confidence interval). CRC controls the mean risk over splits; individual splits may exceed alpha. catseg_native_frozen_full reuses the threshold calibrated under the source vocabulary after all labels are added; catseg_native_replay_full recalibrates under the full vocabulary. Stored scores are float16 logits clamped to [-30, 30].