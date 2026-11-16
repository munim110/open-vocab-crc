# Repeated-split calibrated sets from the headroom probe

2000 ADE validation images (development data; 0 without a source-labelled sampled pixel excluded), 150 source labels, 500 random splits per design; thresholds by image-level CRC on the calibration part, everything reported on the rest. Projective arms calibrate once at the source labels. Nothing is fitted; the confirmation reserve is untouched.

## 200 calibration / 1800 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| sclip_fixed_source | 9.42 | 0.78 | 19.6 | 26.09 [22.79, 29.76] | 33.82 [29.61, 38.52] | 47.82 [41.78, 54.56] | 87.97 [76.29, 101.00] | 103.96 [89.80, 119.84] |
| catseg_anchored | 9.47 | 1.03 | 30.4 | 3.22 [2.76, 3.73] | 3.81 [3.21, 4.47] | 4.65 [3.85, 5.56] | 7.15 [5.76, 8.71] | 7.72 [6.19, 9.48] |
| catseg_native_source | 9.52 | 0.99 | 30.6 | 2.41 [2.04, 2.85] |  |  |  |  |
| catseg_native_frozen_full | 14.84 | 1.31 | 100.0 |  |  |  |  | 2.89 [2.33, 3.58] |
| catseg_native_replay_full | 9.53 | 1.09 | 34.4 |  |  |  |  | 5.34 [4.03, 6.99] |

## 200 calibration / 1800 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| sclip_fixed_source | 4.46 | 0.51 | 14.4 | 45.88 [40.27, 51.59] | 59.07 [51.91, 66.35] | 84.27 [73.86, 94.86] | 159.59 [138.92, 180.72] | 192.40 [166.68, 218.84] |
| catseg_anchored | 4.48 | 0.69 | 22.6 | 5.84 [4.83, 6.98] | 7.23 [5.89, 8.75] | 9.50 [7.56, 11.70] | 15.65 [12.23, 19.54] | 17.37 [13.46, 21.84] |
| catseg_native_source | 4.49 | 0.70 | 21.8 | 5.00 [3.82, 6.41] |  |  |  |  |
| catseg_native_frozen_full | 7.55 | 1.02 | 100.0 |  |  |  |  | 7.42 [5.26, 10.11] |
| catseg_native_replay_full | 4.49 | 0.75 | 25.4 |  |  |  |  | 15.19 [10.17, 21.01] |

## 1000 calibration / 1000 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| sclip_fixed_source | 9.85 | 0.50 | 41.8 | 24.99 [23.91, 26.21] | 32.43 [31.06, 33.99] | 45.83 [43.83, 48.08] | 84.12 [80.08, 88.46] | 99.28 [94.36, 104.62] |
| catseg_anchored | 9.85 | 0.63 | 39.4 | 3.10 [2.94, 3.27] | 3.65 [3.45, 3.87] | 4.44 [4.17, 4.73] | 6.78 [6.29, 7.27] | 7.32 [6.78, 7.86] |
| catseg_native_source | 9.86 | 0.63 | 37.0 | 2.31 [2.20, 2.43] |  |  |  |  |
| catseg_native_frozen_full | 15.36 | 0.79 | 100.0 |  |  |  |  | 2.73 [2.55, 2.92] |
| catseg_native_replay_full | 9.88 | 0.67 | 41.0 |  |  |  |  | 4.99 [4.56, 5.43] |

## 1000 calibration / 1000 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| sclip_fixed_source | 4.87 | 0.34 | 28.0 | 43.35 [41.34, 45.39] | 55.84 [53.27, 58.45] | 79.58 [75.85, 83.34] | 150.24 [142.89, 157.45] | 180.72 [171.62, 189.71] |
| catseg_anchored | 4.87 | 0.45 | 39.6 | 5.46 [5.13, 5.82] | 6.73 [6.30, 7.21] | 8.78 [8.15, 9.48] | 14.37 [13.24, 15.63] | 15.90 [14.62, 17.33] |
| catseg_native_source | 4.88 | 0.45 | 37.2 | 4.54 [4.16, 4.96] |  |  |  |  |
| catseg_native_frozen_full | 8.14 | 0.62 | 100.0 |  |  |  |  | 6.56 [5.85, 7.35] |
| catseg_native_replay_full | 4.89 | 0.48 | 41.0 |  |  |  |  | 13.29 [11.70, 15.06] |

Brackets are the 2.5-97.5% range of the evaluation mean across splits (splits overlap, so this is spread, not a confidence interval). CRC controls the mean risk over splits; individual splits may exceed alpha. catseg_native_frozen_full reuses the threshold calibrated under the source vocabulary after all labels are added; catseg_native_replay_full recalibrates under the full vocabulary. Stored scores are float16 logits clamped to [-30, 30].