# Miss risk on the added labels: declip_bank683 (COCO val2017 (LVIS-annotated), 171 -> 1283)

2000 COCO val2017 (LVIS-annotated) images (0 without a source-labelled sampled pixel excluded), 500 random 1000/1000 splits. Sampled pixels: 93.5% carry a source label, 3.1% one of the 1112 added labels (LVIS v1 annotation, no source label), 0.00% a LVIS v1 label outside the 1283 names (ignored); 1300 images have at least one added-label pixel. Risk = image-level fraction of pixels of the population whose true label is missing from the set, averaged over evaluation images that contain the population. Frozen arms calibrate on source-label pixels only; the two reference arms calibrate on all 1283-labelled pixels (they use the added-label annotations, which the deployment setting does not have). Set size over all labelled pixels at 1283 labels. Development data; nothing fitted.

## alpha = 0.1

| Arm | Risk on source labels (%) | Risk on added labels (%) | Splits above alpha on added (%) | Risk on all labels (%) | Splits above alpha on all (%) | Set size at 1283 |
|---|---:|---:|---:|---:|---:|---:|
| anchored_frozen | 9.90 | 25.22 | 100.0 | 9.99 | 48.4 | 3.25 |
| native_frozen | 12.93 | 38.61 | 100.0 | 13.15 | 100.0 | 2.08 |
| native_replay | 9.94 | 30.81 | 100.0 | 10.08 | 55.0 | 2.65 |
| anchored_calibrated_on_all845 | 9.82 | 25.02 | 100.0 | 9.90 | 42.4 | 3.27 |
| native_calibrated_on_all845 | 9.81 | 30.40 | 100.0 | 9.94 | 46.0 | 2.68 |
| native_at_anchored_frozen_size | 7.83 | 24.69 | 100.0 | 7.90 | 0.0 | 3.25 |
| anchored_at_native_replay_size | 12.94 | 31.65 | 100.0 | 13.07 | 100.0 | 2.65 |

## alpha = 0.05

| Arm | Risk on source labels (%) | Risk on added labels (%) | Splits above alpha on added (%) | Risk on all labels (%) | Splits above alpha on all (%) | Set size at 1283 |
|---|---:|---:|---:|---:|---:|---:|
| anchored_frozen | 4.92 | 13.44 | 100.0 | 4.95 | 44.8 | 5.78 |
| native_frozen | 6.83 | 22.37 | 100.0 | 6.90 | 100.0 | 3.64 |
| native_replay | 4.92 | 15.78 | 100.0 | 4.95 | 45.6 | 4.88 |
| anchored_calibrated_on_all845 | 4.90 | 13.38 | 100.0 | 4.92 | 43.2 | 5.80 |
| native_calibrated_on_all845 | 4.88 | 15.68 | 100.0 | 4.92 | 45.0 | 4.91 |
| native_at_anchored_frozen_size | 4.04 | 13.17 | 100.0 | 4.07 | 1.0 | 5.78 |
| anchored_at_native_replay_size | 6.02 | 16.22 | 100.0 | 6.06 | 97.2 | 4.88 |

The guarantee covers the source-label column only. The added-label column is what a deployment would see on the new labels with the frozen threshold; the reference arms show what recalibrating with added-label annotations would cost in set size. The two size-matched rows carry no guarantee: native_at_anchored_frozen_size moves the native threshold to the grid point whose calibration-image set size is closest to the anchored frozen threshold's (same size, native scores), and anchored_at_native_replay_size shrinks the anchored sets to the native replay size; they separate what the scores do from what the set size does.