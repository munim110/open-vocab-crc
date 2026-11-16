# Repeated-split calibrated sets from the headroom probe

2000 ADE validation images (development data; 0 without a source-labelled sampled pixel excluded), 150 source labels, 500 random splits per design; thresholds by image-level CRC on the calibration part, everything reported on the rest. Projective arms calibrate once at the source labels. Nothing is fitted; the confirmation reserve is untouched.

## 200 calibration / 1800 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 9.51 | 1.07 | 31.8 | 2.87 [2.47, 3.40] | 3.35 [2.84, 4.03] | 4.01 [3.34, 4.91] | 5.93 [4.81, 7.46] | 6.33 [5.09, 8.01] |
| catseg_native_source | 9.52 | 0.98 | 30.6 | 2.41 [2.04, 2.85] |  |  |  |  |
| catseg_native_frozen_full | 14.84 | 1.31 | 100.0 |  |  |  |  | 2.89 [2.33, 3.58] |
| catseg_native_replay_full | 9.53 | 1.09 | 34.4 |  |  |  |  | 5.34 [4.03, 6.99] |

## 200 calibration / 1800 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 4.50 | 0.72 | 24.4 | 5.62 [4.34, 6.96] | 6.96 [5.26, 8.77] | 8.99 [6.60, 11.56] | 14.54 [10.39, 19.05] | 16.01 [11.30, 21.17] |
| catseg_native_source | 4.49 | 0.70 | 21.8 | 5.00 [3.82, 6.41] |  |  |  |  |
| catseg_native_frozen_full | 7.55 | 1.02 | 100.0 |  |  |  |  | 7.42 [5.26, 10.11] |
| catseg_native_replay_full | 4.49 | 0.75 | 25.4 |  |  |  |  | 15.19 [10.17, 21.01] |

## 1000 calibration / 1000 evaluation images, alpha = 0.1

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 9.88 | 0.67 | 40.6 | 2.76 [2.61, 2.91] | 3.21 [3.02, 3.40] | 3.82 [3.57, 4.07] | 5.62 [5.20, 6.03] | 5.98 [5.53, 6.43] |
| catseg_native_source | 9.86 | 0.63 | 37.0 | 2.31 [2.20, 2.43] |  |  |  |  |
| catseg_native_frozen_full | 15.36 | 0.79 | 100.0 |  |  |  |  | 2.73 [2.55, 2.92] |
| catseg_native_replay_full | 9.88 | 0.67 | 41.0 |  |  |  |  | 4.99 [4.56, 5.43] |

## 1000 calibration / 1000 evaluation images, alpha = 0.05

| Arm | Mean risk (%) | Split sd (pp) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_anchored | 4.89 | 0.48 | 40.2 | 5.15 [4.70, 5.64] | 6.34 [5.75, 6.97] | 8.11 [7.28, 8.99] | 13.00 [11.56, 14.54] | 14.25 [12.62, 16.00] |
| catseg_native_source | 4.88 | 0.45 | 37.2 | 4.54 [4.16, 4.96] |  |  |  |  |
| catseg_native_frozen_full | 8.14 | 0.62 | 100.0 |  |  |  |  | 6.56 [5.85, 7.35] |
| catseg_native_replay_full | 4.89 | 0.48 | 41.0 |  |  |  |  | 13.29 [11.70, 15.06] |

Brackets are the 2.5-97.5% range of the evaluation mean across splits (splits overlap, so this is spread, not a confidence interval). CRC controls the mean risk over splits; individual splits may exceed alpha. catseg_native_frozen_full reuses the threshold calibrated under the source vocabulary after all labels are added; catseg_native_replay_full recalibrates under the full vocabulary. Stored scores are float16 logits clamped to [-30, 30].