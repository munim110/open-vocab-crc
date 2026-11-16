# A guarantee for the added labels under (weighted) label exchangeability

CAT-Seg (vitl_bank683), 2000 Pascal Context validation images with a labelled sampled pixel (458-name vocabulary: 59 source names, then the PC-459 annotation mapped to the added names), 500 trials (random half/half image split; source vocabulary as per design). Label loss = pooled fraction of the label's sampled pixels whose score for it is below the threshold. "Added, cal" = mean over added labels present in the calibration images (the quantity the proposition bounds); "added, held-out" = same on the held-out images; "src, class" = class-averaged source loss on held-out images; "src, image" = image-level source risk (the paper's guarantee); size = labels per labelled pixel at 458 names, held-out images; floor = % of added labels present whose threshold is the grid floor. Risks in % (and % of trials above alpha). Development data; nothing fitted.

## alpha = 0.1, exchangeable

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 458 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 7.55 (23) | 7.51 (25) | 7.42 (25) | 4.24 (6) | 11.54 | 0.0 | 29 / 195 | 6.76 | 0.79 | 5.54 |
| anchored, image-level (paper) | 16.68 (86) | 16.69 (85) | 16.61 (81) | 9.92 (45) | 3.73 | 0.0 | 29 / 195 | 16.27 | 0.41 | 5.54 |
| anchored, both | 7.43 (23) | 7.40 (24) | 7.31 (25) | 4.10 (4) | 11.68 | 0.0 | 29 / 195 | 6.68 | 0.75 | 5.54 |
| native, full known, label-level | 7.61 (23) | 7.58 (24) | 7.35 (25) | 3.51 (3) | 14.92 | 0.0 | 29 / 195 | 6.77 | 0.83 | 5.95 |
| anchored, weighted, all3 | 7.48 (24) | 7.45 (25) | 7.52 (26) | 4.26 (7) | 12.61 | 0.0 | 29 / 195 | 6.90 | 0.58 | nan |
| native, full known, weighted, all3 | 7.43 (23) | 7.38 (23) | 7.37 (25) | 3.48 (4) | 15.82 | 0.0 | 29 / 195 | 6.77 | 0.66 | nan |
| anchored, stratified, all3 | 3.36 (0) | 3.37 (1) | 3.17 (1) | 3.35 (2) | 216.65 | 25.7 | 29 / 195 | 2.36 | 0.99 | nan |

## alpha = 0.05, exchangeable

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 458 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 2.76 (16) | 2.74 (16) | 2.65 (18) | 1.03 (2) | 68.36 | 0.6 | 29 / 195 | 1.59 | 1.17 | 5.54 |
| anchored, image-level (paper) | 9.82 (90) | 9.84 (90) | 9.54 (81) | 4.90 (44) | 7.14 | 0.0 | 29 / 195 | 9.50 | 0.32 | 5.54 |
| anchored, both | 2.75 (16) | 2.74 (16) | 2.64 (18) | 1.02 (2) | 68.40 | 0.6 | 29 / 195 | 1.58 | 1.17 | 5.54 |
| native, full known, label-level | 2.74 (16) | 2.72 (17) | 2.67 (18) | 0.89 (1) | 92.77 | 0.6 | 29 / 195 | 1.46 | 1.29 | 5.95 |
| anchored, weighted, all3 | 2.61 (14) | 2.56 (13) | 2.74 (19) | 1.03 (2) | 87.59 | 5.4 | 29 / 195 | 1.74 | 0.87 | nan |
| native, full known, weighted, all3 | 2.57 (13) | 2.53 (14) | 2.68 (19) | 0.88 (1) | 112.18 | 5.1 | 29 / 195 | 1.58 | 0.99 | nan |
| anchored, stratified, all3 | 0.04 (0) | 0.04 (0) | 0.04 (0) | 0.04 (0) | 448.01 | 95.4 | 29 / 195 | 0.02 | 0.02 | nan |

