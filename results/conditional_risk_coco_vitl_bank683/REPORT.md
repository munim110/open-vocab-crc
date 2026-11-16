# Conditional risk under source-calibrated thresholds: coco_vitl_bank683

2000 COCO val2017 (LVIS-annotated) images (0 without a source-labelled sampled pixel excluded), 171 source labels, 1283 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration coco_vitl_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
The CRC guarantee is on the marginal mean of the image loss (fraction of source-labelled sampled pixels whose label is missing from the set). Every stratum below is outside the guarantee for every arm; the table shows how the frozen thresholds behave inside them relative to recalibration. Per-class risk pools the evaluation pixels of the class; scene and label-count rows average the image loss over the evaluation images of the stratum; all numbers are means over splits (nan-skipped splits where the stratum is empty).

## alpha = 0.1

| Arm | Marginal risk (%) | Macro (class-mean) risk (%) | Worst class (%) | Classes > 2 alpha | Frequent third (%) | Medium third (%) | Rare third (%) | Images > 25% lost (%) | Images > 50% lost (%) | 90th pct image loss (%) | 1-3 labels (%) | 4-6 labels (%) | 7-10 labels (%) | 11- labels (%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| native_source | 9.93 | 18.07 | 100.0 | 48.7 | 7.68 | 19.03 | 19.17 | 11.7 | 3.1 | 27.9 | 7.97 | 9.92 | 10.19 | 10.49 |
| native_frozen | 12.88 | 23.22 | 100.0 | 64.2 | 9.77 | 25.07 | 25.69 | 16.4 | 4.8 | 35.3 | 11.64 | 13.14 | 12.57 | 13.47 |
| native_replay | 9.95 | 18.95 | 100.0 | 50.5 | 7.22 | 20.56 | 21.53 | 11.6 | 3.3 | 27.8 | 8.84 | 10.38 | 9.66 | 10.23 |
| anchored_frozen | 9.92 | 17.98 | 100.0 | 48.8 | 7.45 | 19.84 | 19.50 | 11.2 | 3.3 | 27.0 | 8.44 | 10.06 | 9.99 | 10.33 |

Worst classes (pixel-pooled miss rate, %):

- native_source: moss 100, salad 98, mat 90, structural-other 89, tent 88, cloth 85, solid-other 81, waterdrops 77, wall-panel 64, floor-stone 61
- native_frozen: moss 100, salad 100, hair drier 99, cloth 98, mat 96, tent 90, waterdrops 89, structural-other 89, solid-other 81, plastic 76
- native_replay: moss 100, salad 98, cloth 96, tent 89, mat 89, structural-other 79, solid-other 78, waterdrops 73, hair drier 67, clothes 63
- anchored_frozen: moss 100, salad 99, tent 89, structural-other 82, cloth 82, solid-other 80, waterdrops 79, mat 78, plastic 63, wall-panel 60

## alpha = 0.05

| Arm | Marginal risk (%) | Macro (class-mean) risk (%) | Worst class (%) | Classes > 2 alpha | Frequent third (%) | Medium third (%) | Rare third (%) | Images > 25% lost (%) | Images > 50% lost (%) | 90th pct image loss (%) | 1-3 labels (%) | 4-6 labels (%) | 7-10 labels (%) | 11- labels (%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| native_source | 4.92 | 10.21 | 98.9 | 43.7 | 3.40 | 11.47 | 10.37 | 4.9 | 1.5 | 13.6 | 4.12 | 5.18 | 5.24 | 4.59 |
| native_frozen | 7.02 | 14.46 | 99.3 | 63.2 | 4.81 | 15.56 | 16.85 | 7.2 | 2.2 | 19.4 | 5.89 | 7.71 | 6.82 | 6.90 |
| native_replay | 4.92 | 10.66 | 98.1 | 47.2 | 3.24 | 11.59 | 12.04 | 5.1 | 1.5 | 12.6 | 4.03 | 5.48 | 4.97 | 4.57 |
| anchored_frozen | 4.90 | 10.12 | 98.4 | 43.6 | 3.38 | 11.23 | 10.80 | 4.9 | 1.7 | 12.2 | 4.86 | 5.33 | 4.93 | 4.37 |

Worst classes (pixel-pooled miss rate, %):

- native_source: moss 97, salad 87, tent 82, solid-other 73, structural-other 62, mat 50, waterdrops 48, floor-stone 46, cloth 43, branch 38
- native_frozen: moss 97, salad 92, cloth 86, tent 86, solid-other 73, mat 72, structural-other 67, hair drier 59, waterdrops 56, plastic 47
- native_replay: salad 90, moss 82, tent 81, solid-other 71, cloth 68, structural-other 51, mat 47, waterdrops 40, plastic 35, furniture-other 34
- anchored_frozen: moss 95, salad 86, tent 81, solid-other 74, structural-other 50, branch 49, waterdrops 49, cloth 47, mat 45, floor-stone 35

Classes are split into thirds by total sampled-pixel count (frequent third: person, sky-other, tree, wall-concrete, grass, ...; rare third: sports ball, baseball bat, toothbrush, waterdrops, hair drier, ...). native_source is the native model before growth (threshold and evaluation at the source vocabulary); native_frozen reuses that threshold after growth; native_replay recalibrates on the grown vocabulary; anchored_frozen calibrates once at the source vocabulary and its per-label scores do not change with growth. Stored scores are float16 logits clamped to [-30, 30].