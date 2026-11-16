# Calibration-set size under source-calibrated thresholds: declip_bank683

2000 ADE validation images (0 without a source-labelled sampled pixel excluded), 150 source labels, 845 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration declip_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
Evaluation images: the second half of every permutation (1000 images). Calibration: the first n images of the first half (nested). Headline loss (fraction of source-labelled sampled pixels whose label is missing from the set). CRC needs n >= (1 - alpha)/alpha for a non-trivial threshold; smaller n selects every label.

## alpha = 0.1 (needs n >= 9)

| n_cal | Arm | Mean risk (%) | Split sd (pp) | 90th pct risk (%) | Splits above alpha (%) | Set size | Size sd |
|---:|---|---:|---:|---:|---:|---:|---:|
| 10 | native_frozen | 3.71 | 2.23 | 6.88 | 1.0 | 18.62 | 19.50 |
| 10 | native_replay | 2.19 | 1.62 | 4.47 | 0.0 | 119.09 | 257.43 |
| 10 | anchored_frozen | 2.23 | 1.62 | 4.53 | 0.0 | 37.09 | 39.79 |
| 20 | native_frozen | 9.48 | 3.52 | 13.97 | 45.4 | 4.45 | 2.85 |
| 20 | native_replay | 6.04 | 2.58 | 9.52 | 7.0 | 7.86 | 5.55 |
| 20 | anchored_frozen | 6.17 | 2.74 | 10.17 | 11.2 | 8.92 | 5.49 |
| 50 | native_frozen | 12.66 | 2.38 | 15.67 | 86.8 | 2.67 | 0.63 |
| 50 | native_replay | 8.30 | 1.94 | 10.79 | 18.6 | 4.45 | 1.37 |
| 50 | anchored_frozen | 8.33 | 2.01 | 10.93 | 21.8 | 5.47 | 1.41 |
| 100 | native_frozen | 13.74 | 1.85 | 16.10 | 98.6 | 2.38 | 0.33 |
| 100 | native_replay | 9.16 | 1.54 | 11.14 | 27.2 | 3.80 | 0.67 |
| 100 | anchored_frozen | 9.12 | 1.55 | 11.12 | 27.2 | 4.84 | 0.75 |
| 200 | native_frozen | 14.24 | 1.35 | 16.07 | 100.0 | 2.26 | 0.21 |
| 200 | native_replay | 9.54 | 1.17 | 11.15 | 34.8 | 3.58 | 0.44 |
| 200 | anchored_frozen | 9.50 | 1.17 | 11.10 | 33.8 | 4.59 | 0.48 |
| 400 | native_frozen | 14.60 | 1.08 | 15.99 | 100.0 | 2.19 | 0.14 |
| 400 | native_replay | 9.82 | 0.91 | 11.02 | 39.8 | 3.44 | 0.28 |
| 400 | anchored_frozen | 9.80 | 0.92 | 11.03 | 41.2 | 4.43 | 0.31 |
| 1000 | native_frozen | 14.72 | 0.76 | 15.72 | 100.0 | 2.17 | 0.06 |
| 1000 | native_replay | 9.92 | 0.65 | 10.74 | 43.2 | 3.38 | 0.12 |
| 1000 | anchored_frozen | 9.89 | 0.66 | 10.75 | 44.8 | 4.37 | 0.14 |

## alpha = 0.05 (needs n >= 19)

| n_cal | Arm | Mean risk (%) | Split sd (pp) | 90th pct risk (%) | Splits above alpha (%) | Set size | Size sd |
|---:|---|---:|---:|---:|---:|---:|---:|
| 10 | native_frozen | 0.00 | 0.00 | 0.00 | 0.0 | 845.00 | 0.00 |
| 10 | native_replay | 0.00 | 0.00 | 0.00 | 0.0 | 845.00 | 0.00 |
| 10 | anchored_frozen | 0.00 | 0.00 | 0.00 | 0.0 | 845.00 | 0.00 |
| 20 | native_frozen | 1.64 | 0.90 | 2.82 | 0.2 | 35.76 | 26.06 |
| 20 | native_replay | 0.80 | 0.64 | 1.66 | 0.0 | 224.80 | 319.22 |
| 20 | anchored_frozen | 0.75 | 0.58 | 1.53 | 0.0 | 74.79 | 57.63 |
| 50 | native_frozen | 5.47 | 1.68 | 7.72 | 60.0 | 7.59 | 3.19 |
| 50 | native_replay | 3.25 | 1.21 | 4.81 | 7.2 | 14.30 | 7.34 |
| 50 | anchored_frozen | 3.24 | 1.16 | 4.77 | 7.4 | 15.75 | 6.78 |
| 100 | native_frozen | 6.72 | 1.44 | 8.62 | 88.8 | 5.57 | 1.41 |
| 100 | native_replay | 4.11 | 1.05 | 5.51 | 19.6 | 9.99 | 2.84 |
| 100 | anchored_frozen | 4.09 | 1.02 | 5.43 | 18.6 | 11.29 | 3.05 |
| 200 | native_frozen | 7.39 | 1.10 | 8.82 | 99.2 | 4.83 | 0.75 |
| 200 | native_replay | 4.53 | 0.82 | 5.67 | 25.6 | 8.61 | 1.58 |
| 200 | anchored_frozen | 4.51 | 0.80 | 5.67 | 26.0 | 9.76 | 1.62 |
| 400 | native_frozen | 7.83 | 0.85 | 9.03 | 100.0 | 4.47 | 0.46 |
| 400 | native_replay | 4.82 | 0.64 | 5.66 | 35.2 | 7.88 | 0.95 |
| 400 | anchored_frozen | 4.81 | 0.64 | 5.60 | 38.2 | 8.97 | 0.94 |
| 1000 | native_frozen | 7.96 | 0.58 | 8.70 | 100.0 | 4.35 | 0.20 |
| 1000 | native_replay | 4.91 | 0.46 | 5.52 | 41.4 | 7.62 | 0.42 |
| 1000 | anchored_frozen | 4.89 | 0.46 | 5.52 | 39.6 | 8.72 | 0.41 |

CRC controls the mean of the loss over splits; the spread over splits shrinks with n as usual for split conformal methods. Set size is the mean number of labels per labelled sampled pixel at the grown vocabulary. Stored scores are float16 logits clamped to [-30, 30].