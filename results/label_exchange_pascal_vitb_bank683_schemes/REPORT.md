# A guarantee for the added labels under (weighted) label exchangeability

CAT-Seg (vitb_bank683), 2000 Pascal Context validation images with a labelled sampled pixel (458-name vocabulary: 59 source names, then the PC-459 annotation mapped to the added names), 500 trials (random half/half image split; source vocabulary as per design). Label loss = pooled fraction of the label's sampled pixels whose score for it is below the threshold. "Added, cal" = mean over added labels present in the calibration images (the quantity the proposition bounds); "added, held-out" = same on the held-out images; "src, class" = class-averaged source loss on held-out images; "src, image" = image-level source risk (the paper's guarantee); size = labels per labelled pixel at 458 names, held-out images; floor = % of added labels present whose threshold is the grid floor. Risks in % (and % of trials above alpha). Development data; nothing fitted.

## alpha = 0.1, exchangeable

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 458 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 7.47 (25) | 7.48 (26) | 7.33 (26) | 3.57 (5) | 23.90 | 0.0 | 29 / 195 | 6.75 | 0.73 | 5.77 |
| anchored, image-level (paper) | 19.77 (92) | 19.65 (91) | 19.35 (89) | 10.05 (50) | 5.99 | 0.0 | 29 / 195 | 19.18 | 0.59 | 5.77 |
| anchored, both | 7.39 (25) | 7.40 (26) | 7.25 (25) | 3.47 (4) | 24.19 | 0.0 | 29 / 195 | 6.68 | 0.71 | 5.77 |
| native, full known, label-level | 7.57 (27) | 7.53 (27) | 7.38 (26) | 3.03 (3) | 32.12 | 0.0 | 29 / 195 | 6.70 | 0.88 | 5.98 |
| anchored, weighted, all2 | 7.42 (25) | 7.41 (25) | 7.35 (26) | 3.57 (4) | 23.60 | 0.0 | 29 / 195 | 6.79 | 0.63 | nan |
| native, full known, weighted, all2 | 7.56 (25) | 7.50 (25) | 7.48 (26) | 3.06 (3) | 30.38 | 0.0 | 29 / 195 | 6.84 | 0.72 | nan |
| anchored, stratified, all2 | 5.11 (5) | 5.17 (6) | 4.89 (9) | 3.55 (5) | 129.48 | 11.5 | 29 / 195 | 3.84 | 1.27 | nan |
| anchored, weighted, all3 | 7.44 (24) | 7.44 (25) | 7.49 (26) | 3.64 (5) | 24.90 | 0.0 | 29 / 195 | 6.89 | 0.55 | nan |
| native, full known, weighted, all3 | 7.49 (26) | 7.46 (25) | 7.46 (26) | 3.07 (3) | 32.40 | 0.0 | 29 / 195 | 6.80 | 0.69 | nan |
| anchored, stratified, all3 | 3.31 (1) | 3.36 (1) | 3.20 (1) | 3.05 (3) | 231.90 | 26.6 | 29 / 195 | 2.25 | 1.06 | nan |
| anchored, weighted, all5 | 7.26 (24) | 7.27 (25) | 7.51 (28) | 3.59 (4) | 27.75 | 0.4 | 29 / 195 | 6.83 | 0.43 | nan |
| native, full known, weighted, all5 | 7.28 (24) | 7.24 (25) | 7.45 (26) | 3.06 (3) | 37.38 | 0.1 | 29 / 195 | 6.81 | 0.47 | nan |
| anchored, stratified, all5 | 0.66 (0) | 0.68 (0) | 0.82 (0) | 1.09 (0) | 385.48 | 71.0 | 29 / 195 | 0.51 | 0.16 | nan |
| anchored, weighted, src2 | 7.28 (23) | 7.27 (25) | 7.23 (25) | 3.55 (4) | 24.57 | 0.0 | 29 / 195 | 6.70 | 0.58 | nan |
| native, full known, weighted, src2 | 7.41 (23) | 7.35 (24) | 7.33 (25) | 3.01 (3) | 32.60 | 0.0 | 29 / 195 | 6.66 | 0.75 | nan |
| anchored, stratified, src2 | 4.96 (5) | 5.04 (6) | 4.86 (7) | 3.63 (5) | 141.19 | 13.2 | 29 / 195 | 3.93 | 1.03 | nan |
| anchored, weighted, src3 | 7.26 (24) | 7.26 (24) | 7.28 (25) | 3.59 (5) | 25.32 | 0.0 | 29 / 195 | 6.68 | 0.57 | nan |
| native, full known, weighted, src3 | 7.28 (24) | 7.26 (24) | 7.29 (25) | 3.03 (3) | 34.94 | 0.0 | 29 / 195 | 6.64 | 0.64 | nan |
| anchored, stratified, src3 | 3.39 (0) | 3.46 (1) | 3.33 (2) | 3.28 (2) | 228.79 | 26.2 | 29 / 195 | 2.25 | 1.14 | nan |
| anchored, weighted, src5 | 7.16 (23) | 7.16 (24) | 7.34 (26) | 3.60 (4) | 26.23 | 0.1 | 29 / 195 | 6.75 | 0.41 | nan |
| native, full known, weighted, src5 | 7.17 (24) | 7.10 (24) | 7.29 (25) | 3.05 (2) | 35.36 | 0.0 | 29 / 195 | 6.61 | 0.57 | nan |
| anchored, stratified, src5 | 0.51 (0) | 0.53 (0) | 0.55 (0) | 0.97 (0) | 385.25 | 67.4 | 29 / 195 | 0.32 | 0.19 | nan |

