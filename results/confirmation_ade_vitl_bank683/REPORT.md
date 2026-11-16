# Confirmation run on the reserve: vitl_bank683

1999 reserved ADE training images (1 without a source-labelled sampled pixel excluded), read once. Primary: calibration = first 999 reserve images, evaluation = the rest. Secondary: 500 random 999/1000 splits. Image-level CRC; anchored calibrated at the 150 source labels only.

## primary, alpha = 0.1

| Arm | Mean risk (%) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|
| anchored | 8.42 | 0.0 | 2.42 | 2.71 | 3.15 | 4.31 | 4.55 |
| native_source | 9.04 | 0.0 | 2.00 |  |  |  |  |
| native_frozen_full | 13.77 | 100.0 |  |  |  |  | 2.27 |
| native_replay_full | 8.51 | 0.0 |  |  |  |  | 3.71 |

## primary, alpha = 0.05

| Arm | Mean risk (%) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|
| anchored | 4.52 | 0.0 | 3.80 | 4.41 | 5.42 | 8.15 | 8.82 |
| native_source | 4.03 | 0.0 | 3.50 |  |  |  |  |
| native_frozen_full | 7.03 | 100.0 |  |  |  |  | 4.49 |
| native_replay_full | 4.07 | 0.0 |  |  |  |  | 8.07 |

## secondary, alpha = 0.1

| Arm | Mean risk (%) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|
| anchored | 9.73 | 0.0 | 2.33 | 2.63 | 3.06 | 4.21 | 4.43 |
| native_source | 9.66 | 0.0 | 1.99 |  |  |  |  |
| native_frozen_full | 15.03 | 100.0 |  |  |  |  | 2.26 |
| native_replay_full | 10.13 | 100.0 |  |  |  |  | 3.49 |

## secondary, alpha = 0.05

| Arm | Mean risk (%) | Splits above alpha (%) | +0 | +50 | +150 | +500 | +695 |
|---|---:|---:|---:|---:|---:|---:|---:|
| anchored | 4.68 | 0.0 | 3.83 | 4.50 | 5.58 | 8.41 | 9.11 |
| native_source | 4.72 | 0.0 | 3.39 |  |  |  |  |
| native_frozen_full | 8.28 | 100.0 |  |  |  |  | 4.34 |
| native_replay_full | 5.05 | 100.0 |  |  |  |  | 7.56 |

Ranking on the reserve (source rank, source top-10, expanded rank, expanded top-10): native [1.954, 0.98, 4.025, 0.946], anchored [1.998, 0.979, 4.107, 0.939].
Seconds per image: {'features': 0.147, 'native_150_plus_845': 0.938, 'anchored_reference_plus_845': 2.77}; peak memory 9.42 GB.