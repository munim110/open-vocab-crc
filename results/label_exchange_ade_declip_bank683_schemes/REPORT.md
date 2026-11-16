# A guarantee for the added labels under (weighted) label exchangeability

CAT-Seg (declip_bank683), 2000 ADE validation images with a labelled sampled pixel (845-name vocabulary: 150 source names, then the A-847 annotation mapped to the added names), 500 trials (random half/half image split; source vocabulary as per design). Label loss = pooled fraction of the label's sampled pixels whose score for it is below the threshold. "Added, cal" = mean over added labels present in the calibration images (the quantity the proposition bounds); "added, held-out" = same on the held-out images; "src, class" = class-averaged source loss on held-out images; "src, image" = image-level source risk (the paper's guarantee); size = labels per labelled pixel at 845 names, held-out images; floor = % of added labels present whose threshold is the grid floor. Risks in % (and % of trials above alpha). Development data; nothing fitted.

## alpha = 0.1, exchangeable

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 845 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 9.45 (39) | 9.43 (38) | 9.46 (44) | 4.11 (4) | 19.01 | 0.0 | 113 / 523 | 9.14 | 0.31 | 3.50 |
| anchored, image-level (paper) | 20.26 (94) | 20.34 (94) | 20.16 (94) | 9.88 (42) | 7.20 | 0.0 | 113 / 523 | 20.18 | 0.08 | 3.50 |
| anchored, both | 9.39 (37) | 9.37 (36) | 9.39 (43) | 4.03 (3) | 19.16 | 0.0 | 113 / 523 | 9.08 | 0.30 | 3.50 |
| native, full known, label-level | 9.44 (37) | 9.44 (40) | 9.46 (41) | 3.53 (1) | 22.25 | 0.0 | 113 / 523 | 9.15 | 0.29 | 3.67 |
| anchored, weighted, all2 | 9.40 (39) | 9.38 (39) | 9.46 (43) | 4.10 (3) | 19.09 | 0.0 | 113 / 523 | 9.13 | 0.27 | nan |
| native, full known, weighted, all2 | 9.42 (38) | 9.43 (40) | 9.48 (41) | 3.55 (2) | 22.25 | 0.0 | 113 / 523 | 9.16 | 0.26 | nan |
| anchored, stratified, all2 | 8.91 (31) | 8.87 (31) | 8.88 (34) | 6.38 (11) | 20.40 | 0.0 | 113 / 523 | 8.31 | 0.60 | nan |
| anchored, weighted, all3 | 9.40 (38) | 9.38 (39) | 9.47 (43) | 4.11 (4) | 19.11 | 0.0 | 113 / 523 | 9.14 | 0.26 | nan |
| native, full known, weighted, all3 | 9.40 (38) | 9.41 (41) | 9.47 (42) | 3.54 (2) | 22.26 | 0.0 | 113 / 523 | 9.14 | 0.26 | nan |
| anchored, stratified, all3 | 8.38 (23) | 8.33 (23) | 8.23 (24) | 6.29 (10) | 24.26 | 0.0 | 113 / 523 | 7.49 | 0.89 | nan |
| anchored, weighted, all5 | 9.39 (39) | 9.35 (38) | 9.46 (44) | 4.11 (3) | 19.16 | 0.0 | 113 / 523 | 9.13 | 0.26 | nan |
| native, full known, weighted, all5 | 9.36 (38) | 9.36 (41) | 9.43 (41) | 3.53 (2) | 22.55 | 0.0 | 113 / 523 | 9.12 | 0.23 | nan |
| anchored, stratified, all5 | 7.10 (8) | 7.05 (9) | 6.86 (9) | 6.01 (8) | 37.65 | 0.1 | 113 / 523 | 5.82 | 1.28 | nan |
| anchored, weighted, src2 | 9.39 (39) | 9.36 (39) | 9.43 (42) | 4.09 (3) | 19.14 | 0.0 | 113 / 523 | 9.11 | 0.28 | nan |
| native, full known, weighted, src2 | 9.35 (37) | 9.36 (39) | 9.42 (41) | 3.52 (2) | 22.49 | 0.0 | 113 / 523 | 9.09 | 0.26 | nan |
| anchored, stratified, src2 | 8.93 (31) | 8.87 (31) | 8.89 (34) | 6.38 (11) | 20.16 | 0.0 | 113 / 523 | 8.31 | 0.62 | nan |
| anchored, weighted, src3 | 9.36 (38) | 9.34 (39) | 9.43 (43) | 4.10 (4) | 19.17 | 0.0 | 113 / 523 | 9.10 | 0.26 | nan |
| native, full known, weighted, src3 | 9.32 (39) | 9.32 (39) | 9.38 (41) | 3.50 (2) | 22.72 | 0.0 | 113 / 523 | 9.05 | 0.27 | nan |
| anchored, stratified, src3 | 8.34 (22) | 8.29 (21) | 8.23 (23) | 6.28 (10) | 24.25 | 0.0 | 113 / 523 | 7.49 | 0.85 | nan |
| anchored, weighted, src5 | 9.34 (38) | 9.31 (38) | 9.42 (43) | 4.09 (3) | 19.31 | 0.0 | 113 / 523 | 9.07 | 0.27 | nan |
| native, full known, weighted, src5 | 9.33 (37) | 9.33 (40) | 9.41 (41) | 3.52 (2) | 22.59 | 0.0 | 113 / 523 | 9.09 | 0.24 | nan |
| anchored, stratified, src5 | 7.11 (8) | 7.08 (9) | 6.81 (7) | 5.87 (10) | 35.78 | 0.0 | 113 / 523 | 5.84 | 1.27 | nan |

