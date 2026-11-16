# A guarantee for the added labels under (weighted) label exchangeability

CAT-Seg (sed_bank683), 2000 COCO val2017 (LVIS-annotated) images with a labelled sampled pixel (1283-name vocabulary: 171 source names, then the LVIS v1 annotation mapped to the added names), 500 trials (random half/half image split; source vocabulary as per design). Label loss = pooled fraction of the label's sampled pixels whose score for it is below the threshold. "Added, cal" = mean over added labels present in the calibration images (the quantity the proposition bounds); "added, held-out" = same on the held-out images; "src, class" = class-averaged source loss on held-out images; "src, image" = image-level source risk (the paper's guarantee); size = labels per labelled pixel at 1283 names, held-out images; floor = % of added labels present whose threshold is the grid floor. Risks in % (and % of trials above alpha). Development data; nothing fitted.

## alpha = 0.1, exchangeable

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 1283 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 9.03 (34) | 9.07 (36) | 9.08 (36) | 3.62 (0) | 21.24 | 0.0 | 72 / 466 | 8.63 | 0.39 | 4.03 |
| anchored, image-level (paper) | 20.44 (99) | 20.52 (100) | 20.62 (99) | 9.91 (47) | 7.68 | 0.0 | 72 / 466 | 20.45 | -0.00 | 4.03 |
| anchored, both | 9.03 (34) | 9.07 (36) | 9.08 (36) | 3.62 (0) | 21.24 | 0.0 | 72 / 466 | 8.63 | 0.39 | 4.03 |
| native, full known, label-level | 9.09 (35) | 9.10 (37) | 9.16 (36) | 3.33 (0) | 23.91 | 0.0 | 72 / 466 | 8.64 | 0.46 | 4.07 |
| anchored, weighted, all2 | 9.05 (35) | 9.10 (36) | 9.15 (38) | 3.64 (0) | 21.03 | 0.0 | 72 / 466 | 8.68 | 0.37 | nan |
| native, full known, weighted, all2 | 9.11 (37) | 9.12 (36) | 9.22 (39) | 3.35 (0) | 23.82 | 0.0 | 72 / 466 | 8.66 | 0.45 | nan |
| anchored, stratified, all2 | 8.09 (20) | 8.17 (19) | 7.94 (21) | 7.00 (17) | 50.81 | 0.0 | 72 / 466 | 7.22 | 0.87 | nan |
| anchored, weighted, all3 | 9.02 (36) | 9.06 (34) | 9.12 (38) | 3.63 (0) | 21.18 | 0.0 | 72 / 466 | 8.67 | 0.35 | nan |
| native, full known, weighted, all3 | 9.12 (36) | 9.14 (37) | 9.24 (39) | 3.36 (0) | 23.75 | 0.0 | 72 / 466 | 8.69 | 0.43 | nan |
| anchored, stratified, all3 | 7.19 (11) | 7.24 (11) | 7.06 (13) | 7.63 (22) | 189.67 | 4.4 | 72 / 466 | 6.11 | 1.08 | nan |
| anchored, weighted, all5 | 8.99 (34) | 9.03 (35) | 9.13 (38) | 3.62 (0) | 21.32 | 0.0 | 72 / 466 | 8.67 | 0.32 | nan |
| native, full known, weighted, all5 | 9.12 (36) | 9.12 (36) | 9.26 (38) | 3.37 (0) | 23.81 | 0.0 | 72 / 466 | 8.71 | 0.42 | nan |
| anchored, stratified, all5 | 5.33 (1) | 5.35 (1) | 5.21 (2) | 8.01 (25) | 413.62 | 12.5 | 72 / 466 | 4.28 | 1.05 | nan |
| anchored, weighted, src2 | 8.98 (33) | 9.03 (34) | 9.08 (37) | 3.61 (0) | 21.26 | 0.0 | 72 / 466 | 8.60 | 0.38 | nan |
| native, full known, weighted, src2 | 9.06 (35) | 9.07 (36) | 9.15 (37) | 3.34 (0) | 23.93 | 0.0 | 72 / 466 | 8.62 | 0.43 | nan |
| anchored, stratified, src2 | 7.97 (18) | 8.04 (19) | 7.90 (21) | 6.90 (16) | 50.30 | 0.0 | 72 / 466 | 7.22 | 0.75 | nan |
| anchored, weighted, src3 | 8.99 (35) | 9.03 (34) | 9.09 (38) | 3.62 (0) | 21.36 | 0.0 | 72 / 466 | 8.64 | 0.34 | nan |
| native, full known, weighted, src3 | 9.05 (36) | 9.07 (36) | 9.16 (37) | 3.33 (0) | 23.98 | 0.0 | 72 / 466 | 8.63 | 0.42 | nan |
| anchored, stratified, src3 | 7.15 (11) | 7.16 (12) | 7.03 (12) | 7.56 (21) | 188.23 | 4.2 | 72 / 466 | 6.10 | 1.05 | nan |
| anchored, weighted, src5 | 8.89 (33) | 8.93 (34) | 9.01 (37) | 3.59 (0) | 21.55 | 0.0 | 72 / 466 | 8.57 | 0.32 | nan |
| native, full known, weighted, src5 | 9.00 (35) | 9.02 (36) | 9.16 (37) | 3.33 (0) | 24.13 | 0.0 | 72 / 466 | 8.60 | 0.40 | nan |
| anchored, stratified, src5 | 5.36 (0) | 5.38 (1) | 5.20 (3) | 7.82 (23) | 406.63 | 11.7 | 72 / 466 | 4.31 | 1.05 | nan |

