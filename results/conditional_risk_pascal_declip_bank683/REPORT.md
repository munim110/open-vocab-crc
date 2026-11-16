# Conditional risk under source-calibrated thresholds: pascal_declip_bank683

2000 Pascal Context validation images (0 without a source-labelled sampled pixel excluded), 59 source labels, 458 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration pascal_declip_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
The CRC guarantee is on the marginal mean of the image loss (fraction of source-labelled sampled pixels whose label is missing from the set). Every stratum below is outside the guarantee for every arm; the table shows how the frozen thresholds behave inside them relative to recalibration. Per-class risk pools the evaluation pixels of the class; scene and label-count rows average the image loss over the evaluation images of the stratum; all numbers are means over splits (nan-skipped splits where the stratum is empty).

## alpha = 0.1

| Arm | Marginal risk (%) | Macro (class-mean) risk (%) | Worst class (%) | Classes > 2 alpha | Frequent third (%) | Medium third (%) | Rare third (%) | Images > 25% lost (%) | Images > 50% lost (%) | 90th pct image loss (%) | 1-3 labels (%) | 4-6 labels (%) | 7-10 labels (%) | 11- labels (%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| native_source | 9.87 | 8.95 | 49.5 | 7.1 | 10.57 | 6.80 | 7.52 | 13.5 | 3.8 | 32.1 | 10.60 | 10.67 | 7.97 | 7.65 |
| native_frozen | 14.73 | 15.96 | 79.8 | 15.5 | 15.37 | 10.22 | 17.63 | 21.2 | 7.3 | 43.6 | 15.61 | 15.88 | 12.11 | 12.28 |
| native_replay | 9.89 | 10.53 | 56.4 | 9.5 | 10.34 | 6.56 | 12.21 | 13.5 | 4.1 | 32.9 | 11.01 | 10.66 | 7.61 | 7.90 |
| anchored_frozen | 9.90 | 9.20 | 55.1 | 7.8 | 10.73 | 5.55 | 9.39 | 14.1 | 4.2 | 33.5 | 12.44 | 10.22 | 6.91 | 7.87 |

Worst classes (pixel-pooled miss rate, %):

- native_source: cloth 49, building 42, ground 40, shelves 25, cabinet 22, wood 21, bench 20, computer 19, mountain 17, truck 15
- native_frozen: cloth 80, building 54, ground 53, truck 42, wood 42, food 40, computer 37, flower 34, cabinet 33, shelves 31
- native_replay: cloth 56, building 43, ground 34, computer 31, food 31, truck 25, shelves 25, cabinet 24, flower 23, wood 22
- anchored_frozen: cloth 55, building 46, flower 29, food 27, computer 26, ground 25, wood 24, shelves 22, cabinet 20, floor 16

## alpha = 0.05

| Arm | Marginal risk (%) | Macro (class-mean) risk (%) | Worst class (%) | Classes > 2 alpha | Frequent third (%) | Medium third (%) | Rare third (%) | Images > 25% lost (%) | Images > 50% lost (%) | 90th pct image loss (%) | 1-3 labels (%) | 4-6 labels (%) | 7-10 labels (%) | 11- labels (%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| native_source | 4.89 | 4.00 | 27.2 | 6.7 | 5.32 | 3.17 | 3.04 | 6.5 | 1.3 | 14.8 | 5.82 | 4.98 | 3.91 | 3.84 |
| native_frozen | 8.45 | 9.01 | 49.7 | 16.5 | 8.85 | 5.61 | 10.55 | 11.7 | 3.2 | 28.8 | 9.66 | 9.01 | 6.43 | 6.79 |
| native_replay | 4.89 | 4.90 | 33.5 | 7.6 | 5.14 | 3.30 | 5.88 | 6.5 | 1.4 | 15.0 | 6.31 | 4.89 | 3.52 | 4.03 |
| anchored_frozen | 4.89 | 4.22 | 30.7 | 5.2 | 5.26 | 2.79 | 4.39 | 6.4 | 1.5 | 15.4 | 6.95 | 4.84 | 3.01 | 3.11 |

Worst classes (pixel-pooled miss rate, %):

- native_source: building 26, cloth 24, ground 18, shelves 14, wood 11, truck 10, cabinet 10, mountain 9, rock 8, bus 8
- native_frozen: cloth 48, building 39, computer 30, food 29, ground 27, shelves 22, keyboard 22, cabinet 21, truck 19, wood 18
- native_replay: building 28, cloth 27, keyboard 19, shelves 18, food 13, cabinet 13, ground 11, computer 11, rock 9, wood 8
- anchored_frozen: building 29, cloth 28, shelves 14, flower 13, cabinet 11, rock 9, computer 8, food 8, ground 7, wood 7

Classes are split into thirds by total sampled-pixel count (frequent third: person, sky, wall, building, ground, ...; rare third: light, truck, keyboard, bench, mouse, ...). native_source is the native model before growth (threshold and evaluation at the source vocabulary); native_frozen reuses that threshold after growth; native_replay recalibrates on the grown vocabulary; anchored_frozen calibrates once at the source vocabulary and its per-label scores do not change with growth. Stored scores are float16 logits clamped to [-30, 30].