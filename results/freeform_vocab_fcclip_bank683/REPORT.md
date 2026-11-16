# Calibrate, then deploy with free-form per-image names

FC-CLIP (fcclip_bank683), 2000 ADE20K images (0 without a source-labelled sampled pixel excluded), 500 random half/half splits, image-level CRC on the source-label miss rate. Deployed vocabulary = 150 source names + the image's free-form names (16.1 on average, 5797 unique). Risk in %, above = % of splits above alpha, size = deployed labels per source-labelled pixel, added = added names among them.

## alpha = 0.1

| Arm | Risk (%) | Above (%) | Size | Added in set |
|---|---:|---:|---:|---:|
| anchored, calibrated once | 9.88 | 43.0 | 8.00 | 4.21 |
| native, reused at 150 | 21.53 | 100.0 | 4.36 | 2.43 |
| native, recalibrated at 845 | 15.55 | 100.0 | 5.88 | 3.15 |
| native, recalibrated at a 1,690-name lexicon | 13.63 | 100.0 | 6.61 | 3.46 |
| native, recalibrated at a 17,001-name lexicon | 7.76 | 0.0 | 10.99 | 4.97 |
| native, matched to the names | 9.90 | 43.0 | 8.80 | 4.28 |

## alpha = 0.05

| Arm | Risk (%) | Above (%) | Size | Added in set |
|---|---:|---:|---:|---:|
| anchored, calibrated once | 4.91 | 44.0 | 15.10 | 6.42 |
| native, reused at 150 | 10.38 | 100.0 | 8.47 | 4.16 |
| native, recalibrated at 845 | 6.96 | 100.0 | 12.21 | 5.31 |
| native, recalibrated at a 1,690-name lexicon | 6.23 | 96.4 | 13.64 | 5.68 |
| native, recalibrated at a 17,001-name lexicon | 4.15 | 2.4 | 22.01 | 7.40 |
| native, matched to the names | 4.89 | 43.6 | 18.03 | 6.65 |
