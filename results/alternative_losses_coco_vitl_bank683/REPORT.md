# Alternative image losses under source-calibrated thresholds: coco_vitl_bank683

2000 COCO val2017 (LVIS-annotated) images (0 without a source-labelled sampled pixel excluded), 171 source labels, 1283 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration coco_vitl_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
Each block calibrates the threshold by image-level CRC on the named loss and reports the mean of that loss on the evaluation images, the fraction of splits above alpha, and the mean set size at the grown vocabulary (native_source: at the source vocabulary). fnr is the headline loss; fnr_gt_tau is 1[fnr > tau] (CRC then bounds the fraction of images that lose more than tau of their source pixels); class_balanced averages the per-class miss fraction over the classes present in the image; worst_class takes the largest.

## alpha = 0.1

| Loss | Arm | Mean loss (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| fnr | native_source | 9.93 | 0.69 | 45.8 | 1.94 |
| fnr | native_frozen | 12.88 | 0.79 | 100.0 | 2.13 |
| fnr | native_replay | 9.95 | 0.68 | 46.2 | 2.65 |
| fnr | anchored_frozen | 9.92 | 0.68 | 42.4 | 3.21 |
| fnr_gt_0.25 | native_source | 10.07 | 1.39 | 51.4 | 2.13 |
| fnr_gt_0.25 | native_frozen | 13.86 | 1.86 | 99.0 | 2.37 |
| fnr_gt_0.25 | native_replay | 10.09 | 1.40 | 49.0 | 2.89 |
| fnr_gt_0.25 | anchored_frozen | 10.04 | 1.43 | 48.8 | 3.42 |
| fnr_gt_0.10 | native_source | 10.04 | 1.32 | 47.6 | 3.45 |
| fnr_gt_0.10 | native_frozen | 15.61 | 1.70 | 100.0 | 4.23 |
| fnr_gt_0.10 | native_replay | 10.01 | 1.36 | 46.4 | 5.75 |
| fnr_gt_0.10 | anchored_frozen | 9.98 | 1.33 | 47.0 | 6.60 |
| class_balanced | native_source | 9.89 | 0.44 | 36.4 | 3.09 |
| class_balanced | native_frozen | 15.33 | 0.56 | 100.0 | 3.70 |
| class_balanced | native_replay | 9.90 | 0.47 | 37.8 | 5.70 |
| class_balanced | anchored_frozen | 9.89 | 0.45 | 33.8 | 5.94 |
| worst_class | native_source | 9.97 | 1.11 | 49.8 | 11.42 |
| worst_class | native_frozen | 21.37 | 1.51 | 100.0 | 17.10 |
| worst_class | native_replay | 9.93 | 1.16 | 43.6 | 35.64 |
| worst_class | anchored_frozen | 9.94 | 1.12 | 47.2 | 31.76 |

## alpha = 0.05

| Loss | Arm | Mean loss (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| fnr | native_source | 4.92 | 0.49 | 40.8 | 3.01 |
| fnr | native_frozen | 7.02 | 0.57 | 100.0 | 3.59 |
| fnr | native_replay | 4.92 | 0.50 | 43.6 | 4.88 |
| fnr | anchored_frozen | 4.90 | 0.50 | 42.8 | 5.74 |
| fnr_gt_0.25 | native_source | 5.05 | 0.99 | 49.2 | 2.97 |
| fnr_gt_0.25 | native_frozen | 7.44 | 1.19 | 99.0 | 3.53 |
| fnr_gt_0.25 | native_replay | 5.04 | 0.98 | 48.2 | 4.92 |
| fnr_gt_0.25 | anchored_frozen | 5.01 | 0.97 | 49.4 | 5.66 |
| fnr_gt_0.10 | native_source | 5.04 | 0.97 | 45.0 | 5.07 |
| fnr_gt_0.10 | native_frozen | 8.26 | 1.25 | 99.6 | 6.72 |
| fnr_gt_0.10 | native_replay | 4.94 | 0.97 | 44.8 | 9.48 |
| fnr_gt_0.10 | anchored_frozen | 4.96 | 0.96 | 46.4 | 10.52 |
| class_balanced | native_source | 4.91 | 0.32 | 40.8 | 4.88 |
| class_balanced | native_frozen | 8.71 | 0.44 | 100.0 | 6.41 |
| class_balanced | native_replay | 4.91 | 0.32 | 39.6 | 10.65 |
| class_balanced | anchored_frozen | 4.91 | 0.32 | 38.0 | 10.40 |
| worst_class | native_source | 5.00 | 0.82 | 49.6 | 17.19 |
| worst_class | native_frozen | 13.30 | 1.29 | 100.0 | 26.92 |
| worst_class | native_replay | 4.97 | 0.96 | 46.4 | 98.74 |
| worst_class | anchored_frozen | 4.99 | 0.81 | 49.0 | 55.45 |

CRC controls the mean of the loss over splits; individual splits may exceed alpha. Set size is the mean number of labels per labelled sampled pixel at the evaluation vocabulary (2.5-97.5% split range in results.json). Stored scores are float16 logits clamped to [-30, 30].