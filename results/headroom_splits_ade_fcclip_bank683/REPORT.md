# Repeated-split calibrated sets from the headroom probe

2000 ADE validation images (development data; 0 without a source-labelled sampled pixel excluded), 150 source labels, 500 random splits per design; thresholds by image-level CRC on the calibration part, everything reported on the rest. Projective arms calibrate once at the source labels. Nothing is fitted; the confirmation reserve is untouched.

## 200 calibration / 1800 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 9.45 | 1.04 | 30.0 | 4.02 [3.31, 4.95] | 5.14 [4.20, 6.37] | 6.63 [5.31, 8.37] | 10.76 [8.40, 13.90] | 12.05 [9.31, 15.71] |
| catseg_native_source | 9.48 | 1.03 | 29.2 | 3.39 [2.75, 4.11] |  |  |  |  |
| catseg_native_frozen_full | 13.25 | 1.40 | 99.8 |  |  |  |  | 5.53 [4.27, 6.97] |
| catseg_native_replay_full | 9.45 | 1.12 | 28.0 |  |  |  |  | 8.88 [6.55, 11.93] |

## 200 calibration / 1800 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 4.51 | 0.76 | 27.0 | 10.05 [6.92, 14.87] | 13.01 [8.94, 19.25] | 17.96 [12.06, 27.04] | 31.66 [20.62, 48.93] | 36.84 [23.60, 57.77] |
| catseg_native_source | 4.51 | 0.77 | 25.8 | 8.89 [5.66, 13.02] |  |  |  |  |
| catseg_native_frozen_full | 6.22 | 1.09 | 90.2 |  |  |  |  | 17.68 [10.25, 27.84] |
| catseg_native_replay_full | 4.52 | 0.80 | 27.4 |  |  |  |  | 31.15 [17.59, 50.53] |

## 1000 calibration / 1000 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 9.85 | 0.62 | 38.4 | 3.80 [3.55, 4.04] | 4.84 [4.52, 5.16] | 6.21 [5.76, 6.67] | 10.01 [9.20, 10.84] | 11.18 [10.24, 12.13] |
| catseg_native_source | 9.85 | 0.61 | 37.2 | 3.22 [3.03, 3.42] |  |  |  |  |
| catseg_native_frozen_full | 13.76 | 0.76 | 100.0 |  |  |  |  | 5.19 [4.81, 5.56] |
| catseg_native_replay_full | 9.87 | 0.64 | 41.4 |  |  |  |  | 8.18 [7.47, 8.94] |

## 1000 calibration / 1000 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 4.87 | 0.50 | 35.8 | 8.73 [7.69, 9.95] | 11.31 [9.94, 12.91] | 15.48 [13.49, 17.85] | 26.98 [23.29, 31.43] | 31.19 [26.78, 36.50] |
| catseg_native_source | 4.88 | 0.45 | 35.0 | 7.60 [6.63, 8.65] |  |  |  |  |
| catseg_native_frozen_full | 6.76 | 0.61 | 99.8 |  |  |  |  | 14.53 [12.31, 16.99] |
| catseg_native_replay_full | 4.89 | 0.49 | 40.2 |  |  |  |  | 25.65 [21.26, 30.26] |

Brackets are the 2.5-97.5% range of the evaluation mean across splits (splits overlap, so this is spread, not a confidence interval). CRC controls the mean risk over splits; individual splits may exceed alpha. catseg_native_frozen_full reuses the threshold calibrated under the source vocabulary after all labels are added; catseg_native_replay_full recalibrates under the full vocabulary. Stored scores are float16 logits clamped to [-30, 30].