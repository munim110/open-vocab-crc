# Miss risk on the added labels: fcclip_bank683 (Pascal Context validation, 59 -> 458)

2000 Pascal Context validation images (0 without a source-labelled sampled pixel excluded), 500 random 1000/1000 splits. Sampled pixels: 91.8% carry a source label, 5.5% one of the 399 added labels (PC-459 annotation, no source label), 0.00% a PC-459 label outside the 458 names (ignored); 1099 images have at least one added-label pixel. Risk = image-level fraction of pixels of the population whose true label is missing from the set, averaged over evaluation images that contain the population. Frozen arms calibrate on source-label pixels only; the two reference arms calibrate on all 458-labelled pixels (they use the added-label annotations, which the deployment setting does not have). Set size over all labelled pixels at 458 labels. Development data; nothing fitted.

## alpha = 0.1

| Arm | Risk on source labels (%) | Risk on added labels (%) | Splits above alpha on added (%) | Risk on all labels (%) | Splits above alpha on all (%) | Set size at 458 |
|---|---:|---:|---:|---:|---:|---:|
| anchored_frozen | 9.89 | 36.48 | 100.0 | 10.82 | 87.6 | 6.07 |
| native_frozen | 16.25 | 49.90 | 100.0 | 17.52 | 100.0 | 2.89 |
| native_replay | 9.86 | 37.01 | 100.0 | 10.97 | 91.2 | 5.44 |
| anchored_calibrated_on_all845 | 9.01 | 34.23 | 100.0 | 9.88 | 42.8 | 6.89 |
| native_calibrated_on_all845 | 8.81 | 34.34 | 100.0 | 9.86 | 41.0 | 6.28 |
| native_at_anchored_frozen_size | 9.03 | 34.92 | 100.0 | 10.10 | 52.0 | 6.08 |
| anchored_at_native_replay_size | 10.73 | 38.67 | 100.0 | 11.71 | 99.4 | 5.43 |

## alpha = 0.05

| Arm | Risk on source labels (%) | Risk on added labels (%) | Splits above alpha on added (%) | Risk on all labels (%) | Splits above alpha on all (%) | Set size at 458 |
|---|---:|---:|---:|---:|---:|---:|
| anchored_frozen | 4.88 | 22.78 | 100.0 | 5.57 | 84.2 | 14.54 |
| native_frozen | 8.56 | 33.65 | 100.0 | 9.60 | 100.0 | 6.52 |
| native_replay | 4.87 | 22.82 | 100.0 | 5.63 | 88.2 | 13.02 |
| anchored_calibrated_on_all845 | 4.22 | 20.57 | 100.0 | 4.88 | 40.6 | 17.06 |
| native_calibrated_on_all845 | 4.19 | 20.68 | 100.0 | 4.89 | 40.4 | 15.81 |
| native_at_anchored_frozen_size | 4.45 | 21.52 | 100.0 | 5.18 | 64.8 | 14.54 |
| anchored_at_native_replay_size | 5.40 | 24.34 | 100.0 | 6.10 | 98.2 | 13.01 |

The guarantee covers the source-label column only. The added-label column is what a deployment would see on the new labels with the frozen threshold; the reference arms show what recalibrating with added-label annotations would cost in set size. The two size-matched rows carry no guarantee: native_at_anchored_frozen_size moves the native threshold to the grid point whose calibration-image set size is closest to the anchored frozen threshold's (same size, native scores), and anchored_at_native_replay_size shrinks the anchored sets to the native replay size; they separate what the scores do from what the set size does.