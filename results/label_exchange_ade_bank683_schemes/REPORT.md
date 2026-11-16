# A guarantee for the added labels under (weighted) label exchangeability

CAT-Seg (bank683), 2000 ADE validation images with a labelled sampled pixel (845-name vocabulary: 150 source names, then the A-847 annotation mapped to the added names), 500 trials (random half/half image split; source vocabulary as per design). Label loss = pooled fraction of the label's sampled pixels whose score for it is below the threshold. "Added, cal" = mean over added labels present in the calibration images (the quantity the proposition bounds); "added, held-out" = same on the held-out images; "src, class" = class-averaged source loss on held-out images; "src, image" = image-level source risk (the paper's guarantee); size = labels per labelled pixel at 845 names, held-out images; floor = % of added labels present whose threshold is the grid floor. Risks in % (and % of trials above alpha). Development data; nothing fitted.

## alpha = 0.1, exchangeable

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 845 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 9.53 (39) | 9.56 (39) | 9.48 (40) | 3.60 (2) | 46.36 | 0.0 | 113 / 523 | 9.14 | 0.39 | 3.55 |
| anchored, image-level (paper) | 24.78 (98) | 24.79 (97) | 24.57 (98) | 9.91 (49) | 14.61 | 0.0 | 113 / 523 | 24.45 | 0.33 | 3.55 |
| anchored, both | 9.50 (39) | 9.53 (39) | 9.46 (40) | 3.57 (1) | 46.49 | 0.0 | 113 / 523 | 9.12 | 0.39 | 3.55 |
| native, full known, label-level | 9.59 (40) | 9.53 (41) | 9.36 (38) | 3.27 (2) | 59.46 | 0.0 | 113 / 523 | 9.12 | 0.46 | 3.72 |
| anchored, weighted, all2 | 9.46 (38) | 9.48 (37) | 9.43 (41) | 3.59 (2) | 46.61 | 0.0 | 113 / 523 | 9.13 | 0.34 | nan |
| native, full known, weighted, all2 | 9.55 (41) | 9.50 (39) | 9.34 (38) | 3.28 (2) | 59.44 | 0.0 | 113 / 523 | 9.11 | 0.44 | nan |
| anchored, stratified, all2 | 8.98 (31) | 8.97 (30) | 8.92 (31) | 5.29 (3) | 45.78 | 0.0 | 113 / 523 | 8.31 | 0.67 | nan |
| anchored, weighted, all3 | 9.47 (39) | 9.49 (37) | 9.47 (40) | 3.59 (2) | 46.48 | 0.0 | 113 / 523 | 9.14 | 0.33 | nan |
| native, full known, weighted, all3 | 9.55 (39) | 9.50 (41) | 9.33 (39) | 3.29 (2) | 59.80 | 0.0 | 113 / 523 | 9.11 | 0.44 | nan |
| anchored, stratified, all3 | 8.36 (21) | 8.38 (21) | 8.18 (19) | 6.05 (8) | 50.80 | 0.0 | 113 / 523 | 7.47 | 0.89 | nan |
| anchored, weighted, all5 | 9.46 (39) | 9.48 (37) | 9.47 (41) | 3.60 (1) | 46.60 | 0.0 | 113 / 523 | 9.15 | 0.31 | nan |
| native, full known, weighted, all5 | 9.55 (42) | 9.48 (41) | 9.36 (39) | 3.28 (1) | 59.93 | 0.0 | 113 / 523 | 9.11 | 0.44 | nan |
| anchored, stratified, all5 | 7.14 (9) | 7.12 (8) | 6.86 (7) | 5.21 (4) | 72.68 | 0.0 | 113 / 523 | 5.81 | 1.33 | nan |
| anchored, weighted, src2 | 9.46 (39) | 9.49 (38) | 9.43 (42) | 3.60 (2) | 46.60 | 0.0 | 113 / 523 | 9.12 | 0.35 | nan |
| native, full known, weighted, src2 | 9.50 (40) | 9.44 (39) | 9.28 (37) | 3.26 (2) | 60.12 | 0.0 | 113 / 523 | 9.05 | 0.45 | nan |
| anchored, stratified, src2 | 8.97 (32) | 8.96 (30) | 8.92 (30) | 5.36 (4) | 45.44 | 0.0 | 113 / 523 | 8.30 | 0.66 | nan |
| anchored, weighted, src3 | 9.43 (39) | 9.46 (37) | 9.43 (39) | 3.58 (2) | 46.72 | 0.0 | 113 / 523 | 9.10 | 0.34 | nan |
| native, full known, weighted, src3 | 9.51 (38) | 9.44 (40) | 9.30 (38) | 3.27 (2) | 59.36 | 0.0 | 113 / 523 | 9.07 | 0.44 | nan |
| anchored, stratified, src3 | 8.39 (23) | 8.40 (23) | 8.22 (21) | 6.00 (7) | 50.82 | 0.0 | 113 / 523 | 7.47 | 0.92 | nan |
| anchored, weighted, src5 | 9.39 (38) | 9.40 (36) | 9.40 (38) | 3.57 (2) | 46.98 | 0.0 | 113 / 523 | 9.08 | 0.32 | nan |
| native, full known, weighted, src5 | 9.53 (41) | 9.47 (39) | 9.34 (40) | 3.29 (2) | 59.95 | 0.0 | 113 / 523 | 9.08 | 0.45 | nan |
| anchored, stratified, src5 | 7.17 (9) | 7.17 (8) | 6.91 (8) | 5.39 (4) | 70.04 | 0.0 | 113 / 523 | 5.81 | 1.36 | nan |

