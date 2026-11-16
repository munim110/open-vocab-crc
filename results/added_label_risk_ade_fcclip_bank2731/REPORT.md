# Miss risk on the added labels: fcclip_bank2731

2000 ADE validation images (0 without a source-labelled sampled pixel excluded), 500 random 1000/1000 splits. Sampled pixels: 91.6% carry a source label, 6.6% one of the 695 added labels (A-847 annotation, no source label), 0.06% an A-847 label outside the 845 names (ignored); 1367 images have at least one added-label pixel. Risk = image-level fraction of pixels of the population whose true label is missing from the set, averaged over evaluation images that contain the population. Frozen arms calibrate on source-label pixels only; the two reference arms calibrate on all 845-labelled pixels (they use the added-label annotations, which the deployment setting does not have). Set size over all labelled pixels at 845 labels. Development data; nothing fitted.

## alpha = 0.1

| Arm | Risk on source labels (%) | Risk on added labels (%) | Splits above alpha on added (%) | Risk on all labels (%) | Splits above alpha on all (%) | Set size at 845 |
|---|---:|---:|---:|---:|---:|---:|
| anchored_frozen | 9.88 | 29.23 | 100.0 | 9.96 | 47.8 | 11.01 |
| native_frozen | 13.81 | 43.00 | 100.0 | 14.22 | 100.0 | 5.22 |
| native_replay | 9.89 | 34.46 | 100.0 | 10.20 | 63.2 | 8.21 |
| anchored_calibrated_on_all845 | 9.80 | 29.09 | 100.0 | 9.88 | 41.4 | 11.13 |
| native_calibrated_on_all845 | 9.59 | 33.70 | 100.0 | 9.88 | 44.0 | 8.58 |
| native_at_anchored_frozen_size | 8.08 | 30.08 | 100.0 | 8.31 | 0.2 | 11.01 |
| anchored_at_native_replay_size | 12.46 | 33.52 | 100.0 | 12.54 | 100.0 | 8.21 |

## alpha = 0.05

| Arm | Risk on source labels (%) | Risk on added labels (%) | Splits above alpha on added (%) | Risk on all labels (%) | Splits above alpha on all (%) | Set size at 845 |
|---|---:|---:|---:|---:|---:|---:|
| anchored_frozen | 4.91 | 18.04 | 100.0 | 5.02 | 53.0 | 30.14 |
| native_frozen | 6.78 | 26.54 | 100.0 | 7.00 | 100.0 | 14.47 |
| native_replay | 4.90 | 20.44 | 100.0 | 5.01 | 51.0 | 25.43 |
| anchored_calibrated_on_all845 | 4.81 | 17.66 | 100.0 | 4.91 | 44.4 | 31.33 |
| native_calibrated_on_all845 | 4.79 | 20.03 | 100.0 | 4.90 | 40.2 | 26.43 |
| native_at_anchored_frozen_size | 4.46 | 18.66 | 100.0 | 4.53 | 14.4 | 30.13 |
| anchored_at_native_replay_size | 5.43 | 19.83 | 100.0 | 5.55 | 85.2 | 25.43 |

The guarantee covers the source-label column only. The added-label column is what a deployment would see on the new labels with the frozen threshold; the reference arms show what recalibrating with added-label annotations would cost in set size. The two size-matched rows carry no guarantee: native_at_anchored_frozen_size moves the native threshold to the grid point whose calibration-image set size is closest to the anchored frozen threshold's (same size, native scores), and anchored_at_native_replay_size shrinks the anchored sets to the native replay size; they separate what the scores do from what the set size does.