# Distribution of the per-pixel set size at the grown vocabulary

2000 COCO val2017 (LVIS-annotated) images, 171 source labels, 1283 after growth; 500 random half splits (the splits of results/headroom_splits_coco_sed_bank683); thresholds by image-level CRC on the calibration half; distribution over source-labelled sampled pixels of the evaluation half, image-weighted as the mean set size of Tab. 1; mean over splits.

## alpha = 0.1

| Arm | vocabulary | empty (%) | =1 (%) | <=3 (%) | <=10 (%) | >10 (%) | median | p90 | mean | Tab. 1 mean |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_native_source | 171 | 0.1 | 41.2 | 89.6 | 100.0 | 0.0 | 2.0 | 3.6 | 2.01 | 2.01 |
| catseg_native_frozen_full | 1283 | 0.0 | 1.1 | 14.8 | 72.7 | 27.3 | 7.6 | 14.4 | 8.21 | 8.21 |
| catseg_native_replay_full | 1283 | 0.3 | 7.2 | 49.4 | 100.0 | 0.0 | 3.6 | 6.0 | 3.74 | 3.74 |
| catseg_anchored | 1283 | 0.2 | 17.9 | 61.5 | 98.2 | 1.8 | 3.0 | 7.0 | 3.55 | 3.55 |

## alpha = 0.05

| Arm | vocabulary | empty (%) | =1 (%) | <=3 (%) | <=10 (%) | >10 (%) | median | p90 | mean | Tab. 1 mean |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_native_source | 171 | 0.0 | 25.0 | 64.7 | 99.3 | 0.7 | 3.0 | 6.2 | 3.21 | 3.21 |
| catseg_native_frozen_full | 1283 | 0.0 | 0.2 | 5.4 | 38.3 | 61.7 | 13.0 | 26.9 | 14.67 | 14.67 |
| catseg_native_replay_full | 1283 | 0.0 | 2.0 | 20.9 | 88.1 | 11.9 | 6.0 | 10.9 | 6.47 | 6.47 |
| catseg_anchored | 1283 | 0.0 | 7.1 | 34.3 | 84.8 | 15.2 | 5.0 | 12.2 | 6.17 | 6.17 |

Median and p90 are the mean over splits of the per-split quantiles of the evaluation distribution. The `distribution` field of results.json is the split-averaged distribution over set sizes 0..T.