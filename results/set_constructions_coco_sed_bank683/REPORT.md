# Set constructions on the same scores: coco_sed_bank683

2000 COCO val2017 (LVIS-annotated) images (0 without a source-labelled sampled pixel excluded), 171 source labels, 1283 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration coco_sed_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
Rows: construction x arm. Risk = image-level fraction of source-labelled sampled pixels whose label is missing from the set, on the evaluation images; set size = mean labels per labelled pixel at the evaluation vocabulary. logit is the construction used everywhere else in this work (member iff score >= t). softmax, APS and RAPS normalise over the deployed vocabulary, so even anchored scores become candidate-dependent under them; the anchored_frozen row of those constructions is what happens when the score is projective but the set construction is not. Uncalibrated references at the bottom.

## alpha = 0.1

| Construction | Arm | Risk (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| logit | native_source | 9.93 | 0.72 | 49.0 | 2.00 |
| logit | native_frozen | 3.64 | 0.34 | 0.0 | 8.19 |
| logit | native_replay | 9.92 | 0.67 | 44.6 | 3.74 |
| logit | anchored_frozen | 9.92 | 0.69 | 45.0 | 3.55 |
| logit | anchored_replay | 9.92 | 0.69 | 45.0 | 3.55 |
| softmax | native_source | 9.89 | 0.73 | 44.0 | 2.12 |
| softmax | native_frozen | 10.53 | 0.62 | 79.2 | 3.20 |
| softmax | native_replay | 9.90 | 0.68 | 41.8 | 3.39 |
| softmax | anchored_frozen | 12.47 | 0.83 | 99.8 | 2.67 |
| softmax | anchored_replay | 9.88 | 0.72 | 39.2 | 3.30 |
| aps | native_source | 9.93 | 0.72 | 42.0 | 2.38 |
| aps | native_frozen | 8.08 | 0.57 | 0.0 | 5.81 |
| aps | native_replay | 9.95 | 0.68 | 46.0 | 4.41 |
| aps | anchored_frozen | 9.95 | 0.74 | 47.6 | 4.54 |
| aps | anchored_replay | 9.96 | 0.71 | 47.2 | 4.53 |
| raps | native_source | 9.93 | 0.72 | 44.6 | 2.27 |
| raps | native_frozen | 8.89 | 0.54 | 2.4 | 4.05 |
| raps | native_replay | 9.95 | 0.68 | 48.0 | 3.70 |
| raps | anchored_frozen | 10.57 | 0.71 | 77.8 | 3.52 |
| raps | anchored_replay | 9.97 | 0.71 | 48.6 | 3.70 |

## alpha = 0.05

| Construction | Arm | Risk (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| logit | native_source | 4.92 | 0.51 | 42.8 | 3.20 |
| logit | native_frozen | 1.62 | 0.20 | 0.0 | 14.61 |
| logit | native_replay | 4.91 | 0.47 | 39.6 | 6.47 |
| logit | anchored_frozen | 4.92 | 0.48 | 43.4 | 6.16 |
| logit | anchored_replay | 4.92 | 0.48 | 43.4 | 6.16 |
| softmax | native_source | 4.77 | 0.55 | 30.2 | 3.56 |
| softmax | native_frozen | 5.66 | 0.55 | 86.8 | 5.82 |
| softmax | native_replay | 4.65 | 0.54 | 29.2 | 7.01 |
| softmax | anchored_frozen | 6.01 | 0.62 | 98.0 | 5.22 |
| softmax | anchored_replay | 4.69 | 0.52 | 25.4 | 6.50 |
| aps | native_source | 4.87 | 0.53 | 33.4 | 4.21 |
| aps | native_frozen | 4.06 | 0.42 | 1.6 | 14.25 |
| aps | native_replay | 4.91 | 0.50 | 44.4 | 11.25 |
| aps | anchored_frozen | 4.52 | 0.51 | 17.2 | 11.80 |
| aps | anchored_replay | 4.91 | 0.51 | 44.6 | 10.69 |
| raps | native_source | 4.87 | 0.50 | 40.2 | 3.43 |
| raps | native_frozen | 5.78 | 0.39 | 97.8 | 5.54 |
| raps | native_replay | 4.89 | 0.47 | 34.2 | 6.49 |
| raps | anchored_frozen | 5.91 | 0.48 | 98.0 | 5.33 |
| raps | anchored_replay | 4.89 | 0.50 | 35.6 | 6.12 |

## Uncalibrated references (all kept images)

| Scores | Vocabulary | top-1 miss (%) | top-5 miss (%) | softmax >= 0.5: miss (%) | softmax >= 0.5: size |
|---|---|---:|---:|---:|---:|
| native_source | 171 | 26.28 | 4.60 | 29.28 | 0.90 |
| native_full | 1283 | 36.63 | 8.43 | 49.91 | 0.65 |
| anchored_full | 171 | 26.78 | 4.63 | 30.43 | 0.89 |
| anchored_full | 1283 | 34.28 | 8.42 | 43.61 | 0.72 |

Softmax temperature 1 on the stored logits (float16, clamped to [-30, 30]); RAPS lambda 0.01, k_reg 5, no randomisation. APS/RAPS membership is "mass strictly preceding the label < t" with the crossing label included (conformal.py conventions). CRC on a grid: last feasible index for constructions whose loss grows with the threshold (logit, softmax), first feasible index for APS/RAPS.