## alpha = 0.05, exchangeable

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 845 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 4.53 (34) | 4.48 (34) | 4.42 (35) | 1.61 (2) | 52.32 | 0.0 | 113 / 523 | 4.10 | 0.43 | 3.50 |
| anchored, image-level (paper) | 12.16 (97) | 12.11 (97) | 12.06 (96) | 4.91 (43) | 15.14 | 0.0 | 113 / 523 | 11.92 | 0.24 | 3.50 |
| anchored, both | 4.51 (33) | 4.46 (34) | 4.40 (35) | 1.59 (2) | 52.41 | 0.0 | 113 / 523 | 4.09 | 0.42 | 3.50 |
| native, full known, label-level | 4.20 (35) | 4.15 (35) | 3.99 (34) | 1.19 (1) | 194.34 | 0.0 | 113 / 523 | 3.48 | 0.72 | 3.67 |
| anchored, weighted, all2 | 4.50 (33) | 4.45 (33) | 4.42 (35) | 1.61 (2) | 52.56 | 0.0 | 113 / 523 | 4.10 | 0.40 | nan |
| native, full known, weighted, all2 | 4.19 (35) | 4.15 (34) | 4.01 (36) | 1.21 (1) | 192.26 | 0.0 | 113 / 523 | 3.51 | 0.68 | nan |
| anchored, stratified, all2 | 3.89 (23) | 3.86 (21) | 3.70 (21) | 2.29 (5) | 64.53 | 0.0 | 113 / 523 | 3.23 | 0.67 | nan |
| anchored, weighted, all3 | 4.49 (33) | 4.45 (32) | 4.41 (35) | 1.62 (3) | 52.55 | 0.0 | 113 / 523 | 4.10 | 0.39 | nan |
| native, full known, weighted, all3 | 4.17 (34) | 4.12 (35) | 4.00 (33) | 1.21 (1) | 194.48 | 0.0 | 113 / 523 | 3.51 | 0.66 | nan |
| anchored, stratified, all3 | 3.29 (12) | 3.25 (11) | 2.94 (9) | 2.06 (3) | 93.50 | 0.1 | 113 / 523 | 2.35 | 0.94 | nan |
| anchored, weighted, all5 | 4.49 (34) | 4.45 (33) | 4.44 (35) | 1.63 (2) | 52.86 | 0.0 | 113 / 523 | 4.10 | 0.39 | nan |
| native, full known, weighted, all5 | 4.09 (33) | 4.05 (33) | 3.96 (33) | 1.19 (1) | 204.53 | 0.0 | 113 / 523 | 3.44 | 0.64 | nan |
| anchored, stratified, all5 | 1.79 (0) | 1.78 (0) | 1.53 (0) | 1.38 (1) | 276.39 | 18.5 | 113 / 523 | 0.82 | 0.97 | nan |
| anchored, weighted, src2 | 4.48 (33) | 4.44 (32) | 4.40 (36) | 1.61 (2) | 52.58 | 0.0 | 113 / 523 | 4.08 | 0.40 | nan |
| native, full known, weighted, src2 | 4.13 (34) | 4.10 (34) | 3.96 (34) | 1.19 (1) | 198.86 | 0.0 | 113 / 523 | 3.44 | 0.70 | nan |
| anchored, stratified, src2 | 3.86 (23) | 3.84 (21) | 3.70 (21) | 2.29 (5) | 63.88 | 0.0 | 113 / 523 | 3.22 | 0.63 | nan |
| anchored, weighted, src3 | 4.48 (33) | 4.44 (33) | 4.41 (35) | 1.62 (3) | 52.65 | 0.0 | 113 / 523 | 4.08 | 0.40 | nan |
| native, full known, weighted, src3 | 4.13 (34) | 4.09 (33) | 3.98 (33) | 1.20 (1) | 196.65 | 0.0 | 113 / 523 | 3.48 | 0.64 | nan |
| anchored, stratified, src3 | 3.30 (12) | 3.27 (12) | 2.95 (11) | 2.05 (3) | 92.81 | 0.0 | 113 / 523 | 2.35 | 0.95 | nan |
| anchored, weighted, src5 | 4.47 (33) | 4.43 (33) | 4.40 (35) | 1.62 (3) | 53.16 | 0.0 | 113 / 523 | 4.08 | 0.39 | nan |
| native, full known, weighted, src5 | 4.05 (32) | 4.02 (33) | 3.92 (33) | 1.19 (1) | 209.31 | 0.0 | 113 / 523 | 3.40 | 0.65 | nan |
| anchored, stratified, src5 | 1.98 (0) | 1.95 (0) | 1.57 (0) | 1.38 (0) | 215.43 | 9.0 | 113 / 523 | 0.76 | 1.22 | nan |

