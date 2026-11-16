# A guarantee for the added labels under (weighted) label exchangeability

CAT-Seg (vitl_bank683), 2000 ADE validation images with a labelled sampled pixel (845-name vocabulary: 150 source names, then the A-847 annotation mapped to the added names), 500 trials (random half/half image split; source vocabulary as per design). Label loss = pooled fraction of the label's sampled pixels whose score for it is below the threshold. "Added, cal" = mean over added labels present in the calibration images (the quantity the proposition bounds); "added, held-out" = same on the held-out images; "src, class" = class-averaged source loss on held-out images; "src, image" = image-level source risk (the paper's guarantee); size = labels per labelled pixel at 845 names, held-out images; floor = % of added labels present whose threshold is the grid floor. Risks in % (and % of trials above alpha). Development data; nothing fitted.

## alpha = 0.1, exchangeable

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 845 | Floor | Source / added labels present (cal) |
|---|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 9.50 (40) | 9.55 (40) | 9.49 (41) | 3.28 (0) | 27.55 | 0.0 | 113 / 523 |
| anchored, image-level (paper) | 23.18 (100) | 23.21 (99) | 23.15 (100) | 9.89 (44) | 7.70 | 0.0 | 113 / 523 |
| anchored, both | 9.50 (40) | 9.55 (40) | 9.49 (41) | 3.28 (0) | 27.55 | 0.0 | 113 / 523 |
| native, full known, label-level | 9.49 (40) | 9.54 (37) | 9.47 (39) | 2.93 (0) | 34.17 | 0.0 | 113 / 523 |
| anchored, weighted, all3 | 9.44 (40) | 9.48 (37) | 9.44 (40) | 3.27 (0) | 27.69 | 0.0 | 113 / 523 |
| native, full known, weighted, all3 | 9.47 (40) | 9.51 (38) | 9.49 (41) | 2.96 (0) | 34.06 | 0.0 | 113 / 523 |
| anchored, stratified, all3 | 8.28 (21) | 8.31 (22) | 8.27 (22) | 5.37 (4) | 35.93 | 0.0 | 113 / 523 |
| anchored, weighted, all5 | 9.41 (40) | 9.45 (37) | 9.44 (40) | 3.27 (0) | 27.80 | 0.0 | 113 / 523 |
| native, full known, weighted, all5 | 9.44 (40) | 9.46 (37) | 9.46 (40) | 2.95 (0) | 34.29 | 0.0 | 113 / 523 |
| anchored, stratified, all5 | 7.08 (10) | 7.12 (10) | 6.98 (9) | 4.92 (2) | 51.41 | 0.0 | 113 / 523 |

## alpha = 0.05, exchangeable

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 845 | Floor | Source / added labels present (cal) |
|---|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 4.48 (36) | 4.51 (37) | 4.44 (37) | 1.20 (0) | 76.39 | 0.0 | 113 / 523 |
| anchored, image-level (paper) | 13.97 (100) | 13.99 (99) | 13.94 (99) | 4.90 (42) | 17.30 | 0.0 | 113 / 523 |
| anchored, both | 4.48 (36) | 4.51 (37) | 4.44 (37) | 1.20 (0) | 76.39 | 0.0 | 113 / 523 |
| native, full known, label-level | 4.05 (36) | 4.09 (37) | 3.88 (35) | 0.90 (0) | 260.11 | 0.0 | 113 / 523 |
| anchored, weighted, all3 | 4.45 (35) | 4.48 (36) | 4.47 (38) | 1.20 (0) | 76.76 | 0.0 | 113 / 523 |
| native, full known, weighted, all3 | 4.04 (37) | 4.08 (38) | 3.93 (37) | 0.92 (0) | 257.68 | 0.0 | 113 / 523 |
| anchored, stratified, all3 | 3.22 (12) | 3.22 (11) | 3.07 (12) | 1.95 (1) | 112.53 | 0.0 | 113 / 523 |
| anchored, weighted, all5 | 4.42 (36) | 4.44 (37) | 4.43 (36) | 1.20 (0) | 77.62 | 0.0 | 113 / 523 |
| native, full known, weighted, all5 | 3.99 (35) | 4.01 (36) | 3.90 (35) | 0.92 (0) | 265.37 | 0.0 | 113 / 523 |
| anchored, stratified, all5 | 1.79 (0) | 1.79 (0) | 1.58 (1) | 1.21 (0) | 284.41 | 17.2 | 113 / 523 |

