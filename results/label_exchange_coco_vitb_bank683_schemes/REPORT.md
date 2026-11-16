# A guarantee for the added labels under (weighted) label exchangeability

CAT-Seg (vitb_bank683), 2000 COCO val2017 (LVIS-annotated) images with a labelled sampled pixel (1283-name vocabulary: 171 source names, then the LVIS v1 annotation mapped to the added names), 500 trials (random half/half image split; source vocabulary as per design). Label loss = pooled fraction of the label's sampled pixels whose score for it is below the threshold. "Added, cal" = mean over added labels present in the calibration images (the quantity the proposition bounds); "added, held-out" = same on the held-out images; "src, class" = class-averaged source loss on held-out images; "src, image" = image-level source risk (the paper's guarantee); size = labels per labelled pixel at 1283 names, held-out images; floor = % of added labels present whose threshold is the grid floor. Risks in % (and % of trials above alpha). Development data; nothing fitted.

## alpha = 0.1, exchangeable

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 1283 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 9.09 (36) | 9.17 (37) | 9.05 (36) | 3.69 (1) | 21.73 | 0.0 | 72 / 466 | 8.65 | 0.44 | 3.95 |
| anchored, image-level (paper) | 21.09 (100) | 21.06 (99) | 21.15 (99) | 9.86 (44) | 8.17 | 0.0 | 72 / 466 | 21.09 | -0.00 | 3.95 |
| anchored, both | 9.08 (36) | 9.16 (37) | 9.04 (36) | 3.68 (0) | 21.74 | 0.0 | 72 / 466 | 8.64 | 0.44 | 3.95 |
| native, full known, label-level | 9.09 (37) | 9.17 (39) | 9.10 (37) | 3.20 (0) | 26.62 | 0.0 | 72 / 466 | 8.64 | 0.45 | 4.28 |
| anchored, weighted, all2 | 9.08 (36) | 9.17 (37) | 9.10 (36) | 3.69 (1) | 21.64 | 0.0 | 72 / 466 | 8.70 | 0.39 | nan |
| native, full known, weighted, all2 | 9.08 (37) | 9.16 (36) | 9.11 (37) | 3.21 (0) | 26.58 | 0.0 | 72 / 466 | 8.65 | 0.42 | nan |
| anchored, stratified, all2 | 7.98 (18) | 7.97 (19) | 7.96 (22) | 6.02 (9) | 44.89 | 0.0 | 72 / 466 | 7.26 | 0.72 | nan |
| anchored, weighted, all3 | 9.12 (37) | 9.20 (38) | 9.13 (37) | 3.71 (0) | 21.54 | 0.0 | 72 / 466 | 8.74 | 0.38 | nan |
| native, full known, weighted, all3 | 9.09 (37) | 9.16 (37) | 9.14 (37) | 3.22 (0) | 26.47 | 0.0 | 72 / 466 | 8.68 | 0.41 | nan |
| anchored, stratified, all3 | 7.06 (8) | 7.08 (9) | 6.95 (12) | 6.22 (9) | 160.57 | 3.9 | 72 / 466 | 6.12 | 0.94 | nan |
| anchored, weighted, all5 | 9.08 (35) | 9.16 (36) | 9.13 (39) | 3.71 (0) | 21.70 | 0.0 | 72 / 466 | 8.74 | 0.33 | nan |
| native, full known, weighted, all5 | 9.05 (37) | 9.13 (36) | 9.11 (37) | 3.23 (0) | 26.71 | 0.0 | 72 / 466 | 8.70 | 0.35 | nan |
| anchored, stratified, all5 | 5.15 (0) | 5.17 (0) | 5.13 (2) | 6.49 (11) | 395.04 | 14.0 | 72 / 466 | 4.11 | 1.04 | nan |
| anchored, weighted, src2 | 9.04 (36) | 9.13 (36) | 9.05 (36) | 3.68 (1) | 21.79 | 0.0 | 72 / 466 | 8.63 | 0.40 | nan |
| native, full known, weighted, src2 | 9.03 (36) | 9.11 (36) | 9.05 (37) | 3.19 (0) | 26.79 | 0.0 | 72 / 466 | 8.60 | 0.43 | nan |
| anchored, stratified, src2 | 7.91 (16) | 7.91 (17) | 8.00 (21) | 5.97 (8) | 45.50 | 0.0 | 72 / 466 | 7.26 | 0.64 | nan |
| anchored, weighted, src3 | 9.08 (35) | 9.17 (38) | 9.10 (37) | 3.70 (0) | 21.65 | 0.0 | 72 / 466 | 8.70 | 0.38 | nan |
| native, full known, weighted, src3 | 9.04 (36) | 9.11 (37) | 9.09 (36) | 3.20 (0) | 26.78 | 0.0 | 72 / 466 | 8.62 | 0.42 | nan |
| anchored, stratified, src3 | 7.03 (9) | 7.06 (9) | 6.96 (11) | 6.33 (11) | 139.78 | 3.0 | 72 / 466 | 6.09 | 0.94 | nan |
| anchored, weighted, src5 | 9.02 (35) | 9.12 (35) | 9.07 (38) | 3.69 (1) | 21.83 | 0.0 | 72 / 466 | 8.67 | 0.35 | nan |
| native, full known, weighted, src5 | 8.97 (35) | 9.04 (35) | 9.03 (36) | 3.19 (0) | 27.06 | 0.0 | 72 / 466 | 8.59 | 0.38 | nan |
| anchored, stratified, src5 | 5.20 (1) | 5.20 (0) | 5.15 (1) | 6.66 (13) | 396.91 | 13.3 | 72 / 466 | 4.14 | 1.07 | nan |