## alpha = 0.05, exchangeable

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 458 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 2.61 (14) | 2.60 (15) | 2.37 (14) | 0.91 (1) | 98.41 | 0.6 | 29 / 195 | 1.58 | 1.04 | 5.77 |
| anchored, image-level (paper) | 11.78 (92) | 11.78 (92) | 11.41 (89) | 5.00 (48) | 12.59 | 0.0 | 29 / 195 | 11.54 | 0.24 | 5.77 |
| anchored, both | 2.60 (14) | 2.59 (15) | 2.36 (14) | 0.90 (1) | 98.47 | 0.6 | 29 / 195 | 1.57 | 1.03 | 5.77 |
| native, full known, label-level | 2.49 (13) | 2.51 (13) | 2.14 (13) | 0.77 (1) | 160.67 | 0.6 | 29 / 195 | 1.24 | 1.25 | 5.98 |
| anchored, weighted, all2 | 2.54 (12) | 2.53 (13) | 2.38 (16) | 0.91 (2) | 104.79 | 2.2 | 29 / 195 | 1.66 | 0.88 | nan |
| native, full known, weighted, all2 | 2.41 (11) | 2.42 (11) | 2.19 (14) | 0.76 (1) | 164.95 | 1.8 | 29 / 195 | 1.34 | 1.08 | nan |
| anchored, stratified, all2 | 0.50 (0) | 0.53 (0) | 0.51 (1) | 0.29 (0) | 357.13 | 60.7 | 29 / 195 | 0.22 | 0.28 | nan |
| anchored, weighted, all3 | 2.48 (13) | 2.47 (13) | 2.44 (15) | 0.95 (2) | 117.63 | 6.2 | 29 / 195 | 1.78 | 0.70 | nan |
| native, full known, weighted, all3 | 2.35 (11) | 2.39 (12) | 2.26 (15) | 0.81 (1) | 175.46 | 6.1 | 29 / 195 | 1.46 | 0.88 | nan |
| anchored, stratified, all3 | 0.03 (0) | 0.03 (0) | 0.04 (0) | 0.03 (0) | 449.13 | 95.7 | 29 / 195 | 0.02 | 0.01 | nan |
| anchored, weighted, all5 | 2.35 (10) | 2.36 (10) | 2.45 (16) | 0.95 (2) | 136.44 | 11.6 | 29 / 195 | 1.82 | 0.53 | nan |
| native, full known, weighted, all5 | 2.26 (10) | 2.28 (10) | 2.36 (16) | 0.86 (2) | 188.67 | 11.8 | 29 / 195 | 1.54 | 0.72 | nan |
| anchored, stratified, all5 | 0.00 (0) | 0.00 (0) | 0.00 (0) | 0.00 (0) | 458.00 | 100.0 | 29 / 195 | 0.00 | 0.00 | nan |
| anchored, weighted, src2 | 2.49 (12) | 2.49 (13) | 2.34 (15) | 0.90 (1) | 105.30 | 1.9 | 29 / 195 | 1.61 | 0.88 | nan |
| native, full known, weighted, src2 | 2.39 (11) | 2.40 (11) | 2.15 (14) | 0.76 (1) | 165.39 | 1.5 | 29 / 195 | 1.29 | 1.10 | nan |
| anchored, stratified, src2 | 0.49 (0) | 0.51 (0) | 0.51 (1) | 0.30 (0) | 345.78 | 54.2 | 29 / 195 | 0.20 | 0.29 | nan |
| anchored, weighted, src3 | 2.40 (12) | 2.40 (12) | 2.33 (15) | 0.92 (2) | 114.96 | 4.3 | 29 / 195 | 1.62 | 0.78 | nan |
| native, full known, weighted, src3 | 2.29 (11) | 2.31 (11) | 2.11 (12) | 0.79 (2) | 176.53 | 4.3 | 29 / 195 | 1.34 | 0.94 | nan |
| anchored, stratified, src3 | 0.00 (0) | 0.00 (0) | 0.00 (0) | 0.00 (0) | 456.98 | 99.3 | 29 / 195 | 0.00 | 0.00 | nan |
| anchored, weighted, src5 | 2.26 (8) | 2.27 (10) | 2.39 (14) | 0.93 (2) | 137.77 | 10.6 | 29 / 195 | 1.73 | 0.52 | nan |
| native, full known, weighted, src5 | 2.15 (8) | 2.19 (10) | 2.24 (14) | 0.81 (1) | 189.47 | 8.8 | 29 / 195 | 1.44 | 0.72 | nan |
| anchored, stratified, src5 | 0.00 (0) | 0.00 (0) | 0.00 (0) | 0.00 (0) | 458.00 | 100.0 | 29 / 195 | 0.00 | 0.00 | nan |

