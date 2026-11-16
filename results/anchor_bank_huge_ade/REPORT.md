# Reference-bank sensitivity of anchored CAT-Seg

400 ADE development images (the headroom-probe 400). Released weights; only the bank changes. Sets: image-level CRC calibrated once at the 150 source labels; mean over 200 random 200/200 splits, fixed original split in brackets. Ranks are image-averaged.

## alpha = 0.1

| Bank | Labels in bank | Source rank | Rank at +695 | Source top1 | +695 top10 | Risk (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| coco171 | 171 | 2.40 | 5.70 | 69.71% | 90.80% | 9.55 (9.21) | 3.25 (3.36) | 3.88 (4.01) | 4.79 (4.86) | 7.34 (7.38) | 7.92 (7.94) |
| coco_oi1366 | 1366 | 2.30 | 5.33 | 72.33% | 91.48% | 9.52 (9.58) | 2.96 (3.02) | 3.53 (3.60) | 4.31 (4.34) | 6.45 (6.41) | 6.87 (6.80) |
| coco_oi2731 | 2731 | 2.31 | 5.37 | 72.31% | 91.33% | 9.49 (9.73) | 3.01 (3.04) | 3.64 (3.67) | 4.45 (4.43) | 6.73 (6.62) | 7.20 (7.07) |
| coco_oi5462 | 5462 | 2.31 | 5.39 | 72.11% | 91.20% | 9.49 (9.74) | 3.14 (3.16) | 3.82 (3.84) | 4.68 (4.65) | 7.11 (7.00) | 7.62 (7.48) |
| oi683 | 683 | 2.32 | 5.44 | 71.92% | 91.05% | 9.51 (9.79) | 3.41 (3.40) | 4.24 (4.23) | 5.26 (5.20) | 8.13 (7.96) | 8.78 (8.58) |

## alpha = 0.05

| Bank | Labels in bank | Source rank | Rank at +695 | Source top1 | +695 top10 | Risk (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| coco171 | 171 | 2.40 | 5.70 | 69.71% | 90.80% | 4.57 (4.82) | 5.58 (5.54) | 6.95 (6.88) | 9.12 (8.87) | 14.93 (14.38) | 16.52 (15.85) |
| coco_oi1366 | 1366 | 2.30 | 5.33 | 72.33% | 91.48% | 4.53 (4.62) | 5.35 (5.35) | 6.73 (6.73) | 8.67 (8.56) | 13.90 (13.62) | 15.23 (14.90) |
| coco_oi2731 | 2731 | 2.31 | 5.37 | 72.31% | 91.33% | 4.53 (4.71) | 5.54 (5.48) | 7.03 (6.95) | 9.08 (8.86) | 14.60 (14.11) | 16.01 (15.46) |
| coco_oi5462 | 5462 | 2.31 | 5.39 | 72.11% | 91.20% | 4.54 (4.65) | 5.75 (5.73) | 7.33 (7.32) | 9.49 (9.34) | 15.25 (14.90) | 16.75 (16.34) |
| oi683 | 683 | 2.32 | 5.44 | 71.92% | 91.05% | 4.55 (4.53) | 6.13 (6.14) | 7.91 (7.95) | 10.38 (10.31) | 16.81 (16.58) | 18.52 (18.26) |

Every bank gives a candidate-independent score; the bank is part of the frozen scoring rule, so the risk guarantee holds for each. Differences are efficiency only. Development data, previously inspected; one model size.