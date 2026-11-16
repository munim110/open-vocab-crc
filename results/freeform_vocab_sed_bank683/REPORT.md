# Calibrate, then deploy with free-form per-image names

SED (sed_bank683), 2000 ADE20K images (0 without a source-labelled sampled pixel excluded), 500 random half/half splits, image-level CRC on the source-label miss rate. Deployed vocabulary = 150 source names + the image's free-form names (16.1 on average, 5797 unique). Risk in %, above = % of splits above alpha, size = deployed labels per source-labelled pixel, added = added names among them.

## alpha = 0.1

| Arm | Risk (%) | Above (%) | Size | Added in set |
|---|---:|---:|---:|---:|
| anchored, calibrated once | 9.90 | 45.0 | 5.69 | 2.93 |
| native, reused at 150 | 20.47 | 100.0 | 3.42 | 1.83 |
| native, recalibrated at 845 | 30.31 | 100.0 | 2.28 | 1.17 |
| native, recalibrated at a 1,690-name lexicon | 35.40 | 100.0 | 1.88 | 0.93 |
| native, recalibrated at a 17,001-name lexicon | 41.18 | 100.0 | 1.52 | 0.71 |
| native, matched to the names | 9.93 | 46.2 | 6.39 | 3.29 |

## alpha = 0.05

| Arm | Risk (%) | Above (%) | Size | Added in set |
|---|---:|---:|---:|---:|
| anchored, calibrated once | 4.92 | 41.8 | 9.82 | 4.54 |
| native, reused at 150 | 8.86 | 100.0 | 6.99 | 3.54 |
| native, recalibrated at 845 | 12.71 | 100.0 | 5.24 | 2.77 |
| native, recalibrated at a 1,690-name lexicon | 15.50 | 100.0 | 4.43 | 2.36 |
| native, recalibrated at a 17,001-name lexicon | 18.92 | 100.0 | 3.70 | 1.98 |
| native, matched to the names | 4.93 | 43.2 | 10.92 | 4.99 |
