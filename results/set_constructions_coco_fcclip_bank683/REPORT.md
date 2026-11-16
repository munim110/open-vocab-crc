# Set constructions on the same scores: coco_fcclip_bank683

2000 COCO val2017 (LVIS-annotated) images (0 without a source-labelled sampled pixel excluded), 171 source labels, 1283 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration coco_fcclip_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
Rows: construction x arm. Risk = image-level fraction of source-labelled sampled pixels whose label is missing from the set, on the evaluation images; set size = mean labels per labelled pixel at the evaluation vocabulary. logit is the construction used everywhere else in this work (member iff score >= t). softmax, APS and RAPS normalise over the deployed vocabulary, so even anchored scores become candidate-dependent under them; the anchored_frozen row of those constructions is what happens when the score is projective but the set construction is not. Uncalibrated references at the bottom.

## alpha = 0.1

| Construction | Arm | Risk (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| logit | native_source | 9.89 | 0.68 | 45.6 | 5.98 |
| logit | native_frozen | 17.09 | 0.98 | 100.0 | 9.72 |
| logit | native_replay | 9.91 | 0.70 | 43.6 | 26.53 |
| logit | anchored_frozen | 9.88 | 0.66 | 42.8 | 26.85 |
| logit | anchored_replay | 9.88 | 0.66 | 42.8 | 26.85 |
| softmax | native_source | 9.73 | 0.74 | 40.0 | 6.07 |
| softmax | native_frozen | 18.03 | 1.00 | 100.0 | 8.25 |
| softmax | native_replay | 8.80 | 0.57 | 3.4 | 32.08 |
| softmax | anchored_frozen | 15.54 | 0.84 | 100.0 | 9.47 |
| softmax | anchored_replay | 9.29 | 0.62 | 3.4 | 25.73 |
| aps | native_source | 9.88 | 0.68 | 41.4 | 8.75 |
| aps | native_frozen | 9.84 | 0.63 | 41.4 | 74.98 |
| aps | native_replay | 9.85 | 0.69 | 45.2 | 74.90 |
| aps | anchored_frozen | 5.99 | 0.45 | 0.0 | 92.28 |
| aps | anchored_replay | 9.88 | 0.69 | 44.8 | 49.83 |
| raps | native_source | 9.89 | 0.68 | 41.8 | 6.68 |
| raps | native_frozen | 14.68 | 0.69 | 100.0 | 15.67 |
| raps | native_replay | 9.93 | 0.71 | 46.8 | 27.27 |
| raps | anchored_frozen | 12.22 | 0.58 | 100.0 | 17.67 |
| raps | anchored_replay | 9.93 | 0.71 | 43.6 | 25.40 |

## alpha = 0.05

| Construction | Arm | Risk (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| logit | native_source | 4.90 | 0.47 | 42.8 | 12.55 |
| logit | native_frozen | 9.78 | 0.64 | 100.0 | 27.17 |
| logit | native_replay | 4.89 | 0.47 | 41.6 | 83.09 |
| logit | anchored_frozen | 4.90 | 0.47 | 39.8 | 77.35 |
| logit | anchored_replay | 4.90 | 0.47 | 39.8 | 77.35 |
| softmax | native_source | 4.51 | 0.43 | 2.0 | 13.60 |
| softmax | native_frozen | 10.48 | 0.70 | 100.0 | 23.76 |
| softmax | native_replay | 0.00 | 0.00 | 0.0 | 1283.00 |
| softmax | anchored_frozen | 8.04 | 1.02 | 100.0 | 32.68 |
| softmax | anchored_replay | 0.24 | 1.15 | 4.0 | 1234.17 |
| aps | native_source | 4.86 | 0.46 | 38.4 | 18.81 |
| aps | native_frozen | 4.66 | 0.40 | 20.2 | 164.35 |
| aps | native_replay | 4.85 | 0.46 | 38.0 | 158.48 |
| aps | anchored_frozen | 2.47 | 0.29 | 0.0 | 202.00 |
| aps | anchored_replay | 4.88 | 0.47 | 39.8 | 115.69 |
| raps | native_source | 4.89 | 0.46 | 41.2 | 14.14 |
| raps | native_frozen | 10.79 | 0.55 | 100.0 | 23.60 |
| raps | native_replay | 4.90 | 0.48 | 40.2 | 88.12 |
| raps | anchored_frozen | 9.78 | 0.50 | 100.0 | 26.03 |
| raps | anchored_replay | 4.90 | 0.50 | 41.8 | 90.48 |

## Uncalibrated references (all kept images)

| Scores | Vocabulary | top-1 miss (%) | top-5 miss (%) | softmax >= 0.5: miss (%) | softmax >= 0.5: size |
|---|---|---:|---:|---:|---:|
| native_source | 171 | 38.77 | 13.57 | 50.78 | 0.65 |
| native_full | 1283 | 55.79 | 25.06 | 74.27 | 0.39 |
| anchored_full | 171 | 37.63 | 13.45 | 47.44 | 0.69 |
| anchored_full | 1283 | 43.27 | 22.54 | 68.20 | 0.38 |

Softmax temperature 1 on the stored logits (float16, clamped to [-30, 30]); RAPS lambda 0.01, k_reg 5, no randomisation. APS/RAPS membership is "mass strictly preceding the label < t" with the crossing label included (conformal.py conventions). CRC on a grid: last feasible index for constructions whose loss grows with the threshold (logit, softmax), first feasible index for APS/RAPS.