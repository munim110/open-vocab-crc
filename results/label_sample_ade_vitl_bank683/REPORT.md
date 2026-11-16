# Added-label guarantee from m randomly drawn, annotated names

vitl_bank683, 2000 ADE validation images, 845-name vocabulary (150 source names), 500 trials. m = drawn added names; m' = drawn names present in the calibration images (the calibration labels). Added = mean loss over the remaining added labels present (cal: calibration images, the proposition's quantity; held-out: other half). Src, image = image-level source risk (source names at the image-level threshold). Size = labels per labelled pixel at the grown vocabulary, held-out images. Floor = % of trials whose added-name threshold is the grid floor. Risks in % (and % of trials above alpha). Development data; nothing fitted.

## alpha = 0.1

| Arm | m' | Added, cal | Added, held-out | Src, image | Size | Floor |
|---|---:|---:|---:|---:|---:|---:|
| check: random S of T | 113.0 | 9.50 (40) | 9.55 (40) | 1.67 (0) | 27.55 | 0.0 |
| check: dataset split | 149.4 | 22.20 (100) | 22.25 (100) | 4.91 (0) | 9.00 | 0.0 |
| source classes (benchmark split), per-label | 149.4 | 22.20 (100) | 22.25 (100) | 9.89 (39) | 7.55 | 0.0 |
| anchored, m=10 | 6.9 | 0.33 (0) | 0.34 (0) | 9.89 (39) | 627.65 | 86.0 |
| native at grown vocabulary, m=10 | 6.9 | 0.28 (0) | 0.30 (0) | 9.91 (44) | 666.81 | 86.0 |
| anchored, m=20 | 14.0 | 5.84 (17) | 5.85 (20) | 9.89 (39) | 102.10 | 0.4 |
| native at grown vocabulary, m=20 | 14.0 | 5.13 (19) | 5.13 (19) | 9.91 (44) | 335.59 | 0.4 |
| anchored, m=30 | 20.9 | 7.03 (22) | 7.12 (24) | 9.89 (39) | 60.25 | 0.0 |
| native at grown vocabulary, m=30 | 20.9 | 6.42 (23) | 6.45 (25) | 9.91 (44) | 232.32 | 0.0 |
| anchored, m=50 | 34.9 | 8.25 (29) | 8.34 (32) | 9.89 (39) | 42.35 | 0.0 |
| native at grown vocabulary, m=50 | 34.9 | 7.86 (31) | 7.91 (31) | 9.91 (44) | 134.37 | 0.0 |
| anchored, m=75 | 52.5 | 8.83 (34) | 8.92 (36) | 9.89 (39) | 33.93 | 0.0 |
| native at grown vocabulary, m=75 | 52.5 | 8.61 (34) | 8.71 (34) | 9.91 (44) | 79.01 | 0.0 |
| anchored, m=100 | 70.0 | 9.33 (38) | 9.39 (39) | 9.89 (39) | 29.49 | 0.0 |
| native at grown vocabulary, m=100 | 70.0 | 9.24 (37) | 9.36 (37) | 9.91 (44) | 43.40 | 0.0 |
| anchored, m=150 | 105.0 | 9.45 (41) | 9.54 (40) | 9.89 (39) | 27.55 | 0.0 |
| native at grown vocabulary, m=150 | 105.0 | 9.41 (40) | 9.52 (40) | 9.91 (44) | 34.71 | 0.0 |
| anchored, m=200 | 140.0 | 9.62 (42) | 9.74 (41) | 9.89 (39) | 26.15 | 0.0 |
| native at grown vocabulary, m=200 | 140.0 | 9.59 (42) | 9.70 (41) | 9.91 (44) | 32.18 | 0.0 |

## alpha = 0.05

| Arm | m' | Added, cal | Added, held-out | Src, image | Size | Floor |
|---|---:|---:|---:|---:|---:|---:|
| check: random S of T | 113.0 | 4.48 (36) | 4.51 (37) | 0.49 (0) | 76.39 | 0.0 |
| check: dataset split | 149.4 | 13.11 (100) | 13.19 (100) | 2.09 (0) | 20.65 | 0.0 |
| source classes (benchmark split), per-label | 149.4 | 13.11 (100) | 13.19 (100) | 4.89 (42) | 17.53 | 0.0 |
| anchored, m=10 | 6.9 | 0.00 (0) | 0.00 (0) | 4.89 (42) | 698.72 | 100.0 |
| native at grown vocabulary, m=10 | 6.9 | 0.00 (0) | 0.00 (0) | 4.90 (44) | 698.64 | 100.0 |
| anchored, m=20 | 14.0 | 0.01 (0) | 0.01 (0) | 4.89 (42) | 695.20 | 99.2 |
| native at grown vocabulary, m=20 | 14.0 | 0.01 (0) | 0.01 (0) | 4.90 (44) | 697.49 | 99.2 |
| anchored, m=30 | 20.9 | 1.90 (10) | 1.93 (12) | 4.89 (42) | 297.73 | 17.4 |
| native at grown vocabulary, m=30 | 20.9 | 1.34 (15) | 1.36 (16) | 4.90 (44) | 562.25 | 17.4 |
| anchored, m=50 | 34.9 | 3.17 (22) | 3.19 (21) | 4.89 (42) | 142.92 | 0.0 |
| native at grown vocabulary, m=50 | 34.9 | 1.90 (21) | 1.97 (21) | 4.90 (44) | 519.83 | 0.0 |
| anchored, m=75 | 52.5 | 3.87 (27) | 3.92 (27) | 4.89 (42) | 102.14 | 0.0 |
| native at grown vocabulary, m=75 | 52.5 | 2.57 (28) | 2.62 (29) | 4.90 (44) | 445.47 | 0.0 |
| anchored, m=100 | 70.0 | 4.25 (32) | 4.30 (32) | 4.89 (42) | 85.34 | 0.0 |
| native at grown vocabulary, m=100 | 70.0 | 3.00 (35) | 3.02 (33) | 4.90 (44) | 394.75 | 0.0 |
| anchored, m=150 | 105.0 | 4.42 (32) | 4.45 (35) | 4.89 (42) | 77.31 | 0.0 |
| native at grown vocabulary, m=150 | 105.0 | 3.42 (36) | 3.42 (36) | 4.90 (44) | 334.26 | 0.0 |
| anchored, m=200 | 140.0 | 4.58 (36) | 4.63 (38) | 4.89 (42) | 71.73 | 0.0 |
| native at grown vocabulary, m=200 | 140.0 | 3.78 (38) | 3.80 (39) | 4.90 (44) | 293.66 | 0.0 |

Replay of label_exchange_ade_vitl_bank683_schemes (anchored, label-level; added cal / held-out / size): max abs difference 2.80e-04.