## alpha = 0.1, dataset split

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 458 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 27.44 (100) | 27.38 (100) | 8.48 (6) | 7.58 (0) | 3.66 | 0.0 | 59 / 165 | 8.43 | 19.01 | 30.45 |
| anchored, image-level (paper) | 31.74 (100) | 31.69 (100) | 11.00 (91) | 9.87 (44) | 2.96 | 0.0 | 59 / 165 | 10.98 | 20.77 | 30.45 |
| anchored, both | 27.44 (100) | 27.38 (100) | 8.48 (6) | 7.58 (0) | 3.66 | 0.0 | 59 / 165 | 8.43 | 19.01 | 30.45 |
| native, full known, label-level | 32.58 (100) | 32.50 (100) | 8.52 (8) | 6.99 (0) | 3.59 | 0.0 | 59 / 165 | 8.44 | 24.14 | 39.58 |
| native, frozen at source, label-level | 47.77 (100) | 47.79 (100) | 16.65 (100) | 13.11 (100) | 1.94 | 0.0 | 59 / 165 | 8.44 | 39.33 | 50.10 |
| native, frozen at source, image-level | 52.79 (100) | 52.86 (100) | 19.43 (100) | 15.18 (100) | 1.66 | 0.0 | 59 / 165 | 10.48 | 42.32 | 50.10 |
| anchored, weighted, all2 | 7.85 (4) | 7.90 (4) | 3.78 (0) | 3.84 (0) | 234.42 | 42.4 | 59 / 165 | 3.76 | 4.09 | nan |
| native, full known, weighted, all2 | 13.97 (100) | 14.01 (100) | 8.52 (8) | 6.99 (0) | 232.02 | 40.1 | 59 / 165 | 8.44 | 5.54 | nan |
| anchored, stratified, all2 | 12.43 (98) | 12.43 (98) | 7.96 (1) | 7.91 (0) | 232.14 | 42.4 | 59 / 165 | 7.93 | 4.50 | nan |
| anchored, weighted, all3 | 4.13 (0) | 4.16 (0) | 3.23 (0) | 3.47 (0) | 311.23 | 65.3 | 59 / 165 | 3.21 | 0.92 | nan |
| native, full known, weighted, all3 | 4.54 (0) | 4.54 (0) | 3.03 (0) | 2.74 (0) | 311.09 | 65.3 | 59 / 165 | 3.01 | 1.53 | nan |
| anchored, stratified, all3 | 7.17 (0) | 7.15 (0) | 7.79 (1) | 8.12 (0) | 308.87 | 65.3 | 59 / 165 | 7.76 | -0.59 | nan |
| anchored, weighted, all5 | 4.94 (0) | 5.01 (0) | 3.38 (0) | 3.56 (0) | 280.89 | 55.1 | 59 / 165 | 3.35 | 1.59 | nan |
| native, full known, weighted, all5 | 3.59 (0) | 3.54 (0) | 3.55 (0) | 3.37 (0) | 284.70 | 55.6 | 59 / 165 | 3.54 | 0.05 | nan |
| anchored, stratified, all5 | 3.32 (0) | 3.30 (0) | 7.16 (0) | 8.26 (1) | 369.49 | 86.8 | 59 / 165 | 7.08 | -3.76 | nan |
| anchored, weighted, src2 | 21.90 (100) | 21.82 (100) | 6.32 (0) | 6.48 (0) | 4.87 | 0.0 | 59 / 165 | 6.25 | 15.65 | nan |
| native, full known, weighted, src2 | 24.50 (100) | 24.42 (100) | 5.84 (0) | 5.75 (0) | 5.12 | 0.0 | 59 / 165 | 5.77 | 18.72 | nan |
| anchored, stratified, src2 | 21.88 (100) | 21.80 (100) | 6.99 (0) | 7.76 (0) | 4.73 | 0.0 | 59 / 165 | 6.92 | 14.97 | nan |
| anchored, weighted, src3 | 18.03 (100) | 17.90 (100) | 5.19 (0) | 5.42 (0) | 6.25 | 0.0 | 59 / 165 | 5.11 | 12.92 | nan |
| native, full known, weighted, src3 | 19.51 (100) | 19.40 (100) | 4.65 (0) | 4.77 (0) | 6.88 | 0.0 | 59 / 165 | 4.57 | 14.94 | nan |
| anchored, stratified, src3 | 17.85 (100) | 17.72 (100) | 5.49 (0) | 6.10 (0) | 6.23 | 0.0 | 59 / 165 | 5.39 | 12.46 | nan |
| anchored, weighted, src5 | 12.72 (95) | 12.68 (95) | 4.48 (0) | 5.00 (0) | 9.31 | 0.0 | 59 / 165 | 4.41 | 8.31 | nan |
| native, full known, weighted, src5 | 11.91 (84) | 11.82 (84) | 3.82 (0) | 4.04 (0) | 13.60 | 0.0 | 59 / 165 | 3.77 | 8.14 | nan |
| anchored, stratified, src5 | 10.18 (54) | 10.16 (54) | 2.49 (0) | 2.71 (0) | 13.40 | 0.0 | 59 / 165 | 2.36 | 7.82 | nan |

