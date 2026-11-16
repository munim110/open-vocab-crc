# Calibration-set size under source-calibrated thresholds: sed_fast8

2000 ADE validation images (0 without a source-labelled sampled pixel excluded), 150 source labels, 845 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration sed_fast8. Development data; nothing is fitted; the confirmation reserve is untouched.
Evaluation images: the second half of every permutation (1000 images). Calibration: the first n images of the first half (nested). Headline loss (fraction of source-labelled sampled pixels whose label is missing from the set). CRC needs n >= (1 - alpha)/alpha for a non-trivial threshold; smaller n selects every label.

## alpha = 0.1 (needs n >= 9)

| n_cal | Arm | Mean risk (%) | Split sd (pp) | 90th pct risk (%) | Splits above alpha (%) | Set size | Size sd |
|---:|---|---:|---:|---:|---:|---:|---:|
| 10 | native_frozen | 3.00 | 2.94 | 6.72 | 0.0 | 404.29 | 412.20 |
| 10 | native_replay | 1.02 | 2.09 | 5.02 | 0.0 | 683.90 | 326.66 |
| 10 | anchored_frozen | 2.40 | 1.70 | 4.68 | 0.0 | 85.35 | 86.60 |
| 20 | native_frozen | 8.08 | 3.55 | 12.48 | 29.0 | 71.10 | 219.12 |
| 20 | native_replay | 5.35 | 3.73 | 9.73 | 9.0 | 234.19 | 368.18 |
| 20 | anchored_frozen | 6.11 | 2.69 | 9.73 | 8.4 | 18.21 | 16.57 |
| 50 | native_frozen | 10.92 | 2.29 | 13.78 | 68.2 | 5.01 | 2.34 |
| 50 | native_replay | 8.24 | 2.39 | 10.96 | 20.8 | 29.82 | 133.41 |
| 50 | anchored_frozen | 8.23 | 2.03 | 10.89 | 20.2 | 9.38 | 3.36 |
| 100 | native_frozen | 11.88 | 1.84 | 14.17 | 83.6 | 4.12 | 0.92 |
| 100 | native_replay | 9.14 | 1.71 | 11.20 | 31.8 | 6.35 | 2.05 |
| 100 | anchored_frozen | 9.03 | 1.53 | 11.12 | 26.2 | 7.97 | 1.53 |
| 200 | native_frozen | 12.36 | 1.29 | 13.96 | 96.2 | 3.79 | 0.50 |
| 200 | native_replay | 9.53 | 1.24 | 11.17 | 35.4 | 5.66 | 1.06 |
| 200 | anchored_frozen | 9.48 | 1.12 | 10.91 | 33.8 | 7.38 | 0.90 |
| 400 | native_frozen | 12.71 | 0.99 | 13.91 | 99.8 | 3.61 | 0.30 |
| 400 | native_replay | 9.80 | 0.96 | 11.11 | 41.2 | 5.32 | 0.63 |
| 400 | anchored_frozen | 9.79 | 0.88 | 10.84 | 42.0 | 7.06 | 0.57 |
| 1000 | native_frozen | 12.84 | 0.73 | 13.73 | 100.0 | 3.54 | 0.13 |
| 1000 | native_replay | 9.91 | 0.71 | 10.83 | 45.0 | 5.18 | 0.28 |
| 1000 | anchored_frozen | 9.90 | 0.65 | 10.70 | 45.2 | 6.93 | 0.27 |

## alpha = 0.05 (needs n >= 19)

| n_cal | Arm | Mean risk (%) | Split sd (pp) | 90th pct risk (%) | Splits above alpha (%) | Set size | Size sd |
|---:|---|---:|---:|---:|---:|---:|---:|
| 10 | native_frozen | 0.00 | 0.00 | 0.00 | 0.0 | 845.00 | 0.00 |
| 10 | native_replay | 0.00 | 0.00 | 0.00 | 0.0 | 845.00 | 0.00 |
| 10 | anchored_frozen | 0.00 | 0.00 | 0.00 | 0.0 | 845.00 | 0.00 |
| 20 | native_frozen | 0.58 | 1.50 | 4.17 | 1.4 | 739.78 | 272.50 |
| 20 | native_replay | 0.00 | 0.00 | 0.00 | 0.0 | 845.00 | 0.00 |
| 20 | anchored_frozen | 0.90 | 0.81 | 2.15 | 0.0 | 176.04 | 122.88 |
| 50 | native_frozen | 4.22 | 2.67 | 7.07 | 51.0 | 231.90 | 362.02 |
| 50 | native_replay | 1.38 | 2.25 | 5.07 | 11.0 | 615.63 | 368.24 |
| 50 | anchored_frozen | 3.26 | 1.26 | 4.97 | 9.0 | 36.54 | 22.32 |
| 100 | native_frozen | 5.88 | 1.67 | 7.74 | 76.8 | 46.63 | 159.09 |
| 100 | native_replay | 2.64 | 2.59 | 5.82 | 22.4 | 415.40 | 409.96 |
| 100 | anchored_frozen | 4.05 | 1.08 | 5.48 | 19.2 | 23.34 | 9.86 |
| 200 | native_frozen | 6.52 | 0.97 | 7.76 | 93.8 | 11.37 | 3.85 |
| 200 | native_replay | 3.59 | 2.27 | 5.69 | 30.6 | 248.28 | 365.23 |
| 200 | anchored_frozen | 4.48 | 0.83 | 5.53 | 25.4 | 18.61 | 4.49 |
| 400 | native_frozen | 6.87 | 0.76 | 7.75 | 99.0 | 9.76 | 1.67 |
| 400 | native_replay | 4.58 | 1.40 | 5.68 | 41.4 | 81.48 | 209.89 |
| 400 | anchored_frozen | 4.79 | 0.67 | 5.60 | 38.2 | 16.53 | 2.38 |
| 1000 | native_frozen | 6.98 | 0.55 | 7.65 | 100.0 | 9.27 | 0.68 |
| 1000 | native_replay | 4.91 | 0.53 | 5.61 | 40.0 | 21.38 | 4.19 |
| 1000 | anchored_frozen | 4.89 | 0.50 | 5.56 | 43.6 | 15.79 | 1.01 |

CRC controls the mean of the loss over splits; the spread over splits shrinks with n as usual for split conformal methods. Set size is the mean number of labels per labelled sampled pixel at the grown vocabulary. Stored scores are float16 logits clamped to [-30, 30].