## alpha = 0.05, exchangeable

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 845 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 4.45 (34) | 4.46 (35) | 4.31 (31) | 1.50 (1) | 102.59 | 0.0 | 113 / 523 | 4.10 | 0.35 | 3.55 |
| anchored, image-level (paper) | 14.39 (98) | 14.35 (97) | 14.22 (97) | 4.94 (46) | 32.93 | 0.0 | 113 / 523 | 14.00 | 0.39 | 3.55 |
| anchored, both | 4.44 (34) | 4.45 (34) | 4.30 (31) | 1.49 (0) | 102.78 | 0.0 | 113 / 523 | 4.09 | 0.35 | 3.55 |
| native, full known, label-level | 3.37 (37) | 3.38 (37) | 3.05 (30) | 0.90 (1) | 430.08 | 0.0 | 113 / 523 | 2.46 | 0.91 | 3.72 |
| anchored, weighted, all2 | 4.42 (34) | 4.42 (34) | 4.30 (31) | 1.50 (1) | 103.22 | 0.0 | 113 / 523 | 4.09 | 0.32 | nan |
| native, full known, weighted, all2 | 3.33 (37) | 3.34 (38) | 3.05 (31) | 0.91 (1) | 431.92 | 0.0 | 113 / 523 | 2.45 | 0.88 | nan |
| anchored, stratified, all2 | 3.90 (20) | 3.87 (21) | 3.69 (18) | 2.11 (2) | 117.64 | 0.0 | 113 / 523 | 3.22 | 0.68 | nan |
| anchored, weighted, all3 | 4.42 (34) | 4.42 (35) | 4.33 (32) | 1.51 (1) | 103.09 | 0.0 | 113 / 523 | 4.12 | 0.31 | nan |
| native, full known, weighted, all3 | 3.29 (36) | 3.29 (36) | 2.97 (28) | 0.91 (1) | 440.03 | 0.0 | 113 / 523 | 2.42 | 0.87 | nan |
| anchored, stratified, all3 | 3.24 (10) | 3.24 (9) | 3.02 (8) | 2.22 (5) | 151.44 | 0.0 | 113 / 523 | 2.34 | 0.90 | nan |
| anchored, weighted, all5 | 4.42 (36) | 4.41 (35) | 4.33 (31) | 1.51 (1) | 103.80 | 0.0 | 113 / 523 | 4.12 | 0.30 | nan |
| native, full known, weighted, all5 | 3.24 (35) | 3.26 (35) | 3.02 (31) | 0.90 (2) | 446.26 | 0.0 | 113 / 523 | 2.41 | 0.83 | nan |
| anchored, stratified, all5 | 1.78 (1) | 1.77 (1) | 1.60 (1) | 1.22 (0) | 337.12 | 17.5 | 113 / 523 | 0.80 | 0.97 | nan |
| anchored, weighted, src2 | 4.41 (34) | 4.41 (33) | 4.29 (31) | 1.50 (1) | 103.26 | 0.0 | 113 / 523 | 4.09 | 0.32 | nan |
| native, full known, weighted, src2 | 3.27 (36) | 3.29 (36) | 2.99 (28) | 0.90 (1) | 440.38 | 0.0 | 113 / 523 | 2.39 | 0.88 | nan |
| anchored, stratified, src2 | 3.91 (21) | 3.86 (21) | 3.69 (18) | 2.12 (2) | 116.78 | 0.0 | 113 / 523 | 3.22 | 0.68 | nan |
| anchored, weighted, src3 | 4.40 (33) | 4.40 (34) | 4.30 (31) | 1.49 (1) | 103.65 | 0.0 | 113 / 523 | 4.08 | 0.32 | nan |
| native, full known, weighted, src3 | 3.20 (35) | 3.21 (35) | 2.89 (28) | 0.88 (1) | 449.81 | 0.0 | 113 / 523 | 2.34 | 0.86 | nan |
| anchored, stratified, src3 | 3.22 (11) | 3.22 (10) | 2.99 (7) | 2.20 (5) | 153.83 | 0.0 | 113 / 523 | 2.33 | 0.90 | nan |
| anchored, weighted, src5 | 4.38 (35) | 4.38 (34) | 4.31 (31) | 1.50 (1) | 104.32 | 0.0 | 113 / 523 | 4.09 | 0.29 | nan |
| native, full known, weighted, src5 | 3.22 (35) | 3.24 (36) | 2.98 (30) | 0.91 (1) | 448.79 | 0.0 | 113 / 523 | 2.38 | 0.83 | nan |
| anchored, stratified, src5 | 1.94 (1) | 1.94 (0) | 1.61 (1) | 1.34 (0) | 274.30 | 7.5 | 113 / 523 | 0.75 | 1.20 | nan |

