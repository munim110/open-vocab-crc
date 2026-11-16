# Per-name (class-conditional) calibration

vitl_bank683, 2000 Pascal Context validation images, 458 names (59 source; 270 present in some image), 500 random half/half splits. Calibrated: mean number of present names per split with a qualifying threshold (at least 1/alpha - 1 calibration images containing the name); the others are left out of the sets. Per calibrated name: mean loss over the held-out images containing it, averaged over the splits in which it is calibrated (the per-name arms guarantee at most alpha for every name). Over alpha: names calibrated in at least {MIN_SPLITS} splits whose split-averaged risk exceeds alpha by more than 3 standard errors over splits; worst name and the source/added columns use the same names. Image risk: the paper's image-level loss (missed fraction of source-labelled pixels, names outside the sets missed), mean over held-out images and splits. Size: labels per labelled pixel at 458 names, held-out images, first 20 splits. Development data; nothing fitted.

## alpha = 0.1

| Arm | Names | Macro risk (%) | Worst name (%) | Names over alpha | Source: macro / worst (%) | Added: macro / worst (%) | Image risk (%) | Size |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, per-name | 87 | 6.9 | 9.9 | 0 | 8.4 / 9.9 | 5.5 / 9.5 | 6.9 | 3.58 |
| anchored, per-name, 10 images | 87 | 4.1 | 8.0 | 0 | 4.3 / 8.0 | 4.1 / 7.9 | 2.7 | 6.41 |
| anchored, per-name, 20 images | 87 | 5.8 | 7.9 | 0 | 6.7 / 7.9 | 5.2 / 7.8 | 4.9 | 4.32 |
| anchored, per-name, 50 images | 87 | 6.7 | 9.1 | 0 | 8.0 / 9.1 | 5.5 / 8.9 | 6.3 | 3.68 |
| native, per-name, source->grown | 58 | 13.9 | 38.4 | 41 | 13.9 / 38.4 | - / - | 10.3 | nan |
| native, per-name, source | 58 | 8.3 | 9.9 | 0 | 8.3 / 9.9 | - / - | 6.2 | nan |
| native, per-name, grown | 87 | 6.9 | 9.9 | 0 | 8.4 / 9.9 | 5.5 / 9.5 | 6.9 | 5.56 |
| anchored, image-level, all names | 270 | 24.5 | 100.0 | 148 | 13.5 / 52.3 | 27.5 / 100.0 | 9.9 | 2.45 |
| anchored, image-level, per-name names | 87 | 21.1 | 100.0 | 59 | 13.5 / 52.3 | 30.9 / 100.0 | 10.0 | 1.66 |
| hybrid, per-name or image-level | 270 | 20.3 | 100.0 | 98 | 8.4 / 9.9 | 23.7 / 100.0 | 6.9 | 4.37 |
| hybrid, per-name or image-level (calibrated names) | 87 | 6.9 | 9.9 | 0 | 8.4 / 9.9 | 5.5 / 9.5 | 6.9 | nan |
| hybrid, lower of both | 270 | 19.9 | 100.0 | 98 | 6.5 / 9.9 | 23.6 / 100.0 | 4.9 | 4.48 |
| hybrid, lower of both (calibrated names) | 87 | 5.7 | 9.9 | 0 | 6.4 / 9.9 | 5.4 / 9.5 | 4.9 | nan |

## alpha = 0.05

| Arm | Names | Macro risk (%) | Worst name (%) | Names over alpha | Source: macro / worst (%) | Added: macro / worst (%) | Image risk (%) | Size |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, per-name | 61 | 3.3 | 4.9 | 0 | 3.7 / 4.9 | 2.6 / 4.5 | 4.8 | 4.12 |
| anchored, per-name, 10 images | 0 | - | - | 0 | - / - | - / - | 100.0 | 0.00 |
| anchored, per-name, 20 images | 61 | 1.7 | 3.4 | 0 | 1.7 / 3.3 | 1.6 / 3.4 | 2.8 | 7.39 |
| anchored, per-name, 50 images | 61 | 3.0 | 4.1 | 0 | 3.3 / 4.1 | 2.5 / 3.7 | 4.3 | 4.50 |
| native, per-name, source->grown | 50 | 7.0 | 24.6 | 35 | 7.3 / 24.6 | - / - | 7.0 | nan |
| native, per-name, source | 50 | 3.6 | 4.9 | 0 | 3.7 / 4.9 | - / - | 4.6 | nan |
| native, per-name, grown | 61 | 3.4 | 4.9 | 0 | 3.8 / 4.9 | 2.7 / 4.6 | 4.8 | 5.58 |
| anchored, image-level, all names | 270 | 15.5 | 100.0 | 133 | 7.6 / 31.7 | 17.8 / 100.0 | 4.9 | 3.86 |
| anchored, image-level, per-name names | 61 | 12.7 | 98.9 | 41 | 7.8 / 31.7 | 28.1 / 98.9 | 6.7 | 2.07 |
| hybrid, per-name or image-level | 270 | 13.9 | 100.0 | 101 | 4.2 / 12.3 | 16.6 / 100.0 | 3.0 | 5.92 |
| hybrid, per-name or image-level (calibrated names) | 61 | 3.3 | 4.9 | 0 | 3.7 / 4.9 | 2.6 / 4.5 | 3.0 | nan |
| hybrid, lower of both | 270 | 13.7 | 100.0 | 101 | 3.5 / 12.3 | 16.5 / 100.0 | 2.1 | 6.04 |
| hybrid, lower of both (calibrated names) | 61 | 2.7 | 4.9 | 0 | 2.9 / 4.9 | 2.5 / 4.5 | 2.1 | nan |
