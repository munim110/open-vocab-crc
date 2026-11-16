# Added-label guarantee from m randomly drawn, annotated names

sed_bank683, 2000 COCO val2017 (LVIS-annotated) images, 1283-name vocabulary (171 source names), 500 trials. m = drawn added names; m' = drawn names present in the calibration images (the calibration labels). Added = mean loss over the remaining added labels present (cal: calibration images, the proposition's quantity; held-out: other half). Src, image = image-level source risk (source names at the image-level threshold). Size = labels per labelled pixel at the grown vocabulary, held-out images. Floor = % of trials whose added-name threshold is the grid floor. Risks in % (and % of trials above alpha). Development data; nothing fitted.

## alpha = 0.1

| Arm | m' | Added, cal | Added, held-out | Src, image | Size | Floor |
|---|---:|---:|---:|---:|---:|---:|
| check: random S of T | 71.5 | 9.03 (34) | 9.07 (36) | 1.14 (0) | 21.24 | 0.0 |
| check: dataset split | 170.1 | 24.31 (100) | 24.49 (100) | 4.03 (0) | 7.24 | 0.0 |
| source classes (benchmark split), per-label | 170.1 | 24.31 (100) | 24.49 (100) | 9.89 (42) | 5.56 | 0.0 |
| anchored, m=10 | 3.2 | 0.00 (0) | 0.00 (0) | 9.89 (42) | 1114.18 | 100.0 |
| native at grown vocabulary, m=10 | 3.2 | 0.00 (0) | 0.00 (0) | 9.90 (44) | 1114.35 | 100.0 |
| anchored, m=20 | 6.5 | 0.70 (2) | 0.70 (3) | 9.89 (42) | 956.84 | 83.8 |
| native at grown vocabulary, m=20 | 6.5 | 0.73 (2) | 0.73 (2) | 9.90 (44) | 959.24 | 83.8 |
| anchored, m=30 | 9.8 | 3.26 (9) | 3.30 (9) | 9.89 (42) | 427.70 | 31.0 |
| native at grown vocabulary, m=30 | 9.8 | 3.23 (8) | 3.31 (9) | 9.90 (44) | 437.40 | 31.0 |
| anchored, m=50 | 16.5 | 6.31 (22) | 6.36 (22) | 9.89 (42) | 73.24 | 0.6 |
| native at grown vocabulary, m=50 | 16.5 | 6.37 (21) | 6.45 (21) | 9.90 (44) | 81.35 | 0.6 |
| anchored, m=75 | 24.7 | 7.48 (26) | 7.55 (26) | 9.89 (42) | 39.68 | 0.0 |
| native at grown vocabulary, m=75 | 24.7 | 7.45 (26) | 7.55 (27) | 9.90 (44) | 45.15 | 0.0 |
| anchored, m=100 | 32.9 | 8.08 (29) | 8.12 (31) | 9.89 (42) | 29.38 | 0.0 |
| native at grown vocabulary, m=100 | 32.9 | 8.13 (29) | 8.20 (29) | 9.90 (44) | 32.74 | 0.0 |
| anchored, m=150 | 49.4 | 8.82 (33) | 8.89 (35) | 9.89 (42) | 22.91 | 0.0 |
| native at grown vocabulary, m=150 | 49.4 | 8.88 (34) | 8.97 (36) | 9.90 (44) | 25.64 | 0.0 |
| anchored, m=200 | 65.9 | 8.99 (36) | 9.12 (38) | 9.89 (42) | 20.93 | 0.0 |
| native at grown vocabulary, m=200 | 65.9 | 9.03 (36) | 9.16 (38) | 9.90 (44) | 23.47 | 0.0 |

## alpha = 0.05

| Arm | m' | Added, cal | Added, held-out | Src, image | Size | Floor |
|---|---:|---:|---:|---:|---:|---:|
| check: random S of T | 71.5 | 4.04 (27) | 4.08 (29) | 0.36 (0) | 60.08 | 0.0 |
| check: dataset split | 170.1 | 14.17 (100) | 14.30 (100) | 1.55 (0) | 14.85 | 0.0 |
| source classes (benchmark split), per-label | 170.1 | 14.17 (100) | 14.30 (100) | 4.91 (41) | 11.50 | 0.0 |
| anchored, m=10 | 3.2 | 0.00 (0) | 0.00 (0) | 4.91 (41) | 1115.44 | 100.0 |
| native at grown vocabulary, m=10 | 3.2 | 0.00 (0) | 0.00 (0) | 4.91 (41) | 1115.66 | 100.0 |
| anchored, m=20 | 6.5 | 0.00 (0) | 0.00 (0) | 4.91 (41) | 1115.44 | 100.0 |
| native at grown vocabulary, m=20 | 6.5 | 0.00 (0) | 0.00 (0) | 4.91 (41) | 1115.66 | 100.0 |
| anchored, m=30 | 9.8 | 0.00 (0) | 0.00 (0) | 4.91 (41) | 1115.44 | 100.0 |
| native at grown vocabulary, m=30 | 9.8 | 0.00 (0) | 0.00 (0) | 4.91 (41) | 1115.66 | 100.0 |
| anchored, m=50 | 16.5 | 0.52 (2) | 0.54 (2) | 4.91 (41) | 858.11 | 71.0 |
| native at grown vocabulary, m=50 | 16.5 | 0.54 (3) | 0.55 (2) | 4.91 (41) | 862.67 | 71.0 |
| anchored, m=75 | 24.7 | 2.65 (16) | 2.68 (16) | 4.91 (41) | 216.72 | 7.0 |
| native at grown vocabulary, m=75 | 24.7 | 2.63 (15) | 2.68 (17) | 4.91 (41) | 231.73 | 7.0 |
| anchored, m=100 | 32.9 | 3.04 (22) | 3.12 (21) | 4.91 (41) | 117.72 | 0.0 |
| native at grown vocabulary, m=100 | 32.9 | 3.06 (21) | 3.17 (21) | 4.91 (41) | 133.33 | 0.0 |
| anchored, m=150 | 49.4 | 3.84 (27) | 3.89 (28) | 4.91 (41) | 71.24 | 0.0 |
| native at grown vocabulary, m=150 | 49.4 | 3.79 (27) | 3.86 (27) | 4.91 (41) | 79.66 | 0.0 |
| anchored, m=200 | 65.9 | 3.99 (29) | 4.08 (30) | 4.91 (41) | 60.49 | 0.0 |
| native at grown vocabulary, m=200 | 65.9 | 3.99 (30) | 4.07 (31) | 4.91 (41) | 67.42 | 0.0 |

Replay of label_exchange_coco_sed_bank683_schemes (anchored, label-level; added cal / held-out / size): max abs difference 4.62e-04.
