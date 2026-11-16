# A guarantee for the added labels under (weighted) label exchangeability

CAT-Seg (vitl_bank683), 2000 Pascal Context validation images with a labelled sampled pixel (458-name vocabulary: 59 source names, then the PC-459 annotation mapped to the added names), 500 trials (random half/half image split; source vocabulary as per design). Label loss = pooled fraction of the label's sampled pixels whose score for it is below the threshold. "Added, cal" = mean over added labels present in the calibration images (the quantity the proposition bounds); "added, held-out" = same on the held-out images; "src, class" = class-averaged source loss on held-out images; "src, image" = image-level source risk (the paper's guarantee); size = labels per labelled pixel at 458 names, held-out images; floor = % of added labels present whose threshold is the grid floor. Risks in % (and % of trials above alpha). Development data; nothing fitted.

## alpha = 0.1, exchangeable

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 458 | Floor | Source / added labels present (cal) |
|---|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 7.55 (23) | 7.51 (25) | 7.42 (25) | 4.24 (6) | 11.54 | 0.0 | 29 / 195 |
| anchored, image-level (paper) | 16.68 (86) | 16.69 (85) | 16.61 (81) | 9.92 (45) | 3.73 | 0.0 | 29 / 195 |
| anchored, both | 7.43 (23) | 7.40 (24) | 7.31 (25) | 4.10 (4) | 11.68 | 0.0 | 29 / 195 |
| native, full known, label-level | 7.61 (23) | 7.58 (24) | 7.35 (25) | 3.51 (3) | 14.92 | 0.0 | 29 / 195 |
| anchored, weighted, all2 | 7.51 (23) | 7.45 (25) | 7.43 (25) | 4.23 (7) | 12.00 | 0.0 | 29 / 195 |
| native, full known, weighted, all2 | 7.56 (24) | 7.52 (24) | 7.41 (25) | 3.51 (3) | 14.60 | 0.0 | 29 / 195 |
| anchored, stratified, all2 | 5.23 (5) | 5.22 (7) | 5.05 (9) | 3.88 (5) | 127.58 | 13.2 | 29 / 195 |
| anchored, weighted, all3 | 7.48 (24) | 7.45 (25) | 7.52 (26) | 4.26 (7) | 12.61 | 0.0 | 29 / 195 |
| native, full known, weighted, all3 | 7.43 (23) | 7.38 (23) | 7.37 (25) | 3.48 (4) | 15.82 | 0.0 | 29 / 195 |
| anchored, stratified, all3 | 3.36 (0) | 3.37 (1) | 3.17 (1) | 3.35 (2) | 216.65 | 25.7 | 29 / 195 |
| anchored, weighted, all5 | 7.32 (23) | 7.30 (23) | 7.53 (27) | 4.25 (7) | 15.14 | 0.3 | 29 / 195 |
| native, full known, weighted, all5 | 7.39 (22) | 7.34 (21) | 7.50 (25) | 3.61 (4) | 18.07 | 0.4 | 29 / 195 |
| anchored, stratified, all5 | 0.74 (0) | 0.73 (0) | 0.85 (0) | 1.32 (0) | 373.11 | 67.7 | 29 / 195 |
| anchored, weighted, src2 | 7.45 (23) | 7.39 (25) | 7.39 (25) | 4.26 (7) | 12.43 | 0.0 | 29 / 195 |
| native, full known, weighted, src2 | 7.51 (23) | 7.47 (24) | 7.36 (25) | 3.52 (3) | 14.63 | 0.0 | 29 / 195 |
| anchored, stratified, src2 | 5.16 (6) | 5.16 (6) | 4.89 (8) | 3.98 (5) | 134.63 | 13.6 | 29 / 195 |
| anchored, weighted, src3 | 7.36 (24) | 7.32 (24) | 7.38 (24) | 4.24 (7) | 12.55 | 0.0 | 29 / 195 |
| native, full known, weighted, src3 | 7.33 (22) | 7.30 (22) | 7.27 (25) | 3.48 (3) | 16.30 | 0.0 | 29 / 195 |
| anchored, stratified, src3 | 3.50 (1) | 3.54 (1) | 3.31 (2) | 3.57 (2) | 208.07 | 23.0 | 29 / 195 |
| anchored, weighted, src5 | 7.23 (23) | 7.19 (24) | 7.34 (25) | 4.21 (6) | 13.87 | 0.1 | 29 / 195 |
| native, full known, weighted, src5 | 7.19 (21) | 7.13 (22) | 7.24 (25) | 3.49 (4) | 16.83 | 0.0 | 29 / 195 |
| anchored, stratified, src5 | 0.60 (0) | 0.60 (0) | 0.59 (0) | 1.13 (0) | 376.05 | 65.6 | 29 / 195 |

