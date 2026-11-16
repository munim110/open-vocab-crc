# Repeated-split calibrated sets from the headroom probe

2000 COCO val2017 (LVIS-annotated) images (development data; 0 without a source-labelled sampled pixel excluded), 171 source labels, 500 random splits per design; thresholds by image-level CRC on the calibration part, everything reported on the rest. Projective arms calibrate once at the source labels. Nothing is fitted; the confirmation reserve is untouched.

## 200 calibration / 1800 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +1112 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 9.65 | 1.02 | 34.4 | 2.37 [2.08, 2.74] | 2.42 [2.11, 2.79] | 2.52 [2.20, 2.93] | 2.98 [2.57, 3.49] | 3.94 [3.35, 4.71] |
| catseg_native_source | 9.63 | 1.04 | 34.4 | 2.20 [1.93, 2.53] |  |  |  |  |
| catseg_native_frozen_full | 12.61 | 1.17 | 98.4 |  |  |  |  | 2.46 [2.10, 2.91] |
| catseg_native_replay_full | 9.65 | 1.04 | 38.4 |  |  |  |  | 3.21 [2.68, 3.92] |

## 200 calibration / 1800 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +1112 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 4.62 | 0.75 | 31.6 | 3.98 [3.37, 4.73] | 4.07 [3.44, 4.87] | 4.33 [3.63, 5.20] | 5.33 [4.40, 6.53] | 7.56 [6.10, 9.48] |
| catseg_native_source | 4.61 | 0.75 | 32.6 | 3.72 [3.11, 4.56] |  |  |  |  |
| catseg_native_frozen_full | 6.55 | 0.96 | 94.8 |  |  |  |  | 4.66 [3.74, 5.99] |
| catseg_native_replay_full | 4.62 | 0.73 | 31.6 |  |  |  |  | 6.40 [5.12, 8.40] |

## 1000 calibration / 1000 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +1112 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 9.87 | 0.64 | 40.8 | 2.33 [2.22, 2.43] | 2.37 [2.26, 2.48] | 2.47 [2.35, 2.58] | 2.91 [2.76, 3.05] | 3.84 [3.62, 4.05] |
| catseg_native_source | 9.86 | 0.67 | 40.6 | 2.15 [2.05, 2.25] |  |  |  |  |
| catseg_native_frozen_full | 12.88 | 0.72 | 100.0 |  |  |  |  | 2.39 [2.26, 2.53] |
| catseg_native_replay_full | 9.86 | 0.66 | 38.2 |  |  |  |  | 3.11 [2.92, 3.31] |

## 1000 calibration / 1000 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +1112 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 4.89 | 0.47 | 38.4 | 3.80 [3.58, 4.02] | 3.89 [3.67, 4.12] | 4.13 [3.87, 4.37] | 5.06 [4.71, 5.38] | 7.12 [6.58, 7.63] |
| catseg_native_source | 4.88 | 0.49 | 40.2 | 3.54 [3.31, 3.77] |  |  |  |  |
| catseg_native_frozen_full | 6.90 | 0.60 | 100.0 |  |  |  |  | 4.37 [4.02, 4.74] |
| catseg_native_replay_full | 4.88 | 0.46 | 39.4 |  |  |  |  | 5.96 [5.49, 6.48] |

Brackets are the 2.5-97.5% range of the evaluation mean across splits (splits overlap, so this is spread, not a confidence interval). CRC controls the mean risk over splits; individual splits may exceed alpha. catseg_native_frozen_full reuses the threshold calibrated under the source vocabulary after all labels are added; catseg_native_replay_full recalibrates under the full vocabulary. Stored scores are float16 logits clamped to [-30, 30].