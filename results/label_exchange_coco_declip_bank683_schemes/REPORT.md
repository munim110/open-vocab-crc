# A guarantee for the added labels under (weighted) label exchangeability

CAT-Seg (declip_bank683), 2000 COCO val2017 (LVIS-annotated) images with a labelled sampled pixel (1283-name vocabulary: 171 source names, then the LVIS v1 annotation mapped to the added names), 500 trials (random half/half image split; source vocabulary as per design). Label loss = pooled fraction of the label's sampled pixels whose score for it is below the threshold. "Added, cal" = mean over added labels present in the calibration images (the quantity the proposition bounds); "added, held-out" = same on the held-out images; "src, class" = class-averaged source loss on held-out images; "src, image" = image-level source risk (the paper's guarantee); size = labels per labelled pixel at 1283 names, held-out images; floor = % of added labels present whose threshold is the grid floor. Risks in % (and % of trials above alpha). Development data; nothing fitted.

## alpha = 0.1, exchangeable

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 1283 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 9.03 (35) | 9.08 (33) | 8.93 (34) | 5.17 (6) | 9.54 | 0.0 | 72 / 466 | 8.65 | 0.38 | 3.81 |
| anchored, image-level (paper) | 16.49 (94) | 16.52 (93) | 16.58 (90) | 9.88 (45) | 5.31 | 0.0 | 72 / 466 | 16.53 | -0.04 | 3.81 |
| anchored, both | 8.96 (34) | 9.01 (32) | 8.87 (33) | 5.10 (4) | 9.57 | 0.0 | 72 / 466 | 8.59 | 0.37 | 3.81 |
| native, full known, label-level | 9.07 (37) | 9.12 (36) | 9.00 (33) | 4.68 (4) | 10.07 | 0.0 | 72 / 466 | 8.62 | 0.45 | 4.11 |
| anchored, weighted, all2 | 9.05 (34) | 9.10 (33) | 9.02 (35) | 5.20 (7) | 9.49 | 0.0 | 72 / 466 | 8.70 | 0.35 | nan |
| native, full known, weighted, all2 | 9.04 (35) | 9.10 (34) | 9.02 (36) | 4.69 (4) | 10.04 | 0.0 | 72 / 466 | 8.63 | 0.41 | nan |
| anchored, stratified, all2 | 8.13 (19) | 8.16 (19) | 8.04 (22) | 7.79 (24) | 14.75 | 0.0 | 72 / 466 | 7.26 | 0.87 | nan |
| anchored, weighted, all3 | 9.07 (33) | 9.13 (33) | 9.04 (34) | 5.21 (6) | 9.45 | 0.0 | 72 / 466 | 8.72 | 0.35 | nan |
| native, full known, weighted, all3 | 9.06 (36) | 9.11 (35) | 9.06 (37) | 4.71 (5) | 10.03 | 0.0 | 72 / 466 | 8.67 | 0.39 | nan |
| anchored, stratified, all3 | 7.07 (9) | 7.12 (9) | 6.85 (12) | 7.31 (18) | 200.05 | 5.4 | 72 / 466 | 6.16 | 0.91 | nan |
| anchored, weighted, all5 | 9.04 (32) | 9.10 (31) | 9.03 (34) | 5.21 (6) | 9.47 | 0.0 | 72 / 466 | 8.72 | 0.33 | nan |
| native, full known, weighted, all5 | 9.05 (35) | 9.11 (35) | 9.06 (37) | 4.73 (4) | 10.06 | 0.0 | 72 / 466 | 8.68 | 0.37 | nan |
| anchored, stratified, all5 | 5.46 (1) | 5.48 (1) | 5.26 (2) | 7.44 (20) | 371.30 | 9.9 | 72 / 466 | 4.43 | 1.03 | nan |
| anchored, weighted, src2 | 9.00 (33) | 9.05 (32) | 8.95 (33) | 5.17 (6) | 9.54 | 0.0 | 72 / 466 | 8.65 | 0.35 | nan |
| native, full known, weighted, src2 | 8.99 (34) | 9.04 (34) | 8.96 (35) | 4.65 (4) | 10.13 | 0.0 | 72 / 466 | 8.57 | 0.42 | nan |
| anchored, stratified, src2 | 8.03 (17) | 8.08 (18) | 7.99 (20) | 7.71 (23) | 15.23 | 0.0 | 72 / 466 | 7.26 | 0.77 | nan |
| anchored, weighted, src3 | 9.02 (33) | 9.07 (32) | 8.97 (34) | 5.19 (6) | 9.51 | 0.0 | 72 / 466 | 8.67 | 0.35 | nan |
| native, full known, weighted, src3 | 9.00 (35) | 9.06 (34) | 9.00 (35) | 4.67 (4) | 10.09 | 0.0 | 72 / 466 | 8.60 | 0.41 | nan |
| anchored, stratified, src3 | 7.12 (9) | 7.16 (10) | 6.92 (12) | 7.60 (22) | 193.21 | 5.2 | 72 / 466 | 6.17 | 0.95 | nan |
| anchored, weighted, src5 | 9.00 (32) | 9.05 (31) | 8.98 (33) | 5.20 (6) | 9.52 | 0.0 | 72 / 466 | 8.66 | 0.34 | nan |
| native, full known, weighted, src5 | 8.98 (35) | 9.02 (34) | 8.96 (35) | 4.67 (4) | 10.15 | 0.0 | 72 / 466 | 8.60 | 0.38 | nan |
| anchored, stratified, src5 | 5.50 (1) | 5.51 (2) | 5.25 (2) | 7.49 (18) | 378.94 | 10.3 | 72 / 466 | 4.41 | 1.08 | nan |

