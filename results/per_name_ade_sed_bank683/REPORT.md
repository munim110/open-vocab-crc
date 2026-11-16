# Per-name (class-conditional) calibration

sed_bank683, 2000 ADE validation images, 845 names (150 source; 836 present in some image), 500 random half/half splits. Calibrated: mean number of present names per split with a qualifying threshold (at least 1/alpha - 1 calibration images containing the name); the others are left out of the sets. Per calibrated name: mean loss over the held-out images containing it, averaged over the splits in which it is calibrated (the per-name arms guarantee at most alpha for every name). Over alpha: names calibrated in at least {MIN_SPLITS} splits whose split-averaged risk exceeds alpha by more than 3 standard errors over splits; worst name and the source/added columns use the same names. Image risk: the paper's image-level loss (missed fraction of source-labelled pixels, names outside the sets missed), mean over held-out images and splits. Size: labels per labelled pixel at 845 names, held-out images, first 20 splits. Development data; nothing fitted.

## alpha = 0.1

| Arm | Names | Macro risk (%) | Worst name (%) | Names over alpha | Source: macro / worst (%) | Added: macro / worst (%) | Image risk (%) | Size |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, per-name | 160 | 6.7 | 12.6 | 0 | 7.4 / 9.9 | 6.3 / 12.6 | 7.4 | 14.61 |
| anchored, per-name, 10 images | 160 | 5.1 | 12.6 | 0 | 4.9 / 9.1 | 6.1 / 12.6 | 4.6 | 21.55 |
| anchored, per-name, 20 images | 160 | 6.1 | 12.6 | 0 | 6.4 / 9.1 | 6.3 / 12.6 | 6.0 | 16.44 |
| anchored, per-name, 50 images | 160 | 6.6 | 12.6 | 0 | 7.2 / 9.2 | 6.3 / 12.6 | 6.9 | 14.82 |
| native, per-name, source->grown | 118 | 4.1 | 7.9 | 0 | 4.1 / 7.9 | - / - | 5.1 | nan |
| native, per-name, source | 118 | 7.4 | 9.9 | 0 | 7.4 / 9.9 | - / - | 7.1 | nan |
| native, per-name, grown | 160 | 6.8 | 12.5 | 0 | 7.4 / 9.9 | 6.5 / 12.5 | 7.4 | 15.61 |
| anchored, image-level, all names | 836 | 33.9 | 100.0 | 485 | 23.1 / 100.0 | 36.2 / 100.0 | 9.9 | 6.29 |
| anchored, image-level, per-name names | 160 | 33.5 | 100.0 | 145 | 24.8 / 100.0 | 45.9 / 100.0 | 11.8 | 2.70 |
| hybrid, per-name or image-level | 836 | 29.6 | 100.0 | 383 | 10.8 / 97.6 | 33.6 / 100.0 | 5.4 | 18.21 |
| hybrid, per-name or image-level (calibrated names) | 160 | 6.7 | 12.6 | 0 | 7.4 / 9.9 | 6.3 / 12.6 | 5.4 | nan |
| hybrid, lower of both | 836 | 29.4 | 100.0 | 383 | 9.9 / 97.6 | 33.6 / 100.0 | 4.1 | 18.46 |
| hybrid, lower of both (calibrated names) | 160 | 6.0 | 12.6 | 0 | 6.3 / 9.9 | 6.1 / 12.6 | 4.1 | nan |

## alpha = 0.05

| Arm | Names | Macro risk (%) | Worst name (%) | Names over alpha | Source: macro / worst (%) | Added: macro / worst (%) | Image risk (%) | Size |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, per-name | 96 | 3.3 | 6.0 | 0 | 3.3 / 4.9 | 3.0 / 6.0 | 8.2 | 13.12 |
| anchored, per-name, 10 images | 0 | - | - | 0 | - / - | - / - | 100.0 | 0.00 |
| anchored, per-name, 20 images | 96 | 2.4 | 6.0 | 0 | 2.3 / 4.9 | 2.9 / 6.0 | 7.0 | 18.75 |
| anchored, per-name, 50 images | 96 | 3.1 | 6.0 | 0 | 3.1 / 4.6 | 3.0 / 6.0 | 7.8 | 14.13 |
| native, per-name, source->grown | 86 | 2.0 | 4.2 | 0 | 1.8 / 4.2 | - / - | 7.3 | nan |
| native, per-name, source | 86 | 3.5 | 4.8 | 0 | 3.4 / 4.8 | - / - | 8.1 | nan |
| native, per-name, grown | 96 | 3.3 | 6.4 | 0 | 3.4 / 4.9 | 3.2 / 6.4 | 8.2 | 13.80 |
| anchored, image-level, all names | 836 | 20.6 | 100.0 | 387 | 12.6 / 99.7 | 22.3 / 100.0 | 4.9 | 15.96 |
| anchored, image-level, per-name names | 96 | 16.0 | 99.7 | 76 | 12.8 / 99.7 | 32.4 / 96.4 | 10.6 | 3.88 |
| hybrid, per-name or image-level | 836 | 19.3 | 100.0 | 333 | 7.5 / 97.1 | 21.9 / 100.0 | 2.5 | 25.20 |
| hybrid, per-name or image-level (calibrated names) | 96 | 3.3 | 6.0 | 0 | 3.3 / 4.9 | 3.0 / 6.0 | 2.5 | nan |
| hybrid, lower of both | 836 | 19.2 | 100.0 | 333 | 7.1 / 97.1 | 21.9 / 100.0 | 1.9 | 25.67 |
| hybrid, lower of both (calibrated names) | 96 | 2.8 | 6.0 | 0 | 2.7 / 4.8 | 2.9 / 6.0 | 1.9 | nan |
