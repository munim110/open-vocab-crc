# Redraws of the 512 Open Images names in the reference bank

CAT-Seg ViT-L, released weights. 400 ADE development images (the bank-sweep images), 150 source names, 845 names after growth. Every bank is the 171 COCO-Stuff names plus 512 Open Images names; `published` is the draw used in the paper, scored again here, and the others redraw the 512 names with seeds 101-105. Image-level CRC calibrated once at the source names; mean over 200 random 200/200 splits, the same splits for every row. Accuracy is over source-labelled sampled pixels, image-averaged.

## alpha = 0.1

| Bank | Shared names | Risk at 845 (%) | Size at 150 | Size at 845 | Overhead | Top-1 at 150 (%) | Top-1 at 845 (%) | Top-10 at 845 (%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| published | 512 | 9.48 | 2.28 | 4.48 | 0.68 | 74.19 | 66.05 | 94.31 |
| seed101 | 11 | 9.53 | 2.25 | 4.34 | 0.54 | 74.34 | 66.10 | 94.35 |
| seed102 | 20 | 9.50 | 2.31 | 4.52 | 0.72 | 74.22 | 66.02 | 94.29 |
| seed103 | 12 | 9.46 | 2.30 | 4.62 | 0.82 | 74.45 | 66.35 | 94.28 |
| seed104 | 18 | 9.50 | 2.26 | 4.38 | 0.58 | 74.31 | 66.44 | 94.34 |
| seed105 | 18 | 9.51 | 2.27 | 4.44 | 0.65 | 74.45 | 66.26 | 94.35 |
| published draw, stored scores |  | 9.48 | 2.28 | 4.48 | 0.68 | 74.19 | 66.05 | 94.31 |
| **five redraws: mean** | | 9.50 | 2.28 | 4.46 | 0.66 | 74.35 | 66.23 | 94.32 |
| **five redraws: sd** | | 0.03 | 0.03 | 0.11 | 0.11 | 0.10 | 0.17 | 0.03 |
| **five redraws: min** | | 9.46 | 2.25 | 4.34 | 0.54 | 74.22 | 66.02 | 94.28 |
| **five redraws: max** | | 9.53 | 2.31 | 4.62 | 0.82 | 74.45 | 66.44 | 94.35 |

Native model on the same images and splits: reused threshold 15.53% risk, 2.20 labels per pixel; recalibrated at 845 names 9.41% risk, 3.80 labels per pixel. Overhead is the anchored size at 845 minus the recalibrated native size.

Across the 200 splits the size at 845 of the published draw has a standard deviation of 0.27 labels per pixel and its risk 1.39 points.

## alpha = 0.05

| Bank | Shared names | Risk at 845 (%) | Size at 150 | Size at 845 | Overhead | Top-1 at 150 (%) | Top-1 at 845 (%) | Top-10 at 845 (%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| published | 512 | 4.52 | 3.65 | 8.72 | 0.87 | 74.19 | 66.05 | 94.31 |
| seed101 | 11 | 4.53 | 3.65 | 8.65 | 0.79 | 74.34 | 66.10 | 94.35 |
| seed102 | 20 | 4.52 | 3.63 | 8.62 | 0.77 | 74.22 | 66.02 | 94.29 |
| seed103 | 12 | 4.49 | 3.69 | 8.94 | 1.09 | 74.45 | 66.35 | 94.28 |
| seed104 | 18 | 4.51 | 3.68 | 8.89 | 1.03 | 74.31 | 66.44 | 94.34 |
| seed105 | 18 | 4.54 | 3.73 | 9.03 | 1.17 | 74.45 | 66.26 | 94.35 |
| published draw, stored scores |  | 4.52 | 3.65 | 8.72 | 0.87 | 74.19 | 66.05 | 94.31 |
| **five redraws: mean** | | 4.52 | 3.68 | 8.82 | 0.97 | 74.35 | 66.23 | 94.32 |
| **five redraws: sd** | | 0.02 | 0.04 | 0.18 | 0.18 | 0.10 | 0.17 | 0.03 |
| **five redraws: min** | | 4.49 | 3.63 | 8.62 | 0.77 | 74.22 | 66.02 | 94.28 |
| **five redraws: max** | | 4.54 | 3.73 | 9.03 | 1.17 | 74.45 | 66.44 | 94.35 |

Native model on the same images and splits: reused threshold 8.57% risk, 4.17 labels per pixel; recalibrated at 845 names 4.51% risk, 7.86 labels per pixel. Overhead is the anchored size at 845 minus the recalibrated native size.

Across the 200 splits the size at 845 of the published draw has a standard deviation of 0.79 labels per pixel and its risk 0.93 points.

Shared names: Open Images names a redraw has in common with the published draw. Standard deviations over redraws use n-1.

Published draw scored here against the stored scores: largest logit difference 0.0000, 0.000% of stored float16 entries differ.

3.40 s per image and bank on NVIDIA GeForce RTX 5070 Ti (bank pass and 845 candidates; image features excluded); peak memory 8.5 GB.