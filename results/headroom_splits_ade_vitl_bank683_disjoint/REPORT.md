# Repeated-split calibrated sets from the headroom probe

1600 ADE validation images (development data; 0 without a source-labelled sampled pixel excluded), 150 source labels, 500 random splits per design; thresholds by image-level CRC on the calibration part, everything reported on the rest. Projective arms calibrate once at the source labels. Nothing is fitted; the confirmation reserve is untouched.

## 200 calibration / 1400 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| sclip_fixed_source | 9.48 | 0.72 | 23.8 | 25.57 [22.79, 28.69] | 33.17 [29.62, 37.13] | 46.91 [41.81, 52.59] | 86.23 [76.34, 97.26] | 101.84 [89.81, 115.31] |
| catseg_anchored | 9.54 | 1.06 | 31.4 | 2.32 [2.05, 2.64] | 2.63 [2.30, 3.02] | 3.06 [2.64, 3.57] | 4.22 [3.54, 5.05] | 4.44 [3.71, 5.34] |
| catseg_native_source | 9.55 | 1.01 | 32.6 | 1.98 [1.74, 2.24] |  |  |  |  |
| catseg_native_frozen_full | 14.52 | 1.27 | 100.0 |  |  |  |  | 2.26 [1.93, 2.62] |
| catseg_native_replay_full | 9.58 | 1.07 | 34.0 |  |  |  |  | 3.61 [2.93, 4.49] |

## 200 calibration / 1400 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| sclip_fixed_source | 4.50 | 0.48 | 13.6 | 45.10 [40.39, 50.51] | 58.07 [52.08, 64.96] | 82.83 [74.14, 92.83] | 156.76 [139.51, 176.69] | 188.89 [167.37, 213.82] |
| catseg_anchored | 4.55 | 0.76 | 26.4 | 3.99 [3.22, 4.96] | 4.71 [3.73, 5.94] | 5.87 [4.53, 7.59] | 8.98 [6.66, 11.98] | 9.76 [7.13, 13.20] |
| catseg_native_source | 4.56 | 0.76 | 27.6 | 3.58 [2.87, 4.41] |  |  |  |  |
| catseg_native_frozen_full | 7.72 | 1.02 | 100.0 |  |  |  |  | 4.70 [3.55, 6.11] |
| catseg_native_replay_full | 4.57 | 0.79 | 28.2 |  |  |  |  | 8.91 [6.36, 12.49] |

## 800 calibration / 800 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| sclip_fixed_source | 9.80 | 0.54 | 39.4 | 24.71 [23.56, 26.03] | 32.08 [30.59, 33.78] | 45.35 [43.18, 47.79] | 83.22 [78.87, 87.94] | 98.19 [92.93, 103.89] |
| catseg_anchored | 9.83 | 0.74 | 42.0 | 2.26 [2.16, 2.38] | 2.56 [2.43, 2.70] | 2.97 [2.80, 3.15] | 4.06 [3.80, 4.35] | 4.28 [3.99, 4.58] |
| catseg_native_source | 9.85 | 0.71 | 38.0 | 1.92 [1.83, 2.02] |  |  |  |  |
| catseg_native_frozen_full | 14.89 | 0.87 | 100.0 |  |  |  |  | 2.18 [2.05, 2.31] |
| catseg_native_replay_full | 9.85 | 0.75 | 39.8 |  |  |  |  | 3.46 [3.19, 3.73] |

## 800 calibration / 800 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| sclip_fixed_source | 4.84 | 0.36 | 28.0 | 43.00 [40.91, 45.09] | 55.39 [52.73, 58.06] | 78.94 [75.07, 82.81] | 149.01 [141.33, 156.71] | 179.20 [169.73, 188.74] |
| catseg_anchored | 4.88 | 0.57 | 40.2 | 3.74 [3.42, 4.08] | 4.38 [3.98, 4.80] | 5.42 [4.89, 5.99] | 8.19 [7.25, 9.16] | 8.86 [7.80, 9.96] |
| catseg_native_source | 4.88 | 0.56 | 37.6 | 3.36 [3.07, 3.67] |  |  |  |  |
| catseg_native_frozen_full | 8.13 | 0.72 | 100.0 |  |  |  |  | 4.34 [3.88, 4.85] |
| catseg_native_replay_full | 4.88 | 0.58 | 39.2 |  |  |  |  | 8.05 [7.03, 9.22] |

Brackets are the 2.5-97.5% range of the evaluation mean across splits (splits overlap, so this is spread, not a confidence interval). CRC controls the mean risk over splits; individual splits may exceed alpha. catseg_native_frozen_full reuses the threshold calibrated under the source vocabulary after all labels are added; catseg_native_replay_full recalibrates under the full vocabulary. Stored scores are float16 logits clamped to [-30, 30].