# Calibrate once, deploy under per-image vocabularies

SED (sed_bank683), 2000 ADE validation images (0 without a source-labelled sampled pixel excluded), 500 random half/half splits, image-level CRC on the source-label miss rate. Deployed vocabulary = 150 source names + per-image added names A(x): rand50 (50.0 on average), rand200 (200.0 on average), rand500 (500.0 on average), present (1.6 on average), tagger50 (50.0 on average). Risk in %, "above" = % of splits above alpha, size = deployed labels per source-labelled pixel. Development data; nothing fitted.

## alpha = 0.1, policy rand50

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 9.90 | 45.0 | 2.99 |
| native, frozen at 150 | 9.02 | 6.6 | 2.61 |
| native, recalibrated at 845 | 13.62 | 100.0 | 1.81 |
| native, matched to the policy | 9.90 | 42.8 | 2.38 |
| native, worst case over the policies | 7.00 | 0.0 | 3.46 |
| native, calibrated under rand200 | 11.61 | 97.8 | 2.07 |
| native, calibrated under rand500 | 13.26 | 100.0 | 1.85 |
| native, calibrated under present | 8.64 | 2.0 | 2.72 |
| native, calibrated under tagger50 | 7.05 | 0.0 | 3.43 |
| native, recalibrated at a 1,690-name lexicon | 16.19 | 100.0 | 1.57 |
| native, recalibrated at a 3,380-name lexicon | 17.73 | 100.0 | 1.46 |
| native, recalibrated at a 6,760-name lexicon | 18.79 | 100.0 | 1.39 |
| native, recalibrated at a 17,001-name lexicon | 19.42 | 100.0 | 1.35 |

## alpha = 0.1, policy rand200

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 9.90 | 45.0 | 3.71 |
| native, frozen at 150 | 7.95 | 0.0 | 3.95 |
| native, recalibrated at 845 | 11.40 | 96.2 | 2.58 |
| native, matched to the policy | 9.91 | 42.4 | 3.03 |
| native, worst case over the policies | 6.23 | 0.0 | 5.43 |
| native, calibrated under rand50 | 8.68 | 1.4 | 3.57 |
| native, calibrated under rand500 | 11.13 | 93.6 | 2.65 |
| native, calibrated under present | 7.62 | 0.0 | 4.16 |
| native, calibrated under tagger50 | 6.27 | 0.0 | 5.37 |
| native, recalibrated at a 1,690-name lexicon | 13.36 | 100.0 | 2.18 |
| native, recalibrated at a 3,380-name lexicon | 14.50 | 100.0 | 2.01 |
| native, recalibrated at a 6,760-name lexicon | 15.35 | 100.0 | 1.90 |
| native, recalibrated at a 17,001-name lexicon | 15.87 | 100.0 | 1.84 |

## alpha = 0.1, policy rand500

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 9.90 | 45.0 | 5.10 |
| native, frozen at 150 | 7.30 | 0.0 | 6.81 |
| native, recalibrated at 845 | 10.13 | 58.6 | 4.20 |
| native, matched to the policy | 9.90 | 45.2 | 4.33 |
| native, worst case over the policies | 5.84 | 0.0 | 9.76 |
| native, calibrated under rand50 | 7.86 | 0.0 | 6.06 |
| native, calibrated under rand200 | 8.89 | 4.0 | 5.04 |
| native, calibrated under present | 7.05 | 0.0 | 7.20 |
| native, calibrated under tagger50 | 5.88 | 0.0 | 9.65 |
| native, recalibrated at a 1,690-name lexicon | 11.75 | 98.8 | 3.46 |
| native, recalibrated at a 3,380-name lexicon | 12.71 | 100.0 | 3.15 |
| native, recalibrated at a 6,760-name lexicon | 13.41 | 100.0 | 2.95 |
| native, recalibrated at a 17,001-name lexicon | 13.84 | 100.0 | 2.85 |

## alpha = 0.1, policy present

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 9.90 | 45.0 | 2.87 |
| native, frozen at 150 | 10.36 | 70.4 | 2.26 |
| native, recalibrated at 845 | 15.49 | 100.0 | 1.61 |
| native, matched to the policy | 9.91 | 43.8 | 2.35 |
| native, worst case over the policies | 7.92 | 0.0 | 2.94 |
| native, calibrated under rand50 | 11.40 | 97.0 | 2.08 |
| native, calibrated under rand200 | 13.29 | 100.0 | 1.83 |
| native, calibrated under rand500 | 15.08 | 100.0 | 1.65 |
| native, calibrated under tagger50 | 7.98 | 0.0 | 2.91 |
| native, recalibrated at a 1,690-name lexicon | 18.31 | 100.0 | 1.41 |
| native, recalibrated at a 3,380-name lexicon | 19.87 | 100.0 | 1.32 |
| native, recalibrated at a 6,760-name lexicon | 21.02 | 100.0 | 1.26 |
| native, recalibrated at a 17,001-name lexicon | 21.74 | 100.0 | 1.23 |

