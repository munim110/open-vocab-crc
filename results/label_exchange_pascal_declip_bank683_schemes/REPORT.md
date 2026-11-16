# A guarantee for the added labels under (weighted) label exchangeability

CAT-Seg (declip_bank683), 2000 Pascal Context validation images with a labelled sampled pixel (458-name vocabulary: 59 source names, then the PC-459 annotation mapped to the added names), 500 trials (random half/half image split; source vocabulary as per design). Label loss = pooled fraction of the label's sampled pixels whose score for it is below the threshold. "Added, cal" = mean over added labels present in the calibration images (the quantity the proposition bounds); "added, held-out" = same on the held-out images; "src, class" = class-averaged source loss on held-out images; "src, image" = image-level source risk (the paper's guarantee); size = labels per labelled pixel at 458 names, held-out images; floor = % of added labels present whose threshold is the grid floor. Risks in % (and % of trials above alpha). Development data; nothing fitted.

## alpha = 0.1, exchangeable

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 458 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 7.50 (25) | 7.46 (25) | 7.37 (25) | 4.93 (11) | 10.41 | 0.0 | 29 / 195 | 6.75 | 0.75 | 5.75 |
| anchored, image-level (paper) | 15.22 (79) | 15.19 (78) | 14.91 (73) | 9.90 (45) | 3.47 | 0.0 | 29 / 195 | 14.57 | 0.65 | 5.75 |
| anchored, both | 7.29 (23) | 7.25 (21) | 7.15 (22) | 4.65 (7) | 10.59 | 0.0 | 29 / 195 | 6.59 | 0.70 | 5.75 |
| native, full known, label-level | 7.56 (27) | 7.57 (27) | 7.38 (24) | 3.95 (6) | 17.62 | 0.0 | 29 / 195 | 6.69 | 0.86 | 6.22 |
| anchored, weighted, all2 | 7.48 (24) | 7.43 (24) | 7.40 (24) | 4.92 (11) | 10.55 | 0.0 | 29 / 195 | 6.78 | 0.70 | nan |
| native, full known, weighted, all2 | 7.54 (27) | 7.55 (27) | 7.46 (25) | 3.96 (6) | 15.76 | 0.0 | 29 / 195 | 6.79 | 0.75 | nan |
| anchored, stratified, all2 | 5.24 (6) | 5.20 (6) | 4.97 (7) | 4.74 (8) | 140.30 | 15.1 | 29 / 195 | 4.01 | 1.23 | nan |
| anchored, weighted, all3 | 7.46 (24) | 7.42 (24) | 7.49 (26) | 4.94 (11) | 10.73 | 0.0 | 29 / 195 | 6.84 | 0.61 | nan |
| native, full known, weighted, all3 | 7.50 (26) | 7.50 (26) | 7.50 (25) | 3.98 (7) | 17.50 | 0.0 | 29 / 195 | 6.80 | 0.70 | nan |
| anchored, stratified, all3 | 3.19 (0) | 3.18 (0) | 2.93 (1) | 4.26 (4) | 224.94 | 29.1 | 29 / 195 | 2.30 | 0.89 | nan |
| anchored, weighted, all5 | 7.27 (23) | 7.24 (23) | 7.49 (25) | 4.87 (12) | 13.81 | 0.4 | 29 / 195 | 6.85 | 0.43 | nan |
| native, full known, weighted, all5 | 7.35 (24) | 7.36 (26) | 7.50 (26) | 3.96 (6) | 19.85 | 0.2 | 29 / 195 | 6.82 | 0.53 | nan |
| anchored, stratified, all5 | 0.78 (0) | 0.78 (0) | 0.91 (0) | 1.43 (0) | 371.15 | 67.4 | 29 / 195 | 0.58 | 0.20 | nan |
| anchored, weighted, src2 | 7.37 (24) | 7.34 (23) | 7.29 (23) | 4.92 (11) | 10.83 | 0.0 | 29 / 195 | 6.67 | 0.70 | nan |
| native, full known, weighted, src2 | 7.49 (26) | 7.48 (26) | 7.38 (25) | 3.96 (6) | 14.94 | 0.0 | 29 / 195 | 6.68 | 0.81 | nan |
| anchored, stratified, src2 | 5.16 (6) | 5.14 (5) | 4.91 (7) | 4.84 (8) | 136.40 | 14.4 | 29 / 195 | 4.05 | 1.11 | nan |
| anchored, weighted, src3 | 7.46 (25) | 7.41 (25) | 7.45 (25) | 5.01 (12) | 10.73 | 0.0 | 29 / 195 | 6.84 | 0.62 | nan |
| native, full known, weighted, src3 | 7.38 (25) | 7.35 (25) | 7.33 (25) | 3.96 (6) | 19.00 | 0.0 | 29 / 195 | 6.64 | 0.73 | nan |
| anchored, stratified, src3 | 3.40 (0) | 3.40 (0) | 3.08 (1) | 4.60 (6) | 210.57 | 25.1 | 29 / 195 | 2.39 | 1.01 | nan |
| anchored, weighted, src5 | 7.12 (22) | 7.08 (23) | 7.23 (24) | 4.83 (11) | 12.97 | 0.0 | 29 / 195 | 6.57 | 0.55 | nan |
| native, full known, weighted, src5 | 7.18 (23) | 7.17 (24) | 7.22 (24) | 3.92 (6) | 20.01 | 0.0 | 29 / 195 | 6.60 | 0.58 | nan |
| anchored, stratified, src5 | 0.67 (0) | 0.65 (0) | 0.60 (0) | 1.33 (0) | 371.76 | 64.4 | 29 / 195 | 0.41 | 0.26 | nan |

