# Alternative image losses under source-calibrated thresholds: vitl_bank683

2000 ADE validation images (0 without a source-labelled sampled pixel excluded), 150 source labels, 845 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration vitl_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
Each block calibrates the threshold by image-level CRC on the named loss and reports the mean of that loss on the evaluation images, the fraction of splits above alpha, and the mean set size at the grown vocabulary (native_source: at the source vocabulary). fnr is the headline loss; fnr_gt_tau is 1[fnr > tau] (CRC then bounds the fraction of images that lose more than tau of their source pixels); class_balanced averages the per-class miss fraction over the classes present in the image; worst_class takes the largest.

## alpha = 0.1

| Loss | Arm | Mean loss (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| fnr | native_source | 9.90 | 0.59 | 39.4 | 1.91 |
| fnr | native_frozen | 15.22 | 0.74 | 100.0 | 2.16 |
| fnr | native_replay | 9.91 | 0.64 | 43.2 | 3.47 |
| fnr | anchored_frozen | 9.88 | 0.64 | 41.0 | 4.27 |
| fnr_gt_0.25 | native_source | 9.96 | 1.35 | 44.2 | 2.08 |
| fnr_gt_0.25 | native_frozen | 17.97 | 1.56 | 100.0 | 2.40 |
| fnr_gt_0.25 | native_replay | 9.97 | 1.35 | 42.6 | 4.13 |
| fnr_gt_0.25 | anchored_frozen | 9.95 | 1.36 | 45.4 | 5.01 |
| fnr_gt_0.10 | native_source | 9.90 | 1.34 | 44.0 | 4.04 |
| fnr_gt_0.10 | native_frozen | 18.80 | 1.98 | 100.0 | 5.47 |
| fnr_gt_0.10 | native_replay | 9.91 | 1.29 | 45.0 | 10.41 |
| fnr_gt_0.10 | anchored_frozen | 9.87 | 1.33 | 42.2 | 11.06 |
| class_balanced | native_source | 9.88 | 0.47 | 42.0 | 3.24 |
| class_balanced | native_frozen | 15.26 | 0.58 | 100.0 | 4.14 |
| class_balanced | native_replay | 9.88 | 0.49 | 38.8 | 7.35 |
| class_balanced | anchored_frozen | 9.86 | 0.49 | 37.2 | 7.80 |
| worst_class | native_source | 9.90 | 1.09 | 45.8 | 17.41 |
| worst_class | native_frozen | 22.39 | 1.44 | 100.0 | 29.03 |
| worst_class | native_replay | 9.91 | 1.17 | 47.0 | 77.05 |
| worst_class | anchored_frozen | 9.86 | 1.09 | 42.4 | 62.69 |

## alpha = 0.05

| Loss | Arm | Mean loss (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| fnr | native_source | 4.89 | 0.44 | 35.8 | 3.28 |
| fnr | native_frozen | 8.38 | 0.60 | 100.0 | 4.21 |
| fnr | native_replay | 4.90 | 0.47 | 38.0 | 7.81 |
| fnr | anchored_frozen | 4.89 | 0.46 | 39.2 | 8.63 |
| fnr_gt_0.25 | native_source | 5.02 | 0.96 | 46.4 | 3.24 |
| fnr_gt_0.25 | native_frozen | 9.98 | 1.74 | 100.0 | 4.15 |
| fnr_gt_0.25 | native_replay | 5.05 | 0.94 | 47.4 | 8.38 |
| fnr_gt_0.25 | anchored_frozen | 5.00 | 0.96 | 44.4 | 9.45 |
| fnr_gt_0.10 | native_source | 4.94 | 0.96 | 39.8 | 6.24 |
| fnr_gt_0.10 | native_frozen | 11.10 | 1.24 | 100.0 | 9.33 |
| fnr_gt_0.10 | native_replay | 4.96 | 0.97 | 41.6 | 22.12 |
| fnr_gt_0.10 | anchored_frozen | 4.94 | 0.94 | 42.0 | 21.95 |
| class_balanced | native_source | 4.88 | 0.34 | 37.8 | 5.93 |
| class_balanced | native_frozen | 8.62 | 0.44 | 100.0 | 8.79 |
| class_balanced | native_replay | 4.89 | 0.35 | 39.0 | 17.77 |
| class_balanced | anchored_frozen | 4.88 | 0.36 | 35.0 | 17.89 |
| worst_class | native_source | 4.90 | 0.84 | 44.8 | 27.43 |
| worst_class | native_frozen | 15.41 | 1.25 | 100.0 | 46.47 |
| worst_class | native_replay | 4.92 | 0.87 | 46.2 | 165.36 |
| worst_class | anchored_frozen | 4.90 | 0.82 | 43.4 | 103.40 |

CRC controls the mean of the loss over splits; individual splits may exceed alpha. Set size is the mean number of labels per labelled sampled pixel at the evaluation vocabulary (2.5-97.5% split range in results.json). Stored scores are float16 logits clamped to [-30, 30].