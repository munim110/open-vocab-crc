# A guarantee for the added labels under (weighted) label exchangeability

CAT-Seg (fcclip_bank683), 2000 ADE validation images with a labelled sampled pixel (845-name vocabulary: 150 source names, then the A-847 annotation mapped to the added names), 500 trials (random half/half image split; source vocabulary as per design). Label loss = pooled fraction of the label's sampled pixels whose score for it is below the threshold. "Added, cal" = mean over added labels present in the calibration images (the quantity the proposition bounds); "added, held-out" = same on the held-out images; "src, class" = class-averaged source loss on held-out images; "src, image" = image-level source risk (the paper's guarantee); size = labels per labelled pixel at 845 names, held-out images; floor = % of added labels present whose threshold is the grid floor. Risks in % (and % of trials above alpha). Development data; nothing fitted.

## alpha = 0.1, exchangeable

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 845 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 9.55 (40) | 9.50 (40) | 9.29 (38) | 5.37 (11) | 61.01 | 0.0 | 113 / 523 | 9.12 | 0.43 | 4.10 |
| anchored, image-level (paper) | 17.12 (88) | 17.15 (86) | 16.89 (86) | 9.81 (42) | 31.67 | 0.0 | 113 / 523 | 16.91 | 0.21 | 4.10 |
| anchored, both | 9.16 (37) | 9.11 (36) | 8.91 (34) | 4.96 (6) | 66.33 | 0.0 | 113 / 523 | 8.77 | 0.40 | 4.10 |
| native, full known, label-level | 9.55 (41) | 9.54 (40) | 9.25 (36) | 4.62 (9) | 65.65 | 0.0 | 113 / 523 | 9.10 | 0.45 | 4.18 |
| anchored, weighted, all2 | 9.53 (39) | 9.48 (40) | 9.29 (37) | 5.38 (12) | 61.21 | 0.0 | 113 / 523 | 9.10 | 0.43 | nan |
| native, full known, weighted, all2 | 9.47 (39) | 9.46 (40) | 9.19 (35) | 4.61 (9) | 66.29 | 0.0 | 113 / 523 | 9.05 | 0.42 | nan |
| anchored, stratified, all2 | 8.91 (29) | 8.86 (31) | 8.66 (26) | 6.54 (15) | 69.29 | 0.0 | 113 / 523 | 8.25 | 0.65 | nan |
| anchored, weighted, all3 | 9.51 (40) | 9.44 (39) | 9.25 (37) | 5.37 (11) | 61.41 | 0.0 | 113 / 523 | 9.09 | 0.42 | nan |
| native, full known, weighted, all3 | 9.47 (39) | 9.45 (40) | 9.21 (37) | 4.61 (9) | 66.42 | 0.0 | 113 / 523 | 9.04 | 0.43 | nan |
| anchored, stratified, all3 | 8.33 (22) | 8.28 (19) | 8.00 (17) | 6.89 (18) | 79.56 | 0.0 | 113 / 523 | 7.41 | 0.92 | nan |
| anchored, weighted, all5 | 9.53 (41) | 9.48 (39) | 9.31 (37) | 5.40 (11) | 61.32 | 0.0 | 113 / 523 | 9.13 | 0.40 | nan |
| native, full known, weighted, all5 | 9.42 (39) | 9.40 (39) | 9.16 (35) | 4.59 (9) | 66.87 | 0.0 | 113 / 523 | 9.01 | 0.41 | nan |
| anchored, stratified, all5 | 7.08 (8) | 7.07 (9) | 6.64 (6) | 6.45 (14) | 106.76 | 0.1 | 113 / 523 | 5.72 | 1.36 | nan |
| anchored, weighted, src2 | 9.51 (40) | 9.46 (40) | 9.26 (36) | 5.37 (12) | 61.37 | 0.0 | 113 / 523 | 9.07 | 0.43 | nan |
| native, full known, weighted, src2 | 9.45 (39) | 9.44 (40) | 9.17 (35) | 4.59 (9) | 66.44 | 0.0 | 113 / 523 | 9.03 | 0.42 | nan |
| anchored, stratified, src2 | 8.86 (29) | 8.82 (28) | 8.61 (25) | 6.41 (13) | 69.51 | 0.0 | 113 / 523 | 8.26 | 0.60 | nan |
| anchored, weighted, src3 | 9.46 (39) | 9.41 (39) | 9.21 (36) | 5.35 (11) | 61.92 | 0.0 | 113 / 523 | 9.05 | 0.42 | nan |
| native, full known, weighted, src3 | 9.42 (38) | 9.40 (39) | 9.15 (36) | 4.58 (9) | 66.84 | 0.0 | 113 / 523 | 8.98 | 0.44 | nan |
| anchored, stratified, src3 | 8.23 (20) | 8.17 (19) | 7.94 (18) | 6.92 (17) | 80.04 | 0.0 | 113 / 523 | 7.41 | 0.82 | nan |
| anchored, weighted, src5 | 9.45 (39) | 9.39 (38) | 9.23 (37) | 5.35 (11) | 62.02 | 0.0 | 113 / 523 | 9.04 | 0.41 | nan |
| native, full known, weighted, src5 | 9.40 (37) | 9.38 (40) | 9.15 (35) | 4.59 (9) | 67.10 | 0.0 | 113 / 523 | 8.99 | 0.40 | nan |
| anchored, stratified, src5 | 7.15 (8) | 7.13 (9) | 6.65 (6) | 6.52 (16) | 104.93 | 0.0 | 113 / 523 | 5.69 | 1.45 | nan |

