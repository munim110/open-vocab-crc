# A guarantee for the added labels under (weighted) label exchangeability

CAT-Seg (fcclip_bank683), 2000 COCO val2017 (LVIS-annotated) images with a labelled sampled pixel (1283-name vocabulary: 171 source names, then the LVIS v1 annotation mapped to the added names), 500 trials (random half/half image split; source vocabulary as per design). Label loss = pooled fraction of the label's sampled pixels whose score for it is below the threshold. "Added, cal" = mean over added labels present in the calibration images (the quantity the proposition bounds); "added, held-out" = same on the held-out images; "src, class" = class-averaged source loss on held-out images; "src, image" = image-level source risk (the paper's guarantee); size = labels per labelled pixel at 1283 names, held-out images; floor = % of added labels present whose threshold is the grid floor. Risks in % (and % of trials above alpha). Development data; nothing fitted.

## alpha = 0.1, exchangeable

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 1283 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 8.98 (32) | 8.99 (33) | 8.93 (32) | 9.18 (35) | 82.88 | 0.0 | 72 / 466 | 8.61 | 0.37 | 4.65 |
| anchored, image-level (paper) | 11.45 (51) | 11.44 (52) | 11.31 (52) | 9.80 (42) | 72.01 | 0.0 | 72 / 466 | 11.31 | 0.14 | 4.65 |
| anchored, both | 7.99 (21) | 7.98 (22) | 7.89 (21) | 7.25 (17) | 102.73 | 0.0 | 72 / 466 | 7.69 | 0.31 | 4.65 |
| native, full known, label-level | 9.13 (35) | 9.11 (35) | 9.12 (36) | 10.37 (43) | 66.06 | 0.0 | 72 / 466 | 8.63 | 0.50 | 4.75 |
| anchored, weighted, all2 | 8.98 (32) | 8.99 (33) | 8.95 (34) | 9.16 (35) | 82.87 | 0.0 | 72 / 466 | 8.64 | 0.34 | nan |
| native, full known, weighted, all2 | 9.14 (36) | 9.12 (35) | 9.19 (36) | 10.42 (43) | 65.68 | 0.0 | 72 / 466 | 8.67 | 0.46 | nan |
| anchored, stratified, all2 | 8.17 (23) | 8.11 (23) | 7.99 (22) | 9.98 (40) | 132.71 | 0.0 | 72 / 466 | 7.25 | 0.92 | nan |
| anchored, weighted, all3 | 8.96 (31) | 8.97 (34) | 8.95 (33) | 9.15 (35) | 83.14 | 0.0 | 72 / 466 | 8.63 | 0.33 | nan |
| native, full known, weighted, all3 | 9.12 (36) | 9.10 (34) | 9.18 (36) | 10.42 (43) | 66.10 | 0.0 | 72 / 466 | 8.66 | 0.46 | nan |
| anchored, stratified, all3 | 7.18 (11) | 7.17 (11) | 6.94 (13) | 10.68 (45) | 201.21 | 0.2 | 72 / 466 | 5.79 | 1.38 | nan |
| anchored, weighted, all5 | 8.93 (32) | 8.94 (32) | 8.94 (35) | 9.16 (36) | 83.60 | 0.0 | 72 / 466 | 8.62 | 0.32 | nan |
| native, full known, weighted, all5 | 9.09 (34) | 9.07 (33) | 9.16 (35) | 10.39 (43) | 66.74 | 0.0 | 72 / 466 | 8.65 | 0.44 | nan |
| anchored, stratified, all5 | 5.07 (1) | 5.04 (2) | 4.96 (1) | 9.04 (31) | 466.66 | 13.4 | 72 / 466 | 3.64 | 1.43 | nan |
| anchored, weighted, src2 | 8.96 (32) | 8.97 (33) | 8.92 (32) | 9.15 (35) | 83.06 | 0.0 | 72 / 466 | 8.62 | 0.34 | nan |
| native, full known, weighted, src2 | 9.10 (35) | 9.07 (35) | 9.15 (36) | 10.38 (43) | 66.19 | 0.0 | 72 / 466 | 8.63 | 0.47 | nan |
| anchored, stratified, src2 | 8.16 (23) | 8.11 (24) | 7.97 (22) | 9.93 (40) | 131.89 | 0.0 | 72 / 466 | 7.25 | 0.91 | nan |
| anchored, weighted, src3 | 8.94 (32) | 8.96 (33) | 8.91 (33) | 9.15 (35) | 83.38 | 0.0 | 72 / 466 | 8.61 | 0.33 | nan |
| native, full known, weighted, src3 | 9.07 (35) | 9.04 (33) | 9.11 (36) | 10.36 (42) | 66.88 | 0.0 | 72 / 466 | 8.61 | 0.46 | nan |
| anchored, stratified, src3 | 7.19 (11) | 7.19 (13) | 7.02 (12) | 10.97 (46) | 200.11 | 0.2 | 72 / 466 | 5.81 | 1.38 | nan |
| anchored, weighted, src5 | 8.90 (31) | 8.91 (32) | 8.90 (34) | 9.13 (35) | 84.20 | 0.0 | 72 / 466 | 8.57 | 0.33 | nan |
| native, full known, weighted, src5 | 9.05 (35) | 9.02 (33) | 9.14 (34) | 10.36 (42) | 67.18 | 0.0 | 72 / 466 | 8.62 | 0.43 | nan |
| anchored, stratified, src5 | 5.12 (1) | 5.10 (2) | 4.89 (1) | 9.08 (33) | 447.14 | 11.6 | 72 / 466 | 3.57 | 1.55 | nan |

