# A guarantee for the added labels under (weighted) label exchangeability

CAT-Seg (sed_bank683), 2000 Pascal Context validation images with a labelled sampled pixel (458-name vocabulary: 59 source names, then the PC-459 annotation mapped to the added names), 500 trials (random half/half image split; source vocabulary as per design). Label loss = pooled fraction of the label's sampled pixels whose score for it is below the threshold. "Added, cal" = mean over added labels present in the calibration images (the quantity the proposition bounds); "added, held-out" = same on the held-out images; "src, class" = class-averaged source loss on held-out images; "src, image" = image-level source risk (the paper's guarantee); size = labels per labelled pixel at 458 names, held-out images; floor = % of added labels present whose threshold is the grid floor. Risks in % (and % of trials above alpha). Development data; nothing fitted.

## alpha = 0.1, exchangeable

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 458 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 7.53 (25) | 7.48 (27) | 7.28 (24) | 4.27 (7) | 17.48 | 0.0 | 29 / 195 | 6.74 | 0.79 | 5.85 |
| anchored, image-level (paper) | 17.56 (86) | 17.55 (86) | 17.29 (82) | 9.96 (45) | 5.87 | 0.0 | 29 / 195 | 17.19 | 0.37 | 5.85 |
| anchored, both | 7.40 (24) | 7.34 (25) | 7.16 (22) | 4.11 (5) | 17.76 | 0.0 | 29 / 195 | 6.63 | 0.77 | 5.85 |
| native, full known, label-level | 7.64 (26) | 7.59 (28) | 7.32 (23) | 3.72 (5) | 20.15 | 0.0 | 29 / 195 | 6.73 | 0.90 | 6.03 |
| anchored, weighted, all2 | 7.49 (23) | 7.43 (26) | 7.33 (24) | 4.27 (7) | 17.69 | 0.0 | 29 / 195 | 6.75 | 0.74 | nan |
| native, full known, weighted, all2 | 7.59 (25) | 7.54 (26) | 7.39 (23) | 3.75 (5) | 20.55 | 0.0 | 29 / 195 | 6.80 | 0.80 | nan |
| anchored, stratified, all2 | 5.00 (6) | 4.94 (5) | 4.67 (6) | 4.19 (7) | 140.90 | 13.5 | 29 / 195 | 3.95 | 1.05 | nan |
| anchored, weighted, all3 | 7.47 (23) | 7.44 (26) | 7.39 (25) | 4.32 (7) | 18.31 | 0.0 | 29 / 195 | 6.85 | 0.62 | nan |
| native, full known, weighted, all3 | 7.59 (24) | 7.57 (27) | 7.47 (25) | 3.77 (6) | 20.34 | 0.0 | 29 / 195 | 6.85 | 0.74 | nan |
| anchored, stratified, all3 | 3.56 (0) | 3.52 (0) | 3.22 (2) | 3.31 (3) | 220.58 | 24.3 | 29 / 195 | 2.38 | 1.18 | nan |
| anchored, weighted, all5 | 7.38 (23) | 7.32 (23) | 7.40 (24) | 4.29 (7) | 20.64 | 0.4 | 29 / 195 | 6.87 | 0.50 | nan |
| native, full known, weighted, all5 | 7.50 (24) | 7.47 (24) | 7.49 (24) | 3.80 (5) | 23.51 | 0.4 | 29 / 195 | 6.88 | 0.62 | nan |
| anchored, stratified, all5 | 0.86 (0) | 0.88 (0) | 0.85 (0) | 1.25 (0) | 382.44 | 70.2 | 29 / 195 | 0.52 | 0.34 | nan |
| anchored, weighted, src2 | 7.42 (24) | 7.36 (25) | 7.28 (24) | 4.28 (7) | 18.06 | 0.0 | 29 / 195 | 6.70 | 0.72 | nan |
| native, full known, weighted, src2 | 7.51 (24) | 7.46 (26) | 7.32 (23) | 3.74 (5) | 20.61 | 0.0 | 29 / 195 | 6.72 | 0.79 | nan |
| anchored, stratified, src2 | 5.00 (7) | 4.97 (6) | 4.74 (6) | 4.31 (7) | 147.27 | 14.1 | 29 / 195 | 4.03 | 0.97 | nan |
| anchored, weighted, src3 | 7.33 (22) | 7.28 (25) | 7.17 (24) | 4.26 (7) | 18.38 | 0.0 | 29 / 195 | 6.63 | 0.70 | nan |
| native, full known, weighted, src3 | 7.43 (22) | 7.39 (26) | 7.25 (23) | 3.73 (4) | 21.08 | 0.0 | 29 / 195 | 6.63 | 0.80 | nan |
| anchored, stratified, src3 | 3.70 (0) | 3.68 (0) | 3.40 (2) | 3.66 (3) | 203.97 | 19.9 | 29 / 195 | 2.41 | 1.29 | nan |
| anchored, weighted, src5 | 7.29 (23) | 7.23 (24) | 7.27 (24) | 4.29 (7) | 19.86 | 0.0 | 29 / 195 | 6.73 | 0.55 | nan |
| native, full known, weighted, src5 | 7.35 (24) | 7.32 (24) | 7.30 (24) | 3.78 (6) | 22.41 | 0.0 | 29 / 195 | 6.69 | 0.66 | nan |
| anchored, stratified, src5 | 0.64 (0) | 0.65 (0) | 0.46 (0) | 0.99 (0) | 386.96 | 67.1 | 29 / 195 | 0.30 | 0.34 | nan |

