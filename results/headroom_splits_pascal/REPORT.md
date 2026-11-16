# Repeated-split calibrated sets from the headroom probe

2000 Pascal Context validation images (development data; 0 without a source-labelled sampled pixel excluded), 59 source labels, 500 random splits per design; thresholds by image-level CRC on the calibration part, everything reported on the rest. Projective arms calibrate once at the source labels. Nothing is fitted; the confirmation reserve is untouched.

## 200 calibration / 1800 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +399 |
|---|---:|---:|---:|---:|---:|---:|---:|
| sclip_fixed_source | 9.56 | 0.76 | 30.2 | 7.68 [6.73, 8.76] | 11.39 [9.82, 13.17] | 17.93 [15.41, 20.78] | 38.91 [33.37, 45.17] |
| catseg_anchored | 9.61 | 1.21 | 36.4 | 1.81 [1.63, 2.02] | 1.99 [1.77, 2.25] | 2.33 [2.03, 2.70] | 3.45 [2.86, 4.18] |
| catseg_native_source | 9.62 | 1.14 | 37.2 | 1.52 [1.37, 1.71] |  |  |  |
| catseg_native_frozen_full | 14.83 | 1.41 | 100.0 |  |  |  | 1.69 [1.45, 2.00] |
| catseg_native_replay_full | 9.63 | 1.14 | 38.4 |  |  |  | 2.61 [2.16, 3.14] |

## 200 calibration / 1800 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +399 |
|---|---:|---:|---:|---:|---:|---:|---:|
| sclip_fixed_source | 4.54 | 0.52 | 18.6 | 14.46 [12.53, 16.86] | 22.72 [19.48, 26.76] | 36.17 [30.90, 42.73] | 78.84 [67.33, 93.11] |
| catseg_anchored | 4.58 | 0.86 | 29.2 | 2.56 [2.22, 2.97] | 2.94 [2.50, 3.48] | 3.73 [3.07, 4.57] | 6.41 [4.96, 8.27] |
| catseg_native_source | 4.59 | 0.80 | 30.8 | 2.27 [1.96, 2.65] |  |  |  |
| catseg_native_frozen_full | 7.97 | 1.14 | 99.4 |  |  |  | 3.13 [2.49, 3.93] |
| catseg_native_replay_full | 4.59 | 0.81 | 29.8 |  |  |  | 4.99 [3.98, 6.52] |

## 1000 calibration / 1000 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +399 |
|---|---:|---:|---:|---:|---:|---:|---:|
| sclip_fixed_source | 9.82 | 0.46 | 38.4 | 7.45 [7.11, 7.76] | 11.01 [10.43, 11.53] | 17.32 [16.41, 18.15] | 37.57 [35.54, 39.39] |
| catseg_anchored | 9.85 | 0.71 | 42.2 | 1.78 [1.72, 1.84] | 1.95 [1.88, 2.03] | 2.28 [2.17, 2.39] | 3.35 [3.15, 3.56] |
| catseg_native_source | 9.87 | 0.71 | 40.2 | 1.49 [1.44, 1.55] |  |  |  |
| catseg_native_frozen_full | 15.17 | 0.84 | 100.0 |  |  |  | 1.63 [1.55, 1.73] |
| catseg_native_replay_full | 9.87 | 0.72 | 46.2 |  |  |  | 2.52 [2.36, 2.69] |

## 1000 calibration / 1000 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +399 |
|---|---:|---:|---:|---:|---:|---:|---:|
| sclip_fixed_source | 4.86 | 0.31 | 30.4 | 13.67 [13.00, 14.30] | 21.39 [20.26, 22.46] | 34.00 [32.19, 35.72] | 74.10 [70.17, 77.88] |
| catseg_anchored | 4.85 | 0.53 | 37.2 | 2.47 [2.36, 2.59] | 2.83 [2.68, 2.98] | 3.56 [3.33, 3.79] | 6.01 [5.54, 6.53] |
| catseg_native_source | 4.88 | 0.53 | 41.4 | 2.19 [2.08, 2.30] |  |  |  |
| catseg_native_frozen_full | 8.39 | 0.68 | 100.0 |  |  |  | 2.94 [2.71, 3.18] |
| catseg_native_replay_full | 4.88 | 0.52 | 42.2 |  |  |  | 4.66 [4.32, 5.05] |

Brackets are the 2.5-97.5% range of the evaluation mean across splits (splits overlap, so this is spread, not a confidence interval). CRC controls the mean risk over splits; individual splits may exceed alpha. catseg_native_frozen_full reuses the threshold calibrated under the source vocabulary after all labels are added; catseg_native_replay_full recalibrates under the full vocabulary. Stored scores are float16 logits clamped to [-30, 30].