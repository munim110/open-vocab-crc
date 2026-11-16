# Miss risk on the added labels: declip_bank683 (Pascal Context validation, 59 -> 458)

2000 Pascal Context validation images (0 without a source-labelled sampled pixel excluded), 500 random 1000/1000 splits. Sampled pixels: 91.8% carry a source label, 5.5% one of the 399 added labels (PC-459 annotation, no source label), 0.00% a PC-459 label outside the 458 names (ignored); 1099 images have at least one added-label pixel. Risk = image-level fraction of pixels of the population whose true label is missing from the set, averaged over evaluation images that contain the population. Frozen arms calibrate on source-label pixels only; the two reference arms calibrate on all 458-labelled pixels (they use the added-label annotations, which the deployment setting does not have). Set size over all labelled pixels at 458 labels. Development data; nothing fitted.

## alpha = 0.1

| Arm | Risk on source labels (%) | Risk on added labels (%) | Splits above alpha on added (%) | Risk on all labels (%) | Splits above alpha on all (%) | Set size at 458 |
|---|---:|---:|---:|---:|---:|---:|
| anchored_frozen | 9.90 | 22.61 | 100.0 | 10.50 | 73.6 | 2.57 |
| native_frozen | 14.73 | 47.18 | 100.0 | 16.13 | 100.0 | 1.53 |
| native_replay | 9.89 | 32.71 | 100.0 | 10.96 | 90.4 | 2.15 |
| anchored_calibrated_on_all845 | 9.30 | 21.60 | 100.0 | 9.89 | 41.0 | 2.68 |
| native_calibrated_on_all845 | 8.87 | 29.92 | 100.0 | 9.88 | 40.6 | 2.35 |
| native_at_anchored_frozen_size | 7.91 | 27.20 | 100.0 | 8.84 | 4.2 | 2.57 |
| anchored_at_native_replay_size | 12.84 | 27.68 | 100.0 | 13.51 | 100.0 | 2.15 |

## alpha = 0.05

| Arm | Risk on source labels (%) | Risk on added labels (%) | Splits above alpha on added (%) | Risk on all labels (%) | Splits above alpha on all (%) | Set size at 458 |
|---|---:|---:|---:|---:|---:|---:|
| anchored_frozen | 4.89 | 13.94 | 100.0 | 5.34 | 75.0 | 4.11 |
| native_frozen | 8.45 | 28.74 | 100.0 | 9.43 | 100.0 | 2.44 |
| native_replay | 4.89 | 18.49 | 100.0 | 5.61 | 89.4 | 3.73 |
| anchored_calibrated_on_all845 | 4.44 | 13.00 | 100.0 | 4.88 | 40.0 | 4.40 |
| native_calibrated_on_all845 | 4.23 | 16.65 | 100.0 | 4.89 | 36.2 | 4.15 |
| native_at_anchored_frozen_size | 4.28 | 16.79 | 100.0 | 4.95 | 41.8 | 4.11 |
| anchored_at_native_replay_size | 5.64 | 15.43 | 100.0 | 6.12 | 97.6 | 3.73 |

The guarantee covers the source-label column only. The added-label column is what a deployment would see on the new labels with the frozen threshold; the reference arms show what recalibrating with added-label annotations would cost in set size. The two size-matched rows carry no guarantee: native_at_anchored_frozen_size moves the native threshold to the grid point whose calibration-image set size is closest to the anchored frozen threshold's (same size, native scores), and anchored_at_native_replay_size shrinks the anchored sets to the native replay size; they separate what the scores do from what the set size does.