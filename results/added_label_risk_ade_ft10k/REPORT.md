# Miss risk on the added labels: ft10k

2000 ADE validation images (0 without a source-labelled sampled pixel excluded), 500 random 1000/1000 splits. Sampled pixels: 91.6% carry a source label, 6.6% one of the 695 added labels (A-847 annotation, no source label), 0.06% an A-847 label outside the 845 names (ignored); 1367 images have at least one added-label pixel. Risk = image-level fraction of pixels of the population whose true label is missing from the set, averaged over evaluation images that contain the population. Frozen arms calibrate on source-label pixels only; the two reference arms calibrate on all 845-labelled pixels (they use the added-label annotations, which the deployment setting does not have). Set size over all labelled pixels at 845 labels. Development data; nothing fitted.

## alpha = 0.1

| Arm | Risk on source labels (%) | Risk on added labels (%) | Splits above alpha on added (%) | Risk on all labels (%) | Splits above alpha on all (%) | Set size at 845 |
|---|---:|---:|---:|---:|---:|---:|
| anchored_frozen | 9.89 | 37.66 | 100.0 | 10.56 | 81.0 | 7.41 |
| native_frozen | 11.16 | 49.75 | 100.0 | 12.40 | 100.0 | 4.70 |
| native_replay | 9.88 | 46.56 | 100.0 | 11.05 | 95.4 | 5.44 |
| anchored_calibrated_on_all845 | 9.23 | 35.72 | 100.0 | 9.87 | 42.6 | 8.06 |
| native_calibrated_on_all845 | 8.76 | 43.46 | 100.0 | 9.86 | 42.4 | 6.28 |
| native_at_anchored_frozen_size | 7.67 | 39.44 | 100.0 | 8.66 | 0.4 | 7.41 |
| anchored_at_native_replay_size | 12.71 | 45.24 | 100.0 | 13.53 | 100.0 | 5.44 |

## alpha = 0.05

| Arm | Risk on source labels (%) | Risk on added labels (%) | Splits above alpha on added (%) | Risk on all labels (%) | Splits above alpha on all (%) | Set size at 845 |
|---|---:|---:|---:|---:|---:|---:|
| anchored_frozen | 4.89 | 22.56 | 100.0 | 5.24 | 68.6 | 16.99 |
| native_frozen | 6.14 | 32.90 | 100.0 | 6.93 | 100.0 | 9.90 |
| native_replay | 4.90 | 27.19 | 100.0 | 5.49 | 86.0 | 13.49 |
| anchored_calibrated_on_all845 | 4.57 | 21.37 | 100.0 | 4.88 | 40.8 | 18.28 |
| native_calibrated_on_all845 | 4.37 | 24.69 | 100.0 | 4.88 | 39.8 | 15.73 |
| native_at_anchored_frozen_size | 4.12 | 23.50 | 100.0 | 4.59 | 14.4 | 16.98 |
| anchored_at_native_replay_size | 5.97 | 26.13 | 100.0 | 6.41 | 99.6 | 13.50 |

The guarantee covers the source-label column only. The added-label column is what a deployment would see on the new labels with the frozen threshold; the reference arms show what recalibrating with added-label annotations would cost in set size. The two size-matched rows carry no guarantee: native_at_anchored_frozen_size moves the native threshold to the grid point whose calibration-image set size is closest to the anchored frozen threshold's (same size, native scores), and anchored_at_native_replay_size shrinks the anchored sets to the native replay size; they separate what the scores do from what the set size does.