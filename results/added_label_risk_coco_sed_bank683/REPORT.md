# Miss risk on the added labels: sed_bank683 (COCO val2017 (LVIS-annotated), 171 -> 1283)

2000 COCO val2017 (LVIS-annotated) images (0 without a source-labelled sampled pixel excluded), 500 random 1000/1000 splits. Sampled pixels: 93.5% carry a source label, 3.1% one of the 1112 added labels (LVIS v1 annotation, no source label), 0.00% a LVIS v1 label outside the 1283 names (ignored); 1300 images have at least one added-label pixel. Risk = image-level fraction of pixels of the population whose true label is missing from the set, averaged over evaluation images that contain the population. Frozen arms calibrate on source-label pixels only; the two reference arms calibrate on all 1283-labelled pixels (they use the added-label annotations, which the deployment setting does not have). Set size over all labelled pixels at 1283 labels. Development data; nothing fitted.

## alpha = 0.1

| Arm | Risk on source labels (%) | Risk on added labels (%) | Splits above alpha on added (%) | Risk on all labels (%) | Splits above alpha on all (%) | Set size at 1283 |
|---|---:|---:|---:|---:|---:|---:|
| anchored_frozen | 9.92 | 41.23 | 100.0 | 10.26 | 64.0 | 3.60 |
| native_frozen | 3.64 | 22.16 | 100.0 | 3.83 | 0.0 | 8.23 |
| native_replay | 9.92 | 41.97 | 100.0 | 10.24 | 63.6 | 3.75 |
| anchored_calibrated_on_all845 | 9.59 | 40.52 | 100.0 | 9.92 | 45.4 | 3.70 |
| native_calibrated_on_all845 | 9.60 | 41.11 | 100.0 | 9.92 | 46.4 | 3.84 |
| native_at_anchored_frozen_size | 10.49 | 43.49 | 100.0 | 10.83 | 86.4 | 3.60 |
| anchored_at_native_replay_size | 9.41 | 40.14 | 100.0 | 9.74 | 34.8 | 3.75 |

## alpha = 0.05

| Arm | Risk on source labels (%) | Risk on added labels (%) | Splits above alpha on added (%) | Risk on all labels (%) | Splits above alpha on all (%) | Set size at 1283 |
|---|---:|---:|---:|---:|---:|---:|
| anchored_frozen | 4.92 | 27.98 | 100.0 | 5.15 | 59.2 | 6.26 |
| native_frozen | 1.62 | 14.07 | 100.0 | 1.76 | 0.0 | 14.69 |
| native_replay | 4.91 | 26.62 | 100.0 | 5.13 | 59.2 | 6.49 |
| anchored_calibrated_on_all845 | 4.69 | 27.11 | 100.0 | 4.92 | 41.4 | 6.49 |
| native_calibrated_on_all845 | 4.70 | 25.95 | 100.0 | 4.91 | 41.0 | 6.73 |
| native_at_anchored_frozen_size | 5.14 | 27.31 | 100.0 | 5.36 | 78.6 | 6.26 |
| anchored_at_native_replay_size | 4.69 | 27.12 | 100.0 | 4.92 | 42.4 | 6.49 |

The guarantee covers the source-label column only. The added-label column is what a deployment would see on the new labels with the frozen threshold; the reference arms show what recalibrating with added-label annotations would cost in set size. The two size-matched rows carry no guarantee: native_at_anchored_frozen_size moves the native threshold to the grid point whose calibration-image set size is closest to the anchored frozen threshold's (same size, native scores), and anchored_at_native_replay_size shrinks the anchored sets to the native replay size; they separate what the scores do from what the set size does.