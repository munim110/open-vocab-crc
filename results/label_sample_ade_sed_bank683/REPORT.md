# Added-label guarantee from m randomly drawn, annotated names

sed_bank683, 2000 ADE validation images, 845-name vocabulary (150 source names), 500 trials. m = drawn added names; m' = drawn names present in the calibration images (the calibration labels). Added = mean loss over the remaining added labels present (cal: calibration images, the proposition's quantity; held-out: other half). Src, image = image-level source risk (source names at the image-level threshold). Size = labels per labelled pixel at the grown vocabulary, held-out images. Floor = % of trials whose added-name threshold is the grid floor. Risks in % (and % of trials above alpha). Development data; nothing fitted.

## alpha = 0.1

| Arm | m' | Added, cal | Added, held-out | Src, image | Size | Floor |
|---|---:|---:|---:|---:|---:|---:|
| check: random S of T | 113.0 | 9.51 (42) | 9.50 (42) | 2.78 (0) | 45.10 | 0.0 |
| check: dataset split | 149.4 | 22.20 (100) | 22.20 (100) | 5.35 (0) | 14.10 | 0.0 |
| source classes (benchmark split), per-label | 149.4 | 22.20 (100) | 22.20 (100) | 9.87 (42) | 12.01 | 0.0 |
| anchored, m=10 | 6.9 | 0.34 (0) | 0.36 (0) | 9.87 (42) | 637.73 | 86.0 |
| native at grown vocabulary, m=10 | 6.9 | 0.39 (0) | 0.40 (0) | 9.90 (45) | 641.33 | 86.0 |
| anchored, m=20 | 14.0 | 5.80 (16) | 5.80 (16) | 9.87 (42) | 157.71 | 0.4 |
| native at grown vocabulary, m=20 | 14.0 | 5.83 (18) | 5.81 (17) | 9.90 (45) | 181.25 | 0.4 |
| anchored, m=30 | 20.9 | 7.05 (24) | 7.04 (23) | 9.87 (42) | 102.52 | 0.0 |
| native at grown vocabulary, m=30 | 20.9 | 6.93 (24) | 6.92 (23) | 9.90 (45) | 122.93 | 0.0 |
| anchored, m=50 | 34.9 | 8.26 (30) | 8.25 (30) | 9.87 (42) | 68.99 | 0.0 |
| native at grown vocabulary, m=50 | 34.9 | 8.20 (29) | 8.18 (28) | 9.90 (45) | 80.69 | 0.0 |
| anchored, m=75 | 52.5 | 8.92 (33) | 8.91 (35) | 9.87 (42) | 54.40 | 0.0 |
| native at grown vocabulary, m=75 | 52.5 | 8.85 (33) | 8.85 (33) | 9.90 (45) | 62.68 | 0.0 |
| anchored, m=100 | 70.0 | 9.34 (37) | 9.29 (40) | 9.87 (42) | 48.03 | 0.0 |
| native at grown vocabulary, m=100 | 70.0 | 9.29 (38) | 9.26 (38) | 9.90 (45) | 54.86 | 0.0 |
| anchored, m=150 | 105.0 | 9.59 (40) | 9.53 (43) | 9.87 (42) | 44.94 | 0.0 |
| native at grown vocabulary, m=150 | 105.0 | 9.56 (41) | 9.52 (42) | 9.90 (45) | 50.95 | 0.0 |
| anchored, m=200 | 140.0 | 9.68 (42) | 9.64 (45) | 9.87 (42) | 43.34 | 0.0 |
| native at grown vocabulary, m=200 | 140.0 | 9.66 (43) | 9.63 (43) | 9.90 (45) | 48.80 | 0.0 |

## alpha = 0.05

| Arm | m' | Added, cal | Added, held-out | Src, image | Size | Floor |
|---|---:|---:|---:|---:|---:|---:|
| check: random S of T | 113.0 | 4.55 (36) | 4.55 (37) | 1.32 (0) | 118.47 | 0.0 |
| check: dataset split | 149.4 | 12.72 (100) | 12.71 (100) | 3.09 (0) | 35.04 | 0.0 |
| source classes (benchmark split), per-label | 149.4 | 12.72 (100) | 12.71 (100) | 4.89 (42) | 30.67 | 0.0 |
| anchored, m=10 | 6.9 | 0.00 (0) | 0.00 (0) | 4.89 (42) | 700.40 | 100.0 |
| native at grown vocabulary, m=10 | 6.9 | 0.00 (0) | 0.00 (0) | 4.90 (45) | 700.69 | 100.0 |
| anchored, m=20 | 14.0 | 0.02 (0) | 0.02 (0) | 4.89 (42) | 696.40 | 99.2 |
| native at grown vocabulary, m=20 | 14.0 | 0.03 (0) | 0.03 (0) | 4.90 (45) | 696.68 | 99.2 |
| anchored, m=30 | 20.9 | 1.84 (8) | 1.85 (8) | 4.89 (42) | 370.80 | 17.4 |
| native at grown vocabulary, m=30 | 20.9 | 1.87 (8) | 1.88 (9) | 4.90 (45) | 400.04 | 17.4 |
| anchored, m=50 | 34.9 | 3.11 (20) | 3.10 (19) | 4.89 (42) | 221.55 | 0.0 |
| native at grown vocabulary, m=50 | 34.9 | 3.15 (19) | 3.15 (20) | 4.90 (45) | 252.04 | 0.0 |
| anchored, m=75 | 52.5 | 3.84 (28) | 3.84 (31) | 4.89 (42) | 165.79 | 0.0 |
| native at grown vocabulary, m=75 | 52.5 | 3.83 (28) | 3.83 (29) | 4.90 (45) | 195.71 | 0.0 |
| anchored, m=100 | 70.0 | 4.20 (32) | 4.16 (33) | 4.89 (42) | 143.81 | 0.0 |
| native at grown vocabulary, m=100 | 70.0 | 4.20 (32) | 4.18 (34) | 4.90 (45) | 170.00 | 0.0 |
| anchored, m=150 | 105.0 | 4.51 (35) | 4.48 (35) | 4.89 (42) | 122.09 | 0.0 |
| native at grown vocabulary, m=150 | 105.0 | 4.50 (36) | 4.46 (35) | 4.90 (45) | 147.03 | 0.0 |
| anchored, m=200 | 140.0 | 4.56 (36) | 4.55 (38) | 4.89 (42) | 115.32 | 0.0 |
| native at grown vocabulary, m=200 | 140.0 | 4.57 (38) | 4.54 (37) | 4.90 (45) | 137.94 | 0.0 |

Replay of label_exchange_ade_sed_bank683_schemes (anchored, label-level; added cal / held-out / size): max abs difference 5.91e-06.
