# Calibrate once, deploy under per-image vocabularies

SED (sed_bank683), 2000 Pascal Context validation images (0 without a source-labelled sampled pixel excluded), 500 random half/half splits, image-level CRC on the source-label miss rate. Deployed vocabulary = 59 source names + per-image added names A(x): rand50 (50.0 on average), rand100 (100.0 on average), rand300 (300.0 on average), present (1.1 on average), tagger50 (50.0 on average). Risk in %, "above" = % of splits above alpha, size = deployed labels per source-labelled pixel. Development data; nothing fitted.

## alpha = 0.1, policy rand50

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 9.83 | 42.8 | 1.81 |
| native, frozen at 59 | 8.22 | 0.4 | 1.81 |
| native, recalibrated at 458 | 15.17 | 100.0 | 1.23 |
| native, matched to the policy | 9.84 | 41.8 | 1.62 |
| native, worst case over the policies | 6.29 | 0.0 | 2.10 |
| native, calibrated under rand100 | 10.93 | 85.6 | 1.52 |
| native, calibrated under rand300 | 14.24 | 100.0 | 1.28 |
| native, calibrated under present | 8.16 | 0.4 | 1.81 |
| native, calibrated under tagger50 | 6.57 | 0.0 | 2.05 |

## alpha = 0.1, policy rand100

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 9.83 | 42.8 | 1.95 |
| native, frozen at 59 | 7.32 | 0.0 | 2.08 |
| native, recalibrated at 458 | 13.66 | 100.0 | 1.37 |
| native, matched to the policy | 9.83 | 40.0 | 1.72 |
| native, worst case over the policies | 5.52 | 0.0 | 2.47 |
| native, calibrated under rand50 | 8.86 | 3.8 | 1.85 |
| native, calibrated under rand300 | 12.81 | 99.8 | 1.43 |
| native, calibrated under present | 7.26 | 0.0 | 2.09 |
| native, calibrated under tagger50 | 5.78 | 0.0 | 2.41 |

## alpha = 0.1, policy rand300

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 9.83 | 42.8 | 2.52 |
| native, frozen at 59 | 5.01 | 0.0 | 3.85 |
| native, recalibrated at 458 | 10.58 | 76.0 | 2.18 |
| native, matched to the policy | 9.81 | 39.6 | 2.32 |
| native, worst case over the policies | 3.73 | 0.0 | 4.75 |
| native, calibrated under rand50 | 6.25 | 0.0 | 3.29 |
| native, calibrated under rand100 | 7.12 | 0.0 | 2.99 |
| native, calibrated under present | 4.97 | 0.0 | 3.87 |
| native, calibrated under tagger50 | 3.92 | 0.0 | 4.60 |

## alpha = 0.1, policy present

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 9.83 | 42.8 | 1.71 |
| native, frozen at 59 | 9.90 | 47.0 | 1.55 |
| native, recalibrated at 458 | 18.86 | 100.0 | 1.06 |
| native, matched to the policy | 9.83 | 42.4 | 1.56 |
| native, worst case over the policies | 7.69 | 0.2 | 1.78 |
| native, calibrated under rand50 | 11.87 | 98.6 | 1.40 |
| native, calibrated under rand100 | 13.21 | 99.8 | 1.31 |
| native, calibrated under rand300 | 17.55 | 100.0 | 1.10 |
| native, calibrated under tagger50 | 8.01 | 0.2 | 1.74 |

## alpha = 0.1, policy tagger50

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 9.83 | 42.8 | 2.80 |
| native, frozen at 59 | 11.75 | 99.4 | 2.07 |
| native, recalibrated at 458 | 19.41 | 100.0 | 1.27 |
| native, matched to the policy | 9.83 | 42.0 | 2.44 |
| native, worst case over the policies | 9.49 | 23.0 | 2.52 |
| native, calibrated under rand50 | 13.50 | 100.0 | 1.79 |
| native, calibrated under rand100 | 14.70 | 100.0 | 1.65 |
| native, calibrated under rand300 | 18.40 | 100.0 | 1.33 |
| native, calibrated under present | 11.69 | 99.0 | 2.08 |

## alpha = 0.1, policy adversarial

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 9.83 | 42.8 | 2.80 |
| native, frozen at 59 | 12.26 | 99.8 | 1.94 |
| native, recalibrated at 458 | 21.06 | 100.0 | 1.13 |
| native, worst case over the policies | 9.84 | 41.4 | 2.42 |
| native, calibrated under rand50 | 14.21 | 100.0 | 1.64 |
| native, calibrated under rand100 | 15.52 | 100.0 | 1.50 |
| native, calibrated under rand300 | 19.81 | 100.0 | 1.19 |
| native, calibrated under present | 12.19 | 99.8 | 1.95 |
| native, calibrated under tagger50 | 10.20 | 59.0 | 2.34 |