## alpha = 0.05, exchangeable

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 845 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 4.55 (36) | 4.50 (36) | 4.29 (30) | 2.44 (12) | 142.17 | 0.0 | 113 / 523 | 4.07 | 0.47 | 4.10 |
| anchored, image-level (paper) | 10.22 (85) | 10.21 (84) | 9.91 (83) | 4.86 (41) | 72.60 | 0.0 | 113 / 523 | 10.01 | 0.21 | 4.10 |
| anchored, both | 4.32 (33) | 4.27 (33) | 4.05 (27) | 2.10 (6) | 150.25 | 0.0 | 113 / 523 | 3.88 | 0.44 | 4.10 |
| native, full known, label-level | 4.57 (35) | 4.53 (35) | 4.35 (29) | 2.06 (9) | 152.43 | 0.0 | 113 / 523 | 4.07 | 0.50 | 4.18 |
| anchored, weighted, all2 | 4.50 (36) | 4.45 (35) | 4.28 (29) | 2.45 (12) | 142.85 | 0.0 | 113 / 523 | 4.06 | 0.44 | nan |
| native, full known, weighted, all2 | 4.54 (36) | 4.49 (35) | 4.33 (30) | 2.06 (9) | 153.41 | 0.0 | 113 / 523 | 4.04 | 0.51 | nan |
| anchored, stratified, all2 | 3.93 (23) | 3.88 (21) | 3.70 (20) | 2.55 (11) | 157.38 | 0.0 | 113 / 523 | 3.17 | 0.76 | nan |
| anchored, weighted, all3 | 4.48 (35) | 4.44 (36) | 4.25 (30) | 2.44 (12) | 143.54 | 0.0 | 113 / 523 | 4.05 | 0.42 | nan |
| native, full known, weighted, all3 | 4.53 (35) | 4.49 (34) | 4.33 (30) | 2.06 (9) | 153.71 | 0.0 | 113 / 523 | 4.05 | 0.47 | nan |
| anchored, stratified, all3 | 3.21 (11) | 3.20 (8) | 2.99 (8) | 2.31 (8) | 192.46 | 0.0 | 113 / 523 | 2.26 | 0.95 | nan |
| anchored, weighted, all5 | 4.49 (37) | 4.44 (35) | 4.27 (30) | 2.46 (12) | 143.46 | 0.0 | 113 / 523 | 4.07 | 0.42 | nan |
| native, full known, weighted, all5 | 4.51 (34) | 4.46 (34) | 4.33 (30) | 2.06 (10) | 154.53 | 0.0 | 113 / 523 | 4.03 | 0.48 | nan |
| anchored, stratified, all5 | 1.70 (0) | 1.67 (0) | 1.58 (0) | 1.55 (1) | 384.59 | 19.3 | 113 / 523 | 0.81 | 0.89 | nan |
| anchored, weighted, src2 | 4.50 (36) | 4.45 (35) | 4.28 (29) | 2.45 (12) | 142.90 | 0.0 | 113 / 523 | 4.06 | 0.44 | nan |
| native, full known, weighted, src2 | 4.54 (36) | 4.49 (35) | 4.32 (30) | 2.06 (9) | 153.50 | 0.0 | 113 / 523 | 4.04 | 0.50 | nan |
| anchored, stratified, src2 | 3.87 (22) | 3.84 (21) | 3.65 (18) | 2.45 (9) | 158.75 | 0.0 | 113 / 523 | 3.17 | 0.70 | nan |
| anchored, weighted, src3 | 4.45 (36) | 4.41 (34) | 4.23 (30) | 2.43 (12) | 144.13 | 0.0 | 113 / 523 | 4.02 | 0.43 | nan |
| native, full known, weighted, src3 | 4.50 (33) | 4.46 (33) | 4.30 (30) | 2.05 (9) | 154.23 | 0.0 | 113 / 523 | 4.01 | 0.49 | nan |
| anchored, stratified, src3 | 3.21 (9) | 3.19 (10) | 2.96 (8) | 2.32 (7) | 190.23 | 0.0 | 113 / 523 | 2.27 | 0.94 | nan |
| anchored, weighted, src5 | 4.45 (35) | 4.40 (35) | 4.24 (29) | 2.44 (12) | 144.38 | 0.0 | 113 / 523 | 4.04 | 0.41 | nan |
| native, full known, weighted, src5 | 4.48 (33) | 4.43 (33) | 4.30 (31) | 2.05 (9) | 155.28 | 0.0 | 113 / 523 | 4.02 | 0.46 | nan |
| anchored, stratified, src5 | 1.87 (1) | 1.85 (1) | 1.56 (0) | 1.59 (2) | 344.30 | 11.8 | 113 / 523 | 0.75 | 1.12 | nan |

