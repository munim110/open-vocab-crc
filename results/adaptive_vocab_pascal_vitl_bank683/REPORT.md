# Calibrate once, deploy under per-image vocabularies

CAT-Seg (vitl_bank683), 2000 Pascal Context validation images (0 without a source-labelled sampled pixel excluded), 500 random half/half splits, image-level CRC on the source-label miss rate. Deployed vocabulary = 59 source names + per-image added names A(x): rand50 (50.0 on average), rand100 (100.0 on average), rand300 (300.0 on average), present (1.1 on average), tagger50 (50.0 on average). Risk in %, "above" = % of splits above alpha, size = deployed labels per source-labelled pixel. Development data; nothing fitted.

## alpha = 0.1, policy rand50

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 9.82 | 40.8 | 1.62 |
| native, frozen at 59 | 10.87 | 86.8 | 1.38 |
| native, recalibrated at 458 | 6.41 | 0.0 | 1.79 |
| native, matched to the policy | 9.83 | 40.6 | 1.45 |
| native, worst case over the policies | 6.24 | 0.0 | 1.82 |
| native, calibrated under rand100 | 9.17 | 12.0 | 1.51 |
| native, calibrated under rand300 | 7.14 | 0.0 | 1.70 |
| native, calibrated under present | 10.64 | 80.6 | 1.40 |
| native, calibrated under tagger50 | 6.26 | 0.0 | 1.81 |

## alpha = 0.1, policy rand100

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 9.82 | 40.8 | 1.72 |
| native, frozen at 59 | 11.48 | 97.0 | 1.41 |
| native, recalibrated at 458 | 6.95 | 0.0 | 1.85 |
| native, matched to the policy | 9.82 | 40.2 | 1.54 |
| native, worst case over the policies | 6.78 | 0.0 | 1.87 |
| native, calibrated under rand50 | 10.47 | 75.4 | 1.48 |
| native, calibrated under rand300 | 7.71 | 0.0 | 1.75 |
| native, calibrated under present | 11.26 | 95.8 | 1.42 |
| native, calibrated under tagger50 | 6.79 | 0.0 | 1.87 |

## alpha = 0.1, policy rand300

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 9.82 | 40.8 | 2.13 |
| native, frozen at 59 | 14.00 | 100.0 | 1.47 |
| native, recalibrated at 458 | 8.94 | 6.0 | 2.02 |
| native, matched to the policy | 9.81 | 41.8 | 1.89 |
| native, worst case over the policies | 8.73 | 3.6 | 2.05 |
| native, calibrated under rand50 | 12.86 | 100.0 | 1.56 |
| native, calibrated under rand100 | 12.12 | 99.4 | 1.63 |
| native, calibrated under present | 13.75 | 100.0 | 1.49 |
| native, calibrated under tagger50 | 8.75 | 4.0 | 2.04 |

## alpha = 0.1, policy present

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 9.82 | 40.8 | 1.55 |
| native, frozen at 59 | 10.05 | 53.8 | 1.37 |
| native, recalibrated at 458 | 5.96 | 0.0 | 1.75 |
| native, matched to the policy | 9.84 | 41.8 | 1.39 |
| native, worst case over the policies | 5.81 | 0.0 | 1.77 |
| native, calibrated under rand50 | 9.08 | 8.8 | 1.44 |
| native, calibrated under rand100 | 8.47 | 1.4 | 1.49 |
| native, calibrated under rand300 | 6.61 | 0.0 | 1.67 |
| native, calibrated under tagger50 | 5.82 | 0.0 | 1.77 |

## alpha = 0.1, policy tagger50

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 9.82 | 40.8 | 2.33 |
| native, frozen at 59 | 15.20 | 100.0 | 1.46 |
| native, recalibrated at 458 | 10.00 | 51.0 | 2.02 |
| native, matched to the policy | 9.82 | 41.2 | 2.05 |
| native, worst case over the policies | 9.80 | 41.2 | 2.06 |
| native, calibrated under rand50 | 14.06 | 100.0 | 1.56 |
| native, calibrated under rand100 | 13.30 | 100.0 | 1.62 |
| native, calibrated under rand300 | 10.91 | 86.6 | 1.89 |
| native, calibrated under present | 14.96 | 100.0 | 1.48 |

## alpha = 0.1, policy adversarial

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 9.82 | 40.8 | 2.33 |
| native, frozen at 59 | 15.24 | 100.0 | 1.46 |
| native, recalibrated at 458 | 10.03 | 51.4 | 2.03 |
| native, worst case over the policies | 9.82 | 42.6 | 2.06 |
| native, calibrated under rand50 | 14.10 | 100.0 | 1.56 |
| native, calibrated under rand100 | 13.34 | 100.0 | 1.63 |
| native, calibrated under rand300 | 10.94 | 87.2 | 1.90 |
| native, calibrated under present | 15.00 | 100.0 | 1.48 |
| native, calibrated under tagger50 | 9.84 | 42.8 | 2.06 |