## alpha = 0.1, policy tagger50

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 9.90 | 45.0 | 5.86 |
| native, frozen at 150 | 12.68 | 100.0 | 3.36 |
| native, recalibrated at 845 | 18.50 | 100.0 | 2.08 |
| native, matched to the policy | 9.92 | 44.2 | 4.78 |
| native, worst case over the policies | 9.84 | 39.8 | 4.83 |
| native, calibrated under rand50 | 13.86 | 100.0 | 2.99 |
| native, calibrated under rand200 | 16.05 | 100.0 | 2.49 |
| native, calibrated under rand500 | 18.07 | 100.0 | 2.15 |
| native, calibrated under present | 12.15 | 99.6 | 3.55 |
| native, recalibrated at a 1,690-name lexicon | 21.45 | 100.0 | 1.72 |
| native, recalibrated at a 3,380-name lexicon | 23.10 | 100.0 | 1.57 |
| native, recalibrated at a 6,760-name lexicon | 24.26 | 100.0 | 1.48 |
| native, recalibrated at a 17,001-name lexicon | 24.96 | 100.0 | 1.42 |

## alpha = 0.1, policy adversarial

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 9.90 | 45.0 | 5.87 |
| native, frozen at 150 | 12.84 | 100.0 | 3.36 |
| native, recalibrated at 845 | 18.82 | 100.0 | 2.02 |
| native, worst case over the policies | 9.92 | 46.0 | 5.00 |
| native, calibrated under rand50 | 14.08 | 100.0 | 2.96 |
| native, calibrated under rand200 | 16.29 | 100.0 | 2.44 |
| native, calibrated under rand500 | 18.37 | 100.0 | 2.09 |
| native, calibrated under present | 12.30 | 99.8 | 3.56 |
| native, calibrated under tagger50 | 10.00 | 48.8 | 4.93 |
| native, recalibrated at a 1,690-name lexicon | 21.84 | 100.0 | 1.68 |
| native, recalibrated at a 3,380-name lexicon | 23.49 | 100.0 | 1.53 |
| native, recalibrated at a 6,760-name lexicon | 24.67 | 100.0 | 1.43 |
| native, recalibrated at a 17,001-name lexicon | 25.41 | 100.0 | 1.38 |

## alpha = 0.05, policy rand50

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 4.92 | 41.8 | 6.01 |
| native, frozen at 150 | 4.56 | 16.2 | 5.83 |
| native, recalibrated at 845 | 6.03 | 96.2 | 4.13 |
| native, matched to the policy | 4.92 | 44.2 | 5.28 |
| native, worst case over the policies | 3.55 | 0.0 | 8.28 |
| native, calibrated under rand200 | 5.43 | 77.0 | 4.69 |
| native, calibrated under rand500 | 5.85 | 91.8 | 4.29 |
| native, calibrated under present | 4.39 | 9.8 | 6.15 |
| native, calibrated under tagger50 | 3.55 | 0.0 | 8.25 |
| native, recalibrated at a 1,690-name lexicon | 7.08 | 100.0 | 3.42 |
| native, recalibrated at a 3,380-name lexicon | 7.74 | 100.0 | 3.09 |
| native, recalibrated at a 6,760-name lexicon | 8.13 | 100.0 | 2.92 |
| native, recalibrated at a 17,001-name lexicon | 8.38 | 100.0 | 2.82 |

## alpha = 0.05, policy rand200

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 4.92 | 41.8 | 8.24 |
| native, frozen at 150 | 4.20 | 4.8 | 9.75 |
| native, recalibrated at 845 | 5.43 | 76.2 | 6.63 |
| native, matched to the policy | 4.91 | 42.2 | 7.64 |
| native, worst case over the policies | 3.28 | 0.0 | 14.31 |
| native, calibrated under rand50 | 4.50 | 12.6 | 8.72 |
| native, calibrated under rand500 | 5.27 | 68.8 | 6.91 |
| native, calibrated under present | 4.04 | 1.8 | 10.34 |
| native, calibrated under tagger50 | 3.29 | 0.0 | 14.26 |
| native, recalibrated at a 1,690-name lexicon | 6.30 | 98.4 | 5.36 |
| native, recalibrated at a 3,380-name lexicon | 6.85 | 99.8 | 4.78 |
| native, recalibrated at a 6,760-name lexicon | 7.18 | 100.0 | 4.49 |
| native, recalibrated at a 17,001-name lexicon | 7.40 | 100.0 | 4.33 |

