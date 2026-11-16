# Set constructions on the same scores: coco_declip_bank683

2000 COCO val2017 (LVIS-annotated) images (0 without a source-labelled sampled pixel excluded), 171 source labels, 1283 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration coco_declip_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
Rows: construction x arm. Risk = image-level fraction of source-labelled sampled pixels whose label is missing from the set, on the evaluation images; set size = mean labels per labelled pixel at the evaluation vocabulary. logit is the construction used everywhere else in this work (member iff score >= t). softmax, APS and RAPS normalise over the deployed vocabulary, so even anchored scores become candidate-dependent under them; the anchored_frozen row of those constructions is what happens when the score is projective but the set construction is not. Uncalibrated references at the bottom.

## alpha = 0.1

| Construction | Arm | Risk (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| logit | native_source | 9.91 | 0.69 | 43.2 | 1.85 |
| logit | native_frozen | 12.93 | 0.77 | 100.0 | 2.07 |
| logit | native_replay | 9.94 | 0.68 | 46.0 | 2.63 |
| logit | anchored_frozen | 9.90 | 0.68 | 43.6 | 3.19 |
| logit | anchored_replay | 9.90 | 0.68 | 43.6 | 3.19 |
| softmax | native_source | 9.91 | 0.68 | 45.2 | 1.93 |
| softmax | native_frozen | 12.77 | 0.77 | 100.0 | 2.19 |
| softmax | native_replay | 9.88 | 0.68 | 41.8 | 2.79 |
| softmax | anchored_frozen | 12.54 | 0.81 | 100.0 | 2.40 |
| softmax | anchored_replay | 9.88 | 0.68 | 38.0 | 2.96 |
| aps | native_source | 9.96 | 0.69 | 45.2 | 2.16 |
| aps | native_frozen | 11.23 | 0.77 | 95.0 | 3.26 |
| aps | native_replay | 9.95 | 0.69 | 49.2 | 3.81 |
| aps | anchored_frozen | 9.58 | 0.71 | 26.8 | 4.79 |
| aps | anchored_replay | 9.94 | 0.68 | 44.8 | 4.56 |
| raps | native_source | 9.96 | 0.69 | 45.8 | 2.09 |
| raps | native_frozen | 11.61 | 0.73 | 98.8 | 2.76 |
| raps | native_replay | 9.94 | 0.69 | 45.4 | 3.16 |
| raps | anchored_frozen | 10.16 | 0.68 | 60.2 | 3.52 |
| raps | anchored_replay | 9.94 | 0.68 | 47.2 | 3.58 |

## alpha = 0.05

| Construction | Arm | Risk (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| logit | native_source | 4.93 | 0.49 | 44.2 | 2.86 |
| logit | native_frozen | 6.83 | 0.57 | 99.8 | 3.60 |
| logit | native_replay | 4.92 | 0.49 | 43.4 | 4.83 |
| logit | anchored_frozen | 4.92 | 0.49 | 43.8 | 5.66 |
| logit | anchored_replay | 4.92 | 0.49 | 43.8 | 5.66 |
| softmax | native_source | 4.82 | 0.54 | 35.6 | 3.15 |
| softmax | native_frozen | 6.43 | 0.62 | 99.4 | 4.10 |
| softmax | native_replay | 4.67 | 0.52 | 30.6 | 5.54 |
| softmax | anchored_frozen | 5.99 | 0.60 | 93.8 | 4.72 |
| softmax | anchored_replay | 4.77 | 0.52 | 34.6 | 5.80 |
| aps | native_source | 4.88 | 0.51 | 32.6 | 3.75 |
| aps | native_frozen | 5.52 | 0.54 | 82.8 | 7.23 |
| aps | native_replay | 4.85 | 0.49 | 34.6 | 8.22 |
| aps | anchored_frozen | 4.30 | 0.49 | 9.4 | 13.67 |
| aps | anchored_replay | 4.90 | 0.50 | 42.2 | 11.58 |
| raps | native_source | 4.89 | 0.50 | 38.2 | 3.14 |
| raps | native_frozen | 6.46 | 0.51 | 99.8 | 4.16 |
| raps | native_replay | 4.83 | 0.52 | 36.2 | 5.10 |
| raps | anchored_frozen | 5.56 | 0.47 | 88.4 | 5.31 |
| raps | anchored_replay | 4.90 | 0.50 | 42.4 | 5.68 |

## Uncalibrated references (all kept images)

| Scores | Vocabulary | top-1 miss (%) | top-5 miss (%) | softmax >= 0.5: miss (%) | softmax >= 0.5: size |
|---|---|---:|---:|---:|---:|
| native_source | 171 | 25.13 | 3.85 | 28.51 | 0.90 |
| native_full | 1283 | 29.40 | 6.83 | 34.08 | 0.85 |
| anchored_full | 171 | 25.34 | 3.84 | 29.39 | 0.88 |
| anchored_full | 1283 | 30.31 | 7.41 | 40.11 | 0.75 |

Softmax temperature 1 on the stored logits (float16, clamped to [-30, 30]); RAPS lambda 0.01, k_reg 5, no randomisation. APS/RAPS membership is "mass strictly preceding the label < t" with the crossing label included (conformal.py conventions). CRC on a grid: last feasible index for constructions whose loss grows with the threshold (logit, softmax), first feasible index for APS/RAPS.