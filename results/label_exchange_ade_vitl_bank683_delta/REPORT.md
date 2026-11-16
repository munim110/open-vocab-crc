# A guarantee for the added labels under (weighted) label exchangeability

CAT-Seg (vitl_bank683), 2000 ADE validation images with a labelled sampled pixel (845-name vocabulary: 150 source names, then the A-847 annotation mapped to the added names), 500 trials (random half/half image split; source vocabulary as per design). Label loss = pooled fraction of the label's sampled pixels whose score for it is below the threshold. "Added, cal" = mean over added labels present in the calibration images (the quantity the proposition bounds); "added, held-out" = same on the held-out images; "src, class" = class-averaged source loss on held-out images; "src, image" = image-level source risk (the paper's guarantee); size = labels per labelled pixel at 845 names, held-out images; floor = % of added labels present whose threshold is the grid floor. Risks in % (and % of trials above alpha). Development data; nothing fitted.

## alpha = 0.1, exchangeable

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 845 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 9.50 (40) | 9.55 (40) | 9.49 (41) | 3.28 (0) | 27.55 | 0.0 | 113 / 523 | 9.14 | 0.37 | 3.49 |
| anchored, image-level (paper) | 23.18 (100) | 23.21 (99) | 23.15 (100) | 9.89 (44) | 7.70 | 0.0 | 113 / 523 | 22.98 | 0.20 | 3.49 |
| anchored, both | 9.50 (40) | 9.55 (40) | 9.49 (41) | 3.28 (0) | 27.55 | 0.0 | 113 / 523 | 9.14 | 0.37 | 3.49 |
| native, full known, label-level | 9.49 (40) | 9.54 (37) | 9.47 (39) | 2.93 (0) | 34.17 | 0.0 | 113 / 523 | 9.15 | 0.34 | 3.71 |
| anchored, weighted, all3 | 9.44 (40) | 9.48 (37) | 9.44 (40) | 3.27 (0) | 27.69 | 0.0 | 113 / 523 | 9.11 | 0.33 | nan |
| native, full known, weighted, all3 | 9.47 (40) | 9.51 (38) | 9.49 (41) | 2.96 (0) | 34.06 | 0.0 | 113 / 523 | 9.16 | 0.32 | nan |
| anchored, stratified, all3 | 8.28 (21) | 8.31 (22) | 8.27 (22) | 5.37 (4) | 35.93 | 0.0 | 113 / 523 | 7.48 | 0.80 | nan |

## alpha = 0.05, exchangeable

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 845 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 4.48 (36) | 4.51 (37) | 4.44 (37) | 1.20 (0) | 76.39 | 0.0 | 113 / 523 | 4.10 | 0.39 | 3.49 |
| anchored, image-level (paper) | 13.97 (100) | 13.99 (99) | 13.94 (99) | 4.90 (42) | 17.30 | 0.0 | 113 / 523 | 13.74 | 0.23 | 3.49 |
| anchored, both | 4.48 (36) | 4.51 (37) | 4.44 (37) | 1.20 (0) | 76.39 | 0.0 | 113 / 523 | 4.10 | 0.39 | 3.49 |
| native, full known, label-level | 4.05 (36) | 4.09 (37) | 3.88 (35) | 0.90 (0) | 260.11 | 0.0 | 113 / 523 | 3.27 | 0.77 | 3.71 |
| anchored, weighted, all3 | 4.45 (35) | 4.48 (36) | 4.47 (38) | 1.20 (0) | 76.76 | 0.0 | 113 / 523 | 4.09 | 0.36 | nan |
| native, full known, weighted, all3 | 4.04 (37) | 4.08 (38) | 3.93 (37) | 0.92 (0) | 257.68 | 0.0 | 113 / 523 | 3.32 | 0.72 | nan |
| anchored, stratified, all3 | 3.22 (12) | 3.22 (11) | 3.07 (12) | 1.95 (1) | 112.53 | 0.0 | 113 / 523 | 2.33 | 0.89 | nan |

