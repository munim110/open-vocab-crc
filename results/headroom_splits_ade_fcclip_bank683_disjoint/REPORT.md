# Repeated-split calibrated sets from the headroom probe

1600 ADE validation images (development data; 0 without a source-labelled sampled pixel excluded), 150 source labels, 500 random splits per design; thresholds by image-level CRC on the calibration part, everything reported on the rest. Projective arms calibrate once at the source labels. Nothing is fitted; the confirmation reserve is untouched.

## 200 calibration / 1400 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| sclip_fixed_source | 9.48 | 0.72 | 23.8 | 25.57 [22.79, 28.69] | 33.17 [29.62, 37.13] | 46.91 [41.81, 52.59] | 86.23 [76.34, 97.26] | 101.84 [89.81, 115.31] |
| catseg_anchored | 9.54 | 1.04 | 32.6 | 3.93 [3.27, 4.96] | 5.01 [4.13, 6.36] | 6.44 [5.21, 8.35] | 10.39 [8.22, 13.81] | 11.59 [9.09, 15.58] |
| catseg_native_source | 9.62 | 1.03 | 35.8 | 3.31 [2.73, 4.05] |  |  |  |  |
| catseg_native_frozen_full | 13.46 | 1.38 | 99.6 |  |  |  |  | 5.34 [4.19, 6.81] |
| catseg_native_replay_full | 9.63 | 1.06 | 34.0 |  |  |  |  | 8.50 [6.44, 11.32] |

## 200 calibration / 1400 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| sclip_fixed_source | 4.50 | 0.48 | 13.6 | 45.10 [40.39, 50.51] | 58.07 [52.08, 64.96] | 82.83 [74.14, 92.83] | 156.76 [139.51, 176.69] | 188.89 [167.37, 213.82] |
| catseg_anchored | 4.58 | 0.83 | 29.4 | 9.84 [6.58, 16.00] | 12.73 [8.49, 20.71] | 17.55 [11.39, 29.18] | 30.88 [19.39, 53.02] | 35.85 [22.15, 62.74] |
| catseg_native_source | 4.57 | 0.78 | 27.2 | 8.61 [5.63, 13.50] |  |  |  |  |
| catseg_native_frozen_full | 6.42 | 1.14 | 91.0 |  |  |  |  | 16.97 [10.14, 29.08] |
| catseg_native_replay_full | 4.60 | 0.85 | 30.2 |  |  |  |  | 30.65 [16.87, 53.69] |

## 800 calibration / 800 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| sclip_fixed_source | 9.80 | 0.54 | 39.4 | 24.71 [23.56, 26.03] | 32.08 [30.59, 33.78] | 45.35 [43.18, 47.79] | 83.22 [78.87, 87.94] | 98.19 [92.93, 103.89] |
| catseg_anchored | 9.84 | 0.71 | 40.2 | 3.76 [3.46, 4.04] | 4.78 [4.40, 5.15] | 6.11 [5.57, 6.63] | 9.81 [8.86, 10.73] | 10.92 [9.82, 12.00] |
| catseg_native_source | 9.84 | 0.71 | 44.2 | 3.20 [2.98, 3.43] |  |  |  |  |
| catseg_native_frozen_full | 13.76 | 0.88 | 100.0 |  |  |  |  | 5.12 [4.69, 5.57] |
| catseg_native_replay_full | 9.83 | 0.74 | 41.2 |  |  |  |  | 8.07 [7.34, 8.87] |

## 800 calibration / 800 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| sclip_fixed_source | 4.84 | 0.36 | 28.0 | 43.00 [40.91, 45.09] | 55.39 [52.73, 58.06] | 78.94 [75.07, 82.81] | 149.01 [141.33, 156.71] | 179.20 [169.73, 188.74] |
| catseg_anchored | 4.87 | 0.55 | 40.8 | 8.64 [7.56, 9.92] | 11.17 [9.78, 12.86] | 15.27 [13.26, 17.72] | 26.57 [22.86, 31.15] | 30.65 [26.21, 36.14] |
| catseg_native_source | 4.88 | 0.53 | 40.4 | 7.45 [6.40, 8.94] |  |  |  |  |
| catseg_native_frozen_full | 6.89 | 0.72 | 100.0 |  |  |  |  | 14.15 [11.75, 17.52] |
| catseg_native_replay_full | 4.87 | 0.56 | 41.2 |  |  |  |  | 25.83 [20.98, 31.63] |

Brackets are the 2.5-97.5% range of the evaluation mean across splits (splits overlap, so this is spread, not a confidence interval). CRC controls the mean risk over splits; individual splits may exceed alpha. catseg_native_frozen_full reuses the threshold calibrated under the source vocabulary after all labels are added; catseg_native_replay_full recalibrates under the full vocabulary. Stored scores are float16 logits clamped to [-30, 30].