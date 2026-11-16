# Calibrate once, deploy under per-image vocabularies

CAT-Seg (vitl_bank683), 2000 ADE validation images (0 without a source-labelled sampled pixel excluded), 500 random half/half splits, image-level CRC on the source-label miss rate. Deployed vocabulary = 150 source names + per-image added names A(x): rand50 (50.0 on average), rand200 (200.0 on average), rand500 (500.0 on average), present (1.6 on average), tagger50 (50.0 on average). Risk in %, "above" = % of splits above alpha, size = deployed labels per source-labelled pixel. Development data; nothing fitted.

## alpha = 0.1, policy rand50

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 9.90 | 43.4 | 2.39 |
| native, frozen at 150 | 10.30 | 67.6 | 1.95 |
| native, recalibrated at 845 | 6.19 | 0.0 | 2.93 |
| native, matched to the policy | 9.90 | 42.6 | 2.01 |
| native, worst case over the policies | 6.47 | 0.0 | 2.83 |
| native, calibrated under rand200 | 8.53 | 1.2 | 2.27 |
| native, calibrated under rand500 | 6.84 | 0.0 | 2.70 |
| native, calibrated under present | 9.95 | 45.6 | 2.00 |
| native, calibrated under tagger50 | 6.56 | 0.0 | 2.80 |
| native, recalibrated at a 1,690-name lexicon | 5.21 | 0.0 | 3.40 |
| native, recalibrated at a 3,380-name lexicon | 4.40 | 0.0 | 3.92 |
| native, recalibrated at a 6,760-name lexicon | 3.66 | 0.0 | 4.54 |
| native, recalibrated at a 17,001-name lexicon | 2.24 | 0.0 | 6.45 |

## alpha = 0.1, policy rand200

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 9.90 | 43.4 | 2.83 |
| native, frozen at 150 | 11.82 | 100.0 | 2.03 |
| native, recalibrated at 845 | 7.27 | 0.0 | 3.14 |
| native, matched to the policy | 9.91 | 40.0 | 2.38 |
| native, worst case over the policies | 7.59 | 0.0 | 3.02 |
| native, calibrated under rand50 | 11.40 | 98.0 | 2.10 |
| native, calibrated under rand500 | 8.00 | 0.0 | 2.88 |
| native, calibrated under present | 11.46 | 98.6 | 2.09 |
| native, calibrated under tagger50 | 7.69 | 0.0 | 2.98 |
| native, recalibrated at a 1,690-name lexicon | 6.15 | 0.0 | 3.68 |
| native, recalibrated at a 3,380-name lexicon | 5.23 | 0.0 | 4.29 |
| native, recalibrated at a 6,760-name lexicon | 4.44 | 0.0 | 5.02 |
| native, recalibrated at a 17,001-name lexicon | 2.93 | 0.0 | 7.29 |

## alpha = 0.1, policy rand500

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 9.90 | 43.4 | 3.69 |
| native, frozen at 150 | 14.14 | 100.0 | 2.11 |
| native, recalibrated at 845 | 9.09 | 9.4 | 3.35 |
| native, matched to the policy | 9.92 | 43.0 | 3.06 |
| native, worst case over the policies | 9.46 | 20.4 | 3.21 |
| native, calibrated under rand50 | 13.67 | 100.0 | 2.18 |
| native, calibrated under rand200 | 11.99 | 100.0 | 2.50 |
| native, calibrated under present | 13.73 | 100.0 | 2.17 |
| native, calibrated under tagger50 | 9.57 | 25.2 | 3.17 |
| native, recalibrated at a 1,690-name lexicon | 7.76 | 0.0 | 3.97 |
| native, recalibrated at a 3,380-name lexicon | 6.66 | 0.0 | 4.69 |
| native, recalibrated at a 6,760-name lexicon | 5.69 | 0.0 | 5.55 |
| native, recalibrated at a 17,001-name lexicon | 3.93 | 0.0 | 8.25 |

## alpha = 0.1, policy present

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 9.90 | 43.4 | 2.32 |
| native, frozen at 150 | 10.25 | 65.0 | 1.93 |
| native, recalibrated at 845 | 6.18 | 0.0 | 2.85 |
| native, matched to the policy | 9.91 | 45.4 | 1.98 |
| native, worst case over the policies | 6.45 | 0.0 | 2.76 |
| native, calibrated under rand50 | 9.85 | 39.8 | 1.99 |
| native, calibrated under rand200 | 8.46 | 1.4 | 2.23 |
| native, calibrated under rand500 | 6.80 | 0.0 | 2.64 |
| native, calibrated under tagger50 | 6.54 | 0.0 | 2.73 |
| native, recalibrated at a 1,690-name lexicon | 5.22 | 0.0 | 3.28 |
| native, recalibrated at a 3,380-name lexicon | 4.42 | 0.0 | 3.76 |
| native, recalibrated at a 6,760-name lexicon | 3.69 | 0.0 | 4.31 |
| native, recalibrated at a 17,001-name lexicon | 2.27 | 0.0 | 6.01 |

