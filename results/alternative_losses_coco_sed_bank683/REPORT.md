# Alternative image losses under source-calibrated thresholds: coco_sed_bank683

2000 COCO val2017 (LVIS-annotated) images (0 without a source-labelled sampled pixel excluded), 171 source labels, 1283 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration coco_sed_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
Each block calibrates the threshold by image-level CRC on the named loss and reports the mean of that loss on the evaluation images, the fraction of splits above alpha, and the mean set size at the grown vocabulary (native_source: at the source vocabulary). fnr is the headline loss; fnr_gt_tau is 1[fnr > tau] (CRC then bounds the fraction of images that lose more than tau of their source pixels); class_balanced averages the per-class miss fraction over the classes present in the image; worst_class takes the largest.

## alpha = 0.1

| Loss | Arm | Mean loss (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| fnr | native_source | 9.93 | 0.72 | 49.0 | 2.00 |
| fnr | native_frozen | 3.64 | 0.34 | 0.0 | 8.19 |
| fnr | native_replay | 9.92 | 0.67 | 44.6 | 3.74 |
| fnr | anchored_frozen | 9.92 | 0.69 | 45.0 | 3.55 |
| fnr_gt_0.25 | native_source | 10.07 | 1.40 | 47.2 | 2.20 |
| fnr_gt_0.25 | native_frozen | 2.78 | 0.55 | 0.0 | 9.23 |
| fnr_gt_0.25 | native_replay | 10.01 | 1.43 | 49.4 | 3.88 |
| fnr_gt_0.25 | anchored_frozen | 10.01 | 1.42 | 51.2 | 3.75 |
| fnr_gt_0.10 | native_source | 10.05 | 1.34 | 50.0 | 3.68 |
| fnr_gt_0.10 | native_frozen | 2.81 | 0.45 | 0.0 | 17.34 |
| fnr_gt_0.10 | native_replay | 9.93 | 1.37 | 46.0 | 7.67 |
| fnr_gt_0.10 | anchored_frozen | 10.01 | 1.44 | 47.2 | 7.18 |
| class_balanced | native_source | 9.92 | 0.47 | 44.6 | 3.42 |
| class_balanced | native_frozen | 4.29 | 0.25 | 0.0 | 15.89 |
| class_balanced | native_replay | 9.91 | 0.48 | 40.8 | 8.24 |
| class_balanced | anchored_frozen | 9.91 | 0.48 | 39.4 | 7.51 |
| worst_class | native_source | 9.97 | 1.26 | 49.0 | 14.06 |
| worst_class | native_frozen | 4.83 | 0.72 | 0.0 | 93.87 |
| worst_class | native_replay | 9.97 | 1.26 | 49.2 | 47.85 |
| worst_class | anchored_frozen | 10.00 | 1.28 | 49.4 | 45.29 |

## alpha = 0.05

| Loss | Arm | Mean loss (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| fnr | native_source | 4.92 | 0.51 | 42.8 | 3.20 |
| fnr | native_frozen | 1.62 | 0.20 | 0.0 | 14.61 |
| fnr | native_replay | 4.91 | 0.47 | 39.6 | 6.47 |
| fnr | anchored_frozen | 4.92 | 0.48 | 43.4 | 6.16 |
| fnr_gt_0.25 | native_source | 5.05 | 1.01 | 44.4 | 3.32 |
| fnr_gt_0.25 | native_frozen | 1.37 | 0.29 | 0.0 | 15.31 |
| fnr_gt_0.25 | native_replay | 5.03 | 1.01 | 50.4 | 6.02 |
| fnr_gt_0.25 | anchored_frozen | 5.02 | 0.99 | 45.6 | 6.05 |
| fnr_gt_0.10 | native_source | 4.97 | 0.96 | 46.4 | 5.21 |
| fnr_gt_0.10 | native_frozen | 1.86 | 0.40 | 0.0 | 26.30 |
| fnr_gt_0.10 | native_replay | 4.97 | 0.95 | 47.0 | 11.56 |
| fnr_gt_0.10 | anchored_frozen | 4.93 | 0.92 | 45.6 | 11.24 |
| class_balanced | native_source | 4.92 | 0.32 | 38.6 | 5.45 |
| class_balanced | native_frozen | 2.18 | 0.17 | 0.0 | 27.74 |
| class_balanced | native_replay | 4.90 | 0.33 | 36.4 | 14.37 |
| class_balanced | anchored_frozen | 4.92 | 0.32 | 40.6 | 13.46 |
| worst_class | native_source | 4.99 | 0.87 | 48.6 | 23.21 |
| worst_class | native_frozen | 2.01 | 0.52 | 0.0 | 185.66 |
| worst_class | native_replay | 4.98 | 0.90 | 47.4 | 91.61 |
| worst_class | anchored_frozen | 4.98 | 0.90 | 49.0 | 88.93 |

CRC controls the mean of the loss over splits; individual splits may exceed alpha. Set size is the mean number of labels per labelled sampled pixel at the evaluation vocabulary (2.5-97.5% split range in results.json). Stored scores are float16 logits clamped to [-30, 30].