## alpha = 0.05, exchangeable

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 458 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 2.82 (17) | 2.80 (19) | 2.49 (16) | 1.18 (3) | 80.37 | 0.6 | 29 / 195 | 1.57 | 1.25 | 5.85 |
| anchored, image-level (paper) | 10.15 (89) | 10.17 (88) | 9.97 (81) | 4.97 (47) | 11.78 | 0.0 | 29 / 195 | 9.79 | 0.36 | 5.85 |
| anchored, both | 2.79 (17) | 2.78 (19) | 2.47 (15) | 1.15 (2) | 80.48 | 0.6 | 29 / 195 | 1.56 | 1.23 | 5.85 |
| native, full known, label-level | 2.79 (18) | 2.74 (17) | 2.50 (15) | 1.04 (3) | 86.88 | 0.6 | 29 / 195 | 1.54 | 1.25 | 6.03 |
| anchored, weighted, all2 | 2.73 (16) | 2.72 (17) | 2.50 (15) | 1.17 (2) | 86.81 | 2.1 | 29 / 195 | 1.61 | 1.12 | nan |
| native, full known, weighted, all2 | 2.73 (16) | 2.69 (16) | 2.56 (17) | 1.06 (2) | 91.96 | 2.2 | 29 / 195 | 1.60 | 1.13 | nan |
| anchored, stratified, all2 | 0.74 (0) | 0.77 (0) | 0.67 (2) | 0.50 (0) | 351.81 | 57.0 | 29 / 195 | 0.27 | 0.47 | nan |
| anchored, weighted, all3 | 2.66 (15) | 2.61 (15) | 2.54 (16) | 1.18 (3) | 99.75 | 5.8 | 29 / 195 | 1.72 | 0.94 | nan |
| native, full known, weighted, all3 | 2.60 (14) | 2.57 (13) | 2.55 (16) | 1.05 (3) | 105.94 | 5.7 | 29 / 195 | 1.69 | 0.91 | nan |
| anchored, stratified, all3 | 0.05 (0) | 0.06 (0) | 0.03 (0) | 0.05 (0) | 448.52 | 95.4 | 29 / 195 | 0.02 | 0.04 | nan |
| anchored, weighted, all5 | 2.54 (14) | 2.48 (13) | 2.56 (16) | 1.20 (2) | 120.70 | 12.0 | 29 / 195 | 1.80 | 0.75 | nan |
| native, full known, weighted, all5 | 2.48 (13) | 2.42 (11) | 2.54 (17) | 1.10 (3) | 129.78 | 12.8 | 29 / 195 | 1.84 | 0.64 | nan |
| anchored, stratified, all5 | 0.00 (0) | 0.00 (0) | 0.00 (0) | 0.00 (0) | 458.00 | 100.0 | 29 / 195 | 0.00 | 0.00 | nan |
| anchored, weighted, src2 | 2.70 (16) | 2.68 (17) | 2.46 (16) | 1.18 (2) | 88.21 | 1.9 | 29 / 195 | 1.58 | 1.11 | nan |
| native, full known, weighted, src2 | 2.67 (16) | 2.63 (16) | 2.51 (16) | 1.05 (3) | 93.28 | 1.7 | 29 / 195 | 1.55 | 1.12 | nan |
| anchored, stratified, src2 | 0.73 (0) | 0.77 (0) | 0.63 (1) | 0.53 (0) | 340.74 | 50.6 | 29 / 195 | 0.24 | 0.49 | nan |
| anchored, weighted, src3 | 2.63 (15) | 2.60 (15) | 2.49 (14) | 1.20 (2) | 91.87 | 3.4 | 29 / 195 | 1.61 | 1.02 | nan |
| native, full known, weighted, src3 | 2.57 (14) | 2.51 (12) | 2.49 (15) | 1.07 (2) | 101.43 | 3.7 | 29 / 195 | 1.58 | 0.99 | nan |
| anchored, stratified, src3 | 0.00 (0) | 0.00 (0) | 0.00 (0) | 0.00 (0) | 457.49 | 99.4 | 29 / 195 | 0.00 | 0.00 | nan |
| anchored, weighted, src5 | 2.45 (14) | 2.43 (12) | 2.48 (14) | 1.20 (3) | 120.46 | 9.9 | 29 / 195 | 1.72 | 0.73 | nan |
| native, full known, weighted, src5 | 2.43 (14) | 2.38 (12) | 2.49 (16) | 1.09 (3) | 127.88 | 10.4 | 29 / 195 | 1.68 | 0.75 | nan |
| anchored, stratified, src5 | 0.00 (0) | 0.00 (0) | 0.00 (0) | 0.00 (0) | 458.00 | 100.0 | 29 / 195 | 0.00 | 0.00 | nan |

