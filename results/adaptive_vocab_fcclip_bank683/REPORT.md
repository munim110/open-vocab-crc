# Calibrate once, deploy under per-image vocabularies

FC-CLIP (fcclip_bank683), 2000 ADE validation images (0 without a source-labelled sampled pixel excluded), 500 random half/half splits, image-level CRC on the source-label miss rate. Deployed vocabulary = 150 source names + per-image added names A(x): rand50 (50.0 on average), rand200 (200.0 on average), rand500 (500.0 on average), present (1.6 on average), tagger50 (50.0 on average). Risk in %, "above" = % of splits above alpha, size = deployed labels per source-labelled pixel. Development data; nothing fitted.

## alpha = 0.1, policy rand50

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 9.88 | 43.0 | 4.32 |
| native, frozen at 150 | 10.30 | 69.0 | 3.43 |
| native, recalibrated at 845 | 7.33 | 0.0 | 5.07 |
| native, matched to the policy | 9.87 | 38.8 | 3.60 |
| native, worst case over the policies | 7.04 | 0.0 | 5.31 |
| native, calibrated under rand200 | 8.79 | 2.4 | 4.12 |
| native, calibrated under rand500 | 7.75 | 0.0 | 4.76 |
| native, calibrated under present | 9.69 | 30.4 | 3.67 |
| native, calibrated under tagger50 | 7.09 | 0.0 | 5.27 |
| native, recalibrated at a 1,690-name lexicon | 6.44 | 0.0 | 5.94 |
| native, recalibrated at a 3,380-name lexicon | 5.64 | 0.0 | 7.13 |
| native, recalibrated at a 6,760-name lexicon | 4.96 | 0.0 | 8.66 |
| native, recalibrated at a 17,001-name lexicon | 4.05 | 0.0 | 11.87 |

## alpha = 0.1, policy rand200

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 9.88 | 43.0 | 5.92 |
| native, frozen at 150 | 11.64 | 98.6 | 3.92 |
| native, recalibrated at 845 | 8.23 | 0.0 | 5.95 |
| native, matched to the policy | 9.88 | 41.8 | 4.77 |
| native, worst case over the policies | 7.94 | 0.0 | 6.26 |
| native, calibrated under rand50 | 11.18 | 95.4 | 4.12 |
| native, calibrated under rand500 | 8.69 | 2.8 | 5.55 |
| native, calibrated under present | 10.98 | 90.8 | 4.21 |
| native, calibrated under tagger50 | 7.99 | 0.0 | 6.20 |
| native, recalibrated at a 1,690-name lexicon | 7.31 | 0.0 | 7.06 |
| native, recalibrated at a 3,380-name lexicon | 6.41 | 0.0 | 8.54 |
| native, recalibrated at a 6,760-name lexicon | 5.62 | 0.0 | 10.52 |
| native, recalibrated at a 17,001-name lexicon | 4.58 | 0.0 | 14.70 |

## alpha = 0.1, policy rand500

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 9.88 | 43.0 | 9.05 |
| native, frozen at 150 | 13.00 | 100.0 | 4.74 |
| native, recalibrated at 845 | 9.41 | 19.4 | 7.40 |
| native, matched to the policy | 9.90 | 43.2 | 6.88 |
| native, worst case over the policies | 9.08 | 8.6 | 7.80 |
| native, calibrated under rand50 | 12.52 | 100.0 | 4.99 |
| native, calibrated under rand200 | 11.09 | 94.2 | 5.84 |
| native, calibrated under present | 12.30 | 100.0 | 5.12 |
| native, calibrated under tagger50 | 9.13 | 9.2 | 7.73 |
| native, recalibrated at a 1,690-name lexicon | 8.30 | 0.0 | 8.86 |
| native, recalibrated at a 3,380-name lexicon | 7.21 | 0.0 | 10.85 |
| native, recalibrated at a 6,760-name lexicon | 6.28 | 0.0 | 13.53 |
| native, recalibrated at a 17,001-name lexicon | 5.09 | 0.0 | 19.32 |

## alpha = 0.1, policy present

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 9.88 | 43.0 | 4.03 |
| native, frozen at 150 | 10.46 | 77.8 | 3.24 |
| native, recalibrated at 845 | 7.56 | 0.0 | 4.68 |
| native, matched to the policy | 9.89 | 43.8 | 3.45 |
| native, worst case over the policies | 7.30 | 0.0 | 4.89 |
| native, calibrated under rand50 | 10.06 | 51.2 | 3.38 |
| native, calibrated under rand200 | 9.01 | 5.6 | 3.85 |
| native, calibrated under rand500 | 7.96 | 0.0 | 4.41 |
| native, calibrated under tagger50 | 7.34 | 0.0 | 4.85 |
| native, recalibrated at a 1,690-name lexicon | 6.73 | 0.0 | 5.43 |
| native, recalibrated at a 3,380-name lexicon | 5.94 | 0.0 | 6.43 |
| native, recalibrated at a 6,760-name lexicon | 5.21 | 0.0 | 7.73 |
| native, recalibrated at a 17,001-name lexicon | 4.31 | 0.0 | 10.40 |

