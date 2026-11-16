# Repeated-split calibrated sets from the headroom probe

2000 COCO val2017 (LVIS-annotated) images (development data; 0 without a source-labelled sampled pixel excluded), 171 source labels, 500 random splits per design; thresholds by image-level CRC on the calibration part, everything reported on the rest. Projective arms calibrate once at the source labels. Nothing is fitted; the confirmation reserve is untouched.

## 200 calibration / 1800 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +1112 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 9.60 | 1.08 | 32.6 | 6.20 [4.86, 8.06] | 7.15 [5.50, 9.48] | 9.28 [6.90, 12.71] | 15.82 [11.23, 22.54] | 29.28 [20.28, 42.58] |
| catseg_native_source | 9.60 | 1.11 | 36.4 | 6.30 [4.96, 8.06] |  |  |  |  |
| catseg_native_frozen_full | 16.64 | 1.66 | 100.0 |  |  |  |  | 10.49 [7.49, 14.73] |
| catseg_native_replay_full | 9.62 | 1.15 | 35.6 |  |  |  |  | 28.72 [19.45, 41.25] |

## 200 calibration / 1800 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +1112 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 4.60 | 0.73 | 27.8 | 13.68 [10.39, 17.55] | 16.72 [12.47, 21.74] | 23.48 [17.15, 30.94] | 44.20 [31.42, 59.38] | 85.31 [60.14, 115.19] |
| catseg_native_source | 4.60 | 0.75 | 27.0 | 13.58 [10.55, 17.87] |  |  |  |  |
| catseg_native_frozen_full | 9.30 | 1.06 | 100.0 |  |  |  |  | 30.45 [21.29, 44.57] |
| catseg_native_replay_full | 4.59 | 0.75 | 27.4 |  |  |  |  | 92.13 [62.81, 124.79] |

## 1000 calibration / 1000 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +1112 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 9.89 | 0.65 | 42.6 | 5.86 [5.44, 6.33] | 6.72 [6.19, 7.32] | 8.65 [7.86, 9.54] | 14.57 [13.05, 16.33] | 26.82 [23.80, 30.32] |
| catseg_native_source | 9.89 | 0.65 | 42.6 | 5.98 [5.54, 6.43] |  |  |  |  |
| catseg_native_frozen_full | 17.11 | 0.92 | 100.0 |  |  |  |  | 9.71 [8.76, 10.79] |
| catseg_native_replay_full | 9.91 | 0.66 | 44.0 |  |  |  |  | 26.50 [23.17, 29.66] |

## 1000 calibration / 1000 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +1112 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 4.91 | 0.46 | 41.2 | 12.63 [11.69, 13.73] | 15.35 [14.14, 16.79] | 21.45 [19.61, 23.62] | 40.08 [36.27, 44.41] | 77.21 [69.45, 85.65] |
| catseg_native_source | 4.91 | 0.45 | 41.4 | 12.55 [11.46, 13.76] |  |  |  |  |
| catseg_native_frozen_full | 9.79 | 0.61 | 100.0 |  |  |  |  | 27.12 [23.78, 30.92] |
| catseg_native_replay_full | 4.92 | 0.47 | 42.4 |  |  |  |  | 82.70 [73.05, 94.21] |

Brackets are the 2.5-97.5% range of the evaluation mean across splits (splits overlap, so this is spread, not a confidence interval). CRC controls the mean risk over splits; individual splits may exceed alpha. catseg_native_frozen_full reuses the threshold calibrated under the source vocabulary after all labels are added; catseg_native_replay_full recalibrates under the full vocabulary. Stored scores are float16 logits clamped to [-30, 30].