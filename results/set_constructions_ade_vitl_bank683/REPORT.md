# Set constructions on the same scores: vitl_bank683

2000 ADE validation images (0 without a source-labelled sampled pixel excluded), 150 source labels, 845 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration vitl_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
Rows: construction x arm. Risk = image-level fraction of source-labelled sampled pixels whose label is missing from the set, on the evaluation images; set size = mean labels per labelled pixel at the evaluation vocabulary. logit is the construction used everywhere else in this work (member iff score >= t). softmax, APS and RAPS normalise over the deployed vocabulary, so even anchored scores become candidate-dependent under them; the anchored_frozen row of those constructions is what happens when the score is projective but the set construction is not. Uncalibrated references at the bottom.

## alpha = 0.1

| Construction | Arm | Risk (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| logit | native_source | 9.90 | 0.59 | 39.4 | 1.91 |
| logit | native_frozen | 15.22 | 0.74 | 100.0 | 2.16 |
| logit | native_replay | 9.91 | 0.64 | 43.2 | 3.47 |
| logit | anchored_frozen | 9.88 | 0.64 | 41.0 | 4.27 |
| logit | anchored_replay | 9.88 | 0.64 | 41.0 | 4.27 |
| softmax | native_source | 9.87 | 0.57 | 38.6 | 1.99 |
| softmax | native_frozen | 14.37 | 0.72 | 100.0 | 2.38 |
| softmax | native_replay | 9.82 | 0.64 | 41.0 | 3.76 |
| softmax | anchored_frozen | 14.83 | 0.77 | 100.0 | 2.50 |
| softmax | anchored_replay | 9.83 | 0.63 | 38.2 | 4.22 |
| aps | native_source | 9.90 | 0.59 | 43.0 | 2.27 |
| aps | native_frozen | 12.33 | 0.68 | 100.0 | 3.69 |
| aps | native_replay | 9.91 | 0.65 | 42.0 | 5.04 |
| aps | anchored_frozen | 10.19 | 0.63 | 62.0 | 6.72 |
| aps | anchored_replay | 9.93 | 0.63 | 46.0 | 7.00 |
| raps | native_source | 9.91 | 0.59 | 41.8 | 2.18 |
| raps | native_frozen | 12.84 | 0.65 | 100.0 | 3.09 |
| raps | native_replay | 9.91 | 0.64 | 43.4 | 4.03 |
| raps | anchored_frozen | 11.18 | 0.59 | 98.2 | 4.52 |
| raps | anchored_replay | 9.93 | 0.63 | 47.6 | 5.14 |

## alpha = 0.05

| Construction | Arm | Risk (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| logit | native_source | 4.89 | 0.44 | 35.8 | 3.28 |
| logit | native_frozen | 8.38 | 0.60 | 100.0 | 4.21 |
| logit | native_replay | 4.90 | 0.47 | 38.0 | 7.81 |
| logit | anchored_frozen | 4.89 | 0.46 | 39.2 | 8.63 |
| logit | anchored_replay | 4.89 | 0.46 | 39.2 | 8.63 |
| softmax | native_source | 4.74 | 0.45 | 21.8 | 3.64 |
| softmax | native_frozen | 7.52 | 0.58 | 100.0 | 5.19 |
| softmax | native_replay | 4.18 | 0.55 | 11.4 | 10.34 |
| softmax | anchored_frozen | 7.33 | 0.57 | 100.0 | 6.24 |
| softmax | anchored_replay | 4.59 | 0.47 | 17.0 | 11.13 |
| aps | native_source | 4.85 | 0.43 | 29.0 | 4.46 |
| aps | native_frozen | 6.31 | 0.50 | 99.8 | 9.24 |
| aps | native_replay | 4.81 | 0.48 | 25.2 | 12.77 |
| aps | anchored_frozen | 4.68 | 0.42 | 21.8 | 20.68 |
| aps | anchored_replay | 4.89 | 0.45 | 39.0 | 19.54 |
| raps | native_source | 4.85 | 0.43 | 38.8 | 3.63 |
| raps | native_frozen | 7.63 | 0.45 | 100.0 | 5.09 |
| raps | native_replay | 4.89 | 0.44 | 40.4 | 9.24 |
| raps | anchored_frozen | 6.66 | 0.40 | 100.0 | 7.39 |
| raps | anchored_replay | 4.90 | 0.44 | 40.0 | 10.33 |

## Uncalibrated references (all kept images)

| Scores | Vocabulary | top-1 miss (%) | top-5 miss (%) | softmax >= 0.5: miss (%) | softmax >= 0.5: size |
|---|---|---:|---:|---:|---:|
| native_source | 150 | 25.12 | 4.76 | 28.79 | 0.89 |
| native_full | 845 | 31.87 | 9.86 | 37.07 | 0.82 |
| anchored_full | 150 | 25.89 | 5.03 | 31.89 | 0.83 |
| anchored_full | 845 | 33.40 | 11.03 | 45.31 | 0.67 |

Softmax temperature 1 on the stored logits (float16, clamped to [-30, 30]); RAPS lambda 0.01, k_reg 5, no randomisation. APS/RAPS membership is "mass strictly preceding the label < t" with the crossing label included (conformal.py conventions). CRC on a grid: last feasible index for constructions whose loss grows with the threshold (logit, softmax), first feasible index for APS/RAPS.