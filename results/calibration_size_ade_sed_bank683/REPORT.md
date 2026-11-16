# Calibration-set size under source-calibrated thresholds: sed_bank683

2000 ADE validation images (0 without a source-labelled sampled pixel excluded), 150 source labels, 845 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration sed_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
Evaluation images: the second half of every permutation (1000 images). Calibration: the first n images of the first half (nested). Headline loss (fraction of source-labelled sampled pixels whose label is missing from the set). CRC needs n >= (1 - alpha)/alpha for a non-trivial threshold; smaller n selects every label.

## alpha = 0.1 (needs n >= 9)

| n_cal | Arm | Mean risk (%) | Split sd (pp) | 90th pct risk (%) | Splits above alpha (%) | Set size | Size sd |
|---:|---|---:|---:|---:|---:|---:|---:|
| 10 | native_frozen | 1.64 | 1.34 | 3.58 | 0.0 | 135.07 | 129.71 |
| 10 | native_replay | 2.37 | 1.72 | 4.68 | 0.0 | 87.15 | 83.45 |
| 10 | anchored_frozen | 2.46 | 1.70 | 4.71 | 0.0 | 91.13 | 89.54 |
| 20 | native_frozen | 4.52 | 1.85 | 6.79 | 0.2 | 27.94 | 26.64 |
| 20 | native_replay | 6.09 | 2.65 | 9.53 | 7.2 | 18.58 | 18.97 |
| 20 | anchored_frozen | 6.11 | 2.66 | 9.67 | 7.8 | 19.10 | 21.20 |
| 50 | native_frozen | 6.09 | 1.28 | 7.60 | 0.0 | 12.63 | 5.73 |
| 50 | native_replay | 8.33 | 2.02 | 10.97 | 20.0 | 7.88 | 3.80 |
| 50 | anchored_frozen | 8.28 | 2.06 | 10.92 | 19.6 | 8.42 | 3.81 |
| 100 | native_frozen | 6.63 | 0.99 | 7.88 | 0.0 | 10.25 | 2.36 |
| 100 | native_replay | 9.11 | 1.65 | 11.21 | 29.8 | 6.33 | 1.77 |
| 100 | anchored_frozen | 9.08 | 1.61 | 11.25 | 28.8 | 6.93 | 1.47 |
| 200 | native_frozen | 6.88 | 0.70 | 7.73 | 0.0 | 9.39 | 1.23 |
| 200 | native_replay | 9.51 | 1.19 | 11.20 | 33.6 | 5.72 | 0.94 |
| 200 | anchored_frozen | 9.49 | 1.17 | 11.07 | 34.2 | 6.42 | 0.81 |
| 400 | native_frozen | 7.06 | 0.57 | 7.77 | 0.0 | 8.93 | 0.76 |
| 400 | native_replay | 9.80 | 0.93 | 10.98 | 41.8 | 5.39 | 0.57 |
| 400 | anchored_frozen | 9.79 | 0.90 | 10.92 | 40.8 | 6.13 | 0.50 |
| 1000 | native_frozen | 7.12 | 0.46 | 7.70 | 0.0 | 8.78 | 0.35 |
| 1000 | native_replay | 9.90 | 0.68 | 10.78 | 44.6 | 5.27 | 0.25 |
| 1000 | anchored_frozen | 9.89 | 0.66 | 10.69 | 44.8 | 6.04 | 0.23 |

## alpha = 0.05 (needs n >= 19)

| n_cal | Arm | Mean risk (%) | Split sd (pp) | 90th pct risk (%) | Splits above alpha (%) | Set size | Size sd |
|---:|---|---:|---:|---:|---:|---:|---:|
| 10 | native_frozen | 0.00 | 0.00 | 0.00 | 0.0 | 845.00 | 0.00 |
| 10 | native_replay | 0.00 | 0.00 | 0.00 | 0.0 | 845.00 | 0.00 |
| 10 | anchored_frozen | 0.00 | 0.00 | 0.00 | 0.0 | 845.00 | 0.00 |
| 20 | native_frozen | 0.45 | 0.51 | 1.26 | 0.0 | 261.16 | 156.65 |
| 20 | native_replay | 0.85 | 0.75 | 2.03 | 0.0 | 172.64 | 108.41 |
| 20 | anchored_frozen | 0.94 | 0.84 | 2.25 | 0.0 | 184.00 | 118.03 |
| 50 | native_frozen | 2.44 | 1.06 | 3.79 | 0.4 | 57.66 | 32.99 |
| 50 | native_replay | 3.28 | 1.26 | 4.99 | 9.8 | 38.67 | 22.58 |
| 50 | anchored_frozen | 3.29 | 1.27 | 4.94 | 9.6 | 40.95 | 27.78 |
| 100 | native_frozen | 3.14 | 0.87 | 4.28 | 1.6 | 37.25 | 15.71 |
| 100 | native_replay | 4.13 | 1.15 | 5.70 | 21.0 | 24.62 | 10.97 |
| 100 | anchored_frozen | 4.11 | 1.14 | 5.69 | 21.2 | 24.57 | 12.44 |
| 200 | native_frozen | 3.49 | 0.64 | 4.34 | 1.2 | 29.58 | 7.65 |
| 200 | native_replay | 4.51 | 0.85 | 5.60 | 30.2 | 19.54 | 5.43 |
| 200 | anchored_frozen | 4.50 | 0.86 | 5.67 | 27.6 | 18.99 | 5.63 |
| 400 | native_frozen | 3.72 | 0.51 | 4.34 | 1.0 | 26.02 | 4.46 |
| 400 | native_replay | 4.81 | 0.67 | 5.59 | 40.4 | 16.98 | 3.03 |
| 400 | anchored_frozen | 4.80 | 0.69 | 5.61 | 39.4 | 16.45 | 3.00 |
| 1000 | native_frozen | 3.79 | 0.39 | 4.33 | 0.2 | 24.76 | 1.91 |
| 1000 | native_replay | 4.90 | 0.51 | 5.55 | 43.2 | 16.14 | 1.34 |
| 1000 | anchored_frozen | 4.89 | 0.50 | 5.56 | 44.0 | 15.58 | 1.23 |

CRC controls the mean of the loss over splits; the spread over splits shrinks with n as usual for split conformal methods. Set size is the mean number of labels per labelled sampled pixel at the grown vocabulary. Stored scores are float16 logits clamped to [-30, 30].