## alpha = 0.05, exchangeable

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 1283 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 4.02 (26) | 4.02 (28) | 4.02 (27) | 3.52 (23) | 227.59 | 0.0 | 72 / 466 | 3.52 | 0.50 | 4.65 |
| anchored, image-level (paper) | 6.53 (63) | 6.52 (64) | 6.51 (63) | 4.88 (43) | 152.03 | 0.0 | 72 / 466 | 6.40 | 0.13 | 4.65 |
| anchored, both | 3.68 (20) | 3.68 (22) | 3.67 (23) | 2.90 (13) | 245.63 | 0.0 | 72 / 466 | 3.25 | 0.44 | 4.65 |
| native, full known, label-level | 4.09 (27) | 4.07 (28) | 4.11 (31) | 4.50 (32) | 186.35 | 0.0 | 72 / 466 | 3.50 | 0.59 | 4.75 |
| anchored, weighted, all2 | 4.02 (26) | 4.02 (28) | 4.07 (29) | 3.53 (22) | 227.02 | 0.0 | 72 / 466 | 3.54 | 0.48 | nan |
| native, full known, weighted, all2 | 4.09 (27) | 4.07 (27) | 4.13 (32) | 4.54 (33) | 186.01 | 0.0 | 72 / 466 | 3.53 | 0.56 | nan |
| anchored, stratified, all2 | 3.02 (11) | 2.98 (11) | 2.95 (13) | 3.53 (22) | 385.51 | 2.2 | 72 / 466 | 2.12 | 0.90 | nan |
| anchored, weighted, all3 | 4.01 (26) | 4.01 (28) | 4.06 (29) | 3.52 (23) | 226.99 | 0.0 | 72 / 466 | 3.53 | 0.48 | nan |
| native, full known, weighted, all3 | 4.09 (28) | 4.07 (26) | 4.13 (32) | 4.56 (33) | 186.27 | 0.0 | 72 / 466 | 3.52 | 0.56 | nan |
| anchored, stratified, all3 | 1.79 (1) | 1.78 (1) | 1.67 (2) | 3.54 (24) | 761.93 | 30.4 | 72 / 466 | 1.20 | 0.59 | nan |
| anchored, weighted, all5 | 3.99 (25) | 3.98 (27) | 4.04 (28) | 3.51 (23) | 231.12 | 0.0 | 72 / 466 | 3.54 | 0.45 | nan |
| native, full known, weighted, all5 | 4.05 (26) | 4.03 (28) | 4.12 (31) | 4.53 (33) | 188.93 | 0.0 | 72 / 466 | 3.52 | 0.54 | nan |
| anchored, stratified, all5 | 0.67 (0) | 0.66 (0) | 0.63 (0) | 1.51 (4) | 1064.54 | 61.5 | 72 / 466 | 0.43 | 0.24 | nan |
| anchored, weighted, src2 | 4.01 (26) | 4.02 (27) | 4.06 (28) | 3.53 (23) | 227.15 | 0.0 | 72 / 466 | 3.54 | 0.47 | nan |
| native, full known, weighted, src2 | 4.07 (27) | 4.04 (27) | 4.10 (31) | 4.52 (33) | 187.20 | 0.0 | 72 / 466 | 3.51 | 0.56 | nan |
| anchored, stratified, src2 | 3.05 (11) | 3.00 (10) | 2.95 (14) | 3.50 (22) | 374.62 | 1.5 | 72 / 466 | 2.11 | 0.93 | nan |
| anchored, weighted, src3 | 4.00 (25) | 4.00 (27) | 4.04 (28) | 3.52 (22) | 227.32 | 0.0 | 72 / 466 | 3.52 | 0.48 | nan |
| native, full known, weighted, src3 | 4.06 (26) | 4.04 (27) | 4.10 (33) | 4.53 (33) | 187.19 | 0.0 | 72 / 466 | 3.51 | 0.55 | nan |
| anchored, stratified, src3 | 1.78 (1) | 1.75 (0) | 1.66 (1) | 3.68 (25) | 759.23 | 29.7 | 72 / 466 | 1.20 | 0.58 | nan |
| anchored, weighted, src5 | 3.95 (25) | 3.94 (27) | 4.01 (28) | 3.49 (23) | 232.61 | 0.0 | 72 / 466 | 3.49 | 0.46 | nan |
| native, full known, weighted, src5 | 4.05 (26) | 4.03 (27) | 4.07 (31) | 4.52 (33) | 189.14 | 0.0 | 72 / 466 | 3.51 | 0.54 | nan |
| anchored, stratified, src5 | 0.68 (0) | 0.69 (0) | 0.62 (0) | 1.57 (2) | 1059.75 | 60.4 | 72 / 466 | 0.42 | 0.26 | nan |

