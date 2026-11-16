# Miss risk on the added labels: vitl_bank683

2000 ADE validation images (0 without a source-labelled sampled pixel excluded), 500 random 1000/1000 splits. Sampled pixels: 91.6% carry a source label, 6.6% one of the 695 added labels (A-847 annotation, no source label), 0.06% an A-847 label outside the 845 names (ignored); 1367 images have at least one added-label pixel. Risk = image-level fraction of pixels of the population whose true label is missing from the set, averaged over evaluation images that contain the population. Frozen arms calibrate on source-label pixels only; the two reference arms calibrate on all 845-labelled pixels (they use the added-label annotations, which the deployment setting does not have). Set size over all labelled pixels at 845 labels. Development data; nothing fitted.

## alpha = 0.1

| Arm | Risk on source labels (%) | Risk on added labels (%) | Splits above alpha on added (%) | Risk on all labels (%) | Splits above alpha on all (%) | Set size at 845 |
|---|---:|---:|---:|---:|---:|---:|
| anchored_frozen | 9.88 | 32.38 | 100.0 | 10.39 | 73.2 | 4.48 |
| native_frozen | 15.22 | 55.45 | 100.0 | 16.66 | 100.0 | 2.20 |
| native_replay | 9.91 | 42.04 | 100.0 | 10.93 | 91.0 | 3.55 |
| anchored_calibrated_on_all845 | 9.37 | 31.29 | 100.0 | 9.86 | 42.2 | 4.70 |
| native_calibrated_on_all845 | 8.97 | 39.10 | 100.0 | 9.89 | 41.8 | 3.98 |
| native_at_anchored_frozen_size | 8.10 | 36.12 | 100.0 | 8.93 | 2.0 | 4.47 |
| anchored_at_native_replay_size | 12.64 | 37.91 | 100.0 | 13.24 | 100.0 | 3.55 |

## alpha = 0.05

| Arm | Risk on source labels (%) | Risk on added labels (%) | Splits above alpha on added (%) | Risk on all labels (%) | Splits above alpha on all (%) | Set size at 845 |
|---|---:|---:|---:|---:|---:|---:|
| anchored_frozen | 4.89 | 20.69 | 100.0 | 5.17 | 62.8 | 9.02 |
| native_frozen | 8.38 | 37.07 | 100.0 | 9.24 | 100.0 | 4.31 |
| native_replay | 4.90 | 24.39 | 100.0 | 5.37 | 78.4 | 7.98 |
| anchored_calibrated_on_all845 | 4.60 | 19.86 | 100.0 | 4.87 | 36.4 | 9.63 |
| native_calibrated_on_all845 | 4.46 | 22.73 | 100.0 | 4.89 | 39.6 | 8.87 |
| native_at_anchored_frozen_size | 4.39 | 22.48 | 100.0 | 4.81 | 31.0 | 9.02 |
| anchored_at_native_replay_size | 5.49 | 22.23 | 100.0 | 5.79 | 95.0 | 7.98 |

The guarantee covers the source-label column only. The added-label column is what a deployment would see on the new labels with the frozen threshold; the reference arms show what recalibrating with added-label annotations would cost in set size. The two size-matched rows carry no guarantee: native_at_anchored_frozen_size moves the native threshold to the grid point whose calibration-image set size is closest to the anchored frozen threshold's (same size, native scores), and anchored_at_native_replay_size shrinks the anchored sets to the native replay size; they separate what the scores do from what the set size does.