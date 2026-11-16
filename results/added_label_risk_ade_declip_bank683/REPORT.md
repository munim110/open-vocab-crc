# Miss risk on the added labels: declip_bank683 (ADE validation, 150 -> 845)

2000 ADE validation images (0 without a source-labelled sampled pixel excluded), 500 random 1000/1000 splits. Sampled pixels: 91.6% carry a source label, 6.6% one of the 695 added labels (A-847 annotation, no source label), 0.06% a A-847 label outside the 845 names (ignored); 1367 images have at least one added-label pixel. Risk = image-level fraction of pixels of the population whose true label is missing from the set, averaged over evaluation images that contain the population. Frozen arms calibrate on source-label pixels only; the two reference arms calibrate on all 845-labelled pixels (they use the added-label annotations, which the deployment setting does not have). Set size over all labelled pixels at 845 labels. Development data; nothing fitted.

## alpha = 0.1

| Arm | Risk on source labels (%) | Risk on added labels (%) | Splits above alpha on added (%) | Risk on all labels (%) | Splits above alpha on all (%) | Set size at 845 |
|---|---:|---:|---:|---:|---:|---:|
| anchored_frozen | 9.89 | 27.12 | 100.0 | 10.13 | 55.6 | 4.61 |
| native_frozen | 14.72 | 49.64 | 100.0 | 15.97 | 100.0 | 2.21 |
| native_replay | 9.92 | 36.90 | 100.0 | 10.82 | 88.6 | 3.47 |
| anchored_calibrated_on_all845 | 9.66 | 26.65 | 100.0 | 9.89 | 43.0 | 4.72 |
| native_calibrated_on_all845 | 9.06 | 34.29 | 100.0 | 9.90 | 44.0 | 3.84 |
| native_at_anchored_frozen_size | 7.72 | 29.97 | 100.0 | 8.43 | 0.0 | 4.61 |
| anchored_at_native_replay_size | 13.41 | 34.15 | 100.0 | 13.75 | 100.0 | 3.47 |

## alpha = 0.05

| Arm | Risk on source labels (%) | Risk on added labels (%) | Splits above alpha on added (%) | Risk on all labels (%) | Splits above alpha on all (%) | Set size at 845 |
|---|---:|---:|---:|---:|---:|---:|
| anchored_frozen | 4.89 | 15.69 | 100.0 | 4.98 | 46.8 | 9.21 |
| native_frozen | 7.96 | 30.73 | 100.0 | 8.70 | 100.0 | 4.45 |
| native_replay | 4.91 | 19.97 | 100.0 | 5.22 | 65.6 | 7.81 |
| anchored_calibrated_on_all845 | 4.80 | 15.45 | 100.0 | 4.89 | 39.6 | 9.38 |
| native_calibrated_on_all845 | 4.63 | 18.83 | 100.0 | 4.90 | 41.0 | 8.38 |
| native_at_anchored_frozen_size | 4.27 | 17.42 | 100.0 | 4.50 | 10.6 | 9.20 |
| anchored_at_native_replay_size | 5.80 | 17.89 | 100.0 | 5.89 | 95.4 | 7.81 |

The guarantee covers the source-label column only. The added-label column is what a deployment would see on the new labels with the frozen threshold; the reference arms show what recalibrating with added-label annotations would cost in set size. The two size-matched rows carry no guarantee: native_at_anchored_frozen_size moves the native threshold to the grid point whose calibration-image set size is closest to the anchored frozen threshold's (same size, native scores), and anchored_at_native_replay_size shrinks the anchored sets to the native replay size; they separate what the scores do from what the set size does.