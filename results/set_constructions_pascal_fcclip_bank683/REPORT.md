# Set constructions on the same scores: pascal_fcclip_bank683

2000 Pascal Context validation images (0 without a source-labelled sampled pixel excluded), 59 source labels, 458 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration pascal_fcclip_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
Rows: construction x arm. Risk = image-level fraction of source-labelled sampled pixels whose label is missing from the set, on the evaluation images; set size = mean labels per labelled pixel at the evaluation vocabulary. logit is the construction used everywhere else in this work (member iff score >= t). softmax, APS and RAPS normalise over the deployed vocabulary, so even anchored scores become candidate-dependent under them; the anchored_frozen row of those constructions is what happens when the score is projective but the set construction is not. Uncalibrated references at the bottom.

## alpha = 0.1

| Construction | Arm | Risk (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| logit | native_source | 9.89 | 0.75 | 44.0 | 1.95 |
| logit | native_frozen | 16.25 | 1.00 | 100.0 | 2.82 |
| logit | native_replay | 9.86 | 0.78 | 39.6 | 5.31 |
| logit | anchored_frozen | 9.89 | 0.75 | 41.4 | 5.77 |
| logit | anchored_replay | 9.89 | 0.75 | 41.4 | 5.77 |
| softmax | native_source | 9.90 | 0.75 | 44.2 | 1.86 |
| softmax | native_frozen | 18.59 | 1.11 | 100.0 | 2.23 |
| softmax | native_replay | 9.71 | 0.80 | 29.6 | 5.76 |
| softmax | anchored_frozen | 17.37 | 1.02 | 100.0 | 2.06 |
| softmax | anchored_replay | 9.79 | 0.76 | 37.2 | 4.57 |
| aps | native_source | 9.91 | 0.76 | 46.0 | 2.12 |
| aps | native_frozen | 9.42 | 0.82 | 22.0 | 16.14 |
| aps | native_replay | 9.85 | 0.76 | 41.4 | 15.10 |
| aps | anchored_frozen | 6.88 | 0.66 | 0.0 | 17.68 |
| aps | anchored_replay | 9.89 | 0.75 | 44.6 | 10.62 |
| raps | native_source | 9.91 | 0.76 | 45.6 | 2.07 |
| raps | native_frozen | 11.09 | 0.77 | 93.0 | 7.44 |
| raps | native_replay | 9.88 | 0.75 | 42.8 | 8.41 |
| raps | anchored_frozen | 8.98 | 0.64 | 6.2 | 7.55 |
| raps | anchored_replay | 9.91 | 0.74 | 45.8 | 6.80 |

## alpha = 0.05

| Construction | Arm | Risk (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| logit | native_source | 4.89 | 0.55 | 37.6 | 3.13 |
| logit | native_frozen | 8.56 | 0.76 | 100.0 | 6.36 |
| logit | native_replay | 4.87 | 0.54 | 41.4 | 12.78 |
| logit | anchored_frozen | 4.88 | 0.54 | 39.2 | 13.97 |
| logit | anchored_replay | 4.88 | 0.54 | 39.2 | 13.97 |
| softmax | native_source | 4.81 | 0.55 | 37.6 | 3.33 |
| softmax | native_frozen | 9.81 | 0.81 | 100.0 | 5.69 |
| softmax | native_replay | 4.54 | 0.56 | 12.6 | 16.16 |
| softmax | anchored_frozen | 9.09 | 0.76 | 100.0 | 5.14 |
| softmax | anchored_replay | 4.62 | 0.56 | 34.6 | 12.67 |
| aps | native_source | 4.87 | 0.54 | 39.4 | 4.25 |
| aps | native_frozen | 3.75 | 0.43 | 0.0 | 48.41 |
| aps | native_replay | 4.86 | 0.56 | 38.4 | 37.53 |
| aps | anchored_frozen | 2.58 | 0.36 | 0.0 | 46.91 |
| aps | anchored_replay | 4.89 | 0.53 | 40.0 | 27.27 |
| raps | native_source | 4.87 | 0.54 | 37.8 | 3.78 |
| raps | native_frozen | 6.40 | 0.48 | 99.8 | 12.38 |
| raps | native_replay | 4.89 | 0.55 | 40.8 | 15.08 |
| raps | anchored_frozen | 5.60 | 0.42 | 93.0 | 11.84 |
| raps | anchored_replay | 4.90 | 0.54 | 41.4 | 13.33 |

## Uncalibrated references (all kept images)

| Scores | Vocabulary | top-1 miss (%) | top-5 miss (%) | softmax >= 0.5: miss (%) | softmax >= 0.5: size |
|---|---|---:|---:|---:|---:|
| native_source | 59 | 23.64 | 4.35 | 29.64 | 0.84 |
| native_full | 458 | 36.85 | 12.20 | 59.46 | 0.52 |
| anchored_full | 59 | 23.51 | 4.20 | 28.63 | 0.86 |
| anchored_full | 458 | 30.82 | 11.95 | 48.51 | 0.59 |

Softmax temperature 1 on the stored logits (float16, clamped to [-30, 30]); RAPS lambda 0.01, k_reg 5, no randomisation. APS/RAPS membership is "mass strictly preceding the label < t" with the crossing label included (conformal.py conventions). CRC on a grid: last feasible index for constructions whose loss grows with the threshold (logit, softmax), first feasible index for APS/RAPS.