## alpha = 0.1, dataset split

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 845 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 22.61 (100) | 22.62 (100) | 9.42 (25) | 4.29 (0) | 17.30 | 0.0 | 149 / 486 | 9.36 | 13.24 | 24.19 |
| anchored, image-level (paper) | 40.75 (100) | 40.78 (100) | 19.95 (100) | 9.88 (42) | 6.24 | 0.0 | 149 / 486 | 19.82 | 20.93 | 24.19 |
| anchored, both | 22.61 (100) | 22.62 (100) | 9.42 (25) | 4.29 (0) | 17.30 | 0.0 | 149 / 486 | 9.36 | 13.24 | 24.19 |
| native, full known, label-level | 22.31 (100) | 22.35 (100) | 9.41 (26) | 3.60 (0) | 19.80 | 0.0 | 149 / 486 | 9.37 | 12.94 | 27.65 |
| native, frozen at source, label-level | 35.69 (100) | 35.70 (100) | 16.13 (100) | 6.47 (0) | 9.15 | 0.0 | 149 / 486 | 9.37 | 26.32 | 37.89 |
| native, frozen at source, image-level | 60.11 (100) | 60.09 (100) | 33.02 (100) | 15.40 (100) | 2.77 | 0.0 | 149 / 486 | 23.26 | 36.85 | 37.89 |
| anchored, weighted, all2 | 7.62 (1) | 7.66 (1) | 2.56 (0) | 1.20 (0) | 60.90 | 0.0 | 149 / 486 | 2.53 | 5.08 | nan |
| native, full known, weighted, all2 | 8.54 (5) | 8.52 (5) | 2.94 (0) | 1.08 (0) | 71.45 | 0.0 | 149 / 486 | 2.93 | 5.61 | nan |
| anchored, stratified, all2 | 10.73 (84) | 10.77 (81) | 8.86 (14) | 4.01 (0) | 49.03 | 0.0 | 149 / 486 | 8.76 | 1.97 | nan |
| anchored, weighted, all3 | 5.47 (0) | 5.49 (0) | 1.70 (0) | 0.92 (0) | 79.21 | 0.0 | 149 / 486 | 1.67 | 3.80 | nan |
| native, full known, weighted, all3 | 9.37 (27) | 9.34 (26) | 3.51 (0) | 1.34 (0) | 62.55 | 0.0 | 149 / 486 | 3.48 | 5.89 | nan |
| anchored, stratified, all3 | 6.91 (0) | 6.93 (0) | 8.41 (8) | 4.83 (0) | 298.03 | 37.5 | 149 / 486 | 8.29 | -1.38 | nan |
| anchored, weighted, all5 | 6.50 (0) | 6.54 (0) | 2.10 (0) | 0.98 (0) | 69.95 | 0.0 | 149 / 486 | 2.08 | 4.43 | nan |
| native, full known, weighted, all5 | 6.42 (0) | 6.37 (0) | 4.02 (0) | 1.56 (0) | 214.05 | 21.5 | 149 / 486 | 3.99 | 2.44 | nan |
| anchored, stratified, all5 | 5.97 (0) | 5.97 (0) | 7.57 (0) | 4.48 (0) | 352.03 | 45.6 | 149 / 486 | 7.42 | -1.45 | nan |
| anchored, weighted, src2 | 15.85 (100) | 15.92 (100) | 6.11 (0) | 2.94 (0) | 27.36 | 0.0 | 149 / 486 | 6.07 | 9.79 | nan |
| native, full known, weighted, src2 | 13.95 (100) | 13.92 (100) | 5.42 (0) | 2.08 (0) | 37.56 | 0.0 | 149 / 486 | 5.37 | 8.58 | nan |
| anchored, stratified, src2 | 15.98 (100) | 16.04 (100) | 8.83 (10) | 5.82 (0) | 23.61 | 0.0 | 149 / 486 | 8.76 | 7.22 | nan |
| anchored, weighted, src3 | 13.64 (100) | 13.71 (100) | 5.08 (0) | 2.48 (0) | 32.98 | 0.0 | 149 / 486 | 5.05 | 8.58 | nan |
| native, full known, weighted, src3 | 11.44 (93) | 11.40 (91) | 4.07 (0) | 1.58 (0) | 49.41 | 0.0 | 149 / 486 | 4.04 | 7.40 | nan |
| anchored, stratified, src3 | 13.07 (100) | 13.15 (99) | 8.24 (1) | 6.89 (0) | 28.65 | 0.0 | 149 / 486 | 8.16 | 4.91 | nan |
| anchored, weighted, src5 | 10.64 (71) | 10.71 (76) | 3.81 (0) | 1.85 (0) | 43.27 | 0.0 | 149 / 486 | 3.78 | 6.86 | nan |
| native, full known, weighted, src5 | 8.64 (7) | 8.62 (7) | 3.09 (0) | 1.16 (0) | 69.94 | 0.0 | 149 / 486 | 3.08 | 5.56 | nan |
| anchored, stratified, src5 | 9.96 (49) | 10.01 (51) | 7.11 (0) | 7.23 (0) | 39.20 | 0.0 | 149 / 486 | 6.95 | 3.01 | nan |

