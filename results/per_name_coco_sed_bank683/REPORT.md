# Per-name (class-conditional) calibration

sed_bank683, 2000 COCO val2017 (LVIS-annotated) images, 1283 names (171 source; 660 present in some image), 500 random half/half splits. Calibrated: mean number of present names per split with a qualifying threshold (at least 1/alpha - 1 calibration images containing the name); the others are left out of the sets. Per calibrated name: mean loss over the held-out images containing it, averaged over the splits in which it is calibrated (the per-name arms guarantee at most alpha for every name). Over alpha: names calibrated in at least {MIN_SPLITS} splits whose split-averaged risk exceeds alpha by more than 3 standard errors over splits; worst name and the source/added columns use the same names. Image risk: the paper's image-level loss (missed fraction of source-labelled pixels, names outside the sets missed), mean over held-out images and splits. Size: labels per labelled pixel at 1283 names, held-out images, first 20 splits. Development data; nothing fitted.

## alpha = 0.1

| Arm | Names | Macro risk (%) | Worst name (%) | Names over alpha | Source: macro / worst (%) | Added: macro / worst (%) | Image risk (%) | Size |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, per-name | 198 | 6.9 | 18.0 | 0 | 7.8 / 9.8 | 5.6 / 18.0 | 4.9 | 11.68 |
| anchored, per-name, 10 images | 198 | 5.0 | 18.0 | 0 | 5.1 / 9.8 | 4.9 / 18.0 | 2.6 | 18.43 |
| anchored, per-name, 20 images | 198 | 6.3 | 18.0 | 0 | 6.8 / 9.8 | 5.6 / 18.0 | 3.8 | 13.13 |
| anchored, per-name, 50 images | 198 | 6.8 | 18.0 | 0 | 7.6 / 9.8 | 5.6 / 18.0 | 4.6 | 11.85 |
| native, per-name, source->grown | 156 | 3.8 | 9.8 | 0 | 3.8 / 9.8 | - / - | 2.2 | nan |
| native, per-name, source | 156 | 7.7 | 9.8 | 0 | 7.8 / 9.8 | - / - | 5.2 | nan |
| native, per-name, grown | 198 | 6.9 | 17.9 | 0 | 7.8 / 9.8 | 5.6 / 17.9 | 4.9 | 11.50 |
| anchored, image-level, all names | 660 | 39.0 | 100.0 | 458 | 28.1 / 100.0 | 42.9 / 100.0 | 9.9 | 3.61 |
| anchored, image-level, per-name names | 198 | 34.3 | 100.0 | 176 | 26.7 / 96.9 | 49.2 / 100.0 | 10.5 | 2.32 |
| hybrid, per-name or image-level | 660 | 31.9 | 100.0 | 312 | 11.2 / 100.0 | 39.2 / 100.0 | 4.2 | 12.97 |
| hybrid, per-name or image-level (calibrated names) | 198 | 6.9 | 18.0 | 0 | 7.8 / 9.8 | 5.6 / 18.0 | 4.2 | nan |
| hybrid, lower of both | 660 | 31.8 | 100.0 | 312 | 10.7 / 100.0 | 39.2 / 100.0 | 3.4 | 13.04 |
| hybrid, lower of both (calibrated names) | 198 | 6.6 | 18.0 | 0 | 7.2 / 9.8 | 5.6 / 18.0 | 3.4 | nan |

## alpha = 0.05

| Arm | Names | Macro risk (%) | Worst name (%) | Names over alpha | Source: macro / worst (%) | Added: macro / worst (%) | Image risk (%) | Size |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, per-name | 129 | 3.1 | 5.7 | 0 | 3.3 / 5.7 | 2.2 / 5.0 | 9.1 | 12.03 |
| anchored, per-name, 10 images | 0 | - | - | 0 | - / - | - / - | 100.0 | 0.00 |
| anchored, per-name, 20 images | 129 | 2.2 | 5.7 | 0 | 2.3 / 5.7 | 2.0 / 5.0 | 8.2 | 16.95 |
| anchored, per-name, 50 images | 129 | 2.9 | 5.7 | 0 | 3.2 / 5.7 | 2.2 / 5.0 | 8.9 | 12.60 |
| native, per-name, source->grown | 121 | 1.5 | 5.7 | 0 | 1.5 / 5.7 | - / - | 8.1 | nan |
| native, per-name, source | 121 | 3.2 | 5.7 | 0 | 3.3 / 5.7 | - / - | 9.3 | nan |
| native, per-name, grown | 129 | 3.0 | 5.7 | 0 | 3.3 / 5.7 | 2.0 / 4.1 | 9.1 | 12.53 |
| anchored, image-level, all names | 660 | 26.1 | 100.0 | 397 | 17.5 / 100.0 | 29.1 / 100.0 | 4.9 | 6.25 |
| anchored, image-level, per-name names | 129 | 19.1 | 88.6 | 125 | 15.6 / 67.9 | 35.6 / 88.6 | 11.5 | 3.17 |
| hybrid, per-name or image-level | 660 | 23.6 | 100.0 | 313 | 9.4 / 100.0 | 28.6 / 100.0 | 2.5 | 15.11 |
| hybrid, per-name or image-level (calibrated names) | 129 | 3.1 | 5.7 | 0 | 3.3 / 5.7 | 2.2 / 5.0 | 2.5 | nan |
| hybrid, lower of both | 660 | 23.6 | 100.0 | 313 | 9.2 / 100.0 | 28.6 / 100.0 | 2.2 | 15.20 |
| hybrid, lower of both (calibrated names) | 129 | 2.9 | 5.7 | 0 | 3.1 / 5.7 | 2.2 / 5.0 | 2.2 | nan |
