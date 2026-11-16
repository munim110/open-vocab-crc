# Calibrate, then deploy with free-form per-image names

CAT-Seg (vitl_bank683), 2000 ADE20K images (0 without a source-labelled sampled pixel excluded), 500 random half/half splits, image-level CRC on the source-label miss rate. Deployed vocabulary = 150 source names + the image's free-form names (16.1 on average, 5797 unique). Risk in %, above = % of splits above alpha, size = deployed labels per source-labelled pixel, added = added names among them.

## alpha = 0.1

| Arm | Risk (%) | Above (%) | Size | Added in set |
|---|---:|---:|---:|---:|
| anchored, calibrated once | 9.90 | 43.4 | 4.59 | 2.34 |
| native, reused at 150 | 20.63 | 100.0 | 2.66 | 1.26 |
| native, recalibrated at 845 | 12.64 | 100.0 | 4.06 | 2.00 |
| native, matched to the names | 9.92 | 45.0 | 4.79 | 2.35 |

## alpha = 0.05

| Arm | Risk (%) | Above (%) | Size | Added in set |
|---|---:|---:|---:|---:|
| anchored, calibrated once | 4.90 | 43.2 | 7.03 | 3.37 |
| native, reused at 150 | 10.19 | 100.0 | 4.71 | 2.31 |
| native, recalibrated at 845 | 5.13 | 55.4 | 7.29 | 3.40 |
| native, matched to the names | 4.92 | 42.0 | 7.48 | 3.48 |
