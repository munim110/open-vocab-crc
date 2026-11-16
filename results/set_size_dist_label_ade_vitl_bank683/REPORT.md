# Distribution of the per-pixel set size under the label-level threshold

2000 ADE validation images, 150 source and 845 grown names; the 500 trials of results/label_exchange_ade_vitl_bank683 (random half split per trial); distribution over labelled pixels (source or added) of the held-out half, image-weighted as the size column of the label-exchange report; mean over trials.

## a0.1, exchangeable

| Arm | empty (%) | =1 (%) | <=3 (%) | <=10 (%) | >10 (%) | median | p90 | mean | reference mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 0.0 | 1.3 | 5.4 | 26.3 | 73.7 | 19 | 61 | 27.55 | 27.55 |
| anchored, image-level (paper) | 0.1 | 14.7 | 34.8 | 76.4 | 23.6 | 6 | 17 | 7.70 | 7.70 |
| anchored, both | 0.0 | 1.3 | 5.4 | 26.3 | 73.7 | 19 | 61 | 27.55 | 27.55 |
| native, full known, label-level | 0.0 | 0.1 | 0.9 | 13.7 | 86.3 | 26 | 70 | 34.17 | 34.17 |

## a0.05, exchangeable

| Arm | empty (%) | =1 (%) | <=3 (%) | <=10 (%) | >10 (%) | median | p90 | mean | reference mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 0.0 | 0.1 | 0.3 | 4.8 | 95.2 | 54 | 168 | 76.39 | 76.39 |
| anchored, image-level (paper) | 0.0 | 5.1 | 15.1 | 45.4 | 54.6 | 12 | 39 | 17.30 | 17.30 |
| anchored, both | 0.0 | 0.1 | 0.3 | 4.8 | 95.2 | 54 | 168 | 76.39 | 76.39 |
| native, full known, label-level | 0.0 | 0.0 | 0.0 | 0.7 | 99.3 | 118 | 845 | 260.11 | 260.11 |

## a0.1, dataset split

| Arm | empty (%) | =1 (%) | <=3 (%) | <=10 (%) | >10 (%) | median | p90 | mean | reference mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 0.0 | 10.4 | 26.5 | 67.1 | 32.9 | 7 | 19 | 9.00 | 9.00 |
| anchored, image-level (paper) | 0.3 | 22.1 | 49.3 | 93.6 | 6.4 | 4 | 9 | 4.48 | 4.48 |
| anchored, both | 0.0 | 10.4 | 26.5 | 67.1 | 32.9 | 7 | 19 | 9.00 | 9.00 |
| native, full known, label-level | 0.0 | 3.8 | 15.3 | 60.8 | 39.2 | 9 | 20 | 10.14 | 10.14 |

## a0.05, dataset split

| Arm | empty (%) | =1 (%) | <=3 (%) | <=10 (%) | >10 (%) | median | p90 | mean | reference mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 0.0 | 2.0 | 8.1 | 33.5 | 66.5 | 16 | 45 | 20.65 | 20.65 |
| anchored, image-level (paper) | 0.0 | 10.3 | 26.4 | 67.0 | 33.0 | 7 | 19 | 9.03 | 9.03 |
| anchored, both | 0.0 | 2.0 | 8.1 | 33.5 | 66.5 | 16 | 45 | 20.65 | 20.65 |
| native, full known, label-level | 0.0 | 0.2 | 1.2 | 20.1 | 79.9 | 20 | 47 | 24.24 | 24.24 |

## a0.1, exchangeable, native frozen

| Arm | empty (%) | =1 (%) | <=3 (%) | <=10 (%) | >10 (%) | median | p90 | mean | reference mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 0.0 | 1.1 | 4.8 | 24.7 | 75.3 | 20 | 64 | 28.85 | 28.85 |
| anchored, image-level (paper) | 0.1 | 15.3 | 35.8 | 79.7 | 20.3 | 5 | 14 | 6.79 | 6.79 |
| anchored, both | 0.0 | 1.1 | 4.8 | 24.7 | 75.3 | 20 | 64 | 28.85 | 28.85 |
| native, full known, label-level | 0.0 | 0.1 | 0.8 | 12.6 | 87.4 | 27 | 73 | 35.80 | 35.80 |

## a0.05, exchangeable, native frozen

| Arm | empty (%) | =1 (%) | <=3 (%) | <=10 (%) | >10 (%) | median | p90 | mean | reference mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 0.0 | 0.0 | 0.3 | 4.7 | 95.3 | 53 | 163 | 74.52 | 74.52 |
| anchored, image-level (paper) | 0.0 | 5.2 | 16.2 | 47.9 | 52.1 | 11 | 32 | 14.98 | 14.98 |
| anchored, both | 0.0 | 0.0 | 0.3 | 4.7 | 95.3 | 53 | 163 | 74.52 | 74.52 |
| native, full known, label-level | 0.0 | 0.0 | 0.0 | 0.7 | 99.3 | 113 | 845 | 228.11 | 228.11 |

Median and p90: of the trial-averaged distribution. The `distribution` field of results.json is that distribution over set sizes 0..T.