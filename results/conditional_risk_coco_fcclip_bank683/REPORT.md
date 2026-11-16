# Conditional risk under source-calibrated thresholds: coco_fcclip_bank683

2000 COCO val2017 (LVIS-annotated) images (0 without a source-labelled sampled pixel excluded), 171 source labels, 1283 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration coco_fcclip_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
The CRC guarantee is on the marginal mean of the image loss (fraction of source-labelled sampled pixels whose label is missing from the set). Every stratum below is outside the guarantee for every arm; the table shows how the frozen thresholds behave inside them relative to recalibration. Per-class risk pools the evaluation pixels of the class; scene and label-count rows average the image loss over the evaluation images of the stratum; all numbers are means over splits (nan-skipped splits where the stratum is empty).

## alpha = 0.1

| Arm | Marginal risk (%) | Macro (class-mean) risk (%) | Worst class (%) | Classes > 2 alpha | Frequent third (%) | Medium third (%) | Rare third (%) | Images > 25% lost (%) | Images > 50% lost (%) | 90th pct image loss (%) | 1-3 labels (%) | 4-6 labels (%) | 7-10 labels (%) | 11- labels (%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| native_source | 9.89 | 9.99 | 92.6 | 25.4 | 9.27 | 13.34 | 6.29 | 12.7 | 3.5 | 28.5 | 6.57 | 8.98 | 9.65 | 12.73 |
| native_frozen | 17.09 | 15.98 | 99.3 | 39.8 | 16.57 | 18.84 | 13.38 | 26.2 | 8.4 | 45.8 | 13.74 | 16.30 | 17.19 | 19.42 |
| native_replay | 9.91 | 9.45 | 90.9 | 23.3 | 9.53 | 11.73 | 6.74 | 12.8 | 3.0 | 29.1 | 6.11 | 9.46 | 9.93 | 12.11 |
| anchored_frozen | 9.88 | 10.02 | 92.9 | 25.8 | 9.44 | 12.20 | 7.11 | 13.1 | 3.3 | 28.8 | 5.48 | 8.76 | 9.53 | 13.58 |

Worst classes (pixel-pooled miss rate, %):

- native_source: structural-other 87, furniture-other 81, tent 81, clothes 74, metal 72, solid-other 71, straw 63, plastic 53, moss 48, wood 47
- native_frozen: solid-other 98, clothes 95, structural-other 93, furniture-other 91, metal 89, tent 87, salad 83, plastic 80, straw 68, cloth 67
- native_replay: furniture-other 81, metal 80, structural-other 80, solid-other 75, tent 71, clothes 71, plastic 64, salad 54, straw 53, wood 49
- anchored_frozen: furniture-other 82, tent 81, structural-other 79, salad 74, solid-other 72, metal 70, straw 60, plastic 57, plant-other 53, wall-concrete 51

## alpha = 0.05

| Arm | Marginal risk (%) | Macro (class-mean) risk (%) | Worst class (%) | Classes > 2 alpha | Frequent third (%) | Medium third (%) | Rare third (%) | Images > 25% lost (%) | Images > 50% lost (%) | 90th pct image loss (%) | 1-3 labels (%) | 4-6 labels (%) | 7-10 labels (%) | 11- labels (%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| native_source | 4.90 | 5.23 | 78.5 | 22.3 | 4.47 | 7.35 | 2.64 | 4.4 | 1.3 | 14.0 | 2.24 | 4.72 | 4.68 | 6.55 |
| native_frozen | 9.78 | 9.33 | 90.6 | 36.1 | 9.41 | 11.60 | 6.61 | 12.6 | 2.9 | 28.8 | 6.02 | 9.33 | 9.81 | 11.96 |
| native_replay | 4.89 | 4.67 | 77.5 | 20.3 | 4.71 | 6.04 | 2.34 | 4.7 | 1.3 | 14.5 | 2.56 | 4.86 | 4.68 | 6.21 |
| anchored_frozen | 4.90 | 5.22 | 79.6 | 23.3 | 4.61 | 6.50 | 3.09 | 4.6 | 1.1 | 15.2 | 1.67 | 4.57 | 4.57 | 7.12 |

Worst classes (pixel-pooled miss rate, %):

- native_source: structural-other 67, furniture-other 60, metal 50, tent 47, straw 47, waterdrops 38, moss 37, plastic 34, clothes 32, wood 31
- native_frozen: furniture-other 81, metal 80, structural-other 79, solid-other 75, clothes 70, tent 70, plastic 64, straw 53, salad 53, wood 49
- native_replay: structural-other 67, furniture-other 62, metal 61, plastic 39, moss 37, waterdrops 36, solid-other 30, wood 28, straw 28, textile-other 27
- anchored_frozen: structural-other 68, furniture-other 58, metal 44, solid-other 42, salad 39, waterdrops 39, plastic 37, moss 37, straw 36, tent 35

Classes are split into thirds by total sampled-pixel count (frequent third: person, sky-other, tree, wall-concrete, grass, ...; rare third: sports ball, baseball bat, toothbrush, waterdrops, hair drier, ...). native_source is the native model before growth (threshold and evaluation at the source vocabulary); native_frozen reuses that threshold after growth; native_replay recalibrates on the grown vocabulary; anchored_frozen calibrates once at the source vocabulary and its per-label scores do not change with growth. Stored scores are float16 logits clamped to [-30, 30].