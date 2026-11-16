# Calibration-set size under source-calibrated thresholds: pascal_vitb_coco171

2000 Pascal Context validation images (0 without a source-labelled sampled pixel excluded), 59 source labels, 458 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration pascal_vitb_coco171. Development data; nothing is fitted; the confirmation reserve is untouched.
Evaluation images: the second half of every permutation (1000 images). Calibration: the first n images of the first half (nested). Headline loss (fraction of source-labelled sampled pixels whose label is missing from the set). CRC needs n >= (1 - alpha)/alpha for a non-trivial threshold; smaller n selects every label.

## alpha = 0.1 (needs n >= 9)

| n_cal | Arm | Mean risk (%) | Split sd (pp) | 90th pct risk (%) | Splits above alpha (%) | Set size | Size sd |
|---:|---|---:|---:|---:|---:|---:|---:|
| 10 | native_frozen | 4.09 | 2.80 | 7.88 | 4.4 | 8.63 | 8.28 |
| 10 | native_replay | 2.25 | 1.73 | 4.35 | 0.6 | 17.45 | 30.30 |
| 10 | anchored_frozen | 2.35 | 1.82 | 4.64 | 0.4 | 18.06 | 18.39 |
| 20 | native_frozen | 9.93 | 3.77 | 15.24 | 45.0 | 2.85 | 1.17 |
| 20 | native_replay | 6.10 | 2.91 | 9.83 | 9.2 | 4.71 | 2.43 |
| 20 | anchored_frozen | 6.07 | 2.79 | 9.65 | 8.8 | 6.01 | 3.00 |
| 50 | native_frozen | 13.12 | 2.71 | 16.74 | 86.4 | 1.97 | 0.42 |
| 50 | native_replay | 8.41 | 2.18 | 11.33 | 22.2 | 3.08 | 0.73 |
| 50 | anchored_frozen | 8.39 | 2.22 | 11.22 | 21.2 | 4.03 | 0.91 |
| 100 | native_frozen | 14.27 | 2.12 | 16.91 | 97.8 | 1.78 | 0.26 |
| 100 | native_replay | 9.19 | 1.69 | 11.30 | 30.4 | 2.77 | 0.46 |
| 100 | anchored_frozen | 9.19 | 1.70 | 11.33 | 30.0 | 3.63 | 0.56 |
| 200 | native_frozen | 14.82 | 1.49 | 16.64 | 99.8 | 1.69 | 0.15 |
| 200 | native_replay | 9.62 | 1.20 | 11.15 | 37.6 | 2.61 | 0.27 |
| 200 | anchored_frozen | 9.60 | 1.26 | 11.22 | 38.0 | 3.46 | 0.34 |
| 400 | native_frozen | 15.04 | 1.14 | 16.55 | 100.0 | 1.65 | 0.10 |
| 400 | native_replay | 9.78 | 0.95 | 11.06 | 37.0 | 2.56 | 0.18 |
| 400 | anchored_frozen | 9.77 | 0.93 | 10.89 | 40.2 | 3.39 | 0.22 |
| 1000 | native_frozen | 15.17 | 0.85 | 16.26 | 100.0 | 1.63 | 0.05 |
| 1000 | native_replay | 9.88 | 0.73 | 10.87 | 42.4 | 2.52 | 0.09 |
| 1000 | anchored_frozen | 9.87 | 0.71 | 10.84 | 42.8 | 3.35 | 0.11 |

## alpha = 0.05 (needs n >= 19)

| n_cal | Arm | Mean risk (%) | Split sd (pp) | 90th pct risk (%) | Splits above alpha (%) | Set size | Size sd |
|---:|---|---:|---:|---:|---:|---:|---:|
| 10 | native_frozen | 0.00 | 0.00 | 0.00 | 0.0 | 458.00 | 0.00 |
| 10 | native_replay | 0.00 | 0.00 | 0.00 | 0.0 | 458.00 | 0.00 |
| 10 | anchored_frozen | 0.00 | 0.00 | 0.00 | 0.0 | 458.00 | 0.00 |
| 20 | native_frozen | 1.69 | 1.10 | 3.14 | 0.6 | 15.77 | 11.49 |
| 20 | native_replay | 0.78 | 0.67 | 1.76 | 0.0 | 43.72 | 76.82 |
| 20 | anchored_frozen | 0.84 | 0.73 | 1.83 | 0.0 | 34.26 | 28.36 |
| 50 | native_frozen | 5.99 | 2.04 | 8.71 | 65.6 | 4.31 | 1.40 |
| 50 | native_replay | 3.32 | 1.29 | 4.99 | 10.0 | 7.25 | 2.85 |
| 50 | anchored_frozen | 3.35 | 1.38 | 5.12 | 11.2 | 9.08 | 3.32 |
| 100 | native_frozen | 7.34 | 1.64 | 9.45 | 92.2 | 3.44 | 0.68 |
| 100 | native_replay | 4.17 | 1.11 | 5.47 | 21.8 | 5.57 | 1.31 |
| 100 | anchored_frozen | 4.19 | 1.15 | 5.68 | 23.2 | 7.09 | 1.66 |
| 200 | native_frozen | 7.96 | 1.20 | 9.42 | 99.2 | 3.13 | 0.38 |
| 200 | native_replay | 4.59 | 0.86 | 5.71 | 28.2 | 4.99 | 0.66 |
| 200 | anchored_frozen | 4.58 | 0.90 | 5.74 | 30.4 | 6.41 | 0.86 |
| 400 | native_frozen | 8.25 | 0.91 | 9.47 | 100.0 | 3.01 | 0.24 |
| 400 | native_replay | 4.76 | 0.66 | 5.70 | 31.2 | 4.78 | 0.40 |
| 400 | anchored_frozen | 4.76 | 0.69 | 5.71 | 36.2 | 6.15 | 0.55 |
| 1000 | native_frozen | 8.40 | 0.67 | 9.29 | 100.0 | 2.95 | 0.12 |
| 1000 | native_replay | 4.89 | 0.51 | 5.56 | 38.4 | 4.65 | 0.19 |
| 1000 | anchored_frozen | 4.88 | 0.53 | 5.61 | 37.2 | 6.00 | 0.26 |

CRC controls the mean of the loss over splits; the spread over splits shrinks with n as usual for split conformal methods. Set size is the mean number of labels per labelled sampled pixel at the grown vocabulary. Stored scores are float16 logits clamped to [-30, 30].