## alpha = 0.05, dataset split

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 458 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 17.05 (100) | 16.92 (100) | 3.41 (0) | 3.19 (0) | 7.33 | 0.0 | 59 / 165 | 3.37 | 13.68 | 30.45 |
| anchored, image-level (paper) | 21.45 (100) | 21.36 (100) | 5.35 (72) | 4.89 (39) | 5.24 | 0.0 | 59 / 165 | 5.31 | 16.14 | 30.45 |
| anchored, both | 17.05 (100) | 16.92 (100) | 3.41 (0) | 3.19 (0) | 7.33 | 0.0 | 59 / 165 | 3.37 | 13.68 | 30.45 |
| native, full known, label-level | 19.54 (100) | 19.42 (100) | 3.43 (0) | 2.87 (0) | 7.50 | 0.0 | 59 / 165 | 3.37 | 16.17 | 39.58 |
| native, frozen at source, label-level | 30.87 (100) | 30.79 (100) | 7.67 (100) | 6.37 (99) | 3.89 | 0.0 | 59 / 165 | 3.37 | 27.50 | 50.10 |
| native, frozen at source, image-level | 36.13 (100) | 36.07 (100) | 10.37 (100) | 8.42 (100) | 3.02 | 0.0 | 59 / 165 | 4.76 | 31.37 | 50.10 |
| anchored, weighted, all2 | 5.78 (76) | 5.85 (76) | 2.18 (0) | 2.21 (0) | 237.13 | 42.4 | 59 / 165 | 2.15 | 3.63 | nan |
| native, full known, weighted, all2 | 7.93 (100) | 7.99 (100) | 3.43 (0) | 2.87 (0) | 234.60 | 40.1 | 59 / 165 | 3.37 | 4.56 | nan |
| anchored, stratified, all2 | 7.00 (97) | 7.05 (98) | 3.16 (0) | 3.20 (0) | 235.18 | 42.4 | 59 / 165 | 3.12 | 3.88 | nan |
| anchored, weighted, all3 | 2.81 (0) | 2.87 (0) | 1.68 (0) | 1.82 (0) | 314.15 | 65.3 | 59 / 165 | 1.65 | 1.16 | nan |
| native, full known, weighted, all3 | 3.14 (1) | 3.15 (2) | 1.50 (0) | 1.41 (0) | 314.13 | 65.3 | 59 / 165 | 1.47 | 1.67 | nan |
| anchored, stratified, all3 | 3.99 (10) | 4.02 (10) | 3.08 (0) | 3.30 (0) | 311.39 | 65.3 | 59 / 165 | 3.04 | 0.95 | nan |
| anchored, weighted, all5 | 2.35 (0) | 2.37 (0) | 1.87 (0) | 2.12 (0) | 287.51 | 55.1 | 59 / 165 | 1.84 | 0.51 | nan |
| native, full known, weighted, all5 | 1.16 (0) | 1.13 (0) | 1.83 (0) | 1.82 (0) | 372.11 | 85.9 | 59 / 165 | 1.81 | -0.65 | nan |
| anchored, stratified, all5 | 1.45 (0) | 1.42 (0) | 2.74 (0) | 3.21 (0) | 371.57 | 86.8 | 59 / 165 | 2.70 | -1.25 | nan |
| anchored, weighted, src2 | 10.69 (100) | 10.66 (100) | 2.52 (0) | 3.21 (0) | 13.16 | 0.0 | 59 / 165 | 2.48 | 8.21 | nan |
| native, full known, weighted, src2 | 12.48 (100) | 12.37 (100) | 2.14 (0) | 2.73 (0) | 14.19 | 0.0 | 59 / 165 | 2.09 | 10.39 | nan |
| anchored, stratified, src2 | 10.66 (100) | 10.62 (100) | 1.84 (0) | 1.99 (0) | 13.75 | 0.0 | 59 / 165 | 1.77 | 8.89 | nan |
| anchored, weighted, src3 | 2.62 (0) | 2.56 (1) | 1.99 (0) | 2.81 (0) | 60.73 | 0.0 | 59 / 165 | 1.95 | 0.68 | nan |
| native, full known, weighted, src3 | 1.23 (0) | 1.18 (0) | 1.61 (0) | 2.37 (0) | 244.01 | 0.0 | 59 / 165 | 1.56 | -0.33 | nan |
| anchored, stratified, src3 | 0.49 (0) | 0.46 (0) | 0.20 (0) | 0.21 (0) | 239.30 | 0.0 | 59 / 165 | 0.17 | 0.32 | nan |
| anchored, weighted, src5 | 0.88 (0) | 0.83 (0) | 2.36 (0) | 2.91 (0) | 382.56 | 89.8 | 59 / 165 | 2.34 | -1.46 | nan |
| native, full known, weighted, src5 | 0.09 (0) | 0.09 (0) | 1.83 (0) | 2.20 (0) | 396.97 | 94.9 | 59 / 165 | 1.81 | -1.72 | nan |
| anchored, stratified, src5 | 0.00 (0) | 0.00 (0) | 0.00 (0) | 0.00 (0) | 458.00 | 100.0 | 59 / 165 | 0.00 | 0.00 | nan |
