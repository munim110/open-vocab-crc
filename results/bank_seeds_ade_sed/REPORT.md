# Redraws of the 512 Open Images names in the reference bank

SED ConvNeXt-L, released weights. 400 ADE development images (the bank-sweep images), 150 source names, 845 names after growth. Every bank is the 171 COCO-Stuff names plus 512 Open Images names; `published` is the draw used in the paper, scored again here, and the others redraw the 512 names with seeds 101-105. Image-level CRC calibrated once at the source names; mean over 200 random 200/200 splits, the same splits for every row. Accuracy is over source-labelled sampled pixels, image-averaged.

## alpha = 0.1

| Bank | Shared names | Risk at 845 (%) | Size at 150 | Size at 845 | Overhead | Top-1 at 150 (%) | Top-1 at 845 (%) | Top-10 at 845 (%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| published | 512 | 9.46 | 2.84 | 6.50 | 0.85 | 71.96 | 63.90 | 91.65 |
| seed101 | 11 | 9.49 | 2.76 | 6.23 | 0.57 | 71.99 | 63.89 | 91.68 |
| seed102 | 20 | 9.49 | 2.83 | 6.44 | 0.79 | 71.94 | 63.79 | 91.68 |
| seed103 | 12 | 9.44 | 2.80 | 6.42 | 0.77 | 72.00 | 63.92 | 91.77 |
| seed104 | 18 | 9.46 | 2.80 | 6.42 | 0.77 | 72.04 | 64.15 | 91.69 |
| seed105 | 18 | 9.46 | 2.84 | 6.50 | 0.85 | 71.91 | 63.90 | 91.79 |
| published draw, stored scores |  | 9.46 | 2.84 | 6.50 | 0.85 | 71.96 | 63.90 | 91.65 |
| **five redraws: mean** | | 9.47 | 2.81 | 6.40 | 0.75 | 71.98 | 63.93 | 91.72 |
| **five redraws: sd** | | 0.02 | 0.03 | 0.11 | 0.11 | 0.05 | 0.13 | 0.06 |
| **five redraws: min** | | 9.44 | 2.76 | 6.23 | 0.57 | 71.91 | 63.79 | 91.68 |
| **five redraws: max** | | 9.49 | 2.84 | 6.50 | 0.85 | 72.04 | 64.15 | 91.79 |

Native model on the same images and splits: reused threshold 6.95% risk, 8.87 labels per pixel; recalibrated at 845 names 9.51% risk, 5.65 labels per pixel. Overhead is the anchored size at 845 minus the recalibrated native size.

Across the 200 splits the size at 845 of the published draw has a standard deviation of 0.49 labels per pixel and its risk 1.48 points.

## alpha = 0.05

| Bank | Shared names | Risk at 845 (%) | Size at 150 | Size at 845 | Overhead | Top-1 at 150 (%) | Top-1 at 845 (%) | Top-10 at 845 (%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| published | 512 | 4.49 | 5.42 | 16.42 | -1.02 | 71.96 | 63.90 | 91.65 |
| seed101 | 11 | 4.51 | 5.34 | 15.98 | -1.46 | 71.99 | 63.89 | 91.68 |
| seed102 | 20 | 4.50 | 5.35 | 16.02 | -1.43 | 71.94 | 63.79 | 91.68 |
| seed103 | 12 | 4.50 | 5.50 | 16.75 | -0.69 | 72.00 | 63.92 | 91.77 |
| seed104 | 18 | 4.50 | 5.38 | 16.31 | -1.13 | 72.04 | 64.15 | 91.69 |
| seed105 | 18 | 4.50 | 5.38 | 16.27 | -1.18 | 71.91 | 63.90 | 91.79 |
| published draw, stored scores |  | 4.49 | 5.42 | 16.42 | -1.02 | 71.96 | 63.90 | 91.65 |
| **five redraws: mean** | | 4.50 | 5.39 | 16.27 | -1.18 | 71.98 | 63.93 | 91.72 |
| **five redraws: sd** | | 0.00 | 0.06 | 0.31 | 0.31 | 0.05 | 0.13 | 0.06 |
| **five redraws: min** | | 4.50 | 5.34 | 15.98 | -1.46 | 71.91 | 63.79 | 91.68 |
| **five redraws: max** | | 4.51 | 5.50 | 16.75 | -0.69 | 72.04 | 64.15 | 91.79 |

Native model on the same images and splits: reused threshold 3.25% risk, 27.75 labels per pixel; recalibrated at 845 names 4.54% risk, 17.44 labels per pixel. Overhead is the anchored size at 845 minus the recalibrated native size.

Across the 200 splits the size at 845 of the published draw has a standard deviation of 2.97 labels per pixel and its risk 1.04 points.

Shared names: Open Images names a redraw has in common with the published draw. Standard deviations over redraws use n-1.

Published draw scored here against the stored scores: largest logit difference 0.0000, 0.000% of stored float16 entries differ.

0.98 s per image and bank on NVIDIA GeForce RTX 5070 Ti (bank pass and 845 candidates; image features excluded); peak memory 5.7 GB.