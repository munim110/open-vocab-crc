# Distribution of the per-pixel set size at the grown vocabulary

2000 Pascal Context validation images, 59 source labels, 458 after growth; 500 random half splits (the splits of results/headroom_splits_pascal_sed_bank683); thresholds by image-level CRC on the calibration half; distribution over source-labelled sampled pixels of the evaluation half, image-weighted as the mean set size of Tab. 1; mean over splits.

## alpha = 0.1

| Arm | vocabulary | empty (%) | =1 (%) | <=3 (%) | <=10 (%) | >10 (%) | median | p90 | mean | Tab. 1 mean |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_native_source | 59 | 0.1 | 62.7 | 97.2 | 100.0 | 0.0 | 1.0 | 3.0 | 1.53 | 1.53 |
| catseg_native_frozen_full | 458 | 0.0 | 7.5 | 36.0 | 95.8 | 4.2 | 4.1 | 8.6 | 4.80 | 4.80 |
| catseg_native_replay_full | 458 | 0.2 | 17.6 | 77.2 | 100.0 | 0.0 | 2.5 | 4.2 | 2.68 | 2.68 |
| catseg_anchored | 458 | 0.8 | 27.0 | 72.2 | 99.6 | 0.4 | 2.0 | 5.2 | 2.80 | 2.80 |

## alpha = 0.05

| Arm | vocabulary | empty (%) | =1 (%) | <=3 (%) | <=10 (%) | >10 (%) | median | p90 | mean | Tab. 1 mean |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_native_source | 59 | 0.0 | 42.4 | 82.9 | 100.0 | 0.0 | 2.0 | 4.0 | 2.20 | 2.20 |
| catseg_native_frozen_full | 458 | 0.0 | 3.0 | 16.3 | 72.4 | 27.6 | 7.0 | 16.1 | 8.45 | 8.45 |
| catseg_native_replay_full | 458 | 0.0 | 7.9 | 37.9 | 96.7 | 3.3 | 4.0 | 8.2 | 4.63 | 4.63 |
| catseg_anchored | 458 | 0.3 | 12.2 | 44.1 | 93.3 | 6.7 | 4.0 | 9.3 | 4.77 | 4.77 |

Median and p90 are the mean over splits of the per-split quantiles of the evaluation distribution. The `distribution` field of results.json is the split-averaged distribution over set sizes 0..T.