## alpha = 0.1, dataset split

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 458 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 26.22 (100) | 26.22 (100) | 8.46 (8) | 7.67 (0) | 3.55 | 0.0 | 59 / 165 | 8.44 | 17.78 | 30.86 |
| anchored, image-level (paper) | 31.31 (100) | 31.47 (100) | 10.89 (84) | 9.87 (43) | 2.89 | 0.0 | 59 / 165 | 10.89 | 20.42 | 30.86 |
| anchored, both | 26.22 (100) | 26.22 (100) | 8.46 (8) | 7.67 (0) | 3.55 | 0.0 | 59 / 165 | 8.44 | 17.78 | 30.86 |
| native, full known, label-level | 29.75 (100) | 29.71 (100) | 8.48 (9) | 6.73 (0) | 3.70 | 0.0 | 59 / 165 | 8.44 | 21.31 | 40.26 |
| native, frozen at source, label-level | 20.56 (100) | 20.45 (100) | 4.73 (0) | 3.89 (0) | 5.57 | 0.0 | 59 / 165 | 8.44 | 12.12 | 17.24 |
| native, frozen at source, image-level | 23.20 (100) | 23.09 (100) | 5.67 (0) | 4.66 (0) | 4.87 | 0.0 | 59 / 165 | 9.99 | 13.21 | 17.24 |
| anchored, weighted, all2 | 11.36 (81) | 11.42 (83) | 7.56 (2) | 7.16 (1) | 232.67 | 41.1 | 59 / 165 | 7.58 | 3.78 | nan |
| native, full known, weighted, all2 | 19.48 (99) | 19.61 (98) | 14.54 (96) | 12.16 (90) | 231.37 | 40.9 | 59 / 165 | 14.53 | 4.95 | nan |
| anchored, stratified, all2 | 11.87 (95) | 11.93 (94) | 8.13 (5) | 7.68 (0) | 232.43 | 41.1 | 59 / 165 | 8.10 | 3.76 | nan |
| anchored, weighted, all3 | 4.36 (0) | 4.36 (0) | 3.67 (0) | 3.64 (0) | 311.03 | 67.0 | 59 / 165 | 3.66 | 0.70 | nan |
| native, full known, weighted, all3 | 11.47 (88) | 11.48 (86) | 15.17 (96) | 12.75 (93) | 308.21 | 65.7 | 59 / 165 | 15.17 | -3.70 | nan |
| anchored, stratified, all3 | 6.73 (0) | 6.76 (0) | 7.96 (4) | 7.89 (1) | 308.98 | 67.0 | 59 / 165 | 7.93 | -1.21 | nan |
| anchored, weighted, all5 | 4.79 (0) | 4.77 (0) | 3.07 (0) | 3.27 (0) | 281.17 | 56.7 | 59 / 165 | 3.04 | 1.75 | nan |
| native, full known, weighted, all5 | 5.96 (0) | 6.00 (0) | 5.66 (1) | 5.16 (0) | 280.36 | 54.1 | 59 / 165 | 5.59 | 0.37 | nan |
| anchored, stratified, all5 | 2.90 (0) | 2.91 (0) | 7.02 (0) | 8.60 (2) | 369.43 | 86.2 | 59 / 165 | 6.92 | -4.02 | nan |
| anchored, weighted, src2 | 19.41 (100) | 19.38 (100) | 6.07 (0) | 6.47 (0) | 4.80 | 0.0 | 59 / 165 | 6.02 | 13.39 | nan |
| native, full known, weighted, src2 | 21.66 (100) | 21.54 (100) | 5.82 (0) | 5.56 (0) | 4.90 | 0.0 | 59 / 165 | 5.78 | 15.88 | nan |
| anchored, stratified, src2 | 19.29 (100) | 19.25 (100) | 6.97 (0) | 8.51 (2) | 4.58 | 0.0 | 59 / 165 | 6.92 | 12.37 | nan |
| anchored, weighted, src3 | 16.04 (100) | 16.01 (100) | 5.14 (0) | 5.64 (0) | 5.82 | 0.0 | 59 / 165 | 5.05 | 10.99 | nan |
| native, full known, weighted, src3 | 16.98 (100) | 16.91 (100) | 4.98 (0) | 4.84 (0) | 6.31 | 0.0 | 59 / 165 | 4.92 | 12.06 | nan |
| anchored, stratified, src3 | 15.92 (100) | 15.90 (100) | 5.54 (0) | 5.88 (0) | 5.77 | 0.0 | 59 / 165 | 5.40 | 10.52 | nan |
| anchored, weighted, src5 | 11.22 (82) | 11.20 (81) | 3.21 (0) | 3.92 (0) | 8.41 | 0.0 | 59 / 165 | 3.15 | 8.07 | nan |
| native, full known, weighted, src5 | 10.75 (66) | 10.77 (60) | 3.22 (0) | 3.44 (0) | 10.81 | 0.0 | 59 / 165 | 3.10 | 7.65 | nan |
| anchored, stratified, src5 | 9.43 (31) | 9.41 (33) | 2.47 (0) | 3.13 (0) | 10.72 | 0.0 | 59 / 165 | 2.36 | 7.07 | nan |