## alpha = 0.05, exchangeable

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 1283 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 4.09 (27) | 4.13 (29) | 4.03 (30) | 1.95 (2) | 22.51 | 0.0 | 72 / 466 | 3.55 | 0.54 | 3.81 |
| anchored, image-level (paper) | 9.43 (97) | 9.51 (97) | 9.36 (89) | 4.82 (42) | 9.28 | 0.0 | 72 / 466 | 9.46 | -0.03 | 3.81 |
| anchored, both | 4.06 (27) | 4.11 (29) | 4.02 (30) | 1.94 (1) | 22.54 | 0.0 | 72 / 466 | 3.54 | 0.52 | 3.81 |
| native, full known, label-level | 4.10 (31) | 4.13 (32) | 4.04 (32) | 1.65 (2) | 46.81 | 0.0 | 72 / 466 | 3.52 | 0.58 | 4.11 |
| anchored, weighted, all2 | 4.10 (28) | 4.15 (30) | 4.07 (32) | 1.96 (2) | 22.58 | 0.0 | 72 / 466 | 3.59 | 0.51 | nan |
| native, full known, weighted, all2 | 4.08 (30) | 4.11 (32) | 4.06 (32) | 1.64 (2) | 53.01 | 0.0 | 72 / 466 | 3.51 | 0.57 | nan |
| anchored, stratified, all2 | 2.80 (5) | 2.81 (6) | 2.70 (7) | 2.73 (8) | 292.08 | 10.6 | 72 / 466 | 2.34 | 0.47 | nan |
| anchored, weighted, all3 | 4.11 (28) | 4.16 (29) | 4.07 (30) | 1.97 (2) | 22.50 | 0.0 | 72 / 466 | 3.61 | 0.50 | nan |
| native, full known, weighted, all3 | 4.06 (30) | 4.10 (32) | 4.07 (31) | 1.64 (2) | 54.61 | 0.0 | 72 / 466 | 3.51 | 0.55 | nan |
| anchored, stratified, all3 | 2.13 (1) | 2.12 (2) | 2.02 (3) | 2.22 (4) | 525.29 | 17.0 | 72 / 466 | 1.62 | 0.50 | nan |
| anchored, weighted, all5 | 4.07 (27) | 4.13 (29) | 4.09 (30) | 1.97 (2) | 22.80 | 0.0 | 72 / 466 | 3.61 | 0.46 | nan |
| native, full known, weighted, all5 | 4.07 (30) | 4.10 (32) | 4.09 (32) | 1.65 (2) | 62.00 | 0.0 | 72 / 466 | 3.50 | 0.57 | nan |
| anchored, stratified, all5 | 0.72 (0) | 0.74 (0) | 0.73 (0) | 1.38 (1) | 928.48 | 51.6 | 72 / 466 | 0.57 | 0.15 | nan |
| anchored, weighted, src2 | 4.07 (27) | 4.12 (29) | 4.03 (30) | 1.96 (2) | 22.82 | 0.0 | 72 / 466 | 3.55 | 0.52 | nan |
| native, full known, weighted, src2 | 4.05 (29) | 4.08 (31) | 4.04 (32) | 1.64 (2) | 52.62 | 0.0 | 72 / 466 | 3.48 | 0.56 | nan |
| anchored, stratified, src2 | 2.78 (5) | 2.81 (6) | 2.69 (7) | 2.73 (9) | 290.77 | 10.2 | 72 / 466 | 2.35 | 0.43 | nan |
| anchored, weighted, src3 | 4.09 (27) | 4.13 (28) | 4.05 (30) | 1.97 (2) | 22.69 | 0.0 | 72 / 466 | 3.58 | 0.50 | nan |
| native, full known, weighted, src3 | 4.05 (30) | 4.09 (32) | 4.05 (31) | 1.63 (2) | 56.36 | 0.0 | 72 / 466 | 3.49 | 0.56 | nan |
| anchored, stratified, src3 | 2.17 (1) | 2.18 (1) | 2.04 (3) | 2.37 (4) | 516.41 | 16.5 | 72 / 466 | 1.62 | 0.55 | nan |
| anchored, weighted, src5 | 4.05 (26) | 4.10 (29) | 4.06 (30) | 1.96 (2) | 22.89 | 0.0 | 72 / 466 | 3.59 | 0.45 | nan |
| native, full known, weighted, src5 | 4.02 (30) | 4.06 (31) | 4.02 (31) | 1.64 (2) | 64.43 | 0.0 | 72 / 466 | 3.46 | 0.56 | nan |
| anchored, stratified, src5 | 0.76 (0) | 0.77 (0) | 0.71 (0) | 1.57 (1) | 919.79 | 49.6 | 72 / 466 | 0.58 | 0.18 | nan |

