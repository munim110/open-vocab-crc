# Conditional risk under source-calibrated thresholds: coco_declip_bank683

2000 COCO val2017 (LVIS-annotated) images (0 without a source-labelled sampled pixel excluded), 171 source labels, 1283 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration coco_declip_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
The CRC guarantee is on the marginal mean of the image loss (fraction of source-labelled sampled pixels whose label is missing from the set). Every stratum below is outside the guarantee for every arm; the table shows how the frozen thresholds behave inside them relative to recalibration. Per-class risk pools the evaluation pixels of the class; scene and label-count rows average the image loss over the evaluation images of the stratum; all numbers are means over splits (nan-skipped splits where the stratum is empty).

## alpha = 0.1

| Arm | Marginal risk (%) | Macro (class-mean) risk (%) | Worst class (%) | Classes > 2 alpha | Frequent third (%) | Medium third (%) | Rare third (%) | Images > 25% lost (%) | Images > 50% lost (%) | 90th pct image loss (%) | 1-3 labels (%) | 4-6 labels (%) | 7-10 labels (%) | 11- labels (%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| native_source | 9.91 | 17.36 | 100.0 | 45.8 | 7.73 | 18.91 | 18.33 | 11.7 | 3.2 | 28.0 | 8.01 | 9.97 | 10.27 | 10.30 |
| native_frozen | 12.93 | 22.26 | 100.0 | 60.7 | 9.95 | 24.68 | 25.04 | 16.0 | 4.9 | 35.8 | 12.33 | 13.09 | 12.50 | 13.48 |
| native_replay | 9.94 | 17.69 | 100.0 | 46.7 | 7.41 | 19.98 | 20.17 | 11.6 | 3.4 | 27.5 | 9.52 | 10.33 | 9.67 | 9.97 |
| anchored_frozen | 9.90 | 17.09 | 100.0 | 44.8 | 7.62 | 19.18 | 17.99 | 11.2 | 3.4 | 27.5 | 8.72 | 10.19 | 10.00 | 9.98 |

Worst classes (pixel-pooled miss rate, %):

- native_source: moss 100, salad 94, solid-other 88, structural-other 88, tent 88, waterdrops 83, cloth 80, floor-stone 75, mat 67, floor-marble 58
- native_frozen: moss 100, salad 100, cloth 96, waterdrops 95, mat 94, tent 89, solid-other 88, structural-other 88, plastic 77, floor-stone 75
- native_replay: moss 100, salad 96, cloth 94, tent 88, solid-other 84, structural-other 78, waterdrops 77, mat 65, plastic 65, floor-stone 60
- anchored_frozen: moss 100, salad 100, waterdrops 95, solid-other 88, tent 88, structural-other 81, cloth 76, floor-stone 63, mat 59, plastic 57

## alpha = 0.05

| Arm | Marginal risk (%) | Macro (class-mean) risk (%) | Worst class (%) | Classes > 2 alpha | Frequent third (%) | Medium third (%) | Rare third (%) | Images > 25% lost (%) | Images > 50% lost (%) | 90th pct image loss (%) | 1-3 labels (%) | 4-6 labels (%) | 7-10 labels (%) | 11- labels (%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| native_source | 4.93 | 10.10 | 99.7 | 42.3 | 3.45 | 11.18 | 10.97 | 5.1 | 1.5 | 13.8 | 4.19 | 5.21 | 5.19 | 4.63 |
| native_frozen | 6.83 | 13.07 | 99.9 | 57.2 | 4.80 | 14.79 | 15.47 | 7.1 | 2.0 | 19.0 | 5.72 | 7.50 | 6.73 | 6.64 |
| native_replay | 4.92 | 10.23 | 99.2 | 43.4 | 3.25 | 11.38 | 12.49 | 4.9 | 1.5 | 13.7 | 4.09 | 5.58 | 5.02 | 4.37 |
| anchored_frozen | 4.92 | 10.04 | 98.9 | 41.3 | 3.38 | 11.18 | 11.20 | 5.0 | 1.5 | 13.5 | 4.52 | 5.37 | 5.12 | 4.34 |

Worst classes (pixel-pooled miss rate, %):

- native_source: moss 100, salad 88, tent 81, solid-other 76, structural-other 58, waterdrops 56, floor-stone 48, cloth 46, mat 46, branch 44
- native_frozen: moss 100, salad 92, tent 84, solid-other 77, cloth 71, structural-other 62, waterdrops 59, mat 50, floor-stone 49, towel 49
- native_replay: moss 98, salad 91, tent 81, solid-other 73, cloth 62, towel 47, structural-other 45, mat 44, waterdrops 42, floor-stone 39
- anchored_frozen: moss 98, salad 88, tent 81, solid-other 77, waterdrops 53, cloth 49, structural-other 48, branch 47, floor-stone 44, mat 43

Classes are split into thirds by total sampled-pixel count (frequent third: person, sky-other, tree, wall-concrete, grass, ...; rare third: sports ball, baseball bat, toothbrush, waterdrops, hair drier, ...). native_source is the native model before growth (threshold and evaluation at the source vocabulary); native_frozen reuses that threshold after growth; native_replay recalibrates on the grown vocabulary; anchored_frozen calibrates once at the source vocabulary and its per-label scores do not change with growth. Stored scores are float16 logits clamped to [-30, 30].