## alpha = 0.1, dataset split

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 845 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 22.20 (100) | 22.25 (100) | 9.42 (25) | 4.91 (0) | 9.00 | 0.0 | 149 / 486 | 9.37 | 12.83 | 21.99 |
| anchored, image-level (paper) | 34.15 (100) | 34.15 (100) | 16.67 (100) | 9.89 (39) | 4.48 | 0.0 | 149 / 486 | 16.59 | 17.56 | 21.99 |
| anchored, both | 22.20 (100) | 22.25 (100) | 9.42 (25) | 4.91 (0) | 9.00 | 0.0 | 149 / 486 | 9.37 | 12.83 | 21.99 |
| native, full known, label-level | 22.65 (100) | 22.68 (100) | 9.43 (24) | 3.95 (0) | 10.14 | 0.0 | 149 / 486 | 9.37 | 13.28 | 24.58 |
| native, frozen at source, label-level | 33.80 (100) | 33.83 (100) | 15.64 (100) | 7.24 (0) | 5.11 | 0.0 | 149 / 486 | 9.37 | 24.43 | 35.85 |
| native, frozen at source, image-level | 54.05 (100) | 54.04 (100) | 30.30 (100) | 15.23 (100) | 2.20 | 0.0 | 149 / 486 | 20.14 | 33.91 | 35.85 |
| anchored, weighted, all3 | 9.55 (38) | 9.63 (41) | 3.35 (0) | 1.52 (0) | 27.44 | 0.0 | 149 / 486 | 3.34 | 6.21 | nan |
| native, full known, weighted, all3 | 10.81 (79) | 10.87 (82) | 3.52 (0) | 1.41 (0) | 30.31 | 0.0 | 149 / 486 | 3.53 | 7.28 | nan |
| anchored, stratified, all3 | 6.63 (0) | 6.69 (0) | 8.40 (4) | 5.62 (0) | 293.77 | 37.7 | 149 / 486 | 8.29 | -1.66 | nan |

## alpha = 0.05, dataset split

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 845 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 13.11 (100) | 13.19 (100) | 4.35 (14) | 2.09 (0) | 20.65 | 0.0 | 149 / 486 | 4.34 | 8.77 | 21.99 |
| anchored, image-level (paper) | 22.15 (100) | 22.20 (100) | 9.38 (100) | 4.89 (42) | 9.03 | 0.0 | 149 / 486 | 9.35 | 12.80 | 21.99 |
| anchored, both | 13.11 (100) | 13.19 (100) | 4.35 (14) | 2.09 (0) | 20.65 | 0.0 | 149 / 486 | 4.34 | 8.77 | 21.99 |
| native, full known, label-level | 12.98 (100) | 13.05 (100) | 4.38 (14) | 1.73 (0) | 24.24 | 0.0 | 149 / 486 | 4.35 | 8.63 | 24.58 |
| native, frozen at source, label-level | 21.43 (100) | 21.46 (100) | 8.77 (100) | 3.64 (0) | 11.11 | 0.0 | 149 / 486 | 4.35 | 17.09 | 35.85 |
| native, frozen at source, image-level | 37.22 (100) | 37.24 (100) | 17.74 (100) | 8.38 (100) | 4.31 | 0.0 | 149 / 486 | 10.85 | 26.38 | 35.85 |
| anchored, weighted, all3 | 1.90 (0) | 1.89 (0) | 1.45 (0) | 0.59 (0) | 322.35 | 37.7 | 149 / 486 | 1.42 | 0.48 | nan |
| native, full known, weighted, all3 | 5.34 (66) | 5.36 (67) | 1.35 (0) | 0.50 (0) | 108.26 | 0.0 | 149 / 486 | 1.30 | 4.04 | nan |
| anchored, stratified, all3 | 3.18 (0) | 3.19 (0) | 3.57 (1) | 2.22 (0) | 314.33 | 37.7 | 149 / 486 | 3.48 | -0.30 | nan |