## alpha = 0.05, exchangeable

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 458 | Floor | Source / added labels present (cal) |
|---|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 2.76 (16) | 2.74 (16) | 2.65 (18) | 1.03 (2) | 68.36 | 0.6 | 29 / 195 |
| anchored, image-level (paper) | 9.82 (90) | 9.84 (90) | 9.54 (81) | 4.90 (44) | 7.14 | 0.0 | 29 / 195 |
| anchored, both | 2.75 (16) | 2.74 (16) | 2.64 (18) | 1.02 (2) | 68.40 | 0.6 | 29 / 195 |
| native, full known, label-level | 2.74 (16) | 2.72 (17) | 2.67 (18) | 0.89 (1) | 92.77 | 0.6 | 29 / 195 |
| anchored, weighted, all2 | 2.70 (15) | 2.68 (16) | 2.70 (19) | 1.03 (2) | 75.03 | 2.1 | 29 / 195 |
| native, full known, weighted, all2 | 2.65 (15) | 2.63 (16) | 2.68 (18) | 0.88 (1) | 96.81 | 1.9 | 29 / 195 |
| anchored, stratified, all2 | 0.63 (0) | 0.65 (0) | 0.70 (2) | 0.31 (0) | 346.04 | 58.2 | 29 / 195 |
| anchored, weighted, all3 | 2.61 (14) | 2.56 (13) | 2.74 (19) | 1.03 (2) | 87.59 | 5.4 | 29 / 195 |
| native, full known, weighted, all3 | 2.57 (13) | 2.53 (14) | 2.68 (19) | 0.88 (1) | 112.18 | 5.1 | 29 / 195 |
| anchored, stratified, all3 | 0.04 (0) | 0.04 (0) | 0.04 (0) | 0.04 (0) | 448.01 | 95.4 | 29 / 195 |
| anchored, weighted, all5 | 2.47 (11) | 2.41 (12) | 2.76 (19) | 1.04 (2) | 115.49 | 12.7 | 29 / 195 |
| native, full known, weighted, all5 | 2.44 (11) | 2.41 (12) | 2.76 (19) | 0.96 (2) | 133.09 | 12.4 | 29 / 195 |
| anchored, stratified, all5 | 0.00 (0) | 0.00 (0) | 0.00 (0) | 0.00 (0) | 457.90 | 99.9 | 29 / 195 |
| anchored, weighted, src2 | 2.65 (14) | 2.63 (15) | 2.62 (18) | 1.05 (2) | 76.88 | 2.3 | 29 / 195 |
| native, full known, weighted, src2 | 2.66 (15) | 2.62 (15) | 2.67 (19) | 0.91 (1) | 95.49 | 1.1 | 29 / 195 |
| anchored, stratified, src2 | 0.66 (0) | 0.68 (0) | 0.65 (1) | 0.34 (0) | 328.36 | 49.6 | 29 / 195 |
| anchored, weighted, src3 | 2.60 (14) | 2.55 (14) | 2.67 (18) | 1.05 (2) | 85.01 | 3.9 | 29 / 195 |
| native, full known, weighted, src3 | 2.47 (11) | 2.46 (12) | 2.61 (18) | 0.89 (2) | 112.46 | 4.4 | 29 / 195 |
| anchored, stratified, src3 | 0.00 (0) | 0.00 (0) | 0.00 (0) | 0.00 (0) | 456.17 | 98.8 | 29 / 195 |
| anchored, weighted, src5 | 2.40 (11) | 2.35 (9) | 2.62 (18) | 1.05 (2) | 108.14 | 9.5 | 29 / 195 |
| native, full known, weighted, src5 | 2.28 (10) | 2.26 (11) | 2.52 (16) | 0.90 (2) | 133.31 | 10.0 | 29 / 195 |
| anchored, stratified, src5 | 0.00 (0) | 0.00 (0) | 0.00 (0) | 0.00 (0) | 458.00 | 100.0 | 29 / 195 |

