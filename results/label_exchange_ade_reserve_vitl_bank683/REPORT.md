# A guarantee for the added labels under (weighted) label exchangeability

CAT-Seg (vitl_bank683), 2000 reserved ADE training images with a labelled sampled pixel (845-name vocabulary: 150 source names, then the A-847 annotation mapped to the added names), 500 trials (random half/half image split; source vocabulary as per design). Label loss = pooled fraction of the label's sampled pixels whose score for it is below the threshold. "Added, cal" = mean over added labels present in the calibration images (the quantity the proposition bounds); "added, held-out" = same on the held-out images; "src, class" = class-averaged source loss on held-out images; "src, image" = image-level source risk (the paper's guarantee); size = labels per labelled pixel at 845 names, held-out images; floor = % of added labels present whose threshold is the grid floor. Risks in % (and % of trials above alpha). Reserved images, read once under docs/PROTOCOL_ADDED_LABEL_RESERVE.md; nothing fitted.

## alpha = 0.1, exchangeable

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 845 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 9.33 (37) | 9.35 (39) | 9.06 (33) | 3.18 (1) | 26.20 | 0.0 | 90 / 417 | 8.92 | 0.41 | 3.67 |
| anchored, image-level (paper) | 23.07 (99) | 23.01 (99) | 22.64 (99) | 9.90 (44) | 7.24 | 0.0 | 90 / 417 | 22.97 | 0.11 | 3.67 |
| anchored, both | 9.32 (37) | 9.34 (39) | 9.05 (33) | 3.17 (1) | 26.22 | 0.0 | 90 / 417 | 8.91 | 0.41 | 3.67 |
| native, full known, label-level | 9.36 (39) | 9.36 (39) | 9.10 (33) | 2.80 (0) | 32.79 | 0.0 | 90 / 417 | 8.94 | 0.42 | 3.99 |
| anchored, weighted, all3 | 9.29 (35) | 9.31 (37) | 9.06 (34) | 3.18 (1) | 26.36 | 0.0 | 90 / 417 | 8.92 | 0.37 | nan |
| native, full known, weighted, all3 | 9.33 (38) | 9.32 (37) | 9.09 (34) | 2.82 (0) | 33.12 | 0.0 | 90 / 417 | 8.96 | 0.37 | nan |
| anchored, stratified, all3 | 7.83 (16) | 7.77 (14) | 7.62 (17) | 5.44 (6) | 41.79 | 0.0 | 90 / 417 | 6.83 | 1.00 | nan |

## alpha = 0.05, exchangeable

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 845 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 4.40 (34) | 4.35 (34) | 4.22 (32) | 1.17 (0) | 71.31 | 0.0 | 90 / 417 | 3.87 | 0.53 | 3.67 |
| anchored, image-level (paper) | 13.87 (100) | 13.88 (100) | 13.51 (99) | 4.91 (46) | 15.79 | 0.0 | 90 / 417 | 13.66 | 0.22 | 3.67 |
| anchored, both | 4.40 (34) | 4.35 (34) | 4.21 (31) | 1.17 (0) | 71.34 | 0.0 | 90 / 417 | 3.87 | 0.53 | 3.67 |
| native, full known, label-level | 4.21 (36) | 4.15 (33) | 3.94 (32) | 0.87 (0) | 200.26 | 0.0 | 90 / 417 | 3.40 | 0.81 | 3.99 |
| anchored, weighted, all3 | 4.37 (34) | 4.31 (33) | 4.20 (31) | 1.17 (0) | 71.56 | 0.0 | 90 / 417 | 3.85 | 0.51 | nan |
| native, full known, weighted, all3 | 4.23 (36) | 4.15 (33) | 4.00 (32) | 0.90 (0) | 201.30 | 0.0 | 90 / 417 | 3.44 | 0.79 | nan |
| anchored, stratified, all3 | 2.68 (6) | 2.68 (5) | 2.51 (5) | 1.81 (1) | 199.60 | 6.6 | 90 / 417 | 1.77 | 0.91 | nan |

