# Conditional risk under source-calibrated thresholds: pascal_vitl_bank683

2000 Pascal Context validation images (0 without a source-labelled sampled pixel excluded), 59 source labels, 458 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration pascal_vitl_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
The CRC guarantee is on the marginal mean of the image loss (fraction of source-labelled sampled pixels whose label is missing from the set). Every stratum below is outside the guarantee for every arm; the table shows how the frozen thresholds behave inside them relative to recalibration. Per-class risk pools the evaluation pixels of the class; scene and label-count rows average the image loss over the evaluation images of the stratum; all numbers are means over splits (nan-skipped splits where the stratum is empty).

## alpha = 0.1

| Arm | Marginal risk (%) | Macro (class-mean) risk (%) | Worst class (%) | Classes > 2 alpha | Frequent third (%) | Medium third (%) | Rare third (%) | Images > 25% lost (%) | Images > 50% lost (%) | 90th pct image loss (%) | 1-3 labels (%) | 4-6 labels (%) | 7-10 labels (%) | 11- labels (%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| native_source | 9.87 | 9.61 | 48.8 | 7.6 | 10.41 | 7.49 | 8.64 | 13.0 | 3.6 | 31.3 | 10.40 | 10.66 | 8.07 | 8.85 |
| native_frozen | 15.05 | 17.42 | 74.6 | 18.8 | 15.41 | 11.61 | 21.24 | 21.7 | 7.1 | 43.8 | 15.44 | 16.33 | 12.61 | 13.46 |
| native_replay | 9.88 | 11.14 | 54.6 | 10.2 | 10.15 | 7.32 | 13.68 | 13.3 | 3.5 | 32.1 | 10.70 | 10.62 | 7.91 | 8.64 |
| anchored_frozen | 9.90 | 9.84 | 54.1 | 8.6 | 10.51 | 6.55 | 10.57 | 13.4 | 4.1 | 32.5 | 11.82 | 10.38 | 7.28 | 7.88 |

Worst classes (pixel-pooled miss rate, %):

- native_source: cloth 48, building 39, ground 38, shelves 29, wood 23, cabinet 21, mountain 20, bench 20, computer 19, truck 16
- native_frozen: cloth 75, ground 54, building 53, food 41, shelves 39, computer 37, wood 36, truck 35, sign 35, cabinet 34
- native_replay: cloth 54, building 41, ground 33, shelves 30, food 29, cabinet 24, computer 23, keyboard 22, wood 22, truck 20
- anchored_frozen: cloth 54, building 43, wood 30, food 28, ground 27, shelves 26, flower 23, cabinet 22, computer 17, truck 17

## alpha = 0.05

| Arm | Marginal risk (%) | Macro (class-mean) risk (%) | Worst class (%) | Classes > 2 alpha | Frequent third (%) | Medium third (%) | Rare third (%) | Images > 25% lost (%) | Images > 50% lost (%) | 90th pct image loss (%) | 1-3 labels (%) | 4-6 labels (%) | 7-10 labels (%) | 11- labels (%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| native_source | 4.88 | 4.67 | 28.1 | 7.9 | 5.17 | 3.60 | 4.20 | 6.1 | 1.4 | 14.5 | 5.92 | 4.93 | 3.76 | 4.50 |
| native_frozen | 8.56 | 9.60 | 48.7 | 19.4 | 8.79 | 6.27 | 11.87 | 11.3 | 2.9 | 27.6 | 9.61 | 9.04 | 6.74 | 7.54 |
| native_replay | 4.91 | 5.43 | 29.9 | 9.8 | 4.96 | 4.02 | 6.60 | 6.1 | 1.4 | 14.4 | 6.32 | 4.84 | 3.58 | 4.64 |
| anchored_frozen | 4.89 | 4.85 | 29.4 | 7.3 | 5.09 | 3.55 | 5.35 | 5.9 | 1.6 | 14.3 | 6.69 | 4.86 | 3.22 | 3.68 |

Worst classes (pixel-pooled miss rate, %):

- native_source: cloth 25, building 24, shelves 18, ground 16, truck 13, cabinet 11, computer 10, bench 10, rock 10, bedclothes 9
- native_frozen: cloth 48, building 38, shelves 27, ground 27, food 24, keyboard 22, cabinet 22, computer 20, truck 18, wood 18
- native_replay: cloth 27, building 26, shelves 18, cabinet 15, truck 14, computer 13, sign 12, ground 11, rock 11, food 10
- anchored_frozen: cloth 27, building 27, shelves 15, flower 15, cabinet 14, computer 13, rock 10, bedclothes 9, ground 9, mountain 9

Classes are split into thirds by total sampled-pixel count (frequent third: person, sky, wall, building, ground, ...; rare third: light, truck, keyboard, bench, mouse, ...). native_source is the native model before growth (threshold and evaluation at the source vocabulary); native_frozen reuses that threshold after growth; native_replay recalibrates on the grown vocabulary; anchored_frozen calibrates once at the source vocabulary and its per-label scores do not change with growth. Stored scores are float16 logits clamped to [-30, 30].