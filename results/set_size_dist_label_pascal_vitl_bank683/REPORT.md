# Distribution of the per-pixel set size under the label-level threshold

2000 Pascal Context validation images, 59 source and 458 grown names; the 500 trials of results/label_exchange_pascal_vitl_bank683_schemes (random half split per trial); distribution over labelled pixels (source or added) of the held-out half, image-weighted as the size column of the label-exchange report; mean over trials.

## a0.1, exchangeable

| Arm | empty (%) | =1 (%) | <=3 (%) | <=10 (%) | >10 (%) | median | p90 | mean | reference mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 0.0 | 14.1 | 35.0 | 70.1 | 29.9 | 6 | 26 | 11.54 | 11.54 |
| anchored, image-level (paper) | 0.7 | 34.5 | 65.2 | 94.5 | 5.5 | 2 | 8 | 3.73 | 3.73 |
| anchored, both | 0.0 | 13.8 | 34.5 | 69.6 | 30.4 | 6 | 26 | 11.68 | 11.68 |
| native, full known, label-level | 0.0 | 9.8 | 25.4 | 59.5 | 40.5 | 8 | 34 | 14.92 | 14.92 |

## a0.05, exchangeable

| Arm | empty (%) | =1 (%) | <=3 (%) | <=10 (%) | >10 (%) | median | p90 | mean | reference mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 0.0 | 2.4 | 9.0 | 27.8 | 72.2 | 25 | 201 | 68.36 | 68.36 |
| anchored, image-level (paper) | 0.1 | 19.9 | 45.1 | 81.2 | 18.8 | 4 | 16 | 7.14 | 7.14 |
| anchored, both | 0.0 | 2.4 | 9.0 | 27.7 | 72.3 | 25 | 201 | 68.40 | 68.40 |
| native, full known, label-level | 0.0 | 1.3 | 5.0 | 18.1 | 81.9 | 40 | 277 | 92.77 | 92.77 |

## a0.1, dataset split

| Arm | empty (%) | =1 (%) | <=3 (%) | <=10 (%) | >10 (%) | median | p90 | mean | reference mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 0.3 | 39.1 | 72.7 | 99.1 | 0.9 | 2 | 6 | 2.73 | 2.73 |
| anchored, image-level (paper) | 0.4 | 42.8 | 77.3 | 99.6 | 0.4 | 2 | 5 | 2.45 | 2.45 |
| anchored, both | 0.3 | 39.1 | 72.7 | 99.1 | 0.9 | 2 | 6 | 2.73 | 2.73 |
| native, full known, label-level | 0.0 | 38.6 | 73.9 | 99.9 | 0.1 | 2 | 5 | 2.59 | 2.59 |

## a0.05, dataset split

| Arm | empty (%) | =1 (%) | <=3 (%) | <=10 (%) | >10 (%) | median | p90 | mean | reference mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 0.0 | 22.7 | 50.2 | 88.9 | 11.1 | 3 | 11 | 4.99 | 4.99 |
| anchored, image-level (paper) | 0.1 | 28.8 | 58.8 | 94.8 | 5.2 | 3 | 8 | 3.89 | 3.89 |
| anchored, both | 0.0 | 22.7 | 50.2 | 88.9 | 11.1 | 3 | 11 | 4.99 | 4.99 |
| native, full known, label-level | 0.0 | 21.5 | 47.3 | 89.8 | 10.2 | 4 | 11 | 4.93 | 4.93 |

Median and p90: of the trial-averaged distribution. The `distribution` field of results.json is that distribution over set sizes 0..T.