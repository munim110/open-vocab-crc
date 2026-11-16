# Set constructions on the same scores: pascal_vitb_bank683

2000 Pascal Context validation images (0 without a source-labelled sampled pixel excluded), 59 source labels, 458 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration pascal_vitb_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
Rows: construction x arm. Risk = image-level fraction of source-labelled sampled pixels whose label is missing from the set, on the evaluation images; set size = mean labels per labelled pixel at the evaluation vocabulary. logit is the construction used everywhere else in this work (member iff score >= t). softmax, APS and RAPS normalise over the deployed vocabulary, so even anchored scores become candidate-dependent under them; the anchored_frozen row of those constructions is what happens when the score is projective but the set construction is not. Uncalibrated references at the bottom.

## alpha = 0.1

| Construction | Arm | Risk (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| logit | native_source | 9.87 | 0.72 | 38.6 | 1.49 |
| logit | native_frozen | 15.17 | 0.85 | 100.0 | 1.63 |
| logit | native_replay | 9.88 | 0.73 | 42.4 | 2.52 |
| logit | anchored_frozen | 9.89 | 0.72 | 42.8 | 2.81 |
| logit | anchored_replay | 9.89 | 0.72 | 42.8 | 2.81 |
| softmax | native_source | 9.87 | 0.71 | 39.8 | 1.52 |
| softmax | native_frozen | 15.16 | 0.86 | 100.0 | 1.67 |
| softmax | native_replay | 9.80 | 0.75 | 39.8 | 2.71 |
| softmax | anchored_frozen | 14.97 | 0.90 | 100.0 | 1.78 |
| softmax | anchored_replay | 9.81 | 0.72 | 35.8 | 2.85 |
| aps | native_source | 9.88 | 0.71 | 41.8 | 1.62 |
| aps | native_frozen | 12.68 | 0.82 | 100.0 | 2.59 |
| aps | native_replay | 9.86 | 0.74 | 39.8 | 3.71 |
| aps | anchored_frozen | 10.42 | 0.77 | 71.4 | 3.84 |
| aps | anchored_replay | 9.87 | 0.72 | 39.8 | 4.14 |
| raps | native_source | 9.88 | 0.71 | 42.2 | 1.61 |
| raps | native_frozen | 13.08 | 0.79 | 100.0 | 2.29 |
| raps | native_replay | 9.86 | 0.74 | 41.2 | 3.03 |
| raps | anchored_frozen | 11.11 | 0.73 | 95.2 | 3.03 |
| raps | anchored_replay | 9.87 | 0.71 | 40.8 | 3.41 |

## alpha = 0.05

| Construction | Arm | Risk (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| logit | native_source | 4.88 | 0.52 | 39.2 | 2.19 |
| logit | native_frozen | 8.40 | 0.67 | 100.0 | 2.95 |
| logit | native_replay | 4.89 | 0.51 | 38.4 | 4.65 |
| logit | anchored_frozen | 4.88 | 0.52 | 37.2 | 4.94 |
| logit | anchored_replay | 4.88 | 0.52 | 37.2 | 4.94 |
| softmax | native_source | 4.79 | 0.52 | 34.2 | 2.40 |
| softmax | native_frozen | 8.04 | 0.71 | 100.0 | 3.39 |
| softmax | native_replay | 4.50 | 0.63 | 33.2 | 6.23 |
| softmax | anchored_frozen | 7.32 | 0.71 | 100.0 | 3.94 |
| softmax | anchored_replay | 4.68 | 0.53 | 25.0 | 6.18 |
| aps | native_source | 4.84 | 0.52 | 37.6 | 2.74 |
| aps | native_frozen | 6.06 | 0.59 | 97.8 | 7.12 |
| aps | native_replay | 4.80 | 0.52 | 29.6 | 9.54 |
| aps | anchored_frozen | 4.48 | 0.49 | 15.2 | 11.70 |
| aps | anchored_replay | 4.85 | 0.50 | 35.0 | 10.55 |
| raps | native_source | 4.84 | 0.51 | 37.4 | 2.47 |
| raps | native_frozen | 7.36 | 0.55 | 100.0 | 3.85 |
| raps | native_replay | 4.70 | 0.60 | 28.6 | 5.40 |
| raps | anchored_frozen | 6.11 | 0.48 | 99.0 | 5.05 |
| raps | anchored_replay | 4.86 | 0.52 | 35.8 | 5.83 |

## Uncalibrated references (all kept images)

| Scores | Vocabulary | top-1 miss (%) | top-5 miss (%) | softmax >= 0.5: miss (%) | softmax >= 0.5: size |
|---|---|---:|---:|---:|---:|
| native_source | 59 | 20.55 | 2.44 | 22.91 | 0.93 |
| native_full | 458 | 26.26 | 7.06 | 30.12 | 0.87 |
| anchored_full | 59 | 21.37 | 2.60 | 24.09 | 0.92 |
| anchored_full | 458 | 27.04 | 7.63 | 33.75 | 0.80 |

Softmax temperature 1 on the stored logits (float16, clamped to [-30, 30]); RAPS lambda 0.01, k_reg 5, no randomisation. APS/RAPS membership is "mass strictly preceding the label < t" with the crossing label included (conformal.py conventions). CRC on a grid: last feasible index for constructions whose loss grows with the threshold (logit, softmax), first feasible index for APS/RAPS.