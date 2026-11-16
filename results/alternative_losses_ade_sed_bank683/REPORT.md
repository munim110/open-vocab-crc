# Alternative image losses under source-calibrated thresholds: sed_bank683

2000 ADE validation images (0 without a source-labelled sampled pixel excluded), 150 source labels, 845 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration sed_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
Each block calibrates the threshold by image-level CRC on the named loss and reports the mean of that loss on the evaluation images, the fraction of splits above alpha, and the mean set size at the grown vocabulary (native_source: at the source vocabulary). fnr is the headline loss; fnr_gt_tau is 1[fnr > tau] (CRC then bounds the fraction of images that lose more than tau of their source pixels); class_balanced averages the per-class miss fraction over the classes present in the image; worst_class takes the largest.

## alpha = 0.1

| Loss | Arm | Mean loss (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| fnr | native_source | 9.90 | 0.63 | 44.4 | 2.22 |
| fnr | native_frozen | 7.12 | 0.46 | 0.0 | 8.78 |
| fnr | native_replay | 9.90 | 0.68 | 44.6 | 5.27 |
| fnr | anchored_frozen | 9.89 | 0.66 | 44.8 | 6.04 |
| fnr_gt_0.25 | native_source | 10.01 | 1.29 | 48.4 | 2.36 |
| fnr_gt_0.25 | native_frozen | 8.26 | 0.87 | 0.8 | 9.63 |
| fnr_gt_0.25 | native_replay | 10.01 | 1.32 | 48.0 | 6.61 |
| fnr_gt_0.25 | anchored_frozen | 9.98 | 1.29 | 47.6 | 7.40 |
| fnr_gt_0.10 | native_source | 9.91 | 1.32 | 42.6 | 6.77 |
| fnr_gt_0.10 | native_frozen | 8.09 | 1.07 | 4.8 | 38.94 |
| fnr_gt_0.10 | native_replay | 9.93 | 1.32 | 43.8 | 25.90 |
| fnr_gt_0.10 | anchored_frozen | 9.91 | 1.32 | 47.6 | 23.44 |
| class_balanced | native_source | 9.90 | 0.47 | 40.8 | 4.76 |
| class_balanced | native_frozen | 7.21 | 0.37 | 0.0 | 25.19 |
| class_balanced | native_replay | 9.90 | 0.48 | 42.0 | 15.76 |
| class_balanced | anchored_frozen | 9.89 | 0.49 | 41.0 | 14.96 |
| worst_class | native_source | 9.93 | 1.15 | 47.6 | 30.52 |
| worst_class | native_frozen | 4.86 | 0.72 | 0.0 | 210.60 |
| worst_class | native_replay | 9.94 | 1.17 | 47.2 | 134.59 |
| worst_class | anchored_frozen | 9.90 | 1.19 | 47.6 | 138.25 |

## alpha = 0.05

| Loss | Arm | Mean loss (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| fnr | native_source | 4.90 | 0.48 | 43.4 | 4.70 |
| fnr | native_frozen | 3.79 | 0.39 | 0.2 | 24.76 |
| fnr | native_replay | 4.90 | 0.51 | 43.2 | 16.14 |
| fnr | anchored_frozen | 4.89 | 0.50 | 44.0 | 15.58 |
| fnr_gt_0.25 | native_source | 5.00 | 0.96 | 48.4 | 7.00 |
| fnr_gt_0.25 | native_frozen | 4.24 | 1.05 | 22.6 | 40.62 |
| fnr_gt_0.25 | native_replay | 5.00 | 0.96 | 47.4 | 29.76 |
| fnr_gt_0.25 | anchored_frozen | 4.99 | 0.97 | 44.6 | 30.46 |
| fnr_gt_0.10 | native_source | 4.97 | 0.97 | 45.4 | 16.53 |
| fnr_gt_0.10 | native_frozen | 3.01 | 0.72 | 0.4 | 109.49 |
| fnr_gt_0.10 | native_replay | 4.96 | 0.95 | 45.8 | 72.94 |
| fnr_gt_0.10 | anchored_frozen | 5.00 | 0.99 | 46.2 | 84.87 |
| class_balanced | native_source | 4.90 | 0.35 | 36.0 | 10.48 |
| class_balanced | native_frozen | 3.34 | 0.31 | 0.0 | 65.44 |
| class_balanced | native_replay | 4.90 | 0.35 | 37.0 | 42.66 |
| class_balanced | anchored_frozen | 4.89 | 0.37 | 38.6 | 40.84 |
| worst_class | native_source | 4.98 | 0.85 | 48.0 | 45.53 |
| worst_class | native_frozen | 2.06 | 0.46 | 0.0 | 321.15 |
| worst_class | native_replay | 4.97 | 0.85 | 45.2 | 208.26 |
| worst_class | anchored_frozen | 4.95 | 0.83 | 46.0 | 206.25 |

CRC controls the mean of the loss over splits; individual splits may exceed alpha. Set size is the mean number of labels per labelled sampled pixel at the evaluation vocabulary (2.5-97.5% split range in results.json). Stored scores are float16 logits clamped to [-30, 30].