## alpha = 0.05, exchangeable

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 458 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 2.79 (19) | 2.77 (19) | 2.55 (16) | 1.17 (2) | 62.44 | 0.6 | 29 / 195 | 1.57 | 1.22 | 5.75 |
| anchored, image-level (paper) | 8.97 (87) | 8.91 (88) | 8.73 (75) | 4.94 (45) | 6.82 | 0.0 | 29 / 195 | 8.65 | 0.32 | 5.75 |
| anchored, both | 2.77 (18) | 2.75 (18) | 2.53 (16) | 1.14 (2) | 62.49 | 0.6 | 29 / 195 | 1.56 | 1.21 | 5.75 |
| native, full known, label-level | 2.82 (20) | 2.82 (21) | 2.62 (18) | 1.02 (2) | 131.98 | 0.6 | 29 / 195 | 1.28 | 1.54 | 6.22 |
| anchored, weighted, all2 | 2.73 (17) | 2.70 (16) | 2.59 (17) | 1.15 (2) | 66.76 | 1.7 | 29 / 195 | 1.62 | 1.11 | nan |
| native, full known, weighted, all2 | 2.70 (19) | 2.71 (18) | 2.67 (20) | 1.01 (2) | 139.38 | 1.9 | 29 / 195 | 1.37 | 1.34 | nan |
| anchored, stratified, all2 | 0.75 (0) | 0.74 (0) | 0.66 (1) | 0.42 (0) | 331.05 | 52.0 | 29 / 195 | 0.29 | 0.46 | nan |
| anchored, weighted, all3 | 2.63 (15) | 2.61 (15) | 2.62 (17) | 1.19 (3) | 82.77 | 6.0 | 29 / 195 | 1.71 | 0.92 | nan |
| native, full known, weighted, all3 | 2.62 (18) | 2.62 (18) | 2.64 (18) | 1.01 (2) | 151.30 | 5.5 | 29 / 195 | 1.45 | 1.18 | nan |
| anchored, stratified, all3 | 0.03 (0) | 0.03 (0) | 0.04 (0) | 0.05 (0) | 447.49 | 94.9 | 29 / 195 | 0.02 | 0.01 | nan |
| anchored, weighted, all5 | 2.48 (13) | 2.45 (13) | 2.61 (18) | 1.23 (3) | 106.64 | 12.2 | 29 / 195 | 1.79 | 0.70 | nan |
| native, full known, weighted, all5 | 2.46 (15) | 2.47 (14) | 2.65 (18) | 1.03 (2) | 172.94 | 12.0 | 29 / 195 | 1.52 | 0.94 | nan |
| anchored, stratified, all5 | 0.00 (0) | 0.00 (0) | 0.00 (0) | 0.00 (0) | 458.00 | 100.0 | 29 / 195 | 0.00 | 0.00 | nan |
| anchored, weighted, src2 | 2.68 (17) | 2.64 (17) | 2.55 (16) | 1.19 (2) | 68.54 | 1.8 | 29 / 195 | 1.59 | 1.09 | nan |
| native, full known, weighted, src2 | 2.68 (19) | 2.69 (19) | 2.63 (19) | 1.03 (2) | 139.48 | 1.4 | 29 / 195 | 1.34 | 1.34 | nan |
| anchored, stratified, src2 | 0.68 (0) | 0.67 (0) | 0.61 (1) | 0.43 (0) | 321.46 | 48.4 | 29 / 195 | 0.25 | 0.42 | nan |
| anchored, weighted, src3 | 2.66 (16) | 2.63 (17) | 2.63 (17) | 1.20 (3) | 77.77 | 3.4 | 29 / 195 | 1.67 | 0.99 | nan |
| native, full known, weighted, src3 | 2.58 (18) | 2.56 (18) | 2.59 (18) | 1.01 (2) | 150.75 | 3.1 | 29 / 195 | 1.36 | 1.22 | nan |
| anchored, stratified, src3 | 0.00 (0) | 0.00 (0) | 0.00 (0) | 0.00 (0) | 456.90 | 99.2 | 29 / 195 | 0.00 | 0.00 | nan |
| anchored, weighted, src5 | 2.37 (12) | 2.33 (11) | 2.49 (16) | 1.18 (3) | 103.68 | 9.4 | 29 / 195 | 1.58 | 0.79 | nan |
| native, full known, weighted, src5 | 2.30 (11) | 2.31 (12) | 2.55 (18) | 1.04 (3) | 178.37 | 10.5 | 29 / 195 | 1.45 | 0.85 | nan |
| anchored, stratified, src5 | 0.00 (0) | 0.00 (0) | 0.00 (0) | 0.00 (0) | 458.00 | 100.0 | 29 / 195 | 0.00 | 0.00 | nan |

