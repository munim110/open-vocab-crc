# Miss risk on the added labels: fcclip

2000 ADE validation images (0 without a source-labelled sampled pixel excluded), 500 random 1000/1000 splits. Sampled pixels: 91.6% carry a source label, 6.6% one of the 695 added labels (A-847 annotation, no source label), 0.06% an A-847 label outside the 845 names (ignored); 1367 images have at least one added-label pixel. Risk = image-level fraction of pixels of the population whose true label is missing from the set, averaged over evaluation images that contain the population. Frozen arms calibrate on source-label pixels only; the two reference arms calibrate on all 845-labelled pixels (they use the added-label annotations, which the deployment setting does not have). Set size over all labelled pixels at 845 labels. Development data; nothing fitted.

## alpha = 0.1

| Arm | Risk on source labels (%) | Risk on added labels (%) | Splits above alpha on added (%) | Risk on all labels (%) | Splits above alpha on all (%) | Set size at 845 |
|---|---:|---:|---:|---:|---:|---:|
| anchored_frozen | 9.90 | 30.98 | 100.0 | 10.01 | 49.2 | 14.07 |
| native_frozen | 13.81 | 43.00 | 100.0 | 14.22 | 100.0 | 5.22 |
| native_replay | 9.89 | 34.46 | 100.0 | 10.20 | 63.2 | 8.21 |
| anchored_calibrated_on_all845 | 9.79 | 30.70 | 100.0 | 9.90 | 39.0 | 14.30 |
| native_calibrated_on_all845 | 9.59 | 33.70 | 100.0 | 9.88 | 44.0 | 8.58 |
| native_at_anchored_frozen_size | 6.87 | 26.81 | 100.0 | 7.10 | 0.0 | 14.09 |
| anchored_at_native_replay_size | 13.51 | 40.50 | 100.0 | 13.83 | 100.0 | 8.20 |

## alpha = 0.05

| Arm | Risk on source labels (%) | Risk on added labels (%) | Splits above alpha on added (%) | Risk on all labels (%) | Splits above alpha on all (%) | Set size at 845 |
|---|---:|---:|---:|---:|---:|---:|
| anchored_frozen | 4.92 | 17.17 | 100.0 | 4.94 | 45.2 | 37.80 |
| native_frozen | 6.78 | 26.54 | 100.0 | 7.00 | 100.0 | 14.47 |
| native_replay | 4.90 | 20.44 | 100.0 | 5.01 | 51.0 | 25.43 |
| anchored_calibrated_on_all845 | 4.88 | 17.07 | 100.0 | 4.91 | 40.6 | 38.16 |
| native_calibrated_on_all845 | 4.79 | 20.03 | 100.0 | 4.90 | 40.2 | 26.43 |
| native_at_anchored_frozen_size | 3.92 | 16.36 | 100.0 | 3.97 | 0.4 | 37.85 |
| anchored_at_native_replay_size | 6.57 | 21.49 | 100.0 | 6.60 | 99.2 | 25.40 |

The guarantee covers the source-label column only. The added-label column is what a deployment would see on the new labels with the frozen threshold; the reference arms show what recalibrating with added-label annotations would cost in set size. The two size-matched rows carry no guarantee: native_at_anchored_frozen_size moves the native threshold to the grid point whose calibration-image set size is closest to the anchored frozen threshold's (same size, native scores), and anchored_at_native_replay_size shrinks the anchored sets to the native replay size; they separate what the scores do from what the set size does.