## alpha = 0.1, dataset split

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 1283 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 14.62 (100) | 14.70 (100) | 9.53 (33) | 4.52 (0) | 6.17 | 0.0 | 170 / 367 | 9.44 | 5.18 | 28.07 |
| anchored, image-level (paper) | 28.37 (100) | 28.39 (100) | 17.11 (100) | 9.88 (44) | 3.25 | 0.0 | 170 / 367 | 17.11 | 11.26 | 28.07 |
| anchored, both | 14.62 (100) | 14.70 (100) | 9.53 (33) | 4.52 (0) | 6.17 | 0.0 | 170 / 367 | 9.44 | 5.18 | 28.07 |
| native, full known, label-level | 16.97 (100) | 17.03 (100) | 9.52 (34) | 4.44 (0) | 5.34 | 0.0 | 170 / 367 | 9.44 | 7.53 | 31.19 |
| native, frozen at source, label-level | 23.04 (100) | 23.10 (100) | 12.41 (98) | 6.31 (0) | 3.91 | 0.0 | 170 / 367 | 9.44 | 13.60 | 38.51 |
| native, frozen at source, image-level | 39.81 (100) | 39.74 (100) | 22.22 (100) | 12.88 (100) | 2.09 | 0.0 | 170 / 367 | 17.37 | 22.43 | 38.51 |
| anchored, weighted, all2 | 1.70 (0) | 1.72 (0) | 1.67 (0) | 0.63 (0) | 44.71 | 0.0 | 170 / 367 | 1.56 | 0.14 | nan |
| native, full known, weighted, all2 | 4.41 (0) | 4.45 (0) | 2.51 (0) | 0.97 (0) | 34.15 | 0.0 | 170 / 367 | 2.39 | 2.03 | nan |
| anchored, stratified, all2 | 7.30 (0) | 7.23 (0) | 9.01 (18) | 5.80 (0) | 494.32 | 23.9 | 170 / 367 | 8.96 | -1.66 | nan |
| anchored, weighted, all3 | 2.49 (0) | 2.51 (0) | 2.25 (0) | 0.85 (0) | 34.61 | 0.0 | 170 / 367 | 2.13 | 0.36 | nan |
| native, full known, weighted, all3 | 4.10 (0) | 4.19 (0) | 2.69 (0) | 0.96 (0) | 68.38 | 0.0 | 170 / 367 | 2.57 | 1.53 | nan |
| anchored, stratified, all3 | 5.30 (0) | 5.27 (0) | 8.78 (13) | 5.76 (0) | 446.28 | 17.2 | 170 / 367 | 8.60 | -3.30 | nan |
| anchored, weighted, all5 | 1.57 (0) | 1.55 (0) | 1.52 (0) | 0.59 (0) | 290.78 | 6.0 | 170 / 367 | 1.45 | 0.12 | nan |
| native, full known, weighted, all5 | 2.89 (0) | 2.92 (0) | 2.53 (0) | 0.97 (0) | 509.81 | 13.0 | 170 / 367 | 2.45 | 0.45 | nan |
| anchored, stratified, all5 | 2.90 (0) | 2.86 (0) | 8.08 (1) | 6.16 (0) | 640.87 | 27.1 | 170 / 367 | 8.02 | -5.12 | nan |
| anchored, weighted, src2 | 8.88 (20) | 8.94 (20) | 5.89 (0) | 2.52 (0) | 9.82 | 0.0 | 170 / 367 | 5.84 | 3.04 | nan |
| native, full known, weighted, src2 | 9.78 (41) | 9.85 (44) | 5.13 (0) | 2.12 (0) | 9.94 | 0.0 | 170 / 367 | 5.09 | 4.69 | nan |
| anchored, stratified, src2 | 9.03 (24) | 9.09 (22) | 8.95 (12) | 7.00 (0) | 7.93 | 0.0 | 170 / 367 | 8.91 | 0.13 | nan |
| anchored, weighted, src3 | 6.87 (0) | 6.94 (1) | 4.72 (0) | 1.89 (0) | 12.60 | 0.0 | 170 / 367 | 4.68 | 2.19 | nan |
| native, full known, weighted, src3 | 7.40 (4) | 7.49 (3) | 3.96 (0) | 1.55 (0) | 13.43 | 0.0 | 170 / 367 | 3.89 | 3.51 | nan |
| anchored, stratified, src3 | 7.14 (1) | 7.21 (1) | 8.43 (4) | 7.07 (0) | 9.87 | 0.0 | 170 / 367 | 8.38 | -1.23 | nan |
| anchored, weighted, src5 | 4.48 (0) | 4.53 (0) | 3.27 (0) | 1.24 (0) | 18.42 | 0.0 | 170 / 367 | 3.23 | 1.25 | nan |
| native, full known, weighted, src5 | 5.24 (0) | 5.28 (0) | 2.96 (0) | 1.10 (0) | 20.28 | 0.0 | 170 / 367 | 2.88 | 2.36 | nan |
| anchored, stratified, src5 | 4.67 (0) | 4.70 (0) | 7.43 (0) | 6.55 (0) | 15.57 | 0.0 | 170 / 367 | 7.32 | -2.65 | nan |

