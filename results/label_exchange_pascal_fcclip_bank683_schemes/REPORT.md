# A guarantee for the added labels under (weighted) label exchangeability

CAT-Seg (fcclip_bank683), 2000 Pascal Context validation images with a labelled sampled pixel (458-name vocabulary: 59 source names, then the PC-459 annotation mapped to the added names), 500 trials (random half/half image split; source vocabulary as per design). Label loss = pooled fraction of the label's sampled pixels whose score for it is below the threshold. "Added, cal" = mean over added labels present in the calibration images (the quantity the proposition bounds); "added, held-out" = same on the held-out images; "src, class" = class-averaged source loss on held-out images; "src, image" = image-level source risk (the paper's guarantee); size = labels per labelled pixel at 458 names, held-out images; floor = % of added labels present whose threshold is the grid floor. Risks in % (and % of trials above alpha). Development data; nothing fitted.

## alpha = 0.1, exchangeable

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 458 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 7.47 (23) | 7.54 (22) | 7.51 (24) | 5.07 (9) | 43.40 | 0.0 | 29 / 195 | 6.73 | 0.74 | 7.00 |
| anchored, image-level (paper) | 15.37 (77) | 15.44 (77) | 15.07 (78) | 9.90 (45) | 16.54 | 0.0 | 29 / 195 | 15.04 | 0.33 | 7.00 |
| anchored, both | 7.24 (21) | 7.32 (20) | 7.30 (22) | 4.82 (7) | 44.30 | 0.0 | 29 / 195 | 6.59 | 0.66 | 7.00 |
| native, full known, label-level | 7.51 (24) | 7.62 (26) | 7.53 (27) | 4.63 (10) | 49.75 | 0.0 | 29 / 195 | 6.72 | 0.79 | 6.99 |
| anchored, weighted, all2 | 7.36 (22) | 7.42 (21) | 7.48 (24) | 5.10 (9) | 44.70 | 0.0 | 29 / 195 | 6.75 | 0.61 | nan |
| native, full known, weighted, all2 | 7.49 (24) | 7.59 (24) | 7.54 (26) | 4.62 (10) | 49.18 | 0.0 | 29 / 195 | 6.77 | 0.72 | nan |
| anchored, stratified, all2 | 4.98 (5) | 5.06 (4) | 4.73 (6) | 4.34 (5) | 144.92 | 10.6 | 29 / 195 | 3.72 | 1.26 | nan |
| anchored, weighted, all3 | 7.33 (22) | 7.38 (21) | 7.53 (24) | 5.11 (10) | 44.87 | 0.0 | 29 / 195 | 6.75 | 0.58 | nan |
| native, full known, weighted, all3 | 7.44 (22) | 7.56 (24) | 7.61 (26) | 4.61 (9) | 50.14 | 0.0 | 29 / 195 | 6.80 | 0.63 | nan |
| anchored, stratified, all3 | 2.57 (0) | 2.58 (0) | 2.55 (1) | 3.30 (2) | 266.82 | 35.0 | 29 / 195 | 1.90 | 0.67 | nan |
| anchored, weighted, all5 | 7.27 (21) | 7.30 (21) | 7.65 (24) | 5.23 (11) | 48.10 | 0.3 | 29 / 195 | 6.86 | 0.41 | nan |
| native, full known, weighted, all5 | 7.33 (22) | 7.46 (24) | 7.70 (28) | 4.71 (9) | 55.07 | 0.5 | 29 / 195 | 6.93 | 0.40 | nan |
| anchored, stratified, all5 | 0.52 (0) | 0.51 (0) | 0.63 (0) | 1.15 (0) | 405.09 | 75.5 | 29 / 195 | 0.47 | 0.05 | nan |
| anchored, weighted, src2 | 7.30 (21) | 7.37 (21) | 7.43 (23) | 5.10 (10) | 44.87 | 0.0 | 29 / 195 | 6.70 | 0.61 | nan |
| native, full known, weighted, src2 | 7.46 (24) | 7.53 (25) | 7.55 (26) | 4.66 (10) | 49.86 | 0.0 | 29 / 195 | 6.73 | 0.73 | nan |
| anchored, stratified, src2 | 4.93 (5) | 5.01 (5) | 4.76 (5) | 4.30 (5) | 142.47 | 9.4 | 29 / 195 | 3.70 | 1.23 | nan |
| anchored, weighted, src3 | 7.18 (20) | 7.22 (21) | 7.37 (23) | 5.02 (10) | 46.30 | 0.0 | 29 / 195 | 6.57 | 0.61 | nan |
| native, full known, weighted, src3 | 7.25 (22) | 7.38 (22) | 7.41 (26) | 4.54 (9) | 52.47 | 0.0 | 29 / 195 | 6.62 | 0.63 | nan |
| anchored, stratified, src3 | 2.66 (0) | 2.64 (0) | 2.67 (1) | 3.39 (2) | 262.28 | 33.7 | 29 / 195 | 1.86 | 0.80 | nan |
| anchored, weighted, src5 | 7.17 (20) | 7.23 (20) | 7.52 (25) | 5.11 (10) | 46.96 | 0.0 | 29 / 195 | 6.73 | 0.44 | nan |
| native, full known, weighted, src5 | 7.20 (21) | 7.33 (23) | 7.49 (26) | 4.60 (9) | 53.93 | 0.0 | 29 / 195 | 6.73 | 0.47 | nan |
| anchored, stratified, src5 | 0.36 (0) | 0.35 (0) | 0.37 (0) | 0.91 (0) | 407.86 | 71.9 | 29 / 195 | 0.27 | 0.09 | nan |

