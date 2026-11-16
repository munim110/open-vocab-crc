# Set constructions on the same scores: coco_vitl_bank683

2000 COCO val2017 (LVIS-annotated) images (0 without a source-labelled sampled pixel excluded), 171 source labels, 1283 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration coco_vitl_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
Rows: construction x arm. Risk = image-level fraction of source-labelled sampled pixels whose label is missing from the set, on the evaluation images; set size = mean labels per labelled pixel at the evaluation vocabulary. logit is the construction used everywhere else in this work (member iff score >= t). softmax, APS and RAPS normalise over the deployed vocabulary, so even anchored scores become candidate-dependent under them; the anchored_frozen row of those constructions is what happens when the score is projective but the set construction is not. Uncalibrated references at the bottom.

## alpha = 0.1

| Construction | Arm | Risk (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| logit | native_source | 9.93 | 0.69 | 45.8 | 1.94 |
| logit | native_frozen | 12.88 | 0.79 | 100.0 | 2.13 |
| logit | native_replay | 9.95 | 0.68 | 46.2 | 2.65 |
| logit | anchored_frozen | 9.92 | 0.68 | 42.4 | 3.21 |
| logit | anchored_replay | 9.92 | 0.68 | 42.4 | 3.21 |
| softmax | native_source | 9.90 | 0.69 | 45.8 | 2.05 |
| softmax | native_frozen | 12.42 | 0.77 | 99.8 | 2.31 |
| softmax | native_replay | 9.87 | 0.69 | 41.6 | 2.88 |
| softmax | anchored_frozen | 12.18 | 0.78 | 99.8 | 2.46 |
| softmax | anchored_replay | 9.89 | 0.69 | 40.8 | 3.01 |
| aps | native_source | 9.94 | 0.69 | 44.0 | 2.29 |
| aps | native_frozen | 11.25 | 0.73 | 96.0 | 3.27 |
| aps | native_replay | 9.94 | 0.68 | 46.6 | 3.78 |
| aps | anchored_frozen | 9.40 | 0.69 | 17.4 | 4.87 |
| aps | anchored_replay | 9.94 | 0.67 | 47.0 | 4.52 |
| raps | native_source | 9.94 | 0.69 | 43.4 | 2.21 |
| raps | native_frozen | 11.60 | 0.71 | 99.0 | 2.82 |
| raps | native_replay | 9.94 | 0.68 | 45.4 | 3.21 |
| raps | anchored_frozen | 10.03 | 0.67 | 51.0 | 3.62 |
| raps | anchored_replay | 9.94 | 0.68 | 46.8 | 3.64 |

## alpha = 0.05

| Construction | Arm | Risk (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| logit | native_source | 4.92 | 0.49 | 40.8 | 3.01 |
| logit | native_frozen | 7.02 | 0.57 | 100.0 | 3.59 |
| logit | native_replay | 4.92 | 0.50 | 43.6 | 4.88 |
| logit | anchored_frozen | 4.90 | 0.50 | 42.8 | 5.74 |
| logit | anchored_replay | 4.90 | 0.50 | 42.8 | 5.74 |
| softmax | native_source | 4.81 | 0.52 | 26.6 | 3.38 |
| softmax | native_frozen | 6.33 | 0.61 | 99.2 | 4.25 |
| softmax | native_replay | 4.66 | 0.54 | 37.6 | 5.57 |
| softmax | anchored_frozen | 5.95 | 0.60 | 95.8 | 4.79 |
| softmax | anchored_replay | 4.76 | 0.50 | 32.2 | 5.84 |
| aps | native_source | 4.89 | 0.51 | 37.2 | 4.08 |
| aps | native_frozen | 5.48 | 0.54 | 80.4 | 7.14 |
| aps | native_replay | 4.86 | 0.49 | 35.6 | 7.98 |
| aps | anchored_frozen | 4.12 | 0.49 | 5.6 | 13.12 |
| aps | anchored_replay | 4.91 | 0.51 | 39.6 | 10.69 |
| raps | native_source | 4.90 | 0.49 | 34.6 | 3.33 |
| raps | native_frozen | 6.40 | 0.52 | 99.8 | 4.24 |
| raps | native_replay | 4.84 | 0.52 | 33.0 | 5.18 |
| raps | anchored_frozen | 5.38 | 0.46 | 80.0 | 5.43 |
| raps | anchored_replay | 4.91 | 0.48 | 40.6 | 5.72 |

## Uncalibrated references (all kept images)

| Scores | Vocabulary | top-1 miss (%) | top-5 miss (%) | softmax >= 0.5: miss (%) | softmax >= 0.5: size |
|---|---|---:|---:|---:|---:|
| native_source | 171 | 26.07 | 4.22 | 29.55 | 0.89 |
| native_full | 1283 | 30.46 | 7.03 | 35.04 | 0.84 |
| anchored_full | 171 | 26.50 | 4.28 | 31.02 | 0.86 |
| anchored_full | 1283 | 31.47 | 7.59 | 41.00 | 0.74 |

Softmax temperature 1 on the stored logits (float16, clamped to [-30, 30]); RAPS lambda 0.01, k_reg 5, no randomisation. APS/RAPS membership is "mass strictly preceding the label < t" with the crossing label included (conformal.py conventions). CRC on a grid: last feasible index for constructions whose loss grows with the threshold (logit, softmax), first feasible index for APS/RAPS.