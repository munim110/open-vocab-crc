# Distribution of the per-pixel set size under the label-level threshold

2000 ADE validation images, 150 source and 845 grown names; the 500 trials of results/label_exchange_ade_sed_bank683_schemes (random half split per trial); distribution over labelled pixels (source or added) of the held-out half, image-weighted as the size column of the label-exchange report; mean over trials.

## a0.1, exchangeable

| Arm | empty (%) | =1 (%) | <=3 (%) | <=10 (%) | >10 (%) | median | p90 | mean | reference mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 0.0 | 0.6 | 2.9 | 12.9 | 87.1 | 34 | 98 | 45.10 | 45.10 |
| anchored, image-level (paper) | 0.1 | 10.8 | 22.9 | 55.4 | 44.6 | 9 | 38 | 16.79 | 16.79 |
| anchored, both | 0.0 | 0.6 | 2.7 | 12.3 | 87.7 | 35 | 102 | 46.95 | 46.95 |
| native, full known, label-level | 0.0 | 0.0 | 0.2 | 3.5 | 96.5 | 44 | 97 | 51.38 | 51.38 |

## a0.05, exchangeable

| Arm | empty (%) | =1 (%) | <=3 (%) | <=10 (%) | >10 (%) | median | p90 | mean | reference mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 0.0 | 0.0 | 0.1 | 1.5 | 98.5 | 95 | 242 | 118.47 | 118.47 |
| anchored, image-level (paper) | 0.0 | 3.6 | 9.1 | 26.5 | 73.5 | 22 | 95 | 39.10 | 39.10 |
| anchored, both | 0.0 | 0.0 | 0.1 | 1.4 | 98.6 | 97 | 245 | 120.54 | 120.54 |
| native, full known, label-level | 0.0 | 0.0 | 0.0 | 0.0 | 100.0 | 121 | 254 | 139.80 | 139.80 |

## a0.1, dataset split

| Arm | empty (%) | =1 (%) | <=3 (%) | <=10 (%) | >10 (%) | median | p90 | mean | reference mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 0.0 | 8.2 | 17.9 | 48.4 | 51.6 | 11 | 31 | 14.10 | 14.10 |
| anchored, image-level (paper) | 0.1 | 18.2 | 37.8 | 81.3 | 18.7 | 5 | 14 | 6.32 | 6.32 |
| anchored, both | 0.0 | 8.2 | 17.9 | 48.4 | 51.6 | 11 | 31 | 14.10 | 14.10 |
| native, full known, label-level | 0.0 | 1.9 | 5.9 | 32.5 | 67.5 | 14 | 29 | 15.91 | 15.91 |

## a0.05, dataset split

| Arm | empty (%) | =1 (%) | <=3 (%) | <=10 (%) | >10 (%) | median | p90 | mean | reference mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 0.0 | 0.7 | 4.3 | 16.7 | 83.3 | 27 | 75 | 35.04 | 35.04 |
| anchored, image-level (paper) | 0.0 | 6.9 | 15.6 | 42.8 | 57.2 | 12 | 35 | 16.17 | 16.17 |
| anchored, both | 0.0 | 0.7 | 4.3 | 16.7 | 83.3 | 27 | 75 | 35.04 | 35.04 |
| native, full known, label-level | 0.0 | 0.0 | 0.0 | 3.2 | 96.8 | 40 | 80 | 44.79 | 44.79 |

Median and p90: of the trial-averaged distribution. The `distribution` field of results.json is that distribution over set sizes 0..T.