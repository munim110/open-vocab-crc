# Miss risk on the added labels: vitl_bank683 (COCO val2017 (LVIS-annotated), 171 -> 1283)

2000 COCO val2017 (LVIS-annotated) images (0 without a source-labelled sampled pixel excluded), 500 random 1000/1000 splits. Sampled pixels: 93.5% carry a source label, 3.1% one of the 1112 added labels (LVIS v1 annotation, no source label), 0.00% a LVIS v1 label outside the 1283 names (ignored); 1300 images have at least one added-label pixel. Risk = image-level fraction of pixels of the population whose true label is missing from the set, averaged over evaluation images that contain the population. Frozen arms calibrate on source-label pixels only; the two reference arms calibrate on all 1283-labelled pixels (they use the added-label annotations, which the deployment setting does not have). Set size over all labelled pixels at 1283 labels. Development data; nothing fitted.

## alpha = 0.1

| Arm | Risk on source labels (%) | Risk on added labels (%) | Splits above alpha on added (%) | Risk on all labels (%) | Splits above alpha on all (%) | Set size at 1283 |
|---|---:|---:|---:|---:|---:|---:|
| anchored_frozen | 9.92 | 30.19 | 100.0 | 10.23 | 64.0 | 3.26 |
| native_frozen | 12.88 | 46.44 | 100.0 | 13.33 | 100.0 | 2.14 |
| native_replay | 9.95 | 38.95 | 100.0 | 10.33 | 67.2 | 2.67 |
| anchored_calibrated_on_all845 | 9.61 | 29.45 | 100.0 | 9.92 | 46.0 | 3.35 |
| native_calibrated_on_all845 | 9.57 | 37.96 | 100.0 | 9.94 | 44.8 | 2.76 |
| native_at_anchored_frozen_size | 7.91 | 33.21 | 100.0 | 8.25 | 0.0 | 3.26 |
| anchored_at_native_replay_size | 12.72 | 36.60 | 100.0 | 13.11 | 100.0 | 2.67 |

## alpha = 0.05

| Arm | Risk on source labels (%) | Risk on added labels (%) | Splits above alpha on added (%) | Risk on all labels (%) | Splits above alpha on all (%) | Set size at 1283 |
|---|---:|---:|---:|---:|---:|---:|
| anchored_frozen | 4.90 | 17.74 | 100.0 | 5.07 | 53.4 | 5.85 |
| native_frozen | 7.02 | 30.52 | 100.0 | 7.33 | 100.0 | 3.62 |
| native_replay | 4.92 | 23.28 | 100.0 | 5.13 | 56.4 | 4.93 |
| anchored_calibrated_on_all845 | 4.74 | 17.25 | 100.0 | 4.90 | 44.4 | 6.01 |
| native_calibrated_on_all845 | 4.72 | 22.46 | 100.0 | 4.92 | 42.8 | 5.11 |
| native_at_anchored_frozen_size | 4.04 | 19.61 | 100.0 | 4.21 | 4.2 | 5.85 |
| anchored_at_native_replay_size | 6.05 | 20.87 | 100.0 | 6.27 | 98.8 | 4.93 |

The guarantee covers the source-label column only. The added-label column is what a deployment would see on the new labels with the frozen threshold; the reference arms show what recalibrating with added-label annotations would cost in set size. The two size-matched rows carry no guarantee: native_at_anchored_frozen_size moves the native threshold to the grid point whose calibration-image set size is closest to the anchored frozen threshold's (same size, native scores), and anchored_at_native_replay_size shrinks the anchored sets to the native replay size; they separate what the scores do from what the set size does.