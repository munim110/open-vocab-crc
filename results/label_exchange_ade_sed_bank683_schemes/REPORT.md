# A guarantee for the added labels under (weighted) label exchangeability

CAT-Seg (sed_bank683), 2000 ADE validation images with a labelled sampled pixel (845-name vocabulary: 150 source names, then the A-847 annotation mapped to the added names), 500 trials (random half/half image split; source vocabulary as per design). Label loss = pooled fraction of the label's sampled pixels whose score for it is below the threshold. "Added, cal" = mean over added labels present in the calibration images (the quantity the proposition bounds); "added, held-out" = same on the held-out images; "src, class" = class-averaged source loss on held-out images; "src, image" = image-level source risk (the paper's guarantee); size = labels per labelled pixel at 845 names, held-out images; floor = % of added labels present whose threshold is the grid floor. Risks in % (and % of trials above alpha). Development data; nothing fitted.

## alpha = 0.1, exchangeable

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 845 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 9.51 (42) | 9.50 (42) | 9.22 (38) | 4.13 (7) | 45.10 | 0.0 | 113 / 523 | 9.14 | 0.37 | 3.63 |
| anchored, image-level (paper) | 21.66 (90) | 21.72 (90) | 21.54 (92) | 9.90 (45) | 16.79 | 0.0 | 113 / 523 | 21.54 | 0.12 | 3.63 |
| anchored, both | 9.29 (39) | 9.29 (39) | 9.01 (35) | 3.93 (4) | 46.95 | 0.0 | 113 / 523 | 8.94 | 0.35 | 3.63 |
| native, full known, label-level | 9.52 (41) | 9.51 (40) | 9.23 (36) | 3.86 (5) | 51.38 | 0.0 | 113 / 523 | 9.15 | 0.37 | 3.74 |
| anchored, weighted, all2 | 9.45 (41) | 9.45 (41) | 9.21 (38) | 4.13 (7) | 45.20 | 0.0 | 113 / 523 | 9.12 | 0.32 | nan |
| native, full known, weighted, all2 | 9.44 (40) | 9.45 (40) | 9.18 (38) | 3.85 (5) | 51.66 | 0.0 | 113 / 523 | 9.11 | 0.33 | nan |
| anchored, stratified, all2 | 8.96 (30) | 8.93 (33) | 8.68 (25) | 7.09 (16) | 42.51 | 0.0 | 113 / 523 | 8.29 | 0.66 | nan |
| anchored, weighted, all3 | 9.42 (40) | 9.42 (40) | 9.19 (37) | 4.13 (7) | 45.45 | 0.0 | 113 / 523 | 9.10 | 0.32 | nan |
| native, full known, weighted, all3 | 9.40 (40) | 9.40 (39) | 9.15 (36) | 3.85 (5) | 52.04 | 0.0 | 113 / 523 | 9.09 | 0.31 | nan |
| anchored, stratified, all3 | 8.42 (23) | 8.39 (23) | 8.14 (21) | 7.03 (14) | 53.60 | 0.0 | 113 / 523 | 7.48 | 0.94 | nan |
| anchored, weighted, all5 | 9.38 (41) | 9.37 (40) | 9.19 (37) | 4.11 (7) | 45.68 | 0.0 | 113 / 523 | 9.09 | 0.29 | nan |
| native, full known, weighted, all5 | 9.40 (41) | 9.39 (39) | 9.19 (37) | 3.85 (5) | 52.05 | 0.0 | 113 / 523 | 9.11 | 0.29 | nan |
| anchored, stratified, all5 | 7.12 (7) | 7.12 (9) | 6.79 (7) | 6.35 (10) | 74.35 | 0.0 | 113 / 523 | 5.81 | 1.30 | nan |
| anchored, weighted, src2 | 9.42 (39) | 9.42 (41) | 9.18 (37) | 4.12 (7) | 45.41 | 0.0 | 113 / 523 | 9.10 | 0.32 | nan |
| native, full known, weighted, src2 | 9.43 (40) | 9.43 (39) | 9.17 (37) | 3.85 (5) | 51.66 | 0.0 | 113 / 523 | 9.11 | 0.33 | nan |
| anchored, stratified, src2 | 8.93 (32) | 8.91 (33) | 8.69 (26) | 7.03 (16) | 42.72 | 0.0 | 113 / 523 | 8.28 | 0.65 | nan |
| anchored, weighted, src3 | 9.39 (39) | 9.39 (39) | 9.17 (37) | 4.13 (7) | 45.55 | 0.0 | 113 / 523 | 9.07 | 0.32 | nan |
| native, full known, weighted, src3 | 9.40 (41) | 9.40 (39) | 9.15 (36) | 3.85 (5) | 52.10 | 0.0 | 113 / 523 | 9.08 | 0.31 | nan |
| anchored, stratified, src3 | 8.33 (22) | 8.30 (22) | 8.11 (21) | 6.95 (15) | 51.96 | 0.0 | 113 / 523 | 7.47 | 0.87 | nan |
| anchored, weighted, src5 | 9.32 (39) | 9.32 (39) | 9.13 (36) | 4.09 (7) | 46.02 | 0.0 | 113 / 523 | 9.03 | 0.29 | nan |
| native, full known, weighted, src5 | 9.33 (39) | 9.32 (38) | 9.13 (37) | 3.82 (5) | 52.53 | 0.0 | 113 / 523 | 9.04 | 0.28 | nan |
| anchored, stratified, src5 | 7.08 (7) | 7.08 (9) | 6.73 (7) | 6.52 (10) | 71.84 | 0.0 | 113 / 523 | 5.81 | 1.27 | nan |