## alpha = 0.1, dataset split

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 845 | Floor | Source / added labels present (cal) |
|---|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 22.20 (100) | 22.25 (100) | 9.42 (25) | 4.91 (0) | 9.00 | 0.0 | 149 / 486 |
| anchored, image-level (paper) | 34.15 (100) | 34.15 (100) | 16.67 (100) | 9.89 (39) | 4.48 | 0.0 | 149 / 486 |
| anchored, both | 22.20 (100) | 22.25 (100) | 9.42 (25) | 4.91 (0) | 9.00 | 0.0 | 149 / 486 |
| native, full known, label-level | 22.65 (100) | 22.68 (100) | 9.43 (24) | 3.95 (0) | 10.14 | 0.0 | 149 / 486 |
| native, frozen at source, label-level | 33.80 (100) | 33.83 (100) | 15.64 (100) | 7.24 (0) | 5.11 | 0.0 | 149 / 486 |
| native, frozen at source, image-level | 54.05 (100) | 54.04 (100) | 30.30 (100) | 15.23 (100) | 2.20 | 0.0 | 149 / 486 |
| anchored, weighted, all3 | 9.55 (38) | 9.63 (41) | 3.35 (0) | 1.52 (0) | 27.44 | 0.0 | 149 / 486 |
| native, full known, weighted, all3 | 10.81 (79) | 10.87 (82) | 3.52 (0) | 1.41 (0) | 30.31 | 0.0 | 149 / 486 |
| anchored, stratified, all3 | 6.63 (0) | 6.69 (0) | 8.40 (4) | 5.62 (0) | 293.77 | 37.7 | 149 / 486 |
| anchored, weighted, all5 | 10.13 (58) | 10.24 (63) | 3.47 (0) | 1.62 (0) | 25.59 | 0.0 | 149 / 486 |
| native, full known, weighted, all5 | 6.89 (0) | 6.97 (0) | 3.62 (0) | 1.49 (0) | 194.92 | 20.1 | 149 / 486 |
| anchored, stratified, all5 | 4.73 (0) | 4.77 (0) | 7.45 (0) | 6.01 (0) | 353.52 | 45.5 | 149 / 486 |

## alpha = 0.05, dataset split

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 845 | Floor | Source / added labels present (cal) |
|---|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 13.11 (100) | 13.19 (100) | 4.35 (14) | 2.09 (0) | 20.65 | 0.0 | 149 / 486 |
| anchored, image-level (paper) | 22.15 (100) | 22.20 (100) | 9.38 (100) | 4.89 (42) | 9.03 | 0.0 | 149 / 486 |
| anchored, both | 13.11 (100) | 13.19 (100) | 4.35 (14) | 2.09 (0) | 20.65 | 0.0 | 149 / 486 |
| native, full known, label-level | 12.98 (100) | 13.05 (100) | 4.38 (14) | 1.73 (0) | 24.24 | 0.0 | 149 / 486 |
| native, frozen at source, label-level | 21.43 (100) | 21.46 (100) | 8.77 (100) | 3.64 (0) | 11.11 | 0.0 | 149 / 486 |
| native, frozen at source, image-level | 37.22 (100) | 37.24 (100) | 17.74 (100) | 8.38 (100) | 4.31 | 0.0 | 149 / 486 |
| anchored, weighted, all3 | 1.90 (0) | 1.89 (0) | 1.45 (0) | 0.59 (0) | 322.35 | 37.7 | 149 / 486 |
| native, full known, weighted, all3 | 5.34 (66) | 5.36 (67) | 1.35 (0) | 0.50 (0) | 108.26 | 0.0 | 149 / 486 |
| anchored, stratified, all3 | 3.18 (0) | 3.19 (0) | 3.57 (1) | 2.22 (0) | 314.33 | 37.7 | 149 / 486 |
| anchored, weighted, all5 | 4.43 (21) | 4.46 (24) | 1.39 (0) | 0.59 (0) | 62.49 | 0.0 | 149 / 486 |
| native, full known, weighted, all5 | 3.19 (0) | 3.20 (0) | 1.45 (0) | 0.57 (0) | 240.84 | 20.1 | 149 / 486 |
| anchored, stratified, all5 | 1.66 (0) | 1.66 (0) | 2.94 (0) | 2.31 (0) | 523.75 | 68.8 | 149 / 486 |