## alpha = 0.1, dataset split

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 458 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 18.08 (100) | 18.10 (100) | 8.51 (5) | 9.10 (11) | 2.72 | 0.0 | 59 / 165 | 8.44 | 9.65 | 24.93 |
| anchored, image-level (paper) | 19.15 (100) | 19.15 (100) | 9.23 (15) | 9.88 (44) | 2.57 | 0.0 | 59 / 165 | 9.18 | 9.96 | 24.93 |
| anchored, both | 18.07 (100) | 18.09 (100) | 8.51 (5) | 9.09 (11) | 2.72 | 0.0 | 59 / 165 | 8.43 | 9.64 | 24.93 |
| native, full known, label-level | 22.86 (100) | 22.79 (100) | 8.48 (10) | 7.93 (1) | 2.57 | 0.0 | 59 / 165 | 8.45 | 14.41 | 33.48 |
| native, frozen at source, label-level | 35.76 (100) | 35.68 (100) | 15.41 (100) | 14.18 (100) | 1.58 | 0.0 | 59 / 165 | 8.43 | 27.32 | 41.71 |
| native, frozen at source, image-level | 36.89 (100) | 36.84 (100) | 15.97 (100) | 14.71 (100) | 1.53 | 0.0 | 59 / 165 | 8.95 | 27.94 | 41.71 |
| anchored, weighted, all2 | 6.61 (0) | 6.56 (0) | 3.94 (0) | 4.92 (0) | 232.62 | 38.8 | 59 / 165 | 3.91 | 2.70 | nan |
| native, full known, weighted, all2 | 11.15 (83) | 11.14 (83) | 8.48 (10) | 7.93 (1) | 231.40 | 33.5 | 59 / 165 | 8.45 | 2.71 | nan |
| anchored, stratified, all2 | 9.91 (43) | 9.80 (42) | 8.00 (2) | 9.45 (24) | 231.41 | 38.8 | 59 / 165 | 7.93 | 1.98 | nan |
| anchored, weighted, all3 | 3.09 (0) | 3.07 (0) | 4.33 (0) | 5.35 (0) | 309.16 | 64.4 | 59 / 165 | 4.31 | -1.21 | nan |
| native, full known, weighted, all3 | 11.22 (78) | 11.19 (76) | 17.47 (99) | 16.06 (99) | 307.38 | 60.7 | 59 / 165 | 17.50 | -6.28 | nan |
| anchored, stratified, all3 | 4.83 (0) | 4.80 (0) | 8.00 (2) | 9.45 (24) | 308.27 | 64.4 | 59 / 165 | 7.93 | -3.10 | nan |
| anchored, weighted, all5 | 3.62 (0) | 3.60 (0) | 4.30 (0) | 5.38 (0) | 278.39 | 54.1 | 59 / 165 | 4.25 | -0.62 | nan |
| native, full known, weighted, all5 | 5.04 (0) | 5.04 (0) | 6.49 (1) | 6.97 (1) | 278.25 | 47.8 | 59 / 165 | 6.47 | -1.43 | nan |
| anchored, stratified, all5 | 2.58 (0) | 2.54 (0) | 6.85 (0) | 8.30 (1) | 368.91 | 84.3 | 59 / 165 | 6.75 | -4.18 | nan |
| anchored, weighted, src2 | 14.00 (100) | 14.00 (100) | 6.00 (0) | 7.18 (0) | 3.45 | 0.0 | 59 / 165 | 5.94 | 8.06 | nan |
| native, full known, weighted, src2 | 17.41 (100) | 17.43 (100) | 6.04 (0) | 6.77 (0) | 3.37 | 0.0 | 59 / 165 | 5.97 | 11.44 | nan |
| anchored, stratified, src2 | 13.95 (100) | 13.95 (100) | 6.99 (0) | 9.02 (9) | 3.28 | 0.0 | 59 / 165 | 6.91 | 7.04 | nan |
| anchored, weighted, src3 | 12.05 (94) | 12.01 (93) | 5.56 (0) | 6.75 (0) | 3.90 | 0.0 | 59 / 165 | 5.49 | 6.57 | nan |
| native, full known, weighted, src3 | 14.21 (100) | 14.24 (100) | 4.84 (0) | 5.79 (0) | 4.15 | 0.0 | 59 / 165 | 4.75 | 9.46 | nan |
| anchored, stratified, src3 | 11.85 (92) | 11.81 (90) | 5.52 (0) | 6.88 (0) | 3.96 | 0.0 | 59 / 165 | 5.39 | 6.46 | nan |
| anchored, weighted, src5 | 9.21 (22) | 9.13 (22) | 4.56 (0) | 5.70 (0) | 5.10 | 0.0 | 59 / 165 | 4.50 | 4.71 | nan |
| native, full known, weighted, src5 | 9.42 (33) | 9.38 (32) | 4.18 (0) | 5.19 (0) | 6.14 | 0.0 | 59 / 165 | 4.10 | 5.32 | nan |
| anchored, stratified, src5 | 7.51 (1) | 7.44 (2) | 2.46 (0) | 3.01 (0) | 7.16 | 0.0 | 59 / 165 | 2.36 | 5.16 | nan |

