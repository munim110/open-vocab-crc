# Set constructions on the same scores: sed_fast8

2000 ADE validation images (0 without a source-labelled sampled pixel excluded), 150 source labels, 845 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration sed_fast8. Development data; nothing is fitted; the confirmation reserve is untouched.
Rows: construction x arm. Risk = image-level fraction of source-labelled sampled pixels whose label is missing from the set, on the evaluation images; set size = mean labels per labelled pixel at the evaluation vocabulary. logit is the construction used everywhere else in this work (member iff score >= t). softmax, APS and RAPS normalise over the deployed vocabulary, so even anchored scores become candidate-dependent under them; the anchored_frozen row of those constructions is what happens when the score is projective but the set construction is not. Uncalibrated references at the bottom.

## alpha = 0.1

| Construction | Arm | Risk (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| logit | native_source | 9.90 | 0.63 | 43.0 | 2.30 |
| logit | native_frozen | 12.84 | 0.73 | 100.0 | 3.54 |
| logit | native_replay | 9.91 | 0.71 | 45.0 | 5.18 |
| logit | anchored_frozen | 9.90 | 0.65 | 45.2 | 6.93 |
| logit | anchored_replay | 9.90 | 0.65 | 45.2 | 6.93 |
| softmax | native_source | 9.87 | 0.62 | 42.4 | 2.25 |
| softmax | native_frozen | 14.77 | 0.80 | 100.0 | 2.82 |
| softmax | native_replay | 9.75 | 0.72 | 38.0 | 5.05 |
| softmax | anchored_frozen | 15.97 | 0.89 | 100.0 | 3.16 |
| softmax | anchored_replay | 9.81 | 0.66 | 32.2 | 6.20 |
| aps | native_source | 9.90 | 0.62 | 41.2 | 2.34 |
| aps | native_frozen | 13.24 | 0.74 | 100.0 | 3.60 |
| aps | native_replay | 9.88 | 0.70 | 42.6 | 5.44 |
| aps | anchored_frozen | 9.72 | 0.63 | 32.2 | 9.85 |
| aps | anchored_replay | 9.91 | 0.64 | 46.2 | 9.52 |
| raps | native_source | 9.90 | 0.62 | 41.4 | 2.32 |
| raps | native_frozen | 13.70 | 0.70 | 100.0 | 3.28 |
| raps | native_replay | 9.88 | 0.68 | 41.6 | 5.18 |
| raps | anchored_frozen | 11.04 | 0.59 | 95.8 | 6.22 |
| raps | anchored_replay | 9.91 | 0.64 | 46.2 | 7.18 |

## alpha = 0.05

| Construction | Arm | Risk (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| logit | native_source | 4.90 | 0.49 | 43.6 | 4.96 |
| logit | native_frozen | 6.98 | 0.55 | 100.0 | 9.27 |
| logit | native_replay | 4.91 | 0.53 | 40.0 | 21.38 |
| logit | anchored_frozen | 4.89 | 0.50 | 43.6 | 15.79 |
| logit | anchored_replay | 4.89 | 0.50 | 43.6 | 15.79 |
| softmax | native_source | 4.65 | 0.55 | 15.8 | 5.18 |
| softmax | native_frozen | 7.38 | 0.75 | 100.0 | 7.96 |
| softmax | native_replay | 0.00 | 0.00 | 0.0 | 845.00 |
| softmax | anchored_frozen | 7.08 | 0.68 | 100.0 | 10.03 |
| softmax | anchored_replay | 4.60 | 0.56 | 16.0 | 20.38 |
| aps | native_source | 4.81 | 0.50 | 43.8 | 5.17 |
| aps | native_frozen | 7.05 | 0.58 | 100.0 | 9.28 |
| aps | native_replay | 0.96 | 2.11 | 17.2 | 702.72 |
| aps | anchored_frozen | 4.39 | 0.44 | 8.2 | 42.05 |
| aps | anchored_replay | 4.89 | 0.47 | 39.0 | 34.06 |
| raps | native_source | 4.88 | 0.48 | 40.6 | 6.20 |
| raps | native_frozen | 8.66 | 0.59 | 100.0 | 7.11 |
| raps | native_replay | 4.90 | 0.52 | 43.2 | 24.81 |
| raps | anchored_frozen | 7.22 | 0.42 | 100.0 | 11.39 |
| raps | anchored_replay | 4.91 | 0.50 | 43.4 | 22.58 |

## Uncalibrated references (all kept images)

| Scores | Vocabulary | top-1 miss (%) | top-5 miss (%) | softmax >= 0.5: miss (%) | softmax >= 0.5: size |
|---|---|---:|---:|---:|---:|
| native_source | 150 | 27.87 | 6.34 | 31.30 | 0.89 |
| native_full | 845 | 33.58 | 12.12 | 39.18 | 0.80 |
| anchored_full | 150 | 29.78 | 6.80 | 37.95 | 0.77 |
| anchored_full | 845 | 36.90 | 14.20 | 56.13 | 0.51 |

Softmax temperature 1 on the stored logits (float16, clamped to [-30, 30]); RAPS lambda 0.01, k_reg 5, no randomisation. APS/RAPS membership is "mass strictly preceding the label < t" with the crossing label included (conformal.py conventions). CRC on a grid: last feasible index for constructions whose loss grows with the threshold (logit, softmax), first feasible index for APS/RAPS.