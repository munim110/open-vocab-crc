# Conditional risk under source-calibrated thresholds: coco_vitb_bank683

2000 COCO val2017 (LVIS-annotated) images (0 without a source-labelled sampled pixel excluded), 171 source labels, 1283 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration coco_vitb_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
The CRC guarantee is on the marginal mean of the image loss (fraction of source-labelled sampled pixels whose label is missing from the set). Every stratum below is outside the guarantee for every arm; the table shows how the frozen thresholds behave inside them relative to recalibration. Per-class risk pools the evaluation pixels of the class; scene and label-count rows average the image loss over the evaluation images of the stratum; all numbers are means over splits (nan-skipped splits where the stratum is empty).

## alpha = 0.1

| Arm | Marginal risk (%) | Macro (class-mean) risk (%) | Worst class (%) | Classes > 2 alpha | Frequent third (%) | Medium third (%) | Rare third (%) | Images > 25% lost (%) | Images > 50% lost (%) | 90th pct image loss (%) | 1-3 labels (%) | 4-6 labels (%) | 7-10 labels (%) | 11- labels (%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| native_source | 9.93 | 19.29 | 100.0 | 54.3 | 7.49 | 19.29 | 22.05 | 11.2 | 3.0 | 27.2 | 6.90 | 10.01 | 10.21 | 10.85 |
| native_frozen | 12.96 | 24.86 | 100.0 | 70.7 | 9.57 | 25.62 | 29.49 | 16.0 | 5.0 | 34.6 | 11.25 | 13.07 | 12.59 | 14.00 |
| native_replay | 9.94 | 20.19 | 100.0 | 57.5 | 7.05 | 20.69 | 24.59 | 11.0 | 3.5 | 27.0 | 7.96 | 10.54 | 9.57 | 10.49 |
| anchored_frozen | 9.92 | 19.02 | 100.0 | 53.6 | 7.25 | 20.01 | 22.47 | 10.4 | 3.3 | 25.9 | 7.97 | 10.31 | 9.81 | 10.44 |

Worst classes (pixel-pooled miss rate, %):

- native_source: moss 100, salad 91, tent 90, structural-other 86, cloth 85, waterdrops 83, solid-other 82, mat 77, floor-stone 64, wall-panel 64
- native_frozen: moss 100, cloth 100, salad 91, tent 91, structural-other 88, mat 87, pillow 84, solid-other 84, waterdrops 83, clothes 82
- native_replay: moss 100, cloth 98, salad 91, tent 90, solid-other 81, structural-other 75, waterdrops 75, mat 69, tie 65, plastic 65
- anchored_frozen: moss 100, salad 91, tent 90, solid-other 84, cloth 82, waterdrops 81, structural-other 75, mat 60, plastic 60, branch 59

## alpha = 0.05

| Arm | Marginal risk (%) | Macro (class-mean) risk (%) | Worst class (%) | Classes > 2 alpha | Frequent third (%) | Medium third (%) | Rare third (%) | Images > 25% lost (%) | Images > 50% lost (%) | 90th pct image loss (%) | 1-3 labels (%) | 4-6 labels (%) | 7-10 labels (%) | 11- labels (%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| native_source | 4.92 | 10.92 | 98.9 | 49.3 | 3.34 | 11.25 | 12.40 | 5.3 | 1.3 | 12.7 | 3.57 | 5.41 | 5.06 | 4.78 |
| native_frozen | 6.96 | 15.43 | 99.3 | 70.2 | 4.66 | 15.35 | 19.42 | 7.3 | 2.1 | 18.5 | 4.89 | 7.90 | 6.63 | 7.10 |
| native_replay | 4.92 | 11.83 | 97.7 | 54.6 | 3.09 | 11.56 | 15.29 | 4.9 | 1.3 | 12.6 | 3.26 | 5.73 | 4.84 | 4.75 |
| anchored_frozen | 4.92 | 11.41 | 97.9 | 52.5 | 3.16 | 11.58 | 14.18 | 4.7 | 1.5 | 12.0 | 3.87 | 5.56 | 4.78 | 4.75 |

Worst classes (pixel-pooled miss rate, %):

- native_source: moss 99, salad 84, tent 80, solid-other 76, mat 57, structural-other 51, cloth 50, towel 47, floor-stone 44, wall-panel 42
- native_frozen: moss 98, cloth 89, salad 87, tent 86, solid-other 77, waterdrops 64, mat 59, structural-other 58, tie 51, pillow 50
- native_replay: moss 90, salad 85, cloth 81, tent 80, solid-other 72, mat 56, towel 47, structural-other 46, tie 38, floor-stone 36
- anchored_frozen: moss 93, salad 86, tent 78, solid-other 77, waterdrops 63, cloth 54, branch 49, mat 48, towel 47, structural-other 44

Classes are split into thirds by total sampled-pixel count (frequent third: person, sky-other, tree, wall-concrete, grass, ...; rare third: sports ball, baseball bat, toothbrush, waterdrops, hair drier, ...). native_source is the native model before growth (threshold and evaluation at the source vocabulary); native_frozen reuses that threshold after growth; native_replay recalibrates on the grown vocabulary; anchored_frozen calibrates once at the source vocabulary and its per-label scores do not change with growth. Stored scores are float16 logits clamped to [-30, 30].