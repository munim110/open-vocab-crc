# Calibrated set sizes from the headroom probe

200 tuning-calibration images select thresholds (image-level CRC); 200 tuning-evaluation images report. Image-averaged sampled-pixel risk and mean labels per pixel. Development data; one split; no fitting.

## alpha = 0.1

| Arm | Calibrated once? | Risk (%) | +0 | +50 | +150 | +500 | +695 |
|---|---|---:|---:|---:|---:|---:|---:|
| sclip_fixed_source | yes | 8.68 | 28.21 | 36.58 | 51.54 | 94.73 | 111.87 |
| catseg_anchored | yes | 9.21 | 3.36 | 4.01 | 4.86 | 7.38 | 7.94 |
| catseg_native_V150 | n/a | 10.51 | 2.30 |  |  |  |  |
| catseg_native_frozen_V845 | yes (invalid) | 16.85 |  |  |  |  | 2.68 |
| catseg_native_replay_V845 | no, replayed | 9.20 |  |  |  |  | 5.58 |

Anchored minus SCLIP fixed-source, paired image bootstrap 95%: risk +0.01 [-0.01, +0.02]; size_plus_0 -24.85 [-25.29, -24.40]; size_plus_50 -32.57 [-33.19, -31.95]; size_plus_150 -46.68 [-47.70, -45.66]; size_plus_500 -87.35 [-89.62, -85.11]; size_plus_695 -103.93 [-106.76, -101.09]

## alpha = 0.05

| Arm | Calibrated once? | Risk (%) | +0 | +50 | +150 | +500 | +695 |
|---|---|---:|---:|---:|---:|---:|---:|
| sclip_fixed_source | yes | 3.69 | 50.11 | 64.51 | 92.03 | 174.59 | 210.75 |
| catseg_anchored | yes | 4.82 | 5.54 | 6.88 | 8.87 | 14.38 | 15.85 |
| catseg_native_V150 | n/a | 4.73 | 4.50 |  |  |  |  |
| catseg_native_frozen_V845 | yes (invalid) | 8.35 |  |  |  |  | 6.36 |
| catseg_native_replay_V845 | no, replayed | 4.58 |  |  |  |  | 12.64 |

Anchored minus SCLIP fixed-source, paired image bootstrap 95%: risk +0.01 [-0.00, +0.03]; size_plus_0 -44.57 [-45.42, -43.69]; size_plus_50 -57.63 [-58.84, -56.48]; size_plus_150 -83.17 [-84.99, -81.39]; size_plus_500 -160.21 [-164.03, -156.47]; size_plus_695 -194.90 [-199.81, -190.12]

Intervals are conditional on this calibration split. Risk columns are in fraction units in the delta line. Native CAT-Seg scores at +695 include its per-crop top-256 truncation. Stored scores are float16 logits clamped to [-30, 30].