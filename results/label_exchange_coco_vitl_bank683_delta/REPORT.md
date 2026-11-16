# A guarantee for the added labels under (weighted) label exchangeability

CAT-Seg (vitl_bank683), 2000 COCO val2017 (LVIS-annotated) images with a labelled sampled pixel (1283-name vocabulary: 171 source names, then the LVIS v1 annotation mapped to the added names), 500 trials (random half/half image split; source vocabulary as per design). Label loss = pooled fraction of the label's sampled pixels whose score for it is below the threshold. "Added, cal" = mean over added labels present in the calibration images (the quantity the proposition bounds); "added, held-out" = same on the held-out images; "src, class" = class-averaged source loss on held-out images; "src, image" = image-level source risk (the paper's guarantee); size = labels per labelled pixel at 1283 names, held-out images; floor = % of added labels present whose threshold is the grid floor. Risks in % (and % of trials above alpha). Development data; nothing fitted.

## alpha = 0.1, exchangeable

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 1283 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 8.93 (33) | 9.02 (34) | 8.93 (35) | 4.46 (2) | 11.93 | 0.0 | 72 / 466 | 8.62 | 0.31 | 3.86 |
| anchored, image-level (paper) | 17.74 (98) | 17.78 (97) | 17.86 (97) | 9.87 (46) | 5.71 | 0.0 | 72 / 466 | 17.75 | -0.01 | 3.86 |
| anchored, both | 8.91 (33) | 8.99 (34) | 8.91 (35) | 4.44 (2) | 11.94 | 0.0 | 72 / 466 | 8.61 | 0.31 | 3.86 |
| native, full known, label-level | 8.97 (33) | 9.03 (35) | 8.98 (38) | 4.04 (2) | 13.59 | 0.0 | 72 / 466 | 8.63 | 0.34 | 4.12 |
| anchored, weighted, all3 | 8.95 (32) | 9.02 (33) | 8.97 (36) | 4.47 (2) | 11.88 | 0.0 | 72 / 466 | 8.69 | 0.26 | nan |
| native, full known, weighted, all3 | 8.98 (34) | 9.04 (35) | 9.06 (39) | 4.08 (2) | 13.51 | 0.0 | 72 / 466 | 8.70 | 0.28 | nan |
| anchored, stratified, all3 | 7.06 (6) | 7.14 (9) | 6.90 (11) | 7.45 (18) | 198.47 | 5.2 | 72 / 466 | 6.16 | 0.90 | nan |

## alpha = 0.05, exchangeable

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 1283 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 4.01 (27) | 4.06 (28) | 3.96 (30) | 1.71 (1) | 30.23 | 0.0 | 72 / 466 | 3.56 | 0.45 | 3.86 |
| anchored, image-level (paper) | 10.34 (98) | 10.38 (97) | 10.39 (94) | 4.81 (42) | 10.43 | 0.0 | 72 / 466 | 10.35 | -0.01 | 3.86 |
| anchored, both | 4.00 (27) | 4.05 (28) | 3.95 (30) | 1.71 (1) | 30.25 | 0.0 | 72 / 466 | 3.55 | 0.45 | 3.86 |
| native, full known, label-level | 4.05 (28) | 4.15 (31) | 4.02 (31) | 1.42 (1) | 42.13 | 0.0 | 72 / 466 | 3.56 | 0.49 | 4.12 |
| anchored, weighted, all3 | 4.01 (27) | 4.06 (28) | 3.98 (30) | 1.72 (1) | 30.30 | 0.0 | 72 / 466 | 3.61 | 0.40 | nan |
| native, full known, weighted, all3 | 4.04 (28) | 4.15 (31) | 4.05 (32) | 1.42 (1) | 43.50 | 0.0 | 72 / 466 | 3.59 | 0.45 | nan |
| anchored, stratified, all3 | 2.23 (1) | 2.28 (2) | 2.16 (5) | 2.52 (4) | 509.82 | 16.2 | 72 / 466 | 1.62 | 0.61 | nan |

