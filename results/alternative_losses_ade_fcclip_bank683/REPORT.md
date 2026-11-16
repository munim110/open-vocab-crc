# Alternative image losses under source-calibrated thresholds: fcclip_bank683

2000 ADE validation images (0 without a source-labelled sampled pixel excluded), 150 source labels, 845 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration fcclip_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
Each block calibrates the threshold by image-level CRC on the named loss and reports the mean of that loss on the evaluation images, the fraction of splits above alpha, and the mean set size at the grown vocabulary (native_source: at the source vocabulary). fnr is the headline loss; fnr_gt_tau is 1[fnr > tau] (CRC then bounds the fraction of images that lose more than tau of their source pixels); class_balanced averages the per-class miss fraction over the classes present in the image; worst_class takes the largest.

## alpha = 0.1

| Loss | Arm | Mean loss (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| fnr | native_source | 9.89 | 0.62 | 39.8 | 3.22 |
| fnr | native_frozen | 13.81 | 0.77 | 100.0 | 5.17 |
| fnr | native_replay | 9.89 | 0.66 | 43.0 | 8.17 |
| fnr | anchored_frozen | 9.89 | 0.64 | 43.8 | 11.14 |
| fnr_gt_0.25 | native_source | 9.95 | 1.29 | 49.0 | 3.45 |
| fnr_gt_0.25 | native_frozen | 16.05 | 1.73 | 100.0 | 5.64 |
| fnr_gt_0.25 | native_replay | 9.99 | 1.31 | 49.0 | 9.36 |
| fnr_gt_0.25 | anchored_frozen | 9.98 | 1.31 | 48.6 | 13.44 |
| fnr_gt_0.10 | native_source | 9.94 | 1.33 | 45.0 | 11.69 |
| fnr_gt_0.10 | native_frozen | 12.96 | 1.39 | 99.0 | 24.49 |
| fnr_gt_0.10 | native_replay | 9.99 | 1.30 | 47.0 | 42.88 |
| fnr_gt_0.10 | anchored_frozen | 9.96 | 1.33 | 47.4 | 48.54 |
| class_balanced | native_source | 9.91 | 0.47 | 41.4 | 7.61 |
| class_balanced | native_frozen | 13.44 | 0.56 | 100.0 | 14.57 |
| class_balanced | native_replay | 9.90 | 0.49 | 40.8 | 25.05 |
| class_balanced | anchored_frozen | 9.89 | 0.49 | 41.8 | 29.22 |
| worst_class | native_source | 9.92 | 1.10 | 49.0 | 49.47 |
| worst_class | native_frozen | 15.86 | 1.32 | 100.0 | 149.53 |
| worst_class | native_replay | 9.94 | 1.08 | 45.8 | 211.18 |
| worst_class | anchored_frozen | 9.92 | 1.13 | 46.0 | 222.87 |

## alpha = 0.05

| Loss | Arm | Mean loss (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| fnr | native_source | 4.90 | 0.46 | 40.0 | 7.56 |
| fnr | native_frozen | 6.78 | 0.60 | 100.0 | 14.47 |
| fnr | native_replay | 4.90 | 0.49 | 40.8 | 25.58 |
| fnr | anchored_frozen | 4.91 | 0.48 | 42.6 | 30.97 |
| fnr_gt_0.25 | native_source | 5.02 | 0.92 | 47.0 | 10.21 |
| fnr_gt_0.25 | native_frozen | 6.63 | 1.11 | 95.2 | 20.84 |
| fnr_gt_0.25 | native_replay | 5.01 | 0.94 | 47.6 | 42.84 |
| fnr_gt_0.25 | anchored_frozen | 5.00 | 0.93 | 46.6 | 47.29 |
| fnr_gt_0.10 | native_source | 5.04 | 0.99 | 48.2 | 28.80 |
| fnr_gt_0.10 | native_frozen | 7.16 | 1.18 | 99.0 | 74.31 |
| fnr_gt_0.10 | native_replay | 5.01 | 0.96 | 47.0 | 129.57 |
| fnr_gt_0.10 | anchored_frozen | 4.97 | 0.97 | 45.2 | 150.11 |
| class_balanced | native_source | 4.93 | 0.33 | 43.4 | 17.79 |
| class_balanced | native_frozen | 7.30 | 0.43 | 100.0 | 40.72 |
| class_balanced | native_replay | 4.91 | 0.34 | 40.2 | 69.01 |
| class_balanced | anchored_frozen | 4.90 | 0.33 | 36.8 | 77.97 |
| worst_class | native_source | 4.94 | 0.78 | 42.2 | 67.55 |
| worst_class | native_frozen | 8.88 | 1.07 | 100.0 | 227.53 |
| worst_class | native_replay | 4.93 | 0.79 | 44.0 | 317.84 |
| worst_class | anchored_frozen | 4.92 | 0.78 | 43.0 | 319.69 |

CRC controls the mean of the loss over splits; individual splits may exceed alpha. Set size is the mean number of labels per labelled sampled pixel at the evaluation vocabulary (2.5-97.5% split range in results.json). Stored scores are float16 logits clamped to [-30, 30].