## alpha = 0.1, exchangeable, native frozen

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 845 | Floor | Source / added labels present (cal) |
|---|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 9.08 (35) | 9.14 (37) | 9.49 (41) | 2.87 (0) | 28.85 | 0.0 | 114 / 522 |
| anchored, image-level (paper) | 23.65 (100) | 23.61 (100) | 23.99 (100) | 9.99 (48) | 6.79 | 0.0 | 114 / 522 |
| anchored, both | 9.08 (35) | 9.14 (37) | 9.49 (41) | 2.87 (0) | 28.85 | 0.0 | 114 / 522 |
| native, full known, label-level | 9.20 (38) | 9.24 (37) | 9.39 (39) | 2.66 (0) | 35.80 | 0.0 | 114 / 522 |
| native, frozen at source, label-level | 20.76 (100) | 20.74 (100) | 21.48 (100) | 7.50 (20) | 9.67 | 0.0 | 114 / 522 |
| native, frozen at source, image-level | 47.61 (100) | 47.56 (100) | 47.61 (100) | 22.29 (100) | 2.34 | 0.0 | 114 / 522 |
| anchored, weighted, all3 | 9.03 (35) | 9.08 (37) | 9.44 (40) | 2.87 (0) | 29.21 | 0.0 | 114 / 522 |
| native, full known, weighted, all3 | 9.16 (38) | 9.21 (38) | 9.35 (40) | 2.65 (0) | 36.09 | 0.0 | 114 / 522 |
| anchored, stratified, all3 | 8.31 (26) | 8.37 (26) | 8.17 (20) | 5.73 (4) | 34.03 | 0.0 | 114 / 522 |
| anchored, weighted, all5 | 9.17 (38) | 9.23 (40) | 9.63 (44) | 2.93 (0) | 28.64 | 0.0 | 114 / 522 |
| native, full known, weighted, all5 | 9.25 (39) | 9.29 (40) | 9.46 (40) | 2.71 (0) | 36.29 | 0.0 | 114 / 522 |
| anchored, stratified, all5 | 7.21 (15) | 7.29 (15) | 6.87 (8) | 4.68 (1) | 50.06 | 0.0 | 114 / 522 |

## alpha = 0.05, exchangeable, native frozen

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 845 | Floor | Source / added labels present (cal) |
|---|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 4.51 (38) | 4.55 (37) | 4.30 (35) | 1.15 (0) | 74.52 | 0.0 | 114 / 522 |
| anchored, image-level (paper) | 14.29 (100) | 14.32 (100) | 14.78 (100) | 4.97 (47) | 14.98 | 0.0 | 114 / 522 |
| anchored, both | 4.51 (38) | 4.55 (37) | 4.30 (35) | 1.15 (0) | 74.52 | 0.0 | 114 / 522 |
| native, full known, label-level | 4.30 (39) | 4.30 (37) | 3.96 (33) | 0.92 (0) | 228.11 | 0.0 | 114 / 522 |
| native, frozen at source, label-level | 11.78 (100) | 11.80 (100) | 12.13 (100) | 3.64 (19) | 24.34 | 0.0 | 114 / 522 |
| native, frozen at source, image-level | 31.90 (100) | 31.82 (100) | 32.53 (100) | 12.95 (100) | 4.79 | 0.0 | 114 / 522 |
| anchored, weighted, all3 | 4.53 (39) | 4.56 (37) | 4.32 (36) | 1.15 (0) | 75.13 | 0.0 | 114 / 522 |
| native, full known, weighted, all3 | 4.16 (39) | 4.16 (37) | 3.81 (34) | 0.91 (0) | 251.33 | 0.0 | 114 / 522 |
| anchored, stratified, all3 | 3.11 (15) | 3.16 (15) | 2.97 (8) | 1.84 (1) | 121.24 | 0.0 | 114 / 522 |
| anchored, weighted, all5 | 4.59 (39) | 4.63 (38) | 4.44 (37) | 1.17 (0) | 73.96 | 0.0 | 114 / 522 |
| native, full known, weighted, all5 | 4.27 (41) | 4.28 (40) | 3.91 (37) | 0.95 (0) | 248.79 | 0.0 | 114 / 522 |
| anchored, stratified, all5 | 1.75 (0) | 1.77 (1) | 1.58 (1) | 1.06 (0) | 279.57 | 16.0 | 114 / 522 |
