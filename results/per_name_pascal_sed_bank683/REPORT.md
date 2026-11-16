# Per-name (class-conditional) calibration

sed_bank683, 2000 Pascal Context validation images, 458 names (59 source; 270 present in some image), 500 random half/half splits. Calibrated: mean number of present names per split with a qualifying threshold (at least 1/alpha - 1 calibration images containing the name); the others are left out of the sets. Per calibrated name: mean loss over the held-out images containing it, averaged over the splits in which it is calibrated (the per-name arms guarantee at most alpha for every name). Over alpha: names calibrated in at least {MIN_SPLITS} splits whose split-averaged risk exceeds alpha by more than 3 standard errors over splits; worst name and the source/added columns use the same names. Image risk: the paper's image-level loss (missed fraction of source-labelled pixels, names outside the sets missed), mean over held-out images and splits. Size: labels per labelled pixel at 458 names, held-out images, first 20 splits. Development data; nothing fitted.

## alpha = 0.1

| Arm | Names | Macro risk (%) | Worst name (%) | Names over alpha | Source: macro / worst (%) | Added: macro / worst (%) | Image risk (%) | Size |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, per-name | 87 | 7.1 | 12.3 | 0 | 8.4 / 9.9 | 6.2 / 12.3 | 6.0 | 5.52 |
| anchored, per-name, 10 images | 87 | 4.6 | 12.3 | 0 | 4.7 / 9.1 | 5.0 / 12.3 | 2.5 | 9.19 |
| anchored, per-name, 20 images | 87 | 6.1 | 12.3 | 0 | 6.8 / 8.2 | 5.8 / 12.3 | 4.3 | 6.48 |
| anchored, per-name, 50 images | 87 | 6.9 | 12.3 | 0 | 8.1 / 9.1 | 6.2 / 12.3 | 5.5 | 5.67 |
| native, per-name, source->grown | 58 | 4.4 | 8.1 | 0 | 4.4 / 8.1 | - / - | 2.0 | nan |
| native, per-name, source | 58 | 8.4 | 9.9 | 0 | 8.4 / 9.9 | - / - | 5.6 | nan |
| native, per-name, grown | 87 | 7.1 | 9.9 | 0 | 8.4 / 9.9 | 6.1 / 9.6 | 6.0 | 5.51 |
| anchored, image-level, all names | 270 | 30.6 | 100.0 | 171 | 15.9 / 62.8 | 34.7 / 100.0 | 9.9 | 2.86 |
| anchored, image-level, per-name names | 87 | 27.3 | 98.8 | 70 | 15.9 / 62.8 | 42.5 / 98.8 | 10.0 | 1.80 |
| hybrid, per-name or image-level | 270 | 24.6 | 100.0 | 117 | 8.5 / 9.9 | 29.2 / 100.0 | 6.0 | 6.58 |
| hybrid, per-name or image-level (calibrated names) | 87 | 7.1 | 12.3 | 0 | 8.4 / 9.9 | 6.2 / 12.3 | 6.0 | nan |
| hybrid, lower of both | 270 | 24.3 | 100.0 | 117 | 6.9 / 9.9 | 29.1 / 100.0 | 4.3 | 6.71 |
| hybrid, lower of both (calibrated names) | 87 | 6.2 | 12.3 | 0 | 6.8 / 9.9 | 6.1 / 12.3 | 4.3 | nan |

## alpha = 0.05

| Arm | Names | Macro risk (%) | Worst name (%) | Names over alpha | Source: macro / worst (%) | Added: macro / worst (%) | Image risk (%) | Size |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, per-name | 61 | 3.4 | 6.1 | 0 | 3.9 / 6.1 | 2.7 / 4.6 | 4.4 | 6.88 |
| anchored, per-name, 10 images | 0 | - | - | 0 | - / - | - / - | 100.0 | 0.00 |
| anchored, per-name, 20 images | 61 | 2.0 | 6.1 | 0 | 2.2 / 6.1 | 1.9 / 3.2 | 2.6 | 10.31 |
| anchored, per-name, 50 images | 61 | 3.2 | 6.1 | 0 | 3.6 / 6.1 | 2.6 / 3.9 | 3.9 | 7.37 |
| native, per-name, source->grown | 50 | 1.9 | 3.8 | 0 | 2.0 / 3.8 | - / - | 2.6 | nan |
| native, per-name, source | 50 | 3.7 | 5.2 | 0 | 3.9 / 5.2 | - / - | 4.2 | nan |
| native, per-name, grown | 61 | 3.4 | 5.6 | 0 | 3.9 / 5.6 | 2.7 / 4.7 | 4.4 | 7.54 |
| anchored, image-level, all names | 270 | 19.4 | 100.0 | 148 | 9.3 / 38.3 | 22.2 / 100.0 | 4.9 | 4.90 |
| anchored, image-level, per-name names | 61 | 16.5 | 97.6 | 44 | 9.2 / 38.3 | 37.4 / 97.6 | 6.7 | 2.37 |
| hybrid, per-name or image-level | 270 | 17.0 | 100.0 | 113 | 5.0 / 28.6 | 20.3 / 100.0 | 2.6 | 9.40 |
| hybrid, per-name or image-level (calibrated names) | 61 | 3.4 | 6.1 | 0 | 3.9 / 6.1 | 2.7 / 4.6 | 2.6 | nan |
| hybrid, lower of both | 270 | 16.8 | 100.0 | 113 | 4.5 / 28.6 | 20.3 / 100.0 | 1.9 | 9.55 |
| hybrid, lower of both (calibrated names) | 61 | 3.0 | 6.1 | 0 | 3.3 / 6.1 | 2.7 / 4.6 | 1.9 | nan |
