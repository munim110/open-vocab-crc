# Native baselines: set size at V0, tightened alpha, native arg-max outside the anchored set

2000 ADE validation images (0 without a source-labelled sampled pixel excluded), 150 source labels, 845 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration sed_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.

Risk = image-level miss risk on source-labelled pixels (%, mean over splits; % of splits above alpha in brackets). Size = labels per source-labelled pixel at V0 (150 names) and at the grown vocabulary (845 names), evaluation images.

## alpha = 0.1

| Arm | Risk | Size at V0 | Size at 845 |
|---|---:|---:|---:|
| anchored, calibrated at V0 | 9.89 (45) | 2.76 | 6.04 |
| native at V0 (calibrated and deployed at V0) | 9.90 (44) | 2.22 | -- |
| native reused (V0 threshold at the grown vocabulary) | 7.12 (0) | -- | 8.78 |
| native recalibrated at the grown vocabulary | 9.90 (45) | -- | 5.27 |
| native reused with alpha' = 0.1525 (oracle: chosen on the evaluation images at 845 names) | 9.98 (49) | -- | 5.20 |

The native top-1 label at 845 names is outside the anchored set on 0.20% of the evaluation source-labelled pixels, and on 0.21% of those where it is correct (native top-1 accuracy 66.3%).

## alpha = 0.05

| Arm | Risk | Size at V0 | Size at 845 |
|---|---:|---:|---:|
| anchored, calibrated at V0 | 4.89 (44) | 5.30 | 15.58 |
| native at V0 (calibrated and deployed at V0) | 4.90 (43) | 4.70 | -- |
| native reused (V0 threshold at the grown vocabulary) | 3.79 (0) | -- | 24.76 |
| native recalibrated at the grown vocabulary | 4.90 (43) | -- | 16.14 |
| native reused with alpha' = 0.0650 (oracle: chosen on the evaluation images at 845 names) | 4.84 (37) | -- | 16.41 |

The native top-1 label at 845 names is outside the anchored set on 0.00% of the evaluation source-labelled pixels, and on 0.00% of those where it is correct (native top-1 accuracy 66.3%).

The alpha' row is a reference for the set size a tightened reuse would cost: choosing alpha' used the labels of the evaluation images at the grown vocabulary, which a deployment that reuses its V0 calibration does not have.