## alpha = 0.1, policy tagger50

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 9.88 | 43.0 | 9.21 |
| native, frozen at 150 | 14.03 | 100.0 | 4.87 |
| native, recalibrated at 845 | 10.20 | 61.6 | 7.36 |
| native, matched to the policy | 9.90 | 40.2 | 7.65 |
| native, worst case over the policies | 9.83 | 38.2 | 7.70 |
| native, calibrated under rand50 | 13.52 | 100.0 | 5.12 |
| native, calibrated under rand200 | 12.05 | 100.0 | 5.94 |
| native, calibrated under rand500 | 10.74 | 85.6 | 6.90 |
| native, calibrated under present | 13.30 | 100.0 | 5.24 |
| native, recalibrated at a 1,690-name lexicon | 9.03 | 4.6 | 8.60 |
| native, recalibrated at a 3,380-name lexicon | 7.85 | 0.0 | 10.19 |
| native, recalibrated at a 6,760-name lexicon | 6.81 | 0.0 | 12.12 |
| native, recalibrated at a 17,001-name lexicon | 5.58 | 0.0 | 15.86 |

## alpha = 0.1, policy adversarial

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 9.88 | 43.0 | 9.71 |
| native, frozen at 150 | 14.12 | 100.0 | 4.83 |
| native, recalibrated at 845 | 10.27 | 66.6 | 7.37 |
| native, worst case over the policies | 9.90 | 40.6 | 7.74 |
| native, calibrated under rand50 | 13.61 | 100.0 | 5.08 |
| native, calibrated under rand200 | 12.15 | 100.0 | 5.91 |
| native, calibrated under rand500 | 10.82 | 87.4 | 6.89 |
| native, calibrated under present | 13.39 | 100.0 | 5.20 |
| native, calibrated under tagger50 | 9.96 | 47.0 | 7.68 |
| native, recalibrated at a 1,690-name lexicon | 9.08 | 5.6 | 8.71 |
| native, recalibrated at a 3,380-name lexicon | 7.91 | 0.0 | 10.43 |
| native, recalibrated at a 6,760-name lexicon | 6.86 | 0.0 | 12.66 |
| native, recalibrated at a 17,001-name lexicon | 5.61 | 0.0 | 17.35 |

## alpha = 0.05, policy rand50

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 4.91 | 44.0 | 10.30 |
| native, frozen at 150 | 5.09 | 58.4 | 8.35 |
| native, recalibrated at 845 | 3.68 | 0.2 | 13.67 |
| native, matched to the policy | 4.89 | 39.4 | 8.87 |
| native, worst case over the policies | 3.48 | 0.0 | 14.76 |
| native, calibrated under rand200 | 4.32 | 6.2 | 10.79 |
| native, calibrated under rand500 | 3.88 | 1.0 | 12.67 |
| native, calibrated under present | 4.63 | 24.0 | 9.68 |
| native, calibrated under tagger50 | 3.51 | 0.0 | 14.60 |
| native, recalibrated at a 1,690-name lexicon | 3.30 | 0.0 | 15.82 |
| native, recalibrated at a 3,380-name lexicon | 2.94 | 0.0 | 18.48 |
| native, recalibrated at a 6,760-name lexicon | 2.54 | 0.0 | 22.10 |
| native, recalibrated at a 17,001-name lexicon | 2.03 | 0.0 | 28.89 |

## alpha = 0.05, policy rand200

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 4.91 | 44.0 | 15.10 |
| native, frozen at 150 | 5.76 | 90.6 | 10.12 |
| native, recalibrated at 845 | 4.15 | 5.2 | 17.11 |
| native, matched to the policy | 4.90 | 42.0 | 13.28 |
| native, worst case over the policies | 3.94 | 1.4 | 18.58 |
| native, calibrated under rand50 | 5.55 | 85.6 | 10.79 |
| native, calibrated under rand500 | 4.38 | 12.0 | 15.77 |
| native, calibrated under present | 5.27 | 68.0 | 11.83 |
| native, calibrated under tagger50 | 3.97 | 1.6 | 18.36 |
| native, recalibrated at a 1,690-name lexicon | 3.76 | 0.4 | 20.00 |
| native, recalibrated at a 3,380-name lexicon | 3.37 | 0.0 | 23.62 |
| native, recalibrated at a 6,760-name lexicon | 2.97 | 0.0 | 28.63 |
| native, recalibrated at a 17,001-name lexicon | 2.39 | 0.0 | 38.31 |

