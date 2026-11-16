# Miss risk on the added labels: anchored_vitb_distract_near

2000 ADE validation images (0 without a source-labelled sampled pixel excluded), 500 random 1000/1000 splits. Sampled pixels: 91.6% carry a source label, 6.6% one of the 695 added labels (A-847 annotation, no source label), 0.06% an A-847 label outside the 845 names (ignored); 1367 images have at least one added-label pixel. Risk = image-level fraction of pixels of the population whose true label is missing from the set, averaged over evaluation images that contain the population. Frozen arms calibrate on source-label pixels only; the two reference arms calibrate on all 845-labelled pixels (they use the added-label annotations, which the deployment setting does not have). Set size over all labelled pixels at 845 labels. Development data; nothing fitted.

## alpha = 0.1

| Arm | Risk on source labels (%) | Risk on added labels (%) | Splits above alpha on added (%) | Risk on all labels (%) | Splits above alpha on all (%) | Set size at 845 |
|---|---:|---:|---:|---:|---:|---:|
| anchored_frozen | 9.89 | 44.89 | 100.0 | 11.35 | 98.0 | 6.49 |
| native_frozen | 12.90 | 53.48 | 100.0 | 14.48 | 100.0 | 4.12 |
| native_replay | 9.88 | 46.48 | 100.0 | 11.28 | 97.4 | 5.62 |
| anchored_calibrated_on_all845 | 8.58 | 40.39 | 100.0 | 9.88 | 42.2 | 7.80 |
| native_calibrated_on_all845 | 8.56 | 42.79 | 100.0 | 9.87 | 44.8 | 6.65 |
| native_at_anchored_frozen_size | 8.74 | 43.29 | 100.0 | 10.05 | 55.0 | 6.50 |
| anchored_at_native_replay_size | 11.06 | 48.40 | 100.0 | 12.64 | 100.0 | 5.62 |

## alpha = 0.05

| Arm | Risk on source labels (%) | Risk on added labels (%) | Splits above alpha on added (%) | Risk on all labels (%) | Splits above alpha on all (%) | Set size at 845 |
|---|---:|---:|---:|---:|---:|---:|
| anchored_frozen | 4.89 | 27.25 | 100.0 | 5.69 | 93.2 | 15.38 |
| native_frozen | 7.07 | 37.86 | 100.0 | 8.22 | 100.0 | 8.36 |
| native_replay | 4.90 | 29.22 | 100.0 | 5.79 | 94.0 | 13.15 |
| anchored_calibrated_on_all845 | 4.16 | 24.49 | 100.0 | 4.87 | 37.8 | 18.37 |
| native_calibrated_on_all845 | 4.12 | 25.47 | 100.0 | 4.88 | 39.2 | 16.65 |
| native_at_anchored_frozen_size | 4.36 | 26.62 | 100.0 | 5.16 | 67.2 | 15.38 |
| anchored_at_native_replay_size | 5.59 | 29.91 | 100.0 | 6.50 | 100.0 | 13.15 |

The guarantee covers the source-label column only. The added-label column is what a deployment would see on the new labels with the frozen threshold; the reference arms show what recalibrating with added-label annotations would cost in set size. The two size-matched rows carry no guarantee: native_at_anchored_frozen_size moves the native threshold to the grid point whose calibration-image set size is closest to the anchored frozen threshold's (same size, native scores), and anchored_at_native_replay_size shrinks the anchored sets to the native replay size; they separate what the scores do from what the set size does.