## alpha = 0.05, exchangeable

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 458 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 2.50 (12) | 2.59 (13) | 2.29 (12) | 1.35 (4) | 132.28 | 0.6 | 29 / 195 | 1.54 | 0.95 | 7.00 |
| anchored, image-level (paper) | 8.55 (78) | 8.69 (81) | 8.41 (74) | 4.89 (42) | 37.21 | 0.0 | 29 / 195 | 8.38 | 0.17 | 7.00 |
| anchored, both | 2.46 (11) | 2.56 (12) | 2.25 (12) | 1.31 (2) | 132.65 | 0.6 | 29 / 195 | 1.53 | 0.93 | 7.00 |
| native, full known, label-level | 2.52 (12) | 2.61 (15) | 2.43 (16) | 1.18 (3) | 158.70 | 0.6 | 29 / 195 | 1.55 | 0.97 | 6.99 |
| anchored, weighted, all2 | 2.45 (11) | 2.52 (12) | 2.30 (13) | 1.37 (4) | 139.45 | 2.5 | 29 / 195 | 1.58 | 0.87 | nan |
| native, full known, weighted, all2 | 2.40 (11) | 2.50 (13) | 2.40 (13) | 1.14 (2) | 167.56 | 2.5 | 29 / 195 | 1.62 | 0.78 | nan |
| anchored, stratified, all2 | 0.31 (0) | 0.32 (0) | 0.36 (1) | 0.32 (0) | 387.63 | 66.9 | 29 / 195 | 0.17 | 0.14 | nan |
| anchored, weighted, all3 | 2.36 (9) | 2.43 (10) | 2.37 (14) | 1.37 (3) | 148.17 | 5.2 | 29 / 195 | 1.62 | 0.74 | nan |
| native, full known, weighted, all3 | 2.39 (10) | 2.46 (13) | 2.48 (16) | 1.14 (2) | 176.05 | 6.4 | 29 / 195 | 1.69 | 0.70 | nan |
| anchored, stratified, all3 | 0.02 (0) | 0.02 (0) | 0.02 (0) | 0.03 (0) | 453.21 | 97.0 | 29 / 195 | 0.01 | 0.00 | nan |
| anchored, weighted, all5 | 2.25 (8) | 2.32 (9) | 2.49 (16) | 1.45 (5) | 168.79 | 12.7 | 29 / 195 | 1.78 | 0.47 | nan |
| native, full known, weighted, all5 | 2.30 (10) | 2.37 (10) | 2.58 (16) | 1.24 (4) | 191.76 | 12.6 | 29 / 195 | 1.80 | 0.50 | nan |
| anchored, stratified, all5 | 0.00 (0) | 0.00 (0) | 0.00 (0) | 0.00 (0) | 458.00 | 100.0 | 29 / 195 | 0.00 | 0.00 | nan |
| anchored, weighted, src2 | 2.41 (10) | 2.48 (12) | 2.25 (13) | 1.38 (4) | 140.08 | 2.2 | 29 / 195 | 1.55 | 0.85 | nan |
| native, full known, weighted, src2 | 2.38 (10) | 2.48 (13) | 2.35 (13) | 1.18 (3) | 166.65 | 1.7 | 29 / 195 | 1.59 | 0.79 | nan |
| anchored, stratified, src2 | 0.26 (0) | 0.27 (0) | 0.32 (0) | 0.31 (0) | 384.32 | 63.4 | 29 / 195 | 0.14 | 0.12 | nan |
| anchored, weighted, src3 | 2.22 (8) | 2.29 (9) | 2.25 (12) | 1.33 (3) | 149.77 | 4.2 | 29 / 195 | 1.51 | 0.71 | nan |
| native, full known, weighted, src3 | 2.32 (11) | 2.40 (12) | 2.35 (14) | 1.15 (3) | 175.10 | 4.3 | 29 / 195 | 1.56 | 0.76 | nan |
| anchored, stratified, src3 | 0.00 (0) | 0.00 (0) | 0.00 (0) | 0.00 (0) | 457.52 | 99.4 | 29 / 195 | 0.00 | 0.00 | nan |
| anchored, weighted, src5 | 2.16 (7) | 2.22 (8) | 2.34 (13) | 1.39 (4) | 167.21 | 9.8 | 29 / 195 | 1.69 | 0.47 | nan |
| native, full known, weighted, src5 | 2.19 (8) | 2.24 (8) | 2.50 (16) | 1.16 (2) | 192.05 | 9.9 | 29 / 195 | 1.69 | 0.50 | nan |
| anchored, stratified, src5 | 0.00 (0) | 0.00 (0) | 0.00 (0) | 0.00 (0) | 458.00 | 100.0 | 29 / 195 | 0.00 | 0.00 | nan |