## alpha = 0.1, dataset split

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 845 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 18.37 (100) | 18.30 (100) | 9.46 (33) | 4.07 (0) | 11.20 | 0.0 | 149 / 357 | 9.37 | 9.00 | 20.81 |
| anchored, image-level (paper) | 33.81 (100) | 33.59 (100) | 17.59 (100) | 9.86 (44) | 4.52 | 0.0 | 149 / 357 | 17.54 | 16.27 | 20.81 |
| anchored, both | 18.37 (100) | 18.30 (100) | 9.46 (33) | 4.07 (0) | 11.20 | 0.0 | 149 / 357 | 9.37 | 9.00 | 20.81 |
| native, full known, label-level | 20.02 (100) | 19.85 (100) | 9.43 (32) | 3.38 (0) | 11.70 | 0.0 | 149 / 357 | 9.38 | 10.64 | 23.77 |
| native, frozen at source, label-level | 30.44 (100) | 30.22 (100) | 14.70 (100) | 6.08 (0) | 6.16 | 0.0 | 149 / 357 | 9.37 | 21.07 | 34.33 |
| native, frozen at source, image-level | 52.42 (100) | 52.38 (100) | 30.09 (100) | 15.07 (100) | 2.26 | 0.0 | 149 / 357 | 21.10 | 31.32 | 34.33 |
| anchored, weighted, all3 | 6.45 (1) | 6.42 (1) | 3.33 (0) | 1.17 (0) | 38.67 | 0.0 | 149 / 357 | 3.23 | 3.22 | nan |
| native, full known, weighted, all3 | 9.35 (32) | 9.30 (26) | 4.33 (0) | 1.23 (0) | 36.79 | 0.0 | 149 / 357 | 4.22 | 5.13 | nan |
| anchored, stratified, all3 | 6.31 (0) | 6.34 (0) | 8.49 (13) | 5.42 (0) | 297.18 | 31.3 | 149 / 357 | 8.37 | -2.06 | nan |

## alpha = 0.05, dataset split

| Arm | Added, cal | Added, held-out | Src, class | Src, image | Size at 845 | Floor | Source / added labels present (cal) | Src, cal at t | Delta(t) | max Delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, label-level | 9.59 (100) | 9.55 (100) | 4.46 (29) | 1.43 (0) | 29.47 | 0.0 | 149 / 357 | 4.35 | 5.24 | 20.81 |
| anchored, image-level (paper) | 21.03 (100) | 20.92 (100) | 10.73 (100) | 4.90 (38) | 9.11 | 0.0 | 149 / 357 | 10.66 | 10.37 | 20.81 |
| anchored, both | 9.59 (100) | 9.55 (100) | 4.46 (29) | 1.43 (0) | 29.47 | 0.0 | 149 / 357 | 4.35 | 5.24 | 20.81 |
| native, full known, label-level | 9.76 (100) | 9.72 (100) | 4.46 (28) | 1.23 (0) | 35.34 | 0.0 | 149 / 357 | 4.35 | 5.41 | 23.77 |
| native, frozen at source, label-level | 17.61 (100) | 17.50 (100) | 8.31 (100) | 2.85 (0) | 14.15 | 0.0 | 149 / 357 | 4.35 | 13.27 | 34.33 |
| native, frozen at source, image-level | 37.01 (100) | 36.84 (100) | 18.70 (100) | 8.37 (100) | 4.32 | 0.0 | 149 / 357 | 12.23 | 24.78 | 34.33 |
| anchored, weighted, all3 | 1.95 (0) | 1.98 (0) | 2.01 (0) | 0.68 (0) | 326.73 | 31.3 | 149 / 357 | 1.94 | 0.00 | nan |
| native, full known, weighted, all3 | 4.16 (38) | 4.09 (35) | 1.68 (0) | 0.33 (0) | 213.64 | 0.0 | 149 / 357 | 1.48 | 2.68 | nan |
| anchored, stratified, all3 | 2.92 (0) | 2.93 (0) | 3.66 (8) | 1.80 (0) | 320.73 | 31.3 | 149 / 357 | 3.52 | -0.59 | nan |