## alpha = 0.1, dataset split

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 845 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 20.66 (100) | 20.73 (100) | 9.39 (23) | 6.44 (0) | 7.06 | 0.0 | 149 / 486 | 9.36 | 11.29 | 24.74 |
| anchored, image-level (paper) | 28.24 (100) | 28.29 (100) | 13.76 (100) | 9.87 (43) | 4.62 | 0.0 | 149 / 486 | 13.72 | 14.52 | 24.74 |
| anchored, both | 20.66 (100) | 20.73 (100) | 9.39 (23) | 6.44 (0) | 7.06 | 0.0 | 149 / 486 | 9.36 | 11.29 | 24.74 |
| native, full known, label-level | 22.52 (100) | 22.57 (100) | 9.37 (24) | 5.32 (0) | 7.08 | 0.0 | 149 / 486 | 9.37 | 13.15 | 26.18 |
| native, frozen at source, label-level | 32.60 (100) | 32.66 (100) | 15.19 (100) | 8.51 (0) | 4.12 | 0.0 | 149 / 486 | 9.36 | 23.23 | 36.66 |
| native, frozen at source, image-level | 47.98 (100) | 48.05 (100) | 25.18 (100) | 14.72 (100) | 2.21 | 0.0 | 149 / 486 | 17.52 | 30.46 | 36.66 |
| anchored, weighted, all2 | 7.53 (0) | 7.47 (0) | 2.50 (0) | 1.66 (0) | 26.84 | 0.0 | 149 / 486 | 2.51 | 5.02 | nan |
| native, full known, weighted, all2 | 6.35 (0) | 6.29 (0) | 2.38 (0) | 1.07 (0) | 46.14 | 0.0 | 149 / 486 | 2.38 | 3.97 | nan |
| anchored, stratified, all2 | 10.45 (70) | 10.44 (72) | 8.82 (9) | 7.25 (0) | 26.79 | 0.0 | 149 / 486 | 8.75 | 1.70 | nan |
| anchored, weighted, all3 | 5.86 (0) | 5.82 (0) | 1.90 (0) | 1.14 (0) | 34.81 | 0.0 | 149 / 486 | 1.88 | 3.99 | nan |
| native, full known, weighted, all3 | 7.58 (1) | 7.55 (0) | 2.74 (0) | 1.32 (0) | 33.50 | 0.0 | 149 / 486 | 2.75 | 4.84 | nan |
| anchored, stratified, all3 | 8.11 (1) | 8.10 (2) | 8.31 (3) | 7.25 (0) | 288.87 | 37.1 | 149 / 486 | 8.22 | -0.11 | nan |
| anchored, weighted, all5 | 5.21 (0) | 5.16 (0) | 1.64 (0) | 0.93 (0) | 38.55 | 0.0 | 149 / 486 | 1.64 | 3.57 | nan |
| native, full known, weighted, all5 | 5.63 (0) | 5.65 (0) | 3.73 (0) | 2.00 (0) | 188.78 | 20.3 | 149 / 486 | 3.72 | 1.91 | nan |
| anchored, stratified, all5 | 6.53 (0) | 6.55 (0) | 7.52 (0) | 8.40 (2) | 344.09 | 45.2 | 149 / 486 | 7.42 | -0.89 | nan |
| anchored, weighted, src2 | 14.97 (100) | 15.00 (100) | 6.18 (0) | 4.31 (0) | 10.96 | 0.0 | 149 / 486 | 6.17 | 8.80 | nan |
| native, full known, weighted, src2 | 14.35 (100) | 14.42 (100) | 5.43 (0) | 3.22 (0) | 13.23 | 0.0 | 149 / 486 | 5.41 | 8.94 | nan |
| anchored, stratified, src2 | 15.04 (100) | 15.05 (100) | 8.80 (7) | 9.75 (35) | 9.26 | 0.0 | 149 / 486 | 8.76 | 6.28 | nan |
| anchored, weighted, src3 | 12.74 (97) | 12.74 (97) | 5.10 (0) | 3.57 (0) | 13.73 | 0.0 | 149 / 486 | 5.07 | 7.67 | nan |
| native, full known, weighted, src3 | 11.76 (94) | 11.82 (94) | 4.42 (0) | 2.56 (0) | 17.19 | 0.0 | 149 / 486 | 4.38 | 7.38 | nan |
| anchored, stratified, src3 | 12.48 (97) | 12.47 (97) | 8.22 (0) | 9.03 (7) | 11.69 | 0.0 | 149 / 486 | 8.15 | 4.33 | nan |
| anchored, weighted, src5 | 9.65 (38) | 9.61 (39) | 3.64 (0) | 2.55 (0) | 19.25 | 0.0 | 149 / 486 | 3.62 | 6.03 | nan |
| native, full known, weighted, src5 | 9.46 (32) | 9.47 (33) | 3.55 (0) | 1.93 (0) | 23.48 | 0.0 | 149 / 486 | 3.54 | 5.92 | nan |
| anchored, stratified, src5 | 9.75 (43) | 9.71 (43) | 7.06 (0) | 9.43 (24) | 17.23 | 0.0 | 149 / 486 | 6.95 | 2.79 | nan |

