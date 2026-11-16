# Calibration-set size under source-calibrated thresholds: pascal_declip_bank683

2000 Pascal Context validation images (0 without a source-labelled sampled pixel excluded), 59 source labels, 458 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration pascal_declip_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
Evaluation images: the second half of every permutation (1000 images). Calibration: the first n images of the first half (nested). Headline loss (fraction of source-labelled sampled pixels whose label is missing from the set). CRC needs n >= (1 - alpha)/alpha for a non-trivial threshold; smaller n selects every label.

## alpha = 0.1 (needs n >= 9)

| n_cal | Arm | Mean risk (%) | Split sd (pp) | 90th pct risk (%) | Splits above alpha (%) | Set size | Size sd |
|---:|---|---:|---:|---:|---:|---:|---:|
| 10 | native_frozen | 4.12 | 2.85 | 8.20 | 5.0 | 6.04 | 4.92 |
| 10 | native_replay | 2.31 | 1.92 | 4.68 | 0.6 | 12.92 | 36.45 |
| 10 | anchored_frozen | 2.38 | 2.01 | 5.04 | 0.8 | 10.66 | 11.78 |
| 20 | native_frozen | 9.93 | 3.76 | 14.99 | 46.8 | 2.31 | 0.83 |
| 20 | native_replay | 6.15 | 3.00 | 10.30 | 11.4 | 3.59 | 1.67 |
| 20 | anchored_frozen | 6.13 | 3.02 | 10.47 | 12.0 | 3.95 | 1.84 |
| 50 | native_frozen | 13.04 | 2.61 | 16.29 | 88.2 | 1.71 | 0.30 |
| 50 | native_replay | 8.43 | 2.26 | 11.45 | 26.6 | 2.48 | 0.55 |
| 50 | anchored_frozen | 8.45 | 2.35 | 11.67 | 22.0 | 2.79 | 0.55 |
| 100 | native_frozen | 14.00 | 1.99 | 16.42 | 97.4 | 1.59 | 0.18 |
| 100 | native_replay | 9.16 | 1.75 | 11.46 | 31.0 | 2.26 | 0.32 |
| 100 | anchored_frozen | 9.23 | 1.79 | 11.52 | 30.6 | 2.57 | 0.31 |
| 200 | native_frozen | 14.44 | 1.37 | 16.06 | 100.0 | 1.53 | 0.11 |
| 200 | native_replay | 9.60 | 1.22 | 11.13 | 35.8 | 2.15 | 0.18 |
| 200 | anchored_frozen | 9.62 | 1.28 | 11.24 | 36.4 | 2.48 | 0.19 |
| 400 | native_frozen | 14.65 | 1.04 | 16.00 | 100.0 | 1.51 | 0.07 |
| 400 | native_replay | 9.78 | 0.95 | 10.99 | 40.0 | 2.11 | 0.12 |
| 400 | anchored_frozen | 9.80 | 0.97 | 11.04 | 42.0 | 2.43 | 0.12 |
| 1000 | native_frozen | 14.73 | 0.82 | 15.77 | 100.0 | 1.50 | 0.03 |
| 1000 | native_replay | 9.89 | 0.75 | 10.89 | 41.8 | 2.09 | 0.06 |
| 1000 | anchored_frozen | 9.90 | 0.76 | 10.93 | 43.8 | 2.41 | 0.06 |

## alpha = 0.05 (needs n >= 19)

| n_cal | Arm | Mean risk (%) | Split sd (pp) | 90th pct risk (%) | Splits above alpha (%) | Set size | Size sd |
|---:|---|---:|---:|---:|---:|---:|---:|
| 10 | native_frozen | 0.00 | 0.00 | 0.00 | 0.0 | 458.00 | 0.00 |
| 10 | native_replay | 0.00 | 0.00 | 0.00 | 0.0 | 458.00 | 0.00 |
| 10 | anchored_frozen | 0.00 | 0.00 | 0.00 | 0.0 | 458.00 | 0.00 |
| 20 | native_frozen | 1.64 | 1.21 | 3.25 | 2.4 | 11.79 | 9.67 |
| 20 | native_replay | 0.77 | 0.70 | 1.79 | 0.0 | 31.32 | 69.81 |
| 20 | anchored_frozen | 0.77 | 0.71 | 1.78 | 0.0 | 21.21 | 20.07 |
| 50 | native_frozen | 6.10 | 2.07 | 9.03 | 66.0 | 3.25 | 0.85 |
| 50 | native_replay | 3.37 | 1.38 | 5.26 | 12.6 | 5.27 | 1.76 |
| 50 | anchored_frozen | 3.38 | 1.44 | 5.39 | 14.0 | 5.61 | 1.91 |
| 100 | native_frozen | 7.32 | 1.70 | 9.60 | 93.6 | 2.72 | 0.47 |
| 100 | native_replay | 4.16 | 1.18 | 5.69 | 21.8 | 4.23 | 0.90 |
| 100 | anchored_frozen | 4.20 | 1.24 | 5.68 | 24.4 | 4.50 | 0.99 |
| 200 | native_frozen | 7.95 | 1.22 | 9.61 | 99.8 | 2.50 | 0.26 |
| 200 | native_replay | 4.58 | 0.88 | 5.72 | 31.8 | 3.82 | 0.48 |
| 200 | anchored_frozen | 4.58 | 0.90 | 5.81 | 30.8 | 4.08 | 0.49 |
| 400 | native_frozen | 8.28 | 0.93 | 9.55 | 100.0 | 2.41 | 0.16 |
| 400 | native_replay | 4.78 | 0.68 | 5.68 | 35.0 | 3.66 | 0.28 |
| 400 | anchored_frozen | 4.79 | 0.69 | 5.68 | 33.2 | 3.92 | 0.29 |
| 1000 | native_frozen | 8.45 | 0.70 | 9.39 | 100.0 | 2.36 | 0.08 |
| 1000 | native_replay | 4.89 | 0.53 | 5.61 | 38.0 | 3.58 | 0.14 |
| 1000 | anchored_frozen | 4.89 | 0.53 | 5.59 | 38.0 | 3.84 | 0.14 |

CRC controls the mean of the loss over splits; the spread over splits shrinks with n as usual for split conformal methods. Set size is the mean number of labels per labelled sampled pixel at the grown vocabulary. Stored scores are float16 logits clamped to [-30, 30].