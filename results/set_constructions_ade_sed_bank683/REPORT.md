# Set constructions on the same scores: sed_bank683

2000 ADE validation images (0 without a source-labelled sampled pixel excluded), 150 source labels, 845 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration sed_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
Rows: construction x arm. Risk = image-level fraction of source-labelled sampled pixels whose label is missing from the set, on the evaluation images; set size = mean labels per labelled pixel at the evaluation vocabulary. logit is the construction used everywhere else in this work (member iff score >= t). softmax, APS and RAPS normalise over the deployed vocabulary, so even anchored scores become candidate-dependent under them; the anchored_frozen row of those constructions is what happens when the score is projective but the set construction is not. Uncalibrated references at the bottom.

## alpha = 0.1

| Construction | Arm | Risk (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| logit | native_source | 9.90 | 0.63 | 44.4 | 2.22 |
| logit | native_frozen | 7.12 | 0.46 | 0.0 | 8.78 |
| logit | native_replay | 9.90 | 0.68 | 44.6 | 5.27 |
| logit | anchored_frozen | 9.89 | 0.66 | 44.8 | 6.04 |
| logit | anchored_replay | 9.89 | 0.66 | 44.8 | 6.04 |
| softmax | native_source | 9.85 | 0.63 | 46.0 | 2.39 |
| softmax | native_frozen | 13.99 | 0.72 | 100.0 | 3.29 |
| softmax | native_replay | 9.67 | 0.72 | 23.6 | 6.06 |
| softmax | anchored_frozen | 14.08 | 0.80 | 100.0 | 3.54 |
| softmax | anchored_replay | 9.73 | 0.69 | 24.4 | 6.34 |
| aps | native_source | 9.90 | 0.63 | 47.2 | 2.72 |
| aps | native_frozen | 10.99 | 0.64 | 93.6 | 7.68 |
| aps | native_replay | 9.89 | 0.66 | 44.8 | 9.49 |
| aps | anchored_frozen | 10.50 | 0.67 | 78.2 | 9.51 |
| aps | anchored_replay | 9.92 | 0.66 | 44.4 | 10.58 |
| raps | native_source | 9.90 | 0.63 | 44.8 | 2.55 |
| raps | native_frozen | 12.31 | 0.59 | 100.0 | 4.45 |
| raps | native_replay | 9.88 | 0.68 | 43.8 | 5.71 |
| raps | anchored_frozen | 11.99 | 0.61 | 99.8 | 5.21 |
| raps | anchored_replay | 9.90 | 0.66 | 45.0 | 6.41 |

## alpha = 0.05

| Construction | Arm | Risk (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| logit | native_source | 4.90 | 0.48 | 43.4 | 4.70 |
| logit | native_frozen | 3.79 | 0.39 | 0.2 | 24.76 |
| logit | native_replay | 4.90 | 0.51 | 43.2 | 16.14 |
| logit | anchored_frozen | 4.89 | 0.50 | 44.0 | 15.58 |
| logit | anchored_replay | 4.89 | 0.50 | 44.0 | 15.58 |
| softmax | native_source | 4.45 | 0.63 | 25.6 | 6.42 |
| softmax | native_frozen | 6.56 | 0.86 | 99.6 | 15.26 |
| softmax | native_replay | 0.00 | 0.00 | 0.0 | 845.00 |
| softmax | anchored_frozen | 6.32 | 0.75 | 97.6 | 13.27 |
| softmax | anchored_replay | 0.03 | 0.40 | 0.4 | 841.69 |
| aps | native_source | 4.79 | 0.50 | 30.0 | 6.60 |
| aps | native_frozen | 5.45 | 0.53 | 77.2 | 28.47 |
| aps | native_replay | 4.71 | 0.52 | 24.4 | 35.75 |
| aps | anchored_frozen | 4.72 | 0.47 | 31.0 | 39.58 |
| aps | anchored_replay | 4.81 | 0.48 | 39.6 | 38.36 |
| raps | native_source | 4.83 | 0.42 | 42.2 | 5.88 |
| raps | native_frozen | 8.35 | 0.53 | 100.0 | 7.59 |
| raps | native_replay | 4.91 | 0.51 | 42.8 | 19.99 |
| raps | anchored_frozen | 8.22 | 0.50 | 100.0 | 8.57 |
| raps | anchored_replay | 4.91 | 0.50 | 43.8 | 21.47 |

## Uncalibrated references (all kept images)

| Scores | Vocabulary | top-1 miss (%) | top-5 miss (%) | softmax >= 0.5: miss (%) | softmax >= 0.5: size |
|---|---|---:|---:|---:|---:|
| native_source | 150 | 27.67 | 6.24 | 30.91 | 0.90 |
| native_full | 845 | 34.01 | 12.34 | 41.60 | 0.76 |
| anchored_full | 150 | 28.27 | 6.59 | 32.81 | 0.86 |
| anchored_full | 845 | 34.92 | 13.42 | 44.76 | 0.69 |

Softmax temperature 1 on the stored logits (float16, clamped to [-30, 30]); RAPS lambda 0.01, k_reg 5, no randomisation. APS/RAPS membership is "mass strictly preceding the label < t" with the crossing label included (conformal.py conventions). CRC on a grid: last feasible index for constructions whose loss grows with the threshold (logit, softmax), first feasible index for APS/RAPS.