# Alternative image losses under source-calibrated thresholds: coco_vitb_bank683

2000 COCO val2017 (LVIS-annotated) images (0 without a source-labelled sampled pixel excluded), 171 source labels, 1283 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration coco_vitb_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
Each block calibrates the threshold by image-level CRC on the named loss and reports the mean of that loss on the evaluation images, the fraction of splits above alpha, and the mean set size at the grown vocabulary (native_source: at the source vocabulary). fnr is the headline loss; fnr_gt_tau is 1[fnr > tau] (CRC then bounds the fraction of images that lose more than tau of their source pixels); class_balanced averages the per-class miss fraction over the classes present in the image; worst_class takes the largest.

## alpha = 0.1

| Loss | Arm | Mean loss (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| fnr | native_source | 9.93 | 0.69 | 44.8 | 2.14 |
| fnr | native_frozen | 12.96 | 0.77 | 100.0 | 2.38 |
| fnr | native_replay | 9.94 | 0.70 | 45.8 | 3.09 |
| fnr | anchored_frozen | 9.92 | 0.68 | 44.4 | 3.83 |
| fnr_gt_0.25 | native_source | 10.05 | 1.41 | 49.2 | 2.29 |
| fnr_gt_0.25 | native_frozen | 14.11 | 1.82 | 99.8 | 2.58 |
| fnr_gt_0.25 | native_replay | 10.03 | 1.39 | 49.2 | 3.31 |
| fnr_gt_0.25 | anchored_frozen | 10.03 | 1.40 | 49.2 | 3.95 |
| fnr_gt_0.10 | native_source | 10.04 | 1.35 | 49.8 | 4.01 |
| fnr_gt_0.10 | native_frozen | 15.03 | 1.76 | 100.0 | 5.11 |
| fnr_gt_0.10 | native_replay | 9.97 | 1.32 | 46.0 | 7.08 |
| fnr_gt_0.10 | anchored_frozen | 10.03 | 1.32 | 48.2 | 7.98 |
| class_balanced | native_source | 9.90 | 0.47 | 41.0 | 3.72 |
| class_balanced | native_frozen | 15.39 | 0.57 | 100.0 | 4.66 |
| class_balanced | native_replay | 9.91 | 0.48 | 38.8 | 7.39 |
| class_balanced | anchored_frozen | 9.90 | 0.46 | 37.8 | 8.13 |
| worst_class | native_source | 9.93 | 1.10 | 47.0 | 13.74 |
| worst_class | native_frozen | 21.87 | 1.53 | 100.0 | 23.01 |
| worst_class | native_replay | 9.94 | 1.22 | 47.2 | 54.24 |
| worst_class | anchored_frozen | 9.96 | 1.09 | 48.4 | 45.52 |

## alpha = 0.05

| Loss | Arm | Mean loss (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| fnr | native_source | 4.92 | 0.50 | 44.4 | 3.52 |
| fnr | native_frozen | 6.96 | 0.62 | 100.0 | 4.35 |
| fnr | native_replay | 4.92 | 0.48 | 42.4 | 5.94 |
| fnr | anchored_frozen | 4.92 | 0.48 | 39.6 | 7.11 |
| fnr_gt_0.25 | native_source | 5.06 | 1.03 | 47.4 | 3.60 |
| fnr_gt_0.25 | native_frozen | 7.07 | 1.08 | 98.4 | 4.47 |
| fnr_gt_0.25 | native_replay | 4.99 | 0.99 | 47.6 | 5.91 |
| fnr_gt_0.25 | anchored_frozen | 5.03 | 0.99 | 46.6 | 6.81 |
| fnr_gt_0.10 | native_source | 5.03 | 0.95 | 47.6 | 6.03 |
| fnr_gt_0.10 | native_frozen | 7.94 | 1.25 | 99.2 | 8.48 |
| fnr_gt_0.10 | native_replay | 4.96 | 0.98 | 46.6 | 11.91 |
| fnr_gt_0.10 | anchored_frozen | 4.97 | 0.93 | 44.8 | 13.72 |
| class_balanced | native_source | 4.91 | 0.32 | 40.6 | 5.99 |
| class_balanced | native_frozen | 8.69 | 0.47 | 100.0 | 8.40 |
| class_balanced | native_replay | 4.91 | 0.34 | 35.6 | 14.52 |
| class_balanced | anchored_frozen | 4.90 | 0.33 | 38.0 | 14.96 |
| worst_class | native_source | 4.94 | 0.84 | 42.2 | 20.76 |
| worst_class | native_frozen | 13.96 | 1.15 | 100.0 | 36.53 |
| worst_class | native_replay | 3.96 | 2.44 | 47.2 | 454.70 |
| worst_class | anchored_frozen | 4.96 | 0.87 | 50.4 | 77.72 |

CRC controls the mean of the loss over splits; individual splits may exceed alpha. Set size is the mean number of labels per labelled sampled pixel at the evaluation vocabulary (2.5-97.5% split range in results.json). Stored scores are float16 logits clamped to [-30, 30].