## alpha = 0.05, exchangeable

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 1283 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 4.04 (27) | 4.08 (29) | 3.95 (31) | 1.29 (0) | 60.08 | 0.0 | 72 / 466 | 3.53 | 0.51 | 4.03 |
| anchored, image-level (paper) | 12.42 (100) | 12.51 (99) | 12.51 (97) | 4.87 (43) | 14.77 | 0.0 | 72 / 466 | 12.42 | -0.00 | 4.03 |
| anchored, both | 4.04 (27) | 4.08 (29) | 3.95 (31) | 1.29 (0) | 60.08 | 0.0 | 72 / 466 | 3.53 | 0.51 | 4.03 |
| native, full known, label-level | 4.05 (28) | 4.10 (29) | 3.98 (31) | 1.17 (0) | 66.58 | 0.0 | 72 / 466 | 3.54 | 0.52 | 4.07 |
| anchored, weighted, all2 | 4.05 (27) | 4.08 (30) | 4.01 (31) | 1.29 (0) | 59.90 | 0.0 | 72 / 466 | 3.55 | 0.49 | nan |
| native, full known, weighted, all2 | 4.06 (29) | 4.07 (30) | 4.03 (31) | 1.18 (0) | 66.34 | 0.0 | 72 / 466 | 3.55 | 0.51 | nan |
| anchored, stratified, all2 | 2.94 (8) | 2.98 (9) | 2.76 (9) | 2.54 (7) | 310.58 | 8.2 | 72 / 466 | 2.32 | 0.63 | nan |
| anchored, weighted, all3 | 4.06 (28) | 4.09 (29) | 4.02 (32) | 1.30 (0) | 59.87 | 0.0 | 72 / 466 | 3.55 | 0.51 | nan |
| native, full known, weighted, all3 | 4.10 (29) | 4.12 (30) | 4.06 (31) | 1.18 (0) | 65.91 | 0.0 | 72 / 466 | 3.58 | 0.52 | nan |
| anchored, stratified, all3 | 2.15 (1) | 2.18 (1) | 2.03 (3) | 2.38 (7) | 529.89 | 17.0 | 72 / 466 | 1.56 | 0.59 | nan |
| anchored, weighted, all5 | 4.03 (28) | 4.07 (30) | 4.03 (31) | 1.30 (0) | 60.63 | 0.0 | 72 / 466 | 3.55 | 0.48 | nan |
| native, full known, weighted, all5 | 4.07 (28) | 4.09 (30) | 4.06 (31) | 1.19 (0) | 66.87 | 0.0 | 72 / 466 | 3.58 | 0.48 | nan |
| anchored, stratified, all5 | 0.73 (0) | 0.73 (0) | 0.68 (0) | 1.53 (2) | 954.08 | 54.6 | 72 / 466 | 0.51 | 0.22 | nan |
| anchored, weighted, src2 | 4.02 (27) | 4.05 (28) | 3.97 (31) | 1.29 (0) | 60.01 | 0.0 | 72 / 466 | 3.52 | 0.50 | nan |
| native, full known, weighted, src2 | 4.04 (28) | 4.06 (28) | 4.01 (31) | 1.17 (0) | 66.51 | 0.0 | 72 / 466 | 3.54 | 0.50 | nan |
| anchored, stratified, src2 | 2.92 (6) | 2.96 (8) | 2.85 (9) | 2.48 (6) | 302.53 | 7.8 | 72 / 466 | 2.33 | 0.60 | nan |
| anchored, weighted, src3 | 4.04 (28) | 4.07 (29) | 3.99 (30) | 1.30 (0) | 60.10 | 0.0 | 72 / 466 | 3.53 | 0.50 | nan |
| native, full known, weighted, src3 | 4.06 (28) | 4.08 (29) | 4.01 (31) | 1.18 (0) | 66.83 | 0.0 | 72 / 466 | 3.52 | 0.54 | nan |
| anchored, stratified, src3 | 2.16 (1) | 2.21 (1) | 2.03 (3) | 2.40 (7) | 514.43 | 15.8 | 72 / 466 | 1.56 | 0.60 | nan |
| anchored, weighted, src5 | 3.98 (27) | 4.00 (29) | 3.97 (31) | 1.29 (0) | 61.66 | 0.0 | 72 / 466 | 3.50 | 0.48 | nan |
| native, full known, weighted, src5 | 4.01 (28) | 4.03 (27) | 4.01 (31) | 1.18 (0) | 67.55 | 0.0 | 72 / 466 | 3.52 | 0.50 | nan |
| anchored, stratified, src5 | 0.74 (0) | 0.75 (0) | 0.68 (0) | 1.65 (2) | 951.98 | 53.6 | 72 / 466 | 0.50 | 0.24 | nan |