## alpha = 0.1, dataset split

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 845 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 16.35 (100) | 16.36 (100) | 9.36 (27) | 5.36 (0) | 27.82 | 0.0 | 149 / 486 | 9.36 | 6.99 | 15.10 |
| anchored, image-level (paper) | 25.32 (100) | 25.29 (100) | 16.50 (100) | 9.85 (43) | 11.53 | 0.0 | 149 / 486 | 16.55 | 8.77 | 15.10 |
| anchored, both | 16.35 (100) | 16.36 (100) | 9.36 (27) | 5.36 (0) | 27.82 | 0.0 | 149 / 486 | 9.36 | 6.99 | 15.10 |
| native, full known, label-level | 18.32 (100) | 18.34 (100) | 9.36 (26) | 4.77 (0) | 26.65 | 0.0 | 149 / 486 | 9.37 | 8.95 | 15.40 |
| native, frozen at source, label-level | 24.70 (100) | 24.64 (100) | 13.98 (100) | 6.97 (0) | 13.80 | 0.0 | 149 / 486 | 9.35 | 15.34 | 21.97 |
| native, frozen at source, image-level | 38.36 (100) | 38.15 (100) | 24.02 (100) | 13.75 (100) | 5.24 | 0.0 | 149 / 486 | 17.97 | 20.38 | 21.97 |
| anchored, weighted, all2 | 9.13 (23) | 9.06 (22) | 5.06 (0) | 2.96 (0) | 69.87 | 0.0 | 149 / 486 | 5.03 | 4.10 | nan |
| native, full known, weighted, all2 | 12.69 (98) | 12.67 (98) | 6.17 (0) | 3.39 (0) | 48.03 | 0.0 | 149 / 486 | 6.18 | 6.51 | nan |
| anchored, stratified, all2 | 10.78 (78) | 10.80 (76) | 8.80 (11) | 6.32 (0) | 68.76 | 0.0 | 149 / 486 | 8.76 | 2.02 | nan |
| anchored, weighted, all3 | 10.96 (80) | 10.89 (76) | 6.31 (0) | 3.58 (0) | 53.27 | 0.0 | 149 / 486 | 6.30 | 4.66 | nan |
| native, full known, weighted, all3 | 11.61 (93) | 11.61 (91) | 5.57 (0) | 3.11 (0) | 53.98 | 0.0 | 149 / 486 | 5.54 | 6.07 | nan |
| anchored, stratified, all3 | 11.30 (87) | 11.25 (87) | 8.22 (3) | 6.96 (0) | 64.04 | 0.0 | 149 / 486 | 8.15 | 3.15 | nan |
| anchored, weighted, all5 | 7.36 (1) | 7.27 (0) | 6.55 (0) | 3.76 (0) | 213.52 | 22.1 | 149 / 486 | 6.54 | 0.81 | nan |
| native, full known, weighted, all5 | 13.12 (99) | 13.11 (100) | 6.58 (0) | 3.59 (0) | 44.74 | 0.0 | 149 / 486 | 6.58 | 6.53 | nan |
| anchored, stratified, all5 | 6.02 (0) | 6.01 (0) | 7.67 (0) | 7.13 (0) | 240.65 | 22.1 | 149 / 486 | 7.53 | -1.52 | nan |
| anchored, weighted, src2 | 11.44 (89) | 11.37 (86) | 6.58 (0) | 3.74 (0) | 49.97 | 0.0 | 149 / 486 | 6.58 | 4.87 | nan |
| native, full known, weighted, src2 | 13.83 (100) | 13.81 (100) | 6.72 (0) | 3.67 (0) | 43.07 | 0.0 | 149 / 486 | 6.72 | 7.11 | nan |
| anchored, stratified, src2 | 10.84 (76) | 10.78 (74) | 8.78 (11) | 7.65 (0) | 51.14 | 0.0 | 149 / 486 | 8.76 | 2.09 | nan |
| anchored, weighted, src3 | 9.22 (24) | 9.15 (24) | 5.15 (0) | 3.03 (0) | 69.26 | 0.0 | 149 / 486 | 5.13 | 4.09 | nan |
| native, full known, weighted, src3 | 12.36 (98) | 12.35 (97) | 5.97 (0) | 3.33 (0) | 49.89 | 0.0 | 149 / 486 | 5.97 | 6.39 | nan |
| anchored, stratified, src3 | 9.28 (22) | 9.24 (20) | 8.25 (4) | 8.41 (1) | 66.58 | 0.0 | 149 / 486 | 8.14 | 1.14 | nan |
| anchored, weighted, src5 | 14.88 (100) | 14.85 (100) | 9.47 (31) | 5.64 (0) | 30.80 | 0.0 | 149 / 486 | 9.48 | 5.40 | nan |
| native, full known, weighted, src5 | 11.73 (95) | 11.71 (93) | 5.69 (0) | 3.19 (0) | 52.86 | 0.0 | 149 / 486 | 5.67 | 6.06 | nan |
| anchored, stratified, src5 | 12.74 (99) | 12.71 (98) | 7.05 (0) | 7.06 (0) | 42.27 | 0.0 | 149 / 486 | 6.95 | 5.79 | nan |

