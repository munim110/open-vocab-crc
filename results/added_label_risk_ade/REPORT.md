# Miss risk on the added labels: ViT-B, COCO-171 bank

2000 ADE validation images (0 without a source-labelled sampled pixel excluded), 500 random 1000/1000 splits. Sampled pixels: 91.6% carry a source label, 6.6% one of the 695 added labels (A-847 annotation, no source label), 0.06% an A-847 label outside the 845 names (ignored); 1367 images have at least one added-label pixel. Risk = image-level fraction of pixels of the population whose true label is missing from the set, averaged over evaluation images that contain the population. Frozen arms calibrate on source-label pixels only; the two reference arms calibrate on all 845-labelled pixels (they use the added-label annotations, which the deployment setting does not have). Set size over all labelled pixels at 845 labels. Development data; nothing fitted.

## alpha = 0.1

| Arm | Risk on source labels (%) | Risk on added labels (%) | Splits above alpha on added (%) | Risk on all labels (%) | Splits above alpha on all (%) | Set size at 845 |
|---|---:|---:|---:|---:|---:|---:|
| anchored_frozen | 9.88 | 35.96 | 100.0 | 10.52 | 80.6 | 7.81 |
| native_frozen | 15.38 | 63.17 | 100.0 | 17.14 | 100.0 | 2.77 |
| native_replay | 9.90 | 49.87 | 100.0 | 11.28 | 98.0 | 5.07 |
| anchored_calibrated_on_all845 | 9.25 | 34.39 | 100.0 | 9.85 | 40.2 | 8.41 |
| native_calibrated_on_all845 | 8.61 | 45.66 | 100.0 | 9.87 | 44.4 | 6.16 |
| native_at_anchored_frozen_size | 7.24 | 40.75 | 100.0 | 8.34 | 0.0 | 7.81 |
| anchored_at_native_replay_size | 14.31 | 45.41 | 100.0 | 15.14 | 100.0 | 5.06 |

## alpha = 0.05

| Arm | Risk on source labels (%) | Risk on added labels (%) | Splits above alpha on added (%) | Risk on all labels (%) | Splits above alpha on all (%) | Set size at 845 |
|---|---:|---:|---:|---:|---:|---:|
| anchored_frozen | 4.89 | 21.82 | 100.0 | 5.17 | 66.0 | 16.86 |
| native_frozen | 8.15 | 44.07 | 100.0 | 9.36 | 100.0 | 6.66 |
| native_replay | 4.90 | 28.86 | 100.0 | 5.55 | 86.0 | 13.47 |
| anchored_calibrated_on_all845 | 4.60 | 21.01 | 100.0 | 4.87 | 38.6 | 17.80 |
| native_calibrated_on_all845 | 4.34 | 26.18 | 100.0 | 4.89 | 39.2 | 15.78 |
| native_at_anchored_frozen_size | 4.12 | 25.06 | 100.0 | 4.62 | 14.0 | 16.86 |
| anchored_at_native_replay_size | 6.11 | 25.49 | 100.0 | 6.48 | 99.8 | 13.47 |

The guarantee covers the source-label column only. The added-label column is what a deployment would see on the new labels with the frozen threshold; the reference arms show what recalibrating with added-label annotations would cost in set size. The two size-matched rows carry no guarantee: native_at_anchored_frozen_size moves the native threshold to the grid point whose calibration-image set size is closest to the anchored frozen threshold's (same size, native scores), and anchored_at_native_replay_size shrinks the anchored sets to the native replay size; they separate what the scores do from what the set size does.