## alpha = 0.1, dataset split

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 1283 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 16.61 (100) | 16.64 (100) | 9.41 (26) | 9.26 (14) | 31.08 | 0.0 | 170 / 367 | 9.44 | 7.17 | 38.16 |
| anchored, image-level (paper) | 17.79 (100) | 17.81 (100) | 10.02 (48) | 9.90 (42) | 27.18 | 0.0 | 170 / 367 | 10.07 | 7.72 | 38.16 |
| anchored, both | 16.58 (100) | 16.60 (100) | 9.39 (25) | 9.24 (12) | 31.19 | 0.0 | 170 / 367 | 9.42 | 7.16 | 38.16 |
| native, full known, label-level | 15.12 (100) | 15.21 (100) | 9.45 (28) | 9.91 (41) | 26.60 | 0.0 | 170 / 367 | 9.43 | 5.68 | 19.60 |
| native, frozen at source, label-level | 23.32 (100) | 23.37 (100) | 15.21 (100) | 16.21 (100) | 10.86 | 0.0 | 170 / 367 | 9.43 | 13.88 | 35.48 |
| native, frozen at source, image-level | 24.60 (100) | 24.66 (100) | 15.99 (100) | 17.10 (100) | 9.78 | 0.0 | 170 / 367 | 10.04 | 14.56 | 35.48 |
| anchored, weighted, all2 | 4.57 (0) | 4.57 (0) | 5.48 (0) | 5.59 (0) | 679.11 | 49.9 | 170 / 367 | 5.49 | -0.92 | nan |
| native, full known, weighted, all2 | 6.64 (0) | 6.69 (1) | 3.95 (0) | 4.13 (0) | 113.46 | 0.0 | 170 / 367 | 3.95 | 2.69 | nan |
| anchored, stratified, all2 | 7.13 (0) | 7.14 (0) | 9.13 (17) | 9.50 (24) | 658.70 | 49.9 | 170 / 367 | 9.15 | -2.02 | nan |
| anchored, weighted, all3 | 4.13 (0) | 4.20 (0) | 4.90 (0) | 4.88 (0) | 517.24 | 34.2 | 170 / 367 | 4.88 | -0.75 | nan |
| native, full known, weighted, all3 | 7.24 (1) | 7.29 (2) | 4.26 (0) | 4.47 (0) | 102.52 | 0.0 | 170 / 367 | 4.27 | 2.97 | nan |
| anchored, stratified, all3 | 3.31 (0) | 3.34 (0) | 8.96 (12) | 9.36 (17) | 868.28 | 69.6 | 170 / 367 | 8.97 | -5.66 | nan |
| anchored, weighted, all5 | 3.68 (0) | 3.67 (0) | 4.62 (0) | 4.51 (0) | 600.35 | 40.0 | 170 / 367 | 4.62 | -0.95 | nan |
| native, full known, weighted, all5 | 6.92 (1) | 6.94 (0) | 5.37 (0) | 5.72 (0) | 317.71 | 14.6 | 170 / 367 | 5.39 | 1.53 | nan |
| anchored, stratified, all5 | 1.76 (0) | 1.77 (0) | 8.61 (7) | 8.73 (4) | 820.90 | 60.0 | 170 / 367 | 8.61 | -6.85 | nan |
| anchored, weighted, src2 | 10.96 (82) | 10.98 (78) | 6.21 (0) | 6.20 (0) | 64.21 | 0.0 | 170 / 367 | 6.20 | 4.76 | nan |
| native, full known, weighted, src2 | 10.64 (70) | 10.68 (72) | 5.99 (0) | 6.55 (0) | 58.43 | 0.0 | 170 / 367 | 6.01 | 4.63 | nan |
| anchored, stratified, src2 | 10.95 (81) | 10.97 (78) | 8.89 (12) | 9.51 (21) | 61.80 | 0.0 | 170 / 367 | 8.90 | 2.05 | nan |
| anchored, weighted, src3 | 9.21 (24) | 9.22 (27) | 5.10 (0) | 4.94 (0) | 93.69 | 0.0 | 170 / 367 | 5.08 | 4.14 | nan |
| native, full known, weighted, src3 | 10.30 (60) | 10.33 (59) | 6.12 (0) | 6.62 (0) | 61.46 | 0.0 | 170 / 367 | 6.13 | 4.17 | nan |
| anchored, stratified, src3 | 9.20 (24) | 9.23 (28) | 8.38 (4) | 9.64 (29) | 90.62 | 0.0 | 170 / 367 | 8.37 | 0.83 | nan |
| anchored, weighted, src5 | 8.23 (6) | 8.28 (8) | 4.61 (0) | 4.40 (0) | 111.48 | 0.0 | 170 / 367 | 4.60 | 3.63 | nan |
| native, full known, weighted, src5 | 7.32 (3) | 7.36 (4) | 4.40 (0) | 4.67 (0) | 101.07 | 0.0 | 170 / 367 | 4.41 | 2.91 | nan |
| anchored, stratified, src5 | 8.03 (5) | 8.08 (5) | 7.38 (0) | 9.29 (13) | 111.64 | 0.0 | 170 / 367 | 7.31 | 0.71 | nan |

