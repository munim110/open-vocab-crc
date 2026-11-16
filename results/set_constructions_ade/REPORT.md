# Set constructions on the same scores: vitb_coco171

2000 ADE validation images (0 without a source-labelled sampled pixel excluded), 150 source labels, 845 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration vitb_coco171. Development data; nothing is fitted; the confirmation reserve is untouched.
Rows: construction x arm. Risk = image-level fraction of source-labelled sampled pixels whose label is missing from the set, on the evaluation images; set size = mean labels per labelled pixel at the evaluation vocabulary. logit is the construction used everywhere else in this work (member iff score >= t). softmax, APS and RAPS normalise over the deployed vocabulary, so even anchored scores become candidate-dependent under them; the anchored_frozen row of those constructions is what happens when the score is projective but the set construction is not. Uncalibrated references at the bottom.

## alpha = 0.1

| Construction | Arm | Risk (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| logit | native_source | 9.88 | 0.57 | 38.4 | 2.31 |
| logit | native_frozen | 15.38 | 0.73 | 100.0 | 2.73 |
| logit | native_replay | 9.90 | 0.62 | 45.6 | 4.98 |
| logit | anchored_frozen | 9.88 | 0.60 | 42.8 | 7.30 |
| logit | anchored_replay | 9.88 | 0.60 | 42.8 | 7.30 |
| softmax | native_source | 9.84 | 0.57 | 34.2 | 2.48 |
| softmax | native_frozen | 14.65 | 0.73 | 100.0 | 3.11 |
| softmax | native_replay | 9.72 | 0.64 | 40.6 | 5.56 |
| softmax | anchored_frozen | 16.98 | 0.84 | 100.0 | 3.02 |
| softmax | anchored_replay | 9.79 | 0.59 | 36.6 | 6.39 |
| aps | native_source | 9.89 | 0.57 | 40.0 | 3.05 |
| aps | native_frozen | 11.75 | 0.65 | 100.0 | 6.42 |
| aps | native_replay | 9.89 | 0.65 | 45.4 | 8.43 |
| aps | anchored_frozen | 8.37 | 0.52 | 0.0 | 10.73 |
| aps | anchored_replay | 9.90 | 0.60 | 43.6 | 8.56 |
| raps | native_source | 9.89 | 0.57 | 39.8 | 2.80 |
| raps | native_frozen | 12.78 | 0.61 | 100.0 | 4.42 |
| raps | native_replay | 9.88 | 0.62 | 44.8 | 5.77 |
| raps | anchored_frozen | 10.00 | 0.49 | 50.6 | 7.17 |
| raps | anchored_replay | 9.90 | 0.59 | 46.0 | 7.26 |

## alpha = 0.05

| Construction | Arm | Risk (%) | Split sd (pp) | Splits above alpha (%) | Set size |
|---|---|---:|---:|---:|---:|
| logit | native_source | 4.88 | 0.42 | 36.8 | 4.54 |
| logit | native_frozen | 8.15 | 0.57 | 100.0 | 6.55 |
| logit | native_replay | 4.90 | 0.45 | 40.8 | 13.25 |
| logit | anchored_frozen | 4.89 | 0.42 | 41.6 | 15.86 |
| logit | anchored_replay | 4.89 | 0.42 | 41.6 | 15.86 |
| softmax | native_source | 4.69 | 0.44 | 20.6 | 5.07 |
| softmax | native_frozen | 7.58 | 0.60 | 100.0 | 7.97 |
| softmax | native_replay | 4.33 | 1.07 | 2.2 | 62.08 |
| softmax | anchored_frozen | 8.17 | 0.61 | 100.0 | 8.12 |
| softmax | anchored_replay | 4.65 | 0.44 | 8.0 | 16.46 |
| aps | native_source | 4.85 | 0.41 | 40.4 | 6.56 |
| aps | native_frozen | 6.00 | 0.46 | 98.8 | 17.02 |
| aps | native_replay | 4.83 | 0.46 | 30.4 | 22.12 |
| aps | anchored_frozen | 3.72 | 0.35 | 0.0 | 30.37 |
| aps | anchored_replay | 4.90 | 0.44 | 39.8 | 21.55 |
| raps | native_source | 4.83 | 0.43 | 32.8 | 4.91 |
| raps | native_frozen | 7.92 | 0.47 | 100.0 | 7.09 |
| raps | native_replay | 4.90 | 0.45 | 41.6 | 15.94 |
| raps | anchored_frozen | 6.46 | 0.35 | 100.0 | 12.28 |
| raps | anchored_replay | 4.90 | 0.44 | 42.6 | 18.44 |

## Uncalibrated references (all kept images)

| Scores | Vocabulary | top-1 miss (%) | top-5 miss (%) | softmax >= 0.5: miss (%) | softmax >= 0.5: size |
|---|---|---:|---:|---:|---:|
| native_source | 150 | 28.16 | 6.78 | 32.71 | 0.85 |
| native_full | 845 | 33.96 | 12.36 | 40.98 | 0.76 |
| anchored_full | 150 | 30.63 | 7.66 | 43.10 | 0.68 |
| anchored_full | 845 | 36.94 | 14.74 | 62.43 | 0.42 |

Softmax temperature 1 on the stored logits (float16, clamped to [-30, 30]); RAPS lambda 0.01, k_reg 5, no randomisation. APS/RAPS membership is "mass strictly preceding the label < t" with the crossing label included (conformal.py conventions). CRC on a grid: last feasible index for constructions whose loss grows with the threshold (logit, softmax), first feasible index for APS/RAPS.