## alpha = 0.1, dataset split

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 458 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 22.95 (100) | 23.00 (100) | 8.52 (7) | 7.92 (0) | 8.25 | 0.0 | 59 / 165 | 8.44 | 14.51 | 28.48 |
| anchored, image-level (paper) | 26.37 (100) | 26.43 (100) | 10.43 (71) | 9.86 (42) | 6.09 | 0.0 | 59 / 165 | 10.36 | 16.01 | 28.48 |
| anchored, both | 22.95 (100) | 23.00 (100) | 8.52 (7) | 7.92 (0) | 8.25 | 0.0 | 59 / 165 | 8.44 | 14.51 | 28.48 |
| native, full known, label-level | 25.08 (100) | 25.03 (100) | 8.54 (8) | 9.00 (10) | 6.12 | 0.0 | 59 / 165 | 8.43 | 16.65 | 27.30 |
| native, frozen at source, label-level | 35.47 (100) | 35.45 (100) | 15.10 (100) | 15.43 (100) | 3.10 | 0.0 | 59 / 165 | 8.43 | 27.04 | 38.98 |
| native, frozen at source, image-level | 36.83 (100) | 36.79 (100) | 15.90 (100) | 16.24 (100) | 2.89 | 0.0 | 59 / 165 | 9.01 | 27.82 | 38.98 |
| anchored, weighted, all2 | 5.78 (0) | 5.81 (0) | 4.27 (0) | 3.26 (0) | 239.54 | 46.6 | 59 / 165 | 4.21 | 1.57 | nan |
| native, full known, weighted, all2 | 13.51 (100) | 13.41 (100) | 9.21 (20) | 9.52 (23) | 232.81 | 38.3 | 59 / 165 | 9.10 | 4.41 | nan |
| anchored, stratified, all2 | 9.33 (27) | 9.32 (27) | 8.35 (5) | 6.58 (0) | 234.33 | 46.6 | 59 / 165 | 8.27 | 1.06 | nan |
| anchored, weighted, all3 | 2.94 (0) | 2.91 (0) | 3.46 (0) | 2.95 (0) | 314.61 | 67.7 | 59 / 165 | 3.43 | -0.48 | nan |
| native, full known, weighted, all3 | 11.90 (77) | 11.92 (79) | 8.08 (25) | 8.46 (30) | 162.33 | 42.2 | 59 / 165 | 7.99 | 3.91 | nan |
| anchored, stratified, all3 | 5.05 (0) | 5.05 (0) | 7.82 (1) | 6.76 (0) | 310.14 | 67.7 | 59 / 165 | 7.76 | -2.71 | nan |
| anchored, weighted, all5 | 4.60 (0) | 4.55 (0) | 5.25 (0) | 4.03 (0) | 282.86 | 59.1 | 59 / 165 | 5.18 | -0.58 | nan |
| native, full known, weighted, all5 | 9.35 (29) | 9.36 (30) | 7.01 (0) | 7.36 (0) | 192.86 | 39.5 | 59 / 165 | 6.88 | 2.47 | nan |
| anchored, stratified, all5 | 3.07 (0) | 3.02 (0) | 6.69 (0) | 4.45 (0) | 289.21 | 59.1 | 59 / 165 | 6.58 | -3.52 | nan |
| anchored, weighted, src2 | 17.95 (100) | 18.07 (100) | 6.74 (0) | 5.91 (0) | 12.44 | 0.0 | 59 / 165 | 6.62 | 11.33 | nan |
| native, full known, weighted, src2 | 16.93 (100) | 16.95 (100) | 5.02 (0) | 5.39 (0) | 12.55 | 0.0 | 59 / 165 | 4.91 | 12.02 | nan |
| anchored, stratified, src2 | 17.76 (100) | 17.88 (100) | 7.04 (0) | 6.12 (0) | 12.51 | 0.0 | 59 / 165 | 6.91 | 10.85 | nan |
| anchored, weighted, src3 | 14.75 (100) | 14.85 (100) | 6.04 (0) | 4.88 (0) | 17.15 | 0.0 | 59 / 165 | 5.95 | 8.80 | nan |
| native, full known, weighted, src3 | 15.12 (100) | 15.14 (100) | 4.65 (0) | 5.02 (0) | 16.36 | 0.0 | 59 / 165 | 4.59 | 10.53 | nan |
| anchored, stratified, src3 | 13.73 (99) | 13.80 (100) | 5.54 (0) | 4.87 (0) | 19.21 | 0.0 | 59 / 165 | 5.39 | 8.35 | nan |
| anchored, weighted, src5 | 9.62 (39) | 9.65 (39) | 5.77 (0) | 5.24 (0) | 32.93 | 0.0 | 59 / 165 | 5.67 | 3.94 | nan |
| native, full known, weighted, src5 | 13.16 (99) | 13.22 (98) | 5.35 (0) | 4.93 (0) | 21.88 | 0.0 | 59 / 165 | 5.27 | 7.89 | nan |
| anchored, stratified, src5 | 6.47 (2) | 6.54 (1) | 2.51 (0) | 2.01 (0) | 50.35 | 0.0 | 59 / 165 | 2.35 | 4.12 | nan |

