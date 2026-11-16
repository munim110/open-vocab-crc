# A guarantee for the added labels under (weighted) label exchangeability

CAT-Seg (vitl_bank683), 2000 COCO val2017 (LVIS-annotated) images with a labelled sampled pixel (1283-name vocabulary: 171 source names, then the LVIS v1 annotation mapped to the added names), 500 trials (random half/half image split; source vocabulary as per design). Label loss = pooled fraction of the label's sampled pixels whose score for it is below the threshold. "Added, cal" = mean over added labels present in the calibration images (the quantity the proposition bounds); "added, held-out" = same on the held-out images; "src, class" = class-averaged source loss on held-out images; "src, image" = image-level source risk (the paper's guarantee); size = labels per labelled pixel at 1283 names, held-out images; floor = % of added labels present whose threshold is the grid floor. Risks in % (and % of trials above alpha). Development data; nothing fitted.

## alpha = 0.1, exchangeable

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 1283 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 8.93 (33) | 9.02 (34) | 8.93 (35) | 4.46 (2) | 11.93 | 0.0 | 72 / 466 | 8.62 | 0.31 | 3.86 |
| anchored, image-level (paper) | 17.74 (98) | 17.78 (97) | 17.86 (97) | 9.87 (46) | 5.71 | 0.0 | 72 / 466 | 17.75 | -0.01 | 3.86 |
| anchored, both | 8.91 (33) | 8.99 (34) | 8.91 (35) | 4.44 (2) | 11.94 | 0.0 | 72 / 466 | 8.61 | 0.31 | 3.86 |
| native, full known, label-level | 8.97 (33) | 9.03 (35) | 8.98 (38) | 4.04 (2) | 13.59 | 0.0 | 72 / 466 | 8.63 | 0.34 | 4.12 |
| anchored, weighted, all2 | 8.97 (33) | 9.03 (34) | 8.98 (36) | 4.49 (2) | 11.86 | 0.0 | 72 / 466 | 8.68 | 0.29 | nan |
| native, full known, weighted, all2 | 8.96 (36) | 9.02 (34) | 8.99 (38) | 4.04 (2) | 13.57 | 0.0 | 72 / 466 | 8.66 | 0.30 | nan |
| anchored, stratified, all2 | 8.08 (21) | 8.13 (19) | 8.06 (21) | 6.92 (15) | 26.68 | 0.0 | 72 / 466 | 7.27 | 0.82 | nan |
| anchored, weighted, all3 | 8.95 (32) | 9.02 (33) | 8.97 (36) | 4.47 (2) | 11.88 | 0.0 | 72 / 466 | 8.69 | 0.26 | nan |
| native, full known, weighted, all3 | 8.98 (34) | 9.04 (35) | 9.06 (39) | 4.08 (2) | 13.51 | 0.0 | 72 / 466 | 8.70 | 0.28 | nan |
| anchored, stratified, all3 | 7.06 (6) | 7.14 (9) | 6.90 (11) | 7.45 (18) | 198.47 | 5.2 | 72 / 466 | 6.16 | 0.90 | nan |
| anchored, weighted, all5 | 8.95 (33) | 9.01 (33) | 8.97 (37) | 4.49 (2) | 11.88 | 0.0 | 72 / 466 | 8.72 | 0.23 | nan |
| native, full known, weighted, all5 | 8.95 (33) | 9.01 (34) | 9.02 (38) | 4.08 (2) | 13.56 | 0.0 | 72 / 466 | 8.70 | 0.25 | nan |
| anchored, stratified, all5 | 5.50 (1) | 5.55 (1) | 5.26 (1) | 6.91 (14) | 383.97 | 10.5 | 72 / 466 | 4.42 | 1.08 | nan |
| anchored, weighted, src2 | 8.94 (32) | 9.00 (33) | 8.93 (36) | 4.47 (2) | 11.91 | 0.0 | 72 / 466 | 8.65 | 0.29 | nan |
| native, full known, weighted, src2 | 8.92 (34) | 8.98 (34) | 8.95 (38) | 4.03 (2) | 13.65 | 0.0 | 72 / 466 | 8.62 | 0.30 | nan |
| anchored, stratified, src2 | 8.00 (21) | 8.05 (20) | 8.00 (20) | 6.89 (15) | 28.04 | 0.0 | 72 / 466 | 7.26 | 0.74 | nan |
| anchored, weighted, src3 | 8.91 (31) | 8.98 (32) | 8.91 (35) | 4.46 (2) | 11.92 | 0.0 | 72 / 466 | 8.64 | 0.27 | nan |
| native, full known, weighted, src3 | 8.90 (34) | 8.96 (34) | 8.97 (38) | 4.04 (2) | 13.63 | 0.0 | 72 / 466 | 8.60 | 0.30 | nan |
| anchored, stratified, src3 | 7.01 (7) | 7.11 (8) | 6.80 (10) | 7.46 (18) | 197.36 | 5.1 | 72 / 466 | 6.17 | 0.84 | nan |
| anchored, weighted, src5 | 8.85 (31) | 8.91 (32) | 8.89 (35) | 4.45 (2) | 12.00 | 0.0 | 72 / 466 | 8.61 | 0.24 | nan |
| native, full known, weighted, src5 | 8.88 (33) | 8.93 (32) | 8.98 (38) | 4.05 (2) | 13.72 | 0.0 | 72 / 466 | 8.62 | 0.26 | nan |
| anchored, stratified, src5 | 5.52 (1) | 5.59 (1) | 5.34 (2) | 6.97 (15) | 379.40 | 9.9 | 72 / 466 | 4.41 | 1.11 | nan |

