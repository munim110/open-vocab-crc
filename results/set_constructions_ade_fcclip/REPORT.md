# Set constructions on the same scores: fcclip

2000 ADE validation images (0 without a source-labelled sampled pixel excluded), 150 source labels, 845 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration fcclip. Development data; nothing is fitted; the confirmation reserve is untouched.
Rows: construction x arm. Risk = image-level fraction of source-labelled sampled pixels whose label is missing from the set, on the evaluation images; set size = mean labels per labelled pixel at the evaluation vocabulary. logit is the construction used everywhere else in this work (member iff score >= t). softmax, APS and RAPS normalise over the deployed vocabulary, so even anchored scores become candidate-dependent under them; the anchored_frozen row of those constructions is what happens when the score is projective but the set construction is not. Uncalibrated references at the bottom.

## alpha = 0.1

| Construction | Arm | Risk (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| logit | native_source | 9.89 | 0.62 | 39.8 | 3.22 |
| logit | native_frozen | 13.81 | 0.77 | 100.0 | 5.17 |
| logit | native_replay | 9.89 | 0.66 | 43.0 | 8.17 |
| logit | anchored_frozen | 9.90 | 0.62 | 45.2 | 13.49 |
| logit | anchored_replay | 9.90 | 0.62 | 45.2 | 13.49 |
| softmax | native_source | 9.86 | 0.61 | 36.0 | 3.05 |
| softmax | native_frozen | 17.24 | 0.89 | 100.0 | 3.84 |
| softmax | native_replay | 9.68 | 0.71 | 42.4 | 9.10 |
| softmax | anchored_frozen | 16.32 | 0.96 | 100.0 | 3.31 |
| softmax | anchored_replay | 9.79 | 0.67 | 34.4 | 8.15 |
| aps | native_source | 9.91 | 0.59 | 42.6 | 4.63 |
| aps | native_frozen | 10.94 | 0.63 | 93.0 | 19.85 |
| aps | native_replay | 9.89 | 0.70 | 45.8 | 23.77 |
| aps | anchored_frozen | 7.74 | 0.52 | 0.0 | 25.84 |
| aps | anchored_replay | 9.91 | 0.64 | 45.6 | 16.86 |
| raps | native_source | 9.90 | 0.59 | 43.4 | 3.97 |
| raps | native_frozen | 12.65 | 0.64 | 100.0 | 8.66 |
| raps | native_replay | 9.92 | 0.68 | 47.6 | 11.36 |
| raps | anchored_frozen | 9.80 | 0.52 | 35.8 | 11.01 |
| raps | anchored_replay | 9.93 | 0.64 | 47.2 | 10.81 |

## alpha = 0.05

| Construction | Arm | Risk (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| logit | native_source | 4.90 | 0.46 | 40.0 | 7.56 |
| logit | native_frozen | 6.78 | 0.60 | 100.0 | 14.47 |
| logit | native_replay | 4.90 | 0.49 | 40.8 | 25.58 |
| logit | anchored_frozen | 4.92 | 0.47 | 41.6 | 36.66 |
| logit | anchored_replay | 4.92 | 0.47 | 41.6 | 36.66 |
| softmax | native_source | 4.78 | 0.47 | 42.8 | 8.00 |
| softmax | native_frozen | 8.04 | 0.77 | 100.0 | 12.00 |
| softmax | native_replay | 4.16 | 0.81 | 33.0 | 38.50 |
| softmax | anchored_frozen | 7.20 | 0.72 | 100.0 | 14.26 |
| softmax | anchored_replay | 4.52 | 0.62 | 40.0 | 32.82 |
| aps | native_source | 4.90 | 0.46 | 39.0 | 11.55 |
| aps | native_frozen | 4.84 | 0.50 | 36.4 | 63.58 |
| aps | native_replay | 4.89 | 0.50 | 38.8 | 62.80 |
| aps | anchored_frozen | 3.55 | 0.40 | 0.0 | 80.65 |
| aps | anchored_replay | 4.90 | 0.49 | 41.6 | 51.92 |
| raps | native_source | 4.90 | 0.46 | 41.0 | 8.34 |
| raps | native_frozen | 7.54 | 0.49 | 100.0 | 14.85 |
| raps | native_replay | 4.91 | 0.50 | 43.2 | 27.84 |
| raps | anchored_frozen | 6.61 | 0.41 | 100.0 | 18.47 |
| raps | anchored_replay | 4.91 | 0.51 | 42.2 | 31.23 |

## Uncalibrated references (all kept images)

| Scores | Vocabulary | top-1 miss (%) | top-5 miss (%) | softmax >= 0.5: miss (%) | softmax >= 0.5: size |
|---|---|---:|---:|---:|---:|
| native_source | 150 | 33.77 | 8.36 | 45.67 | 0.70 |
| native_full | 845 | 47.71 | 16.29 | 69.85 | 0.42 |
| anchored_full | 150 | 30.32 | 8.11 | 42.69 | 0.70 |
| anchored_full | 845 | 34.24 | 14.54 | 66.55 | 0.39 |

Softmax temperature 1 on the stored logits (float16, clamped to [-30, 30]); RAPS lambda 0.01, k_reg 5, no randomisation. APS/RAPS membership is "mass strictly preceding the label < t" with the crossing label included (conformal.py conventions). CRC on a grid: last feasible index for constructions whose loss grows with the threshold (logit, softmax), first feasible index for APS/RAPS.