## alpha = 0.05, dataset split

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 458 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 12.23 (100) | 12.32 (100) | 3.43 (0) | 3.04 (0) | 23.85 | 0.0 | 59 / 165 | 3.37 | 8.85 | 28.48 |
| anchored, image-level (paper) | 16.57 (100) | 16.68 (100) | 5.30 (71) | 4.90 (41) | 14.51 | 0.0 | 59 / 165 | 5.24 | 11.33 | 28.48 |
| anchored, both | 12.23 (100) | 12.32 (100) | 3.43 (0) | 3.04 (0) | 23.85 | 0.0 | 59 / 165 | 3.37 | 8.85 | 28.48 |
| native, full known, label-level | 14.41 (100) | 14.49 (100) | 3.44 (0) | 3.66 (0) | 18.63 | 0.0 | 59 / 165 | 3.37 | 11.04 | 27.30 |
| native, frozen at source, label-level | 21.80 (100) | 21.78 (100) | 6.92 (100) | 7.30 (100) | 8.00 | 0.0 | 59 / 165 | 3.37 | 18.43 | 38.98 |
| native, frozen at source, image-level | 24.33 (100) | 24.32 (100) | 8.10 (100) | 8.58 (100) | 6.51 | 0.0 | 59 / 165 | 4.10 | 20.23 | 38.98 |
| anchored, weighted, all2 | 2.72 (0) | 2.72 (0) | 1.68 (0) | 1.18 (0) | 251.11 | 46.6 | 59 / 165 | 1.66 | 1.06 | nan |
| native, full known, weighted, all2 | 8.14 (100) | 8.16 (100) | 4.61 (29) | 5.05 (49) | 236.92 | 38.3 | 59 / 165 | 4.53 | 3.61 | nan |
| anchored, stratified, all2 | 4.74 (35) | 4.75 (40) | 3.35 (0) | 2.48 (0) | 242.08 | 46.6 | 59 / 165 | 3.29 | 1.45 | nan |
| anchored, weighted, all3 | 1.39 (0) | 1.36 (0) | 1.41 (0) | 1.13 (0) | 322.29 | 67.7 | 59 / 165 | 1.40 | -0.01 | nan |
| native, full known, weighted, all3 | 3.35 (11) | 3.32 (9) | 4.10 (27) | 4.53 (34) | 313.63 | 65.7 | 59 / 165 | 4.06 | -0.71 | nan |
| anchored, stratified, all3 | 2.73 (0) | 2.70 (0) | 3.09 (0) | 2.60 (0) | 315.31 | 67.7 | 59 / 165 | 3.03 | -0.30 | nan |
| anchored, weighted, all5 | 1.83 (0) | 1.80 (0) | 1.96 (0) | 1.21 (0) | 293.60 | 59.1 | 59 / 165 | 1.94 | -0.11 | nan |
| native, full known, weighted, all5 | 2.42 (0) | 2.39 (0) | 2.71 (0) | 2.62 (0) | 289.63 | 54.4 | 59 / 165 | 2.67 | -0.25 | nan |
| anchored, stratified, all5 | 0.66 (0) | 0.64 (0) | 2.32 (0) | 1.08 (0) | 373.38 | 83.6 | 59 / 165 | 2.28 | -1.62 | nan |
| anchored, weighted, src2 | 7.42 (98) | 7.49 (99) | 2.76 (0) | 1.91 (0) | 44.58 | 0.0 | 59 / 165 | 2.72 | 4.71 | nan |
| native, full known, weighted, src2 | 7.47 (98) | 7.56 (99) | 1.60 (0) | 1.39 (0) | 50.29 | 0.0 | 59 / 165 | 1.56 | 5.90 | nan |
| anchored, stratified, src2 | 7.04 (97) | 7.11 (99) | 1.82 (0) | 1.41 (0) | 48.08 | 0.0 | 59 / 165 | 1.77 | 5.28 | nan |
| anchored, weighted, src3 | 2.78 (0) | 2.86 (2) | 2.18 (0) | 1.06 (0) | 106.75 | 0.0 | 59 / 165 | 2.15 | 0.63 | nan |
| native, full known, weighted, src3 | 3.26 (2) | 3.31 (4) | 1.36 (0) | 1.49 (0) | 112.54 | 0.0 | 59 / 165 | 1.34 | 1.93 | nan |
| anchored, stratified, src3 | 0.06 (0) | 0.06 (0) | 0.19 (0) | 0.10 (0) | 376.02 | 0.0 | 59 / 165 | 0.17 | -0.11 | nan |
| anchored, weighted, src5 | 0.65 (0) | 0.65 (0) | 2.64 (0) | 2.21 (0) | 370.89 | 83.0 | 59 / 165 | 2.61 | -1.96 | nan |
| native, full known, weighted, src5 | 1.44 (0) | 1.45 (0) | 2.41 (0) | 1.89 (0) | 348.17 | 75.8 | 59 / 165 | 2.38 | -0.94 | nan |
| anchored, stratified, src5 | 0.00 (0) | 0.00 (0) | 0.00 (0) | 0.00 (0) | 458.00 | 100.0 | 59 / 165 | 0.00 | 0.00 | nan |
