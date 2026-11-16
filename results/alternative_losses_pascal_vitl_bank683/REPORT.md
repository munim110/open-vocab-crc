# Alternative image losses under source-calibrated thresholds: pascal_vitl_bank683

2000 Pascal Context validation images (0 without a source-labelled sampled pixel excluded), 59 source labels, 458 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration pascal_vitl_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
Each block calibrates the threshold by image-level CRC on the named loss and reports the mean of that loss on the evaluation images, the fraction of splits above alpha, and the mean set size at the grown vocabulary (native_source: at the source vocabulary). fnr is the headline loss; fnr_gt_tau is 1[fnr > tau] (CRC then bounds the fraction of images that lose more than tau of their source pixels); class_balanced averages the per-class miss fraction over the classes present in the image; worst_class takes the largest.

## alpha = 0.1

| Loss | Arm | Mean loss (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| fnr | native_source | 9.87 | 0.73 | 40.0 | 1.37 |
| fnr | native_frozen | 15.05 | 0.83 | 100.0 | 1.49 |
| fnr | native_replay | 9.88 | 0.73 | 42.8 | 2.07 |
| fnr | anchored_frozen | 9.90 | 0.76 | 44.4 | 2.33 |
| fnr_gt_0.25 | native_source | 9.94 | 1.32 | 45.4 | 1.54 |
| fnr_gt_0.25 | native_frozen | 17.17 | 1.65 | 100.0 | 1.75 |
| fnr_gt_0.25 | native_replay | 10.00 | 1.38 | 45.8 | 2.48 |
| fnr_gt_0.25 | anchored_frozen | 9.95 | 1.34 | 46.8 | 2.74 |
| fnr_gt_0.10 | native_source | 10.09 | 1.41 | 50.4 | 2.08 |
| fnr_gt_0.10 | native_frozen | 19.27 | 2.03 | 100.0 | 2.67 |
| fnr_gt_0.10 | native_replay | 10.08 | 1.39 | 47.4 | 4.04 |
| fnr_gt_0.10 | anchored_frozen | 10.05 | 1.33 | 48.6 | 4.34 |
| class_balanced | native_source | 9.88 | 0.54 | 42.0 | 1.59 |
| class_balanced | native_frozen | 15.53 | 0.68 | 100.0 | 1.84 |
| class_balanced | native_replay | 9.90 | 0.57 | 41.2 | 2.63 |
| class_balanced | anchored_frozen | 9.89 | 0.55 | 39.6 | 2.84 |
| worst_class | native_source | 9.90 | 1.13 | 42.8 | 3.53 |
| worst_class | native_frozen | 18.91 | 1.38 | 100.0 | 5.37 |
| worst_class | native_replay | 9.90 | 1.13 | 49.6 | 10.43 |
| worst_class | anchored_frozen | 9.90 | 1.11 | 44.2 | 9.82 |

## alpha = 0.05

| Loss | Arm | Mean loss (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| fnr | native_source | 4.88 | 0.51 | 38.4 | 1.87 |
| fnr | native_frozen | 8.56 | 0.68 | 100.0 | 2.30 |
| fnr | native_replay | 4.91 | 0.52 | 42.0 | 3.37 |
| fnr | anchored_frozen | 4.89 | 0.52 | 41.0 | 3.66 |
| fnr_gt_0.25 | native_source | 4.96 | 0.98 | 44.2 | 2.04 |
| fnr_gt_0.25 | native_frozen | 9.32 | 1.38 | 100.0 | 2.60 |
| fnr_gt_0.25 | native_replay | 4.97 | 0.96 | 42.2 | 3.85 |
| fnr_gt_0.25 | anchored_frozen | 4.98 | 0.95 | 44.8 | 4.09 |
| fnr_gt_0.10 | native_source | 4.94 | 1.01 | 39.2 | 2.76 |
| fnr_gt_0.10 | native_frozen | 10.62 | 1.55 | 100.0 | 3.91 |
| fnr_gt_0.10 | native_replay | 4.99 | 1.00 | 46.0 | 6.49 |
| fnr_gt_0.10 | anchored_frozen | 5.02 | 1.00 | 47.0 | 6.17 |
| class_balanced | native_source | 4.89 | 0.40 | 40.0 | 2.22 |
| class_balanced | native_frozen | 8.70 | 0.53 | 100.0 | 2.91 |
| class_balanced | native_replay | 4.89 | 0.40 | 37.8 | 4.62 |
| class_balanced | anchored_frozen | 4.89 | 0.41 | 39.4 | 4.78 |
| worst_class | native_source | 4.90 | 0.80 | 42.2 | 5.17 |
| worst_class | native_frozen | 11.75 | 1.15 | 100.0 | 8.78 |
| worst_class | native_replay | 4.90 | 0.78 | 42.0 | 18.93 |
| worst_class | anchored_frozen | 4.91 | 0.79 | 42.2 | 16.96 |

CRC controls the mean of the loss over splits; individual splits may exceed alpha. Set size is the mean number of labels per labelled sampled pixel at the evaluation vocabulary (2.5-97.5% split range in results.json). Stored scores are float16 logits clamped to [-30, 30].