## alpha = 0.1, exchangeable, native frozen

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 845 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 9.08 (35) | 9.14 (37) | 9.49 (41) | 2.87 (0) | 28.85 | 0.0 | 114 / 522 | 9.15 | -0.08 | 3.63 |
| anchored, image-level (paper) | 23.65 (100) | 23.61 (100) | 23.99 (100) | 9.99 (48) | 6.79 | 0.0 | 114 / 522 | 23.57 | 0.08 | 3.63 |
| anchored, both | 9.08 (35) | 9.14 (37) | 9.49 (41) | 2.87 (0) | 28.85 | 0.0 | 114 / 522 | 9.15 | -0.08 | 3.63 |
| native, full known, label-level | 9.20 (38) | 9.24 (37) | 9.39 (39) | 2.66 (0) | 35.80 | 0.0 | 114 / 522 | 9.17 | 0.03 | 3.34 |
| native, frozen at source, label-level | 20.76 (100) | 20.74 (100) | 21.48 (100) | 7.50 (20) | 9.67 | 0.0 | 114 / 522 | 9.15 | 11.62 | 23.65 |
| native, frozen at source, image-level | 47.61 (100) | 47.56 (100) | 47.61 (100) | 22.29 (100) | 2.34 | 0.0 | 114 / 522 | 27.10 | 20.51 | 23.65 |
| anchored, weighted, all3 | 9.03 (35) | 9.08 (37) | 9.44 (40) | 2.87 (0) | 29.21 | 0.0 | 114 / 522 | 9.11 | -0.08 | nan |
| native, full known, weighted, all3 | 9.16 (38) | 9.21 (38) | 9.35 (40) | 2.65 (0) | 36.09 | 0.0 | 114 / 522 | 9.14 | 0.02 | nan |
| anchored, stratified, all3 | 8.31 (26) | 8.37 (26) | 8.17 (20) | 5.73 (4) | 34.03 | 0.0 | 114 / 522 | 7.49 | 0.82 | nan |

## alpha = 0.05, exchangeable, native frozen

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 845 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 4.51 (38) | 4.55 (37) | 4.30 (35) | 1.15 (0) | 74.52 | 0.0 | 114 / 522 | 4.11 | 0.40 | 3.63 |
| anchored, image-level (paper) | 14.29 (100) | 14.32 (100) | 14.78 (100) | 4.97 (47) | 14.98 | 0.0 | 114 / 522 | 14.62 | -0.33 | 3.63 |
| anchored, both | 4.51 (38) | 4.55 (37) | 4.30 (35) | 1.15 (0) | 74.52 | 0.0 | 114 / 522 | 4.11 | 0.40 | 3.63 |
| native, full known, label-level | 4.30 (39) | 4.30 (37) | 3.96 (33) | 0.92 (0) | 228.11 | 0.0 | 114 / 522 | 3.48 | 0.81 | 3.34 |
| native, frozen at source, label-level | 11.78 (100) | 11.80 (100) | 12.13 (100) | 3.64 (19) | 24.34 | 0.0 | 114 / 522 | 4.11 | 7.67 | 23.65 |
| native, frozen at source, image-level | 31.90 (100) | 31.82 (100) | 32.53 (100) | 12.95 (100) | 4.79 | 0.0 | 114 / 522 | 16.05 | 15.85 | 23.65 |
| anchored, weighted, all3 | 4.53 (39) | 4.56 (37) | 4.32 (36) | 1.15 (0) | 75.13 | 0.0 | 114 / 522 | 4.11 | 0.42 | nan |
| native, full known, weighted, all3 | 4.16 (39) | 4.16 (37) | 3.81 (34) | 0.91 (0) | 251.33 | 0.0 | 114 / 522 | 3.33 | 0.83 | nan |
| anchored, stratified, all3 | 3.11 (15) | 3.16 (15) | 2.97 (8) | 1.84 (1) | 121.24 | 0.0 | 114 / 522 | 2.37 | 0.74 | nan |
