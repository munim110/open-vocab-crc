# Calibration-set size under source-calibrated thresholds: pascal_fcclip_bank683

2000 Pascal Context validation images (0 without a source-labelled sampled pixel excluded), 59 source labels, 458 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration pascal_fcclip_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
Evaluation images: the second half of every permutation (1000 images). Calibration: the first n images of the first half (nested). Headline loss (fraction of source-labelled sampled pixels whose label is missing from the set). CRC needs n >= (1 - alpha)/alpha for a non-trivial threshold; smaller n selects every label.

## alpha = 0.1 (needs n >= 9)

| n_cal | Arm | Mean risk (%) | Split sd (pp) | 90th pct risk (%) | Splits above alpha (%) | Set size | Size sd |
|---:|---|---:|---:|---:|---:|---:|---:|
| 10 | native_frozen | 4.02 | 2.78 | 7.98 | 2.6 | 29.45 | 32.24 |
| 10 | native_replay | 2.15 | 1.72 | 4.68 | 0.2 | 49.82 | 43.16 |
| 10 | anchored_frozen | 2.14 | 1.67 | 4.49 | 0.0 | 48.66 | 37.96 |
| 20 | native_frozen | 10.43 | 4.36 | 16.20 | 50.2 | 6.74 | 5.39 |
| 20 | native_replay | 6.13 | 2.85 | 10.20 | 11.0 | 12.98 | 9.12 |
| 20 | anchored_frozen | 5.99 | 2.73 | 9.57 | 7.6 | 14.23 | 9.88 |
| 50 | native_frozen | 14.12 | 3.42 | 18.49 | 90.8 | 3.67 | 1.21 |
| 50 | native_replay | 8.43 | 2.29 | 11.57 | 22.4 | 7.13 | 2.55 |
| 50 | anchored_frozen | 8.45 | 2.26 | 11.46 | 23.2 | 7.84 | 2.74 |
| 100 | native_frozen | 15.17 | 2.47 | 18.15 | 98.4 | 3.19 | 0.63 |
| 100 | native_replay | 9.16 | 1.69 | 11.32 | 29.0 | 6.07 | 1.39 |
| 100 | anchored_frozen | 9.20 | 1.73 | 11.43 | 32.2 | 6.69 | 1.69 |
| 200 | native_frozen | 15.82 | 1.73 | 17.87 | 100.0 | 2.96 | 0.36 |
| 200 | native_replay | 9.58 | 1.23 | 11.24 | 33.8 | 5.59 | 0.78 |
| 200 | anchored_frozen | 9.60 | 1.23 | 11.30 | 34.0 | 6.12 | 0.91 |
| 400 | native_frozen | 16.07 | 1.32 | 17.72 | 100.0 | 2.88 | 0.25 |
| 400 | native_replay | 9.76 | 0.95 | 10.95 | 39.0 | 5.41 | 0.50 |
| 400 | anchored_frozen | 9.80 | 0.97 | 11.07 | 41.4 | 5.89 | 0.61 |
| 1000 | native_frozen | 16.25 | 1.00 | 17.52 | 100.0 | 2.82 | 0.12 |
| 1000 | native_replay | 9.86 | 0.78 | 10.84 | 39.6 | 5.31 | 0.25 |
| 1000 | anchored_frozen | 9.89 | 0.75 | 10.89 | 41.4 | 5.77 | 0.30 |

## alpha = 0.05 (needs n >= 19)

| n_cal | Arm | Mean risk (%) | Split sd (pp) | 90th pct risk (%) | Splits above alpha (%) | Set size | Size sd |
|---:|---|---:|---:|---:|---:|---:|---:|
| 10 | native_frozen | 0.00 | 0.00 | 0.00 | 0.0 | 458.00 | 0.00 |
| 10 | native_replay | 0.00 | 0.00 | 0.00 | 0.0 | 458.00 | 0.00 |
| 10 | anchored_frozen | 0.00 | 0.00 | 0.00 | 0.0 | 458.00 | 0.00 |
| 20 | native_frozen | 1.34 | 0.99 | 2.77 | 0.2 | 62.84 | 45.11 |
| 20 | native_replay | 0.59 | 0.44 | 1.12 | 0.0 | 101.72 | 55.66 |
| 20 | anchored_frozen | 0.61 | 0.47 | 1.27 | 0.0 | 99.31 | 52.69 |
| 50 | native_frozen | 6.06 | 2.20 | 8.77 | 66.0 | 11.65 | 5.96 |
| 50 | native_replay | 3.43 | 1.37 | 5.27 | 13.0 | 22.11 | 9.80 |
| 50 | anchored_frozen | 3.40 | 1.39 | 5.18 | 11.6 | 23.41 | 9.93 |
| 100 | native_frozen | 7.40 | 1.79 | 9.82 | 93.0 | 8.21 | 2.49 |
| 100 | native_replay | 4.18 | 1.11 | 5.61 | 21.6 | 16.51 | 4.81 |
| 100 | anchored_frozen | 4.17 | 1.09 | 5.68 | 20.8 | 17.54 | 4.68 |
| 200 | native_frozen | 8.05 | 1.33 | 9.65 | 99.6 | 7.06 | 1.33 |
| 200 | native_replay | 4.56 | 0.85 | 5.62 | 26.6 | 14.33 | 2.77 |
| 200 | anchored_frozen | 4.57 | 0.84 | 5.61 | 28.4 | 15.39 | 2.70 |
| 400 | native_frozen | 8.38 | 1.02 | 9.70 | 100.0 | 6.60 | 0.83 |
| 400 | native_replay | 4.75 | 0.67 | 5.63 | 31.4 | 13.35 | 1.74 |
| 400 | anchored_frozen | 4.77 | 0.68 | 5.66 | 35.0 | 14.46 | 1.71 |
| 1000 | native_frozen | 8.56 | 0.76 | 9.53 | 100.0 | 6.36 | 0.40 |
| 1000 | native_replay | 4.87 | 0.54 | 5.58 | 41.4 | 12.78 | 0.86 |
| 1000 | anchored_frozen | 4.88 | 0.54 | 5.57 | 39.2 | 13.97 | 0.87 |

CRC controls the mean of the loss over splits; the spread over splits shrinks with n as usual for split conformal methods. Set size is the mean number of labels per labelled sampled pixel at the grown vocabulary. Stored scores are float16 logits clamped to [-30, 30].