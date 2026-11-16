# Per-name (class-conditional) calibration

vitl_bank683, 2000 ADE validation images, 845 names (150 source; 836 present in some image), 500 random half/half splits. Calibrated: mean number of present names per split with a qualifying threshold (at least 1/alpha - 1 calibration images containing the name); the others are left out of the sets. Per calibrated name: mean loss over the held-out images containing it, averaged over the splits in which it is calibrated (the per-name arms guarantee at most alpha for every name). Over alpha: names calibrated in at least {MIN_SPLITS} splits whose split-averaged risk exceeds alpha by more than 3 standard errors over splits; worst name and the source/added columns use the same names. Image risk: the paper's image-level loss (missed fraction of source-labelled pixels, names outside the sets missed), mean over held-out images and splits. Size: labels per labelled pixel at 845 names, held-out images, first 20 splits. Development data; nothing fitted.

## alpha = 0.1

| Arm | Names | Macro risk (%) | Worst name (%) | Names over alpha | Source: macro / worst (%) | Added: macro / worst (%) | Image risk (%) | Size |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, per-name | 160 | 6.8 | 12.4 | 0 | 7.4 / 9.9 | 6.2 / 12.4 | 8.1 | 10.94 |
| anchored, per-name, 10 images | 160 | 5.0 | 12.4 | 0 | 4.7 / 9.3 | 5.8 / 12.4 | 4.8 | 16.07 |
| anchored, per-name, 20 images | 160 | 6.1 | 12.4 | 0 | 6.3 / 8.5 | 6.2 / 12.4 | 6.5 | 12.35 |
| anchored, per-name, 50 images | 160 | 6.6 | 12.4 | 0 | 7.2 / 9.0 | 6.2 / 12.4 | 7.5 | 11.13 |
| native, per-name, source->grown | 118 | 13.8 | 53.3 | 89 | 13.8 / 53.3 | - / - | 11.9 | nan |
| native, per-name, source | 118 | 7.3 | 9.9 | 0 | 7.3 / 9.9 | - / - | 7.7 | nan |
| native, per-name, grown | 160 | 6.6 | 15.4 | 0 | 7.4 / 9.9 | 5.9 / 15.4 | 8.2 | 21.71 |
| anchored, image-level, all names | 836 | 33.8 | 100.0 | 511 | 22.1 / 100.0 | 36.3 / 100.0 | 9.9 | 4.47 |
| anchored, image-level, per-name names | 160 | 29.9 | 100.0 | 154 | 22.8 / 100.0 | 40.0 / 100.0 | 11.8 | 2.26 |
| hybrid, per-name or image-level | 836 | 30.1 | 100.0 | 403 | 11.2 / 97.7 | 34.2 / 100.0 | 6.1 | 13.15 |
| hybrid, per-name or image-level (calibrated names) | 160 | 6.8 | 12.4 | 0 | 7.4 / 9.9 | 6.2 / 12.4 | 6.1 | nan |
| hybrid, lower of both | 836 | 30.0 | 100.0 | 403 | 10.5 / 97.7 | 34.2 / 100.0 | 4.8 | 13.30 |
| hybrid, lower of both (calibrated names) | 160 | 6.2 | 12.4 | 0 | 6.5 / 9.9 | 6.1 / 12.4 | 4.8 | nan |

## alpha = 0.05

| Arm | Names | Macro risk (%) | Worst name (%) | Names over alpha | Source: macro / worst (%) | Added: macro / worst (%) | Image risk (%) | Size |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, per-name | 96 | 3.0 | 4.9 | 0 | 3.3 / 4.9 | 2.6 / 4.9 | 8.6 | 9.04 |
| anchored, per-name, 10 images | 0 | - | - | 0 | - / - | - / - | 100.0 | 0.00 |
| anchored, per-name, 20 images | 96 | 2.0 | 5.2 | 0 | 2.0 / 4.4 | 2.4 / 5.2 | 7.1 | 13.96 |
| anchored, per-name, 50 images | 96 | 2.8 | 4.9 | 0 | 3.1 / 4.4 | 2.6 / 4.9 | 8.1 | 9.66 |
| native, per-name, source->grown | 86 | 7.2 | 43.1 | 65 | 7.3 / 43.1 | - / - | 10.7 | nan |
| native, per-name, source | 86 | 3.2 | 4.9 | 0 | 3.3 / 4.9 | - / - | 8.4 | nan |
| native, per-name, grown | 96 | 3.0 | 5.0 | 0 | 3.4 / 4.9 | 2.4 / 5.0 | 8.6 | 17.36 |
| anchored, image-level, all names | 836 | 22.1 | 100.0 | 427 | 13.5 / 98.6 | 24.0 / 100.0 | 4.9 | 8.95 |
| anchored, image-level, per-name names | 96 | 15.2 | 100.0 | 82 | 12.6 / 97.1 | 24.3 / 100.0 | 10.4 | 2.91 |
| hybrid, per-name or image-level | 836 | 21.1 | 100.0 | 368 | 8.7 / 98.6 | 23.8 / 100.0 | 3.1 | 15.07 |
| hybrid, per-name or image-level (calibrated names) | 96 | 3.0 | 4.9 | 0 | 3.3 / 4.9 | 2.6 / 4.9 | 3.1 | nan |
| hybrid, lower of both | 836 | 21.0 | 100.0 | 368 | 8.5 / 98.6 | 23.8 / 100.0 | 2.5 | 15.26 |
| hybrid, lower of both (calibrated names) | 96 | 2.7 | 4.9 | 0 | 2.9 / 4.9 | 2.5 / 4.9 | 2.5 | nan |
