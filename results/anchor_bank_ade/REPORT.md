# Reference-bank sensitivity of anchored CAT-Seg

400 ADE development images (the headroom-probe 400). Released weights; only the bank changes. Sets: image-level CRC calibrated once at the 150 source labels; mean over 200 random 200/200 splits, fixed original split in brackets. Ranks are image-averaged.

## alpha = 0.1

| Bank | Labels in bank | Source rank | Rank at +695 | Source top1 | +695 top10 | Risk (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| coco171 | 171 | 2.40 | 5.70 | 69.71% | 90.80% | 9.55 (9.21) | 3.25 (3.36) | 3.88 (4.01) | 4.79 (4.86) | 7.34 (7.38) | 7.92 (7.94) |
| coco85 | 85 | 2.39 | 5.79 | 70.76% | 90.88% | 9.51 (10.72) | 3.84 (3.64) | 4.91 (4.64) | 6.39 (5.94) | 10.07 (9.24) | 11.18 (10.20) |
| coco20 | 20 | 2.62 | 6.77 | 67.67% | 88.42% | 9.51 (7.75) | 9.67 (10.35) | 12.61 (13.52) | 17.16 (18.32) | 29.71 (31.94) | 33.68 (36.29) |
| pascal171 | 171 | 2.33 | 5.36 | 70.49% | 91.01% | 9.54 (9.13) | 3.55 (3.73) | 4.36 (4.61) | 5.30 (5.55) | 8.09 (8.44) | 8.85 (9.23) |
| candidate_only | 0 | 5.92 | 19.57 | 23.23% | 49.26% | 9.42 (10.35) | 21.42 (20.56) | 28.58 (27.50) | 41.37 (39.66) | 72.09 (68.97) | 82.34 (78.59) |

## alpha = 0.05

| Bank | Labels in bank | Source rank | Rank at +695 | Source top1 | +695 top10 | Risk (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| coco171 | 171 | 2.40 | 5.70 | 69.71% | 90.80% | 4.57 (4.82) | 5.58 (5.54) | 6.95 (6.88) | 9.12 (8.87) | 14.93 (14.38) | 16.52 (15.85) |
| coco85 | 85 | 2.39 | 5.79 | 70.76% | 90.88% | 4.55 (5.27) | 7.02 (6.60) | 9.17 (8.59) | 12.60 (11.60) | 20.90 (19.05) | 23.56 (21.40) |
| coco20 | 20 | 2.62 | 6.77 | 67.67% | 88.42% | 4.60 (3.20) | 13.12 (14.67) | 17.17 (19.23) | 23.99 (26.90) | 42.37 (47.90) | 48.54 (55.10) |
| pascal171 | 171 | 2.33 | 5.36 | 70.49% | 91.01% | 4.55 (4.57) | 6.12 (6.26) | 7.79 (8.00) | 9.90 (10.06) | 16.14 (16.35) | 17.95 (18.16) |
| candidate_only | 0 | 5.92 | 19.57 | 23.23% | 49.26% | 4.48 (5.16) | 30.09 (28.66) | 39.94 (38.12) | 58.24 (55.43) | 102.98 (97.76) | 118.53 (112.25) |

Every bank gives a candidate-independent score; the bank is part of the frozen scoring rule, so the risk guarantee holds for each. Differences are efficiency only. Development data, previously inspected; one model size.