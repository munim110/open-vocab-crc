# Calibration-set size under source-calibrated thresholds: pascal_vitl_bank683

2000 Pascal Context validation images (0 without a source-labelled sampled pixel excluded), 59 source labels, 458 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration pascal_vitl_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
Evaluation images: the second half of every permutation (1000 images). Calibration: the first n images of the first half (nested). Headline loss (fraction of source-labelled sampled pixels whose label is missing from the set). CRC needs n >= (1 - alpha)/alpha for a non-trivial threshold; smaller n selects every label.

## alpha = 0.1 (needs n >= 9)

| n_cal | Arm | Mean risk (%) | Split sd (pp) | 90th pct risk (%) | Splits above alpha (%) | Set size | Size sd |
|---:|---|---:|---:|---:|---:|---:|---:|
| 10 | native_frozen | 4.13 | 2.71 | 7.85 | 4.8 | 5.42 | 3.75 |
| 10 | native_replay | 2.27 | 1.77 | 4.44 | 0.0 | 10.37 | 12.81 |
| 10 | anchored_frozen | 2.30 | 1.82 | 4.82 | 0.0 | 9.59 | 8.90 |
| 20 | native_frozen | 10.10 | 3.69 | 14.68 | 49.4 | 2.23 | 0.77 |
| 20 | native_replay | 6.20 | 2.88 | 10.04 | 10.4 | 3.35 | 1.44 |
| 20 | anchored_frozen | 6.17 | 2.88 | 10.30 | 12.4 | 3.64 | 1.53 |
| 50 | native_frozen | 13.22 | 2.64 | 16.61 | 88.6 | 1.69 | 0.27 |
| 50 | native_replay | 8.41 | 2.18 | 11.20 | 24.0 | 2.41 | 0.44 |
| 50 | anchored_frozen | 8.43 | 2.24 | 11.19 | 22.2 | 2.67 | 0.47 |
| 100 | native_frozen | 14.26 | 2.03 | 16.74 | 97.8 | 1.57 | 0.17 |
| 100 | native_replay | 9.23 | 1.69 | 11.45 | 30.4 | 2.21 | 0.28 |
| 100 | anchored_frozen | 9.23 | 1.71 | 11.50 | 30.0 | 2.47 | 0.28 |
| 200 | native_frozen | 14.75 | 1.40 | 16.49 | 100.0 | 1.52 | 0.10 |
| 200 | native_replay | 9.63 | 1.21 | 11.10 | 36.8 | 2.12 | 0.17 |
| 200 | anchored_frozen | 9.66 | 1.28 | 11.43 | 37.2 | 2.38 | 0.17 |
| 400 | native_frozen | 14.96 | 1.09 | 16.36 | 100.0 | 1.50 | 0.07 |
| 400 | native_replay | 9.79 | 0.94 | 11.01 | 40.8 | 2.09 | 0.11 |
| 400 | anchored_frozen | 9.82 | 0.97 | 11.10 | 42.4 | 2.35 | 0.11 |
| 1000 | native_frozen | 15.05 | 0.83 | 16.14 | 100.0 | 1.49 | 0.03 |
| 1000 | native_replay | 9.88 | 0.73 | 10.81 | 42.8 | 2.07 | 0.05 |
| 1000 | anchored_frozen | 9.90 | 0.76 | 10.90 | 44.4 | 2.33 | 0.06 |

## alpha = 0.05 (needs n >= 19)

| n_cal | Arm | Mean risk (%) | Split sd (pp) | 90th pct risk (%) | Splits above alpha (%) | Set size | Size sd |
|---:|---|---:|---:|---:|---:|---:|---:|
| 10 | native_frozen | 0.00 | 0.00 | 0.00 | 0.0 | 458.00 | 0.00 |
| 10 | native_replay | 0.00 | 0.00 | 0.00 | 0.0 | 458.00 | 0.00 |
| 10 | anchored_frozen | 0.00 | 0.00 | 0.00 | 0.0 | 458.00 | 0.00 |
| 20 | native_frozen | 1.69 | 1.12 | 3.19 | 1.4 | 9.91 | 6.80 |
| 20 | native_replay | 0.74 | 0.64 | 1.58 | 0.0 | 23.47 | 27.80 |
| 20 | anchored_frozen | 0.75 | 0.62 | 1.57 | 0.0 | 20.08 | 20.02 |
| 50 | native_frozen | 6.15 | 2.09 | 9.15 | 68.4 | 3.10 | 0.83 |
| 50 | native_replay | 3.31 | 1.33 | 5.12 | 11.2 | 4.96 | 1.54 |
| 50 | anchored_frozen | 3.31 | 1.34 | 5.21 | 12.8 | 5.16 | 1.53 |
| 100 | native_frozen | 7.47 | 1.64 | 9.60 | 94.4 | 2.59 | 0.39 |
| 100 | native_replay | 4.17 | 1.12 | 5.64 | 20.4 | 3.96 | 0.75 |
| 100 | anchored_frozen | 4.18 | 1.16 | 5.63 | 24.2 | 4.20 | 0.77 |
| 200 | native_frozen | 8.06 | 1.21 | 9.55 | 99.8 | 2.42 | 0.23 |
| 200 | native_replay | 4.58 | 0.87 | 5.66 | 29.6 | 3.60 | 0.43 |
| 200 | anchored_frozen | 4.60 | 0.89 | 5.73 | 32.6 | 3.87 | 0.43 |
| 400 | native_frozen | 8.40 | 0.92 | 9.55 | 100.0 | 2.34 | 0.14 |
| 400 | native_replay | 4.80 | 0.68 | 5.66 | 36.4 | 3.45 | 0.26 |
| 400 | anchored_frozen | 4.80 | 0.69 | 5.77 | 35.8 | 3.73 | 0.28 |
| 1000 | native_frozen | 8.56 | 0.68 | 9.47 | 100.0 | 2.30 | 0.07 |
| 1000 | native_replay | 4.91 | 0.52 | 5.59 | 42.0 | 3.37 | 0.12 |
| 1000 | anchored_frozen | 4.89 | 0.52 | 5.58 | 41.0 | 3.66 | 0.13 |

CRC controls the mean of the loss over splits; the spread over splits shrinks with n as usual for split conformal methods. Set size is the mean number of labels per labelled sampled pixel at the grown vocabulary. Stored scores are float16 logits clamped to [-30, 30].