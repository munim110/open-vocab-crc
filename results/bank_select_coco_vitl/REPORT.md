# Bank size chosen on COCO-Stuff validation images

CAT-Seg ViT-L, released weights. 500 COCO-Stuff val2017 images (0 without a source-labelled sampled pixel excluded), 4096 sampled pixels each; source = the 171 COCO-Stuff names, grown by 695 Open Images names that are in no bank. Image-level CRC calibrated on the source labels; mean over 200 random half/half splits. Anchored thresholds are frozen (the source-label loss does not depend on the other candidates); native is recalibrated on the grown vocabulary. No ADE20K or Pascal Context image is read.

## alpha = 0.1

| Arm | Labels in bank | Risk (%) | Size at 171 | Size at 866 |
|---|---:|---:|---:|---:|
| native_grown | -- | 9.66 | 2.03 | 2.33 |
| candidate_only | 0 | 9.62 | 32.58 | 139.25 |
| coco20 | 20 | 9.57 | 7.93 | 28.05 |
| coco85 | 85 | 9.56 | 2.92 | 4.81 |
| coco171 | 171 | 9.61 | 2.14 | 2.86 |
| coco_oi255 | 255 | 9.60 | 2.10 | 2.71 |
| coco_oi342 | 342 | 9.64 | 2.05 | 2.60 |
| coco_oi683 | 683 | 9.64 | 2.12 | 2.81 |
| coco_oi1366 | 1366 | 9.65 | 2.30 | 3.19 |
| coco_oi2731 | 2731 | 9.64 | 2.45 | 3.39 |
| coco_oi5462 | 5462 | 9.64 | 2.56 | 3.57 |
| oi683 | 683 | 9.62 | 2.73 | 3.95 |

Smallest anchored set at 866 labels: **coco_oi342** (2.60 labels per pixel; native recalibrated 2.33).

## alpha = 0.05

| Arm | Labels in bank | Risk (%) | Size at 171 | Size at 866 |
|---|---:|---:|---:|---:|
| native_grown | -- | 4.60 | 3.18 | 4.36 |
| candidate_only | 0 | 4.62 | 41.35 | 176.06 |
| coco20 | 20 | 4.58 | 9.89 | 35.88 |
| coco85 | 85 | 4.57 | 3.97 | 7.48 |
| coco171 | 171 | 4.57 | 3.05 | 4.85 |
| coco_oi255 | 255 | 4.58 | 3.07 | 4.70 |
| coco_oi342 | 342 | 4.59 | 3.08 | 4.67 |
| coco_oi683 | 683 | 4.61 | 3.28 | 5.01 |
| coco_oi1366 | 1366 | 4.64 | 3.46 | 5.41 |
| coco_oi2731 | 2731 | 4.62 | 3.64 | 5.65 |
| coco_oi5462 | 5462 | 4.62 | 3.78 | 5.90 |
| oi683 | 683 | 4.63 | 4.02 | 6.48 |

Smallest anchored set at 866 labels: **coco_oi342** (4.67 labels per pixel; native recalibrated 4.36).