## alpha = 0.05, dataset split

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 845 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 7.98 (100) | 7.91 (100) | 4.37 (19) | 2.63 (0) | 84.75 | 0.0 | 149 / 486 | 4.34 | 3.64 | 15.10 |
| anchored, image-level (paper) | 15.21 (100) | 15.19 (100) | 8.56 (100) | 4.88 (41) | 31.81 | 0.0 | 149 / 486 | 8.58 | 6.63 | 15.10 |
| anchored, both | 7.98 (100) | 7.91 (100) | 4.37 (19) | 2.63 (0) | 84.75 | 0.0 | 149 / 486 | 4.34 | 3.64 | 15.10 |
| native, full known, label-level | 9.66 (100) | 9.61 (100) | 4.38 (21) | 2.53 (0) | 72.61 | 0.0 | 149 / 486 | 4.35 | 5.32 | 15.40 |
| native, frozen at source, label-level | 14.70 (100) | 14.71 (100) | 7.11 (99) | 3.77 (0) | 40.27 | 0.0 | 149 / 486 | 4.34 | 10.36 | 21.97 |
| native, frozen at source, image-level | 24.19 (100) | 24.13 (100) | 13.57 (100) | 6.76 (100) | 14.55 | 0.0 | 149 / 486 | 9.07 | 15.12 | 21.97 |
| anchored, weighted, all2 | 4.22 (15) | 4.19 (15) | 2.21 (0) | 1.62 (0) | 151.27 | 0.0 | 149 / 486 | 2.16 | 2.06 | nan |
| native, full known, weighted, all2 | 6.19 (91) | 6.15 (90) | 2.71 (0) | 1.69 (0) | 120.04 | 0.0 | 149 / 486 | 2.65 | 3.54 | nan |
| anchored, stratified, all2 | 5.24 (63) | 5.23 (61) | 3.77 (2) | 2.24 (0) | 148.68 | 0.0 | 149 / 486 | 3.70 | 1.54 | nan |
| anchored, weighted, all3 | 5.15 (57) | 5.13 (53) | 2.70 (0) | 1.93 (0) | 131.99 | 0.0 | 149 / 486 | 2.64 | 2.51 | nan |
| native, full known, weighted, all3 | 5.66 (81) | 5.60 (76) | 2.36 (0) | 1.50 (0) | 131.62 | 0.0 | 149 / 486 | 2.32 | 3.35 | nan |
| anchored, stratified, all3 | 4.01 (9) | 4.00 (8) | 3.14 (0) | 2.22 (0) | 169.53 | 0.0 | 149 / 486 | 3.06 | 0.95 | nan |
| anchored, weighted, all5 | 2.95 (0) | 2.93 (0) | 2.74 (0) | 2.00 (0) | 282.64 | 22.1 | 149 / 486 | 2.67 | 0.28 | nan |
| native, full known, weighted, all5 | 6.12 (89) | 6.05 (86) | 2.96 (0) | 1.83 (0) | 116.96 | 0.0 | 149 / 486 | 2.90 | 3.23 | nan |
| anchored, stratified, all5 | 2.62 (0) | 2.61 (0) | 2.70 (0) | 2.29 (0) | 423.97 | 43.2 | 149 / 486 | 2.64 | -0.02 | nan |
| anchored, weighted, src2 | 5.49 (70) | 5.46 (69) | 2.81 (0) | 1.99 (0) | 126.59 | 0.0 | 149 / 486 | 2.75 | 2.73 | nan |
| native, full known, weighted, src2 | 6.75 (98) | 6.70 (98) | 3.01 (0) | 1.89 (0) | 110.88 | 0.0 | 149 / 486 | 2.95 | 3.79 | nan |
| anchored, stratified, src2 | 5.11 (56) | 5.06 (52) | 3.75 (4) | 3.01 (0) | 124.42 | 0.0 | 149 / 486 | 3.71 | 1.41 | nan |
| anchored, weighted, src3 | 4.06 (13) | 4.04 (11) | 2.16 (0) | 1.63 (0) | 154.72 | 0.0 | 149 / 486 | 2.11 | 1.96 | nan |
| native, full known, weighted, src3 | 6.08 (89) | 6.03 (90) | 2.60 (0) | 1.67 (0) | 123.96 | 0.0 | 149 / 486 | 2.55 | 3.52 | nan |
| anchored, stratified, src3 | 3.90 (6) | 3.85 (3) | 3.11 (0) | 2.85 (0) | 148.50 | 0.0 | 149 / 486 | 3.07 | 0.84 | nan |
| anchored, weighted, src5 | 5.92 (77) | 5.85 (78) | 4.76 (35) | 2.95 (0) | 106.77 | 0.0 | 149 / 486 | 4.73 | 1.19 | nan |
| native, full known, weighted, src5 | 5.71 (81) | 5.65 (79) | 2.39 (0) | 1.54 (0) | 130.62 | 0.0 | 149 / 486 | 2.34 | 3.37 | nan |
| anchored, stratified, src5 | 3.57 (11) | 3.55 (9) | 1.99 (0) | 1.68 (0) | 166.54 | 0.0 | 149 / 486 | 1.78 | 1.79 | nan |