## alpha = 0.05, exchangeable

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 1283 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 4.01 (27) | 4.06 (28) | 3.96 (30) | 1.71 (1) | 30.23 | 0.0 | 72 / 466 | 3.56 | 0.45 | 3.86 |
| anchored, image-level (paper) | 10.34 (98) | 10.38 (97) | 10.39 (94) | 4.81 (42) | 10.43 | 0.0 | 72 / 466 | 10.35 | -0.01 | 3.86 |
| anchored, both | 4.00 (27) | 4.05 (28) | 3.95 (30) | 1.71 (1) | 30.25 | 0.0 | 72 / 466 | 3.55 | 0.45 | 3.86 |
| native, full known, label-level | 4.05 (28) | 4.15 (31) | 4.02 (31) | 1.42 (1) | 42.13 | 0.0 | 72 / 466 | 3.56 | 0.49 | 4.12 |
| anchored, weighted, all2 | 4.02 (28) | 4.06 (28) | 3.98 (31) | 1.72 (1) | 30.49 | 0.0 | 72 / 466 | 3.60 | 0.42 | nan |
| native, full known, weighted, all2 | 4.03 (27) | 4.13 (32) | 4.02 (32) | 1.41 (1) | 44.26 | 0.0 | 72 / 466 | 3.57 | 0.47 | nan |
| anchored, stratified, all2 | 2.85 (6) | 2.90 (6) | 2.82 (10) | 2.63 (7) | 334.84 | 11.7 | 72 / 466 | 2.36 | 0.49 | nan |
| anchored, weighted, all3 | 4.01 (27) | 4.06 (28) | 3.98 (30) | 1.72 (1) | 30.30 | 0.0 | 72 / 466 | 3.61 | 0.40 | nan |
| native, full known, weighted, all3 | 4.04 (28) | 4.15 (31) | 4.05 (32) | 1.42 (1) | 43.50 | 0.0 | 72 / 466 | 3.59 | 0.45 | nan |
| anchored, stratified, all3 | 2.23 (1) | 2.28 (2) | 2.16 (5) | 2.52 (4) | 509.82 | 16.2 | 72 / 466 | 1.62 | 0.61 | nan |
| anchored, weighted, all5 | 4.00 (28) | 4.05 (29) | 4.00 (30) | 1.72 (1) | 30.66 | 0.0 | 72 / 466 | 3.62 | 0.39 | nan |
| native, full known, weighted, all5 | 4.02 (28) | 4.13 (31) | 4.06 (31) | 1.43 (1) | 43.01 | 0.0 | 72 / 466 | 3.61 | 0.40 | nan |
| anchored, stratified, all5 | 0.72 (0) | 0.73 (0) | 0.73 (0) | 1.38 (0) | 920.41 | 51.0 | 72 / 466 | 0.57 | 0.15 | nan |
| anchored, weighted, src2 | 3.99 (27) | 4.03 (28) | 3.95 (30) | 1.71 (1) | 30.63 | 0.0 | 72 / 466 | 3.57 | 0.42 | nan |
| native, full known, weighted, src2 | 4.02 (27) | 4.12 (31) | 4.01 (32) | 1.41 (1) | 44.44 | 0.0 | 72 / 466 | 3.54 | 0.48 | nan |
| anchored, stratified, src2 | 2.88 (6) | 2.93 (7) | 2.81 (10) | 2.62 (7) | 325.28 | 11.1 | 72 / 466 | 2.35 | 0.52 | nan |
| anchored, weighted, src3 | 3.99 (28) | 4.04 (28) | 3.97 (30) | 1.72 (1) | 30.52 | 0.0 | 72 / 466 | 3.58 | 0.42 | nan |
| native, full known, weighted, src3 | 4.01 (28) | 4.12 (30) | 4.03 (32) | 1.42 (1) | 42.15 | 0.0 | 72 / 466 | 3.56 | 0.45 | nan |
| anchored, stratified, src3 | 2.27 (2) | 2.33 (2) | 2.14 (4) | 2.54 (6) | 509.27 | 16.0 | 72 / 466 | 1.63 | 0.64 | nan |
| anchored, weighted, src5 | 3.94 (27) | 4.00 (28) | 3.95 (31) | 1.71 (2) | 30.83 | 0.0 | 72 / 466 | 3.55 | 0.40 | nan |
| native, full known, weighted, src5 | 3.99 (28) | 4.11 (30) | 4.04 (31) | 1.42 (1) | 43.89 | 0.0 | 72 / 466 | 3.57 | 0.42 | nan |
| anchored, stratified, src5 | 0.76 (0) | 0.77 (0) | 0.74 (0) | 1.54 (1) | 921.36 | 50.0 | 72 / 466 | 0.57 | 0.19 | nan |

