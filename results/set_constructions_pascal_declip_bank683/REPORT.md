# Set constructions on the same scores: pascal_declip_bank683

2000 Pascal Context validation images (0 without a source-labelled sampled pixel excluded), 59 source labels, 458 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration pascal_declip_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
Rows: construction x arm. Risk = image-level fraction of source-labelled sampled pixels whose label is missing from the set, on the evaluation images; set size = mean labels per labelled pixel at the evaluation vocabulary. logit is the construction used everywhere else in this work (member iff score >= t). softmax, APS and RAPS normalise over the deployed vocabulary, so even anchored scores become candidate-dependent under them; the anchored_frozen row of those constructions is what happens when the score is projective but the set construction is not. Uncalibrated references at the bottom.

## alpha = 0.1

| Construction | Arm | Risk (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| logit | native_source | 9.87 | 0.74 | 42.0 | 1.37 |
| logit | native_frozen | 14.73 | 0.82 | 100.0 | 1.50 |
| logit | native_replay | 9.89 | 0.75 | 41.8 | 2.09 |
| logit | anchored_frozen | 9.90 | 0.76 | 43.8 | 2.41 |
| logit | anchored_replay | 9.90 | 0.76 | 43.8 | 2.41 |
| softmax | native_source | 9.87 | 0.74 | 41.4 | 1.39 |
| softmax | native_frozen | 14.78 | 0.87 | 100.0 | 1.51 |
| softmax | native_replay | 9.81 | 0.76 | 38.4 | 2.20 |
| softmax | anchored_frozen | 14.47 | 0.88 | 100.0 | 1.62 |
| softmax | anchored_replay | 9.81 | 0.73 | 37.4 | 2.36 |
| aps | native_source | 9.88 | 0.74 | 42.8 | 1.44 |
| aps | native_frozen | 13.23 | 0.89 | 100.0 | 1.92 |
| aps | native_replay | 9.85 | 0.75 | 41.8 | 2.73 |
| aps | anchored_frozen | 11.33 | 0.83 | 95.4 | 2.63 |
| aps | anchored_replay | 9.86 | 0.73 | 39.0 | 3.20 |
| raps | native_source | 9.88 | 0.74 | 43.2 | 1.43 |
| raps | native_frozen | 13.41 | 0.86 | 100.0 | 1.82 |
| raps | native_replay | 9.85 | 0.75 | 41.0 | 2.37 |
| raps | anchored_frozen | 11.74 | 0.80 | 99.6 | 2.27 |
| raps | anchored_replay | 9.85 | 0.73 | 39.8 | 2.69 |

## alpha = 0.05

| Construction | Arm | Risk (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| logit | native_source | 4.89 | 0.52 | 39.4 | 1.89 |
| logit | native_frozen | 8.45 | 0.70 | 100.0 | 2.36 |
| logit | native_replay | 4.89 | 0.53 | 38.0 | 3.58 |
| logit | anchored_frozen | 4.89 | 0.53 | 38.0 | 3.84 |
| logit | anchored_replay | 4.89 | 0.53 | 38.0 | 3.84 |
| softmax | native_source | 4.80 | 0.52 | 39.4 | 2.05 |
| softmax | native_frozen | 7.96 | 0.69 | 100.0 | 2.67 |
| softmax | native_replay | 4.56 | 0.59 | 28.8 | 4.55 |
| softmax | anchored_frozen | 7.30 | 0.68 | 100.0 | 3.15 |
| softmax | anchored_replay | 4.65 | 0.57 | 15.8 | 4.85 |
| aps | native_source | 4.85 | 0.50 | 34.4 | 2.24 |
| aps | native_frozen | 6.39 | 0.62 | 99.2 | 4.79 |
| aps | native_replay | 4.79 | 0.53 | 30.6 | 6.92 |
| aps | anchored_frozen | 5.27 | 0.53 | 66.6 | 8.19 |
| aps | anchored_replay | 4.82 | 0.51 | 32.2 | 9.27 |
| raps | native_source | 4.85 | 0.51 | 33.8 | 2.10 |
| raps | native_frozen | 7.34 | 0.60 | 100.0 | 2.97 |
| raps | native_replay | 4.72 | 0.58 | 24.2 | 4.02 |
| raps | anchored_frozen | 6.44 | 0.53 | 99.8 | 3.76 |
| raps | anchored_replay | 4.82 | 0.53 | 33.2 | 4.45 |

## Uncalibrated references (all kept images)

| Scores | Vocabulary | top-1 miss (%) | top-5 miss (%) | softmax >= 0.5: miss (%) | softmax >= 0.5: size |
|---|---|---:|---:|---:|---:|
| native_source | 59 | 18.70 | 1.65 | 20.43 | 0.95 |
| native_full | 458 | 24.32 | 5.50 | 26.97 | 0.91 |
| anchored_full | 59 | 19.51 | 1.72 | 21.40 | 0.94 |
| anchored_full | 458 | 25.13 | 5.89 | 29.45 | 0.87 |

Softmax temperature 1 on the stored logits (float16, clamped to [-30, 30]); RAPS lambda 0.01, k_reg 5, no randomisation. APS/RAPS membership is "mass strictly preceding the label < t" with the crossing label included (conformal.py conventions). CRC on a grid: last feasible index for constructions whose loss grows with the threshold (logit, softmax), first feasible index for APS/RAPS.