# Miss risk on the added labels: sed_bank683

2000 ADE validation images (0 without a source-labelled sampled pixel excluded), 500 random 1000/1000 splits. Sampled pixels: 91.6% carry a source label, 6.6% one of the 695 added labels (A-847 annotation, no source label), 0.06% an A-847 label outside the 845 names (ignored); 1367 images have at least one added-label pixel. Risk = image-level fraction of pixels of the population whose true label is missing from the set, averaged over evaluation images that contain the population. Frozen arms calibrate on source-label pixels only; the two reference arms calibrate on all 845-labelled pixels (they use the added-label annotations, which the deployment setting does not have). Set size over all labelled pixels at 845 labels. Development data; nothing fitted.

## alpha = 0.1

| Arm | Risk on source labels (%) | Risk on added labels (%) | Splits above alpha on added (%) | Risk on all labels (%) | Splits above alpha on all (%) | Set size at 845 |
|---|---:|---:|---:|---:|---:|---:|
| anchored_frozen | 9.89 | 36.17 | 100.0 | 10.24 | 64.8 | 6.31 |
| native_frozen | 7.12 | 31.91 | 100.0 | 7.53 | 0.0 | 8.88 |
| native_replay | 9.90 | 42.48 | 100.0 | 10.67 | 82.8 | 5.34 |
| anchored_calibrated_on_all845 | 9.54 | 35.34 | 100.0 | 9.88 | 46.0 | 6.58 |
| native_calibrated_on_all845 | 9.21 | 40.30 | 100.0 | 9.90 | 44.4 | 5.94 |
| native_at_anchored_frozen_size | 8.83 | 39.04 | 100.0 | 9.47 | 15.8 | 6.31 |
| anchored_at_native_replay_size | 11.43 | 39.22 | 100.0 | 11.82 | 98.0 | 5.34 |

## alpha = 0.05

| Arm | Risk on source labels (%) | Risk on added labels (%) | Splits above alpha on added (%) | Risk on all labels (%) | Splits above alpha on all (%) | Set size at 845 |
|---|---:|---:|---:|---:|---:|---:|
| anchored_frozen | 4.89 | 20.29 | 100.0 | 5.04 | 52.8 | 16.14 |
| native_frozen | 3.79 | 16.01 | 100.0 | 3.90 | 0.6 | 24.91 |
| native_replay | 4.90 | 21.76 | 100.0 | 5.10 | 57.0 | 16.28 |
| anchored_calibrated_on_all845 | 4.76 | 19.77 | 100.0 | 4.90 | 42.0 | 16.80 |
| native_calibrated_on_all845 | 4.71 | 20.82 | 100.0 | 4.90 | 39.2 | 17.31 |
| native_at_anchored_frozen_size | 4.92 | 21.89 | 100.0 | 5.13 | 60.4 | 16.14 |
| anchored_at_native_replay_size | 4.87 | 20.18 | 100.0 | 5.01 | 50.6 | 16.29 |

The guarantee covers the source-label column only. The added-label column is what a deployment would see on the new labels with the frozen threshold; the reference arms show what recalibrating with added-label annotations would cost in set size. The two size-matched rows carry no guarantee: native_at_anchored_frozen_size moves the native threshold to the grid point whose calibration-image set size is closest to the anchored frozen threshold's (same size, native scores), and anchored_at_native_replay_size shrinks the anchored sets to the native replay size; they separate what the scores do from what the set size does.