# Set constructions on the same scores: pascal_vitl_bank683

2000 Pascal Context validation images (0 without a source-labelled sampled pixel excluded), 59 source labels, 458 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration pascal_vitl_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
Rows: construction x arm. Risk = image-level fraction of source-labelled sampled pixels whose label is missing from the set, on the evaluation images; set size = mean labels per labelled pixel at the evaluation vocabulary. logit is the construction used everywhere else in this work (member iff score >= t). softmax, APS and RAPS normalise over the deployed vocabulary, so even anchored scores become candidate-dependent under them; the anchored_frozen row of those constructions is what happens when the score is projective but the set construction is not. Uncalibrated references at the bottom.

## alpha = 0.1

| Construction | Arm | Risk (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| logit | native_source | 9.87 | 0.73 | 40.0 | 1.37 |
| logit | native_frozen | 15.05 | 0.83 | 100.0 | 1.49 |
| logit | native_replay | 9.88 | 0.73 | 42.8 | 2.07 |
| logit | anchored_frozen | 9.90 | 0.76 | 44.4 | 2.33 |
| logit | anchored_replay | 9.90 | 0.76 | 44.4 | 2.33 |
| softmax | native_source | 9.87 | 0.73 | 40.8 | 1.38 |
| softmax | native_frozen | 14.78 | 0.88 | 100.0 | 1.52 |
| softmax | native_replay | 9.81 | 0.74 | 35.0 | 2.18 |
| softmax | anchored_frozen | 14.87 | 0.88 | 100.0 | 1.58 |
| softmax | anchored_replay | 9.83 | 0.73 | 35.6 | 2.28 |
| aps | native_source | 9.87 | 0.72 | 41.8 | 1.44 |
| aps | native_frozen | 13.01 | 0.87 | 100.0 | 1.94 |
| aps | native_replay | 9.85 | 0.75 | 40.2 | 2.67 |
| aps | anchored_frozen | 11.45 | 0.79 | 98.2 | 2.52 |
| aps | anchored_replay | 9.85 | 0.73 | 39.8 | 3.05 |
| raps | native_source | 9.87 | 0.72 | 40.8 | 1.43 |
| raps | native_frozen | 13.17 | 0.85 | 100.0 | 1.85 |
| raps | native_replay | 9.86 | 0.74 | 40.0 | 2.38 |
| raps | anchored_frozen | 11.77 | 0.76 | 99.4 | 2.24 |
| raps | anchored_replay | 9.85 | 0.73 | 38.6 | 2.64 |

## alpha = 0.05

| Construction | Arm | Risk (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| logit | native_source | 4.88 | 0.51 | 38.4 | 1.87 |
| logit | native_frozen | 8.56 | 0.68 | 100.0 | 2.30 |
| logit | native_replay | 4.91 | 0.52 | 42.0 | 3.37 |
| logit | anchored_frozen | 4.89 | 0.52 | 41.0 | 3.66 |
| logit | anchored_replay | 4.89 | 0.52 | 41.0 | 3.66 |
| softmax | native_source | 4.80 | 0.51 | 35.2 | 2.04 |
| softmax | native_frozen | 7.68 | 0.66 | 100.0 | 2.69 |
| softmax | native_replay | 4.63 | 0.59 | 18.4 | 4.26 |
| softmax | anchored_frozen | 7.15 | 0.67 | 100.0 | 3.05 |
| softmax | anchored_replay | 4.69 | 0.54 | 29.2 | 4.54 |
| aps | native_source | 4.84 | 0.50 | 33.8 | 2.25 |
| aps | native_frozen | 6.16 | 0.59 | 98.8 | 4.62 |
| aps | native_replay | 4.82 | 0.52 | 37.4 | 6.26 |
| aps | anchored_frozen | 5.05 | 0.53 | 51.6 | 7.51 |
| aps | anchored_replay | 4.83 | 0.50 | 34.6 | 7.98 |
| raps | native_source | 4.84 | 0.50 | 36.2 | 2.11 |
| raps | native_frozen | 7.02 | 0.55 | 100.0 | 3.02 |
| raps | native_replay | 4.80 | 0.54 | 37.8 | 3.84 |
| raps | anchored_frozen | 6.12 | 0.51 | 99.6 | 3.77 |
| raps | anchored_replay | 4.84 | 0.51 | 35.0 | 4.35 |

## Uncalibrated references (all kept images)

| Scores | Vocabulary | top-1 miss (%) | top-5 miss (%) | softmax >= 0.5: miss (%) | softmax >= 0.5: size |
|---|---|---:|---:|---:|---:|
| native_source | 59 | 18.75 | 1.58 | 20.56 | 0.95 |
| native_full | 458 | 24.50 | 5.39 | 27.38 | 0.90 |
| anchored_full | 59 | 19.60 | 1.68 | 21.79 | 0.94 |
| anchored_full | 458 | 25.26 | 5.80 | 30.05 | 0.85 |

Softmax temperature 1 on the stored logits (float16, clamped to [-30, 30]); RAPS lambda 0.01, k_reg 5, no randomisation. APS/RAPS membership is "mass strictly preceding the label < t" with the crossing label included (conformal.py conventions). CRC on a grid: last feasible index for constructions whose loss grows with the threshold (logit, softmax), first feasible index for APS/RAPS.