## alpha = 0.05, exchangeable

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 845 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 4.55 (36) | 4.55 (37) | 4.27 (31) | 1.73 (7) | 118.47 | 0.0 | 113 / 523 | 4.10 | 0.45 | 3.63 |
| anchored, image-level (paper) | 13.04 (88) | 13.04 (88) | 12.67 (89) | 4.90 (46) | 39.10 | 0.0 | 113 / 523 | 12.75 | 0.29 | 3.63 |
| anchored, both | 4.48 (34) | 4.48 (35) | 4.18 (29) | 1.59 (5) | 120.54 | 0.0 | 113 / 523 | 4.03 | 0.45 | 3.63 |
| native, full known, label-level | 4.55 (36) | 4.54 (37) | 4.26 (30) | 1.39 (2) | 139.80 | 0.0 | 113 / 523 | 4.09 | 0.46 | 3.74 |
| anchored, weighted, all2 | 4.51 (36) | 4.50 (35) | 4.25 (31) | 1.73 (7) | 119.26 | 0.0 | 113 / 523 | 4.08 | 0.44 | nan |
| native, full known, weighted, all2 | 4.49 (36) | 4.48 (35) | 4.24 (31) | 1.38 (3) | 141.63 | 0.0 | 113 / 523 | 4.07 | 0.42 | nan |
| anchored, stratified, all2 | 3.93 (22) | 3.92 (23) | 3.65 (17) | 2.78 (10) | 125.94 | 0.0 | 113 / 523 | 3.22 | 0.71 | nan |
| anchored, weighted, all3 | 4.48 (37) | 4.48 (36) | 4.24 (30) | 1.74 (7) | 120.58 | 0.0 | 113 / 523 | 4.06 | 0.42 | nan |
| native, full known, weighted, all3 | 4.46 (35) | 4.45 (34) | 4.23 (30) | 1.38 (3) | 142.28 | 0.0 | 113 / 523 | 4.07 | 0.39 | nan |
| anchored, stratified, all3 | 3.28 (13) | 3.26 (14) | 2.97 (7) | 2.40 (5) | 164.55 | 0.0 | 113 / 523 | 2.35 | 0.93 | nan |
| anchored, weighted, all5 | 4.46 (36) | 4.46 (36) | 4.25 (31) | 1.71 (7) | 120.92 | 0.0 | 113 / 523 | 4.06 | 0.40 | nan |
| native, full known, weighted, all5 | 4.47 (35) | 4.46 (34) | 4.27 (31) | 1.39 (3) | 142.61 | 0.0 | 113 / 523 | 4.08 | 0.40 | nan |
| anchored, stratified, all5 | 1.81 (0) | 1.78 (0) | 1.54 (0) | 1.46 (1) | 334.95 | 17.4 | 113 / 523 | 0.82 | 0.99 | nan |
| anchored, weighted, src2 | 4.51 (36) | 4.50 (36) | 4.25 (31) | 1.73 (7) | 119.41 | 0.0 | 113 / 523 | 4.07 | 0.44 | nan |
| native, full known, weighted, src2 | 4.49 (35) | 4.48 (36) | 4.23 (30) | 1.38 (3) | 141.73 | 0.0 | 113 / 523 | 4.07 | 0.42 | nan |
| anchored, stratified, src2 | 3.92 (23) | 3.91 (23) | 3.66 (17) | 2.75 (9) | 127.13 | 0.0 | 113 / 523 | 3.22 | 0.71 | nan |
| anchored, weighted, src3 | 4.47 (35) | 4.47 (35) | 4.23 (31) | 1.73 (7) | 120.80 | 0.0 | 113 / 523 | 4.06 | 0.41 | nan |
| native, full known, weighted, src3 | 4.47 (35) | 4.46 (34) | 4.23 (28) | 1.39 (3) | 141.78 | 0.0 | 113 / 523 | 4.07 | 0.39 | nan |
| anchored, stratified, src3 | 3.23 (12) | 3.22 (14) | 2.98 (8) | 2.36 (4) | 162.09 | 0.0 | 113 / 523 | 2.34 | 0.89 | nan |
| anchored, weighted, src5 | 4.43 (35) | 4.42 (34) | 4.20 (29) | 1.71 (7) | 121.33 | 0.0 | 113 / 523 | 4.02 | 0.41 | nan |
| native, full known, weighted, src5 | 4.43 (34) | 4.42 (34) | 4.22 (30) | 1.38 (3) | 143.78 | 0.0 | 113 / 523 | 4.04 | 0.39 | nan |
| anchored, stratified, src5 | 1.94 (0) | 1.95 (1) | 1.52 (0) | 1.59 (1) | 275.75 | 7.5 | 113 / 523 | 0.74 | 1.20 | nan |