## alpha = 0.1, dataset split

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 1283 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 17.60 (100) | 17.67 (100) | 9.50 (31) | 4.48 (0) | 6.29 | 0.0 | 170 / 367 | 9.44 | 8.16 | 29.71 |
| anchored, image-level (paper) | 32.14 (100) | 31.99 (100) | 17.96 (100) | 9.87 (42) | 3.27 | 0.0 | 170 / 367 | 17.96 | 14.19 | 29.71 |
| anchored, both | 17.60 (100) | 17.67 (100) | 9.50 (31) | 4.48 (0) | 6.29 | 0.0 | 170 / 367 | 9.44 | 8.16 | 29.71 |
| native, full known, label-level | 21.23 (100) | 21.29 (100) | 9.51 (32) | 4.28 (0) | 5.59 | 0.0 | 170 / 367 | 9.44 | 11.79 | 31.14 |
| native, frozen at source, label-level | 29.18 (100) | 29.15 (100) | 13.36 (100) | 6.37 (0) | 3.93 | 0.0 | 170 / 367 | 9.44 | 19.74 | 39.38 |
| native, frozen at source, image-level | 47.32 (100) | 47.13 (100) | 23.17 (100) | 12.81 (100) | 2.14 | 0.0 | 170 / 367 | 18.05 | 29.27 | 39.38 |
| anchored, weighted, all3 | 3.94 (0) | 4.00 (0) | 2.34 (0) | 0.94 (0) | 33.98 | 0.0 | 170 / 367 | 2.25 | 1.69 | nan |
| native, full known, weighted, all3 | 7.19 (7) | 7.24 (8) | 3.53 (0) | 1.37 (0) | 38.57 | 0.0 | 170 / 367 | 3.44 | 3.75 | nan |
| anchored, stratified, all3 | 6.47 (0) | 6.49 (0) | 8.77 (9) | 5.69 (0) | 439.68 | 17.3 | 170 / 367 | 8.59 | -2.12 | nan |

## alpha = 0.05, dataset split

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 1283 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 8.92 (100) | 9.01 (100) | 4.47 (25) | 1.66 (0) | 13.25 | 0.0 | 170 / 367 | 4.42 | 4.50 | 29.71 |
| anchored, image-level (paper) | 18.76 (100) | 18.83 (100) | 10.20 (100) | 4.91 (43) | 5.85 | 0.0 | 170 / 367 | 10.16 | 8.59 | 29.71 |
| anchored, both | 8.92 (100) | 9.01 (100) | 4.47 (25) | 1.66 (0) | 13.25 | 0.0 | 170 / 367 | 4.42 | 4.50 | 29.71 |
| native, full known, label-level | 11.42 (100) | 11.50 (100) | 4.48 (29) | 1.68 (0) | 11.71 | 0.0 | 170 / 367 | 4.43 | 6.99 | 31.14 |
| native, frozen at source, label-level | 16.05 (100) | 16.09 (100) | 6.89 (98) | 2.86 (0) | 7.72 | 0.0 | 170 / 367 | 4.43 | 11.62 | 39.38 |
| native, frozen at source, image-level | 30.98 (100) | 30.92 (100) | 14.49 (100) | 6.99 (100) | 3.63 | 0.0 | 170 / 367 | 10.22 | 20.76 | 39.38 |
| anchored, weighted, all3 | 1.18 (0) | 1.20 (0) | 0.90 (0) | 0.40 (0) | 484.89 | 17.3 | 170 / 367 | 0.88 | 0.31 | nan |
| native, full known, weighted, all3 | 2.26 (2) | 2.34 (3) | 1.53 (0) | 0.60 (0) | 514.95 | 29.3 | 170 / 367 | 1.42 | 0.84 | nan |
| anchored, stratified, all3 | 2.02 (0) | 2.03 (0) | 3.89 (3) | 2.40 (0) | 863.68 | 61.9 | 170 / 367 | 3.83 | -1.82 | nan |
