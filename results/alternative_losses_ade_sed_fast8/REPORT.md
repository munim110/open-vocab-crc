# Alternative image losses under source-calibrated thresholds: sed_fast8

2000 ADE validation images (0 without a source-labelled sampled pixel excluded), 150 source labels, 845 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration sed_fast8. Development data; nothing is fitted; the confirmation reserve is untouched.
Each block calibrates the threshold by image-level CRC on the named loss and reports the mean of that loss on the evaluation images, the fraction of splits above alpha, and the mean set size at the grown vocabulary (native_source: at the source vocabulary). fnr is the headline loss; fnr_gt_tau is 1[fnr > tau] (CRC then bounds the fraction of images that lose more than tau of their source pixels); class_balanced averages the per-class miss fraction over the classes present in the image; worst_class takes the largest.

## alpha = 0.1

| Loss | Arm | Mean loss (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| fnr | native_source | 9.90 | 0.63 | 43.0 | 2.30 |
| fnr | native_frozen | 12.84 | 0.73 | 100.0 | 3.54 |
| fnr | native_replay | 9.91 | 0.71 | 45.0 | 5.18 |
| fnr | anchored_frozen | 9.90 | 0.65 | 45.2 | 6.93 |
| fnr_gt_0.25 | native_source | 10.01 | 1.26 | 48.8 | 2.60 |
| fnr_gt_0.25 | native_frozen | 14.37 | 1.83 | 99.2 | 4.16 |
| fnr_gt_0.25 | native_replay | 10.05 | 1.34 | 50.4 | 7.30 |
| fnr_gt_0.25 | anchored_frozen | 10.04 | 1.31 | 52.0 | 8.57 |
| fnr_gt_0.10 | native_source | 9.95 | 1.31 | 45.2 | 7.40 |
| fnr_gt_0.10 | native_frozen | 14.06 | 1.44 | 100.0 | 14.08 |
| fnr_gt_0.10 | native_replay | 2.87 | 5.05 | 24.6 | 648.25 |
| fnr_gt_0.10 | anchored_frozen | 9.90 | 1.28 | 45.2 | 22.93 |
| class_balanced | native_source | 9.91 | 0.49 | 43.4 | 5.74 |
| class_balanced | native_frozen | 14.70 | 0.48 | 100.0 | 10.89 |
| class_balanced | native_replay | 0.00 | 0.00 | 0.0 | 845.00 |
| class_balanced | anchored_frozen | 9.88 | 0.46 | 39.6 | 13.26 |
| worst_class | native_source | 0.00 | 0.00 | 0.0 | 150.00 |
| worst_class | native_frozen | 0.00 | 0.00 | 0.0 | 845.00 |
| worst_class | native_replay | 0.00 | 0.00 | 0.0 | 845.00 |
| worst_class | anchored_frozen | 9.92 | 1.15 | 45.2 | 116.68 |

## alpha = 0.05

| Loss | Arm | Mean loss (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| fnr | native_source | 4.90 | 0.49 | 43.6 | 4.96 |
| fnr | native_frozen | 6.98 | 0.55 | 100.0 | 9.27 |
| fnr | native_replay | 4.91 | 0.53 | 40.0 | 21.38 |
| fnr | anchored_frozen | 4.89 | 0.50 | 43.6 | 15.79 |
| fnr_gt_0.25 | native_source | 5.01 | 1.02 | 47.6 | 11.54 |
| fnr_gt_0.25 | native_frozen | 6.97 | 1.33 | 95.2 | 23.12 |
| fnr_gt_0.25 | native_replay | 0.83 | 2.22 | 12.2 | 746.52 |
| fnr_gt_0.25 | anchored_frozen | 4.99 | 0.96 | 45.6 | 26.59 |
| fnr_gt_0.10 | native_source | 0.13 | 1.00 | 1.6 | 148.08 |
| fnr_gt_0.10 | native_frozen | 0.20 | 1.54 | 1.6 | 832.25 |
| fnr_gt_0.10 | native_replay | 0.00 | 0.00 | 0.0 | 845.00 |
| fnr_gt_0.10 | anchored_frozen | 4.97 | 0.97 | 48.2 | 71.45 |
| class_balanced | native_source | 3.61 | 2.35 | 44.0 | 65.16 |
| class_balanced | native_frozen | 8.01 | 5.18 | 70.6 | 282.29 |
| class_balanced | native_replay | 0.00 | 0.00 | 0.0 | 845.00 |
| class_balanced | anchored_frozen | 4.89 | 0.36 | 37.8 | 34.22 |
| worst_class | native_source | 0.00 | 0.00 | 0.0 | 150.00 |
| worst_class | native_frozen | 0.00 | 0.00 | 0.0 | 845.00 |
| worst_class | native_replay | 0.00 | 0.00 | 0.0 | 845.00 |
| worst_class | anchored_frozen | 4.95 | 0.81 | 48.0 | 181.84 |

CRC controls the mean of the loss over splits; individual splits may exceed alpha. Set size is the mean number of labels per labelled sampled pixel at the evaluation vocabulary (2.5-97.5% split range in results.json). Stored scores are float16 logits clamped to [-30, 30].