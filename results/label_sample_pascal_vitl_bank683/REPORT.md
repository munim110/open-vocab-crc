# Added-label guarantee from m randomly drawn, annotated names

vitl_bank683, 2000 Pascal Context validation images, 458-name vocabulary (59 source names), 500 trials. m = drawn added names; m' = drawn names present in the calibration images (the calibration labels). Added = mean loss over the remaining added labels present (cal: calibration images, the proposition's quantity; held-out: other half). Src, image = image-level source risk (source names at the image-level threshold). Size = labels per labelled pixel at the grown vocabulary, held-out images. Floor = % of trials whose added-name threshold is the grid floor. Risks in % (and % of trials above alpha). Development data; nothing fitted.

## alpha = 0.1

| Arm | m' | Added, cal | Added, held-out | Src, image | Size | Floor |
|---|---:|---:|---:|---:|---:|---:|
| check: random S of T | 28.8 | 7.55 (23) | 7.51 (25) | 2.12 (0) | 11.54 | 0.0 |
| check: dataset split | 59.0 | 22.30 (100) | 22.29 (100) | 8.40 (1) | 2.73 | 0.0 |
| source classes (benchmark split), per-label | 59.0 | 22.30 (100) | 22.29 (100) | 9.88 (44) | 2.63 | 0.0 |
| anchored, m=10 | 4.2 | 0.01 (0) | 0.01 (0) | 9.88 (44) | 399.72 | 99.8 |
| native at grown vocabulary, m=10 | 4.2 | 0.01 (0) | 0.01 (0) | 9.87 (44) | 399.70 | 99.8 |
| anchored, m=20 | 8.3 | 1.56 (2) | 1.53 (2) | 9.88 (44) | 251.21 | 53.8 |
| native at grown vocabulary, m=20 | 8.3 | 1.59 (3) | 1.56 (2) | 9.87 (44) | 260.98 | 53.8 |
| anchored, m=30 | 12.4 | 4.38 (8) | 4.30 (11) | 9.88 (44) | 74.83 | 6.6 |
| native at grown vocabulary, m=30 | 12.4 | 4.50 (10) | 4.37 (10) | 9.87 (44) | 91.37 | 6.6 |
| anchored, m=50 | 20.7 | 6.85 (24) | 6.78 (22) | 9.88 (44) | 20.04 | 0.0 |
| native at grown vocabulary, m=50 | 20.7 | 7.02 (25) | 6.92 (23) | 9.87 (44) | 25.14 | 0.0 |
| anchored, m=75 | 31.2 | 7.76 (28) | 7.72 (28) | 9.88 (44) | 11.40 | 0.0 |
| native at grown vocabulary, m=75 | 31.2 | 7.87 (28) | 7.79 (27) | 9.87 (44) | 14.66 | 0.0 |
| anchored, m=100 | 41.7 | 8.50 (32) | 8.44 (33) | 9.88 (44) | 8.87 | 0.0 |
| native at grown vocabulary, m=100 | 41.7 | 8.55 (32) | 8.49 (32) | 9.87 (44) | 11.50 | 0.0 |
| anchored, m=150 | 62.4 | 8.88 (37) | 8.99 (39) | 9.88 (44) | 7.35 | 0.0 |
| native at grown vocabulary, m=150 | 62.4 | 8.91 (38) | 8.95 (37) | 9.87 (44) | 9.56 | 0.0 |
| anchored, m=200 | 83.0 | 9.20 (37) | 9.32 (40) | 9.88 (44) | 6.69 | 0.0 |
| native at grown vocabulary, m=200 | 83.0 | 9.23 (39) | 9.28 (40) | 9.87 (44) | 8.72 | 0.0 |

## alpha = 0.05

| Arm | m' | Added, cal | Added, held-out | Src, image | Size | Floor |
|---|---:|---:|---:|---:|---:|---:|
| check: random S of T | 28.8 | 2.76 (16) | 2.74 (16) | 0.37 (0) | 68.36 | 0.6 |
| check: dataset split | 59.0 | 12.58 (100) | 12.56 (100) | 3.38 (0) | 4.99 | 0.0 |
| source classes (benchmark split), per-label | 59.0 | 12.58 (100) | 12.56 (100) | 4.89 (40) | 4.66 | 0.0 |
| anchored, m=10 | 4.2 | 0.00 (0) | 0.00 (0) | 4.89 (40) | 401.00 | 100.0 |
| native at grown vocabulary, m=10 | 4.2 | 0.00 (0) | 0.00 (0) | 4.90 (41) | 401.00 | 100.0 |
| anchored, m=20 | 8.3 | 0.00 (0) | 0.00 (0) | 4.89 (40) | 401.00 | 100.0 |
| native at grown vocabulary, m=20 | 8.3 | 0.00 (0) | 0.00 (0) | 4.90 (41) | 401.00 | 100.0 |
| anchored, m=30 | 12.4 | 0.02 (0) | 0.01 (0) | 4.89 (40) | 399.55 | 99.6 |
| native at grown vocabulary, m=30 | 12.4 | 0.01 (0) | 0.01 (0) | 4.90 (41) | 399.72 | 99.6 |
| anchored, m=50 | 20.7 | 1.48 (7) | 1.46 (6) | 4.89 (40) | 179.68 | 25.4 |
| native at grown vocabulary, m=50 | 20.7 | 1.45 (7) | 1.38 (4) | 4.90 (41) | 207.95 | 25.4 |
| anchored, m=75 | 31.2 | 2.81 (21) | 2.77 (18) | 4.89 (40) | 67.18 | 0.0 |
| native at grown vocabulary, m=75 | 31.2 | 2.87 (20) | 2.84 (17) | 4.90 (41) | 88.39 | 0.0 |
| anchored, m=100 | 41.7 | 3.34 (23) | 3.34 (23) | 4.89 (40) | 43.67 | 0.0 |
| native at grown vocabulary, m=100 | 41.7 | 3.41 (24) | 3.39 (22) | 4.90 (41) | 54.52 | 0.0 |
| anchored, m=150 | 62.4 | 3.80 (26) | 3.83 (29) | 4.89 (40) | 27.31 | 0.0 |
| native at grown vocabulary, m=150 | 62.4 | 3.83 (27) | 3.86 (30) | 4.90 (41) | 35.39 | 0.0 |
| anchored, m=200 | 83.0 | 4.09 (32) | 4.19 (34) | 4.89 (40) | 23.07 | 0.0 |
| native at grown vocabulary, m=200 | 83.0 | 4.21 (34) | 4.24 (33) | 4.90 (41) | 29.82 | 0.0 |

Replay of label_exchange_pascal_vitl_bank683_schemes (anchored, label-level; added cal / held-out / size): max abs difference 1.38e-05.