## alpha = 0.1, dataset split

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 1283 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 24.31 (100) | 24.49 (100) | 9.47 (29) | 4.03 (0) | 7.24 | 0.0 | 170 / 367 | 9.44 | 14.88 | 30.01 |
| anchored, image-level (paper) | 40.03 (100) | 40.13 (100) | 18.63 (100) | 9.89 (42) | 3.60 | 0.0 | 170 / 367 | 18.65 | 21.38 | 30.01 |
| anchored, both | 24.31 (100) | 24.49 (100) | 9.47 (29) | 4.03 (0) | 7.24 | 0.0 | 170 / 367 | 9.44 | 14.88 | 30.01 |
| native, full known, label-level | 25.68 (100) | 25.85 (100) | 9.48 (29) | 4.08 (0) | 7.55 | 0.0 | 170 / 367 | 9.44 | 16.24 | 37.85 |
| native, frozen at source, label-level | 14.68 (100) | 14.78 (100) | 4.02 (0) | 1.40 (0) | 16.35 | 0.0 | 170 / 367 | 9.44 | 5.24 | 9.15 |
| native, frozen at source, image-level | 24.00 (100) | 24.15 (100) | 8.61 (2) | 3.63 (0) | 8.25 | 0.0 | 170 / 367 | 17.90 | 6.10 | 9.15 |
| anchored, weighted, all2 | 2.30 (0) | 2.34 (0) | 2.50 (0) | 0.93 (0) | 668.85 | 40.9 | 170 / 367 | 2.50 | -0.20 | nan |
| native, full known, weighted, all2 | 9.54 (51) | 9.63 (53) | 10.80 (62) | 4.96 (0) | 651.21 | 42.1 | 170 / 367 | 10.76 | -1.22 | nan |
| anchored, stratified, all2 | 8.26 (4) | 8.34 (5) | 9.20 (21) | 4.47 (0) | 648.21 | 40.9 | 170 / 367 | 9.18 | -0.92 | nan |
| anchored, weighted, all3 | 2.78 (0) | 2.82 (0) | 1.82 (0) | 0.68 (0) | 475.13 | 19.6 | 170 / 367 | 1.81 | 0.97 | nan |
| native, full known, weighted, all3 | 12.51 (75) | 12.65 (79) | 9.64 (47) | 4.34 (0) | 435.95 | 21.8 | 170 / 367 | 9.64 | 2.87 | nan |
| anchored, stratified, all3 | 5.44 (1) | 5.47 (1) | 8.89 (14) | 4.74 (0) | 450.05 | 19.6 | 170 / 367 | 8.76 | -3.32 | nan |
| anchored, weighted, all5 | 1.97 (0) | 1.98 (0) | 1.44 (0) | 0.52 (0) | 556.77 | 27.4 | 170 / 367 | 1.43 | 0.54 | nan |
| native, full known, weighted, all5 | 9.96 (46) | 10.05 (47) | 9.51 (42) | 4.26 (0) | 521.93 | 28.6 | 170 / 367 | 9.47 | 0.49 | nan |
| anchored, stratified, all5 | 3.26 (0) | 3.29 (0) | 8.38 (3) | 5.64 (0) | 777.33 | 55.9 | 170 / 367 | 8.36 | -5.10 | nan |
| anchored, weighted, src2 | 17.81 (100) | 17.97 (100) | 6.15 (0) | 2.44 (0) | 10.88 | 0.0 | 170 / 367 | 6.15 | 11.66 | nan |
| native, full known, weighted, src2 | 21.06 (100) | 21.20 (100) | 7.24 (1) | 3.09 (0) | 9.45 | 0.0 | 170 / 367 | 7.21 | 13.85 | nan |
| anchored, stratified, src2 | 17.49 (100) | 17.64 (100) | 8.91 (12) | 5.90 (0) | 8.70 | 0.0 | 170 / 367 | 8.91 | 8.58 | nan |
| anchored, weighted, src3 | 15.06 (100) | 15.20 (100) | 5.18 (0) | 2.01 (0) | 13.06 | 0.0 | 170 / 367 | 5.17 | 9.88 | nan |
| native, full known, weighted, src3 | 16.73 (100) | 16.84 (100) | 5.37 (0) | 2.21 (0) | 12.70 | 0.0 | 170 / 367 | 5.38 | 11.35 | nan |
| anchored, stratified, src3 | 14.58 (99) | 14.72 (100) | 8.40 (5) | 6.51 (0) | 10.23 | 0.0 | 170 / 367 | 8.38 | 6.20 | nan |
| anchored, weighted, src5 | 12.41 (83) | 12.54 (82) | 4.58 (0) | 1.75 (0) | 16.09 | 0.0 | 170 / 367 | 4.56 | 7.85 | nan |
| native, full known, weighted, src5 | 12.19 (85) | 12.33 (85) | 3.78 (0) | 1.46 (0) | 18.53 | 0.0 | 170 / 367 | 3.77 | 8.42 | nan |
| anchored, stratified, src5 | 11.29 (66) | 11.44 (64) | 7.42 (0) | 5.81 (0) | 14.25 | 0.0 | 170 / 367 | 7.32 | 3.97 | nan |

