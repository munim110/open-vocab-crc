# Repeated-split calibrated sets from the headroom probe

2000 COCO val2017 (LVIS-annotated) images (development data; 0 without a source-labelled sampled pixel excluded), 171 source labels, 500 random splits per design; thresholds by image-level CRC on the calibration part, everything reported on the rest. Projective arms calibrate once at the source labels. Nothing is fitted; the confirmation reserve is untouched.

## 200 calibration / 1800 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +1112 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 9.63 | 1.05 | 34.2 | 2.23 [1.98, 2.54] | 2.27 [2.02, 2.59] | 2.37 [2.09, 2.70] | 2.76 [2.42, 3.18] | 3.65 [3.16, 4.26] |
| catseg_native_source | 9.61 | 1.08 | 35.6 | 2.06 [1.81, 2.36] |  |  |  |  |
| catseg_native_frozen_full | 3.49 | 0.49 | 0.0 |  |  |  |  | 8.49 [7.21, 10.04] |
| catseg_native_replay_full | 9.65 | 1.06 | 35.0 |  |  |  |  | 3.84 [3.35, 4.46] |

## 200 calibration / 1800 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +1112 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 4.60 | 0.74 | 29.6 | 3.60 [3.09, 4.32] | 3.67 [3.15, 4.42] | 3.88 [3.31, 4.70] | 4.74 [3.98, 5.85] | 6.55 [5.43, 8.20] |
| catseg_native_source | 4.60 | 0.77 | 33.0 | 3.36 [2.84, 4.10] |  |  |  |  |
| catseg_native_frozen_full | 1.51 | 0.27 | 0.0 |  |  |  |  | 15.56 [12.60, 19.69] |
| catseg_native_replay_full | 4.60 | 0.76 | 30.8 |  |  |  |  | 6.91 [5.59, 8.80] |

## 1000 calibration / 1000 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +1112 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 9.89 | 0.64 | 42.6 | 2.19 [2.10, 2.28] | 2.22 [2.13, 2.31] | 2.31 [2.22, 2.41] | 2.69 [2.57, 2.82] | 3.55 [3.37, 3.73] |
| catseg_native_source | 9.87 | 0.69 | 42.0 | 2.01 [1.91, 2.11] |  |  |  |  |
| catseg_native_frozen_full | 3.62 | 0.32 | 0.0 |  |  |  |  | 8.21 [7.73, 8.75] |
| catseg_native_replay_full | 9.89 | 0.63 | 42.6 |  |  |  |  | 3.74 [3.58, 3.91] |

## 1000 calibration / 1000 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +1112 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 4.90 | 0.48 | 42.0 | 3.43 [3.24, 3.63] | 3.50 [3.30, 3.71] | 3.69 [3.48, 3.92] | 4.48 [4.18, 4.78] | 6.17 [5.73, 6.60] |
| catseg_native_source | 4.88 | 0.51 | 38.4 | 3.21 [3.01, 3.40] |  |  |  |  |
| catseg_native_frozen_full | 1.60 | 0.19 | 0.0 |  |  |  |  | 14.67 [13.58, 15.73] |
| catseg_native_replay_full | 4.90 | 0.45 | 37.6 |  |  |  |  | 6.47 [6.03, 6.92] |

Brackets are the 2.5-97.5% range of the evaluation mean across splits (splits overlap, so this is spread, not a confidence interval). CRC controls the mean risk over splits; individual splits may exceed alpha. catseg_native_frozen_full reuses the threshold calibrated under the source vocabulary after all labels are added; catseg_native_replay_full recalibrates under the full vocabulary. Stored scores are float16 logits clamped to [-30, 30].