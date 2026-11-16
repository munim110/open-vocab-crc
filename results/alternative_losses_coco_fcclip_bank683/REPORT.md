# Alternative image losses under source-calibrated thresholds: coco_fcclip_bank683

2000 COCO val2017 (LVIS-annotated) images (0 without a source-labelled sampled pixel excluded), 171 source labels, 1283 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration coco_fcclip_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
Each block calibrates the threshold by image-level CRC on the named loss and reports the mean of that loss on the evaluation images, the fraction of splits above alpha, and the mean set size at the grown vocabulary (native_source: at the source vocabulary). fnr is the headline loss; fnr_gt_tau is 1[fnr > tau] (CRC then bounds the fraction of images that lose more than tau of their source pixels); class_balanced averages the per-class miss fraction over the classes present in the image; worst_class takes the largest.

## alpha = 0.1

| Loss | Arm | Mean loss (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| fnr | native_source | 9.89 | 0.68 | 45.6 | 5.98 |
| fnr | native_frozen | 17.09 | 0.98 | 100.0 | 9.72 |
| fnr | native_replay | 9.91 | 0.70 | 43.6 | 26.53 |
| fnr | anchored_frozen | 9.88 | 0.66 | 42.8 | 26.85 |
| fnr_gt_0.25 | native_source | 9.92 | 1.37 | 47.6 | 7.25 |
| fnr_gt_0.25 | native_frozen | 22.58 | 1.71 | 100.0 | 12.69 |
| fnr_gt_0.25 | native_replay | 9.92 | 1.36 | 43.0 | 36.77 |
| fnr_gt_0.25 | anchored_frozen | 9.91 | 1.36 | 46.0 | 38.76 |
| fnr_gt_0.10 | native_source | 9.92 | 1.37 | 47.6 | 16.28 |
| fnr_gt_0.10 | native_frozen | 24.36 | 2.34 | 100.0 | 39.07 |
| fnr_gt_0.10 | native_replay | 9.93 | 1.32 | 46.6 | 120.74 |
| fnr_gt_0.10 | anchored_frozen | 9.89 | 1.35 | 43.4 | 112.02 |
| class_balanced | native_source | 9.90 | 0.45 | 38.4 | 12.51 |
| class_balanced | native_frozen | 17.37 | 0.54 | 100.0 | 27.04 |
| class_balanced | native_replay | 9.87 | 0.46 | 36.6 | 81.81 |
| class_balanced | anchored_frozen | 9.89 | 0.45 | 38.8 | 72.86 |
| worst_class | native_source | 9.83 | 1.07 | 44.8 | 73.98 |
| worst_class | native_frozen | 22.96 | 1.63 | 100.0 | 298.39 |
| worst_class | native_replay | 9.86 | 1.05 | 43.6 | 518.43 |
| worst_class | anchored_frozen | 9.84 | 1.07 | 42.2 | 463.87 |

## alpha = 0.05

| Loss | Arm | Mean loss (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| fnr | native_source | 4.90 | 0.47 | 42.8 | 12.55 |
| fnr | native_frozen | 9.78 | 0.64 | 100.0 | 27.17 |
| fnr | native_replay | 4.89 | 0.47 | 41.6 | 83.09 |
| fnr | anchored_frozen | 4.90 | 0.47 | 39.8 | 77.35 |
| fnr_gt_0.25 | native_source | 4.96 | 1.01 | 44.4 | 11.79 |
| fnr_gt_0.25 | native_frozen | 13.34 | 1.31 | 100.0 | 24.90 |
| fnr_gt_0.25 | native_replay | 4.97 | 0.99 | 46.4 | 80.17 |
| fnr_gt_0.25 | anchored_frozen | 4.99 | 0.99 | 44.0 | 72.35 |
| fnr_gt_0.10 | native_source | 4.95 | 1.01 | 45.6 | 27.49 |
| fnr_gt_0.10 | native_frozen | 14.25 | 1.44 | 100.0 | 79.86 |
| fnr_gt_0.10 | native_replay | 4.91 | 0.97 | 40.0 | 218.80 |
| fnr_gt_0.10 | anchored_frozen | 4.95 | 1.01 | 40.2 | 184.46 |
| class_balanced | native_source | 4.89 | 0.29 | 34.4 | 25.93 |
| class_balanced | native_frozen | 10.58 | 0.43 | 100.0 | 73.86 |
| class_balanced | native_replay | 4.88 | 0.31 | 31.2 | 190.94 |
| class_balanced | anchored_frozen | 4.89 | 0.30 | 37.0 | 169.14 |
| worst_class | native_source | 4.87 | 0.73 | 42.0 | 97.62 |
| worst_class | native_frozen | 13.22 | 1.20 | 100.0 | 441.37 |
| worst_class | native_replay | 4.89 | 0.73 | 41.2 | 668.04 |
| worst_class | anchored_frozen | 4.88 | 0.74 | 41.4 | 632.84 |

CRC controls the mean of the loss over splits; individual splits may exceed alpha. Set size is the mean number of labels per labelled sampled pixel at the evaluation vocabulary (2.5-97.5% split range in results.json). Stored scores are float16 logits clamped to [-30, 30].