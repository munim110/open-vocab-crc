# Added-label guarantee from m randomly drawn, annotated names

vitl_bank683, 2000 COCO val2017 (LVIS-annotated) images, 1283-name vocabulary (171 source names), 500 trials. m = drawn added names; m' = drawn names present in the calibration images (the calibration labels). Added = mean loss over the remaining added labels present (cal: calibration images, the proposition's quantity; held-out: other half). Src, image = image-level source risk (source names at the image-level threshold). Size = labels per labelled pixel at the grown vocabulary, held-out images. Floor = % of trials whose added-name threshold is the grid floor. Risks in % (and % of trials above alpha). Development data; nothing fitted.

## alpha = 0.1

| Arm | m' | Added, cal | Added, held-out | Src, image | Size | Floor |
|---|---:|---:|---:|---:|---:|---:|
| check: random S of T | 71.5 | 8.93 (33) | 9.02 (34) | 2.16 (0) | 11.93 | 0.0 |
| check: dataset split | 170.1 | 17.60 (100) | 17.67 (100) | 4.48 (0) | 6.29 | 0.0 |
| source classes (benchmark split), per-label | 170.1 | 17.60 (100) | 17.67 (100) | 9.87 (42) | 4.86 | 0.0 |
| anchored, m=10 | 3.2 | 0.00 (0) | 0.00 (0) | 9.87 (42) | 1114.05 | 100.0 |
| native at grown vocabulary, m=10 | 3.2 | 0.00 (0) | 0.00 (0) | 9.89 (41) | 1114.07 | 100.0 |
| anchored, m=20 | 6.5 | 0.56 (1) | 0.54 (2) | 9.87 (42) | 946.93 | 83.8 |
| native at grown vocabulary, m=20 | 6.5 | 0.57 (1) | 0.57 (1) | 9.89 (41) | 970.67 | 83.8 |
| anchored, m=30 | 9.8 | 3.00 (7) | 3.02 (7) | 9.87 (42) | 387.81 | 31.0 |
| native at grown vocabulary, m=30 | 9.8 | 3.10 (8) | 3.17 (8) | 9.89 (41) | 493.39 | 31.0 |
| anchored, m=50 | 16.5 | 6.02 (17) | 6.06 (18) | 9.87 (42) | 39.91 | 0.6 |
| native at grown vocabulary, m=50 | 16.5 | 6.18 (18) | 6.23 (19) | 9.89 (41) | 124.71 | 0.6 |
| anchored, m=75 | 24.7 | 7.37 (23) | 7.36 (25) | 9.87 (42) | 18.83 | 0.0 |
| native at grown vocabulary, m=75 | 24.7 | 7.41 (26) | 7.44 (25) | 9.89 (41) | 47.37 | 0.0 |
| anchored, m=100 | 32.9 | 7.93 (26) | 7.98 (28) | 9.87 (42) | 13.67 | 0.0 |
| native at grown vocabulary, m=100 | 32.9 | 7.96 (27) | 8.05 (30) | 9.89 (41) | 20.20 | 0.0 |
| anchored, m=150 | 49.4 | 8.74 (32) | 8.86 (33) | 9.87 (42) | 10.74 | 0.0 |
| native at grown vocabulary, m=150 | 49.4 | 8.71 (32) | 8.83 (34) | 9.89 (41) | 13.04 | 0.0 |
| anchored, m=200 | 65.9 | 8.98 (35) | 9.12 (35) | 9.87 (42) | 9.92 | 0.0 |
| native at grown vocabulary, m=200 | 65.9 | 9.01 (34) | 9.14 (36) | 9.89 (41) | 11.59 | 0.0 |

## alpha = 0.05

| Arm | m' | Added, cal | Added, held-out | Src, image | Size | Floor |
|---|---:|---:|---:|---:|---:|---:|
| check: random S of T | 71.5 | 4.01 (27) | 4.06 (28) | 0.76 (0) | 30.23 | 0.0 |
| check: dataset split | 170.1 | 8.92 (100) | 9.01 (100) | 1.66 (0) | 13.25 | 0.0 |
| source classes (benchmark split), per-label | 170.1 | 8.92 (100) | 9.01 (100) | 4.91 (43) | 10.30 | 0.0 |
| anchored, m=10 | 3.2 | 0.00 (0) | 0.00 (0) | 4.91 (43) | 1115.29 | 100.0 |
| native at grown vocabulary, m=10 | 3.2 | 0.00 (0) | 0.00 (0) | 4.92 (40) | 1115.28 | 100.0 |
| anchored, m=20 | 6.5 | 0.00 (0) | 0.00 (0) | 4.91 (43) | 1115.29 | 100.0 |
| native at grown vocabulary, m=20 | 6.5 | 0.00 (0) | 0.00 (0) | 4.92 (40) | 1115.28 | 100.0 |
| anchored, m=30 | 9.8 | 0.00 (0) | 0.00 (0) | 4.91 (43) | 1115.29 | 100.0 |
| native at grown vocabulary, m=30 | 9.8 | 0.00 (0) | 0.00 (0) | 4.92 (40) | 1115.28 | 100.0 |
| anchored, m=50 | 16.5 | 0.52 (2) | 0.51 (2) | 4.91 (43) | 825.47 | 71.0 |
| native at grown vocabulary, m=50 | 16.5 | 0.52 (2) | 0.54 (3) | 4.92 (40) | 905.82 | 71.0 |
| anchored, m=75 | 24.7 | 2.40 (11) | 2.46 (12) | 4.91 (43) | 147.19 | 7.0 |
| native at grown vocabulary, m=75 | 24.7 | 2.50 (15) | 2.58 (15) | 4.92 (40) | 301.74 | 7.0 |
| anchored, m=100 | 32.9 | 3.02 (18) | 3.07 (18) | 4.91 (43) | 59.31 | 0.0 |
| native at grown vocabulary, m=100 | 32.9 | 3.06 (22) | 3.12 (20) | 4.92 (40) | 214.56 | 0.0 |
| anchored, m=150 | 49.4 | 3.71 (26) | 3.79 (25) | 4.91 (43) | 35.82 | 0.0 |
| native at grown vocabulary, m=150 | 49.4 | 3.77 (28) | 3.83 (27) | 4.92 (40) | 84.74 | 0.0 |
| anchored, m=200 | 65.9 | 3.99 (28) | 4.09 (30) | 4.91 (43) | 28.59 | 0.0 |
| native at grown vocabulary, m=200 | 65.9 | 4.06 (30) | 4.16 (30) | 4.92 (40) | 45.05 | 0.0 |

Replay of label_exchange_coco_vitl_bank683_schemes (anchored, label-level; added cal / held-out / size): max abs difference 1.65e-04.
