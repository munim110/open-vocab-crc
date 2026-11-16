# Conditional risk under source-calibrated thresholds: pascal_sed_bank683

2000 Pascal Context validation images (0 without a source-labelled sampled pixel excluded), 59 source labels, 458 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration pascal_sed_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
The CRC guarantee is on the marginal mean of the image loss (fraction of source-labelled sampled pixels whose label is missing from the set). Every stratum below is outside the guarantee for every arm; the table shows how the frozen thresholds behave inside them relative to recalibration. Per-class risk pools the evaluation pixels of the class; scene and label-count rows average the image loss over the evaluation images of the stratum; all numbers are means over splits (nan-skipped splits where the stratum is empty).

## alpha = 0.1

| Arm | Marginal risk (%) | Macro (class-mean) risk (%) | Worst class (%) | Classes > 2 alpha | Frequent third (%) | Medium third (%) | Rare third (%) | Images > 25% lost (%) | Images > 50% lost (%) | 90th pct image loss (%) | 1-3 labels (%) | 4-6 labels (%) | 7-10 labels (%) | 11- labels (%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| native_source | 9.90 | 10.01 | 66.9 | 8.3 | 10.51 | 6.94 | 8.38 | 13.2 | 3.9 | 31.3 | 10.97 | 10.50 | 7.89 | 8.61 |
| native_frozen | 4.65 | 5.67 | 45.9 | 3.4 | 4.74 | 3.46 | 5.99 | 5.8 | 1.3 | 13.6 | 6.10 | 4.83 | 2.94 | 3.81 |
| native_replay | 9.91 | 12.14 | 73.9 | 10.9 | 10.18 | 7.00 | 13.85 | 13.1 | 3.8 | 31.0 | 11.27 | 10.47 | 7.60 | 9.18 |
| anchored_frozen | 9.90 | 10.90 | 66.4 | 9.3 | 10.45 | 6.15 | 11.70 | 13.4 | 4.0 | 31.9 | 11.91 | 10.50 | 6.87 | 9.13 |

Worst classes (pixel-pooled miss rate, %):

- native_source: cloth 67, ground 38, computer 37, building 37, cabinet 23, truck 22, shelves 22, wood 21, mountain 19, keyboard 18
- native_frozen: cloth 44, computer 26, building 23, keyboard 22, truck 14, shelves 12, cabinet 11, book 10, wood 10, bag 9
- native_replay: cloth 73, computer 52, truck 44, building 38, bag 31, ground 27, wood 25, food 25, keyboard 23, cabinet 21
- anchored_frozen: cloth 66, building 38, computer 37, food 34, flower 28, water 28, bag 27, keyboard 22, cabinet 20, mountain 18

## alpha = 0.05

| Arm | Marginal risk (%) | Macro (class-mean) risk (%) | Worst class (%) | Classes > 2 alpha | Frequent third (%) | Medium third (%) | Rare third (%) | Images > 25% lost (%) | Images > 50% lost (%) | 90th pct image loss (%) | 1-3 labels (%) | 4-6 labels (%) | 7-10 labels (%) | 11- labels (%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| native_source | 4.90 | 4.80 | 37.6 | 8.0 | 5.21 | 3.53 | 3.60 | 5.8 | 1.1 | 14.7 | 5.99 | 5.06 | 3.57 | 4.19 |
| native_frozen | 2.07 | 2.53 | 26.8 | 3.2 | 2.07 | 1.78 | 2.56 | 2.3 | 0.6 | 4.0 | 3.11 | 1.96 | 1.21 | 1.59 |
| native_replay | 4.90 | 5.98 | 47.5 | 9.2 | 5.00 | 3.63 | 6.32 | 6.1 | 1.4 | 14.6 | 6.35 | 5.11 | 3.12 | 4.03 |
| anchored_frozen | 4.90 | 5.43 | 37.7 | 8.9 | 5.06 | 3.48 | 5.49 | 6.1 | 1.4 | 14.0 | 6.89 | 4.83 | 3.05 | 3.90 |

Worst classes (pixel-pooled miss rate, %):

- native_source: cloth 37, building 23, computer 18, ground 16, cabinet 11, shelves 11, wood 10, mountain 9, bench 9, keyboard 8
- native_frozen: keyboard 19, cloth 15, building 13, computer 11, cabinet 7, book 6, rock 6, shelves 6, wood 4, mountain 4
- native_replay: cloth 46, computer 27, building 24, keyboard 22, truck 16, shelves 13, cabinet 12, wood 11, book 10, bag 9
- anchored_frozen: cloth 37, building 23, computer 22, keyboard 17, flower 15, water 13, mountain 12, shelves 11, cabinet 10, food 10

Classes are split into thirds by total sampled-pixel count (frequent third: person, sky, wall, building, ground, ...; rare third: light, truck, keyboard, bench, mouse, ...). native_source is the native model before growth (threshold and evaluation at the source vocabulary); native_frozen reuses that threshold after growth; native_replay recalibrates on the grown vocabulary; anchored_frozen calibrates once at the source vocabulary and its per-label scores do not change with growth. Stored scores are float16 logits clamped to [-30, 30].