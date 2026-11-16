# Calibration-set size under source-calibrated thresholds: coco_declip_bank683

2000 COCO val2017 (LVIS-annotated) images (0 without a source-labelled sampled pixel excluded), 171 source labels, 1283 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration coco_declip_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
Evaluation images: the second half of every permutation (1000 images). Calibration: the first n images of the first half (nested). Headline loss (fraction of source-labelled sampled pixels whose label is missing from the set). CRC needs n >= (1 - alpha)/alpha for a non-trivial threshold; smaller n selects every label.

## alpha = 0.1 (needs n >= 9)

| n_cal | Arm | Mean risk (%) | Split sd (pp) | 90th pct risk (%) | Splits above alpha (%) | Set size | Size sd |
|---:|---|---:|---:|---:|---:|---:|---:|
| 10 | native_frozen | 3.13 | 2.06 | 6.06 | 0.4 | 13.83 | 20.87 |
| 10 | native_replay | 2.03 | 1.52 | 4.17 | 0.0 | 55.24 | 210.73 |
| 10 | anchored_frozen | 1.99 | 1.46 | 4.15 | 0.0 | 28.82 | 65.02 |
| 20 | native_frozen | 7.99 | 2.86 | 11.81 | 24.8 | 3.58 | 1.56 |
| 20 | native_replay | 5.86 | 2.38 | 9.06 | 4.8 | 4.83 | 2.49 |
| 20 | anchored_frozen | 5.85 | 2.30 | 9.03 | 5.4 | 5.58 | 2.74 |
| 50 | native_frozen | 11.18 | 2.17 | 13.72 | 72.2 | 2.43 | 0.44 |
| 50 | native_replay | 8.44 | 1.90 | 10.92 | 20.8 | 3.14 | 0.66 |
| 50 | anchored_frozen | 8.44 | 1.87 | 10.74 | 19.0 | 3.76 | 0.74 |
| 100 | native_frozen | 12.12 | 1.64 | 14.20 | 90.4 | 2.23 | 0.26 |
| 100 | native_replay | 9.24 | 1.43 | 11.17 | 29.8 | 2.84 | 0.35 |
| 100 | anchored_frozen | 9.21 | 1.38 | 10.93 | 28.4 | 3.43 | 0.40 |
| 200 | native_frozen | 12.60 | 1.24 | 14.22 | 98.2 | 2.13 | 0.17 |
| 200 | native_replay | 9.66 | 1.09 | 11.02 | 38.6 | 2.71 | 0.23 |
| 200 | anchored_frozen | 9.63 | 1.08 | 10.96 | 37.8 | 3.28 | 0.25 |
| 400 | native_frozen | 12.85 | 0.96 | 14.09 | 99.8 | 2.09 | 0.11 |
| 400 | native_replay | 9.88 | 0.83 | 11.00 | 41.4 | 2.65 | 0.14 |
| 400 | anchored_frozen | 9.84 | 0.83 | 10.90 | 42.8 | 3.21 | 0.16 |
| 1000 | native_frozen | 12.93 | 0.77 | 13.97 | 100.0 | 2.07 | 0.06 |
| 1000 | native_replay | 9.94 | 0.68 | 10.74 | 46.0 | 2.63 | 0.08 |
| 1000 | anchored_frozen | 9.90 | 0.68 | 10.76 | 43.6 | 3.19 | 0.09 |

## alpha = 0.05 (needs n >= 19)

| n_cal | Arm | Mean risk (%) | Split sd (pp) | 90th pct risk (%) | Splits above alpha (%) | Set size | Size sd |
|---:|---|---:|---:|---:|---:|---:|---:|
| 10 | native_frozen | 0.00 | 0.00 | 0.00 | 0.0 | 1283.00 | 0.00 |
| 10 | native_replay | 0.00 | 0.00 | 0.00 | 0.0 | 1283.00 | 0.00 |
| 10 | anchored_frozen | 0.00 | 0.00 | 0.00 | 0.0 | 1283.00 | 0.00 |
| 20 | native_frozen | 1.21 | 0.74 | 2.16 | 0.0 | 26.08 | 27.64 |
| 20 | native_replay | 0.67 | 0.48 | 1.31 | 0.0 | 186.29 | 403.62 |
| 20 | anchored_frozen | 0.66 | 0.44 | 1.29 | 0.0 | 60.01 | 95.88 |
| 50 | native_frozen | 4.97 | 1.58 | 7.02 | 49.6 | 5.21 | 1.83 |
| 50 | native_replay | 3.40 | 1.27 | 5.16 | 12.2 | 7.32 | 2.89 |
| 50 | anchored_frozen | 3.38 | 1.25 | 5.06 | 11.4 | 8.18 | 2.92 |
| 100 | native_frozen | 5.96 | 1.16 | 7.33 | 78.8 | 4.19 | 0.73 |
| 100 | native_replay | 4.17 | 0.97 | 5.43 | 19.8 | 5.73 | 1.09 |
| 100 | anchored_frozen | 4.17 | 0.99 | 5.40 | 19.4 | 6.57 | 1.14 |
| 200 | native_frozen | 6.49 | 0.92 | 7.71 | 95.4 | 3.82 | 0.42 |
| 200 | native_replay | 4.61 | 0.78 | 5.63 | 33.6 | 5.17 | 0.66 |
| 200 | anchored_frozen | 4.63 | 0.77 | 5.61 | 33.4 | 5.98 | 0.67 |
| 400 | native_frozen | 6.73 | 0.71 | 7.69 | 99.6 | 3.67 | 0.25 |
| 400 | native_replay | 4.82 | 0.61 | 5.62 | 39.0 | 4.94 | 0.41 |
| 400 | anchored_frozen | 4.83 | 0.60 | 5.62 | 39.6 | 5.76 | 0.41 |
| 1000 | native_frozen | 6.83 | 0.57 | 7.54 | 99.8 | 3.60 | 0.13 |
| 1000 | native_replay | 4.92 | 0.49 | 5.56 | 43.4 | 4.83 | 0.21 |
| 1000 | anchored_frozen | 4.92 | 0.49 | 5.60 | 43.8 | 5.66 | 0.21 |

CRC controls the mean of the loss over splits; the spread over splits shrinks with n as usual for split conformal methods. Set size is the mean number of labels per labelled sampled pixel at the grown vocabulary. Stored scores are float16 logits clamped to [-30, 30].