# A guarantee for the added labels under (weighted) label exchangeability

CAT-Seg (vitl_bank683), 2000 ADE validation images with a labelled sampled pixel (845-name vocabulary: 150 source names, then the A-847 annotation mapped to the added names), 500 trials (random half/half image split; source vocabulary as per design). Label loss = pooled fraction of the label's sampled pixels whose score for it is below the threshold. "Added, cal" = mean over added labels present in the calibration images (the quantity the proposition bounds); "added, held-out" = same on the held-out images; "src, class" = class-averaged source loss on held-out images; "src, image" = image-level source risk (the paper's guarantee); size = labels per labelled pixel at 845 names, held-out images; floor = % of added labels present whose threshold is the grid floor. Risks in % (and % of trials above alpha). Development data; nothing fitted.

## alpha = 0.1, dataset split

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 845 | Floor | Source / added labels present (cal) |
|---|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 22.20 (100) | 22.25 (100) | 9.42 (25) | 4.91 (0) | 9.00 | 0.0 | 149 / 486 |
| anchored, image-level (paper) | 34.15 (100) | 34.15 (100) | 16.67 (100) | 9.89 (39) | 4.48 | 0.0 | 149 / 486 |
| anchored, both | 22.20 (100) | 22.25 (100) | 9.42 (25) | 4.91 (0) | 9.00 | 0.0 | 149 / 486 |
| native, full known, label-level | 22.65 (100) | 22.68 (100) | 9.43 (24) | 3.95 (0) | 10.14 | 0.0 | 149 / 486 |
| native, frozen at source, label-level | 33.80 (100) | 33.83 (100) | 15.64 (100) | 7.24 (0) | 5.11 | 0.0 | 149 / 486 |
| native, frozen at source, image-level | 54.05 (100) | 54.04 (100) | 30.30 (100) | 15.23 (100) | 2.20 | 0.0 | 149 / 486 |
| anchored, weighted, all2 | 10.12 (55) | 10.22 (61) | 3.18 (0) | 1.52 (0) | 26.81 | 0.0 | 149 / 486 |
| native, full known, weighted, all2 | 8.90 (17) | 8.94 (21) | 3.01 (0) | 1.15 (0) | 40.65 | 0.0 | 149 / 486 |
| anchored, stratified, all2 | 12.24 (98) | 12.37 (98) | 8.84 (12) | 5.45 (0) | 23.73 | 0.0 | 149 / 486 |
| anchored, weighted by true prevalence, all2 | 11.53 (68) | 11.63 (66) | 18.09 (94) | 10.83 (44) | 426.57 | 56.2 | 149 / 486 |
| native, full known, weighted by true prevalence, all2 | 13.33 (90) | 13.44 (91) | 19.70 (94) | 9.46 (42) | 426.34 | 56.2 | 149 / 486 |
| anchored, weighted, all3 | 9.55 (38) | 9.63 (41) | 3.35 (0) | 1.52 (0) | 27.44 | 0.0 | 149 / 486 |
| native, full known, weighted, all3 | 10.81 (79) | 10.87 (82) | 3.52 (0) | 1.41 (0) | 30.31 | 0.0 | 149 / 486 |
| anchored, stratified, all3 | 6.63 (0) | 6.69 (0) | 8.40 (4) | 5.62 (0) | 293.77 | 37.7 | 149 / 486 |
| anchored, weighted by true prevalence, all3 | 4.34 (0) | 4.36 (0) | 14.05 (83) | 8.29 (30) | 569.55 | 78.4 | 149 / 486 |
| native, full known, weighted by true prevalence, all3 | 5.04 (0) | 5.08 (0) | 16.02 (88) | 7.61 (20) | 569.75 | 78.4 | 149 / 486 |
| anchored, weighted, all5 | 10.13 (58) | 10.24 (63) | 3.47 (0) | 1.62 (0) | 25.59 | 0.0 | 149 / 486 |
| native, full known, weighted, all5 | 6.89 (0) | 6.97 (0) | 3.62 (0) | 1.49 (0) | 194.92 | 20.1 | 149 / 486 |
| anchored, stratified, all5 | 4.73 (0) | 4.77 (0) | 7.45 (0) | 6.01 (0) | 353.52 | 45.5 | 149 / 486 |
| anchored, weighted by true prevalence, all5 | 4.49 (0) | 4.52 (0) | 11.70 (76) | 6.68 (1) | 511.89 | 69.2 | 149 / 486 |
| native, full known, weighted by true prevalence, all5 | 5.37 (0) | 5.41 (0) | 13.38 (93) | 6.20 (0) | 511.67 | 69.2 | 149 / 486 |
| anchored, weighted, src2 | 16.08 (100) | 16.13 (100) | 6.25 (0) | 3.19 (0) | 14.51 | 0.0 | 149 / 486 |
| native, full known, weighted, src2 | 14.68 (100) | 14.76 (100) | 5.40 (0) | 2.23 (0) | 19.42 | 0.0 | 149 / 486 |
| anchored, stratified, src2 | 16.44 (100) | 16.51 (100) | 8.81 (7) | 7.41 (0) | 12.16 | 0.0 | 149 / 486 |
| anchored, weighted by true prevalence, src2 | 20.35 (100) | 20.40 (100) | 8.77 (9) | 4.82 (0) | 10.11 | 0.0 | 149 / 486 |
| native, full known, weighted by true prevalence, src2 | 19.80 (100) | 19.85 (100) | 8.32 (3) | 3.65 (0) | 12.23 | 0.0 | 149 / 486 |
| anchored, weighted, src3 | 13.54 (100) | 13.61 (100) | 4.78 (0) | 2.41 (0) | 18.77 | 0.0 | 149 / 486 |
| native, full known, weighted, src3 | 12.46 (99) | 12.54 (99) | 4.23 (0) | 1.75 (0) | 24.75 | 0.0 | 149 / 486 |
| anchored, stratified, src3 | 13.67 (100) | 13.77 (100) | 8.24 (2) | 7.22 (0) | 15.53 | 0.0 | 149 / 486 |
| anchored, weighted by true prevalence, src3 | 19.16 (100) | 19.22 (100) | 8.66 (14) | 4.77 (0) | 10.97 | 0.0 | 149 / 486 |
| native, full known, weighted by true prevalence, src3 | 19.66 (100) | 19.71 (100) | 8.79 (15) | 3.90 (0) | 12.20 | 0.0 | 149 / 486 |
| anchored, weighted, src5 | 11.62 (92) | 11.70 (93) | 3.81 (0) | 1.90 (0) | 22.88 | 0.0 | 149 / 486 |
| native, full known, weighted, src5 | 10.73 (76) | 10.79 (79) | 3.39 (0) | 1.40 (0) | 30.75 | 0.0 | 149 / 486 |
| anchored, stratified, src5 | 11.60 (90) | 11.70 (91) | 7.07 (0) | 7.36 (0) | 20.09 | 0.0 | 149 / 486 |
| anchored, weighted by true prevalence, src5 | 15.13 (100) | 15.20 (100) | 6.60 (0) | 3.57 (0) | 15.62 | 0.0 | 149 / 486 |
| native, full known, weighted by true prevalence, src5 | 15.65 (100) | 15.74 (100) | 7.16 (2) | 3.12 (0) | 16.99 | 0.0 | 149 / 486 |