## alpha = 0.05, policy rand50

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 4.86 | 40.8 | 2.21 |
| native, frozen at 59 | 5.35 | 74.6 | 1.95 |
| native, recalibrated at 458 | 2.85 | 0.0 | 2.66 |
| native, matched to the policy | 4.86 | 41.4 | 2.05 |
| native, worst case over the policies | 2.71 | 0.0 | 2.73 |
| native, calibrated under rand100 | 4.39 | 10.0 | 2.16 |
| native, calibrated under rand300 | 3.21 | 0.0 | 2.50 |
| native, calibrated under present | 5.22 | 65.4 | 1.98 |
| native, calibrated under tagger50 | 2.72 | 0.0 | 2.72 |

## alpha = 0.05, policy rand100

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 4.86 | 40.8 | 2.42 |
| native, frozen at 59 | 5.85 | 93.2 | 2.02 |
| native, recalibrated at 458 | 3.24 | 0.0 | 2.81 |
| native, matched to the policy | 4.84 | 38.8 | 2.24 |
| native, worst case over the policies | 3.10 | 0.0 | 2.89 |
| native, calibrated under rand50 | 5.34 | 73.4 | 2.13 |
| native, calibrated under rand300 | 3.62 | 0.0 | 2.63 |
| native, calibrated under present | 5.72 | 89.0 | 2.05 |
| native, calibrated under tagger50 | 3.11 | 0.0 | 2.88 |

## alpha = 0.05, policy rand300

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 4.86 | 40.8 | 3.26 |
| native, frozen at 59 | 7.65 | 100.0 | 2.24 |
| native, recalibrated at 458 | 4.36 | 7.4 | 3.25 |
| native, matched to the policy | 4.86 | 40.8 | 3.02 |
| native, worst case over the policies | 4.16 | 4.0 | 3.36 |
| native, calibrated under rand50 | 7.03 | 100.0 | 2.37 |
| native, calibrated under rand100 | 6.40 | 98.4 | 2.52 |
| native, calibrated under present | 7.49 | 100.0 | 2.27 |
| native, calibrated under tagger50 | 4.18 | 4.2 | 3.35 |

## alpha = 0.05, policy present

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 4.86 | 40.8 | 2.05 |
| native, frozen at 59 | 4.98 | 47.4 | 1.89 |
| native, recalibrated at 458 | 2.58 | 0.0 | 2.52 |
| native, matched to the policy | 4.86 | 40.4 | 1.92 |
| native, worst case over the policies | 2.45 | 0.0 | 2.58 |
| native, calibrated under rand50 | 4.51 | 15.8 | 1.98 |
| native, calibrated under rand100 | 4.06 | 3.2 | 2.07 |
| native, calibrated under rand300 | 2.93 | 0.0 | 2.38 |
| native, calibrated under tagger50 | 2.46 | 0.0 | 2.58 |

## alpha = 0.05, policy tagger50

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 4.86 | 40.8 | 3.63 |
| native, frozen at 59 | 8.71 | 100.0 | 2.25 |
| native, recalibrated at 458 | 5.08 | 56.2 | 3.29 |
| native, matched to the policy | 4.86 | 41.8 | 3.40 |
| native, worst case over the policies | 4.85 | 40.4 | 3.40 |
| native, calibrated under rand50 | 8.04 | 100.0 | 2.39 |
| native, calibrated under rand100 | 7.35 | 100.0 | 2.54 |
| native, calibrated under rand300 | 5.64 | 87.4 | 3.06 |
| native, calibrated under present | 8.54 | 100.0 | 2.28 |

## alpha = 0.05, policy adversarial

| Arm | Risk (%) | Above (%) | Size |
|---|---:|---:|---:|
| anchored, calibrated once | 4.86 | 40.8 | 3.63 |
| native, frozen at 59 | 8.72 | 100.0 | 2.26 |
| native, recalibrated at 458 | 5.09 | 56.6 | 3.32 |
| native, worst case over the policies | 4.86 | 40.4 | 3.43 |
| native, calibrated under rand50 | 8.05 | 100.0 | 2.40 |
| native, calibrated under rand100 | 7.36 | 100.0 | 2.56 |
| native, calibrated under rand300 | 5.66 | 87.4 | 3.08 |
| native, calibrated under present | 8.55 | 100.0 | 2.29 |
| native, calibrated under tagger50 | 4.88 | 41.8 | 3.42 |
