# Miss risk on the added labels: sed_fast8

2000 ADE validation images (0 without a source-labelled sampled pixel excluded), 500 random 1000/1000 splits. Sampled pixels: 91.6% carry a source label, 6.6% one of the 695 added labels (A-847 annotation, no source label), 0.06% an A-847 label outside the 845 names (ignored); 1367 images have at least one added-label pixel. Risk = image-level fraction of pixels of the population whose true label is missing from the set, averaged over evaluation images that contain the population. Frozen arms calibrate on source-label pixels only; the two reference arms calibrate on all 845-labelled pixels (they use the added-label annotations, which the deployment setting does not have). Set size over all labelled pixels at 845 labels. Development data; nothing fitted.

## alpha = 0.1

| Arm | Risk on source labels (%) | Risk on added labels (%) | Splits above alpha on added (%) | Risk on all labels (%) | Splits above alpha on all (%) | Set size at 845 |
|---|---:|---:|---:|---:|---:|---:|
| anchored_frozen | 9.90 | 30.81 | 100.0 | 10.16 | 62.6 | 7.38 |
| native_frozen | 12.84 | 52.84 | 100.0 | 14.07 | 100.0 | 3.60 |
| native_replay | 9.91 | 46.16 | 100.0 | 10.86 | 87.6 | 5.27 |
| anchored_calibrated_on_all845 | 9.63 | 30.29 | 100.0 | 9.89 | 41.6 | 7.62 |
| native_calibrated_on_all845 | 9.09 | 43.84 | 100.0 | 9.90 | 43.2 | 6.04 |
| native_at_anchored_frozen_size | 8.02 | 41.05 | 100.0 | 8.67 | 1.0 | 7.39 |
| anchored_at_native_replay_size | 13.29 | 37.36 | 100.0 | 13.66 | 100.0 | 5.27 |

## alpha = 0.05

| Arm | Risk on source labels (%) | Risk on added labels (%) | Splits above alpha on added (%) | Risk on all labels (%) | Splits above alpha on all (%) | Set size at 845 |
|---|---:|---:|---:|---:|---:|---:|
| anchored_frozen | 4.89 | 18.53 | 100.0 | 4.99 | 51.0 | 16.62 |
| native_frozen | 6.98 | 38.11 | 100.0 | 7.50 | 100.0 | 9.39 |
| native_replay | 4.91 | 31.93 | 100.0 | 5.21 | 65.6 | 21.48 |
| anchored_calibrated_on_all845 | 4.79 | 18.24 | 100.0 | 4.89 | 40.4 | 17.03 |
| native_calibrated_on_all845 | 4.59 | 30.92 | 99.0 | 4.88 | 39.6 | 35.29 |
| native_at_anchored_frozen_size | 5.31 | 33.09 | 100.0 | 5.64 | 93.8 | 16.64 |
| anchored_at_native_replay_size | 4.12 | 15.66 | 100.0 | 4.19 | 13.4 | 21.44 |

The guarantee covers the source-label column only. The added-label column is what a deployment would see on the new labels with the frozen threshold; the reference arms show what recalibrating with added-label annotations would cost in set size. The two size-matched rows carry no guarantee: native_at_anchored_frozen_size moves the native threshold to the grid point whose calibration-image set size is closest to the anchored frozen threshold's (same size, native scores), and anchored_at_native_replay_size shrinks the anchored sets to the native replay size; they separate what the scores do from what the set size does.