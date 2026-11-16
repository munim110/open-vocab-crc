# Calibration-set size under source-calibrated thresholds: vitb_coco171

2000 ADE validation images (0 without a source-labelled sampled pixel excluded), 150 source labels, 845 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration vitb_coco171. Development data; nothing is fitted; the confirmation reserve is untouched.
Evaluation images: the second half of every permutation (1000 images). Calibration: the first n images of the first half (nested). Headline loss (fraction of source-labelled sampled pixels whose label is missing from the set). CRC needs n >= (1 - alpha)/alpha for a non-trivial threshold; smaller n selects every label.

## alpha = 0.1 (needs n >= 9)

| n_cal | Arm | Mean risk (%) | Split sd (pp) | 90th pct risk (%) | Splits above alpha (%) | Set size | Size sd |
|---:|---|---:|---:|---:|---:|---:|---:|
| 10 | native_frozen | 3.78 | 2.06 | 6.55 | 0.2 | 28.71 | 25.86 |
| 10 | native_replay | 2.06 | 1.55 | 4.30 | 0.0 | 158.54 | 277.68 |
| 10 | anchored_frozen | 2.01 | 1.38 | 3.89 | 0.0 | 62.77 | 61.68 |
| 20 | native_frozen | 9.73 | 3.36 | 14.06 | 47.0 | 6.53 | 4.44 |
| 20 | native_replay | 5.98 | 2.49 | 9.45 | 7.2 | 16.62 | 53.41 |
| 20 | anchored_frozen | 6.01 | 2.40 | 9.63 | 7.4 | 15.20 | 8.60 |
| 50 | native_frozen | 13.06 | 2.50 | 16.02 | 88.4 | 3.63 | 1.10 |
| 50 | native_replay | 8.28 | 1.87 | 10.59 | 16.8 | 6.97 | 2.46 |
| 50 | anchored_frozen | 8.20 | 1.84 | 10.51 | 16.6 | 9.55 | 2.51 |
| 100 | native_frozen | 14.25 | 1.92 | 16.57 | 99.2 | 3.10 | 0.55 |
| 100 | native_replay | 9.14 | 1.52 | 11.07 | 28.0 | 5.79 | 1.25 |
| 100 | anchored_frozen | 9.02 | 1.44 | 10.97 | 25.8 | 8.30 | 1.43 |
| 200 | native_frozen | 14.86 | 1.36 | 16.56 | 100.0 | 2.89 | 0.32 |
| 200 | native_replay | 9.53 | 1.13 | 10.96 | 32.8 | 5.34 | 0.78 |
| 200 | anchored_frozen | 9.48 | 1.06 | 10.89 | 31.4 | 7.73 | 0.88 |
| 400 | native_frozen | 15.23 | 1.04 | 16.56 | 100.0 | 2.77 | 0.20 |
| 400 | native_replay | 9.80 | 0.88 | 10.94 | 41.6 | 5.09 | 0.49 |
| 400 | anchored_frozen | 9.77 | 0.83 | 10.88 | 38.8 | 7.42 | 0.56 |
| 1000 | native_frozen | 15.38 | 0.73 | 16.31 | 100.0 | 2.73 | 0.09 |
| 1000 | native_replay | 9.90 | 0.62 | 10.65 | 45.6 | 4.98 | 0.21 |
| 1000 | anchored_frozen | 9.88 | 0.60 | 10.62 | 42.8 | 7.30 | 0.25 |

## alpha = 0.05 (needs n >= 19)

| n_cal | Arm | Mean risk (%) | Split sd (pp) | 90th pct risk (%) | Splits above alpha (%) | Set size | Size sd |
|---:|---|---:|---:|---:|---:|---:|---:|
| 10 | native_frozen | 0.00 | 0.00 | 0.00 | 0.0 | 845.00 | 0.00 |
| 10 | native_replay | 0.00 | 0.00 | 0.00 | 0.0 | 845.00 | 0.00 |
| 10 | anchored_frozen | 0.00 | 0.00 | 0.00 | 0.0 | 845.00 | 0.00 |
| 20 | native_frozen | 1.84 | 0.90 | 3.07 | 0.2 | 54.84 | 36.58 |
| 20 | native_replay | 0.69 | 0.66 | 1.61 | 0.0 | 357.31 | 360.89 |
| 20 | anchored_frozen | 0.74 | 0.56 | 1.48 | 0.0 | 124.98 | 93.13 |
| 50 | native_frozen | 5.70 | 1.51 | 7.65 | 67.8 | 11.94 | 4.82 |
| 50 | native_replay | 3.21 | 1.13 | 4.74 | 6.4 | 27.30 | 38.62 |
| 50 | anchored_frozen | 3.19 | 1.08 | 4.68 | 5.8 | 26.32 | 11.13 |
| 100 | native_frozen | 6.92 | 1.37 | 8.62 | 93.4 | 8.68 | 2.33 |
| 100 | native_replay | 4.10 | 1.01 | 5.43 | 16.6 | 17.74 | 5.30 |
| 100 | anchored_frozen | 4.04 | 0.94 | 5.30 | 16.0 | 19.56 | 4.03 |
| 200 | native_frozen | 7.56 | 1.05 | 9.03 | 100.0 | 7.42 | 1.26 |
| 200 | native_replay | 4.50 | 0.78 | 5.55 | 24.6 | 15.19 | 2.88 |
| 200 | anchored_frozen | 4.49 | 0.72 | 5.47 | 22.6 | 17.37 | 2.20 |
| 400 | native_frozen | 7.98 | 0.82 | 9.00 | 100.0 | 6.79 | 0.77 |
| 400 | native_replay | 4.79 | 0.62 | 5.64 | 35.0 | 13.78 | 1.79 |
| 400 | anchored_frozen | 4.78 | 0.58 | 5.52 | 36.2 | 16.26 | 1.40 |
| 1000 | native_frozen | 8.15 | 0.57 | 8.91 | 100.0 | 6.55 | 0.34 |
| 1000 | native_replay | 4.90 | 0.45 | 5.48 | 40.8 | 13.25 | 0.79 |
| 1000 | anchored_frozen | 4.89 | 0.42 | 5.43 | 41.6 | 15.86 | 0.64 |

CRC controls the mean of the loss over splits; the spread over splits shrinks with n as usual for split conformal methods. Set size is the mean number of labels per labelled sampled pixel at the grown vocabulary. Stored scores are float16 logits clamped to [-30, 30].