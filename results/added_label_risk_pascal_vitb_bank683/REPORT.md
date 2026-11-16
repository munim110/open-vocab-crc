# Miss risk on the added labels: vitb_bank683 (Pascal Context validation, 59 -> 458)

2000 Pascal Context validation images (0 without a source-labelled sampled pixel excluded), 500 random 1000/1000 splits. Sampled pixels: 91.8% carry a source label, 5.5% one of the 399 added labels (PC-459 annotation, no source label), 0.00% a PC-459 label outside the 458 names (ignored); 1099 images have at least one added-label pixel. Risk = image-level fraction of pixels of the population whose true label is missing from the set, averaged over evaluation images that contain the population. Frozen arms calibrate on source-label pixels only; the two reference arms calibrate on all 458-labelled pixels (they use the added-label annotations, which the deployment setting does not have). Set size over all labelled pixels at 458 labels. Development data; nothing fitted.

## alpha = 0.1

| Arm | Risk on source labels (%) | Risk on added labels (%) | Splits above alpha on added (%) | Risk on all labels (%) | Splits above alpha on all (%) | Set size at 458 |
|---|---:|---:|---:|---:|---:|---:|
| anchored_frozen | 9.89 | 36.52 | 100.0 | 10.97 | 91.8 | 2.96 |
| native_frozen | 15.17 | 58.67 | 100.0 | 16.95 | 100.0 | 1.66 |
| native_replay | 9.88 | 44.29 | 100.0 | 11.31 | 97.2 | 2.59 |
| anchored_calibrated_on_all845 | 8.83 | 34.33 | 100.0 | 9.88 | 41.0 | 3.24 |
| native_calibrated_on_all845 | 8.54 | 40.25 | 100.0 | 9.89 | 39.2 | 2.98 |
| native_at_anchored_frozen_size | 8.61 | 40.45 | 100.0 | 9.96 | 45.4 | 2.96 |
| anchored_at_native_replay_size | 11.57 | 39.89 | 100.0 | 12.69 | 100.0 | 2.59 |

## alpha = 0.05

| Arm | Risk on source labels (%) | Risk on added labels (%) | Splits above alpha on added (%) | Risk on all labels (%) | Splits above alpha on all (%) | Set size at 458 |
|---|---:|---:|---:|---:|---:|---:|
| anchored_frozen | 4.88 | 25.09 | 100.0 | 5.73 | 92.2 | 5.25 |
| native_frozen | 8.40 | 39.83 | 100.0 | 9.74 | 100.0 | 3.03 |
| native_replay | 4.89 | 29.11 | 100.0 | 5.98 | 97.2 | 4.81 |
| anchored_calibrated_on_all845 | 4.06 | 22.83 | 100.0 | 4.86 | 37.6 | 6.06 |
| native_calibrated_on_all845 | 3.90 | 25.61 | 100.0 | 4.89 | 38.8 | 5.79 |
| native_at_anchored_frozen_size | 4.39 | 27.44 | 100.0 | 5.44 | 82.8 | 5.24 |
| anchored_at_native_replay_size | 5.41 | 26.57 | 100.0 | 6.28 | 99.8 | 4.81 |

The guarantee covers the source-label column only. The added-label column is what a deployment would see on the new labels with the frozen threshold; the reference arms show what recalibrating with added-label annotations would cost in set size. The two size-matched rows carry no guarantee: native_at_anchored_frozen_size moves the native threshold to the grid point whose calibration-image set size is closest to the anchored frozen threshold's (same size, native scores), and anchored_at_native_replay_size shrinks the anchored sets to the native replay size; they separate what the scores do from what the set size does.