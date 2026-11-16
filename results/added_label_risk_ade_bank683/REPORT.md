# Miss risk on the added labels: bank683

2000 ADE validation images (0 without a source-labelled sampled pixel excluded), 500 random 1000/1000 splits. Sampled pixels: 91.6% carry a source label, 6.6% one of the 695 added labels (A-847 annotation, no source label), 0.06% an A-847 label outside the 845 names (ignored); 1367 images have at least one added-label pixel. Risk = image-level fraction of pixels of the population whose true label is missing from the set, averaged over evaluation images that contain the population. Frozen arms calibrate on source-label pixels only; the two reference arms calibrate on all 845-labelled pixels (they use the added-label annotations, which the deployment setting does not have). Set size over all labelled pixels at 845 labels. Development data; nothing fitted.

## alpha = 0.1

| Arm | Risk on source labels (%) | Risk on added labels (%) | Splits above alpha on added (%) | Risk on all labels (%) | Splits above alpha on all (%) | Set size at 845 |
|---|---:|---:|---:|---:|---:|---:|
| anchored_frozen | 9.88 | 40.31 | 100.0 | 10.64 | 84.2 | 6.24 |
| native_frozen | 15.38 | 63.17 | 100.0 | 17.14 | 100.0 | 2.77 |
| native_replay | 9.90 | 49.87 | 100.0 | 11.28 | 98.0 | 5.07 |
| anchored_calibrated_on_all845 | 9.14 | 38.28 | 100.0 | 9.86 | 45.0 | 6.84 |
| native_calibrated_on_all845 | 8.61 | 45.66 | 100.0 | 9.87 | 44.4 | 6.16 |
| native_at_anchored_frozen_size | 8.54 | 45.42 | 100.0 | 9.79 | 36.0 | 6.23 |
| anchored_at_native_replay_size | 11.83 | 44.94 | 100.0 | 12.67 | 100.0 | 5.07 |

## alpha = 0.05

| Arm | Risk on source labels (%) | Risk on added labels (%) | Splits above alpha on added (%) | Risk on all labels (%) | Splits above alpha on all (%) | Set size at 845 |
|---|---:|---:|---:|---:|---:|---:|
| anchored_frozen | 4.89 | 24.34 | 100.0 | 5.28 | 72.2 | 14.79 |
| native_frozen | 8.15 | 44.07 | 100.0 | 9.36 | 100.0 | 6.66 |
| native_replay | 4.90 | 28.86 | 100.0 | 5.55 | 86.0 | 13.47 |
| anchored_calibrated_on_all845 | 4.54 | 23.10 | 100.0 | 4.88 | 40.0 | 16.19 |
| native_calibrated_on_all845 | 4.34 | 26.18 | 100.0 | 4.89 | 39.2 | 15.78 |
| native_at_anchored_frozen_size | 4.57 | 27.24 | 100.0 | 5.15 | 63.0 | 14.78 |
| anchored_at_native_replay_size | 5.26 | 25.77 | 100.0 | 5.69 | 92.2 | 13.47 |

The guarantee covers the source-label column only. The added-label column is what a deployment would see on the new labels with the frozen threshold; the reference arms show what recalibrating with added-label annotations would cost in set size. The two size-matched rows carry no guarantee: native_at_anchored_frozen_size moves the native threshold to the grid point whose calibration-image set size is closest to the anchored frozen threshold's (same size, native scores), and anchored_at_native_replay_size shrinks the anchored sets to the native replay size; they separate what the scores do from what the set size does.