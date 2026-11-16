# Per-name (class-conditional) calibration

fcclip_bank683, 2000 ADE validation images, 845 names (150 source; 836 present in some image), 500 random half/half splits. Calibrated: mean number of present names per split with a qualifying threshold (at least 1/alpha - 1 calibration images containing the name); the others are left out of the sets. Per calibrated name: mean loss over the held-out images containing it, averaged over the splits in which it is calibrated (the per-name arms guarantee at most alpha for every name). Over alpha: names calibrated in at least {MIN_SPLITS} splits whose split-averaged risk exceeds alpha by more than 3 standard errors over splits; worst name and the source/added columns use the same names. Image risk: the paper's image-level loss (missed fraction of source-labelled pixels, names outside the sets missed), mean over held-out images and splits. Size: labels per labelled pixel at 845 names, held-out images, first 20 splits. Development data; nothing fitted.

## alpha = 0.1

| Arm | Names | Macro risk (%) | Worst name (%) | Names over alpha | Source: macro / worst (%) | Added: macro / worst (%) | Image risk (%) | Size |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, per-name | 160 | 6.6 | 10.9 | 0 | 7.3 / 10.9 | 5.5 / 10.5 | 8.1 | 25.29 |
| anchored, per-name, 10 images | 160 | 4.5 | 10.9 | 0 | 4.3 / 10.9 | 4.8 / 10.5 | 4.4 | 36.64 |
| anchored, per-name, 20 images | 160 | 5.9 | 10.9 | 0 | 6.3 / 10.9 | 5.4 / 10.5 | 6.5 | 27.97 |
| anchored, per-name, 50 images | 160 | 6.5 | 10.9 | 0 | 7.2 / 10.9 | 5.5 / 10.5 | 7.6 | 25.58 |
| native, per-name, source->grown | 118 | 11.6 | 71.9 | 65 | 11.6 / 71.9 | - / - | 12.3 | nan |
| native, per-name, source | 118 | 7.4 | 11.4 | 0 | 7.4 / 11.4 | - / - | 7.7 | nan |
| native, per-name, grown | 160 | 6.7 | 20.3 | 0 | 7.3 / 9.9 | 5.8 / 20.3 | 7.8 | 24.76 |
| anchored, image-level, all names | 836 | 25.8 | 100.0 | 404 | 21.5 / 99.9 | 26.7 / 100.0 | 9.9 | 11.56 |
| anchored, image-level, per-name names | 160 | 29.5 | 100.0 | 135 | 23.3 / 99.9 | 38.2 / 100.0 | 11.9 | 4.10 |
| hybrid, per-name or image-level | 836 | 22.0 | 100.0 | 308 | 10.2 / 96.7 | 24.6 / 100.0 | 6.1 | 32.75 |
| hybrid, per-name or image-level (calibrated names) | 160 | 6.6 | 10.9 | 0 | 7.3 / 10.9 | 5.5 / 10.5 | 6.1 | nan |
| hybrid, lower of both | 836 | 21.8 | 100.0 | 308 | 9.2 / 96.7 | 24.6 / 100.0 | 4.7 | 33.12 |
| hybrid, lower of both (calibrated names) | 160 | 5.9 | 10.9 | 0 | 6.2 / 10.9 | 5.3 / 10.5 | 4.7 | nan |

## alpha = 0.05

| Arm | Names | Macro risk (%) | Worst name (%) | Names over alpha | Source: macro / worst (%) | Added: macro / worst (%) | Image risk (%) | Size |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| anchored, per-name | 96 | 2.9 | 5.6 | 0 | 3.2 / 4.9 | 2.9 / 5.6 | 8.4 | 21.06 |
| anchored, per-name, 10 images | 0 | - | - | 0 | - / - | - / - | 100.0 | 0.00 |
| anchored, per-name, 20 images | 96 | 1.7 | 5.6 | 0 | 1.6 / 4.1 | 2.8 / 5.6 | 6.9 | 31.18 |
| anchored, per-name, 50 images | 96 | 2.7 | 5.6 | 0 | 2.9 / 4.1 | 2.9 / 5.6 | 7.9 | 22.06 |
| native, per-name, source->grown | 86 | 4.9 | 19.7 | 37 | 5.0 / 19.7 | - / - | 9.8 | nan |
| native, per-name, source | 86 | 3.1 | 4.9 | 0 | 3.2 / 4.9 | - / - | 8.2 | nan |
| native, per-name, grown | 96 | 3.0 | 6.5 | 0 | 3.2 / 4.9 | 2.6 / 6.5 | 8.3 | 21.63 |
| anchored, image-level, all names | 836 | 15.7 | 100.0 | 330 | 11.9 / 97.5 | 16.6 / 100.0 | 4.9 | 31.37 |
| anchored, image-level, per-name names | 96 | 14.7 | 97.5 | 67 | 11.7 / 97.5 | 28.9 / 91.3 | 10.6 | 6.55 |
| hybrid, per-name or image-level | 836 | 14.6 | 100.0 | 280 | 7.2 / 84.6 | 16.2 / 100.0 | 2.7 | 45.89 |
| hybrid, per-name or image-level (calibrated names) | 96 | 2.9 | 5.6 | 0 | 3.2 / 4.9 | 2.9 / 5.6 | 2.7 | nan |
| hybrid, lower of both | 836 | 14.5 | 100.0 | 280 | 6.8 / 84.6 | 16.2 / 100.0 | 1.9 | 46.70 |
| hybrid, lower of both (calibrated names) | 96 | 2.4 | 5.6 | 0 | 2.5 / 4.7 | 2.8 / 5.6 | 1.9 | nan |