## alpha = 0.05, exchangeable

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 1283 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 4.09 (29) | 4.14 (28) | 4.02 (31) | 1.33 (0) | 58.76 | 0.0 | 72 / 466 | 3.57 | 0.52 | 3.95 |
| anchored, image-level (paper) | 12.39 (99) | 12.50 (99) | 12.39 (98) | 4.85 (40) | 15.80 | 0.0 | 72 / 466 | 12.43 | -0.04 | 3.95 |
| anchored, both | 4.09 (29) | 4.14 (28) | 4.02 (31) | 1.33 (0) | 58.77 | 0.0 | 72 / 466 | 3.56 | 0.52 | 3.95 |
| native, full known, label-level | 4.04 (31) | 4.10 (29) | 3.98 (31) | 1.16 (0) | 177.31 | 0.0 | 72 / 466 | 3.29 | 0.75 | 4.28 |
| anchored, weighted, all2 | 4.10 (28) | 4.15 (29) | 4.06 (32) | 1.33 (1) | 58.42 | 0.0 | 72 / 466 | 3.60 | 0.50 | nan |
| native, full known, weighted, all2 | 4.04 (30) | 4.10 (29) | 3.98 (32) | 1.16 (0) | 173.68 | 0.0 | 72 / 466 | 3.31 | 0.73 | nan |
| anchored, stratified, all2 | 2.94 (8) | 2.96 (8) | 2.88 (11) | 2.14 (4) | 237.26 | 6.6 | 72 / 466 | 2.29 | 0.66 | nan |
| anchored, weighted, all3 | 4.11 (28) | 4.18 (30) | 4.09 (31) | 1.34 (0) | 58.37 | 0.0 | 72 / 466 | 3.64 | 0.47 | nan |
| native, full known, weighted, all3 | 4.05 (30) | 4.11 (30) | 4.01 (33) | 1.17 (0) | 169.89 | 0.0 | 72 / 466 | 3.37 | 0.69 | nan |
| anchored, stratified, all3 | 2.09 (1) | 2.09 (1) | 1.99 (3) | 1.84 (2) | 549.53 | 20.0 | 72 / 466 | 1.49 | 0.60 | nan |
| anchored, weighted, all5 | 4.10 (28) | 4.15 (31) | 4.11 (33) | 1.35 (1) | 58.89 | 0.0 | 72 / 466 | 3.64 | 0.46 | nan |
| native, full known, weighted, all5 | 4.02 (30) | 4.08 (29) | 4.02 (32) | 1.18 (0) | 178.72 | 0.0 | 72 / 466 | 3.34 | 0.68 | nan |
| anchored, stratified, all5 | 0.68 (0) | 0.67 (0) | 0.69 (0) | 1.31 (0) | 971.76 | 55.4 | 72 / 466 | 0.54 | 0.14 | nan |
| anchored, weighted, src2 | 4.07 (28) | 4.13 (29) | 4.04 (31) | 1.33 (1) | 58.83 | 0.0 | 72 / 466 | 3.59 | 0.49 | nan |
| native, full known, weighted, src2 | 4.00 (30) | 4.07 (29) | 3.95 (32) | 1.15 (0) | 176.61 | 0.0 | 72 / 466 | 3.28 | 0.72 | nan |
| anchored, stratified, src2 | 2.92 (7) | 2.94 (7) | 2.90 (10) | 2.14 (4) | 249.99 | 7.0 | 72 / 466 | 2.30 | 0.62 | nan |
| anchored, weighted, src3 | 4.07 (27) | 4.13 (29) | 4.05 (32) | 1.33 (0) | 59.09 | 0.0 | 72 / 466 | 3.60 | 0.47 | nan |
| native, full known, weighted, src3 | 4.02 (29) | 4.08 (29) | 4.00 (31) | 1.16 (0) | 170.46 | 0.0 | 72 / 466 | 3.33 | 0.69 | nan |
| anchored, stratified, src3 | 2.09 (1) | 2.09 (1) | 1.96 (2) | 1.90 (2) | 546.75 | 20.0 | 72 / 466 | 1.49 | 0.60 | nan |
| anchored, weighted, src5 | 4.07 (28) | 4.12 (30) | 4.08 (33) | 1.34 (1) | 59.01 | 0.0 | 72 / 466 | 3.62 | 0.45 | nan |
| native, full known, weighted, src5 | 3.99 (29) | 4.05 (30) | 3.97 (31) | 1.17 (0) | 177.29 | 0.0 | 72 / 466 | 3.32 | 0.67 | nan |
| anchored, stratified, src5 | 0.72 (0) | 0.71 (0) | 0.70 (0) | 1.46 (0) | 965.17 | 54.2 | 72 / 466 | 0.55 | 0.18 | nan |