## alpha = 0.1, dataset split

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 845 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 22.20 (100) | 22.20 (100) | 9.43 (28) | 5.35 (0) | 14.10 | 0.0 | 149 / 486 | 9.37 | 12.83 | 20.67 |
| anchored, image-level (paper) | 34.11 (100) | 34.13 (100) | 17.30 (100) | 9.87 (42) | 6.32 | 0.0 | 149 / 486 | 17.24 | 16.86 | 20.67 |
| anchored, both | 22.20 (100) | 22.20 (100) | 9.43 (28) | 5.35 (0) | 14.10 | 0.0 | 149 / 486 | 9.37 | 12.83 | 20.67 |
| native, full known, label-level | 21.92 (100) | 21.89 (100) | 9.42 (26) | 4.96 (0) | 15.91 | 0.0 | 149 / 486 | 9.37 | 12.55 | 24.92 |
| native, frozen at source, label-level | 16.76 (100) | 16.71 (100) | 6.93 (0) | 3.75 (0) | 25.13 | 0.0 | 149 / 486 | 9.37 | 7.39 | 12.82 |
| native, frozen at source, image-level | 30.70 (100) | 30.69 (100) | 14.23 (100) | 7.11 (0) | 8.89 | 0.0 | 149 / 486 | 19.86 | 10.85 | 12.82 |
| anchored, weighted, all2 | 10.70 (71) | 10.68 (70) | 3.93 (0) | 2.90 (0) | 38.93 | 0.0 | 149 / 486 | 3.90 | 6.80 | nan |
| native, full known, weighted, all2 | 8.74 (8) | 8.72 (8) | 3.03 (0) | 1.87 (0) | 60.31 | 0.0 | 149 / 486 | 3.01 | 5.73 | nan |
| anchored, stratified, all2 | 10.83 (78) | 10.83 (76) | 8.79 (9) | 6.28 (0) | 32.67 | 0.0 | 149 / 486 | 8.77 | 2.06 | nan |
| anchored, weighted, all3 | 8.71 (12) | 8.68 (11) | 2.82 (0) | 2.30 (0) | 52.21 | 0.0 | 149 / 486 | 2.81 | 5.90 | nan |
| native, full known, weighted, all3 | 6.78 (0) | 6.76 (0) | 1.99 (0) | 1.25 (0) | 79.43 | 0.0 | 149 / 486 | 1.97 | 4.81 | nan |
| anchored, stratified, all3 | 9.31 (21) | 9.31 (22) | 8.25 (2) | 6.26 (0) | 49.37 | 0.0 | 149 / 486 | 8.16 | 1.15 | nan |
| anchored, weighted, all5 | 7.70 (1) | 7.67 (1) | 2.41 (0) | 2.03 (0) | 58.78 | 0.0 | 149 / 486 | 2.41 | 5.28 | nan |
| native, full known, weighted, all5 | 7.69 (1) | 7.68 (1) | 2.41 (0) | 1.54 (0) | 70.08 | 0.0 | 149 / 486 | 2.40 | 5.29 | nan |
| anchored, stratified, all5 | 5.56 (0) | 5.52 (0) | 7.35 (0) | 6.59 (0) | 211.86 | 22.0 | 149 / 486 | 7.16 | -1.60 | nan |
| anchored, weighted, src2 | 15.53 (100) | 15.52 (100) | 6.18 (0) | 3.92 (0) | 24.00 | 0.0 | 149 / 486 | 6.13 | 9.40 | nan |
| native, full known, weighted, src2 | 14.28 (100) | 14.26 (100) | 5.97 (0) | 3.40 (0) | 30.52 | 0.0 | 149 / 486 | 5.93 | 8.35 | nan |
| anchored, stratified, src2 | 15.35 (100) | 15.34 (100) | 8.83 (9) | 8.42 (1) | 19.63 | 0.0 | 149 / 486 | 8.77 | 6.59 | nan |
| anchored, weighted, src3 | 12.53 (98) | 12.52 (98) | 4.56 (0) | 3.23 (0) | 33.43 | 0.0 | 149 / 486 | 4.52 | 8.02 | nan |
| native, full known, weighted, src3 | 11.64 (95) | 11.63 (93) | 4.57 (0) | 2.73 (0) | 41.84 | 0.0 | 149 / 486 | 4.51 | 7.13 | nan |
| anchored, stratified, src3 | 11.81 (95) | 11.78 (93) | 8.22 (2) | 8.71 (5) | 27.37 | 0.0 | 149 / 486 | 8.16 | 3.65 | nan |
| anchored, weighted, src5 | 10.88 (76) | 10.84 (75) | 3.89 (0) | 2.91 (0) | 39.21 | 0.0 | 149 / 486 | 3.86 | 7.02 | nan |
| native, full known, weighted, src5 | 9.27 (18) | 9.25 (18) | 3.25 (0) | 2.02 (0) | 57.26 | 0.0 | 149 / 486 | 3.22 | 6.05 | nan |
| anchored, stratified, src5 | 9.51 (32) | 9.48 (32) | 7.05 (0) | 9.52 (24) | 33.53 | 0.0 | 149 / 486 | 6.96 | 2.55 | nan |

