# Alternative image losses under source-calibrated thresholds: pascal_declip_bank683

2000 Pascal Context validation images (0 without a source-labelled sampled pixel excluded), 59 source labels, 458 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration pascal_declip_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
Each block calibrates the threshold by image-level CRC on the named loss and reports the mean of that loss on the evaluation images, the fraction of splits above alpha, and the mean set size at the grown vocabulary (native_source: at the source vocabulary). fnr is the headline loss; fnr_gt_tau is 1[fnr > tau] (CRC then bounds the fraction of images that lose more than tau of their source pixels); class_balanced averages the per-class miss fraction over the classes present in the image; worst_class takes the largest.

## alpha = 0.1

| Loss | Arm | Mean loss (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| fnr | native_source | 9.87 | 0.74 | 42.0 | 1.37 |
| fnr | native_frozen | 14.73 | 0.82 | 100.0 | 1.50 |
| fnr | native_replay | 9.89 | 0.75 | 41.8 | 2.09 |
| fnr | anchored_frozen | 9.90 | 0.76 | 43.8 | 2.41 |
| fnr_gt_0.25 | native_source | 9.95 | 1.35 | 46.2 | 1.55 |
| fnr_gt_0.25 | native_frozen | 16.76 | 1.77 | 100.0 | 1.80 |
| fnr_gt_0.25 | native_replay | 9.93 | 1.42 | 43.0 | 2.67 |
| fnr_gt_0.25 | anchored_frozen | 9.93 | 1.38 | 42.4 | 2.96 |
| fnr_gt_0.10 | native_source | 10.02 | 1.43 | 47.8 | 2.20 |
| fnr_gt_0.10 | native_frozen | 17.88 | 1.58 | 100.0 | 2.94 |
| fnr_gt_0.10 | native_replay | 9.98 | 1.42 | 46.8 | 4.37 |
| fnr_gt_0.10 | anchored_frozen | 9.99 | 1.37 | 47.2 | 4.72 |
| class_balanced | native_source | 9.87 | 0.56 | 39.8 | 1.56 |
| class_balanced | native_frozen | 15.05 | 0.66 | 100.0 | 1.82 |
| class_balanced | native_replay | 9.89 | 0.57 | 39.4 | 2.55 |
| class_balanced | anchored_frozen | 9.90 | 0.57 | 42.8 | 2.82 |
| worst_class | native_source | 9.92 | 1.03 | 44.8 | 3.30 |
| worst_class | native_frozen | 18.34 | 1.35 | 100.0 | 5.16 |
| worst_class | native_replay | 9.91 | 1.05 | 46.2 | 9.16 |
| worst_class | anchored_frozen | 9.91 | 1.07 | 46.0 | 9.05 |

## alpha = 0.05

| Loss | Arm | Mean loss (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| fnr | native_source | 4.89 | 0.52 | 39.4 | 1.89 |
| fnr | native_frozen | 8.45 | 0.70 | 100.0 | 2.36 |
| fnr | native_replay | 4.89 | 0.53 | 38.0 | 3.58 |
| fnr | anchored_frozen | 4.89 | 0.53 | 38.0 | 3.84 |
| fnr_gt_0.25 | native_source | 4.96 | 1.00 | 41.8 | 2.12 |
| fnr_gt_0.25 | native_frozen | 9.37 | 1.39 | 100.0 | 2.78 |
| fnr_gt_0.25 | native_replay | 4.97 | 0.99 | 42.8 | 4.25 |
| fnr_gt_0.25 | anchored_frozen | 4.96 | 1.00 | 43.8 | 4.57 |
| fnr_gt_0.10 | native_source | 4.98 | 1.01 | 42.2 | 2.99 |
| fnr_gt_0.10 | native_frozen | 9.55 | 1.28 | 100.0 | 4.50 |
| fnr_gt_0.10 | native_replay | 4.94 | 1.00 | 42.0 | 7.54 |
| fnr_gt_0.10 | anchored_frozen | 4.98 | 1.02 | 46.4 | 7.48 |
| class_balanced | native_source | 4.90 | 0.40 | 40.0 | 2.18 |
| class_balanced | native_frozen | 8.48 | 0.52 | 100.0 | 2.90 |
| class_balanced | native_replay | 4.90 | 0.41 | 42.8 | 4.55 |
| class_balanced | anchored_frozen | 4.90 | 0.42 | 43.0 | 4.79 |
| worst_class | native_source | 4.94 | 0.72 | 46.4 | 4.79 |
| worst_class | native_frozen | 10.61 | 1.09 | 100.0 | 8.63 |
| worst_class | native_replay | 4.92 | 0.77 | 45.6 | 16.71 |
| worst_class | anchored_frozen | 4.94 | 0.76 | 46.2 | 15.41 |

CRC controls the mean of the loss over splits; individual splits may exceed alpha. Set size is the mean number of labels per labelled sampled pixel at the evaluation vocabulary (2.5-97.5% split range in results.json). Stored scores are float16 logits clamped to [-30, 30].