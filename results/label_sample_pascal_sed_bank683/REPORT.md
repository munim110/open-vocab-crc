# Added-label guarantee from m randomly drawn, annotated names

sed_bank683, 2000 Pascal Context validation images, 458-name vocabulary (59 source names), 500 trials. m = drawn added names; m' = drawn names present in the calibration images (the calibration labels). Added = mean loss over the remaining added labels present (cal: calibration images, the proposition's quantity; held-out: other half). Src, image = image-level source risk (source names at the image-level threshold). Size = labels per labelled pixel at the grown vocabulary, held-out images. Floor = % of trials whose added-name threshold is the grid floor. Risks in % (and % of trials above alpha). Development data; nothing fitted.

## alpha = 0.1

| Arm | m' | Added, cal | Added, held-out | Src, image | Size | Floor |
|---|---:|---:|---:|---:|---:|---:|
| check: random S of T | 28.8 | 7.53 (25) | 7.48 (27) | 1.43 (0) | 17.48 | 0.0 |
| check: dataset split | 59.0 | 26.22 (100) | 26.22 (100) | 7.67 (0) | 3.55 | 0.0 |
| source classes (benchmark split), per-label | 59.0 | 26.22 (100) | 26.22 (100) | 9.87 (43) | 3.32 | 0.0 |
| anchored, m=10 | 4.2 | 0.00 (0) | 0.00 (0) | 9.87 (43) | 400.36 | 99.8 |
| native at grown vocabulary, m=10 | 4.2 | 0.00 (0) | 0.00 (0) | 9.88 (44) | 400.12 | 99.8 |
| anchored, m=20 | 8.3 | 1.49 (2) | 1.44 (2) | 9.87 (43) | 262.77 | 53.8 |
| native at grown vocabulary, m=20 | 8.3 | 1.49 (2) | 1.45 (1) | 9.88 (44) | 264.35 | 53.8 |
| anchored, m=30 | 12.4 | 4.49 (11) | 4.35 (10) | 9.87 (43) | 85.70 | 6.6 |
| native at grown vocabulary, m=30 | 12.4 | 4.51 (11) | 4.38 (11) | 9.88 (44) | 87.94 | 6.6 |
| anchored, m=50 | 20.7 | 6.63 (20) | 6.50 (22) | 9.87 (43) | 27.88 | 0.0 |
| native at grown vocabulary, m=50 | 20.7 | 6.74 (22) | 6.63 (20) | 9.88 (44) | 30.74 | 0.0 |
| anchored, m=75 | 31.2 | 7.89 (26) | 7.77 (27) | 9.87 (43) | 16.24 | 0.0 |
| native at grown vocabulary, m=75 | 31.2 | 7.97 (28) | 7.83 (27) | 9.88 (44) | 18.44 | 0.0 |
| anchored, m=100 | 41.7 | 8.46 (32) | 8.35 (31) | 9.87 (43) | 14.10 | 0.0 |
| native at grown vocabulary, m=100 | 41.7 | 8.59 (32) | 8.46 (30) | 9.88 (44) | 15.74 | 0.0 |
| anchored, m=150 | 62.4 | 9.02 (39) | 8.97 (35) | 9.87 (43) | 11.95 | 0.0 |
| native at grown vocabulary, m=150 | 62.4 | 9.09 (38) | 9.08 (35) | 9.88 (44) | 13.63 | 0.0 |
| anchored, m=200 | 83.0 | 9.36 (44) | 9.29 (38) | 9.87 (43) | 11.10 | 0.0 |
| native at grown vocabulary, m=200 | 83.0 | 9.44 (44) | 9.39 (38) | 9.88 (44) | 12.79 | 0.0 |

## alpha = 0.05

| Arm | m' | Added, cal | Added, held-out | Src, image | Size | Floor |
|---|---:|---:|---:|---:|---:|---:|
| check: random S of T | 28.8 | 2.82 (17) | 2.80 (19) | 0.25 (0) | 80.37 | 0.6 |
| check: dataset split | 59.0 | 15.46 (100) | 15.43 (100) | 3.20 (0) | 6.71 | 0.0 |
| source classes (benchmark split), per-label | 59.0 | 15.46 (100) | 15.43 (100) | 4.89 (40) | 6.19 | 0.0 |
| anchored, m=10 | 4.2 | 0.00 (0) | 0.00 (0) | 4.89 (40) | 401.34 | 100.0 |
| native at grown vocabulary, m=10 | 4.2 | 0.00 (0) | 0.00 (0) | 4.90 (41) | 401.28 | 100.0 |
| anchored, m=20 | 8.3 | 0.00 (0) | 0.00 (0) | 4.89 (40) | 401.34 | 100.0 |
| native at grown vocabulary, m=20 | 8.3 | 0.00 (0) | 0.00 (0) | 4.90 (41) | 401.28 | 100.0 |
| anchored, m=30 | 12.4 | 0.01 (0) | 0.01 (0) | 4.89 (40) | 400.25 | 99.6 |
| native at grown vocabulary, m=30 | 12.4 | 0.01 (0) | 0.01 (0) | 4.90 (41) | 400.22 | 99.6 |
| anchored, m=50 | 20.7 | 1.45 (6) | 1.44 (6) | 4.89 (40) | 193.53 | 25.4 |
| native at grown vocabulary, m=50 | 20.7 | 1.39 (6) | 1.39 (5) | 4.90 (41) | 197.62 | 25.4 |
| anchored, m=75 | 31.2 | 2.90 (19) | 2.83 (19) | 4.89 (40) | 72.93 | 0.0 |
| native at grown vocabulary, m=75 | 31.2 | 2.89 (19) | 2.81 (18) | 4.90 (41) | 79.22 | 0.0 |
| anchored, m=100 | 41.7 | 3.43 (26) | 3.39 (24) | 4.89 (40) | 52.80 | 0.0 |
| native at grown vocabulary, m=100 | 41.7 | 3.40 (25) | 3.32 (22) | 4.90 (41) | 58.16 | 0.0 |
| anchored, m=150 | 62.4 | 3.94 (31) | 3.89 (30) | 4.89 (40) | 36.31 | 0.0 |
| native at grown vocabulary, m=150 | 62.4 | 3.96 (31) | 3.89 (29) | 4.90 (41) | 39.78 | 0.0 |
| anchored, m=200 | 83.0 | 4.26 (34) | 4.19 (31) | 4.89 (40) | 31.41 | 0.0 |
| native at grown vocabulary, m=200 | 83.0 | 4.30 (35) | 4.22 (32) | 4.90 (41) | 34.60 | 0.0 |

Replay of label_exchange_pascal_sed_bank683_schemes (anchored, label-level; added cal / held-out / size): max abs difference 1.41e-05.
