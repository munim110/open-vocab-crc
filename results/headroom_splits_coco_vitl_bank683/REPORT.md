# Repeated-split calibrated sets from the headroom probe

2000 COCO val2017 (LVIS-annotated) images (development data; 0 without a source-labelled sampled pixel excluded), 171 source labels, 500 random splits per design; thresholds by image-level CRC on the calibration part, everything reported on the rest. Projective arms calibrate once at the source labels. Nothing is fitted; the confirmation reserve is untouched.

## 200 calibration / 1800 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +1112 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 9.64 | 1.05 | 36.4 | 2.10 [1.86, 2.41] | 2.15 [1.90, 2.47] | 2.22 [1.95, 2.55] | 2.55 [2.23, 2.96] | 3.31 [2.84, 3.90] |
| catseg_native_source | 9.62 | 1.05 | 36.8 | 1.99 [1.76, 2.28] |  |  |  |  |
| catseg_native_frozen_full | 12.50 | 1.26 | 97.8 |  |  |  |  | 2.19 [1.90, 2.57] |
| catseg_native_replay_full | 9.66 | 1.04 | 37.0 |  |  |  |  | 2.73 [2.33, 3.27] |

## 200 calibration / 1800 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +1112 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 4.61 | 0.76 | 32.6 | 3.44 [2.90, 4.08] | 3.54 [2.98, 4.20] | 3.69 [3.10, 4.41] | 4.44 [3.66, 5.38] | 6.09 [4.92, 7.53] |
| catseg_native_source | 4.59 | 0.74 | 31.6 | 3.17 [2.73, 3.84] |  |  |  |  |
| catseg_native_frozen_full | 6.59 | 0.90 | 96.0 |  |  |  |  | 3.82 [3.19, 4.81] |
| catseg_native_replay_full | 4.61 | 0.75 | 30.4 |  |  |  |  | 5.23 [4.15, 6.83] |

## 1000 calibration / 1000 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +1112 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 9.85 | 0.67 | 39.8 | 2.06 [1.97, 2.15] | 2.11 [2.02, 2.20] | 2.17 [2.07, 2.26] | 2.49 [2.38, 2.61] | 3.22 [3.04, 3.39] |
| catseg_native_source | 9.83 | 0.68 | 38.2 | 1.95 [1.87, 2.04] |  |  |  |  |
| catseg_native_frozen_full | 12.77 | 0.77 | 100.0 |  |  |  |  | 2.13 [2.02, 2.25] |
| catseg_native_replay_full | 9.83 | 0.68 | 39.8 |  |  |  |  | 2.66 [2.51, 2.80] |

## 1000 calibration / 1000 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +1112 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 4.87 | 0.52 | 40.2 | 3.29 [3.07, 3.50] | 3.39 [3.16, 3.60] | 3.53 [3.29, 3.77] | 4.22 [3.89, 4.53] | 5.75 [5.28, 6.22] |
| catseg_native_source | 4.87 | 0.52 | 36.8 | 3.02 [2.85, 3.22] |  |  |  |  |
| catseg_native_frozen_full | 6.95 | 0.60 | 100.0 |  |  |  |  | 3.60 [3.34, 3.88] |
| catseg_native_replay_full | 4.88 | 0.51 | 39.8 |  |  |  |  | 4.89 [4.48, 5.34] |

Brackets are the 2.5-97.5% range of the evaluation mean across splits (splits overlap, so this is spread, not a confidence interval). CRC controls the mean risk over splits; individual splits may exceed alpha. catseg_native_frozen_full reuses the threshold calibrated under the source vocabulary after all labels are added; catseg_native_replay_full recalibrates under the full vocabulary. Stored scores are float16 logits clamped to [-30, 30].