## alpha = 0.1, dataset split

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 1283 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 17.60 (100) | 17.67 (100) | 9.50 (31) | 4.48 (0) | 6.29 | 0.0 | 170 / 367 | 9.44 | 8.16 | 29.71 |
| anchored, image-level (paper) | 32.14 (100) | 31.99 (100) | 17.96 (100) | 9.87 (42) | 3.27 | 0.0 | 170 / 367 | 17.96 | 14.19 | 29.71 |
| anchored, both | 17.60 (100) | 17.67 (100) | 9.50 (31) | 4.48 (0) | 6.29 | 0.0 | 170 / 367 | 9.44 | 8.16 | 29.71 |
| native, full known, label-level | 21.23 (100) | 21.29 (100) | 9.51 (32) | 4.28 (0) | 5.59 | 0.0 | 170 / 367 | 9.44 | 11.79 | 31.14 |
| native, frozen at source, label-level | 29.18 (100) | 29.15 (100) | 13.36 (100) | 6.37 (0) | 3.93 | 0.0 | 170 / 367 | 9.44 | 19.74 | 39.38 |
| native, frozen at source, image-level | 47.32 (100) | 47.13 (100) | 23.17 (100) | 12.81 (100) | 2.14 | 0.0 | 170 / 367 | 18.05 | 29.27 | 39.38 |
| anchored, weighted, all2 | 2.73 (0) | 2.79 (0) | 1.83 (0) | 0.73 (0) | 54.88 | 0.0 | 170 / 367 | 1.70 | 1.03 | nan |
| native, full known, weighted, all2 | 6.89 (9) | 6.96 (8) | 2.80 (0) | 1.10 (0) | 23.90 | 0.0 | 170 / 367 | 2.70 | 4.19 | nan |
| anchored, stratified, all2 | 8.55 (6) | 8.54 (5) | 9.07 (19) | 5.41 (0) | 646.91 | 37.0 | 170 / 367 | 9.01 | -0.46 | nan |
| anchored, weighted, all3 | 3.94 (0) | 4.00 (0) | 2.34 (0) | 0.94 (0) | 33.98 | 0.0 | 170 / 367 | 2.25 | 1.69 | nan |
| native, full known, weighted, all3 | 7.19 (7) | 7.24 (8) | 3.53 (0) | 1.37 (0) | 38.57 | 0.0 | 170 / 367 | 3.44 | 3.75 | nan |
| anchored, stratified, all3 | 6.47 (0) | 6.49 (0) | 8.77 (9) | 5.69 (0) | 439.68 | 17.3 | 170 / 367 | 8.59 | -2.12 | nan |
| anchored, weighted, all5 | 3.03 (0) | 3.03 (0) | 2.86 (0) | 1.15 (0) | 277.50 | 19.4 | 170 / 367 | 2.80 | 0.23 | nan |
| native, full known, weighted, all5 | 6.09 (0) | 6.13 (0) | 4.29 (0) | 1.62 (0) | 374.22 | 14.0 | 170 / 367 | 4.22 | 1.87 | nan |
| anchored, stratified, all5 | 3.01 (0) | 2.99 (0) | 8.19 (2) | 6.04 (0) | 776.40 | 51.1 | 170 / 367 | 8.13 | -5.12 | nan |
| anchored, weighted, src2 | 11.68 (87) | 11.75 (88) | 6.04 (0) | 2.68 (0) | 9.69 | 0.0 | 170 / 367 | 5.99 | 5.69 | nan |
| native, full known, weighted, src2 | 12.60 (98) | 12.68 (98) | 5.22 (0) | 2.09 (0) | 10.08 | 0.0 | 170 / 367 | 5.19 | 7.42 | nan |
| anchored, stratified, src2 | 11.85 (89) | 11.94 (90) | 8.95 (13) | 6.85 (0) | 7.77 | 0.0 | 170 / 367 | 8.91 | 2.94 | nan |
| anchored, weighted, src3 | 8.91 (22) | 8.99 (23) | 4.73 (0) | 1.94 (0) | 12.68 | 0.0 | 170 / 367 | 4.69 | 4.22 | nan |
| native, full known, weighted, src3 | 9.92 (47) | 10.03 (50) | 3.97 (0) | 1.52 (0) | 13.48 | 0.0 | 170 / 367 | 3.90 | 6.02 | nan |
| anchored, stratified, src3 | 9.19 (27) | 9.24 (27) | 8.44 (5) | 7.09 (0) | 9.82 | 0.0 | 170 / 367 | 8.37 | 0.81 | nan |
| anchored, weighted, src5 | 6.40 (1) | 6.45 (1) | 3.41 (0) | 1.35 (0) | 17.52 | 0.0 | 170 / 367 | 3.34 | 3.06 | nan |
| native, full known, weighted, src5 | 7.41 (8) | 7.47 (7) | 2.99 (0) | 1.13 (0) | 18.93 | 0.0 | 170 / 367 | 2.91 | 4.49 | nan |
| anchored, stratified, src5 | 6.86 (1) | 6.89 (2) | 7.46 (1) | 6.78 (0) | 13.82 | 0.0 | 170 / 367 | 7.32 | -0.46 | nan |