## alpha = 0.05, dataset split

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 1283 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 14.17 (100) | 14.30 (100) | 4.45 (24) | 1.55 (0) | 14.85 | 0.0 | 170 / 367 | 4.43 | 9.75 | 30.01 |
| anchored, image-level (paper) | 27.15 (100) | 27.31 (100) | 10.97 (100) | 4.91 (41) | 6.27 | 0.0 | 170 / 367 | 10.98 | 16.17 | 30.01 |
| anchored, both | 14.17 (100) | 14.30 (100) | 4.45 (24) | 1.55 (0) | 14.85 | 0.0 | 170 / 367 | 4.43 | 9.75 | 30.01 |
| native, full known, label-level | 15.81 (100) | 15.90 (100) | 4.44 (25) | 1.60 (0) | 14.95 | 0.0 | 170 / 367 | 4.43 | 11.38 | 37.85 |
| native, frozen at source, label-level | 8.76 (100) | 8.85 (100) | 2.04 (0) | 0.61 (0) | 31.58 | 0.0 | 170 / 367 | 4.42 | 4.34 | 9.15 |
| native, frozen at source, image-level | 16.01 (100) | 16.10 (100) | 4.47 (17) | 1.62 (0) | 14.72 | 0.0 | 170 / 367 | 10.44 | 5.57 | 9.15 |
| anchored, weighted, all2 | 1.09 (0) | 1.11 (0) | 1.20 (0) | 0.41 (0) | 703.12 | 40.9 | 170 / 367 | 1.21 | -0.12 | nan |
| native, full known, weighted, all2 | 5.64 (76) | 5.74 (77) | 6.41 (81) | 2.64 (0) | 662.46 | 42.1 | 170 / 367 | 6.37 | -0.73 | nan |
| anchored, stratified, all2 | 3.89 (4) | 3.96 (7) | 4.32 (18) | 1.73 (0) | 653.88 | 40.9 | 170 / 367 | 4.30 | -0.40 | nan |
| anchored, weighted, all3 | 1.26 (0) | 1.29 (0) | 0.84 (0) | 0.30 (0) | 515.60 | 19.6 | 170 / 367 | 0.80 | 0.45 | nan |
| native, full known, weighted, all3 | 4.85 (40) | 4.92 (40) | 4.99 (53) | 2.01 (0) | 454.23 | 21.8 | 170 / 367 | 4.89 | -0.04 | nan |
| anchored, stratified, all3 | 1.88 (0) | 1.91 (0) | 4.04 (10) | 1.86 (0) | 866.16 | 65.4 | 170 / 367 | 4.01 | -2.13 | nan |
| anchored, weighted, all5 | 0.86 (0) | 0.88 (0) | 0.71 (0) | 0.26 (0) | 594.29 | 27.4 | 170 / 367 | 0.68 | 0.18 | nan |
| native, full known, weighted, all5 | 3.27 (19) | 3.32 (19) | 4.38 (35) | 1.73 (0) | 581.04 | 29.9 | 170 / 367 | 4.36 | -1.10 | nan |
| anchored, stratified, all5 | 1.39 (0) | 1.39 (0) | 3.65 (2) | 2.18 (0) | 787.39 | 55.9 | 170 / 367 | 3.59 | -2.20 | nan |
| anchored, weighted, src2 | 9.07 (100) | 9.16 (100) | 2.61 (1) | 0.88 (0) | 24.94 | 0.0 | 170 / 367 | 2.57 | 6.50 | nan |
| native, full known, weighted, src2 | 11.21 (100) | 11.33 (100) | 3.08 (3) | 1.12 (0) | 21.51 | 0.0 | 170 / 367 | 3.06 | 8.15 | nan |
| anchored, stratified, src2 | 8.85 (100) | 8.96 (100) | 3.91 (7) | 2.25 (0) | 21.76 | 0.0 | 170 / 367 | 3.87 | 4.99 | nan |
| anchored, weighted, src3 | 7.34 (94) | 7.44 (94) | 2.10 (0) | 0.73 (0) | 32.22 | 0.0 | 170 / 367 | 2.06 | 5.28 | nan |
| native, full known, weighted, src3 | 7.97 (95) | 8.05 (97) | 2.11 (0) | 0.75 (0) | 32.99 | 0.0 | 170 / 367 | 2.03 | 5.94 | nan |
| anchored, stratified, src3 | 6.98 (90) | 7.08 (92) | 3.40 (2) | 2.49 (0) | 28.86 | 0.0 | 170 / 367 | 3.31 | 3.67 | nan |
| anchored, weighted, src5 | 4.93 (52) | 4.99 (53) | 1.68 (0) | 0.61 (0) | 53.84 | 0.0 | 170 / 367 | 1.60 | 3.33 | nan |
| native, full known, weighted, src5 | 5.04 (42) | 5.13 (43) | 1.47 (0) | 0.53 (0) | 53.68 | 0.0 | 170 / 367 | 1.34 | 3.71 | nan |
| anchored, stratified, src5 | 4.01 (32) | 4.06 (34) | 2.40 (0) | 1.76 (0) | 62.07 | 0.0 | 170 / 367 | 2.19 | 1.82 | nan |
