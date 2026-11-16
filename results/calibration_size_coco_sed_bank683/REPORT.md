# Calibration-set size under source-calibrated thresholds: coco_sed_bank683

2000 COCO val2017 (LVIS-annotated) images (0 without a source-labelled sampled pixel excluded), 171 source labels, 1283 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration coco_sed_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
Evaluation images: the second half of every permutation (1000 images). Calibration: the first n images of the first half (nested). Headline loss (fraction of source-labelled sampled pixels whose label is missing from the set). CRC needs n >= (1 - alpha)/alpha for a non-trivial threshold; smaller n selects every label.

## alpha = 0.1 (needs n >= 9)

| n_cal | Arm | Mean risk (%) | Split sd (pp) | 90th pct risk (%) | Splits above alpha (%) | Set size | Size sd |
|---:|---|---:|---:|---:|---:|---:|---:|
| 10 | native_frozen | 0.69 | 0.48 | 1.30 | 0.0 | 64.32 | 114.52 |
| 10 | native_replay | 1.93 | 1.33 | 3.75 | 0.0 | 24.12 | 34.18 |
| 10 | anchored_frozen | 1.94 | 1.38 | 3.93 | 0.0 | 28.81 | 78.75 |
| 20 | native_frozen | 2.00 | 0.90 | 3.15 | 0.0 | 14.41 | 6.72 |
| 20 | native_replay | 5.90 | 2.39 | 9.05 | 5.0 | 6.41 | 3.23 |
| 20 | anchored_frozen | 5.87 | 2.39 | 9.10 | 5.6 | 6.17 | 3.29 |
| 50 | native_frozen | 3.00 | 0.82 | 4.04 | 0.0 | 9.75 | 1.99 |
| 50 | native_replay | 8.44 | 1.92 | 10.94 | 21.0 | 4.38 | 0.81 |
| 50 | anchored_frozen | 8.49 | 1.95 | 11.15 | 21.2 | 4.17 | 0.80 |
| 100 | native_frozen | 3.31 | 0.65 | 4.17 | 0.0 | 8.89 | 1.18 |
| 100 | native_replay | 9.21 | 1.44 | 11.11 | 28.8 | 4.01 | 0.46 |
| 100 | anchored_frozen | 9.24 | 1.44 | 11.09 | 29.2 | 3.81 | 0.46 |
| 200 | native_frozen | 3.49 | 0.52 | 4.14 | 0.0 | 8.49 | 0.79 |
| 200 | native_replay | 9.66 | 1.11 | 11.05 | 36.8 | 3.84 | 0.29 |
| 200 | anchored_frozen | 9.65 | 1.11 | 11.18 | 34.4 | 3.65 | 0.29 |
| 400 | native_frozen | 3.59 | 0.41 | 4.12 | 0.0 | 8.28 | 0.51 |
| 400 | native_replay | 9.85 | 0.83 | 10.95 | 41.4 | 3.77 | 0.18 |
| 400 | anchored_frozen | 9.84 | 0.85 | 10.96 | 39.8 | 3.58 | 0.18 |
| 1000 | native_frozen | 3.64 | 0.34 | 4.09 | 0.0 | 8.19 | 0.27 |
| 1000 | native_replay | 9.92 | 0.67 | 10.77 | 44.6 | 3.74 | 0.09 |
| 1000 | anchored_frozen | 9.92 | 0.69 | 10.78 | 45.0 | 3.55 | 0.10 |

## alpha = 0.05 (needs n >= 19)

| n_cal | Arm | Mean risk (%) | Split sd (pp) | 90th pct risk (%) | Splits above alpha (%) | Set size | Size sd |
|---:|---|---:|---:|---:|---:|---:|---:|
| 10 | native_frozen | 0.00 | 0.00 | 0.00 | 0.0 | 1283.00 | 0.00 |
| 10 | native_replay | 0.00 | 0.00 | 0.00 | 0.0 | 1283.00 | 0.00 |
| 10 | anchored_frozen | 0.00 | 0.00 | 0.00 | 0.0 | 1283.00 | 0.00 |
| 20 | native_frozen | 0.26 | 0.20 | 0.52 | 0.0 | 129.19 | 163.38 |
| 20 | native_replay | 0.66 | 0.46 | 1.28 | 0.0 | 49.88 | 53.29 |
| 20 | anchored_frozen | 0.67 | 0.47 | 1.27 | 0.0 | 58.22 | 114.62 |
| 50 | native_frozen | 1.12 | 0.40 | 1.64 | 0.0 | 20.95 | 7.36 |
| 50 | native_replay | 3.34 | 1.19 | 4.95 | 9.6 | 9.43 | 3.08 |
| 50 | anchored_frozen | 3.34 | 1.22 | 4.89 | 9.0 | 9.05 | 3.32 |
| 100 | native_frozen | 1.36 | 0.35 | 1.81 | 0.0 | 17.10 | 3.15 |
| 100 | native_replay | 4.15 | 0.97 | 5.41 | 19.0 | 7.60 | 1.36 |
| 100 | anchored_frozen | 4.14 | 0.98 | 5.37 | 19.6 | 7.22 | 1.32 |
| 200 | native_frozen | 1.51 | 0.29 | 1.88 | 0.0 | 15.55 | 1.85 |
| 200 | native_replay | 4.60 | 0.79 | 5.65 | 30.4 | 6.91 | 0.85 |
| 200 | anchored_frozen | 4.61 | 0.77 | 5.61 | 31.2 | 6.54 | 0.73 |
| 400 | native_frozen | 1.58 | 0.23 | 1.88 | 0.0 | 14.91 | 1.11 |
| 400 | native_replay | 4.81 | 0.59 | 5.61 | 35.0 | 6.61 | 0.49 |
| 400 | anchored_frozen | 4.81 | 0.59 | 5.59 | 36.6 | 6.29 | 0.43 |
| 1000 | native_frozen | 1.62 | 0.20 | 1.88 | 0.0 | 14.61 | 0.56 |
| 1000 | native_replay | 4.91 | 0.47 | 5.57 | 39.6 | 6.47 | 0.24 |
| 1000 | anchored_frozen | 4.92 | 0.48 | 5.60 | 43.4 | 6.16 | 0.23 |

CRC controls the mean of the loss over splits; the spread over splits shrinks with n as usual for split conformal methods. Set size is the mean number of labels per labelled sampled pixel at the grown vocabulary. Stored scores are float16 logits clamped to [-30, 30].