# Conditional risk under source-calibrated thresholds: coco_sed_bank683

2000 COCO val2017 (LVIS-annotated) images (0 without a source-labelled sampled pixel excluded), 171 source labels, 1283 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration coco_sed_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
The CRC guarantee is on the marginal mean of the image loss (fraction of source-labelled sampled pixels whose label is missing from the set). Every stratum below is outside the guarantee for every arm; the table shows how the frozen thresholds behave inside them relative to recalibration. Per-class risk pools the evaluation pixels of the class; scene and label-count rows average the image loss over the evaluation images of the stratum; all numbers are means over splits (nan-skipped splits where the stratum is empty).

## alpha = 0.1

| Arm | Marginal risk (%) | Macro (class-mean) risk (%) | Worst class (%) | Classes > 2 alpha | Frequent third (%) | Medium third (%) | Rare third (%) | Images > 25% lost (%) | Images > 50% lost (%) | 90th pct image loss (%) | 1-3 labels (%) | 4-6 labels (%) | 7-10 labels (%) | 11- labels (%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| native_source | 9.93 | 17.90 | 100.0 | 50.0 | 7.63 | 19.24 | 19.58 | 11.4 | 3.4 | 27.8 | 8.21 | 9.95 | 10.16 | 10.42 |
| native_frozen | 3.64 | 8.62 | 96.7 | 20.1 | 2.15 | 8.88 | 11.94 | 3.3 | 1.1 | 9.0 | 2.93 | 3.96 | 3.64 | 3.58 |
| native_replay | 9.92 | 18.83 | 100.0 | 51.6 | 7.04 | 20.55 | 22.26 | 10.6 | 3.2 | 26.1 | 7.20 | 9.92 | 9.76 | 11.30 |
| anchored_frozen | 9.92 | 18.62 | 100.0 | 50.9 | 7.17 | 20.85 | 20.52 | 11.1 | 3.3 | 26.9 | 7.39 | 10.10 | 10.20 | 10.52 |

Worst classes (pixel-pooled miss rate, %):

- native_source: moss 100, salad 100, cloth 92, solid-other 89, tent 86, structural-other 82, mat 72, waterdrops 64, branch 62, floor-marble 59
- native_frozen: salad 90, cloth 77, solid-other 76, tent 73, moss 67, towel 46, mat 43, floor-marble 37, railing 33, plastic 30
- native_replay: salad 100, moss 100, cloth 95, solid-other 89, tent 88, plastic 75, structural-other 72, waterdrops 67, furniture-other 61, mat 59
- anchored_frozen: moss 100, salad 100, solid-other 95, cloth 91, tent 87, structural-other 72, waterdrops 72, branch 64, leaves 60, tie 58

## alpha = 0.05

| Arm | Marginal risk (%) | Macro (class-mean) risk (%) | Worst class (%) | Classes > 2 alpha | Frequent third (%) | Medium third (%) | Rare third (%) | Images > 25% lost (%) | Images > 50% lost (%) | 90th pct image loss (%) | 1-3 labels (%) | 4-6 labels (%) | 7-10 labels (%) | 11- labels (%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| native_source | 4.92 | 10.43 | 99.7 | 45.7 | 3.28 | 11.79 | 11.62 | 5.3 | 1.5 | 13.3 | 4.43 | 5.07 | 5.20 | 4.66 |
| native_frozen | 1.62 | 4.49 | 90.4 | 17.7 | 0.87 | 4.19 | 6.24 | 1.4 | 0.5 | 3.0 | 1.14 | 1.78 | 1.81 | 1.41 |
| native_replay | 4.91 | 11.00 | 98.8 | 49.9 | 3.05 | 11.55 | 14.56 | 4.5 | 1.3 | 12.6 | 3.55 | 5.20 | 4.89 | 5.17 |
| anchored_frozen | 4.92 | 10.94 | 99.8 | 47.8 | 3.05 | 12.23 | 13.29 | 4.8 | 1.3 | 12.8 | 4.05 | 5.07 | 5.09 | 4.93 |

Worst classes (pixel-pooled miss rate, %):

- native_source: moss 100, salad 90, solid-other 84, tent 77, cloth 61, mat 51, structural-other 49, floor-marble 48, floor-stone 46, towel 43
- native_frozen: salad 82, solid-other 58, tent 55, moss 39, mat 34, cloth 28, floor-marble 27, light 20, railing 19, straw 15
- native_replay: salad 95, moss 90, cloth 85, solid-other 81, tent 77, towel 50, mat 45, floor-marble 43, structural-other 40, railing 39
- anchored_frozen: moss 100, salad 93, solid-other 89, tent 78, cloth 65, branch 53, floor-marble 45, mat 44, towel 42, waterdrops 42

Classes are split into thirds by total sampled-pixel count (frequent third: person, sky-other, tree, wall-concrete, grass, ...; rare third: sports ball, baseball bat, toothbrush, waterdrops, hair drier, ...). native_source is the native model before growth (threshold and evaluation at the source vocabulary); native_frozen reuses that threshold after growth; native_replay recalibrates on the grown vocabulary; anchored_frozen calibrates once at the source vocabulary and its per-label scores do not change with growth. Stored scores are float16 logits clamped to [-30, 30].