## alpha = 0.05, dataset split

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 1283 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 6.97 (99) | 7.03 (99) | 4.46 (24) | 1.59 (0) | 13.05 | 0.0 | 170 / 367 | 4.42 | 2.54 | 28.07 |
| anchored, image-level (paper) | 15.61 (100) | 15.68 (100) | 10.09 (100) | 4.92 (45) | 5.78 | 0.0 | 170 / 367 | 10.03 | 5.58 | 28.07 |
| anchored, both | 6.97 (99) | 7.03 (99) | 4.46 (24) | 1.59 (0) | 13.05 | 0.0 | 170 / 367 | 4.42 | 2.54 | 28.07 |
| native, full known, label-level | 8.82 (100) | 8.90 (100) | 4.47 (27) | 1.72 (0) | 11.41 | 0.0 | 170 / 367 | 4.43 | 4.39 | 31.19 |
| native, frozen at source, label-level | 12.34 (100) | 12.42 (100) | 6.55 (96) | 2.77 (0) | 7.75 | 0.0 | 170 / 367 | 4.42 | 7.92 | 38.51 |
| native, frozen at source, image-level | 24.45 (100) | 24.51 (100) | 13.10 (100) | 6.80 (100) | 3.65 | 0.0 | 170 / 367 | 10.09 | 14.36 | 38.51 |
| anchored, weighted, all2 | 0.62 (0) | 0.60 (0) | 0.53 (0) | 0.27 (0) | 683.74 | 37.3 | 170 / 367 | 0.52 | 0.10 | nan |
| native, full known, weighted, all2 | 1.16 (0) | 1.14 (0) | 0.86 (0) | 0.37 (0) | 682.05 | 18.9 | 170 / 367 | 0.85 | 0.31 | nan |
| anchored, stratified, all2 | 3.16 (0) | 3.13 (0) | 4.21 (14) | 2.30 (0) | 650.42 | 37.3 | 170 / 367 | 4.18 | -1.02 | nan |
| anchored, weighted, all3 | 0.78 (0) | 0.76 (0) | 0.78 (0) | 0.34 (0) | 478.01 | 17.2 | 170 / 367 | 0.74 | 0.03 | nan |
| native, full known, weighted, all3 | 0.80 (0) | 0.79 (0) | 0.81 (0) | 0.33 (0) | 801.24 | 31.2 | 170 / 367 | 0.75 | 0.05 | nan |
| anchored, stratified, all3 | 2.09 (0) | 2.05 (0) | 3.93 (5) | 2.32 (0) | 863.54 | 60.4 | 170 / 367 | 3.89 | -1.80 | nan |
| anchored, weighted, all5 | 0.63 (0) | 0.62 (0) | 0.55 (0) | 0.26 (0) | 338.11 | 6.0 | 170 / 367 | 0.51 | 0.11 | nan |
| native, full known, weighted, all5 | 0.74 (0) | 0.76 (0) | 0.75 (0) | 0.32 (0) | 850.09 | 31.3 | 170 / 367 | 0.67 | 0.07 | nan |
| anchored, stratified, all5 | 0.99 (0) | 0.97 (0) | 3.50 (1) | 2.48 (0) | 787.67 | 50.4 | 170 / 367 | 3.42 | -2.43 | nan |
| anchored, weighted, src2 | 3.60 (10) | 3.66 (11) | 2.50 (0) | 0.88 (0) | 22.41 | 0.0 | 170 / 367 | 2.44 | 1.16 | nan |
| native, full known, weighted, src2 | 4.59 (31) | 4.65 (35) | 2.25 (0) | 0.75 (0) | 24.08 | 0.0 | 170 / 367 | 2.17 | 2.42 | nan |
| anchored, stratified, src2 | 3.64 (10) | 3.69 (9) | 3.96 (10) | 2.85 (0) | 19.66 | 0.0 | 170 / 367 | 3.87 | -0.23 | nan |
| anchored, weighted, src3 | 2.46 (0) | 2.49 (1) | 1.91 (0) | 0.67 (0) | 31.12 | 0.0 | 170 / 367 | 1.84 | 0.62 | nan |
| native, full known, weighted, src3 | 3.25 (4) | 3.30 (3) | 1.58 (0) | 0.52 (0) | 43.91 | 0.0 | 170 / 367 | 1.48 | 1.76 | nan |
| anchored, stratified, src3 | 2.54 (0) | 2.55 (0) | 3.41 (1) | 2.72 (0) | 28.13 | 0.0 | 170 / 367 | 3.31 | -0.76 | nan |
| anchored, weighted, src5 | 1.43 (0) | 1.45 (0) | 1.25 (0) | 0.46 (0) | 50.27 | 0.0 | 170 / 367 | 1.13 | 0.30 | nan |
| native, full known, weighted, src5 | 1.60 (0) | 1.62 (0) | 1.05 (0) | 0.39 (0) | 393.44 | 0.0 | 170 / 367 | 0.87 | 0.73 | nan |
| anchored, stratified, src5 | 1.51 (0) | 1.51 (0) | 2.39 (0) | 1.97 (0) | 49.45 | 0.0 | 170 / 367 | 2.19 | -0.68 | nan |
