# Repeated-split calibrated sets from the headroom probe

2000 COCO val2017 (LVIS-annotated) images (development data; 0 without a source-labelled sampled pixel excluded), 171 source labels, 500 random splits per design; thresholds by image-level CRC on the calibration part, everything reported on the rest. Projective arms calibrate once at the source labels. Nothing is fitted; the confirmation reserve is untouched.

## 200 calibration / 1800 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +1112 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 9.63 | 1.01 | 38.2 | 1.98 [1.77, 2.26] | 2.03 [1.81, 2.31] | 2.10 [1.87, 2.41] | 2.46 [2.17, 2.85] | 3.28 [2.86, 3.86] |
| catseg_native_source | 9.60 | 1.02 | 34.6 | 1.89 [1.70, 2.14] |  |  |  |  |
| catseg_native_frozen_full | 12.58 | 1.16 | 98.2 |  |  |  |  | 2.13 [1.87, 2.50] |
| catseg_native_replay_full | 9.64 | 1.02 | 35.8 |  |  |  |  | 2.71 [2.33, 3.20] |

## 200 calibration / 1800 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +1112 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 4.63 | 0.73 | 31.6 | 3.19 [2.73, 3.80] | 3.29 [2.80, 3.93] | 3.47 [2.93, 4.16] | 4.25 [3.54, 5.20] | 5.98 [4.91, 7.47] |
| catseg_native_source | 4.61 | 0.75 | 31.0 | 3.00 [2.59, 3.63] |  |  |  |  |
| catseg_native_frozen_full | 6.48 | 0.87 | 95.6 |  |  |  |  | 3.82 [3.17, 4.83] |
| catseg_native_replay_full | 4.61 | 0.73 | 31.6 |  |  |  |  | 5.17 [4.12, 6.65] |

## 1000 calibration / 1000 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +1112 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 9.86 | 0.66 | 42.4 | 1.94 [1.86, 2.03] | 1.99 [1.90, 2.07] | 2.06 [1.97, 2.15] | 2.40 [2.30, 2.52] | 3.19 [3.03, 3.37] |
| catseg_native_source | 9.85 | 0.69 | 40.4 | 1.85 [1.78, 1.93] |  |  |  |  |
| catseg_native_frozen_full | 12.85 | 0.76 | 100.0 |  |  |  |  | 2.08 [1.97, 2.19] |
| catseg_native_replay_full | 9.85 | 0.68 | 41.4 |  |  |  |  | 2.64 [2.50, 2.80] |

## 1000 calibration / 1000 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +1112 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 4.89 | 0.52 | 41.8 | 3.07 [2.87, 3.24] | 3.16 [2.95, 3.34] | 3.32 [3.10, 3.51] | 4.05 [3.76, 4.30] | 5.67 [5.21, 6.06] |
| catseg_native_source | 4.88 | 0.52 | 39.4 | 2.87 [2.70, 3.04] |  |  |  |  |
| catseg_native_frozen_full | 6.78 | 0.59 | 100.0 |  |  |  |  | 3.62 [3.35, 3.88] |
| catseg_native_replay_full | 4.89 | 0.52 | 41.4 |  |  |  |  | 4.84 [4.42, 5.25] |

Brackets are the 2.5-97.5% range of the evaluation mean across splits (splits overlap, so this is spread, not a confidence interval). CRC controls the mean risk over splits; individual splits may exceed alpha. catseg_native_frozen_full reuses the threshold calibrated under the source vocabulary after all labels are added; catseg_native_replay_full recalibrates under the full vocabulary. Stored scores are float16 logits clamped to [-30, 30].