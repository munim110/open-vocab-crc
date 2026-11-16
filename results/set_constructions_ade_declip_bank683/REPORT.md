# Set constructions on the same scores: declip_bank683

2000 ADE validation images (0 without a source-labelled sampled pixel excluded), 150 source labels, 845 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration declip_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
Rows: construction x arm. Risk = image-level fraction of source-labelled sampled pixels whose label is missing from the set, on the evaluation images; set size = mean labels per labelled pixel at the evaluation vocabulary. logit is the construction used everywhere else in this work (member iff score >= t). softmax, APS and RAPS normalise over the deployed vocabulary, so even anchored scores become candidate-dependent under them; the anchored_frozen row of those constructions is what happens when the score is projective but the set construction is not. Uncalibrated references at the bottom.

## alpha = 0.1

| Construction | Arm | Risk (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| logit | native_source | 9.90 | 0.61 | 43.2 | 1.84 |
| logit | native_frozen | 14.72 | 0.76 | 100.0 | 2.17 |
| logit | native_replay | 9.92 | 0.65 | 43.2 | 3.38 |
| logit | anchored_frozen | 9.89 | 0.66 | 44.8 | 4.37 |
| logit | anchored_replay | 9.89 | 0.66 | 44.8 | 4.37 |
| softmax | native_source | 9.88 | 0.60 | 42.0 | 1.93 |
| softmax | native_frozen | 13.97 | 0.74 | 100.0 | 2.39 |
| softmax | native_replay | 9.82 | 0.64 | 42.6 | 3.64 |
| softmax | anchored_frozen | 14.66 | 0.76 | 100.0 | 2.48 |
| softmax | anchored_replay | 9.83 | 0.63 | 35.2 | 4.15 |
| aps | native_source | 9.91 | 0.60 | 42.4 | 2.17 |
| aps | native_frozen | 11.62 | 0.68 | 99.8 | 3.93 |
| aps | native_replay | 9.92 | 0.65 | 42.8 | 4.97 |
| aps | anchored_frozen | 10.13 | 0.62 | 58.6 | 6.61 |
| aps | anchored_replay | 9.95 | 0.64 | 49.4 | 6.81 |
| raps | native_source | 9.91 | 0.60 | 42.2 | 2.10 |
| raps | native_frozen | 12.21 | 0.65 | 100.0 | 3.19 |
| raps | native_replay | 9.92 | 0.64 | 44.2 | 3.94 |
| raps | anchored_frozen | 11.10 | 0.60 | 97.4 | 4.39 |
| raps | anchored_replay | 9.94 | 0.63 | 48.2 | 4.93 |

## alpha = 0.05

| Construction | Arm | Risk (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| logit | native_source | 4.90 | 0.44 | 41.2 | 3.10 |
| logit | native_frozen | 7.96 | 0.58 | 100.0 | 4.35 |
| logit | native_replay | 4.91 | 0.46 | 41.4 | 7.62 |
| logit | anchored_frozen | 4.89 | 0.46 | 39.6 | 8.72 |
| logit | anchored_replay | 4.89 | 0.46 | 39.6 | 8.72 |
| softmax | native_source | 4.76 | 0.45 | 22.0 | 3.41 |
| softmax | native_frozen | 7.30 | 0.56 | 100.0 | 5.20 |
| softmax | native_replay | 4.24 | 0.65 | 22.4 | 10.29 |
| softmax | anchored_frozen | 7.25 | 0.59 | 100.0 | 6.12 |
| softmax | anchored_replay | 4.62 | 0.51 | 8.6 | 10.90 |
| aps | native_source | 4.86 | 0.43 | 41.4 | 4.30 |
| aps | native_frozen | 5.75 | 0.47 | 95.0 | 10.50 |
| aps | native_replay | 4.82 | 0.48 | 30.8 | 13.09 |
| aps | anchored_frozen | 4.69 | 0.43 | 24.2 | 20.82 |
| aps | anchored_replay | 4.89 | 0.46 | 42.6 | 19.68 |
| raps | native_source | 4.86 | 0.44 | 39.6 | 3.44 |
| raps | native_frozen | 7.40 | 0.45 | 100.0 | 5.13 |
| raps | native_replay | 4.91 | 0.45 | 43.0 | 9.04 |
| raps | anchored_frozen | 6.71 | 0.41 | 100.0 | 7.06 |
| raps | anchored_replay | 4.91 | 0.45 | 40.6 | 10.08 |

## Uncalibrated references (all kept images)

| Scores | Vocabulary | top-1 miss (%) | top-5 miss (%) | softmax >= 0.5: miss (%) | softmax >= 0.5: size |
|---|---|---:|---:|---:|---:|
| native_source | 150 | 24.31 | 4.65 | 27.48 | 0.90 |
| native_full | 845 | 30.00 | 9.54 | 35.54 | 0.81 |
| anchored_full | 150 | 25.02 | 4.96 | 30.03 | 0.85 |
| anchored_full | 845 | 31.34 | 10.83 | 42.56 | 0.69 |

Softmax temperature 1 on the stored logits (float16, clamped to [-30, 30]); RAPS lambda 0.01, k_reg 5, no randomisation. APS/RAPS membership is "mass strictly preceding the label < t" with the crossing label included (conformal.py conventions). CRC on a grid: last feasible index for constructions whose loss grows with the threshold (logit, softmax), first feasible index for APS/RAPS.