## alpha = 0.05, policy rand500

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 4.91 | 44.0 | 24.70 |
| native, frozen at 150 | 6.45 | 99.0 | 12.99 |
| native, recalibrated at 845 | 4.67 | 26.2 | 22.66 |
| native, matched to the policy | 4.91 | 44.2 | 20.80 |
| native, worst case over the policies | 4.44 | 13.8 | 24.73 |
| native, calibrated under rand50 | 6.18 | 96.8 | 13.90 |
| native, calibrated under rand200 | 5.41 | 78.2 | 17.34 |
| native, calibrated under present | 5.83 | 88.6 | 15.33 |
| native, calibrated under tagger50 | 4.47 | 15.0 | 24.42 |
| native, recalibrated at a 1,690-name lexicon | 4.24 | 6.6 | 26.75 |
| native, recalibrated at a 3,380-name lexicon | 3.82 | 0.6 | 31.93 |
| native, recalibrated at a 6,760-name lexicon | 3.37 | 0.0 | 39.19 |
| native, recalibrated at a 17,001-name lexicon | 2.72 | 0.0 | 53.47 |

## alpha = 0.05, policy present

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 4.91 | 44.0 | 9.10 |
| native, frozen at 150 | 5.35 | 74.2 | 7.47 |
| native, recalibrated at 845 | 3.91 | 0.8 | 11.87 |
| native, matched to the policy | 4.90 | 44.4 | 8.58 |
| native, worst case over the policies | 3.68 | 0.4 | 12.77 |
| native, calibrated under rand50 | 5.15 | 62.8 | 7.91 |
| native, calibrated under rand200 | 4.59 | 19.4 | 9.51 |
| native, calibrated under rand500 | 4.13 | 4.8 | 11.06 |
| native, calibrated under tagger50 | 3.71 | 0.4 | 12.64 |
| native, recalibrated at a 1,690-name lexicon | 3.48 | 0.0 | 13.63 |
| native, recalibrated at a 3,380-name lexicon | 3.09 | 0.0 | 15.81 |
| native, recalibrated at a 6,760-name lexicon | 2.70 | 0.0 | 18.76 |
| native, recalibrated at a 17,001-name lexicon | 2.12 | 0.0 | 24.27 |

## alpha = 0.05, policy tagger50

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 4.91 | 44.0 | 19.56 |
| native, frozen at 150 | 7.00 | 100.0 | 11.74 |
| native, recalibrated at 845 | 5.11 | 59.8 | 17.84 |
| native, matched to the policy | 4.90 | 41.2 | 18.84 |
| native, worst case over the policies | 4.87 | 41.0 | 19.02 |
| native, calibrated under rand50 | 6.73 | 99.6 | 12.37 |
| native, calibrated under rand200 | 5.94 | 95.2 | 14.62 |
| native, calibrated under rand500 | 5.36 | 73.2 | 16.75 |
| native, calibrated under present | 6.37 | 99.0 | 13.32 |
| native, recalibrated at a 1,690-name lexicon | 4.64 | 23.2 | 20.13 |
| native, recalibrated at a 3,380-name lexicon | 4.17 | 3.8 | 22.87 |
| native, recalibrated at a 6,760-name lexicon | 3.70 | 0.2 | 26.49 |
| native, recalibrated at a 17,001-name lexicon | 3.00 | 0.0 | 33.14 |

## alpha = 0.05, policy adversarial

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 4.91 | 44.0 | 25.08 |
| native, frozen at 150 | 7.05 | 100.0 | 12.21 |
| native, recalibrated at 845 | 5.15 | 62.2 | 20.09 |
| native, worst case over the policies | 4.90 | 41.4 | 21.79 |
| native, calibrated under rand50 | 6.77 | 99.8 | 12.95 |
| native, calibrated under rand200 | 5.98 | 95.6 | 15.74 |
| native, calibrated under rand500 | 5.40 | 75.0 | 18.56 |
| native, calibrated under present | 6.42 | 99.2 | 14.11 |
| native, calibrated under tagger50 | 4.94 | 45.6 | 21.53 |
| native, recalibrated at a 1,690-name lexicon | 4.68 | 25.2 | 23.47 |
| native, recalibrated at a 3,380-name lexicon | 4.21 | 5.2 | 27.81 |
| native, recalibrated at a 6,760-name lexicon | 3.73 | 0.4 | 33.84 |
| native, recalibrated at a 17,001-name lexicon | 3.02 | 0.0 | 46.12 |
