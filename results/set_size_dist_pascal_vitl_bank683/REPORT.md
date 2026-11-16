# Distribution of the per-pixel set size at the grown vocabulary

2000 Pascal Context validation images, 59 source labels, 458 after growth; 500 random half splits (the splits of results/headroom_splits_pascal_vitl_bank683); thresholds by image-level CRC on the calibration half; distribution over source-labelled sampled pixels of the evaluation half, image-weighted as the mean set size of Tab. 1; mean over splits.

## alpha = 0.1

| Arm | vocabulary | empty (%) | =1 (%) | <=3 (%) | <=10 (%) | >10 (%) | median | p90 | mean | Tab. 1 mean |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_native_source | 59 | 0.2 | 70.7 | 99.2 | 100.0 | 0.0 | 1.0 | 2.0 | 1.37 | 1.37 |
| catseg_native_frozen_full | 458 | 0.5 | 63.6 | 97.8 | 100.0 | 0.0 | 1.0 | 2.7 | 1.49 | 1.49 |
| catseg_native_replay_full | 458 | 0.0 | 47.4 | 85.1 | 100.0 | 0.0 | 2.0 | 4.0 | 2.07 | 2.07 |
| catseg_anchored | 458 | 0.4 | 44.6 | 79.3 | 99.8 | 0.2 | 2.0 | 5.0 | 2.34 | 2.34 |

## alpha = 0.05

| Arm | vocabulary | empty (%) | =1 (%) | <=3 (%) | <=10 (%) | >10 (%) | median | p90 | mean | Tab. 1 mean |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_native_source | 59 | 0.0 | 52.6 | 89.7 | 100.0 | 0.0 | 1.0 | 3.6 | 1.87 | 1.87 |
| catseg_native_frozen_full | 458 | 0.0 | 43.3 | 79.8 | 100.0 | 0.0 | 2.0 | 4.7 | 2.30 | 2.30 |
| catseg_native_replay_full | 458 | 0.0 | 31.1 | 62.4 | 98.1 | 1.9 | 2.8 | 7.1 | 3.38 | 3.38 |
| catseg_anchored | 458 | 0.1 | 30.2 | 61.1 | 96.0 | 4.0 | 2.9 | 7.9 | 3.66 | 3.66 |

Median and p90 are the mean over splits of the per-split quantiles of the evaluation distribution. The `distribution` field of results.json is the split-averaged distribution over set sizes 0..T.