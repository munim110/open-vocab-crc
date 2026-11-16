# Calibration-set size under source-calibrated thresholds: coco_vitl_bank683

2000 COCO val2017 (LVIS-annotated) images (0 without a source-labelled sampled pixel excluded), 171 source labels, 1283 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration coco_vitl_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
Evaluation images: the second half of every permutation (1000 images). Calibration: the first n images of the first half (nested). Headline loss (fraction of source-labelled sampled pixels whose label is missing from the set). CRC needs n >= (1 - alpha)/alpha for a non-trivial threshold; smaller n selects every label.

## alpha = 0.1 (needs n >= 9)

| n_cal | Arm | Mean risk (%) | Split sd (pp) | 90th pct risk (%) | Splits above alpha (%) | Set size | Size sd |
|---:|---|---:|---:|---:|---:|---:|---:|
| 10 | native_frozen | 3.22 | 2.05 | 6.10 | 0.0 | 13.96 | 22.15 |
| 10 | native_replay | 2.04 | 1.50 | 4.16 | 0.0 | 44.60 | 171.25 |
| 10 | anchored_frozen | 2.03 | 1.49 | 4.21 | 0.0 | 31.57 | 87.49 |
| 20 | native_frozen | 8.07 | 2.81 | 11.61 | 23.8 | 3.59 | 1.57 |
| 20 | native_replay | 5.94 | 2.33 | 8.90 | 4.4 | 4.84 | 2.50 |
| 20 | anchored_frozen | 5.93 | 2.39 | 9.11 | 7.0 | 5.64 | 2.66 |
| 50 | native_frozen | 11.10 | 2.16 | 13.80 | 68.6 | 2.48 | 0.44 |
| 50 | native_replay | 8.48 | 1.88 | 10.80 | 20.8 | 3.17 | 0.67 |
| 50 | anchored_frozen | 8.47 | 1.89 | 10.90 | 20.8 | 3.81 | 0.79 |
| 100 | native_frozen | 12.02 | 1.73 | 14.16 | 86.0 | 2.28 | 0.27 |
| 100 | native_replay | 9.24 | 1.44 | 11.12 | 30.6 | 2.87 | 0.38 |
| 100 | anchored_frozen | 9.23 | 1.45 | 11.07 | 29.6 | 3.46 | 0.44 |
| 200 | native_frozen | 12.53 | 1.33 | 14.22 | 97.2 | 2.19 | 0.18 |
| 200 | native_replay | 9.68 | 1.10 | 11.11 | 38.8 | 2.73 | 0.24 |
| 200 | anchored_frozen | 9.65 | 1.11 | 11.11 | 38.0 | 3.31 | 0.27 |
| 400 | native_frozen | 12.80 | 1.00 | 14.10 | 99.8 | 2.14 | 0.11 |
| 400 | native_replay | 9.89 | 0.83 | 10.95 | 44.2 | 2.67 | 0.14 |
| 400 | anchored_frozen | 9.86 | 0.83 | 11.00 | 41.8 | 3.24 | 0.17 |
| 1000 | native_frozen | 12.88 | 0.79 | 13.81 | 100.0 | 2.13 | 0.06 |
| 1000 | native_replay | 9.95 | 0.68 | 10.73 | 46.2 | 2.65 | 0.07 |
| 1000 | anchored_frozen | 9.92 | 0.68 | 10.77 | 42.4 | 3.21 | 0.09 |

## alpha = 0.05 (needs n >= 19)

| n_cal | Arm | Mean risk (%) | Split sd (pp) | 90th pct risk (%) | Splits above alpha (%) | Set size | Size sd |
|---:|---|---:|---:|---:|---:|---:|---:|
| 10 | native_frozen | 0.00 | 0.00 | 0.00 | 0.0 | 1283.00 | 0.00 |
| 10 | native_replay | 0.00 | 0.00 | 0.00 | 0.0 | 1283.00 | 0.00 |
| 10 | anchored_frozen | 0.00 | 0.00 | 0.00 | 0.0 | 1283.00 | 0.00 |
| 20 | native_frozen | 1.29 | 0.82 | 2.35 | 0.0 | 26.97 | 30.57 |
| 20 | native_replay | 0.69 | 0.52 | 1.44 | 0.0 | 154.28 | 354.30 |
| 20 | anchored_frozen | 0.68 | 0.48 | 1.35 | 0.0 | 65.85 | 126.05 |
| 50 | native_frozen | 5.04 | 1.56 | 7.08 | 51.0 | 5.19 | 1.79 |
| 50 | native_replay | 3.39 | 1.25 | 5.19 | 11.8 | 7.38 | 2.82 |
| 50 | anchored_frozen | 3.40 | 1.26 | 5.09 | 11.4 | 8.34 | 3.03 |
| 100 | native_frozen | 6.03 | 1.23 | 7.59 | 78.2 | 4.21 | 0.78 |
| 100 | native_replay | 4.17 | 1.02 | 5.42 | 21.4 | 5.82 | 1.21 |
| 100 | anchored_frozen | 4.19 | 1.03 | 5.51 | 22.6 | 6.68 | 1.27 |
| 200 | native_frozen | 6.60 | 0.94 | 7.85 | 95.4 | 3.82 | 0.43 |
| 200 | native_replay | 4.61 | 0.78 | 5.66 | 30.8 | 5.23 | 0.70 |
| 200 | anchored_frozen | 4.61 | 0.80 | 5.68 | 31.6 | 6.09 | 0.73 |
| 400 | native_frozen | 6.88 | 0.70 | 7.81 | 99.8 | 3.66 | 0.24 |
| 400 | native_replay | 4.82 | 0.61 | 5.62 | 38.8 | 4.99 | 0.41 |
| 400 | anchored_frozen | 4.81 | 0.61 | 5.63 | 36.4 | 5.84 | 0.43 |
| 1000 | native_frozen | 7.02 | 0.57 | 7.70 | 100.0 | 3.59 | 0.12 |
| 1000 | native_replay | 4.92 | 0.50 | 5.58 | 43.6 | 4.88 | 0.22 |
| 1000 | anchored_frozen | 4.90 | 0.50 | 5.55 | 42.8 | 5.74 | 0.23 |

CRC controls the mean of the loss over splits; the spread over splits shrinks with n as usual for split conformal methods. Set size is the mean number of labels per labelled sampled pixel at the grown vocabulary. Stored scores are float16 logits clamped to [-30, 30].