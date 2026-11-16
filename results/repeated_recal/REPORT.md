# Repeated recalibration: set size of a simultaneous calibration-conditional guarantee

Half of the images calibrate, half evaluate, 500 random splits (the splits of exp_headroom_splits.py), alpha = 0.1, delta = 0.1. Native: recalibrated at the grown vocabulary, at level delta/K so that K recalibrations hold at once (union bound). Anchored: calibrated once at the source labels, level delta for every vocabulary. RCPS with the Hoeffding-Bentkus bound. Sizes are labels per pixel at the grown vocabulary; risk is the mean evaluation risk; "fail" is the share of splits with evaluation risk above alpha.

## CAT-Seg ViT-L, ade (2000 images)

CRC (marginal, one vocabulary): native recal. 3.47, anchored 4.27. Anchored RCPS at delta: size 5.11, risk 8.19%, fail 0.2%. Smallest K with native size >= anchored: 50.

| K | native size | risk (%) | fail (%) |
|---:|---:|---:|---:|
| 1 | 4.32 | 8.19 | 0.2 |
| 2 | 4.44 | 7.99 | 0.2 |
| 5 | 4.65 | 7.69 | 0.0 |
| 10 | 4.87 | 7.39 | 0.0 |
| 20 | 5.03 | 7.20 | 0.0 |
| 50 | 5.19 | 7.00 | 0.0 |
| 100 | 5.37 | 6.80 | 0.0 |
| 1,000 | 5.86 | 6.30 | 0.0 |
| 10,000 | 6.31 | 5.90 | 0.0 |
| 1,000,000 | 7.30 | 5.20 | 0.0 |

## SED, ade (2000 images)

CRC (marginal, one vocabulary): native recal. 5.28, anchored 6.05. Anchored RCPS at delta: size 7.55, risk 8.17%, fail 0.4%. Smallest K with native size >= anchored: 5.

| K | native size | risk (%) | fail (%) |
|---:|---:|---:|---:|
| 1 | 7.02 | 8.18 | 0.4 |
| 2 | 7.30 | 7.98 | 0.2 |
| 5 | 7.77 | 7.68 | 0.0 |
| 10 | 8.29 | 7.38 | 0.0 |
| 20 | 8.67 | 7.18 | 0.0 |
| 50 | 9.09 | 6.98 | 0.0 |
| 100 | 9.53 | 6.78 | 0.0 |
| 1,000 | 10.82 | 6.28 | 0.0 |
| 10,000 | 12.04 | 5.88 | 0.0 |
| 1,000,000 | 14.73 | 5.18 | 0.0 |

## FC-CLIP, ade (2000 images)

CRC (marginal, one vocabulary): native recal. 8.18, anchored 11.18. Anchored RCPS at delta: size 14.72, risk 8.15%, fail 0.0%. Smallest K with native size >= anchored: 1000.

| K | native size | risk (%) | fail (%) |
|---:|---:|---:|---:|
| 1 | 10.80 | 8.17 | 0.2 |
| 2 | 11.20 | 7.97 | 0.0 |
| 5 | 11.86 | 7.67 | 0.0 |
| 10 | 12.61 | 7.37 | 0.0 |
| 20 | 13.16 | 7.17 | 0.0 |
| 50 | 13.77 | 6.97 | 0.0 |
| 100 | 14.45 | 6.77 | 0.0 |
| 1,000 | 16.44 | 6.28 | 0.0 |
| 10,000 | 18.42 | 5.88 | 0.0 |
| 1,000,000 | 23.06 | 5.18 | 0.0 |

## CAT-Seg ViT-L, pascal (2000 images)

CRC (marginal, one vocabulary): native recal. 2.07, anchored 2.34. Anchored RCPS at delta: size 2.64, risk 8.13%, fail 0.4%. Smallest K with native size >= anchored: 50.

| K | native size | risk (%) | fail (%) |
|---:|---:|---:|---:|
| 1 | 2.38 | 8.15 | 0.2 |
| 2 | 2.42 | 7.95 | 0.2 |
| 5 | 2.49 | 7.65 | 0.0 |
| 10 | 2.55 | 7.35 | 0.0 |
| 20 | 2.60 | 7.15 | 0.0 |
| 50 | 2.65 | 6.96 | 0.0 |
| 100 | 2.70 | 6.76 | 0.0 |
| 1,000 | 2.85 | 6.26 | 0.0 |
| 10,000 | 2.98 | 5.87 | 0.0 |
| 1,000,000 | 3.24 | 5.18 | 0.0 |

## SED, pascal (2000 images)

CRC (marginal, one vocabulary): native recal. 2.68, anchored 2.80. Anchored RCPS at delta: size 3.26, risk 8.14%, fail 0.0%. Smallest K with native size >= anchored: 5.

| K | native size | risk (%) | fail (%) |
|---:|---:|---:|---:|
| 1 | 3.14 | 8.13 | 0.6 |
| 2 | 3.20 | 7.94 | 0.0 |
| 5 | 3.30 | 7.64 | 0.0 |
| 10 | 3.40 | 7.34 | 0.0 |
| 20 | 3.47 | 7.14 | 0.0 |
| 50 | 3.55 | 6.95 | 0.0 |
| 100 | 3.63 | 6.75 | 0.0 |
| 1,000 | 3.84 | 6.25 | 0.0 |
| 10,000 | 4.03 | 5.85 | 0.0 |
| 1,000,000 | 4.43 | 5.15 | 0.0 |

## SED, coco (2000 images)

CRC (marginal, one vocabulary): native recal. 3.74, anchored 3.55. Anchored RCPS at delta: size 4.12, risk 8.19%, fail 0.2%. Smallest K with native size >= anchored: 1.

| K | native size | risk (%) | fail (%) |
|---:|---:|---:|---:|
| 1 | 4.32 | 8.19 | 0.0 |
| 2 | 4.40 | 7.99 | 0.0 |
| 5 | 4.53 | 7.69 | 0.0 |
| 10 | 4.68 | 7.39 | 0.0 |
| 20 | 4.78 | 7.19 | 0.0 |
| 50 | 4.88 | 6.99 | 0.0 |
| 100 | 5.00 | 6.79 | 0.0 |
| 1,000 | 5.31 | 6.29 | 0.0 |
| 10,000 | 5.59 | 5.89 | 0.0 |
| 1,000,000 | 6.17 | 5.20 | 0.0 |