## alpha = 0.05, dataset split

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 1283 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 9.16 (100) | 9.17 (100) | 4.43 (24) | 4.13 (5) | 96.36 | 0.0 | 170 / 367 | 4.42 | 4.74 | 38.16 |
| anchored, image-level (paper) | 10.05 (100) | 10.05 (100) | 5.19 (61) | 4.90 (38) | 78.00 | 0.0 | 170 / 367 | 5.20 | 4.85 | 38.16 |
| anchored, both | 9.16 (100) | 9.17 (100) | 4.43 (24) | 4.13 (5) | 96.40 | 0.0 | 170 / 367 | 4.42 | 4.74 | 38.16 |
| native, full known, label-level | 8.09 (100) | 8.12 (100) | 4.41 (21) | 4.62 (25) | 89.84 | 0.0 | 170 / 367 | 4.42 | 3.66 | 19.60 |
| native, frozen at source, label-level | 13.45 (100) | 13.49 (100) | 8.02 (100) | 8.54 (100) | 35.10 | 0.0 | 170 / 367 | 4.42 | 9.03 | 35.48 |
| native, frozen at source, image-level | 14.90 (100) | 14.98 (100) | 9.33 (100) | 9.79 (100) | 27.16 | 0.0 | 170 / 367 | 5.25 | 9.65 | 35.48 |
| anchored, weighted, all2 | 3.29 (0) | 3.29 (1) | 3.58 (1) | 3.42 (1) | 703.42 | 49.9 | 170 / 367 | 3.59 | -0.30 | nan |
| native, full known, weighted, all2 | 2.30 (0) | 2.27 (0) | 1.70 (0) | 1.76 (0) | 273.17 | 0.0 | 170 / 367 | 1.71 | 0.59 | nan |
| anchored, stratified, all2 | 3.79 (3) | 3.79 (3) | 4.29 (18) | 4.19 (8) | 691.28 | 49.9 | 170 / 367 | 4.28 | -0.49 | nan |
| anchored, weighted, all3 | 1.12 (0) | 1.14 (0) | 2.84 (0) | 2.67 (0) | 905.36 | 69.6 | 170 / 367 | 2.86 | -1.74 | nan |
| native, full known, weighted, all3 | 3.09 (0) | 3.07 (0) | 1.83 (0) | 1.97 (0) | 231.31 | 0.0 | 170 / 367 | 1.83 | 1.25 | nan |
| anchored, stratified, all3 | 1.55 (0) | 1.57 (0) | 4.21 (15) | 4.13 (7) | 889.22 | 69.6 | 170 / 367 | 4.19 | -2.64 | nan |
| anchored, weighted, all5 | 1.28 (0) | 1.28 (0) | 2.43 (0) | 2.19 (0) | 845.80 | 60.0 | 170 / 367 | 2.44 | -1.16 | nan |
| native, full known, weighted, all5 | 3.04 (0) | 3.01 (0) | 2.23 (0) | 2.40 (0) | 413.67 | 14.6 | 170 / 367 | 2.20 | 0.84 | nan |
| anchored, stratified, all5 | 0.14 (0) | 0.14 (0) | 3.86 (9) | 3.37 (0) | 1044.25 | 89.5 | 170 / 367 | 3.79 | -3.66 | nan |
| anchored, weighted, src2 | 5.72 (75) | 5.76 (73) | 2.48 (0) | 2.28 (0) | 178.29 | 0.0 | 170 / 367 | 2.47 | 3.25 | nan |
| native, full known, weighted, src2 | 4.72 (35) | 4.71 (36) | 2.57 (0) | 2.80 (0) | 168.46 | 0.0 | 170 / 367 | 2.55 | 2.16 | nan |
| anchored, stratified, src2 | 5.69 (75) | 5.73 (73) | 3.88 (8) | 4.43 (18) | 173.12 | 0.0 | 170 / 367 | 3.85 | 1.83 | nan |
| anchored, weighted, src3 | 3.69 (13) | 3.73 (16) | 1.75 (0) | 1.55 (0) | 263.09 | 0.0 | 170 / 367 | 1.72 | 1.97 | nan |
| native, full known, weighted, src3 | 4.23 (18) | 4.23 (20) | 2.51 (0) | 2.71 (0) | 184.09 | 0.0 | 170 / 367 | 2.48 | 1.74 | nan |
| anchored, stratified, src3 | 3.63 (12) | 3.67 (15) | 3.31 (1) | 4.03 (6) | 257.33 | 0.0 | 170 / 367 | 3.28 | 0.35 | nan |
| anchored, weighted, src5 | 2.81 (3) | 2.82 (5) | 1.90 (0) | 1.60 (0) | 345.58 | 0.0 | 170 / 367 | 1.89 | 0.92 | nan |
| native, full known, weighted, src5 | 2.64 (0) | 2.65 (1) | 1.76 (0) | 1.92 (0) | 258.75 | 0.0 | 170 / 367 | 1.74 | 0.90 | nan |
| anchored, stratified, src5 | 2.56 (2) | 2.57 (2) | 2.44 (0) | 3.39 (0) | 382.05 | 0.0 | 170 / 367 | 2.18 | 0.38 | nan |