## alpha = 0.1, dataset split

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 458 | Floor | Source / added labels present (cal) |
|---|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 22.30 (100) | 22.29 (100) | 8.48 (7) | 8.40 (1) | 2.73 | 0.0 | 59 / 165 |
| anchored, image-level (paper) | 24.66 (100) | 24.64 (100) | 9.85 (39) | 9.88 (44) | 2.45 | 0.0 | 59 / 165 |
| anchored, both | 22.30 (100) | 22.29 (100) | 8.48 (7) | 8.40 (1) | 2.73 | 0.0 | 59 / 165 |
| native, full known, label-level | 26.53 (100) | 26.52 (100) | 8.48 (9) | 7.55 (0) | 2.59 | 0.0 | 59 / 165 |
| native, frozen at source, label-level | 39.89 (100) | 39.86 (100) | 15.82 (100) | 13.80 (100) | 1.62 | 0.0 | 59 / 165 |
| native, frozen at source, image-level | 42.84 (100) | 42.84 (100) | 17.45 (100) | 15.06 (100) | 1.51 | 0.0 | 59 / 165 |
| anchored, weighted, all2 | 8.10 (4) | 8.12 (3) | 4.32 (0) | 4.67 (0) | 232.60 | 40.5 | 59 / 165 |
| native, full known, weighted, all2 | 12.28 (87) | 12.29 (88) | 8.38 (19) | 7.60 (3) | 231.41 | 35.0 | 59 / 165 |
| anchored, stratified, all2 | 11.79 (94) | 11.72 (94) | 7.96 (1) | 8.72 (6) | 231.45 | 40.5 | 59 / 165 |
| anchored, weighted, all3 | 4.24 (0) | 4.26 (0) | 4.25 (0) | 4.69 (0) | 309.33 | 64.6 | 59 / 165 |
| native, full known, weighted, all3 | 8.09 (3) | 8.04 (3) | 10.62 (71) | 9.67 (40) | 307.97 | 62.2 | 59 / 165 |
| anchored, stratified, all3 | 6.26 (0) | 6.24 (0) | 7.80 (0) | 8.71 (6) | 308.32 | 64.6 | 59 / 165 |
| anchored, weighted, all5 | 4.77 (0) | 4.80 (0) | 3.61 (0) | 3.93 (0) | 278.94 | 54.9 | 59 / 165 |
| native, full known, weighted, all5 | 1.78 (0) | 1.75 (0) | 4.42 (0) | 4.54 (0) | 369.61 | 84.7 | 59 / 165 |
| anchored, stratified, all5 | 2.29 (0) | 2.27 (0) | 7.00 (0) | 7.65 (0) | 368.91 | 85.1 | 59 / 165 |
| anchored, weighted, src2 | 16.80 (100) | 16.83 (100) | 6.06 (0) | 6.72 (0) | 3.51 | 0.0 | 59 / 165 |
| native, full known, weighted, src2 | 19.89 (100) | 19.88 (100) | 5.84 (0) | 6.21 (0) | 3.49 | 0.0 | 59 / 165 |
| anchored, stratified, src2 | 16.78 (100) | 16.81 (100) | 6.97 (0) | 8.40 (1) | 3.36 | 0.0 | 59 / 165 |
| anchored, weighted, src3 | 13.28 (99) | 13.27 (99) | 4.87 (0) | 5.50 (0) | 4.30 | 0.0 | 59 / 165 |
| native, full known, weighted, src3 | 16.18 (100) | 16.18 (100) | 5.18 (0) | 5.69 (0) | 4.19 | 0.0 | 59 / 165 |
| anchored, stratified, src3 | 13.12 (98) | 13.12 (98) | 5.50 (0) | 6.33 (0) | 4.22 | 0.0 | 59 / 165 |
| anchored, weighted, src5 | 10.39 (60) | 10.32 (59) | 4.33 (0) | 4.81 (0) | 5.47 | 0.0 | 59 / 165 |
| native, full known, weighted, src5 | 9.73 (43) | 9.62 (42) | 4.33 (0) | 4.86 (0) | 8.20 | 0.0 | 59 / 165 |
| anchored, stratified, src5 | 8.25 (8) | 8.18 (10) | 2.50 (0) | 2.65 (0) | 8.01 | 0.0 | 59 / 165 |