## alpha = 0.05, dataset split

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 458 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 15.46 (100) | 15.43 (100) | 3.43 (1) | 3.20 (0) | 6.71 | 0.0 | 59 / 165 | 3.37 | 12.09 | 30.86 |
| anchored, image-level (paper) | 19.95 (100) | 19.92 (100) | 5.42 (74) | 4.89 (40) | 4.94 | 0.0 | 59 / 165 | 5.43 | 14.52 | 30.86 |
| anchored, both | 15.46 (100) | 15.43 (100) | 3.43 (1) | 3.20 (0) | 6.71 | 0.0 | 59 / 165 | 3.37 | 12.09 | 30.86 |
| native, full known, label-level | 17.12 (100) | 17.04 (100) | 3.39 (1) | 2.84 (0) | 6.99 | 0.0 | 59 / 165 | 3.38 | 13.75 | 40.26 |
| native, frozen at source, label-level | 12.36 (100) | 12.34 (100) | 1.85 (0) | 1.48 (0) | 10.84 | 0.0 | 59 / 165 | 3.37 | 8.99 | 17.24 |
| native, frozen at source, image-level | 14.59 (100) | 14.52 (100) | 2.51 (0) | 2.07 (0) | 8.61 | 0.0 | 59 / 165 | 4.78 | 9.81 | 17.24 |
| anchored, weighted, all2 | 7.87 (98) | 7.88 (97) | 4.11 (26) | 3.92 (21) | 234.78 | 41.1 | 59 / 165 | 4.10 | 3.77 | nan |
| native, full known, weighted, all2 | 9.83 (93) | 9.89 (93) | 6.05 (65) | 4.93 (53) | 234.54 | 40.9 | 59 / 165 | 6.06 | 3.77 | nan |
| anchored, stratified, all2 | 6.92 (99) | 6.93 (99) | 3.25 (0) | 3.15 (0) | 235.35 | 41.1 | 59 / 165 | 3.20 | 3.72 | nan |
| anchored, weighted, all3 | 3.20 (1) | 3.17 (1) | 2.03 (0) | 2.14 (0) | 312.84 | 67.0 | 59 / 165 | 2.02 | 1.18 | nan |
| native, full known, weighted, all3 | 5.78 (67) | 5.81 (70) | 6.57 (70) | 5.34 (61) | 310.96 | 65.7 | 59 / 165 | 6.58 | -0.81 | nan |
| anchored, stratified, all3 | 4.05 (6) | 4.04 (10) | 3.17 (1) | 3.17 (0) | 311.42 | 67.0 | 59 / 165 | 3.12 | 0.93 | nan |
| anchored, weighted, all5 | 2.85 (0) | 2.80 (0) | 1.59 (0) | 1.91 (0) | 285.79 | 56.7 | 59 / 165 | 1.57 | 1.28 | nan |
| native, full known, weighted, all5 | 1.71 (0) | 1.71 (0) | 1.67 (0) | 1.94 (0) | 372.53 | 86.7 | 59 / 165 | 1.64 | 0.07 | nan |
| anchored, stratified, all5 | 1.80 (0) | 1.79 (0) | 2.66 (0) | 3.32 (0) | 371.24 | 86.2 | 59 / 165 | 2.62 | -0.81 | nan |
| anchored, weighted, src2 | 9.88 (100) | 9.85 (100) | 2.15 (0) | 3.05 (0) | 10.74 | 0.0 | 59 / 165 | 2.12 | 7.76 | nan |
| native, full known, weighted, src2 | 10.30 (100) | 10.29 (100) | 2.11 (0) | 2.63 (0) | 12.05 | 0.0 | 59 / 165 | 2.03 | 8.27 | nan |
| anchored, stratified, src2 | 9.73 (100) | 9.70 (100) | 1.82 (0) | 2.42 (0) | 11.19 | 0.0 | 59 / 165 | 1.77 | 7.96 | nan |
| anchored, weighted, src3 | 1.81 (0) | 1.76 (0) | 1.81 (0) | 2.81 (0) | 68.95 | 0.0 | 59 / 165 | 1.77 | 0.04 | nan |
| native, full known, weighted, src3 | 2.56 (1) | 2.46 (0) | 1.52 (0) | 2.20 (0) | 68.76 | 0.0 | 59 / 165 | 1.48 | 1.08 | nan |
| anchored, stratified, src3 | 0.09 (0) | 0.08 (0) | 0.19 (0) | 0.35 (0) | 327.83 | 0.0 | 59 / 165 | 0.17 | -0.08 | nan |
| anchored, weighted, src5 | 1.39 (0) | 1.37 (0) | 1.54 (0) | 2.24 (0) | 375.19 | 86.8 | 59 / 165 | 1.51 | -0.12 | nan |
| native, full known, weighted, src5 | 1.10 (0) | 1.08 (0) | 1.28 (0) | 1.67 (0) | 384.65 | 91.0 | 59 / 165 | 1.26 | -0.16 | nan |
| anchored, stratified, src5 | 0.00 (0) | 0.00 (0) | 0.00 (0) | 0.00 (0) | 458.00 | 100.0 | 59 / 165 | 0.00 | 0.00 | nan |
