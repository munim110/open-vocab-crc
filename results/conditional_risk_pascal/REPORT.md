# Conditional risk under source-calibrated thresholds: pascal_vitb_coco171

2000 Pascal Context validation images (0 without a source-labelled sampled pixel excluded), 59 source labels, 458 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration pascal_vitb_coco171. Development data; nothing is fitted; the confirmation reserve is untouched.
The CRC guarantee is on the marginal mean of the image loss (fraction of source-labelled sampled pixels whose label is missing from the set). Every stratum below is outside the guarantee for every arm; the table shows how the frozen thresholds behave inside them relative to recalibration. Per-class risk pools the evaluation pixels of the class; scene and label-count rows average the image loss over the evaluation images of the stratum; all numbers are means over splits (nan-skipped splits where the stratum is empty).

## alpha = 0.1

| Arm | Marginal risk (%) | Macro (class-mean) risk (%) | Worst class (%) | Classes > 2 alpha | Frequent third (%) | Medium third (%) | Rare third (%) | Images > 25% lost (%) | Images > 50% lost (%) | 90th pct image loss (%) | 1-3 labels (%) | 4-6 labels (%) | 7-10 labels (%) | 11- labels (%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| native_source | 9.87 | 10.47 | 54.7 | 7.2 | 10.20 | 8.14 | 10.06 | 12.8 | 3.5 | 31.7 | 10.29 | 10.48 | 8.39 | 9.66 |
| native_frozen | 15.17 | 19.36 | 80.4 | 21.4 | 15.18 | 12.75 | 23.97 | 22.1 | 7.2 | 43.4 | 15.73 | 16.38 | 12.54 | 14.77 |
| native_replay | 9.88 | 12.21 | 59.6 | 11.5 | 9.96 | 7.92 | 15.32 | 13.1 | 4.1 | 32.4 | 10.62 | 10.56 | 8.03 | 9.19 |
| anchored_frozen | 9.87 | 9.47 | 48.1 | 8.1 | 10.69 | 5.55 | 11.40 | 13.7 | 3.6 | 32.7 | 11.24 | 10.21 | 7.79 | 10.47 |

Worst classes (pixel-pooled miss rate, %):

- native_source: cloth 55, ground 38, building 37, shelves 29, bench 22, wood 21, mountain 20, bedclothes 18, cabinet 18, computer 17
- native_frozen: cloth 80, building 51, computer 50, ground 49, bag 45, food 43, truck 41, shelves 39, wood 39, sign 33
- native_replay: cloth 59, building 41, bag 32, computer 32, ground 31, shelves 31, food 28, keyboard 23, sign 22, cabinet 22
- anchored_frozen: cloth 47, building 41, track 39, water 33, shelves 24, ground 23, floor 23, wood 19, food 18, table 17

## alpha = 0.05

| Arm | Marginal risk (%) | Macro (class-mean) risk (%) | Worst class (%) | Classes > 2 alpha | Frequent third (%) | Medium third (%) | Rare third (%) | Images > 25% lost (%) | Images > 50% lost (%) | 90th pct image loss (%) | 1-3 labels (%) | 4-6 labels (%) | 7-10 labels (%) | 11- labels (%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| native_source | 4.88 | 4.74 | 28.1 | 7.5 | 5.12 | 3.94 | 4.34 | 6.1 | 1.5 | 13.8 | 5.69 | 4.98 | 3.89 | 4.57 |
| native_frozen | 8.40 | 10.31 | 53.0 | 21.0 | 8.50 | 6.80 | 12.83 | 11.2 | 3.0 | 27.9 | 9.20 | 8.89 | 6.78 | 7.79 |
| native_replay | 4.89 | 5.84 | 33.0 | 10.0 | 4.92 | 4.39 | 6.70 | 6.1 | 1.3 | 13.8 | 5.94 | 5.00 | 3.66 | 4.33 |
| anchored_frozen | 4.88 | 4.27 | 27.4 | 6.5 | 5.31 | 2.91 | 4.45 | 6.5 | 1.8 | 14.3 | 6.33 | 4.95 | 3.26 | 4.58 |

Worst classes (pixel-pooled miss rate, %):

- native_source: cloth 27, building 23, shelves 19, ground 17, bedclothes 13, mountain 12, bag 9, bench 9, cabinet 8, light 8
- native_frozen: cloth 53, building 37, shelves 28, bag 27, ground 26, computer 25, food 23, keyboard 22, sign 20, cabinet 19
- native_replay: cloth 33, building 27, shelves 18, bag 15, sign 14, mouse 12, bedclothes 11, cabinet 10, ground 10, keyboard 10
- anchored_frozen: building 27, cloth 18, shelves 15, water 14, bedclothes 10, bag 9, ground 9, floor 9, mountain 9, food 7

Classes are split into thirds by total sampled-pixel count (frequent third: person, sky, wall, building, ground, ...; rare third: light, truck, keyboard, bench, mouse, ...). native_source is the native model before growth (threshold and evaluation at the source vocabulary); native_frozen reuses that threshold after growth; native_replay recalibrates on the grown vocabulary; anchored_frozen calibrates once at the source vocabulary and its per-label scores do not change with growth. Stored scores are float16 logits clamped to [-30, 30].