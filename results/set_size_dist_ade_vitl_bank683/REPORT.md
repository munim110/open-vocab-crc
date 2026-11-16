# Distribution of the per-pixel set size at the grown vocabulary

2000 ADE validation images, 150 source labels, 845 after growth; 500 random half splits (the splits of results/headroom_splits_ade_vitl_bank683); thresholds by image-level CRC on the calibration half; distribution over source-labelled sampled pixels of the evaluation half, image-weighted as the mean set size of Tab. 1; mean over splits.

## alpha = 0.1

| Arm | vocabulary | empty (%) | =1 (%) | <=3 (%) | <=10 (%) | >10 (%) | median | p90 | mean | Tab. 1 mean |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_native_source | 150 | 0.2 | 46.6 | 90.5 | 100.0 | 0.0 | 2.0 | 3.3 | 1.91 | 1.91 |
| catseg_native_frozen_full | 845 | 0.3 | 38.0 | 85.5 | 100.0 | 0.0 | 2.0 | 4.0 | 2.16 | 2.16 |
| catseg_native_replay_full | 845 | 0.0 | 22.1 | 58.0 | 99.4 | 0.6 | 3.0 | 6.7 | 3.47 | 3.47 |
| catseg_anchored | 845 | 0.3 | 23.5 | 51.8 | 94.5 | 5.5 | 3.1 | 9.0 | 4.27 | 4.27 |

## alpha = 0.05

| Arm | vocabulary | empty (%) | =1 (%) | <=3 (%) | <=10 (%) | >10 (%) | median | p90 | mean | Tab. 1 mean |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| catseg_native_source | 150 | 0.0 | 23.9 | 62.4 | 99.4 | 0.6 | 3.0 | 6.3 | 3.28 | 3.28 |
| catseg_native_frozen_full | 845 | 0.0 | 17.0 | 48.4 | 97.0 | 3.0 | 3.8 | 8.1 | 4.21 | 4.21 |
| catseg_native_replay_full | 845 | 0.0 | 6.5 | 23.5 | 74.2 | 25.8 | 6.7 | 15.3 | 7.81 | 7.81 |
| catseg_anchored | 845 | 0.0 | 11.0 | 27.9 | 69.1 | 30.9 | 7.0 | 18.3 | 8.63 | 8.63 |

Median and p90 are the mean over splits of the per-split quantiles of the evaluation distribution. The `distribution` field of results.json is the split-averaged distribution over set sizes 0..T.