## alpha = 0.05, dataset split

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 845 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 12.72 (100) | 12.71 (100) | 4.40 (16) | 3.09 (0) | 35.04 | 0.0 | 149 / 486 | 4.35 | 8.37 | 20.67 |
| anchored, image-level (paper) | 20.45 (100) | 20.43 (100) | 8.49 (100) | 4.89 (42) | 16.17 | 0.0 | 149 / 486 | 8.45 | 12.00 | 20.67 |
| anchored, both | 12.72 (100) | 12.71 (100) | 4.40 (16) | 3.09 (0) | 35.04 | 0.0 | 149 / 486 | 4.35 | 8.37 | 20.67 |
| native, full known, label-level | 11.63 (100) | 11.61 (100) | 4.41 (17) | 2.61 (0) | 44.79 | 0.0 | 149 / 486 | 4.35 | 7.28 | 24.92 |
| native, frozen at source, label-level | 9.18 (100) | 9.16 (100) | 2.96 (0) | 1.92 (0) | 63.58 | 0.0 | 149 / 486 | 4.35 | 4.83 | 12.82 |
| native, frozen at source, image-level | 16.84 (100) | 16.81 (100) | 6.96 (100) | 3.78 (0) | 24.96 | 0.0 | 149 / 486 | 9.45 | 7.39 | 12.82 |
| anchored, weighted, all2 | 5.08 (52) | 5.10 (55) | 1.36 (0) | 1.30 (0) | 91.60 | 0.0 | 149 / 486 | 1.33 | 3.76 | nan |
| native, full known, weighted, all2 | 4.44 (20) | 4.44 (22) | 1.02 (0) | 0.67 (0) | 125.71 | 0.0 | 149 / 486 | 0.97 | 3.47 | nan |
| anchored, stratified, all2 | 4.86 (44) | 4.85 (41) | 3.77 (4) | 2.06 (0) | 97.15 | 0.0 | 149 / 486 | 3.71 | 1.15 | nan |
| anchored, weighted, all3 | 4.42 (16) | 4.44 (19) | 0.92 (0) | 0.89 (0) | 108.95 | 0.0 | 149 / 486 | 0.88 | 3.54 | nan |
| native, full known, weighted, all3 | 2.87 (0) | 2.85 (0) | 0.57 (0) | 0.31 (0) | 182.47 | 0.0 | 149 / 486 | 0.57 | 2.31 | nan |
| anchored, stratified, all3 | 2.85 (0) | 2.82 (0) | 3.38 (1) | 2.21 (0) | 315.97 | 37.9 | 149 / 486 | 3.31 | -0.46 | nan |
| anchored, weighted, all5 | 3.96 (4) | 3.97 (4) | 0.73 (0) | 0.65 (0) | 119.62 | 0.0 | 149 / 486 | 0.71 | 3.25 | nan |
| native, full known, weighted, all5 | 3.92 (5) | 3.91 (4) | 0.79 (0) | 0.49 (0) | 143.57 | 0.0 | 149 / 486 | 0.75 | 3.17 | nan |
| anchored, stratified, all5 | 1.51 (0) | 1.50 (0) | 2.67 (0) | 2.32 (0) | 527.31 | 69.0 | 149 / 486 | 2.65 | -1.14 | nan |
| anchored, weighted, src2 | 8.31 (100) | 8.28 (100) | 2.48 (0) | 2.23 (0) | 59.61 | 0.0 | 149 / 486 | 2.47 | 5.84 | nan |
| native, full known, weighted, src2 | 8.34 (100) | 8.33 (100) | 2.44 (0) | 1.70 (0) | 70.01 | 0.0 | 149 / 486 | 2.42 | 5.93 | nan |
| anchored, stratified, src2 | 7.84 (100) | 7.85 (100) | 3.73 (2) | 3.74 (0) | 51.95 | 0.0 | 149 / 486 | 3.71 | 4.14 | nan |
| anchored, weighted, src3 | 6.56 (97) | 6.55 (97) | 1.74 (0) | 1.76 (0) | 76.40 | 0.0 | 149 / 486 | 1.72 | 4.84 | nan |
| native, full known, weighted, src3 | 7.08 (99) | 7.07 (99) | 1.78 (0) | 1.33 (0) | 83.95 | 0.0 | 149 / 486 | 1.78 | 5.31 | nan |
| anchored, stratified, src3 | 5.92 (88) | 5.92 (88) | 3.17 (0) | 3.17 (0) | 64.46 | 0.0 | 149 / 486 | 3.08 | 2.84 | nan |
| anchored, weighted, src5 | 5.33 (66) | 5.34 (66) | 1.37 (0) | 1.40 (0) | 90.00 | 0.0 | 149 / 486 | 1.34 | 3.99 | nan |
| native, full known, weighted, src5 | 5.28 (61) | 5.25 (63) | 1.14 (0) | 0.86 (0) | 110.55 | 0.0 | 149 / 486 | 1.12 | 4.16 | nan |
| anchored, stratified, src5 | 4.37 (13) | 4.40 (16) | 1.97 (0) | 2.42 (0) | 91.93 | 0.0 | 149 / 486 | 1.80 | 2.57 | nan |
