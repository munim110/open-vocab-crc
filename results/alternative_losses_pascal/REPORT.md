# Alternative image losses under source-calibrated thresholds: pascal_vitb_coco171

2000 Pascal Context validation images (0 without a source-labelled sampled pixel excluded), 59 source labels, 458 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration pascal_vitb_coco171. Development data; nothing is fitted; the confirmation reserve is untouched.
Each block calibrates the threshold by image-level CRC on the named loss and reports the mean of that loss on the evaluation images, the fraction of splits above alpha, and the mean set size at the grown vocabulary (native_source: at the source vocabulary). fnr is the headline loss; fnr_gt_tau is 1[fnr > tau] (CRC then bounds the fraction of images that lose more than tau of their source pixels); class_balanced averages the per-class miss fraction over the classes present in the image; worst_class takes the largest.

## alpha = 0.1

| Loss | Arm | Mean loss (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| fnr | native_source | 9.87 | 0.72 | 38.6 | 1.49 |
| fnr | native_frozen | 15.17 | 0.85 | 100.0 | 1.63 |
| fnr | native_replay | 9.88 | 0.73 | 42.4 | 2.52 |
| fnr | anchored_frozen | 9.87 | 0.71 | 42.8 | 3.35 |
| fnr_gt_0.25 | native_source | 9.91 | 1.29 | 45.0 | 1.71 |
| fnr_gt_0.25 | native_frozen | 17.41 | 1.64 | 100.0 | 2.01 |
| fnr_gt_0.25 | native_replay | 9.98 | 1.33 | 42.0 | 3.24 |
| fnr_gt_0.25 | anchored_frozen | 9.94 | 1.39 | 47.0 | 4.40 |
| fnr_gt_0.10 | native_source | 10.04 | 1.39 | 49.2 | 2.45 |
| fnr_gt_0.10 | native_frozen | 19.72 | 1.87 | 100.0 | 3.49 |
| fnr_gt_0.10 | native_replay | 10.01 | 1.37 | 46.2 | 5.59 |
| fnr_gt_0.10 | anchored_frozen | 9.94 | 1.37 | 42.4 | 7.20 |
| class_balanced | native_source | 9.87 | 0.54 | 40.2 | 1.86 |
| class_balanced | native_frozen | 15.66 | 0.66 | 100.0 | 2.28 |
| class_balanced | native_replay | 9.89 | 0.53 | 42.0 | 3.63 |
| class_balanced | anchored_frozen | 9.87 | 0.53 | 43.0 | 4.02 |
| worst_class | native_source | 9.89 | 1.05 | 45.8 | 4.37 |
| worst_class | native_frozen | 20.10 | 1.41 | 100.0 | 7.88 |
| worst_class | native_replay | 9.90 | 1.12 | 46.2 | 16.12 |
| worst_class | anchored_frozen | 9.88 | 1.08 | 44.8 | 15.36 |

## alpha = 0.05

| Loss | Arm | Mean loss (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| fnr | native_source | 4.88 | 0.52 | 39.2 | 2.19 |
| fnr | native_frozen | 8.40 | 0.67 | 100.0 | 2.95 |
| fnr | native_replay | 4.89 | 0.51 | 38.4 | 4.65 |
| fnr | anchored_frozen | 4.88 | 0.53 | 37.2 | 6.00 |
| fnr_gt_0.25 | native_source | 4.97 | 1.01 | 46.2 | 2.41 |
| fnr_gt_0.25 | native_frozen | 9.42 | 1.33 | 100.0 | 3.40 |
| fnr_gt_0.25 | native_replay | 4.96 | 0.97 | 45.0 | 5.29 |
| fnr_gt_0.25 | anchored_frozen | 4.91 | 0.97 | 41.6 | 7.23 |
| fnr_gt_0.10 | native_source | 4.98 | 1.07 | 43.4 | 3.55 |
| fnr_gt_0.10 | native_frozen | 9.16 | 1.43 | 100.0 | 5.97 |
| fnr_gt_0.10 | native_replay | 4.99 | 1.00 | 45.8 | 9.88 |
| fnr_gt_0.10 | anchored_frozen | 4.97 | 1.00 | 42.6 | 12.60 |
| class_balanced | native_source | 4.89 | 0.39 | 36.4 | 2.70 |
| class_balanced | native_frozen | 8.84 | 0.52 | 100.0 | 4.05 |
| class_balanced | native_replay | 4.89 | 0.38 | 37.8 | 7.09 |
| class_balanced | anchored_frozen | 4.88 | 0.40 | 39.0 | 7.41 |
| worst_class | native_source | 4.91 | 0.75 | 44.2 | 6.41 |
| worst_class | native_frozen | 12.43 | 1.12 | 100.0 | 12.79 |
| worst_class | native_replay | 4.89 | 0.76 | 41.0 | 28.54 |
| worst_class | anchored_frozen | 4.91 | 0.76 | 41.6 | 26.29 |

CRC controls the mean of the loss over splits; individual splits may exceed alpha. Set size is the mean number of labels per labelled sampled pixel at the evaluation vocabulary (2.5-97.5% split range in results.json). Stored scores are float16 logits clamped to [-30, 30].