## alpha = 0.05, policy rand500

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 4.92 | 41.8 | 12.63 |
| native, frozen at 150 | 3.92 | 0.8 | 18.59 |
| native, recalibrated at 845 | 5.07 | 52.0 | 12.22 |
| native, matched to the policy | 4.92 | 42.4 | 12.79 |
| native, worst case over the policies | 3.06 | 0.0 | 27.84 |
| native, calibrated under rand50 | 4.21 | 5.4 | 16.49 |
| native, calibrated under rand200 | 4.59 | 19.0 | 14.29 |
| native, calibrated under present | 3.77 | 0.6 | 19.80 |
| native, calibrated under tagger50 | 3.06 | 0.0 | 27.74 |
| native, recalibrated at a 1,690-name lexicon | 5.90 | 93.0 | 9.62 |
| native, recalibrated at a 3,380-name lexicon | 6.40 | 98.4 | 8.45 |
| native, recalibrated at a 6,760-name lexicon | 6.68 | 99.4 | 7.88 |
| native, recalibrated at a 17,001-name lexicon | 6.86 | 99.8 | 7.55 |

## alpha = 0.05, policy present

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 4.92 | 41.8 | 5.50 |
| native, frozen at 150 | 5.14 | 60.2 | 4.78 |
| native, recalibrated at 845 | 6.83 | 99.8 | 3.47 |
| native, matched to the policy | 4.93 | 44.6 | 5.03 |
| native, worst case over the policies | 3.97 | 1.2 | 6.63 |
| native, calibrated under rand50 | 5.58 | 83.2 | 4.36 |
| native, calibrated under rand200 | 6.16 | 97.6 | 3.90 |
| native, calibrated under rand500 | 6.63 | 99.6 | 3.59 |
| native, calibrated under tagger50 | 3.98 | 1.6 | 6.61 |
| native, recalibrated at a 1,690-name lexicon | 8.03 | 100.0 | 2.91 |
| native, recalibrated at a 3,380-name lexicon | 8.82 | 100.0 | 2.64 |
| native, recalibrated at a 6,760-name lexicon | 9.30 | 100.0 | 2.51 |
| native, recalibrated at a 17,001-name lexicon | 9.60 | 100.0 | 2.43 |

## alpha = 0.05, policy tagger50

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 4.92 | 41.8 | 13.09 |
| native, frozen at 150 | 6.42 | 99.4 | 9.12 |
| native, recalibrated at 845 | 8.50 | 100.0 | 6.05 |
| native, matched to the policy | 4.93 | 43.8 | 13.26 |
| native, worst case over the policies | 4.92 | 43.8 | 13.30 |
| native, calibrated under rand50 | 6.98 | 100.0 | 8.13 |
| native, calibrated under rand200 | 7.68 | 100.0 | 7.07 |
| native, calibrated under rand500 | 8.25 | 100.0 | 6.34 |
| native, calibrated under present | 6.15 | 97.2 | 9.69 |
| native, recalibrated at a 1,690-name lexicon | 9.97 | 100.0 | 4.76 |
| native, recalibrated at a 3,380-name lexicon | 10.89 | 100.0 | 4.18 |
| native, recalibrated at a 6,760-name lexicon | 11.44 | 100.0 | 3.89 |
| native, recalibrated at a 17,001-name lexicon | 11.80 | 100.0 | 3.73 |

## alpha = 0.05, policy adversarial

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 4.92 | 41.8 | 13.53 |
| native, frozen at 150 | 6.45 | 99.4 | 10.39 |
| native, recalibrated at 845 | 8.55 | 100.0 | 6.45 |
| native, worst case over the policies | 4.93 | 44.4 | 16.51 |
| native, calibrated under rand50 | 7.01 | 100.0 | 9.04 |
| native, calibrated under rand200 | 7.72 | 100.0 | 7.69 |
| native, calibrated under rand500 | 8.29 | 100.0 | 6.80 |
| native, calibrated under present | 6.17 | 97.2 | 11.18 |
| native, calibrated under tagger50 | 4.94 | 46.0 | 16.45 |
| native, recalibrated at a 1,690-name lexicon | 10.05 | 100.0 | 4.92 |
| native, recalibrated at a 3,380-name lexicon | 11.00 | 100.0 | 4.24 |
| native, recalibrated at a 6,760-name lexicon | 11.57 | 100.0 | 3.93 |
| native, recalibrated at a 17,001-name lexicon | 11.93 | 100.0 | 3.75 |