## alpha = 0.1, dataset split

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 1283 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 22.54 (100) | 22.52 (100) | 9.48 (32) | 3.86 (0) | 8.79 | 0.0 | 170 / 367 | 9.43 | 13.11 | 32.67 |
| anchored, image-level (paper) | 41.12 (100) | 40.90 (100) | 18.96 (100) | 9.87 (41) | 3.90 | 0.0 | 170 / 367 | 19.01 | 22.12 | 32.67 |
| anchored, both | 22.54 (100) | 22.52 (100) | 9.48 (32) | 3.86 (0) | 8.79 | 0.0 | 170 / 367 | 9.43 | 13.11 | 32.67 |
| native, full known, label-level | 26.52 (100) | 26.45 (100) | 9.48 (31) | 3.75 (0) | 7.73 | 0.0 | 170 / 367 | 9.44 | 17.07 | 35.09 |
| native, frozen at source, label-level | 35.27 (100) | 35.13 (100) | 13.61 (100) | 5.86 (0) | 5.14 | 0.0 | 170 / 367 | 9.44 | 25.84 | 43.21 |
| native, frozen at source, image-level | 55.32 (100) | 55.17 (100) | 24.77 (100) | 12.88 (100) | 2.40 | 0.0 | 170 / 367 | 19.26 | 36.07 | 43.21 |
| anchored, weighted, all2 | 5.08 (4) | 5.13 (4) | 2.88 (0) | 1.01 (0) | 53.85 | 0.0 | 170 / 367 | 2.78 | 2.30 | nan |
| native, full known, weighted, all2 | 10.35 (52) | 10.49 (53) | 3.31 (0) | 1.14 (0) | 28.02 | 0.0 | 170 / 367 | 3.20 | 7.15 | nan |
| anchored, stratified, all2 | 8.64 (9) | 8.56 (6) | 9.00 (17) | 4.50 (0) | 481.90 | 26.8 | 170 / 367 | 8.95 | -0.31 | nan |
| anchored, weighted, all3 | 4.86 (2) | 4.88 (3) | 2.34 (0) | 0.82 (0) | 56.28 | 0.0 | 170 / 367 | 2.23 | 2.63 | nan |
| native, full known, weighted, all3 | 9.04 (30) | 9.10 (32) | 4.50 (0) | 1.61 (0) | 442.03 | 29.5 | 170 / 367 | 4.44 | 4.61 | nan |
| anchored, stratified, all3 | 7.89 (6) | 7.81 (4) | 8.71 (11) | 5.10 (0) | 445.90 | 20.7 | 170 / 367 | 8.59 | -0.71 | nan |
| anchored, weighted, all5 | 3.47 (0) | 3.51 (0) | 2.19 (0) | 0.76 (0) | 301.41 | 18.7 | 170 / 367 | 2.08 | 1.38 | nan |
| native, full known, weighted, all5 | 7.29 (2) | 7.28 (2) | 4.90 (0) | 1.76 (0) | 526.01 | 32.3 | 170 / 367 | 4.84 | 2.45 | nan |
| anchored, stratified, all5 | 4.49 (0) | 4.45 (0) | 8.15 (3) | 5.69 (0) | 629.66 | 31.4 | 170 / 367 | 8.07 | -3.58 | nan |
| anchored, weighted, src2 | 14.21 (100) | 14.33 (100) | 5.62 (0) | 2.08 (0) | 14.97 | 0.0 | 170 / 367 | 5.58 | 8.63 | nan |
| native, full known, weighted, src2 | 16.37 (100) | 16.42 (100) | 5.20 (0) | 1.86 (0) | 14.51 | 0.0 | 170 / 367 | 5.09 | 11.28 | nan |
| anchored, stratified, src2 | 14.93 (100) | 15.01 (100) | 8.93 (14) | 6.34 (0) | 12.18 | 0.0 | 170 / 367 | 8.90 | 6.02 | nan |
| anchored, weighted, src3 | 11.31 (75) | 11.42 (79) | 4.52 (0) | 1.65 (0) | 19.19 | 0.0 | 170 / 367 | 4.45 | 6.86 | nan |
| native, full known, weighted, src3 | 13.16 (96) | 13.28 (96) | 4.04 (0) | 1.39 (0) | 19.48 | 0.0 | 170 / 367 | 3.95 | 9.21 | nan |
| anchored, stratified, src3 | 11.45 (77) | 11.55 (80) | 8.45 (7) | 7.02 (0) | 15.62 | 0.0 | 170 / 367 | 8.37 | 3.08 | nan |
| anchored, weighted, src5 | 7.33 (8) | 7.42 (10) | 3.04 (0) | 1.06 (0) | 31.42 | 0.0 | 170 / 367 | 2.95 | 4.38 | nan |
| native, full known, weighted, src5 | 9.17 (33) | 9.32 (35) | 2.84 (0) | 0.97 (0) | 30.81 | 0.0 | 170 / 367 | 2.76 | 6.41 | nan |
| anchored, stratified, src5 | 7.64 (8) | 7.72 (8) | 7.43 (1) | 6.67 (0) | 27.99 | 0.0 | 170 / 367 | 7.32 | 0.31 | nan |