## alpha = 0.1, policy tagger50

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 9.90 | 43.4 | 4.17 |
| native, frozen at 150 | 14.75 | 100.0 | 2.22 |
| native, recalibrated at 845 | 9.41 | 18.8 | 3.69 |
| native, matched to the policy | 9.92 | 44.8 | 3.47 |
| native, worst case over the policies | 9.80 | 39.4 | 3.52 |
| native, calibrated under rand50 | 14.25 | 100.0 | 2.31 |
| native, calibrated under rand200 | 12.49 | 100.0 | 2.67 |
| native, calibrated under rand500 | 10.29 | 65.6 | 3.33 |
| native, calibrated under present | 14.31 | 100.0 | 2.30 |
| native, recalibrated at a 1,690-name lexicon | 8.01 | 0.0 | 4.43 |
| native, recalibrated at a 3,380-name lexicon | 6.86 | 0.0 | 5.28 |
| native, recalibrated at a 6,760-name lexicon | 5.84 | 0.0 | 6.29 |
| native, recalibrated at a 17,001-name lexicon | 3.99 | 0.0 | 9.23 |

## alpha = 0.1, policy adversarial

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 9.90 | 43.4 | 4.17 |
| native, frozen at 150 | 14.86 | 100.0 | 2.20 |
| native, recalibrated at 845 | 9.53 | 24.8 | 3.58 |
| native, worst case over the policies | 9.92 | 42.8 | 3.43 |
| native, calibrated under rand50 | 14.35 | 100.0 | 2.28 |
| native, calibrated under rand200 | 12.59 | 100.0 | 2.63 |
| native, calibrated under rand500 | 10.41 | 71.0 | 3.25 |
| native, calibrated under present | 14.42 | 100.0 | 2.27 |
| native, calibrated under tagger50 | 10.04 | 49.6 | 3.38 |
| native, recalibrated at a 1,690-name lexicon | 8.14 | 0.2 | 4.27 |
| native, recalibrated at a 3,380-name lexicon | 6.98 | 0.0 | 5.07 |
| native, recalibrated at a 6,760-name lexicon | 5.95 | 0.0 | 6.03 |
| native, recalibrated at a 17,001-name lexicon | 4.12 | 0.0 | 8.92 |

## alpha = 0.05, policy rand50

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 4.90 | 43.2 | 4.01 |
| native, frozen at 150 | 5.12 | 57.2 | 3.45 |
| native, recalibrated at 845 | 2.62 | 0.0 | 5.81 |
| native, matched to the policy | 4.91 | 41.8 | 3.58 |
| native, worst case over the policies | 2.88 | 0.0 | 5.44 |
| native, calibrated under rand200 | 4.11 | 2.6 | 4.15 |
| native, calibrated under rand500 | 3.05 | 0.0 | 5.22 |
| native, calibrated under present | 4.89 | 40.2 | 3.59 |
| native, calibrated under tagger50 | 2.97 | 0.0 | 5.32 |
| native, recalibrated at a 1,690-name lexicon | 2.04 | 0.0 | 6.89 |
| native, recalibrated at a 3,380-name lexicon | 1.58 | 0.0 | 8.27 |
| native, recalibrated at a 6,760-name lexicon | 1.14 | 0.0 | 10.79 |
| native, recalibrated at a 17,001-name lexicon | 0.15 | 0.0 | 45.41 |

## alpha = 0.05, policy rand200

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 4.90 | 43.2 | 5.09 |
| native, frozen at 150 | 6.05 | 98.4 | 3.74 |
| native, recalibrated at 845 | 3.34 | 0.0 | 6.52 |
| native, matched to the policy | 4.91 | 42.0 | 4.56 |
| native, worst case over the policies | 3.60 | 0.0 | 6.09 |
| native, calibrated under rand50 | 5.81 | 93.0 | 3.89 |
| native, calibrated under rand500 | 3.78 | 0.4 | 5.82 |
| native, calibrated under present | 5.78 | 93.2 | 3.90 |
| native, calibrated under tagger50 | 3.69 | 0.0 | 5.94 |
| native, recalibrated at a 1,690-name lexicon | 2.70 | 0.0 | 7.81 |
| native, recalibrated at a 3,380-name lexicon | 2.15 | 0.0 | 9.46 |
| native, recalibrated at a 6,760-name lexicon | 1.57 | 0.0 | 12.49 |
| native, recalibrated at a 17,001-name lexicon | 0.28 | 0.0 | 55.78 |

