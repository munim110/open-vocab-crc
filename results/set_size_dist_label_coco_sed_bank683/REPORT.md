# Distribution of the per-pixel set size under the label-level threshold

2000 COCO val2017 (LVIS-annotated) images, 171 source and 1283 grown names; the 500 trials of results/label_exchange_coco_sed_bank683_schemes (random half split per trial); distribution over labelled pixels (source or added) of the held-out half, image-weighted as the size column of the label-exchange report; mean over trials.

## a0.1, exchangeable

| Arm | empty (%) | =1 (%) | <=3 (%) | <=10 (%) | >10 (%) | median | p90 | mean | reference mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 0.0 | 0.5 | 7.0 | 34.7 | 65.3 | 15 | 45 | 21.24 | 21.24 |
| anchored, image-level (paper) | 0.0 | 6.7 | 30.4 | 76.2 | 23.8 | 6 | 16 | 7.68 | 7.68 |
| anchored, both | 0.0 | 0.5 | 7.0 | 34.7 | 65.3 | 15 | 45 | 21.24 | 21.24 |
| native, full known, label-level | 0.0 | 0.1 | 2.7 | 23.5 | 76.5 | 19 | 47 | 23.91 | 23.91 |

## a0.05, exchangeable

| Arm | empty (%) | =1 (%) | <=3 (%) | <=10 (%) | >10 (%) | median | p90 | mean | reference mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 0.0 | 0.0 | 1.0 | 9.7 | 90.3 | 42 | 130 | 60.08 | 60.08 |
| anchored, image-level (paper) | 0.0 | 1.9 | 13.3 | 49.5 | 50.5 | 11 | 32 | 14.77 | 14.77 |
| anchored, both | 0.0 | 0.0 | 1.0 | 9.7 | 90.3 | 42 | 130 | 60.08 | 60.08 |
| native, full known, label-level | 0.0 | 0.0 | 0.2 | 4.4 | 95.6 | 52 | 133 | 66.58 | 66.58 |

## a0.1, dataset split

| Arm | empty (%) | =1 (%) | <=3 (%) | <=10 (%) | >10 (%) | median | p90 | mean | reference mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 0.0 | 5.7 | 28.3 | 77.9 | 22.1 | 6 | 14 | 7.24 | 7.24 |
| anchored, image-level (paper) | 0.2 | 17.6 | 60.7 | 98.0 | 2.0 | 3 | 7 | 3.60 | 3.60 |
| anchored, both | 0.0 | 5.7 | 28.3 | 77.9 | 22.1 | 6 | 14 | 7.24 | 7.24 |
| native, full known, label-level | 0.0 | 1.4 | 16.7 | 78.5 | 21.5 | 7 | 13 | 7.55 | 7.55 |

## a0.05, dataset split

| Arm | empty (%) | =1 (%) | <=3 (%) | <=10 (%) | >10 (%) | median | p90 | mean | reference mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 0.0 | 0.9 | 10.3 | 45.4 | 54.6 | 12 | 30 | 14.85 | 14.85 |
| anchored, image-level (paper) | 0.0 | 7.1 | 33.7 | 84.1 | 15.9 | 5 | 12 | 6.27 | 6.27 |
| anchored, both | 0.0 | 0.9 | 10.3 | 45.4 | 54.6 | 12 | 30 | 14.85 | 14.85 |
| native, full known, label-level | 0.0 | 0.2 | 5.3 | 37.6 | 62.4 | 13 | 28 | 14.95 | 14.95 |

Median and p90: of the trial-averaged distribution. The `distribution` field of results.json is that distribution over set sizes 0..T.