## alpha = 0.05, dataset split

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 1283 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 11.91 (100) | 12.03 (100) | 4.49 (29) | 1.53 (0) | 18.76 | 0.0 | 170 / 367 | 4.42 | 7.48 | 32.67 |
| anchored, image-level (paper) | 26.13 (100) | 26.10 (100) | 11.39 (100) | 4.90 (40) | 7.27 | 0.0 | 170 / 367 | 11.38 | 14.74 | 32.67 |
| anchored, both | 11.91 (100) | 12.03 (100) | 4.49 (29) | 1.53 (0) | 18.76 | 0.0 | 170 / 367 | 4.42 | 7.48 | 32.67 |
| native, full known, label-level | 14.98 (100) | 15.05 (100) | 4.52 (30) | 1.51 (0) | 16.82 | 0.0 | 170 / 367 | 4.43 | 10.55 | 35.09 |
| native, frozen at source, label-level | 20.80 (100) | 20.76 (100) | 6.98 (95) | 2.58 (0) | 10.72 | 0.0 | 170 / 367 | 4.42 | 16.37 | 43.21 |
| native, frozen at source, image-level | 38.76 (100) | 38.63 (100) | 15.38 (100) | 6.92 (100) | 4.41 | 0.0 | 170 / 367 | 10.87 | 27.89 | 43.21 |
| anchored, weighted, all2 | 1.02 (0) | 1.02 (0) | 1.03 (0) | 0.36 (0) | 691.57 | 41.7 | 170 / 367 | 1.02 | -0.00 | nan |
| native, full known, weighted, all2 | 4.21 (28) | 4.23 (30) | 1.15 (0) | 0.42 (0) | 205.89 | 0.0 | 170 / 367 | 1.07 | 3.15 | nan |
| anchored, stratified, all2 | 3.77 (2) | 3.76 (2) | 4.22 (17) | 1.73 (0) | 655.45 | 41.7 | 170 / 367 | 4.18 | -0.42 | nan |
| anchored, weighted, all3 | 1.32 (0) | 1.29 (0) | 0.82 (0) | 0.30 (0) | 506.27 | 20.7 | 170 / 367 | 0.77 | 0.54 | nan |
| native, full known, weighted, all3 | 4.31 (25) | 4.34 (27) | 2.07 (0) | 0.70 (0) | 466.39 | 29.5 | 170 / 367 | 1.97 | 2.34 | nan |
| anchored, stratified, all3 | 2.81 (0) | 2.77 (0) | 3.81 (5) | 2.04 (0) | 866.39 | 62.5 | 170 / 367 | 3.77 | -0.97 | nan |
| anchored, weighted, all5 | 0.84 (0) | 0.82 (0) | 0.75 (0) | 0.28 (0) | 588.89 | 29.4 | 170 / 367 | 0.69 | 0.14 | nan |
| native, full known, weighted, all5 | 3.47 (4) | 3.47 (5) | 2.40 (0) | 0.79 (0) | 553.00 | 32.3 | 170 / 367 | 2.30 | 1.17 | nan |
| anchored, stratified, all5 | 1.71 (0) | 1.67 (0) | 3.49 (1) | 2.31 (0) | 797.65 | 53.1 | 170 / 367 | 3.45 | -1.74 | nan |
| anchored, weighted, src2 | 6.49 (88) | 6.59 (90) | 2.41 (0) | 0.76 (0) | 36.29 | 0.0 | 170 / 367 | 2.34 | 4.15 | nan |
| native, full known, weighted, src2 | 8.31 (99) | 8.45 (99) | 2.28 (0) | 0.73 (0) | 35.71 | 0.0 | 170 / 367 | 2.21 | 6.10 | nan |
| anchored, stratified, src2 | 6.46 (88) | 6.52 (89) | 3.95 (11) | 2.47 (0) | 32.54 | 0.0 | 170 / 367 | 3.87 | 2.59 | nan |
| anchored, weighted, src3 | 4.74 (43) | 4.77 (42) | 1.80 (0) | 0.58 (0) | 52.73 | 0.0 | 170 / 367 | 1.73 | 3.01 | nan |
| native, full known, weighted, src3 | 5.87 (70) | 5.93 (66) | 1.68 (0) | 0.54 (0) | 60.25 | 0.0 | 170 / 367 | 1.59 | 4.28 | nan |
| anchored, stratified, src3 | 4.53 (35) | 4.55 (36) | 3.43 (2) | 2.63 (0) | 49.04 | 0.0 | 170 / 367 | 3.31 | 1.22 | nan |
| anchored, weighted, src5 | 2.58 (4) | 2.56 (3) | 1.12 (0) | 0.37 (0) | 97.05 | 0.0 | 170 / 367 | 0.99 | 1.59 | nan |
| native, full known, weighted, src5 | 3.42 (7) | 3.46 (11) | 1.05 (0) | 0.37 (0) | 210.01 | 0.0 | 170 / 367 | 0.95 | 2.47 | nan |
| anchored, stratified, src5 | 2.30 (1) | 2.29 (1) | 2.41 (0) | 1.91 (0) | 103.58 | 0.0 | 170 / 367 | 2.19 | 0.10 | nan |
