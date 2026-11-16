# Alternative image losses under source-calibrated thresholds: pascal_fcclip_bank683

2000 Pascal Context validation images (0 without a source-labelled sampled pixel excluded), 59 source labels, 458 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration pascal_fcclip_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
Each block calibrates the threshold by image-level CRC on the named loss and reports the mean of that loss on the evaluation images, the fraction of splits above alpha, and the mean set size at the grown vocabulary (native_source: at the source vocabulary). fnr is the headline loss; fnr_gt_tau is 1[fnr > tau] (CRC then bounds the fraction of images that lose more than tau of their source pixels); class_balanced averages the per-class miss fraction over the classes present in the image; worst_class takes the largest.

## alpha = 0.1

| Loss | Arm | Mean loss (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| fnr | native_source | 9.89 | 0.75 | 44.0 | 1.95 |
| fnr | native_frozen | 16.25 | 1.00 | 100.0 | 2.82 |
| fnr | native_replay | 9.86 | 0.78 | 39.6 | 5.31 |
| fnr | anchored_frozen | 9.89 | 0.75 | 41.4 | 5.77 |
| fnr_gt_0.25 | native_source | 9.95 | 1.37 | 45.6 | 2.27 |
| fnr_gt_0.25 | native_frozen | 18.26 | 2.31 | 100.0 | 3.69 |
| fnr_gt_0.25 | native_replay | 9.92 | 1.38 | 44.8 | 7.25 |
| fnr_gt_0.25 | anchored_frozen | 9.93 | 1.37 | 43.6 | 8.19 |
| fnr_gt_0.10 | native_source | 9.99 | 1.40 | 47.8 | 3.75 |
| fnr_gt_0.10 | native_frozen | 17.99 | 1.96 | 100.0 | 8.59 |
| fnr_gt_0.10 | native_replay | 9.98 | 1.37 | 46.0 | 16.72 |
| fnr_gt_0.10 | anchored_frozen | 9.96 | 1.40 | 43.8 | 17.41 |
| class_balanced | native_source | 9.90 | 0.55 | 42.4 | 2.47 |
| class_balanced | native_frozen | 16.50 | 0.72 | 100.0 | 4.27 |
| class_balanced | native_replay | 9.88 | 0.57 | 39.4 | 9.22 |
| class_balanced | anchored_frozen | 9.89 | 0.56 | 39.0 | 10.28 |
| worst_class | native_source | 9.89 | 1.04 | 46.2 | 8.24 |
| worst_class | native_frozen | 19.49 | 1.38 | 100.0 | 29.28 |
| worst_class | native_replay | 9.88 | 1.05 | 45.4 | 61.29 |
| worst_class | anchored_frozen | 9.91 | 1.06 | 46.8 | 59.70 |

## alpha = 0.05

| Loss | Arm | Mean loss (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| fnr | native_source | 4.89 | 0.55 | 37.6 | 3.13 |
| fnr | native_frozen | 8.56 | 0.76 | 100.0 | 6.36 |
| fnr | native_replay | 4.87 | 0.54 | 41.4 | 12.78 |
| fnr | anchored_frozen | 4.88 | 0.54 | 39.2 | 13.97 |
| fnr_gt_0.25 | native_source | 4.98 | 0.97 | 47.0 | 3.45 |
| fnr_gt_0.25 | native_frozen | 9.64 | 1.55 | 100.0 | 7.48 |
| fnr_gt_0.25 | native_replay | 4.97 | 1.02 | 46.4 | 15.37 |
| fnr_gt_0.25 | anchored_frozen | 4.94 | 1.01 | 43.0 | 16.55 |
| fnr_gt_0.10 | native_source | 4.93 | 0.97 | 46.2 | 5.98 |
| fnr_gt_0.10 | native_frozen | 9.45 | 1.43 | 100.0 | 18.17 |
| fnr_gt_0.10 | native_replay | 4.96 | 1.01 | 47.8 | 36.22 |
| fnr_gt_0.10 | anchored_frozen | 4.97 | 0.99 | 44.4 | 34.90 |
| class_balanced | native_source | 4.89 | 0.39 | 34.4 | 4.30 |
| class_balanced | native_frozen | 8.88 | 0.51 | 100.0 | 10.73 |
| class_balanced | native_replay | 4.90 | 0.39 | 36.8 | 24.06 |
| class_balanced | anchored_frozen | 4.90 | 0.38 | 37.4 | 25.17 |
| worst_class | native_source | 4.92 | 0.70 | 43.8 | 13.66 |
| worst_class | native_frozen | 10.38 | 1.01 | 100.0 | 58.23 |
| worst_class | native_replay | 4.90 | 0.75 | 44.0 | 107.20 |
| worst_class | anchored_frozen | 4.93 | 0.74 | 43.2 | 105.39 |

CRC controls the mean of the loss over splits; individual splits may exceed alpha. Set size is the mean number of labels per labelled sampled pixel at the evaluation vocabulary (2.5-97.5% split range in results.json). Stored scores are float16 logits clamped to [-30, 30].