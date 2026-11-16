# Set constructions on the same scores: coco_vitb_bank683

2000 COCO val2017 (LVIS-annotated) images (0 without a source-labelled sampled pixel excluded), 171 source labels, 1283 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration coco_vitb_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
Rows: construction x arm. Risk = image-level fraction of source-labelled sampled pixels whose label is missing from the set, on the evaluation images; set size = mean labels per labelled pixel at the evaluation vocabulary. logit is the construction used everywhere else in this work (member iff score >= t). softmax, APS and RAPS normalise over the deployed vocabulary, so even anchored scores become candidate-dependent under them; the anchored_frozen row of those constructions is what happens when the score is projective but the set construction is not. Uncalibrated references at the bottom.

## alpha = 0.1

| Construction | Arm | Risk (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| logit | native_source | 9.93 | 0.69 | 44.8 | 2.14 |
| logit | native_frozen | 12.96 | 0.77 | 100.0 | 2.38 |
| logit | native_replay | 9.94 | 0.70 | 45.8 | 3.09 |
| logit | anchored_frozen | 9.92 | 0.68 | 44.4 | 3.83 |
| logit | anchored_replay | 9.92 | 0.68 | 44.4 | 3.83 |
| softmax | native_source | 9.91 | 0.68 | 43.4 | 2.28 |
| softmax | native_frozen | 12.56 | 0.76 | 100.0 | 2.62 |
| softmax | native_replay | 9.85 | 0.68 | 45.0 | 3.35 |
| softmax | anchored_frozen | 12.74 | 0.82 | 100.0 | 2.69 |
| softmax | anchored_replay | 9.88 | 0.69 | 40.8 | 3.48 |
| aps | native_source | 9.94 | 0.69 | 43.6 | 2.68 |
| aps | native_frozen | 10.59 | 0.73 | 78.4 | 4.58 |
| aps | native_replay | 9.93 | 0.68 | 43.4 | 4.97 |
| aps | anchored_frozen | 8.68 | 0.68 | 3.4 | 6.99 |
| aps | anchored_replay | 9.94 | 0.68 | 44.8 | 5.85 |
| raps | native_source | 9.94 | 0.69 | 45.2 | 2.52 |
| raps | native_frozen | 11.16 | 0.70 | 95.6 | 3.49 |
| raps | native_replay | 9.93 | 0.68 | 44.0 | 3.85 |
| raps | anchored_frozen | 9.58 | 0.65 | 24.0 | 4.53 |
| raps | anchored_replay | 9.94 | 0.69 | 46.2 | 4.39 |

## alpha = 0.05

| Construction | Arm | Risk (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| logit | native_source | 4.92 | 0.50 | 44.4 | 3.52 |
| logit | native_frozen | 6.96 | 0.62 | 100.0 | 4.35 |
| logit | native_replay | 4.92 | 0.48 | 42.4 | 5.94 |
| logit | anchored_frozen | 4.92 | 0.48 | 39.6 | 7.11 |
| logit | anchored_replay | 4.92 | 0.48 | 39.6 | 7.11 |
| softmax | native_source | 4.78 | 0.52 | 41.6 | 3.97 |
| softmax | native_frozen | 6.38 | 0.60 | 99.6 | 5.25 |
| softmax | native_replay | 4.63 | 0.50 | 19.2 | 7.22 |
| softmax | anchored_frozen | 6.11 | 0.62 | 98.0 | 5.67 |
| softmax | anchored_replay | 4.76 | 0.50 | 37.8 | 7.24 |
| aps | native_source | 4.90 | 0.50 | 39.8 | 4.94 |
| aps | native_frozen | 5.09 | 0.51 | 53.4 | 10.61 |
| aps | native_replay | 4.88 | 0.49 | 38.0 | 11.08 |
| aps | anchored_frozen | 3.85 | 0.44 | 0.6 | 18.23 |
| aps | anchored_replay | 4.92 | 0.50 | 42.4 | 13.81 |
| raps | native_source | 4.90 | 0.49 | 39.6 | 3.88 |
| raps | native_frozen | 6.34 | 0.48 | 99.8 | 5.22 |
| raps | native_replay | 4.81 | 0.49 | 37.2 | 6.62 |
| raps | anchored_frozen | 5.38 | 0.43 | 79.8 | 6.72 |
| raps | anchored_replay | 4.92 | 0.48 | 40.8 | 7.10 |

## Uncalibrated references (all kept images)

| Scores | Vocabulary | top-1 miss (%) | top-5 miss (%) | softmax >= 0.5: miss (%) | softmax >= 0.5: size |
|---|---|---:|---:|---:|---:|
| native_source | 171 | 27.54 | 5.14 | 31.86 | 0.86 |
| native_full | 1283 | 31.86 | 8.39 | 37.92 | 0.80 |
| anchored_full | 171 | 27.90 | 5.18 | 33.79 | 0.83 |
| anchored_full | 1283 | 32.78 | 9.20 | 44.79 | 0.68 |

Softmax temperature 1 on the stored logits (float16, clamped to [-30, 30]); RAPS lambda 0.01, k_reg 5, no randomisation. APS/RAPS membership is "mass strictly preceding the label < t" with the crossing label included (conformal.py conventions). CRC on a grid: last feasible index for constructions whose loss grows with the threshold (logit, softmax), first feasible index for APS/RAPS.