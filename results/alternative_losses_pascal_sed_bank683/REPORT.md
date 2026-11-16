# Alternative image losses under source-calibrated thresholds: pascal_sed_bank683

2000 Pascal Context validation images (0 without a source-labelled sampled pixel excluded), 59 source labels, 458 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration pascal_sed_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
Each block calibrates the threshold by image-level CRC on the named loss and reports the mean of that loss on the evaluation images, the fraction of splits above alpha, and the mean set size at the grown vocabulary (native_source: at the source vocabulary). fnr is the headline loss; fnr_gt_tau is 1[fnr > tau] (CRC then bounds the fraction of images that lose more than tau of their source pixels); class_balanced averages the per-class miss fraction over the classes present in the image; worst_class takes the largest.

## alpha = 0.1

| Loss | Arm | Mean loss (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| fnr | native_source | 9.90 | 0.72 | 44.0 | 1.52 |
| fnr | native_frozen | 4.65 | 0.43 | 0.0 | 4.79 |
| fnr | native_replay | 9.91 | 0.71 | 44.2 | 2.67 |
| fnr | anchored_frozen | 9.90 | 0.71 | 44.2 | 2.79 |
| fnr_gt_0.25 | native_source | 10.01 | 1.42 | 47.4 | 1.77 |
| fnr_gt_0.25 | native_frozen | 3.90 | 0.70 | 0.0 | 6.03 |
| fnr_gt_0.25 | native_replay | 10.00 | 1.37 | 48.2 | 3.31 |
| fnr_gt_0.25 | anchored_frozen | 10.06 | 1.35 | 46.0 | 3.52 |
| fnr_gt_0.10 | native_source | 10.06 | 1.48 | 48.4 | 2.52 |
| fnr_gt_0.10 | native_frozen | 3.92 | 0.64 | 0.0 | 10.38 |
| fnr_gt_0.10 | native_replay | 10.03 | 1.41 | 47.8 | 5.51 |
| fnr_gt_0.10 | anchored_frozen | 10.04 | 1.33 | 47.2 | 5.70 |
| class_balanced | native_source | 9.89 | 0.56 | 43.2 | 1.92 |
| class_balanced | native_frozen | 4.98 | 0.34 | 0.0 | 6.89 |
| class_balanced | native_replay | 9.90 | 0.57 | 43.2 | 3.92 |
| class_balanced | anchored_frozen | 9.89 | 0.54 | 41.8 | 3.99 |
| worst_class | native_source | 9.91 | 1.12 | 47.2 | 5.18 |
| worst_class | native_frozen | 4.49 | 0.57 | 0.0 | 28.88 |
| worst_class | native_replay | 9.93 | 1.12 | 48.2 | 14.89 |
| worst_class | anchored_frozen | 9.91 | 1.11 | 46.8 | 14.77 |

## alpha = 0.05

| Loss | Arm | Mean loss (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| fnr | native_source | 4.90 | 0.52 | 38.0 | 2.20 |
| fnr | native_frozen | 2.07 | 0.28 | 0.0 | 8.43 |
| fnr | native_replay | 4.90 | 0.52 | 39.4 | 4.62 |
| fnr | anchored_frozen | 4.90 | 0.50 | 40.0 | 4.76 |
| fnr_gt_0.25 | native_source | 4.96 | 1.01 | 46.2 | 2.32 |
| fnr_gt_0.25 | native_frozen | 2.03 | 0.43 | 0.0 | 9.17 |
| fnr_gt_0.25 | native_replay | 4.96 | 1.00 | 43.8 | 5.22 |
| fnr_gt_0.25 | anchored_frozen | 4.94 | 0.97 | 45.0 | 5.26 |
| fnr_gt_0.10 | native_source | 5.01 | 1.05 | 46.0 | 3.43 |
| fnr_gt_0.10 | native_frozen | 1.84 | 0.58 | 0.0 | 16.23 |
| fnr_gt_0.10 | native_replay | 4.97 | 0.99 | 46.0 | 8.96 |
| fnr_gt_0.10 | anchored_frozen | 4.99 | 0.98 | 45.8 | 8.48 |
| class_balanced | native_source | 4.90 | 0.41 | 38.6 | 2.85 |
| class_balanced | native_frozen | 2.42 | 0.24 | 0.0 | 12.40 |
| class_balanced | native_replay | 4.89 | 0.40 | 39.0 | 6.99 |
| class_balanced | anchored_frozen | 4.90 | 0.40 | 42.2 | 7.05 |
| worst_class | native_source | 4.94 | 0.80 | 46.4 | 7.90 |
| worst_class | native_frozen | 2.16 | 0.42 | 0.0 | 50.81 |
| worst_class | native_replay | 4.91 | 0.80 | 45.8 | 26.73 |
| worst_class | anchored_frozen | 4.91 | 0.80 | 44.2 | 25.95 |

CRC controls the mean of the loss over splits; individual splits may exceed alpha. Set size is the mean number of labels per labelled sampled pixel at the evaluation vocabulary (2.5-97.5% split range in results.json). Stored scores are float16 logits clamped to [-30, 30].