## alpha = 0.05, policy rand500

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 4.90 | 43.2 | 7.22 |
| native, frozen at 150 | 7.64 | 100.0 | 4.04 |
| native, recalibrated at 845 | 4.39 | 10.2 | 7.34 |
| native, matched to the policy | 4.92 | 43.2 | 6.50 |
| native, worst case over the policies | 4.71 | 28.8 | 6.82 |
| native, calibrated under rand50 | 7.35 | 100.0 | 4.21 |
| native, calibrated under rand200 | 6.27 | 99.4 | 5.00 |
| native, calibrated under present | 7.32 | 100.0 | 4.23 |
| native, calibrated under tagger50 | 4.83 | 35.2 | 6.64 |
| native, recalibrated at a 1,690-name lexicon | 3.67 | 0.0 | 8.88 |
| native, recalibrated at a 3,380-name lexicon | 3.03 | 0.0 | 10.85 |
| native, recalibrated at a 6,760-name lexicon | 2.31 | 0.0 | 14.45 |
| native, recalibrated at a 17,001-name lexicon | 0.56 | 0.0 | 61.74 |

## alpha = 0.05, policy present

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 4.90 | 43.2 | 3.79 |
| native, frozen at 150 | 5.14 | 59.6 | 3.33 |
| native, recalibrated at 845 | 2.65 | 0.0 | 5.44 |
| native, matched to the policy | 4.90 | 40.8 | 3.46 |
| native, worst case over the policies | 2.91 | 0.0 | 5.11 |
| native, calibrated under rand50 | 4.93 | 43.0 | 3.44 |
| native, calibrated under rand200 | 4.13 | 3.2 | 3.96 |
| native, calibrated under rand500 | 3.08 | 0.0 | 4.92 |
| native, calibrated under tagger50 | 3.00 | 0.0 | 5.00 |
| native, recalibrated at a 1,690-name lexicon | 2.07 | 0.0 | 6.40 |
| native, recalibrated at a 3,380-name lexicon | 1.62 | 0.0 | 7.61 |
| native, recalibrated at a 6,760-name lexicon | 1.16 | 0.0 | 9.81 |
| native, recalibrated at a 17,001-name lexicon | 0.14 | 0.0 | 38.03 |

## alpha = 0.05, policy tagger50

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 4.90 | 43.2 | 7.86 |
| native, frozen at 150 | 7.89 | 100.0 | 4.51 |
| native, recalibrated at 845 | 4.48 | 15.0 | 8.27 |
| native, matched to the policy | 4.92 | 43.2 | 7.52 |
| native, worst case over the policies | 4.80 | 34.0 | 7.71 |
| native, calibrated under rand50 | 7.58 | 100.0 | 4.72 |
| native, calibrated under rand200 | 6.45 | 99.8 | 5.65 |
| native, calibrated under rand500 | 5.02 | 49.8 | 7.36 |
| native, calibrated under present | 7.55 | 100.0 | 4.74 |
| native, recalibrated at a 1,690-name lexicon | 3.72 | 0.4 | 9.87 |
| native, recalibrated at a 3,380-name lexicon | 3.03 | 0.0 | 11.77 |
| native, recalibrated at a 6,760-name lexicon | 2.26 | 0.0 | 15.03 |
| native, recalibrated at a 17,001-name lexicon | 0.43 | 0.0 | 50.25 |

## alpha = 0.05, policy adversarial

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 4.90 | 43.2 | 7.95 |
| native, frozen at 150 | 8.01 | 100.0 | 4.35 |
| native, recalibrated at 845 | 4.60 | 23.8 | 7.96 |
| native, worst case over the policies | 4.92 | 42.8 | 7.41 |
| native, calibrated under rand50 | 7.70 | 100.0 | 4.54 |
| native, calibrated under rand200 | 6.57 | 99.8 | 5.43 |
| native, calibrated under rand500 | 5.14 | 58.0 | 7.07 |
| native, calibrated under present | 7.67 | 100.0 | 4.56 |
| native, calibrated under tagger50 | 5.04 | 51.6 | 7.22 |
| native, recalibrated at a 1,690-name lexicon | 3.85 | 1.0 | 9.58 |
| native, recalibrated at a 3,380-name lexicon | 3.16 | 0.0 | 11.57 |
| native, recalibrated at a 6,760-name lexicon | 2.40 | 0.0 | 15.12 |
| native, recalibrated at a 17,001-name lexicon | 0.57 | 0.0 | 61.87 |
