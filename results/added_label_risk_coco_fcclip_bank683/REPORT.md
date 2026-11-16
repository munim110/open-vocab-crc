# Miss risk on the added labels: fcclip_bank683 (COCO val2017 (LVIS-annotated), 171 -> 1283)

2000 COCO val2017 (LVIS-annotated) images (0 without a source-labelled sampled pixel excluded), 500 random 1000/1000 splits. Sampled pixels: 93.5% carry a source label, 3.1% one of the 1112 added labels (LVIS v1 annotation, no source label), 0.00% a LVIS v1 label outside the 1283 names (ignored); 1300 images have at least one added-label pixel. Risk = image-level fraction of pixels of the population whose true label is missing from the set, averaged over evaluation images that contain the population. Frozen arms calibrate on source-label pixels only; the two reference arms calibrate on all 1283-labelled pixels (they use the added-label annotations, which the deployment setting does not have). Set size over all labelled pixels at 1283 labels. Development data; nothing fitted.

## alpha = 0.1

| Arm | Risk on source labels (%) | Risk on added labels (%) | Splits above alpha on added (%) | Risk on all labels (%) | Splits above alpha on all (%) | Set size at 1283 |
|---|---:|---:|---:|---:|---:|---:|
| anchored_frozen | 9.88 | 23.08 | 100.0 | 9.69 | 31.6 | 27.17 |
| native_frozen | 17.09 | 29.35 | 100.0 | 16.81 | 100.0 | 9.76 |
| native_replay | 9.91 | 18.28 | 100.0 | 9.69 | 32.8 | 26.53 |
| anchored_calibrated_on_all845 | 10.06 | 23.41 | 100.0 | 9.88 | 44.4 | 26.30 |
| native_calibrated_on_all845 | 10.11 | 18.66 | 100.0 | 9.90 | 43.2 | 25.43 |
| native_at_anchored_frozen_size | 9.79 | 18.06 | 100.0 | 9.56 | 23.6 | 27.16 |
| anchored_at_native_replay_size | 10.02 | 23.30 | 100.0 | 9.83 | 38.8 | 26.54 |

## alpha = 0.05

| Arm | Risk on source labels (%) | Risk on added labels (%) | Splits above alpha on added (%) | Risk on all labels (%) | Splits above alpha on all (%) | Set size at 1283 |
|---|---:|---:|---:|---:|---:|---:|
| anchored_frozen | 4.90 | 13.36 | 100.0 | 4.80 | 33.4 | 77.90 |
| native_frozen | 9.78 | 18.07 | 100.0 | 9.56 | 100.0 | 27.16 |
| native_replay | 4.89 | 9.40 | 100.0 | 4.76 | 32.0 | 82.73 |
| anchored_calibrated_on_all845 | 5.00 | 13.54 | 100.0 | 4.90 | 38.8 | 76.17 |
| native_calibrated_on_all845 | 5.03 | 9.66 | 100.0 | 4.89 | 41.4 | 79.85 |
| native_at_anchored_frozen_size | 5.13 | 9.84 | 100.0 | 4.99 | 48.4 | 77.86 |
| anchored_at_native_replay_size | 4.65 | 12.94 | 100.0 | 4.56 | 14.8 | 82.77 |

The guarantee covers the source-label column only. The added-label column is what a deployment would see on the new labels with the frozen threshold; the reference arms show what recalibrating with added-label annotations would cost in set size. The two size-matched rows carry no guarantee: native_at_anchored_frozen_size moves the native threshold to the grid point whose calibration-image set size is closest to the anchored frozen threshold's (same size, native scores), and anchored_at_native_replay_size shrinks the anchored sets to the native replay size; they separate what the scores do from what the set size does.