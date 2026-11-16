# Miss risk on the added labels: sed_bank683 (Pascal Context validation, 59 -> 458)

2000 Pascal Context validation images (0 without a source-labelled sampled pixel excluded), 500 random 1000/1000 splits. Sampled pixels: 91.8% carry a source label, 5.5% one of the 399 added labels (PC-459 annotation, no source label), 0.00% a PC-459 label outside the 458 names (ignored); 1099 images have at least one added-label pixel. Risk = image-level fraction of pixels of the population whose true label is missing from the set, averaged over evaluation images that contain the population. Frozen arms calibrate on source-label pixels only; the two reference arms calibrate on all 458-labelled pixels (they use the added-label annotations, which the deployment setting does not have). Set size over all labelled pixels at 458 labels. Development data; nothing fitted.

## alpha = 0.1

| Arm | Risk on source labels (%) | Risk on added labels (%) | Splits above alpha on added (%) | Risk on all labels (%) | Splits above alpha on all (%) | Set size at 458 |
|---|---:|---:|---:|---:|---:|---:|
| anchored_frozen | 9.90 | 43.63 | 100.0 | 11.07 | 92.8 | 2.89 |
| native_frozen | 4.65 | 31.24 | 100.0 | 5.67 | 0.0 | 4.88 |
| native_replay | 9.91 | 49.78 | 100.0 | 11.49 | 98.4 | 2.70 |
| anchored_calibrated_on_all845 | 8.82 | 40.78 | 100.0 | 9.90 | 44.0 | 3.17 |
| native_calibrated_on_all845 | 8.45 | 45.17 | 100.0 | 9.90 | 43.0 | 3.09 |
| native_at_anchored_frozen_size | 9.15 | 47.35 | 100.0 | 10.66 | 85.2 | 2.89 |
| anchored_at_native_replay_size | 10.78 | 45.69 | 100.0 | 12.01 | 100.0 | 2.69 |

## alpha = 0.05

| Arm | Risk on source labels (%) | Risk on added labels (%) | Splits above alpha on added (%) | Risk on all labels (%) | Splits above alpha on all (%) | Set size at 458 |
|---|---:|---:|---:|---:|---:|---:|
| anchored_frozen | 4.90 | 28.59 | 100.0 | 5.72 | 93.0 | 4.94 |
| native_frozen | 2.07 | 17.93 | 100.0 | 2.74 | 0.0 | 8.63 |
| native_replay | 4.90 | 32.33 | 100.0 | 5.95 | 97.2 | 4.70 |
| anchored_calibrated_on_all845 | 4.13 | 25.46 | 100.0 | 4.88 | 39.2 | 5.60 |
| native_calibrated_on_all845 | 3.95 | 27.78 | 100.0 | 4.89 | 40.0 | 5.50 |
| native_at_anchored_frozen_size | 4.58 | 30.89 | 100.0 | 5.59 | 88.8 | 4.94 |
| anchored_at_native_replay_size | 5.25 | 29.87 | 100.0 | 6.10 | 99.0 | 4.70 |

The guarantee covers the source-label column only. The added-label column is what a deployment would see on the new labels with the frozen threshold; the reference arms show what recalibrating with added-label annotations would cost in set size. The two size-matched rows carry no guarantee: native_at_anchored_frozen_size moves the native threshold to the grid point whose calibration-image set size is closest to the anchored frozen threshold's (same size, native scores), and anchored_at_native_replay_size shrinks the anchored sets to the native replay size; they separate what the scores do from what the set size does.