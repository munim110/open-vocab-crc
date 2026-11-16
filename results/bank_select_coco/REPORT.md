# Bank size chosen on COCO-Stuff validation images

CAT-Seg ViT-B, released weights. 500 COCO-Stuff val2017 images (0 without a source-labelled sampled pixel excluded), 4096 sampled pixels each; source = the 171 COCO-Stuff names, grown by 695 Open Images names that are in no bank. Image-level CRC calibrated on the source labels; mean over 200 random half/half splits. Anchored thresholds are frozen (the source-label loss does not depend on the other candidates); native is recalibrated on the grown vocabulary. No ADE20K or Pascal Context image is read.

## alpha = 0.1

| Arm | Labels in bank | Risk (%) | Size at 171 | Size at 866 |
|---|---:|---:|---:|---:|
| native_grown | -- | 9.70 | 2.35 | 2.87 |
| candidate_only | 0 | 9.66 | 27.03 | 108.50 |
| coco20 | 20 | 9.61 | 8.91 | 32.74 |
| coco85 | 85 | 9.56 | 3.32 | 6.18 |
| coco171 | 171 | 9.67 | 2.28 | 3.15 |
| coco_oi255 | 255 | 9.69 | 2.27 | 2.99 |
| coco_oi342 | 342 | 9.69 | 2.29 | 3.04 |
| coco_oi683 | 683 | 9.67 | 2.44 | 3.32 |
| coco_oi1366 | 1366 | 9.65 | 2.63 | 3.72 |
| coco_oi2731 | 2731 | 9.65 | 2.78 | 3.89 |
| coco_oi5462 | 5462 | 9.65 | 2.91 | 4.10 |
| oi683 | 683 | 9.65 | 3.12 | 4.58 |

Smallest anchored set at 866 labels: **coco_oi255** (2.99 labels per pixel; native recalibrated 2.87).

## alpha = 0.05

| Arm | Labels in bank | Risk (%) | Size at 171 | Size at 866 |
|---|---:|---:|---:|---:|
| native_grown | -- | 4.65 | 3.78 | 5.48 |
| candidate_only | 0 | 4.64 | 36.08 | 145.26 |
| coco20 | 20 | 4.60 | 11.85 | 45.42 |
| coco85 | 85 | 4.58 | 4.61 | 9.85 |
| coco171 | 171 | 4.62 | 3.56 | 6.08 |
| coco_oi255 | 255 | 4.62 | 3.58 | 5.78 |
| coco_oi342 | 342 | 4.62 | 3.64 | 5.79 |
| coco_oi683 | 683 | 4.61 | 3.83 | 5.98 |
| coco_oi1366 | 1366 | 4.63 | 3.99 | 6.33 |
| coco_oi2731 | 2731 | 4.65 | 4.30 | 6.77 |
| coco_oi5462 | 5462 | 4.65 | 4.49 | 7.11 |
| oi683 | 683 | 4.64 | 4.74 | 7.83 |

Smallest anchored set at 866 labels: **coco_oi255** (5.78 labels per pixel; native recalibrated 5.48).
