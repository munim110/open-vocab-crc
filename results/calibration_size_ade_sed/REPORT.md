# Calibration-set size under source-calibrated thresholds: sed

2000 ADE validation images (0 without a source-labelled sampled pixel excluded), 150 source labels, 845 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration sed. Development data; nothing is fitted; the confirmation reserve is untouched.
Evaluation images: the second half of every permutation (1000 images). Calibration: the first n images of the first half (nested). Headline loss (fraction of source-labelled sampled pixels whose label is missing from the set). CRC needs n >= (1 - alpha)/alpha for a non-trivial threshold; smaller n selects every label.

## alpha = 0.1 (needs n >= 9)

| n_cal | Arm | Mean risk (%) | Split sd (pp) | 90th pct risk (%) | Splits above alpha (%) | Set size | Size sd |
|---:|---|---:|---:|---:|---:|---:|---:|
| 10 | native_frozen | 1.64 | 1.34 | 3.58 | 0.0 | 135.07 | 129.71 |
| 10 | native_replay | 2.37 | 1.72 | 4.68 | 0.0 | 87.15 | 83.45 |
| 10 | anchored_frozen | 2.40 | 1.70 | 4.68 | 0.0 | 85.35 | 86.60 |
| 20 | native_frozen | 4.52 | 1.85 | 6.79 | 0.2 | 27.94 | 26.64 |
| 20 | native_replay | 6.09 | 2.65 | 9.53 | 7.2 | 18.58 | 18.97 |
| 20 | anchored_frozen | 6.11 | 2.69 | 9.73 | 8.4 | 18.21 | 16.57 |
| 50 | native_frozen | 6.09 | 1.28 | 7.60 | 0.0 | 12.63 | 5.73 |
| 50 | native_replay | 8.33 | 2.02 | 10.97 | 20.0 | 7.88 | 3.80 |
| 50 | anchored_frozen | 8.23 | 2.03 | 10.89 | 20.2 | 9.38 | 3.36 |
| 100 | native_frozen | 6.63 | 0.99 | 7.88 | 0.0 | 10.25 | 2.36 |
| 100 | native_replay | 9.11 | 1.65 | 11.21 | 29.8 | 6.33 | 1.77 |
| 100 | anchored_frozen | 9.03 | 1.53 | 11.12 | 26.2 | 7.97 | 1.53 |
| 200 | native_frozen | 6.88 | 0.70 | 7.73 | 0.0 | 9.39 | 1.23 |
| 200 | native_replay | 9.51 | 1.19 | 11.20 | 33.6 | 5.72 | 0.94 |
| 200 | anchored_frozen | 9.48 | 1.12 | 10.91 | 33.8 | 7.38 | 0.90 |
| 400 | native_frozen | 7.06 | 0.57 | 7.77 | 0.0 | 8.93 | 0.76 |
| 400 | native_replay | 9.80 | 0.93 | 10.98 | 41.8 | 5.39 | 0.57 |
| 400 | anchored_frozen | 9.79 | 0.88 | 10.84 | 42.0 | 7.06 | 0.57 |
| 1000 | native_frozen | 7.12 | 0.46 | 7.70 | 0.0 | 8.78 | 0.35 |
| 1000 | native_replay | 9.90 | 0.68 | 10.78 | 44.6 | 5.27 | 0.25 |
| 1000 | anchored_frozen | 9.90 | 0.65 | 10.70 | 45.2 | 6.93 | 0.27 |

## alpha = 0.05 (needs n >= 19)

| n_cal | Arm | Mean risk (%) | Split sd (pp) | 90th pct risk (%) | Splits above alpha (%) | Set size | Size sd |
|---:|---|---:|---:|---:|---:|---:|---:|
| 10 | native_frozen | 0.00 | 0.00 | 0.00 | 0.0 | 845.00 | 0.00 |
| 10 | native_replay | 0.00 | 0.00 | 0.00 | 0.0 | 845.00 | 0.00 |
| 10 | anchored_frozen | 0.00 | 0.00 | 0.00 | 0.0 | 845.00 | 0.00 |
| 20 | native_frozen | 0.45 | 0.51 | 1.26 | 0.0 | 261.16 | 156.65 |
| 20 | native_replay | 0.85 | 0.75 | 2.03 | 0.0 | 172.64 | 108.41 |
| 20 | anchored_frozen | 0.90 | 0.81 | 2.15 | 0.0 | 176.04 | 122.88 |
| 50 | native_frozen | 2.44 | 1.06 | 3.79 | 0.4 | 57.66 | 32.99 |
| 50 | native_replay | 3.28 | 1.26 | 4.99 | 9.8 | 38.67 | 22.58 |
| 50 | anchored_frozen | 3.26 | 1.26 | 4.97 | 9.0 | 36.54 | 22.32 |
| 100 | native_frozen | 3.14 | 0.87 | 4.28 | 1.6 | 37.25 | 15.71 |
| 100 | native_replay | 4.13 | 1.15 | 5.70 | 21.0 | 24.62 | 10.97 |
| 100 | anchored_frozen | 4.05 | 1.08 | 5.48 | 19.2 | 23.34 | 9.86 |
| 200 | native_frozen | 3.49 | 0.64 | 4.34 | 1.2 | 29.58 | 7.65 |
| 200 | native_replay | 4.51 | 0.85 | 5.60 | 30.2 | 19.54 | 5.43 |
| 200 | anchored_frozen | 4.48 | 0.83 | 5.53 | 25.4 | 18.61 | 4.49 |
| 400 | native_frozen | 3.72 | 0.51 | 4.34 | 1.0 | 26.02 | 4.46 |
| 400 | native_replay | 4.81 | 0.67 | 5.59 | 40.4 | 16.98 | 3.03 |
| 400 | anchored_frozen | 4.79 | 0.67 | 5.60 | 38.2 | 16.53 | 2.38 |
| 1000 | native_frozen | 3.79 | 0.39 | 4.33 | 0.2 | 24.76 | 1.91 |
| 1000 | native_replay | 4.90 | 0.51 | 5.55 | 43.2 | 16.14 | 1.34 |
| 1000 | anchored_frozen | 4.89 | 0.50 | 5.56 | 43.6 | 15.79 | 1.01 |

CRC controls the mean of the loss over splits; the spread over splits shrinks with n as usual for split conformal methods. Set size is the mean number of labels per labelled sampled pixel at the grown vocabulary. Stored scores are float16 logits clamped to [-30, 30].