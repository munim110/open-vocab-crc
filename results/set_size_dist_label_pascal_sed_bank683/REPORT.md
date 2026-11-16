# Distribution of the per-pixel set size under the label-level threshold

2000 Pascal Context validation images, 59 source and 458 grown names; the 500 trials of results/label_exchange_pascal_sed_bank683_schemes (random half split per trial); distribution over labelled pixels (source or added) of the held-out half, image-weighted as the size column of the label-exchange report; mean over trials.

## a0.1, exchangeable

| Arm | empty (%) | =1 (%) | <=3 (%) | <=10 (%) | >10 (%) | median | p90 | mean | reference mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 0.0 | 3.3 | 14.1 | 51.2 | 48.8 | 10 | 40 | 17.48 | 17.48 |
| anchored, image-level (paper) | 0.6 | 15.3 | 44.8 | 87.0 | 13.0 | 4 | 12 | 5.87 | 5.87 |
| anchored, both | 0.0 | 3.2 | 13.7 | 50.5 | 49.5 | 10 | 40 | 17.76 | 17.76 |
| native, full known, label-level | 0.0 | 1.3 | 7.4 | 42.0 | 58.0 | 13 | 44 | 20.15 | 20.15 |

## a0.05, exchangeable

| Arm | empty (%) | =1 (%) | <=3 (%) | <=10 (%) | >10 (%) | median | p90 | mean | reference mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 0.0 | 0.3 | 2.0 | 15.0 | 85.0 | 40 | 214 | 80.37 | 80.37 |
| anchored, image-level (paper) | 0.1 | 6.0 | 22.6 | 65.1 | 34.9 | 7 | 25 | 11.78 | 11.78 |
| anchored, both | 0.0 | 0.3 | 2.0 | 14.7 | 85.3 | 40 | 214 | 80.48 | 80.48 |
| native, full known, label-level | 0.0 | 0.1 | 0.7 | 8.9 | 91.1 | 48 | 222 | 86.88 | 86.88 |

## a0.1, dataset split

| Arm | empty (%) | =1 (%) | <=3 (%) | <=10 (%) | >10 (%) | median | p90 | mean | reference mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 0.6 | 19.2 | 60.0 | 98.3 | 1.7 | 3 | 7 | 3.55 | 3.55 |
| anchored, image-level (paper) | 0.9 | 26.1 | 70.5 | 99.5 | 0.5 | 2 | 6 | 2.89 | 2.89 |
| anchored, both | 0.6 | 19.2 | 60.0 | 98.3 | 1.7 | 3 | 7 | 3.55 | 3.55 |
| native, full known, label-level | 0.0 | 10.9 | 51.8 | 99.6 | 0.4 | 3 | 6 | 3.70 | 3.70 |

## a0.05, dataset split

| Arm | empty (%) | =1 (%) | <=3 (%) | <=10 (%) | >10 (%) | median | p90 | mean | reference mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 0.1 | 8.2 | 30.1 | 81.7 | 18.3 | 5 | 13 | 6.71 | 6.71 |
| anchored, image-level (paper) | 0.3 | 12.0 | 42.8 | 92.3 | 7.7 | 4 | 10 | 4.94 | 4.94 |
| anchored, both | 0.1 | 8.2 | 30.1 | 81.7 | 18.3 | 5 | 13 | 6.71 | 6.71 |
| native, full known, label-level | 0.0 | 4.5 | 21.9 | 81.5 | 18.5 | 6 | 13 | 6.99 | 6.99 |

Median and p90: of the trial-averaged distribution. The `distribution` field of results.json is that distribution over set sizes 0..T.