# Calibration-set size under source-calibrated thresholds: coco_vitb_bank683

2000 COCO val2017 (LVIS-annotated) images (0 without a source-labelled sampled pixel excluded), 171 source labels, 1283 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration coco_vitb_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
Evaluation images: the second half of every permutation (1000 images). Calibration: the first n images of the first half (nested). Headline loss (fraction of source-labelled sampled pixels whose label is missing from the set). CRC needs n >= (1 - alpha)/alpha for a non-trivial threshold; smaller n selects every label.

## alpha = 0.1 (needs n >= 9)

| n_cal | Arm | Mean risk (%) | Split sd (pp) | 90th pct risk (%) | Splits above alpha (%) | Set size | Size sd |
|---:|---|---:|---:|---:|---:|---:|---:|
| 10 | native_frozen | 3.04 | 1.96 | 5.81 | 0.2 | 17.94 | 24.95 |
| 10 | native_replay | 1.91 | 1.38 | 3.63 | 0.0 | 88.02 | 271.48 |
| 10 | anchored_frozen | 1.91 | 1.34 | 3.77 | 0.0 | 37.29 | 75.26 |
| 20 | native_frozen | 8.04 | 2.85 | 11.67 | 24.2 | 4.37 | 2.25 |
| 20 | native_replay | 5.93 | 2.33 | 8.87 | 5.4 | 6.04 | 4.10 |
| 20 | anchored_frozen | 5.90 | 2.30 | 8.93 | 4.6 | 7.09 | 4.27 |
| 50 | native_frozen | 11.15 | 2.13 | 13.93 | 71.0 | 2.86 | 0.58 |
| 50 | native_replay | 8.46 | 1.89 | 11.00 | 20.8 | 3.77 | 0.83 |
| 50 | anchored_frozen | 8.43 | 1.83 | 10.94 | 19.2 | 4.59 | 0.95 |
| 100 | native_frozen | 12.12 | 1.63 | 14.25 | 89.8 | 2.58 | 0.33 |
| 100 | native_replay | 9.23 | 1.46 | 11.10 | 29.6 | 3.39 | 0.49 |
| 100 | anchored_frozen | 9.22 | 1.42 | 11.02 | 28.6 | 4.15 | 0.54 |
| 200 | native_frozen | 12.64 | 1.26 | 14.30 | 97.6 | 2.46 | 0.21 |
| 200 | native_replay | 9.67 | 1.11 | 11.09 | 39.4 | 3.21 | 0.31 |
| 200 | anchored_frozen | 9.67 | 1.08 | 11.01 | 39.6 | 3.94 | 0.34 |
| 400 | native_frozen | 12.87 | 0.97 | 14.13 | 99.8 | 2.40 | 0.13 |
| 400 | native_replay | 9.88 | 0.86 | 10.97 | 44.0 | 3.12 | 0.19 |
| 400 | anchored_frozen | 9.86 | 0.83 | 10.88 | 44.0 | 3.86 | 0.21 |
| 1000 | native_frozen | 12.96 | 0.77 | 13.92 | 100.0 | 2.38 | 0.07 |
| 1000 | native_replay | 9.94 | 0.70 | 10.85 | 45.8 | 3.09 | 0.10 |
| 1000 | anchored_frozen | 9.92 | 0.68 | 10.74 | 44.4 | 3.83 | 0.12 |

## alpha = 0.05 (needs n >= 19)

| n_cal | Arm | Mean risk (%) | Split sd (pp) | 90th pct risk (%) | Splits above alpha (%) | Set size | Size sd |
|---:|---|---:|---:|---:|---:|---:|---:|
| 10 | native_frozen | 0.00 | 0.00 | 0.00 | 0.0 | 1283.00 | 0.00 |
| 10 | native_replay | 0.00 | 0.00 | 0.00 | 0.0 | 1283.00 | 0.00 |
| 10 | anchored_frozen | 0.00 | 0.00 | 0.00 | 0.0 | 1283.00 | 0.00 |
| 20 | native_frozen | 1.23 | 0.75 | 2.22 | 0.0 | 35.21 | 36.68 |
| 20 | native_replay | 0.65 | 0.48 | 1.25 | 0.0 | 227.05 | 432.52 |
| 20 | anchored_frozen | 0.65 | 0.46 | 1.21 | 0.0 | 82.88 | 123.78 |
| 50 | native_frozen | 4.90 | 1.62 | 6.92 | 44.6 | 6.63 | 2.54 |
| 50 | native_replay | 3.36 | 1.23 | 4.97 | 9.6 | 9.40 | 3.75 |
| 50 | anchored_frozen | 3.33 | 1.22 | 5.04 | 10.6 | 10.83 | 4.15 |
| 100 | native_frozen | 5.96 | 1.27 | 7.62 | 77.2 | 5.18 | 1.05 |
| 100 | native_replay | 4.17 | 1.00 | 5.39 | 19.6 | 7.20 | 1.57 |
| 100 | anchored_frozen | 4.17 | 1.00 | 5.47 | 20.8 | 8.40 | 1.70 |
| 200 | native_frozen | 6.56 | 1.01 | 7.89 | 94.2 | 4.66 | 0.60 |
| 200 | native_replay | 4.62 | 0.76 | 5.61 | 32.6 | 6.40 | 0.89 |
| 200 | anchored_frozen | 4.63 | 0.78 | 5.65 | 31.2 | 7.56 | 0.95 |
| 400 | native_frozen | 6.83 | 0.77 | 7.81 | 99.6 | 4.44 | 0.35 |
| 400 | native_replay | 4.82 | 0.59 | 5.62 | 38.0 | 6.08 | 0.50 |
| 400 | anchored_frozen | 4.83 | 0.60 | 5.63 | 34.4 | 7.24 | 0.54 |
| 1000 | native_frozen | 6.96 | 0.62 | 7.69 | 100.0 | 4.35 | 0.18 |
| 1000 | native_replay | 4.92 | 0.48 | 5.52 | 42.4 | 5.94 | 0.25 |
| 1000 | anchored_frozen | 4.92 | 0.48 | 5.55 | 39.6 | 7.11 | 0.27 |

CRC controls the mean of the loss over splits; the spread over splits shrinks with n as usual for split conformal methods. Set size is the mean number of labels per labelled sampled pixel at the grown vocabulary. Stored scores are float16 logits clamped to [-30, 30].