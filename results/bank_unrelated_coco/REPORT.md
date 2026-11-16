# Unrelated reference banks on COCO-Stuff validation images

CAT-Seg ViT-B, released weights. 500 COCO-Stuff val2017 images (0 excluded), 4096 sampled pixels each; source = the 171 COCO-Stuff names, grown by 695 Open Images names in no bank; protocol and splits of exp_bank_select_coco.py. abstract = WordNet nouns with only abstract senses; pseudo = pronounceable non-words; coco_* = the COCO-171 core plus 512 of them. Anchored thresholds frozen; native recalibrated on the grown vocabulary. No ADE20K or Pascal Context image is read.

## alpha = 0.1

| Arm | Labels in bank | Risk (%) | Splits above alpha (%) | Size at 171 | Size at 866 |
|---|---:|---:|---:|---:|---:|
| native_grown | -- | 9.70 | 42.0 | 2.35 | 2.87 |
| coco171 | 171 | 9.67 | 36.5 | 2.28 | 3.15 |
| coco_oi683 | 683 | 9.67 | 39.0 | 2.44 | 3.32 |
| oi683 | 683 | 9.65 | 36.5 | 3.12 | 4.58 |
| abstract683 | 683 | 9.72 | 38.0 | 2.92 | 4.56 |
| pseudo683 | 683 | 9.65 | 38.0 | 3.08 | 5.06 |
| coco_abstract683 | 683 | 9.70 | 42.5 | 2.64 | 3.92 |
| coco_pseudo683 | 683 | 9.66 | 37.5 | 2.60 | 4.01 |

## alpha = 0.05

| Arm | Labels in bank | Risk (%) | Splits above alpha (%) | Size at 171 | Size at 866 |
|---|---:|---:|---:|---:|---:|
| native_grown | -- | 4.65 | 34.5 | 3.78 | 5.48 |
| coco171 | 171 | 4.62 | 33.0 | 3.56 | 6.08 |
| coco_oi683 | 683 | 4.61 | 34.0 | 3.83 | 5.98 |
| oi683 | 683 | 4.64 | 29.5 | 4.74 | 7.83 |
| abstract683 | 683 | 4.67 | 36.5 | 4.59 | 8.07 |
| pseudo683 | 683 | 4.68 | 35.0 | 4.76 | 8.56 |
| coco_abstract683 | 683 | 4.67 | 36.0 | 4.16 | 7.05 |
| coco_pseudo683 | 683 | 4.67 | 36.0 | 4.11 | 7.08 |