## alpha = 0.05, dataset split

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 845 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 11.80 (100) | 11.79 (100) | 4.38 (11) | 2.96 (0) | 16.05 | 0.0 | 149 / 486 | 4.35 | 7.45 | 24.74 |
| anchored, image-level (paper) | 17.24 (100) | 17.31 (100) | 7.28 (100) | 4.89 (40) | 9.22 | 0.0 | 149 / 486 | 7.27 | 9.97 | 24.74 |
| anchored, both | 11.80 (100) | 11.79 (100) | 4.38 (11) | 2.96 (0) | 16.05 | 0.0 | 149 / 486 | 4.35 | 7.45 | 24.74 |
| native, full known, label-level | 12.11 (100) | 12.17 (100) | 4.38 (15) | 2.40 (0) | 17.38 | 0.0 | 149 / 486 | 4.35 | 7.75 | 26.18 |
| native, frozen at source, label-level | 19.44 (100) | 19.50 (100) | 7.78 (100) | 4.45 (8) | 8.75 | 0.0 | 149 / 486 | 4.35 | 15.09 | 36.66 |
| native, frozen at source, image-level | 30.96 (100) | 31.00 (100) | 14.19 (100) | 7.94 (100) | 4.46 | 0.0 | 149 / 486 | 8.66 | 22.30 | 36.66 |
| anchored, weighted, all2 | 3.46 (0) | 3.44 (0) | 0.85 (0) | 0.47 (0) | 66.08 | 0.0 | 149 / 486 | 0.82 | 2.64 | nan |
| native, full known, weighted, all2 | 0.80 (0) | 0.79 (0) | 0.38 (0) | 0.13 (0) | 486.46 | 0.0 | 149 / 486 | 0.38 | 0.42 | nan |
| anchored, stratified, all2 | 3.98 (2) | 3.98 (2) | 3.81 (3) | 2.65 (0) | 430.99 | 57.5 | 149 / 486 | 3.78 | 0.20 | nan |
| anchored, weighted, all3 | 2.59 (0) | 2.55 (0) | 0.57 (0) | 0.28 (0) | 87.36 | 0.0 | 149 / 486 | 0.56 | 2.02 | nan |
| native, full known, weighted, all3 | 1.59 (1) | 1.56 (1) | 0.53 (0) | 0.21 (0) | 366.42 | 0.0 | 149 / 486 | 0.49 | 1.10 | nan |
| anchored, stratified, all3 | 3.74 (1) | 3.71 (1) | 3.52 (0) | 2.73 (0) | 304.79 | 37.1 | 149 / 486 | 3.44 | 0.30 | nan |
| anchored, weighted, all5 | 1.67 (0) | 1.65 (0) | 0.49 (0) | 0.24 (0) | 233.79 | 21.7 | 149 / 486 | 0.48 | 1.20 | nan |
| native, full known, weighted, all5 | 2.16 (0) | 2.15 (0) | 1.16 (0) | 0.52 (0) | 277.13 | 20.3 | 149 / 486 | 1.11 | 1.05 | nan |
| anchored, stratified, all5 | 2.05 (0) | 2.01 (0) | 2.85 (0) | 3.38 (0) | 517.56 | 68.5 | 149 / 486 | 2.78 | -0.73 | nan |
| anchored, weighted, src2 | 8.04 (99) | 8.01 (99) | 2.59 (0) | 1.84 (0) | 26.75 | 0.0 | 149 / 486 | 2.59 | 5.44 | nan |
| native, full known, weighted, src2 | 7.35 (100) | 7.34 (100) | 2.27 (0) | 1.21 (0) | 36.67 | 0.0 | 149 / 486 | 2.27 | 5.09 | nan |
| anchored, stratified, src2 | 8.08 (100) | 8.03 (100) | 3.74 (1) | 4.03 (1) | 24.62 | 0.0 | 149 / 486 | 3.71 | 4.37 | nan |
| anchored, weighted, src3 | 6.43 (94) | 6.38 (90) | 2.06 (0) | 1.40 (0) | 33.86 | 0.0 | 149 / 486 | 2.04 | 4.38 | nan |
| native, full known, weighted, src3 | 5.72 (77) | 5.66 (75) | 1.78 (0) | 0.90 (0) | 53.95 | 0.0 | 149 / 486 | 1.77 | 3.96 | nan |
| anchored, stratified, src3 | 6.02 (92) | 5.98 (90) | 3.17 (0) | 3.29 (0) | 32.94 | 0.0 | 149 / 486 | 3.07 | 2.95 | nan |
| anchored, weighted, src5 | 4.61 (25) | 4.59 (28) | 1.38 (0) | 0.87 (0) | 47.84 | 0.0 | 149 / 486 | 1.35 | 3.26 | nan |
| native, full known, weighted, src5 | 4.03 (12) | 3.98 (10) | 1.22 (0) | 0.57 (0) | 130.70 | 0.0 | 149 / 486 | 1.19 | 2.84 | nan |
| anchored, stratified, src5 | 4.14 (8) | 4.10 (5) | 1.91 (0) | 2.25 (0) | 53.75 | 0.0 | 149 / 486 | 1.81 | 2.33 | nan |