## alpha = 0.05, dataset split

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 845 | Floor | Source / added labels present (cal) |
|---|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 13.11 (100) | 13.19 (100) | 4.35 (14) | 2.09 (0) | 20.65 | 0.0 | 149 / 486 |
| anchored, image-level (paper) | 22.15 (100) | 22.20 (100) | 9.38 (100) | 4.89 (42) | 9.03 | 0.0 | 149 / 486 |
| anchored, both | 13.11 (100) | 13.19 (100) | 4.35 (14) | 2.09 (0) | 20.65 | 0.0 | 149 / 486 |
| native, full known, label-level | 12.98 (100) | 13.05 (100) | 4.38 (14) | 1.73 (0) | 24.24 | 0.0 | 149 / 486 |
| native, frozen at source, label-level | 21.43 (100) | 21.46 (100) | 8.77 (100) | 3.64 (0) | 11.11 | 0.0 | 149 / 486 |
| native, frozen at source, image-level | 37.22 (100) | 37.24 (100) | 17.74 (100) | 8.38 (100) | 4.31 | 0.0 | 149 / 486 |
| anchored, weighted, all2 | 5.07 (52) | 5.11 (58) | 1.33 (0) | 0.56 (0) | 58.85 | 0.0 | 149 / 486 |
| native, full known, weighted, all2 | 1.63 (5) | 1.60 (5) | 0.70 (0) | 0.20 (0) | 418.45 | 0.0 | 149 / 486 |
| anchored, stratified, all2 | 3.81 (2) | 3.82 (2) | 3.81 (4) | 2.07 (0) | 433.41 | 57.5 | 149 / 486 |
| anchored, weighted by true prevalence, all2 | 7.43 (92) | 7.49 (92) | 11.08 (93) | 6.05 (92) | 428.78 | 56.2 | 149 / 486 |
| native, full known, weighted by true prevalence, all2 | 7.92 (92) | 7.99 (92) | 11.47 (93) | 5.01 (70) | 429.26 | 56.2 | 149 / 486 |
| anchored, weighted, all3 | 1.90 (0) | 1.89 (0) | 1.45 (0) | 0.59 (0) | 322.35 | 37.7 | 149 / 486 |
| native, full known, weighted, all3 | 5.34 (66) | 5.36 (67) | 1.35 (0) | 0.50 (0) | 108.26 | 0.0 | 149 / 486 |
| anchored, stratified, all3 | 3.18 (0) | 3.19 (0) | 3.57 (1) | 2.22 (0) | 314.33 | 37.7 | 149 / 486 |
| anchored, weighted by true prevalence, all3 | 2.22 (0) | 2.24 (1) | 7.37 (73) | 3.94 (28) | 575.48 | 78.4 | 149 / 486 |
| native, full known, weighted by true prevalence, all3 | 2.47 (2) | 2.49 (2) | 8.22 (73) | 3.57 (24) | 576.25 | 78.4 | 149 / 486 |
| anchored, weighted, all5 | 4.43 (21) | 4.46 (24) | 1.39 (0) | 0.59 (0) | 62.49 | 0.0 | 149 / 486 |
| native, full known, weighted, all5 | 3.19 (0) | 3.20 (0) | 1.45 (0) | 0.57 (0) | 240.84 | 20.1 | 149 / 486 |
| anchored, stratified, all5 | 1.66 (0) | 1.66 (0) | 2.94 (0) | 2.31 (0) | 523.75 | 68.8 | 149 / 486 |
| anchored, weighted by true prevalence, all5 | 2.24 (0) | 2.26 (0) | 5.89 (86) | 3.12 (0) | 516.85 | 69.2 | 149 / 486 |
| native, full known, weighted by true prevalence, all5 | 2.29 (0) | 2.30 (0) | 6.32 (87) | 2.70 (0) | 517.89 | 69.2 | 149 / 486 |
| anchored, weighted, src2 | 9.24 (100) | 9.32 (100) | 2.63 (0) | 1.30 (0) | 32.68 | 0.0 | 149 / 486 |
| native, full known, weighted, src2 | 8.58 (100) | 8.61 (100) | 2.25 (0) | 0.98 (0) | 46.38 | 0.0 | 149 / 486 |
| anchored, stratified, src2 | 9.02 (100) | 9.10 (100) | 3.76 (2) | 2.77 (0) | 30.76 | 0.0 | 149 / 486 |
| anchored, weighted by true prevalence, src2 | 12.67 (100) | 12.76 (100) | 4.68 (34) | 2.53 (0) | 21.04 | 0.0 | 149 / 486 |
| native, full known, weighted by true prevalence, src2 | 12.52 (100) | 12.59 (100) | 4.47 (18) | 1.96 (0) | 24.88 | 0.0 | 149 / 486 |
| anchored, weighted, src3 | 7.40 (100) | 7.46 (99) | 1.96 (0) | 0.95 (0) | 42.67 | 0.0 | 149 / 486 |
| native, full known, weighted, src3 | 6.76 (96) | 6.80 (95) | 1.72 (0) | 0.72 (0) | 65.44 | 0.0 | 149 / 486 |
| anchored, stratified, src3 | 6.98 (99) | 7.06 (99) | 3.16 (0) | 2.38 (0) | 40.67 | 0.0 | 149 / 486 |
| anchored, weighted by true prevalence, src3 | 11.03 (100) | 11.12 (100) | 4.41 (26) | 2.41 (0) | 25.18 | 0.0 | 149 / 486 |
| native, full known, weighted by true prevalence, src3 | 11.63 (100) | 11.70 (100) | 4.57 (25) | 2.02 (0) | 27.30 | 0.0 | 149 / 486 |
| anchored, weighted, src5 | 6.09 (87) | 6.15 (87) | 1.57 (0) | 0.74 (0) | 51.57 | 0.0 | 149 / 486 |
| native, full known, weighted, src5 | 5.36 (69) | 5.39 (68) | 1.33 (0) | 0.52 (0) | 97.54 | 0.0 | 149 / 486 |
| anchored, stratified, src5 | 5.25 (63) | 5.30 (67) | 1.95 (0) | 1.79 (0) | 58.78 | 0.0 | 149 / 486 |
| anchored, weighted by true prevalence, src5 | 7.58 (96) | 7.65 (97) | 3.38 (2) | 1.87 (0) | 41.03 | 0.0 | 149 / 486 |
| native, full known, weighted by true prevalence, src5 | 8.42 (100) | 8.48 (100) | 3.66 (3) | 1.66 (0) | 44.90 | 0.0 | 149 / 486 |
