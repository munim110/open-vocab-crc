# Conditional risk under source-calibrated thresholds: pascal_fcclip_bank683

2000 Pascal Context validation images (0 without a source-labelled sampled pixel excluded), 59 source labels, 458 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration pascal_fcclip_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
The CRC guarantee is on the marginal mean of the image loss (fraction of source-labelled sampled pixels whose label is missing from the set). Every stratum below is outside the guarantee for every arm; the table shows how the frozen thresholds behave inside them relative to recalibration. Per-class risk pools the evaluation pixels of the class; scene and label-count rows average the image loss over the evaluation images of the stratum; all numbers are means over splits (nan-skipped splits where the stratum is empty).

## alpha = 0.1

| Arm | Marginal risk (%) | Macro (class-mean) risk (%) | Worst class (%) | Classes > 2 alpha | Frequent third (%) | Medium third (%) | Rare third (%) | Images > 25% lost (%) | Images > 50% lost (%) | 90th pct image loss (%) | 1-3 labels (%) | 4-6 labels (%) | 7-10 labels (%) | 11- labels (%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| native_source | 9.89 | 9.04 | 56.4 | 7.0 | 10.56 | 6.54 | 9.83 | 12.7 | 4.2 | 31.0 | 10.75 | 10.66 | 7.75 | 9.25 |
| native_frozen | 16.25 | 15.87 | 66.0 | 14.7 | 17.00 | 10.16 | 20.73 | 23.6 | 8.8 | 47.2 | 17.62 | 17.07 | 13.60 | 14.57 |
| native_replay | 9.86 | 9.30 | 56.3 | 7.8 | 10.48 | 6.11 | 11.33 | 12.8 | 4.2 | 31.1 | 10.40 | 10.80 | 7.88 | 8.10 |
| anchored_frozen | 9.89 | 10.43 | 71.5 | 9.6 | 10.50 | 5.79 | 13.01 | 13.5 | 3.9 | 32.1 | 10.54 | 10.32 | 8.23 | 12.04 |

Worst classes (pixel-pooled miss rate, %):

- native_source: plate 55, building 49, wood 39, shelves 32, cloth 25, ground 25, bench 20, truck 20, bedclothes 14, cabinet 13
- native_frozen: building 59, wood 59, plate 53, ground 48, truck 45, cloth 44, shelves 44, track 39, computer 36, cabinet 22
- native_replay: wood 54, building 47, ground 33, shelves 31, cloth 28, plate 23, computer 22, truck 19, bench 17, food 16
- anchored_frozen: light 71, wood 44, building 41, shelves 33, ground 32, cloth 27, food 22, plate 20, bag 20, cup 20

## alpha = 0.05

| Arm | Marginal risk (%) | Macro (class-mean) risk (%) | Worst class (%) | Classes > 2 alpha | Frequent third (%) | Medium third (%) | Rare third (%) | Images > 25% lost (%) | Images > 50% lost (%) | 90th pct image loss (%) | 1-3 labels (%) | 4-6 labels (%) | 7-10 labels (%) | 11- labels (%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| native_source | 4.89 | 4.13 | 32.7 | 6.3 | 5.34 | 2.95 | 4.33 | 5.6 | 1.6 | 14.2 | 5.84 | 5.03 | 3.71 | 4.51 |
| native_frozen | 8.56 | 8.05 | 51.3 | 13.0 | 9.15 | 5.24 | 9.80 | 10.9 | 3.5 | 27.2 | 9.10 | 9.34 | 6.85 | 6.88 |
| native_replay | 4.87 | 4.48 | 35.1 | 6.8 | 5.17 | 3.13 | 5.72 | 5.6 | 1.8 | 13.5 | 5.44 | 5.18 | 3.84 | 4.07 |
| anchored_frozen | 4.88 | 5.27 | 48.1 | 8.4 | 5.13 | 2.88 | 7.26 | 5.8 | 1.6 | 13.5 | 5.14 | 5.10 | 4.09 | 5.95 |

Worst classes (pixel-pooled miss rate, %):

- native_source: building 31, wood 20, shelves 20, cloth 15, truck 14, ground 13, bench 11, plate 9, book 8, light 6
- native_frozen: wood 49, building 43, ground 29, shelves 29, cloth 25, plate 19, truck 18, computer 16, bench 15, light 15
- native_replay: wood 34, building 28, shelves 25, cloth 18, ground 17, plate 11, light 9, bedclothes 7, sign 7, book 6
- anchored_frozen: light 48, wood 27, building 26, shelves 23, cloth 17, ground 15, plate 11, food 11, sign 8, cup 8

Classes are split into thirds by total sampled-pixel count (frequent third: person, sky, wall, building, ground, ...; rare third: light, truck, keyboard, bench, mouse, ...). native_source is the native model before growth (threshold and evaluation at the source vocabulary); native_frozen reuses that threshold after growth; native_replay recalibrates on the grown vocabulary; anchored_frozen calibrates once at the source vocabulary and its per-label scores do not change with growth. Stored scores are float16 logits clamped to [-30, 30].