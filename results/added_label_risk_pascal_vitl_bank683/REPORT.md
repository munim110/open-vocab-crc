# Miss risk on the added labels: vitl_bank683 (Pascal Context validation, 59 -> 458)

2000 Pascal Context validation images (0 without a source-labelled sampled pixel excluded), 500 random 1000/1000 splits. Sampled pixels: 91.8% carry a source label, 5.5% one of the 399 added labels (PC-459 annotation, no source label), 0.00% a PC-459 label outside the 458 names (ignored); 1099 images have at least one added-label pixel. Risk = image-level fraction of pixels of the population whose true label is missing from the set, averaged over evaluation images that contain the population. Frozen arms calibrate on source-label pixels only; the two reference arms calibrate on all 458-labelled pixels (they use the added-label annotations, which the deployment setting does not have). Set size over all labelled pixels at 458 labels. Development data; nothing fitted.

## alpha = 0.1

| Arm | Risk on source labels (%) | Risk on added labels (%) | Splits above alpha on added (%) | Risk on all labels (%) | Splits above alpha on all (%) | Set size at 458 |
|---|---:|---:|---:|---:|---:|---:|
| anchored_frozen | 9.90 | 30.65 | 100.0 | 10.82 | 86.6 | 2.45 |
| native_frozen | 15.05 | 55.16 | 100.0 | 16.74 | 100.0 | 1.51 |
| native_replay | 9.88 | 40.63 | 100.0 | 11.23 | 95.4 | 2.12 |
| anchored_calibrated_on_all845 | 9.00 | 28.77 | 100.0 | 9.88 | 40.4 | 2.61 |
| native_calibrated_on_all845 | 8.65 | 36.54 | 100.0 | 9.88 | 41.0 | 2.35 |
| native_at_anchored_frozen_size | 8.16 | 34.93 | 100.0 | 9.34 | 14.0 | 2.45 |
| anchored_at_native_replay_size | 12.33 | 35.63 | 100.0 | 13.33 | 100.0 | 2.12 |

## alpha = 0.05

| Arm | Risk on source labels (%) | Risk on added labels (%) | Splits above alpha on added (%) | Risk on all labels (%) | Splits above alpha on all (%) | Set size at 458 |
|---|---:|---:|---:|---:|---:|---:|
| anchored_frozen | 4.89 | 18.85 | 100.0 | 5.54 | 85.2 | 3.89 |
| native_frozen | 8.56 | 36.26 | 100.0 | 9.78 | 100.0 | 2.37 |
| native_replay | 4.91 | 23.62 | 100.0 | 5.79 | 93.8 | 3.51 |
| anchored_calibrated_on_all845 | 4.27 | 17.13 | 100.0 | 4.88 | 37.2 | 4.27 |
| native_calibrated_on_all845 | 4.10 | 20.78 | 100.0 | 4.89 | 41.6 | 4.00 |
| native_at_anchored_frozen_size | 4.24 | 21.33 | 100.0 | 5.06 | 56.2 | 3.90 |
| anchored_at_native_replay_size | 5.71 | 21.17 | 100.0 | 6.41 | 99.4 | 3.50 |

The guarantee covers the source-label column only. The added-label column is what a deployment would see on the new labels with the frozen threshold; the reference arms show what recalibrating with added-label annotations would cost in set size. The two size-matched rows carry no guarantee: native_at_anchored_frozen_size moves the native threshold to the grid point whose calibration-image set size is closest to the anchored frozen threshold's (same size, native scores), and anchored_at_native_replay_size shrinks the anchored sets to the native replay size; they separate what the scores do from what the set size does.