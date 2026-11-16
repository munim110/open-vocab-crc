# Repeated-split calibrated sets from the headroom probe

1600 ADE validation images (development data; 0 without a source-labelled sampled pixel excluded), 150 source labels, 500 random splits per design; thresholds by image-level CRC on the calibration part, everything reported on the rest. Projective arms calibrate once at the source labels. Nothing is fitted; the confirmation reserve is untouched.

## 200 calibration / 1400 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| sclip_fixed_source | 9.48 | 0.72 | 23.8 | 25.57 [22.79, 28.69] | 33.17 [29.62, 37.13] | 46.91 [41.81, 52.59] | 86.23 [76.34, 97.26] | 101.84 [89.81, 115.31] |
| catseg_anchored | 9.55 | 1.10 | 33.6 | 2.86 [2.45, 3.41] | 3.37 [2.84, 4.10] | 4.10 [3.36, 5.15] | 5.92 [4.74, 7.62] | 6.32 [5.04, 8.19] |
| catseg_native_source | 9.60 | 1.06 | 34.8 | 2.32 [2.00, 2.75] |  |  |  |  |
| catseg_native_frozen_full | 6.91 | 0.64 | 0.0 |  |  |  |  | 9.40 [7.53, 12.02] |
| catseg_native_replay_full | 9.58 | 1.11 | 36.0 |  |  |  |  | 5.63 [4.28, 7.72] |

## 200 calibration / 1400 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| sclip_fixed_source | 4.50 | 0.48 | 13.6 | 45.10 [40.39, 50.51] | 58.07 [52.08, 64.96] | 82.83 [74.14, 92.83] | 156.76 [139.51, 176.69] | 188.89 [167.37, 213.82] |
| catseg_anchored | 4.58 | 0.86 | 27.0 | 6.13 [4.29, 9.49] | 7.85 [5.30, 12.54] | 10.80 [6.91, 18.02] | 17.30 [10.57, 29.98] | 19.03 [11.45, 33.46] |
| catseg_native_source | 4.56 | 0.82 | 26.6 | 5.37 [3.71, 7.81] |  |  |  |  |
| catseg_native_frozen_full | 3.59 | 0.61 | 0.6 |  |  |  |  | 29.47 [18.14, 46.42] |
| catseg_native_replay_full | 4.59 | 0.86 | 30.0 |  |  |  |  | 19.57 [11.41, 33.29] |

## 800 calibration / 800 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| sclip_fixed_source | 9.80 | 0.54 | 39.4 | 24.71 [23.56, 26.03] | 32.08 [30.59, 33.78] | 45.35 [43.18, 47.79] | 83.22 [78.87, 87.94] | 98.19 [92.93, 103.89] |
| catseg_anchored | 9.82 | 0.77 | 38.2 | 2.77 [2.59, 2.95] | 3.25 [3.02, 3.48] | 3.93 [3.62, 4.25] | 5.64 [5.16, 6.14] | 6.03 [5.50, 6.56] |
| catseg_native_source | 9.84 | 0.74 | 43.0 | 2.25 [2.11, 2.39] |  |  |  |  |
| catseg_native_frozen_full | 7.06 | 0.55 | 0.0 |  |  |  |  | 8.95 [8.16, 9.82] |
| catseg_native_replay_full | 9.84 | 0.79 | 41.4 |  |  |  |  | 5.29 [4.74, 5.95] |

## 800 calibration / 800 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| sclip_fixed_source | 4.84 | 0.36 | 28.0 | 43.00 [40.91, 45.09] | 55.39 [52.73, 58.06] | 78.94 [75.07, 82.81] | 149.01 [141.33, 156.71] | 179.20 [169.73, 188.74] |
| catseg_anchored | 4.89 | 0.57 | 43.8 | 5.43 [4.84, 6.26] | 6.88 [6.06, 8.01] | 9.31 [8.06, 11.01] | 14.68 [12.56, 17.65] | 16.06 [13.67, 19.38] |
| catseg_native_source | 4.89 | 0.56 | 42.8 | 4.74 [4.20, 5.45] |  |  |  |  |
| catseg_native_frozen_full | 3.85 | 0.44 | 0.2 |  |  |  |  | 25.18 [21.34, 29.94] |
| catseg_native_replay_full | 4.89 | 0.59 | 43.2 |  |  |  |  | 16.53 [13.82, 20.14] |

Brackets are the 2.5-97.5% range of the evaluation mean across splits (splits overlap, so this is spread, not a confidence interval). CRC controls the mean risk over splits; individual splits may exceed alpha. catseg_native_frozen_full reuses the threshold calibrated under the source vocabulary after all labels are added; catseg_native_replay_full recalibrates under the full vocabulary. Stored scores are float16 logits clamped to [-30, 30].