## alpha = 0.05, dataset split

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 458 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 11.05 (100) | 11.02 (100) | 3.41 (0) | 4.02 (1) | 4.72 | 0.0 | 59 / 165 | 3.37 | 7.68 | 24.93 |
| anchored, image-level (paper) | 12.45 (100) | 12.42 (100) | 4.25 (6) | 4.90 (42) | 4.11 | 0.0 | 59 / 165 | 4.22 | 8.23 | 24.93 |
| anchored, both | 11.05 (100) | 11.02 (100) | 3.41 (0) | 4.02 (1) | 4.72 | 0.0 | 59 / 165 | 3.37 | 7.68 | 24.93 |
| native, full known, label-level | 13.79 (100) | 13.81 (100) | 3.42 (0) | 3.58 (0) | 4.73 | 0.0 | 59 / 165 | 3.37 | 10.41 | 33.48 |
| native, frozen at source, label-level | 21.95 (100) | 21.89 (100) | 7.98 (100) | 7.48 (100) | 2.69 | 0.0 | 59 / 165 | 3.37 | 18.57 | 41.71 |
| native, frozen at source, image-level | 23.97 (100) | 23.91 (100) | 9.04 (100) | 8.48 (100) | 2.43 | 0.0 | 59 / 165 | 3.98 | 19.98 | 41.71 |
| anchored, weighted, all2 | 4.26 (13) | 4.21 (15) | 1.92 (0) | 2.57 (0) | 234.58 | 38.8 | 59 / 165 | 1.90 | 2.36 | nan |
| native, full known, weighted, all2 | 6.33 (94) | 6.34 (94) | 3.42 (0) | 3.58 (0) | 233.07 | 33.5 | 59 / 165 | 3.37 | 2.95 | nan |
| anchored, stratified, all2 | 5.84 (85) | 5.79 (82) | 3.17 (0) | 4.04 (2) | 233.09 | 38.8 | 59 / 165 | 3.12 | 2.72 | nan |
| anchored, weighted, all3 | 1.82 (0) | 1.80 (0) | 2.16 (0) | 2.86 (0) | 310.63 | 64.4 | 59 / 165 | 2.14 | -0.32 | nan |
| native, full known, weighted, all3 | 6.62 (94) | 6.57 (93) | 8.87 (100) | 8.34 (100) | 308.24 | 60.7 | 59 / 165 | 8.85 | -2.23 | nan |
| anchored, stratified, all3 | 2.47 (0) | 2.44 (0) | 3.17 (0) | 4.04 (2) | 309.72 | 64.4 | 59 / 165 | 3.12 | -0.65 | nan |
| anchored, weighted, all5 | 2.08 (0) | 2.09 (0) | 2.18 (0) | 2.93 (0) | 280.62 | 54.1 | 59 / 165 | 2.15 | -0.07 | nan |
| native, full known, weighted, all5 | 0.98 (0) | 0.96 (0) | 3.48 (0) | 4.04 (3) | 369.77 | 83.4 | 59 / 165 | 3.47 | -2.49 | nan |
| anchored, stratified, all5 | 1.30 (0) | 1.31 (0) | 2.59 (0) | 3.53 (0) | 370.16 | 84.3 | 59 / 165 | 2.53 | -1.23 | nan |
| anchored, weighted, src2 | 7.11 (98) | 7.04 (97) | 2.32 (0) | 3.68 (0) | 7.70 | 0.0 | 59 / 165 | 2.28 | 4.83 | nan |
| native, full known, weighted, src2 | 8.27 (100) | 8.21 (100) | 2.25 (0) | 3.56 (0) | 7.88 | 0.0 | 59 / 165 | 2.22 | 6.06 | nan |
| anchored, stratified, src2 | 7.06 (97) | 6.98 (96) | 1.81 (0) | 2.63 (0) | 8.06 | 0.0 | 59 / 165 | 1.77 | 5.29 | nan |
| anchored, weighted, src3 | 1.59 (0) | 1.53 (1) | 2.15 (0) | 3.54 (0) | 90.92 | 0.0 | 59 / 165 | 2.08 | -0.48 | nan |
| native, full known, weighted, src3 | 1.89 (0) | 1.86 (0) | 1.82 (0) | 3.16 (0) | 125.77 | 0.0 | 59 / 165 | 1.74 | 0.15 | nan |
| anchored, stratified, src3 | 0.16 (0) | 0.15 (0) | 0.21 (0) | 0.36 (0) | 247.93 | 0.0 | 59 / 165 | 0.17 | -0.01 | nan |
| anchored, weighted, src5 | 1.12 (0) | 1.13 (0) | 2.35 (0) | 3.34 (0) | 374.32 | 85.7 | 59 / 165 | 2.31 | -1.19 | nan |
| native, full known, weighted, src5 | 0.24 (0) | 0.23 (0) | 2.28 (0) | 3.13 (0) | 396.92 | 93.5 | 59 / 165 | 2.23 | -1.99 | nan |
| anchored, stratified, src5 | 0.00 (0) | 0.00 (0) | 0.00 (0) | 0.00 (0) | 458.00 | 100.0 | 59 / 165 | 0.00 | 0.00 | nan |
