# Set constructions on the same scores: pascal_sed_bank683

2000 Pascal Context validation images (0 without a source-labelled sampled pixel excluded), 59 source labels, 458 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration pascal_sed_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
Rows: construction x arm. Risk = image-level fraction of source-labelled sampled pixels whose label is missing from the set, on the evaluation images; set size = mean labels per labelled pixel at the evaluation vocabulary. logit is the construction used everywhere else in this work (member iff score >= t). softmax, APS and RAPS normalise over the deployed vocabulary, so even anchored scores become candidate-dependent under them; the anchored_frozen row of those constructions is what happens when the score is projective but the set construction is not. Uncalibrated references at the bottom.

## alpha = 0.1

| Construction | Arm | Risk (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| logit | native_source | 9.90 | 0.72 | 44.0 | 1.52 |
| logit | native_frozen | 4.65 | 0.43 | 0.0 | 4.79 |
| logit | native_replay | 9.91 | 0.71 | 44.2 | 2.67 |
| logit | anchored_frozen | 9.90 | 0.71 | 44.2 | 2.79 |
| logit | anchored_replay | 9.90 | 0.71 | 44.2 | 2.79 |
| softmax | native_source | 9.90 | 0.73 | 41.2 | 1.52 |
| softmax | native_frozen | 16.50 | 0.74 | 100.0 | 1.54 |
| softmax | native_replay | 9.76 | 0.73 | 30.0 | 2.88 |
| softmax | anchored_frozen | 13.99 | 0.85 | 100.0 | 1.88 |
| softmax | anchored_replay | 9.82 | 0.72 | 36.6 | 2.77 |
| aps | native_source | 9.91 | 0.72 | 41.8 | 1.55 |
| aps | native_frozen | 14.66 | 0.74 | 100.0 | 2.09 |
| aps | native_replay | 9.85 | 0.71 | 40.8 | 3.91 |
| aps | anchored_frozen | 11.38 | 0.81 | 96.2 | 3.19 |
| aps | anchored_replay | 9.87 | 0.72 | 40.6 | 3.94 |
| raps | native_source | 9.91 | 0.72 | 42.6 | 1.55 |
| raps | native_frozen | 14.86 | 0.71 | 100.0 | 1.94 |
| raps | native_replay | 9.86 | 0.71 | 39.2 | 3.01 |
| raps | anchored_frozen | 11.86 | 0.77 | 99.8 | 2.57 |
| raps | anchored_replay | 9.88 | 0.71 | 38.0 | 3.06 |

## alpha = 0.05

| Construction | Arm | Risk (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| logit | native_source | 4.90 | 0.52 | 38.0 | 2.20 |
| logit | native_frozen | 2.07 | 0.28 | 0.0 | 8.43 |
| logit | native_replay | 4.90 | 0.52 | 39.4 | 4.62 |
| logit | anchored_frozen | 4.90 | 0.50 | 40.0 | 4.76 |
| logit | anchored_replay | 4.90 | 0.50 | 40.0 | 4.76 |
| softmax | native_source | 4.83 | 0.53 | 35.6 | 2.23 |
| softmax | native_frozen | 11.08 | 0.66 | 100.0 | 2.49 |
| softmax | native_replay | 4.04 | 0.76 | 22.6 | 6.81 |
| softmax | anchored_frozen | 7.00 | 0.69 | 100.0 | 3.92 |
| softmax | anchored_replay | 4.56 | 0.58 | 16.4 | 5.80 |
| aps | native_source | 4.87 | 0.52 | 33.8 | 2.29 |
| aps | native_frozen | 9.14 | 0.61 | 100.0 | 4.39 |
| aps | native_replay | 4.73 | 0.50 | 24.6 | 10.79 |
| aps | anchored_frozen | 5.04 | 0.54 | 48.8 | 9.85 |
| aps | anchored_replay | 4.81 | 0.50 | 35.8 | 10.38 |
| raps | native_source | 4.88 | 0.52 | 37.0 | 2.26 |
| raps | native_frozen | 10.05 | 0.58 | 100.0 | 2.96 |
| raps | native_replay | 4.50 | 0.57 | 27.4 | 5.66 |
| raps | anchored_frozen | 6.62 | 0.51 | 100.0 | 4.14 |
| raps | anchored_replay | 4.75 | 0.54 | 30.2 | 5.20 |

## Uncalibrated references (all kept images)

| Scores | Vocabulary | top-1 miss (%) | top-5 miss (%) | softmax >= 0.5: miss (%) | softmax >= 0.5: size |
|---|---|---:|---:|---:|---:|
| native_source | 59 | 20.28 | 2.42 | 22.53 | 0.93 |
| native_full | 458 | 26.12 | 6.42 | 28.96 | 0.91 |
| anchored_full | 59 | 20.99 | 2.39 | 22.86 | 0.94 |
| anchored_full | 458 | 26.65 | 6.69 | 30.96 | 0.87 |

Softmax temperature 1 on the stored logits (float16, clamped to [-30, 30]); RAPS lambda 0.01, k_reg 5, no randomisation. APS/RAPS membership is "mass strictly preceding the label < t" with the crossing label included (conformal.py conventions). CRC on a grid: last feasible index for constructions whose loss grows with the threshold (logit, softmax), first feasible index for APS/RAPS.