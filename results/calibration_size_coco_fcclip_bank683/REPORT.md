# Calibration-set size under source-calibrated thresholds: coco_fcclip_bank683

2000 COCO val2017 (LVIS-annotated) images (0 without a source-labelled sampled pixel excluded), 171 source labels, 1283 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration coco_fcclip_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
Evaluation images: the second half of every permutation (1000 images). Calibration: the first n images of the first half (nested). Headline loss (fraction of source-labelled sampled pixels whose label is missing from the set). CRC needs n >= (1 - alpha)/alpha for a non-trivial threshold; smaller n selects every label.

## alpha = 0.1 (needs n >= 9)

| n_cal | Arm | Mean risk (%) | Split sd (pp) | 90th pct risk (%) | Splits above alpha (%) | Set size | Size sd |
|---:|---|---:|---:|---:|---:|---:|---:|
| 10 | native_frozen | 4.37 | 2.59 | 7.91 | 2.8 | 149.57 | 145.22 |
| 10 | native_replay | 1.97 | 1.48 | 3.92 | 0.0 | 304.97 | 200.47 |
| 10 | anchored_frozen | 1.94 | 1.43 | 3.88 | 0.0 | 251.61 | 176.36 |
| 20 | native_frozen | 11.35 | 3.68 | 16.29 | 61.0 | 27.26 | 20.77 |
| 20 | native_replay | 6.03 | 2.58 | 9.48 | 7.2 | 80.14 | 56.00 |
| 20 | anchored_frozen | 6.05 | 2.50 | 9.57 | 7.0 | 72.35 | 40.88 |
| 50 | native_frozen | 14.92 | 2.97 | 18.74 | 97.0 | 13.93 | 5.14 |
| 50 | native_replay | 8.47 | 2.00 | 11.02 | 21.2 | 39.31 | 15.74 |
| 50 | anchored_frozen | 8.44 | 1.95 | 11.03 | 20.0 | 39.45 | 14.54 |
| 100 | native_frozen | 15.98 | 2.19 | 18.67 | 99.8 | 11.62 | 2.98 |
| 100 | native_replay | 9.16 | 1.50 | 10.99 | 27.2 | 32.30 | 9.13 |
| 100 | anchored_frozen | 9.16 | 1.47 | 11.03 | 26.4 | 32.73 | 9.04 |
| 200 | native_frozen | 16.64 | 1.69 | 18.82 | 100.0 | 10.49 | 1.92 |
| 200 | native_replay | 9.62 | 1.19 | 11.16 | 35.4 | 28.72 | 5.75 |
| 200 | anchored_frozen | 9.59 | 1.11 | 11.13 | 35.8 | 29.29 | 5.84 |
| 400 | native_frozen | 16.95 | 1.30 | 18.62 | 100.0 | 9.96 | 1.16 |
| 400 | native_replay | 9.82 | 0.92 | 10.94 | 41.6 | 27.16 | 3.49 |
| 400 | anchored_frozen | 9.81 | 0.88 | 10.92 | 38.6 | 27.58 | 3.61 |
| 1000 | native_frozen | 17.09 | 0.98 | 18.29 | 100.0 | 9.72 | 0.57 |
| 1000 | native_replay | 9.91 | 0.70 | 10.73 | 43.6 | 26.53 | 1.85 |
| 1000 | anchored_frozen | 9.88 | 0.66 | 10.71 | 42.8 | 26.85 | 1.68 |

## alpha = 0.05 (needs n >= 19)

| n_cal | Arm | Mean risk (%) | Split sd (pp) | 90th pct risk (%) | Splits above alpha (%) | Set size | Size sd |
|---:|---|---:|---:|---:|---:|---:|---:|
| 10 | native_frozen | 0.00 | 0.00 | 0.00 | 0.0 | 1283.00 | 0.00 |
| 10 | native_replay | 0.00 | 0.00 | 0.00 | 0.0 | 1283.00 | 0.00 |
| 10 | anchored_frozen | 0.00 | 0.00 | 0.00 | 0.0 | 1283.00 | 0.00 |
| 20 | native_frozen | 1.57 | 1.00 | 2.94 | 0.4 | 336.80 | 199.29 |
| 20 | native_replay | 0.62 | 0.44 | 1.13 | 0.0 | 557.90 | 205.01 |
| 20 | anchored_frozen | 0.57 | 0.35 | 1.00 | 0.0 | 472.39 | 208.65 |
| 50 | native_frozen | 7.30 | 1.96 | 9.77 | 87.6 | 51.98 | 25.41 |
| 50 | native_replay | 3.34 | 1.19 | 4.87 | 8.6 | 144.60 | 59.59 |
| 50 | anchored_frozen | 3.38 | 1.13 | 4.84 | 8.0 | 124.33 | 40.71 |
| 100 | native_frozen | 8.69 | 1.45 | 10.63 | 99.6 | 35.65 | 11.02 |
| 100 | native_replay | 4.16 | 0.99 | 5.44 | 19.0 | 106.26 | 29.02 |
| 100 | anchored_frozen | 4.19 | 0.94 | 5.39 | 19.8 | 96.47 | 22.14 |
| 200 | native_frozen | 9.31 | 1.11 | 10.75 | 100.0 | 30.45 | 5.95 |
| 200 | native_replay | 4.59 | 0.78 | 5.62 | 27.2 | 92.17 | 16.74 |
| 200 | anchored_frozen | 4.60 | 0.77 | 5.62 | 28.0 | 85.38 | 14.55 |
| 400 | native_frozen | 9.61 | 0.83 | 10.62 | 100.0 | 28.24 | 3.47 |
| 400 | native_replay | 4.80 | 0.61 | 5.56 | 35.0 | 86.22 | 10.53 |
| 400 | anchored_frozen | 4.81 | 0.61 | 5.58 | 35.8 | 79.82 | 9.10 |
| 1000 | native_frozen | 9.78 | 0.64 | 10.59 | 100.0 | 27.17 | 1.89 |
| 1000 | native_replay | 4.89 | 0.47 | 5.45 | 41.6 | 83.09 | 5.26 |
| 1000 | anchored_frozen | 4.90 | 0.47 | 5.50 | 39.8 | 77.35 | 4.32 |

CRC controls the mean of the loss over splits; the spread over splits shrinks with n as usual for split conformal methods. Set size is the mean number of labels per labelled sampled pixel at the grown vocabulary. Stored scores are float16 logits clamped to [-30, 30].