# Alternative image losses under source-calibrated thresholds: declip_bank683

2000 ADE validation images (0 without a source-labelled sampled pixel excluded), 150 source labels, 845 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration declip_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
Each block calibrates the threshold by image-level CRC on the named loss and reports the mean of that loss on the evaluation images, the fraction of splits above alpha, and the mean set size at the grown vocabulary (native_source: at the source vocabulary). fnr is the headline loss; fnr_gt_tau is 1[fnr > tau] (CRC then bounds the fraction of images that lose more than tau of their source pixels); class_balanced averages the per-class miss fraction over the classes present in the image; worst_class takes the largest.

## alpha = 0.1

| Loss | Arm | Mean loss (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| fnr | native_source | 9.90 | 0.61 | 43.2 | 1.84 |
| fnr | native_frozen | 14.72 | 0.76 | 100.0 | 2.17 |
| fnr | native_replay | 9.92 | 0.65 | 43.2 | 3.38 |
| fnr | anchored_frozen | 9.89 | 0.66 | 44.8 | 4.37 |
| fnr_gt_0.25 | native_source | 9.99 | 1.25 | 49.8 | 2.00 |
| fnr_gt_0.25 | native_frozen | 17.07 | 1.58 | 100.0 | 2.43 |
| fnr_gt_0.25 | native_replay | 10.02 | 1.31 | 44.6 | 4.08 |
| fnr_gt_0.25 | anchored_frozen | 9.97 | 1.32 | 48.2 | 5.39 |
| fnr_gt_0.10 | native_source | 9.91 | 1.35 | 39.8 | 3.71 |
| fnr_gt_0.10 | native_frozen | 17.69 | 2.05 | 100.0 | 5.52 |
| fnr_gt_0.10 | native_replay | 9.92 | 1.31 | 44.8 | 10.42 |
| fnr_gt_0.10 | anchored_frozen | 9.90 | 1.33 | 47.6 | 12.06 |
| class_balanced | native_source | 9.89 | 0.46 | 43.4 | 2.90 |
| class_balanced | native_frozen | 14.28 | 0.54 | 100.0 | 3.99 |
| class_balanced | native_replay | 9.90 | 0.48 | 41.8 | 6.22 |
| class_balanced | anchored_frozen | 9.87 | 0.49 | 41.8 | 7.03 |
| worst_class | native_source | 9.89 | 1.13 | 44.4 | 14.05 |
| worst_class | native_frozen | 19.11 | 1.42 | 100.0 | 26.45 |
| worst_class | native_replay | 9.91 | 1.22 | 47.0 | 60.05 |
| worst_class | anchored_frozen | 9.87 | 1.13 | 44.8 | 51.34 |

## alpha = 0.05

| Loss | Arm | Mean loss (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| fnr | native_source | 4.90 | 0.44 | 41.2 | 3.10 |
| fnr | native_frozen | 7.96 | 0.58 | 100.0 | 4.35 |
| fnr | native_replay | 4.91 | 0.46 | 41.4 | 7.62 |
| fnr | anchored_frozen | 4.89 | 0.46 | 39.6 | 8.72 |
| fnr_gt_0.25 | native_source | 5.00 | 0.93 | 45.8 | 3.16 |
| fnr_gt_0.25 | native_frozen | 9.24 | 1.43 | 99.8 | 4.47 |
| fnr_gt_0.25 | native_replay | 5.01 | 0.94 | 49.2 | 8.70 |
| fnr_gt_0.25 | anchored_frozen | 4.99 | 0.96 | 42.4 | 10.41 |
| fnr_gt_0.10 | native_source | 5.02 | 0.97 | 47.8 | 6.52 |
| fnr_gt_0.10 | native_frozen | 9.38 | 1.17 | 100.0 | 11.16 |
| fnr_gt_0.10 | native_replay | 4.99 | 0.97 | 43.6 | 22.59 |
| fnr_gt_0.10 | anchored_frozen | 5.02 | 0.93 | 47.0 | 24.32 |
| class_balanced | native_source | 4.89 | 0.34 | 39.0 | 4.99 |
| class_balanced | native_frozen | 8.01 | 0.42 | 100.0 | 8.05 |
| class_balanced | native_replay | 4.90 | 0.35 | 38.6 | 14.52 |
| class_balanced | anchored_frozen | 4.89 | 0.35 | 37.6 | 15.76 |
| worst_class | native_source | 4.91 | 0.77 | 42.0 | 23.50 |
| worst_class | native_frozen | 12.46 | 1.05 | 100.0 | 44.57 |
| worst_class | native_replay | 4.96 | 0.87 | 49.6 | 136.71 |
| worst_class | anchored_frozen | 4.91 | 0.78 | 44.8 | 89.40 |

CRC controls the mean of the loss over splits; individual splits may exceed alpha. Set size is the mean number of labels per labelled sampled pixel at the evaluation vocabulary (2.5-97.5% split range in results.json). Stored scores are float16 logits clamped to [-30, 30].