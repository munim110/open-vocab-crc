# Native baselines: set size at V0, tightened alpha, native arg-max outside the anchored set

2000 ADE validation images (0 without a source-labelled sampled pixel excluded), 150 source labels, 845 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration vitl_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.

Risk = image-level miss risk on source-labelled pixels (%, mean over splits; % of splits above alpha in brackets). Size = labels per source-labelled pixel at V0 (150 names) and at the grown vocabulary (845 names), evaluation images.

## alpha = 0.1

| Arm | Risk | Size at V0 | Size at 845 |
|---|---:|---:|---:|
| anchored, calibrated at V0 | 9.88 (41) | 2.25 | 4.27 |
| native at V0 (calibrated and deployed at V0) | 9.90 (39) | 1.91 | -- |
| native reused (V0 threshold at the grown vocabulary) | 15.22 (100) | -- | 2.16 |
| native recalibrated at the grown vocabulary | 9.91 (43) | -- | 3.47 |
| native reused with alpha' = 0.0600 (oracle: chosen on the evaluation images at 845 names) | 9.88 (41) | -- | 3.48 |

The native top-1 label at 845 names is outside the anchored set on 0.34% of the evaluation source-labelled pixels, and on 0.30% of those where it is correct (native top-1 accuracy 68.4%).

## alpha = 0.05

| Arm | Risk | Size at V0 | Size at 845 |
|---|---:|---:|---:|
| anchored, calibrated at V0 | 4.89 (39) | 3.66 | 8.63 |
| native at V0 (calibrated and deployed at V0) | 4.89 (36) | 3.28 | -- |
| native reused (V0 threshold at the grown vocabulary) | 8.38 (100) | -- | 4.21 |
| native recalibrated at the grown vocabulary | 4.90 (38) | -- | 7.81 |
| native reused with alpha' = 0.0250 (oracle: chosen on the evaluation images at 845 names) | 4.82 (30) | -- | 7.95 |

The native top-1 label at 845 names is outside the anchored set on 0.01% of the evaluation source-labelled pixels, and on 0.01% of those where it is correct (native top-1 accuracy 68.4%).

The alpha' row is a reference for the set size a tightened reuse would cost: choosing alpha' used the labels of the evaluation images at the grown vocabulary, which a deployment that reuses its V0 calibration does not have.