## alpha = 0.05, dataset split

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 1283 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 8.92 (100) | 9.01 (100) | 4.47 (25) | 1.66 (0) | 13.25 | 0.0 | 170 / 367 | 4.42 | 4.50 | 29.71 |
| anchored, image-level (paper) | 18.76 (100) | 18.83 (100) | 10.20 (100) | 4.91 (43) | 5.85 | 0.0 | 170 / 367 | 10.16 | 8.59 | 29.71 |
| anchored, both | 8.92 (100) | 9.01 (100) | 4.47 (25) | 1.66 (0) | 13.25 | 0.0 | 170 / 367 | 4.42 | 4.50 | 29.71 |
| native, full known, label-level | 11.42 (100) | 11.50 (100) | 4.48 (29) | 1.68 (0) | 11.71 | 0.0 | 170 / 367 | 4.43 | 6.99 | 31.14 |
| native, frozen at source, label-level | 16.05 (100) | 16.09 (100) | 6.89 (98) | 2.86 (0) | 7.72 | 0.0 | 170 / 367 | 4.43 | 11.62 | 39.38 |
| native, frozen at source, image-level | 30.98 (100) | 30.92 (100) | 14.49 (100) | 6.99 (100) | 3.63 | 0.0 | 170 / 367 | 10.22 | 20.76 | 39.38 |
| anchored, weighted, all2 | 0.65 (0) | 0.64 (0) | 0.65 (0) | 0.30 (0) | 689.83 | 37.0 | 170 / 367 | 0.66 | -0.01 | nan |
| native, full known, weighted, all2 | 2.08 (1) | 2.10 (1) | 0.91 (0) | 0.43 (0) | 574.76 | 0.0 | 170 / 367 | 0.86 | 1.22 | nan |
| anchored, stratified, all2 | 3.89 (5) | 3.88 (5) | 4.25 (14) | 2.20 (0) | 651.07 | 37.0 | 170 / 367 | 4.21 | -0.32 | nan |
| anchored, weighted, all3 | 1.18 (0) | 1.20 (0) | 0.90 (0) | 0.40 (0) | 484.89 | 17.3 | 170 / 367 | 0.88 | 0.31 | nan |
| native, full known, weighted, all3 | 2.26 (2) | 2.34 (3) | 1.53 (0) | 0.60 (0) | 514.95 | 29.3 | 170 / 367 | 1.42 | 0.84 | nan |
| anchored, stratified, all3 | 2.02 (0) | 2.03 (0) | 3.89 (3) | 2.40 (0) | 863.68 | 61.9 | 170 / 367 | 3.83 | -1.82 | nan |
| anchored, weighted, all5 | 1.14 (0) | 1.15 (0) | 1.11 (0) | 0.47 (0) | 365.40 | 20.2 | 170 / 367 | 1.00 | 0.14 | nan |
| native, full known, weighted, all5 | 2.66 (1) | 2.72 (1) | 2.14 (0) | 0.77 (0) | 547.25 | 31.0 | 170 / 367 | 2.05 | 0.61 | nan |
| anchored, stratified, all5 | 1.16 (0) | 1.15 (0) | 3.57 (1) | 2.53 (0) | 792.79 | 51.1 | 170 / 367 | 3.48 | -2.32 | nan |
| anchored, weighted, src2 | 5.29 (60) | 5.33 (59) | 2.59 (1) | 0.99 (0) | 21.78 | 0.0 | 170 / 367 | 2.53 | 2.76 | nan |
| native, full known, weighted, src2 | 6.37 (87) | 6.45 (88) | 2.29 (0) | 0.84 (0) | 23.63 | 0.0 | 170 / 367 | 2.24 | 4.13 | nan |
| anchored, stratified, src2 | 5.38 (61) | 5.43 (59) | 3.96 (8) | 2.78 (0) | 18.89 | 0.0 | 170 / 367 | 3.87 | 1.52 | nan |
| anchored, weighted, src3 | 3.83 (15) | 3.88 (14) | 1.99 (0) | 0.76 (0) | 29.48 | 0.0 | 170 / 367 | 1.93 | 1.90 | nan |
| native, full known, weighted, src3 | 4.39 (30) | 4.47 (34) | 1.63 (0) | 0.58 (0) | 38.67 | 0.0 | 170 / 367 | 1.55 | 2.84 | nan |
| anchored, stratified, src3 | 3.76 (12) | 3.81 (13) | 3.43 (2) | 2.71 (0) | 26.40 | 0.0 | 170 / 367 | 3.31 | 0.46 | nan |
| anchored, weighted, src5 | 2.32 (1) | 2.37 (2) | 1.35 (0) | 0.54 (0) | 53.54 | 0.0 | 170 / 367 | 1.26 | 1.05 | nan |
| native, full known, weighted, src5 | 2.39 (2) | 2.41 (4) | 1.17 (0) | 0.43 (0) | 118.54 | 0.0 | 170 / 367 | 1.07 | 1.31 | nan |
| anchored, stratified, src5 | 2.10 (0) | 2.15 (1) | 2.39 (0) | 2.01 (0) | 60.00 | 0.0 | 170 / 367 | 2.19 | -0.09 | nan |
