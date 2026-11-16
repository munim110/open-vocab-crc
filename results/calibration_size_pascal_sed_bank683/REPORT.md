# Calibration-set size under source-calibrated thresholds: pascal_sed_bank683

2000 Pascal Context validation images (0 without a source-labelled sampled pixel excluded), 59 source labels, 458 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration pascal_sed_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
Evaluation images: the second half of every permutation (1000 images). Calibration: the first n images of the first half (nested). Headline loss (fraction of source-labelled sampled pixels whose label is missing from the set). CRC needs n >= (1 - alpha)/alpha for a non-trivial threshold; smaller n selects every label.

## alpha = 0.1 (needs n >= 9)

| n_cal | Arm | Mean risk (%) | Split sd (pp) | 90th pct risk (%) | Splits above alpha (%) | Set size | Size sd |
|---:|---|---:|---:|---:|---:|---:|---:|
| 10 | native_frozen | 0.87 | 0.78 | 1.87 | 0.0 | 22.82 | 18.96 |
| 10 | native_replay | 2.32 | 1.78 | 4.85 | 0.2 | 12.11 | 12.45 |
| 10 | anchored_frozen | 2.33 | 1.76 | 4.79 | 0.2 | 11.79 | 10.37 |
| 20 | native_frozen | 2.72 | 1.43 | 4.68 | 0.0 | 8.26 | 3.69 |
| 20 | native_replay | 6.12 | 2.88 | 10.37 | 12.0 | 4.56 | 2.00 |
| 20 | anchored_frozen | 6.17 | 2.90 | 10.05 | 10.4 | 4.70 | 2.10 |
| 50 | native_frozen | 3.88 | 1.18 | 5.51 | 0.0 | 5.73 | 1.21 |
| 50 | native_replay | 8.45 | 2.22 | 11.37 | 24.6 | 3.17 | 0.67 |
| 50 | anchored_frozen | 8.46 | 2.28 | 11.41 | 24.8 | 3.31 | 0.70 |
| 100 | native_frozen | 4.31 | 0.92 | 5.52 | 0.0 | 5.18 | 0.75 |
| 100 | native_replay | 9.20 | 1.67 | 11.43 | 30.8 | 2.89 | 0.41 |
| 100 | anchored_frozen | 9.22 | 1.72 | 11.59 | 31.6 | 3.02 | 0.43 |
| 200 | native_frozen | 4.52 | 0.71 | 5.42 | 0.0 | 4.94 | 0.47 |
| 200 | native_replay | 9.63 | 1.22 | 11.12 | 36.8 | 2.75 | 0.26 |
| 200 | anchored_frozen | 9.61 | 1.24 | 11.20 | 38.6 | 2.89 | 0.26 |
| 400 | native_frozen | 4.61 | 0.54 | 5.31 | 0.0 | 4.84 | 0.30 |
| 400 | native_replay | 9.81 | 0.90 | 11.00 | 39.6 | 2.70 | 0.17 |
| 400 | anchored_frozen | 9.80 | 0.90 | 10.93 | 39.6 | 2.83 | 0.16 |
| 1000 | native_frozen | 4.65 | 0.43 | 5.19 | 0.0 | 4.79 | 0.14 |
| 1000 | native_replay | 9.91 | 0.71 | 10.88 | 44.2 | 2.67 | 0.08 |
| 1000 | anchored_frozen | 9.90 | 0.71 | 10.87 | 44.2 | 2.79 | 0.08 |

## alpha = 0.05 (needs n >= 19)

| n_cal | Arm | Mean risk (%) | Split sd (pp) | 90th pct risk (%) | Splits above alpha (%) | Set size | Size sd |
|---:|---|---:|---:|---:|---:|---:|---:|
| 10 | native_frozen | 0.00 | 0.00 | 0.00 | 0.0 | 458.00 | 0.00 |
| 10 | native_replay | 0.00 | 0.00 | 0.00 | 0.0 | 458.00 | 0.00 |
| 10 | anchored_frozen | 0.00 | 0.00 | 0.00 | 0.0 | 458.00 | 0.00 |
| 20 | native_frozen | 0.22 | 0.21 | 0.48 | 0.0 | 45.14 | 30.05 |
| 20 | native_replay | 0.71 | 0.63 | 1.52 | 0.0 | 24.04 | 20.51 |
| 20 | anchored_frozen | 0.71 | 0.59 | 1.47 | 0.0 | 22.95 | 16.57 |
| 50 | native_frozen | 1.38 | 0.60 | 2.27 | 0.0 | 12.06 | 3.51 |
| 50 | native_replay | 3.38 | 1.37 | 5.23 | 13.0 | 6.60 | 2.02 |
| 50 | anchored_frozen | 3.42 | 1.42 | 5.35 | 13.8 | 6.69 | 2.00 |
| 100 | native_frozen | 1.76 | 0.50 | 2.43 | 0.0 | 9.76 | 1.82 |
| 100 | native_replay | 4.20 | 1.12 | 5.71 | 23.8 | 5.36 | 1.03 |
| 100 | anchored_frozen | 4.24 | 1.19 | 5.80 | 23.2 | 5.49 | 1.09 |
| 200 | native_frozen | 1.95 | 0.40 | 2.45 | 0.0 | 8.91 | 1.02 |
| 200 | native_replay | 4.61 | 0.89 | 5.75 | 32.2 | 4.90 | 0.61 |
| 200 | anchored_frozen | 4.63 | 0.89 | 5.74 | 33.2 | 5.04 | 0.63 |
| 400 | native_frozen | 2.02 | 0.34 | 2.46 | 0.0 | 8.60 | 0.66 |
| 400 | native_replay | 4.79 | 0.68 | 5.70 | 36.2 | 4.72 | 0.38 |
| 400 | anchored_frozen | 4.79 | 0.68 | 5.66 | 36.6 | 4.86 | 0.39 |
| 1000 | native_frozen | 2.07 | 0.28 | 2.42 | 0.0 | 8.43 | 0.31 |
| 1000 | native_replay | 4.90 | 0.52 | 5.54 | 39.4 | 4.62 | 0.17 |
| 1000 | anchored_frozen | 4.90 | 0.50 | 5.53 | 40.0 | 4.76 | 0.17 |

CRC controls the mean of the loss over splits; the spread over splits shrinks with n as usual for split conformal methods. Set size is the mean number of labels per labelled sampled pixel at the grown vocabulary. Stored scores are float16 logits clamped to [-30, 30].