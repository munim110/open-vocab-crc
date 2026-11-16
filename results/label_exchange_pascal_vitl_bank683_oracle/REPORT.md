# A guarantee for the added labels under (weighted) label exchangeability

CAT-Seg (vitl_bank683), 2000 Pascal Context validation images with a labelled sampled pixel (458-name vocabulary: 59 source names, then the PC-459 annotation mapped to the added names), 500 trials (random half/half image split; source vocabulary as per design). Label loss = pooled fraction of the label's sampled pixels whose score for it is below the threshold. "Added, cal" = mean over added labels present in the calibration images (the quantity the proposition bounds); "added, held-out" = same on the held-out images; "src, class" = class-averaged source loss on held-out images; "src, image" = image-level source risk (the paper's guarantee); size = labels per labelled pixel at 458 names, held-out images; floor = % of added labels present whose threshold is the grid floor. Risks in % (and % of trials above alpha). Development data; nothing fitted.

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
| anchored, weighted by true prevalence, all2 | 18.12 (100) | 18.14 (100) | 8.48 (7) | 8.40 (1) | 231.24 | 13.8 | 59 / 165 |
| native, full known, weighted by true prevalence, all2 | 21.31 (100) | 21.31 (100) | 8.48 (9) | 7.55 (0) | 231.19 | 13.8 | 59 / 165 |
| anchored, weighted, all3 | 4.24 (0) | 4.26 (0) | 4.25 (0) | 4.69 (0) | 309.33 | 64.6 | 59 / 165 |
| native, full known, weighted, all3 | 8.09 (3) | 8.04 (3) | 10.62 (71) | 9.67 (40) | 307.97 | 62.2 | 59 / 165 |
| anchored, stratified, all3 | 6.26 (0) | 6.24 (0) | 7.80 (0) | 8.71 (6) | 308.32 | 64.6 | 59 / 165 |
| anchored, weighted by true prevalence, all3 | 17.53 (99) | 17.38 (99) | 16.05 (97) | 16.42 (97) | 307.46 | 47.2 | 59 / 165 |
| native, full known, weighted by true prevalence, all3 | 21.18 (100) | 21.00 (99) | 15.68 (97) | 13.74 (96) | 307.46 | 47.2 | 59 / 165 |
| anchored, weighted, all5 | 4.77 (0) | 4.80 (0) | 3.61 (0) | 3.93 (0) | 278.94 | 54.9 | 59 / 165 |
| native, full known, weighted, all5 | 1.78 (0) | 1.75 (0) | 4.42 (0) | 4.54 (0) | 369.61 | 84.7 | 59 / 165 |
| anchored, stratified, all5 | 2.29 (0) | 2.27 (0) | 7.00 (0) | 7.65 (0) | 368.91 | 85.1 | 59 / 165 |
| anchored, weighted by true prevalence, all5 | 7.83 (1) | 7.80 (0) | 18.23 (97) | 18.50 (97) | 368.26 | 80.0 | 59 / 165 |
| native, full known, weighted by true prevalence, all5 | 9.16 (20) | 9.14 (21) | 17.41 (97) | 15.04 (97) | 368.33 | 80.0 | 59 / 165 |
| anchored, weighted, src2 | 16.80 (100) | 16.83 (100) | 6.06 (0) | 6.72 (0) | 3.51 | 0.0 | 59 / 165 |
| native, full known, weighted, src2 | 19.89 (100) | 19.88 (100) | 5.84 (0) | 6.21 (0) | 3.49 | 0.0 | 59 / 165 |
| anchored, stratified, src2 | 16.78 (100) | 16.81 (100) | 6.97 (0) | 8.40 (1) | 3.36 | 0.0 | 59 / 165 |
| anchored, weighted by true prevalence, src2 | 19.52 (100) | 19.54 (100) | 8.47 (13) | 9.74 (39) | 2.97 | 0.0 | 59 / 165 |
| native, full known, weighted by true prevalence, src2 | 22.23 (100) | 22.23 (100) | 7.39 (3) | 7.67 (1) | 3.05 | 0.0 | 59 / 165 |
| anchored, weighted, src3 | 13.28 (99) | 13.27 (99) | 4.87 (0) | 5.50 (0) | 4.30 | 0.0 | 59 / 165 |
| native, full known, weighted, src3 | 16.18 (100) | 16.18 (100) | 5.18 (0) | 5.69 (0) | 4.19 | 0.0 | 59 / 165 |
| anchored, stratified, src3 | 13.12 (98) | 13.12 (98) | 5.50 (0) | 6.33 (0) | 4.22 | 0.0 | 59 / 165 |
| anchored, weighted by true prevalence, src3 | 15.85 (100) | 15.90 (100) | 7.60 (5) | 8.92 (24) | 3.57 | 0.0 | 59 / 165 |
| native, full known, weighted by true prevalence, src3 | 18.44 (100) | 18.43 (100) | 6.42 (0) | 6.92 (0) | 3.71 | 0.0 | 59 / 165 |
| anchored, weighted, src5 | 10.39 (60) | 10.32 (59) | 4.33 (0) | 4.81 (0) | 5.47 | 0.0 | 59 / 165 |
| native, full known, weighted, src5 | 9.73 (43) | 9.62 (42) | 4.33 (0) | 4.86 (0) | 8.20 | 0.0 | 59 / 165 |
| anchored, stratified, src5 | 8.25 (8) | 8.18 (10) | 2.50 (0) | 2.65 (0) | 8.01 | 0.0 | 59 / 165 |
| anchored, weighted by true prevalence, src5 | 9.65 (39) | 9.54 (40) | 7.58 (10) | 8.94 (32) | 6.45 | 0.0 | 59 / 165 |
| native, full known, weighted by true prevalence, src5 | 11.04 (74) | 10.94 (71) | 6.41 (1) | 6.97 (2) | 6.95 | 0.0 | 59 / 165 |

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
| anchored, weighted by true prevalence, all2 | 10.51 (100) | 10.55 (100) | 3.42 (1) | 3.38 (0) | 232.83 | 13.8 | 59 / 165 |
| native, full known, weighted by true prevalence, all2 | 12.79 (100) | 12.83 (100) | 3.46 (1) | 3.12 (0) | 232.85 | 13.8 | 59 / 165 |
| anchored, weighted, all3 | 2.90 (0) | 2.94 (0) | 2.64 (0) | 2.75 (0) | 310.53 | 64.6 | 59 / 165 |
| native, full known, weighted, all3 | 4.73 (42) | 4.73 (39) | 4.50 (31) | 4.17 (21) | 309.36 | 62.2 | 59 / 165 |
| anchored, stratified, all3 | 3.24 (0) | 3.29 (1) | 3.09 (0) | 3.30 (0) | 310.09 | 64.6 | 59 / 165 |
| anchored, weighted by true prevalence, all3 | 10.53 (97) | 10.51 (96) | 7.09 (81) | 7.10 (82) | 308.51 | 47.2 | 59 / 165 |
| native, full known, weighted by true prevalence, all3 | 12.41 (97) | 12.35 (96) | 7.12 (81) | 6.41 (79) | 308.60 | 47.2 | 59 / 165 |
| anchored, weighted, all5 | 2.14 (0) | 2.15 (0) | 2.36 (0) | 2.50 (0) | 283.06 | 54.9 | 59 / 165 |
| native, full known, weighted, all5 | 0.92 (0) | 0.92 (0) | 2.11 (0) | 2.17 (0) | 370.92 | 84.7 | 59 / 165 |
| anchored, stratified, all5 | 0.86 (0) | 0.88 (0) | 2.67 (0) | 2.95 (0) | 370.33 | 85.1 | 59 / 165 |
| anchored, weighted by true prevalence, all5 | 5.02 (60) | 5.01 (58) | 9.11 (87) | 9.22 (87) | 369.03 | 80.0 | 59 / 165 |
| native, full known, weighted by true prevalence, all5 | 5.91 (77) | 5.91 (79) | 9.09 (86) | 8.13 (84) | 369.17 | 80.0 | 59 / 165 |
| anchored, weighted, src2 | 7.51 (98) | 7.42 (96) | 2.33 (0) | 3.18 (0) | 9.21 | 0.0 | 59 / 165 |
| native, full known, weighted, src2 | 8.48 (99) | 8.39 (99) | 2.03 (0) | 2.85 (0) | 10.39 | 0.0 | 59 / 165 |
| anchored, stratified, src2 | 7.48 (98) | 7.39 (96) | 1.85 (0) | 2.23 (0) | 9.53 | 0.0 | 59 / 165 |
| anchored, weighted by true prevalence, src2 | 8.46 (100) | 8.37 (99) | 3.42 (1) | 4.74 (32) | 7.87 | 0.0 | 59 / 165 |
| native, full known, weighted by true prevalence, src2 | 9.68 (100) | 9.59 (100) | 2.90 (0) | 3.76 (2) | 8.65 | 0.0 | 59 / 165 |
| anchored, weighted, src3 | 1.83 (0) | 1.79 (0) | 1.93 (0) | 2.88 (0) | 55.52 | 0.0 | 59 / 165 |
| native, full known, weighted, src3 | 0.89 (0) | 0.91 (0) | 1.84 (0) | 2.72 (0) | 184.78 | 0.0 | 59 / 165 |
| anchored, stratified, src3 | 0.52 (0) | 0.50 (0) | 0.19 (0) | 0.31 (0) | 145.30 | 0.0 | 59 / 165 |
| anchored, weighted by true prevalence, src3 | 1.08 (0) | 1.06 (0) | 3.00 (0) | 4.42 (24) | 85.31 | 0.0 | 59 / 165 |
| native, full known, weighted by true prevalence, src3 | 0.35 (0) | 0.32 (0) | 2.59 (0) | 3.60 (3) | 336.64 | 0.0 | 59 / 165 |
| anchored, weighted, src5 | 0.77 (0) | 0.80 (0) | 2.46 (0) | 2.92 (0) | 379.25 | 87.6 | 59 / 165 |
| native, full known, weighted, src5 | 0.56 (0) | 0.57 (0) | 2.06 (0) | 2.51 (0) | 399.13 | 94.6 | 59 / 165 |
| anchored, stratified, src5 | 0.00 (0) | 0.00 (0) | 0.00 (0) | 0.00 (0) | 458.00 | 100.0 | 59 / 165 |
| anchored, weighted by true prevalence, src5 | 1.05 (0) | 1.04 (0) | 3.48 (6) | 4.36 (26) | 406.09 | 96.4 | 59 / 165 |
| native, full known, weighted by true prevalence, src5 | 1.14 (0) | 1.12 (0) | 3.33 (3) | 3.83 (12) | 406.25 | 96.4 | 59 / 165 |