## alpha = 0.05, dataset split

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 845 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 12.69 (100) | 12.76 (100) | 4.38 (13) | 2.10 (0) | 37.90 | 0.0 | 149 / 486 | 4.35 | 8.34 | 24.19 |
| anchored, image-level (paper) | 24.99 (100) | 24.98 (100) | 10.71 (100) | 4.90 (40) | 14.78 | 0.0 | 149 / 486 | 10.66 | 14.33 | 24.19 |
| anchored, both | 12.69 (100) | 12.76 (100) | 4.38 (13) | 2.10 (0) | 37.90 | 0.0 | 149 / 486 | 4.35 | 8.34 | 24.19 |
| native, full known, label-level | 12.29 (100) | 12.25 (100) | 4.38 (12) | 1.66 (0) | 46.35 | 0.0 | 149 / 486 | 4.35 | 7.94 | 27.65 |
| native, frozen at source, label-level | 21.85 (100) | 21.87 (100) | 9.18 (100) | 3.50 (0) | 20.38 | 0.0 | 149 / 486 | 4.34 | 17.50 | 37.89 |
| native, frozen at source, image-level | 41.83 (100) | 41.89 (100) | 19.77 (100) | 8.16 (100) | 6.66 | 0.0 | 149 / 486 | 12.14 | 29.69 | 37.89 |
| anchored, weighted, all2 | 3.68 (1) | 3.68 (1) | 0.91 (0) | 0.42 (0) | 112.73 | 0.0 | 149 / 486 | 0.88 | 2.80 | nan |
| native, full known, weighted, all2 | 0.40 (0) | 0.41 (0) | 0.11 (0) | 0.03 (0) | 749.26 | 0.0 | 149 / 486 | 0.11 | 0.30 | nan |
| anchored, stratified, all2 | 3.77 (1) | 3.78 (0) | 3.81 (3) | 1.62 (0) | 441.34 | 57.9 | 149 / 486 | 3.78 | -0.01 | nan |
| anchored, weighted, all3 | 1.28 (0) | 1.26 (0) | 0.61 (0) | 0.41 (0) | 370.77 | 37.5 | 149 / 486 | 0.61 | 0.67 | nan |
| native, full known, weighted, all3 | 0.44 (0) | 0.42 (0) | 0.29 (0) | 0.09 (0) | 689.65 | 0.0 | 149 / 486 | 0.29 | 0.15 | nan |
| anchored, stratified, all3 | 2.84 (0) | 2.86 (0) | 3.54 (0) | 1.95 (0) | 321.80 | 37.5 | 149 / 486 | 3.47 | -0.63 | nan |
| anchored, weighted, all5 | 3.23 (0) | 3.21 (0) | 0.76 (0) | 0.32 (0) | 129.84 | 0.0 | 149 / 486 | 0.72 | 2.50 | nan |
| native, full known, weighted, all5 | 0.85 (0) | 0.83 (0) | 0.64 (0) | 0.26 (0) | 575.20 | 21.5 | 149 / 486 | 0.60 | 0.25 | nan |
| anchored, stratified, all5 | 2.28 (0) | 2.26 (0) | 2.77 (0) | 1.76 (0) | 401.31 | 45.7 | 149 / 486 | 2.71 | -0.43 | nan |
| anchored, weighted, src2 | 8.05 (100) | 8.10 (100) | 2.54 (0) | 1.27 (0) | 62.38 | 0.0 | 149 / 486 | 2.52 | 5.53 | nan |
| native, full known, weighted, src2 | 7.22 (100) | 7.21 (100) | 2.24 (0) | 0.83 (0) | 99.49 | 0.0 | 149 / 486 | 2.24 | 4.97 | nan |
| anchored, stratified, src2 | 7.78 (100) | 7.84 (100) | 3.77 (1) | 2.40 (0) | 57.28 | 0.0 | 149 / 486 | 3.71 | 4.08 | nan |
| anchored, weighted, src3 | 6.37 (96) | 6.38 (96) | 2.02 (0) | 1.01 (0) | 74.36 | 0.0 | 149 / 486 | 2.00 | 4.37 | nan |
| native, full known, weighted, src3 | 3.13 (42) | 3.13 (41) | 1.05 (0) | 0.38 (0) | 402.71 | 0.0 | 149 / 486 | 0.92 | 2.22 | nan |
| anchored, stratified, src3 | 5.88 (90) | 5.91 (90) | 3.15 (0) | 2.39 (0) | 68.16 | 0.0 | 149 / 486 | 3.07 | 2.81 | nan |
| anchored, weighted, src5 | 5.09 (56) | 5.10 (56) | 1.42 (0) | 0.72 (0) | 89.31 | 0.0 | 149 / 486 | 1.40 | 3.69 | nan |
| native, full known, weighted, src5 | 0.24 (0) | 0.23 (0) | 0.15 (0) | 0.06 (0) | 749.17 | 0.0 | 149 / 486 | 0.15 | 0.09 | nan |
| anchored, stratified, src5 | 4.29 (13) | 4.28 (12) | 1.90 (0) | 1.74 (0) | 91.26 | 0.0 | 149 / 486 | 1.81 | 2.49 | nan |
