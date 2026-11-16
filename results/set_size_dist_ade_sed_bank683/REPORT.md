# Distribution of the per-pixel set size at the grown vocabulary

2000 ADE validation images, 150 source labels, 845 after growth; 500 random half splits (the splits of results/headroom_splits_ade_sed_bank683); thresholds by image-level CRC on the calibration half; distribution over source-labelled sampled pixels of the evaluation half, image-weighted as the mean set size of Tab. 1; mean over splits.

## alpha = 0.1

| Arm | vocabulary | empty (%) | =1 (%) | <=3 (%) | <=10 (%) | >10 (%) | median | p90 | mean | Tab. 1 mean |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_native_source | 150 | 0.1 | 38.9 | 83.3 | 100.0 | 0.0 | 2.0 | 4.0 | 2.22 | 2.22 |
| catseg_native_frozen_full | 845 | 0.0 | 5.9 | 15.2 | 67.0 | 33.0 | 8.1 | 15.7 | 8.80 | 8.80 |
| catseg_native_replay_full | 845 | 0.0 | 10.5 | 29.8 | 95.2 | 4.8 | 5.0 | 9.1 | 5.28 | 5.28 |
| catseg_anchored | 845 | 0.1 | 19.4 | 39.7 | 82.9 | 17.1 | 4.9 | 13.0 | 6.05 | 6.05 |

## alpha = 0.05

| Arm | vocabulary | empty (%) | =1 (%) | <=3 (%) | <=10 (%) | >10 (%) | median | p90 | mean | Tab. 1 mean |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_native_source | 150 | 0.0 | 14.8 | 43.6 | 93.9 | 6.1 | 4.0 | 9.2 | 4.71 | 4.71 |
| catseg_native_frozen_full | 845 | 0.0 | 0.2 | 1.9 | 15.7 | 84.3 | 22.1 | 45.4 | 24.84 | 24.84 |
| catseg_native_replay_full | 845 | 0.0 | 1.9 | 5.9 | 32.0 | 68.0 | 14.6 | 29.4 | 16.19 | 16.19 |
| catseg_anchored | 845 | 0.0 | 7.2 | 16.5 | 44.4 | 55.6 | 12.0 | 34.2 | 15.62 | 15.62 |

Median and p90 are the mean over splits of the per-split quantiles of the evaluation distribution. The `distribution` field of results.json is the split-averaged distribution over set sizes 0..T.