## alpha = 0.05, dataset split

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 458 | Floor | Source / added labels present (cal) |
|---|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 12.58 (100) | 12.56 (100) | 3.42 (1) | 3.38 (0) | 4.99 | 0.0 | 59 / 165 |
| anchored, image-level (paper) | 15.97 (100) | 15.99 (100) | 4.86 (39) | 4.89 (40) | 3.89 | 0.0 | 59 / 165 |
| anchored, both | 12.58 (100) | 12.56 (100) | 3.42 (1) | 3.38 (0) | 4.99 | 0.0 | 59 / 165 |
| native, full known, label-level | 15.56 (100) | 15.55 (100) | 3.46 (1) | 3.12 (0) | 4.93 | 0.0 | 59 / 165 |
| native, frozen at source, label-level | 24.41 (100) | 24.41 (100) | 7.28 (100) | 6.52 (99) | 2.87 | 0.0 | 59 / 165 |
| native, frozen at source, image-level | 28.53 (100) | 28.48 (100) | 9.60 (100) | 8.56 (100) | 2.37 | 0.0 | 59 / 165 |
| anchored, weighted, all2 | 5.88 (82) | 5.92 (83) | 2.51 (0) | 2.56 (0) | 234.24 | 40.5 | 59 / 165 |
| native, full known, weighted, all2 | 7.26 (95) | 7.29 (94) | 3.69 (11) | 3.40 (5) | 233.07 | 35.0 | 59 / 165 |
| anchored, stratified, all2 | 6.65 (95) | 6.68 (97) | 3.17 (0) | 3.33 (0) | 233.45 | 40.5 | 59 / 165 |
| anchored, weighted, all3 | 2.90 (0) | 2.94 (0) | 2.64 (0) | 2.75 (0) | 310.53 | 64.6 | 59 / 165 |
| native, full known, weighted, all3 | 4.73 (42) | 4.73 (39) | 4.50 (31) | 4.17 (21) | 309.36 | 62.2 | 59 / 165 |
| anchored, stratified, all3 | 3.24 (0) | 3.29 (1) | 3.09 (0) | 3.30 (0) | 310.09 | 64.6 | 59 / 165 |
| anchored, weighted, all5 | 2.14 (0) | 2.15 (0) | 2.36 (0) | 2.50 (0) | 283.06 | 54.9 | 59 / 165 |
| native, full known, weighted, all5 | 0.92 (0) | 0.92 (0) | 2.11 (0) | 2.17 (0) | 370.92 | 84.7 | 59 / 165 |
| anchored, stratified, all5 | 0.86 (0) | 0.88 (0) | 2.67 (0) | 2.95 (0) | 370.33 | 85.1 | 59 / 165 |
| anchored, weighted, src2 | 7.51 (98) | 7.42 (96) | 2.33 (0) | 3.18 (0) | 9.21 | 0.0 | 59 / 165 |
| native, full known, weighted, src2 | 8.48 (99) | 8.39 (99) | 2.03 (0) | 2.85 (0) | 10.39 | 0.0 | 59 / 165 |
| anchored, stratified, src2 | 7.48 (98) | 7.39 (96) | 1.85 (0) | 2.23 (0) | 9.53 | 0.0 | 59 / 165 |
| anchored, weighted, src3 | 1.83 (0) | 1.79 (0) | 1.93 (0) | 2.88 (0) | 55.52 | 0.0 | 59 / 165 |
| native, full known, weighted, src3 | 0.89 (0) | 0.91 (0) | 1.84 (0) | 2.72 (0) | 184.78 | 0.0 | 59 / 165 |
| anchored, stratified, src3 | 0.52 (0) | 0.50 (0) | 0.19 (0) | 0.31 (0) | 145.30 | 0.0 | 59 / 165 |
| anchored, weighted, src5 | 0.77 (0) | 0.80 (0) | 2.46 (0) | 2.92 (0) | 379.25 | 87.6 | 59 / 165 |
| native, full known, weighted, src5 | 0.56 (0) | 0.57 (0) | 2.06 (0) | 2.51 (0) | 399.13 | 94.6 | 59 / 165 |
| anchored, stratified, src5 | 0.00 (0) | 0.00 (0) | 0.00 (0) | 0.00 (0) | 458.00 | 100.0 | 59 / 165 |
