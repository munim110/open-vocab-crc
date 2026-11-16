# A guarantee for the added labels under (weighted) label exchangeability

CAT-Seg (vitl_bank683), 2000 COCO val2017 (LVIS-annotated) images with a labelled sampled pixel (1283-name vocabulary: 171 source names, then the LVIS v1 annotation mapped to the added names), 500 trials (random half/half image split; source vocabulary as per design). Label loss = pooled fraction of the label's sampled pixels whose score for it is below the threshold. "Added, cal" = mean over added labels present in the calibration images (the quantity the proposition bounds); "added, held-out" = same on the held-out images; "src, class" = class-averaged source loss on held-out images; "src, image" = image-level source risk (the paper's guarantee); size = labels per labelled pixel at 1283 names, held-out images; floor = % of added labels present whose threshold is the grid floor. Risks in % (and % of trials above alpha). Development data; nothing fitted.

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
| anchored, weighted by true prevalence, all2 | 16.64 (100) | 16.73 (100) | 9.50 (31) | 4.48 (0) | 647.09 | 2.8 | 170 / 367 | 9.44 | 7.20 | nan |
| native, full known, weighted by true prevalence, all2 | 20.17 (100) | 20.24 (100) | 9.51 (32) | 4.28 (0) | 646.78 | 2.8 | 170 / 367 | 9.44 | 10.73 | nan |
| anchored, weighted, all3 | 3.94 (0) | 4.00 (0) | 2.34 (0) | 0.94 (0) | 33.98 | 0.0 | 170 / 367 | 2.25 | 1.69 | nan |
| native, full known, weighted, all3 | 7.19 (7) | 7.24 (8) | 3.53 (0) | 1.37 (0) | 38.57 | 0.0 | 170 / 367 | 3.44 | 3.75 | nan |
| anchored, stratified, all3 | 6.47 (0) | 6.49 (0) | 8.77 (9) | 5.69 (0) | 439.68 | 17.3 | 170 / 367 | 8.59 | -2.12 | nan |
| anchored, weighted by true prevalence, all3 | 9.59 (42) | 9.57 (42) | 10.44 (62) | 5.04 (0) | 860.23 | 39.5 | 170 / 367 | 10.38 | -0.79 | nan |
| native, full known, weighted by true prevalence, all3 | 10.18 (57) | 10.14 (53) | 9.17 (17) | 4.12 (0) | 860.53 | 39.5 | 170 / 367 | 9.13 | 1.04 | nan |
| anchored, weighted, all5 | 3.03 (0) | 3.03 (0) | 2.86 (0) | 1.15 (0) | 277.50 | 19.4 | 170 / 367 | 2.80 | 0.23 | nan |
| native, full known, weighted, all5 | 6.09 (0) | 6.13 (0) | 4.29 (0) | 1.62 (0) | 374.22 | 14.0 | 170 / 367 | 4.22 | 1.87 | nan |
| anchored, stratified, all5 | 3.01 (0) | 2.99 (0) | 8.19 (2) | 6.04 (0) | 776.40 | 51.1 | 170 / 367 | 8.13 | -5.12 | nan |
| anchored, weighted by true prevalence, all5 | 2.24 (0) | 2.24 (0) | 9.73 (27) | 4.82 (5) | 1031.14 | 77.9 | 170 / 367 | 9.69 | -7.45 | nan |
| native, full known, weighted by true prevalence, all5 | 2.84 (0) | 2.82 (0) | 10.23 (33) | 4.85 (3) | 1030.94 | 77.9 | 170 / 367 | 10.20 | -7.37 | nan |
| anchored, weighted, src2 | 11.68 (87) | 11.75 (88) | 6.04 (0) | 2.68 (0) | 9.69 | 0.0 | 170 / 367 | 5.99 | 5.69 | nan |
| native, full known, weighted, src2 | 12.60 (98) | 12.68 (98) | 5.22 (0) | 2.09 (0) | 10.08 | 0.0 | 170 / 367 | 5.19 | 7.42 | nan |
| anchored, stratified, src2 | 11.85 (89) | 11.94 (90) | 8.95 (13) | 6.85 (0) | 7.77 | 0.0 | 170 / 367 | 8.91 | 2.94 | nan |
| anchored, weighted by true prevalence, src2 | 11.87 (86) | 11.95 (87) | 6.34 (0) | 2.90 (0) | 9.49 | 0.0 | 170 / 367 | 6.28 | 5.59 | nan |
| native, full known, weighted by true prevalence, src2 | 13.88 (99) | 13.95 (100) | 6.12 (0) | 2.64 (0) | 8.80 | 0.0 | 170 / 367 | 6.08 | 7.80 | nan |
| anchored, weighted, src3 | 8.91 (22) | 8.99 (23) | 4.73 (0) | 1.94 (0) | 12.68 | 0.0 | 170 / 367 | 4.69 | 4.22 | nan |
| native, full known, weighted, src3 | 9.92 (47) | 10.03 (50) | 3.97 (0) | 1.52 (0) | 13.48 | 0.0 | 170 / 367 | 3.90 | 6.02 | nan |
| anchored, stratified, src3 | 9.19 (27) | 9.24 (27) | 8.44 (5) | 7.09 (0) | 9.82 | 0.0 | 170 / 367 | 8.37 | 0.81 | nan |
| anchored, weighted by true prevalence, src3 | 11.44 (71) | 11.51 (76) | 6.56 (0) | 3.08 (0) | 9.70 | 0.0 | 170 / 367 | 6.52 | 4.93 | nan |
| native, full known, weighted by true prevalence, src3 | 12.97 (96) | 13.06 (96) | 5.95 (0) | 2.60 (0) | 9.38 | 0.0 | 170 / 367 | 5.93 | 7.05 | nan |
| anchored, weighted, src5 | 6.40 (1) | 6.45 (1) | 3.41 (0) | 1.35 (0) | 17.52 | 0.0 | 170 / 367 | 3.34 | 3.06 | nan |
| native, full known, weighted, src5 | 7.41 (8) | 7.47 (7) | 2.99 (0) | 1.13 (0) | 18.93 | 0.0 | 170 / 367 | 2.91 | 4.49 | nan |
| anchored, stratified, src5 | 6.86 (1) | 6.89 (2) | 7.46 (1) | 6.78 (0) | 13.82 | 0.0 | 170 / 367 | 7.32 | -0.46 | nan |
| anchored, weighted by true prevalence, src5 | 6.56 (3) | 6.61 (3) | 3.96 (0) | 1.66 (0) | 17.45 | 0.0 | 170 / 367 | 3.88 | 2.69 | nan |
| native, full known, weighted by true prevalence, src5 | 8.60 (24) | 8.67 (28) | 3.89 (0) | 1.60 (0) | 15.87 | 0.0 | 170 / 367 | 3.81 | 4.79 | nan |

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
| anchored, weighted by true prevalence, all2 | 8.35 (100) | 8.46 (100) | 4.47 (25) | 1.66 (0) | 652.01 | 2.8 | 170 / 367 | 4.42 | 3.93 | nan |
| native, full known, weighted by true prevalence, all2 | 10.68 (100) | 10.79 (100) | 4.48 (29) | 1.68 (0) | 651.38 | 2.8 | 170 / 367 | 4.43 | 6.25 | nan |
| anchored, weighted, all3 | 1.18 (0) | 1.20 (0) | 0.90 (0) | 0.40 (0) | 484.89 | 17.3 | 170 / 367 | 0.88 | 0.31 | nan |
| native, full known, weighted, all3 | 2.26 (2) | 2.34 (3) | 1.53 (0) | 0.60 (0) | 514.95 | 29.3 | 170 / 367 | 1.42 | 0.84 | nan |
| anchored, stratified, all3 | 2.02 (0) | 2.03 (0) | 3.89 (3) | 2.40 (0) | 863.68 | 61.9 | 170 / 367 | 3.83 | -1.82 | nan |
| anchored, weighted by true prevalence, all3 | 6.78 (48) | 6.79 (48) | 7.65 (61) | 3.46 (46) | 862.53 | 39.5 | 170 / 367 | 7.56 | -0.78 | nan |
| native, full known, weighted by true prevalence, all3 | 6.99 (70) | 6.98 (66) | 6.37 (63) | 2.65 (0) | 862.75 | 39.5 | 170 / 367 | 6.32 | 0.68 | nan |
| anchored, weighted, all5 | 1.14 (0) | 1.15 (0) | 1.11 (0) | 0.47 (0) | 365.40 | 20.2 | 170 / 367 | 1.00 | 0.14 | nan |
| native, full known, weighted, all5 | 2.66 (1) | 2.72 (1) | 2.14 (0) | 0.77 (0) | 547.25 | 31.0 | 170 / 367 | 2.05 | 0.61 | nan |
| anchored, stratified, all5 | 1.16 (0) | 1.15 (0) | 3.57 (1) | 2.53 (0) | 792.79 | 51.1 | 170 / 367 | 3.48 | -2.32 | nan |
| anchored, weighted by true prevalence, all5 | 1.52 (0) | 1.52 (0) | 7.39 (88) | 3.37 (15) | 1032.22 | 77.9 | 170 / 367 | 7.35 | -5.83 | nan |
| native, full known, weighted by true prevalence, all5 | 2.06 (0) | 2.04 (0) | 7.90 (100) | 3.45 (5) | 1031.78 | 77.9 | 170 / 367 | 7.86 | -5.80 | nan |
| anchored, weighted, src2 | 5.29 (60) | 5.33 (59) | 2.59 (1) | 0.99 (0) | 21.78 | 0.0 | 170 / 367 | 2.53 | 2.76 | nan |
| native, full known, weighted, src2 | 6.37 (87) | 6.45 (88) | 2.29 (0) | 0.84 (0) | 23.63 | 0.0 | 170 / 367 | 2.24 | 4.13 | nan |
| anchored, stratified, src2 | 5.38 (61) | 5.43 (59) | 3.96 (8) | 2.78 (0) | 18.89 | 0.0 | 170 / 367 | 3.87 | 1.52 | nan |
| anchored, weighted by true prevalence, src2 | 5.30 (60) | 5.36 (59) | 2.64 (1) | 1.03 (0) | 21.81 | 0.0 | 170 / 367 | 2.58 | 2.72 | nan |
| native, full known, weighted by true prevalence, src2 | 6.93 (93) | 7.02 (94) | 2.62 (1) | 1.01 (0) | 20.72 | 0.0 | 170 / 367 | 2.56 | 4.37 | nan |
| anchored, weighted, src3 | 3.83 (15) | 3.88 (14) | 1.99 (0) | 0.76 (0) | 29.48 | 0.0 | 170 / 367 | 1.93 | 1.90 | nan |
| native, full known, weighted, src3 | 4.39 (30) | 4.47 (34) | 1.63 (0) | 0.58 (0) | 38.67 | 0.0 | 170 / 367 | 1.55 | 2.84 | nan |
| anchored, stratified, src3 | 3.76 (12) | 3.81 (13) | 3.43 (2) | 2.71 (0) | 26.40 | 0.0 | 170 / 367 | 3.31 | 0.46 | nan |
| anchored, weighted by true prevalence, src3 | 4.50 (34) | 4.57 (38) | 2.69 (2) | 1.10 (0) | 25.88 | 0.0 | 170 / 367 | 2.62 | 1.88 | nan |
| native, full known, weighted by true prevalence, src3 | 5.74 (64) | 5.79 (64) | 2.57 (2) | 1.04 (0) | 27.49 | 0.0 | 170 / 367 | 2.48 | 3.26 | nan |
| anchored, weighted, src5 | 2.32 (1) | 2.37 (2) | 1.35 (0) | 0.54 (0) | 53.54 | 0.0 | 170 / 367 | 1.26 | 1.05 | nan |
| native, full known, weighted, src5 | 2.39 (2) | 2.41 (4) | 1.17 (0) | 0.43 (0) | 118.54 | 0.0 | 170 / 367 | 1.07 | 1.31 | nan |
| anchored, stratified, src5 | 2.10 (0) | 2.15 (1) | 2.39 (0) | 2.01 (0) | 60.00 | 0.0 | 170 / 367 | 2.19 | -0.09 | nan |
| anchored, weighted by true prevalence, src5 | 1.90 (1) | 1.95 (2) | 1.52 (0) | 0.64 (0) | 71.90 | 0.0 | 170 / 367 | 1.42 | 0.48 | nan |
| native, full known, weighted by true prevalence, src5 | 2.13 (5) | 2.18 (5) | 1.52 (0) | 0.64 (0) | 156.51 | 0.0 | 170 / 367 | 1.41 | 0.72 | nan |
