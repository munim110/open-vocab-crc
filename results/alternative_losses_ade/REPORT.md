# Alternative image losses under source-calibrated thresholds: vitb_coco171

2000 ADE validation images (0 without a source-labelled sampled pixel excluded), 150 source labels, 845 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration vitb_coco171. Development data; nothing is fitted; the confirmation reserve is untouched.
Each block calibrates the threshold by image-level CRC on the named loss and reports the mean of that loss on the evaluation images, the fraction of splits above alpha, and the mean set size at the grown vocabulary (native_source: at the source vocabulary). fnr is the headline loss; fnr_gt_tau is 1[fnr > tau] (CRC then bounds the fraction of images that lose more than tau of their source pixels); class_balanced averages the per-class miss fraction over the classes present in the image; worst_class takes the largest.

## alpha = 0.1

| Loss | Arm | Mean loss (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| fnr | native_source | 9.88 | 0.57 | 38.4 | 2.31 |
| fnr | native_frozen | 15.38 | 0.73 | 100.0 | 2.73 |
| fnr | native_replay | 9.90 | 0.62 | 45.6 | 4.98 |
| fnr | anchored_frozen | 9.88 | 0.60 | 42.8 | 7.30 |
| fnr_gt_0.25 | native_source | 9.98 | 1.30 | 47.2 | 2.47 |
| fnr_gt_0.25 | native_frozen | 18.64 | 1.86 | 100.0 | 2.98 |
| fnr_gt_0.25 | native_replay | 9.98 | 1.30 | 46.0 | 6.27 |
| fnr_gt_0.25 | anchored_frozen | 9.99 | 1.30 | 47.0 | 8.69 |
| fnr_gt_0.10 | native_source | 9.92 | 1.30 | 46.0 | 5.84 |
| fnr_gt_0.10 | native_frozen | 17.23 | 1.81 | 100.0 | 9.00 |
| fnr_gt_0.10 | native_replay | 9.97 | 1.32 | 46.6 | 19.25 |
| fnr_gt_0.10 | anchored_frozen | 9.87 | 1.31 | 45.2 | 21.76 |
| class_balanced | native_source | 9.88 | 0.45 | 39.6 | 4.97 |
| class_balanced | native_frozen | 15.27 | 0.53 | 100.0 | 7.34 |
| class_balanced | native_replay | 9.90 | 0.46 | 40.2 | 14.07 |
| class_balanced | anchored_frozen | 9.87 | 0.46 | 37.0 | 14.10 |
| worst_class | native_source | 9.92 | 1.12 | 46.6 | 27.66 |
| worst_class | native_frozen | 24.99 | 1.33 | 100.0 | 52.54 |
| worst_class | native_replay | 4.44 | 5.51 | 39.6 | 615.18 |
| worst_class | anchored_frozen | 9.89 | 1.10 | 45.0 | 102.92 |

## alpha = 0.05

| Loss | Arm | Mean loss (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| fnr | native_source | 4.88 | 0.42 | 36.8 | 4.54 |
| fnr | native_frozen | 8.15 | 0.57 | 100.0 | 6.55 |
| fnr | native_replay | 4.90 | 0.45 | 40.8 | 13.25 |
| fnr | anchored_frozen | 4.89 | 0.42 | 41.6 | 15.86 |
| fnr_gt_0.25 | native_source | 4.99 | 0.98 | 43.8 | 4.98 |
| fnr_gt_0.25 | native_frozen | 8.86 | 1.45 | 100.0 | 7.37 |
| fnr_gt_0.25 | native_replay | 5.03 | 0.94 | 46.6 | 16.46 |
| fnr_gt_0.25 | anchored_frozen | 4.95 | 0.92 | 46.0 | 16.97 |
| fnr_gt_0.10 | native_source | 4.98 | 0.94 | 42.6 | 10.48 |
| fnr_gt_0.10 | native_frozen | 10.36 | 1.18 | 100.0 | 18.31 |
| fnr_gt_0.10 | native_replay | 5.02 | 0.96 | 47.6 | 43.43 |
| fnr_gt_0.10 | anchored_frozen | 5.00 | 0.95 | 46.4 | 41.10 |
| class_balanced | native_source | 4.89 | 0.32 | 38.2 | 9.52 |
| class_balanced | native_frozen | 8.89 | 0.41 | 100.0 | 16.34 |
| class_balanced | native_replay | 4.90 | 0.35 | 37.0 | 35.84 |
| class_balanced | anchored_frozen | 4.88 | 0.34 | 37.6 | 30.94 |
| worst_class | native_source | 4.93 | 0.76 | 44.4 | 39.06 |
| worst_class | native_frozen | 19.92 | 1.16 | 100.0 | 74.19 |
| worst_class | native_replay | 0.00 | 0.00 | 0.0 | 845.00 |
| worst_class | anchored_frozen | 4.95 | 0.74 | 47.4 | 148.92 |

CRC controls the mean of the loss over splits; individual splits may exceed alpha. Set size is the mean number of labels per labelled sampled pixel at the evaluation vocabulary (2.5-97.5% split range in results.json). Stored scores are float16 logits clamped to [-30, 30].