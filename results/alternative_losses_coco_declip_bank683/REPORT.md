# Alternative image losses under source-calibrated thresholds: coco_declip_bank683

2000 COCO val2017 (LVIS-annotated) images (0 without a source-labelled sampled pixel excluded), 171 source labels, 1283 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration coco_declip_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
Each block calibrates the threshold by image-level CRC on the named loss and reports the mean of that loss on the evaluation images, the fraction of splits above alpha, and the mean set size at the grown vocabulary (native_source: at the source vocabulary). fnr is the headline loss; fnr_gt_tau is 1[fnr > tau] (CRC then bounds the fraction of images that lose more than tau of their source pixels); class_balanced averages the per-class miss fraction over the classes present in the image; worst_class takes the largest.

## alpha = 0.1

| Loss | Arm | Mean loss (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| fnr | native_source | 9.91 | 0.69 | 43.2 | 1.85 |
| fnr | native_frozen | 12.93 | 0.77 | 100.0 | 2.07 |
| fnr | native_replay | 9.94 | 0.68 | 46.0 | 2.63 |
| fnr | anchored_frozen | 9.90 | 0.68 | 43.6 | 3.19 |
| fnr_gt_0.25 | native_source | 10.05 | 1.34 | 48.0 | 2.01 |
| fnr_gt_0.25 | native_frozen | 13.95 | 1.50 | 99.6 | 2.30 |
| fnr_gt_0.25 | native_replay | 10.07 | 1.35 | 46.8 | 2.87 |
| fnr_gt_0.25 | anchored_frozen | 9.96 | 1.39 | 42.6 | 3.45 |
| fnr_gt_0.10 | native_source | 10.08 | 1.34 | 50.0 | 3.34 |
| fnr_gt_0.10 | native_frozen | 14.65 | 1.72 | 100.0 | 4.37 |
| fnr_gt_0.10 | native_replay | 9.97 | 1.29 | 50.8 | 5.97 |
| fnr_gt_0.10 | anchored_frozen | 10.02 | 1.33 | 49.6 | 6.79 |
| class_balanced | native_source | 9.91 | 0.47 | 43.6 | 2.82 |
| class_balanced | native_frozen | 14.79 | 0.58 | 100.0 | 3.54 |
| class_balanced | native_replay | 9.92 | 0.48 | 45.4 | 5.17 |
| class_balanced | anchored_frozen | 9.89 | 0.47 | 37.8 | 5.67 |
| worst_class | native_source | 9.92 | 1.13 | 45.4 | 9.59 |
| worst_class | native_frozen | 19.86 | 1.60 | 100.0 | 15.70 |
| worst_class | native_replay | 9.92 | 1.18 | 46.6 | 31.23 |
| worst_class | anchored_frozen | 9.90 | 1.14 | 43.8 | 28.49 |

## alpha = 0.05

| Loss | Arm | Mean loss (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| fnr | native_source | 4.93 | 0.49 | 44.2 | 2.86 |
| fnr | native_frozen | 6.83 | 0.57 | 99.8 | 3.60 |
| fnr | native_replay | 4.92 | 0.49 | 43.4 | 4.83 |
| fnr | anchored_frozen | 4.92 | 0.49 | 43.8 | 5.66 |
| fnr_gt_0.25 | native_source | 5.04 | 1.02 | 48.0 | 2.90 |
| fnr_gt_0.25 | native_frozen | 6.99 | 1.15 | 96.6 | 3.67 |
| fnr_gt_0.25 | native_replay | 5.00 | 0.99 | 47.8 | 4.82 |
| fnr_gt_0.25 | anchored_frozen | 5.03 | 1.00 | 45.8 | 5.67 |
| fnr_gt_0.10 | native_source | 5.00 | 0.93 | 45.0 | 4.82 |
| fnr_gt_0.10 | native_frozen | 8.26 | 1.08 | 100.0 | 6.85 |
| fnr_gt_0.10 | native_replay | 5.00 | 0.96 | 48.4 | 9.87 |
| fnr_gt_0.10 | anchored_frozen | 4.97 | 0.92 | 46.4 | 10.53 |
| class_balanced | native_source | 4.91 | 0.32 | 37.6 | 4.29 |
| class_balanced | native_frozen | 8.44 | 0.43 | 100.0 | 5.94 |
| class_balanced | native_replay | 4.91 | 0.32 | 36.6 | 9.37 |
| class_balanced | anchored_frozen | 4.91 | 0.32 | 35.0 | 9.60 |
| worst_class | native_source | 4.93 | 0.81 | 46.6 | 15.24 |
| worst_class | native_frozen | 11.44 | 1.22 | 100.0 | 26.43 |
| worst_class | native_replay | 4.91 | 0.92 | 43.0 | 89.47 |
| worst_class | anchored_frozen | 4.94 | 0.81 | 45.0 | 53.77 |

CRC controls the mean of the loss over splits; individual splits may exceed alpha. Set size is the mean number of labels per labelled sampled pixel at the evaluation vocabulary (2.5-97.5% split range in results.json). Stored scores are float16 logits clamped to [-30, 30].