## alpha = 0.1, dataset split

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 458 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 22.30 (100) | 22.29 (100) | 8.48 (7) | 8.40 (1) | 2.73 | 0.0 | 59 / 165 | 8.43 | 13.87 | 25.79 |
| anchored, image-level (paper) | 24.66 (100) | 24.64 (100) | 9.85 (39) | 9.88 (44) | 2.45 | 0.0 | 59 / 165 | 9.82 | 14.84 | 25.79 |
| anchored, both | 22.30 (100) | 22.29 (100) | 8.48 (7) | 8.40 (1) | 2.73 | 0.0 | 59 / 165 | 8.43 | 13.87 | 25.79 |
| native, full known, label-level | 26.53 (100) | 26.52 (100) | 8.48 (9) | 7.55 (0) | 2.59 | 0.0 | 59 / 165 | 8.44 | 18.09 | 34.66 |
| native, frozen at source, label-level | 39.89 (100) | 39.86 (100) | 15.82 (100) | 13.80 (100) | 1.62 | 0.0 | 59 / 165 | 8.43 | 31.46 | 44.32 |
| native, frozen at source, image-level | 42.84 (100) | 42.84 (100) | 17.45 (100) | 15.06 (100) | 1.51 | 0.0 | 59 / 165 | 9.59 | 33.25 | 44.32 |
| anchored, weighted, all3 | 4.24 (0) | 4.26 (0) | 4.25 (0) | 4.69 (0) | 309.33 | 64.6 | 59 / 165 | 4.25 | -0.01 | nan |
| native, full known, weighted, all3 | 8.09 (3) | 8.04 (3) | 10.62 (71) | 9.67 (40) | 307.97 | 62.2 | 59 / 165 | 10.66 | -2.57 | nan |
| anchored, stratified, all3 | 6.26 (0) | 6.24 (0) | 7.80 (0) | 8.71 (6) | 308.32 | 64.6 | 59 / 165 | 7.76 | -1.50 | nan |

## alpha = 0.05, dataset split

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 458 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 12.58 (100) | 12.56 (100) | 3.42 (1) | 3.38 (0) | 4.99 | 0.0 | 59 / 165 | 3.37 | 9.21 | 25.79 |
| anchored, image-level (paper) | 15.97 (100) | 15.99 (100) | 4.86 (39) | 4.89 (40) | 3.89 | 0.0 | 59 / 165 | 4.85 | 11.12 | 25.79 |
| anchored, both | 12.58 (100) | 12.56 (100) | 3.42 (1) | 3.38 (0) | 4.99 | 0.0 | 59 / 165 | 3.37 | 9.21 | 25.79 |
| native, full known, label-level | 15.56 (100) | 15.55 (100) | 3.46 (1) | 3.12 (0) | 4.93 | 0.0 | 59 / 165 | 3.37 | 12.19 | 34.66 |
| native, frozen at source, label-level | 24.41 (100) | 24.41 (100) | 7.28 (100) | 6.52 (99) | 2.87 | 0.0 | 59 / 165 | 3.37 | 21.04 | 44.32 |
| native, frozen at source, image-level | 28.53 (100) | 28.48 (100) | 9.60 (100) | 8.56 (100) | 2.37 | 0.0 | 59 / 165 | 4.65 | 23.88 | 44.32 |
| anchored, weighted, all3 | 2.90 (0) | 2.94 (0) | 2.64 (0) | 2.75 (0) | 310.53 | 64.6 | 59 / 165 | 2.61 | 0.29 | nan |
| native, full known, weighted, all3 | 4.73 (42) | 4.73 (39) | 4.50 (31) | 4.17 (21) | 309.36 | 62.2 | 59 / 165 | 4.46 | 0.27 | nan |
| anchored, stratified, all3 | 3.24 (0) | 3.29 (1) | 3.09 (0) | 3.30 (0) | 310.09 | 64.6 | 59 / 165 | 3.04 | 0.20 | nan |