## alpha = 0.05, policy rand50

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 4.84 | 34.8 | 2.63 |
| native, frozen at 59 | 3.93 | 1.0 | 2.72 |
| native, recalibrated at 458 | 8.57 | 100.0 | 1.76 |
| native, matched to the policy | 4.86 | 38.8 | 2.43 |
| native, worst case over the policies | 2.87 | 0.0 | 3.21 |
| native, calibrated under rand100 | 5.60 | 86.0 | 2.25 |
| native, calibrated under rand300 | 7.97 | 100.0 | 1.84 |
| native, calibrated under present | 3.87 | 0.6 | 2.74 |
| native, calibrated under tagger50 | 2.94 | 0.0 | 3.16 |

## alpha = 0.05, policy rand100

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 4.84 | 34.8 | 2.95 |
| native, frozen at 59 | 3.33 | 0.0 | 3.31 |
| native, recalibrated at 458 | 7.65 | 100.0 | 2.03 |
| native, matched to the policy | 4.84 | 38.2 | 2.67 |
| native, worst case over the policies | 2.48 | 0.0 | 3.99 |
| native, calibrated under rand50 | 4.14 | 4.0 | 2.92 |
| native, calibrated under rand300 | 7.08 | 99.8 | 2.13 |
| native, calibrated under present | 3.28 | 0.0 | 3.34 |
| native, calibrated under tagger50 | 2.54 | 0.0 | 3.93 |

## alpha = 0.05, policy rand300

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 4.84 | 34.8 | 4.18 |
| native, frozen at 59 | 2.24 | 0.0 | 6.68 |
| native, recalibrated at 458 | 5.26 | 66.2 | 3.72 |
| native, matched to the policy | 4.85 | 41.2 | 3.95 |
| native, worst case over the policies | 1.65 | 0.0 | 8.24 |
| native, calibrated under rand50 | 2.79 | 0.0 | 5.78 |
| native, calibrated under rand100 | 3.26 | 0.0 | 5.21 |
| native, calibrated under present | 2.21 | 0.0 | 6.75 |
| native, calibrated under tagger50 | 1.69 | 0.0 | 8.09 |

## alpha = 0.05, policy present

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 4.84 | 34.8 | 2.41 |
| native, frozen at 59 | 4.93 | 44.8 | 2.25 |
| native, recalibrated at 458 | 10.32 | 100.0 | 1.51 |
| native, matched to the policy | 4.85 | 40.0 | 2.26 |
| native, worst case over the policies | 3.65 | 0.4 | 2.60 |
| native, calibrated under rand50 | 6.00 | 96.8 | 2.03 |
| native, calibrated under rand100 | 6.86 | 99.8 | 1.90 |
| native, calibrated under rand300 | 9.61 | 100.0 | 1.58 |
| native, calibrated under tagger50 | 3.74 | 0.4 | 2.57 |

## alpha = 0.05, policy tagger50

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 4.84 | 34.8 | 4.77 |
| native, frozen at 59 | 6.27 | 98.8 | 3.51 |
| native, recalibrated at 458 | 12.13 | 100.0 | 2.00 |
| native, matched to the policy | 4.85 | 39.0 | 4.25 |
| native, worst case over the policies | 4.73 | 29.8 | 4.32 |
| native, calibrated under rand50 | 7.54 | 100.0 | 3.04 |
| native, calibrated under rand100 | 8.56 | 100.0 | 2.75 |
| native, calibrated under rand300 | 11.47 | 100.0 | 2.12 |
| native, calibrated under present | 6.18 | 98.2 | 3.54 |

## alpha = 0.05, policy adversarial

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 4.84 | 34.8 | 4.77 |
| native, frozen at 59 | 6.46 | 99.0 | 3.59 |
| native, recalibrated at 458 | 12.68 | 100.0 | 1.87 |
| native, worst case over the policies | 4.84 | 37.6 | 4.72 |
| native, calibrated under rand50 | 7.79 | 100.0 | 3.03 |
| native, calibrated under rand100 | 8.86 | 100.0 | 2.68 |
| native, calibrated under rand300 | 11.96 | 100.0 | 2.00 |
| native, calibrated under present | 6.36 | 98.8 | 3.64 |
| native, calibrated under tagger50 | 4.97 | 47.8 | 4.61 |
