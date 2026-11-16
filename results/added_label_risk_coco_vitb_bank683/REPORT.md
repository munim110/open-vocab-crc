# Miss risk on the added labels: vitb_bank683 (COCO val2017 (LVIS-annotated), 171 -> 1283)

2000 COCO val2017 (LVIS-annotated) images (0 without a source-labelled sampled pixel excluded), 500 random 1000/1000 splits. Sampled pixels: 93.5% carry a source label, 3.1% one of the 1112 added labels (LVIS v1 annotation, no source label), 0.00% a LVIS v1 label outside the 1283 names (ignored); 1300 images have at least one added-label pixel. Risk = image-level fraction of pixels of the population whose true label is missing from the set, averaged over evaluation images that contain the population. Frozen arms calibrate on source-label pixels only; the two reference arms calibrate on all 1283-labelled pixels (they use the added-label annotations, which the deployment setting does not have). Set size over all labelled pixels at 1283 labels. Development data; nothing fitted.

## alpha = 0.1

| Arm | Risk on source labels (%) | Risk on added labels (%) | Splits above alpha on added (%) | Risk on all labels (%) | Splits above alpha on all (%) | Set size at 1283 |
|---|---:|---:|---:|---:|---:|---:|
| anchored_frozen | 9.92 | 38.02 | 100.0 | 10.35 | 67.6 | 3.90 |
| native_frozen | 12.96 | 54.08 | 100.0 | 13.62 | 100.0 | 2.40 |
| native_replay | 9.94 | 45.93 | 100.0 | 10.49 | 74.4 | 3.12 |
| anchored_calibrated_on_all845 | 9.50 | 36.88 | 100.0 | 9.92 | 44.4 | 4.05 |
| native_calibrated_on_all845 | 9.40 | 44.17 | 100.0 | 9.94 | 47.4 | 3.29 |
| native_at_anchored_frozen_size | 7.93 | 38.91 | 100.0 | 8.40 | 0.2 | 3.89 |
| anchored_at_native_replay_size | 12.58 | 44.54 | 100.0 | 13.07 | 100.0 | 3.12 |

## alpha = 0.05

| Arm | Risk on source labels (%) | Risk on added labels (%) | Splits above alpha on added (%) | Risk on all labels (%) | Splits above alpha on all (%) | Set size at 1283 |
|---|---:|---:|---:|---:|---:|---:|
| anchored_frozen | 4.92 | 24.01 | 100.0 | 5.18 | 61.2 | 7.25 |
| native_frozen | 6.96 | 35.81 | 100.0 | 7.38 | 100.0 | 4.40 |
| native_replay | 4.92 | 28.97 | 100.0 | 5.24 | 65.8 | 6.01 |
| anchored_calibrated_on_all845 | 4.66 | 23.28 | 100.0 | 4.92 | 41.8 | 7.56 |
| native_calibrated_on_all845 | 4.61 | 27.69 | 100.0 | 4.92 | 41.0 | 6.37 |
| native_at_anchored_frozen_size | 4.01 | 25.02 | 100.0 | 4.28 | 3.2 | 7.25 |
| anchored_at_native_replay_size | 6.12 | 27.47 | 100.0 | 6.42 | 99.8 | 6.01 |

The guarantee covers the source-label column only. The added-label column is what a deployment would see on the new labels with the frozen threshold; the reference arms show what recalibrating with added-label annotations would cost in set size. The two size-matched rows carry no guarantee: native_at_anchored_frozen_size moves the native threshold to the grid point whose calibration-image set size is closest to the anchored frozen threshold's (same size, native scores), and anchored_at_native_replay_size shrinks the anchored sets to the native replay size; they separate what the scores do from what the set size does.