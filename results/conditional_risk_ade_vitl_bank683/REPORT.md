# Conditional risk under source-calibrated thresholds: vitl_bank683

2000 ADE validation images (0 without a source-labelled sampled pixel excluded), 150 source labels, 845 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration vitl_bank683. Development data; nothing is fitted; the confirmation reserve is untouched.
The CRC guarantee is on the marginal mean of the image loss (fraction of source-labelled sampled pixels whose label is missing from the set). Every stratum below is outside the guarantee for every arm; the table shows how the frozen thresholds behave inside them relative to recalibration. Per-class risk pools the evaluation pixels of the class; scene and label-count rows average the image loss over the evaluation images of the stratum; all numbers are means over splits (nan-skipped splits where the stratum is empty).

## alpha = 0.1

| Arm | Marginal risk (%) | Macro (class-mean) risk (%) | Worst class (%) | Classes > 2 alpha | Frequent third (%) | Medium third (%) | Rare third (%) | Worst scene (%) | Scenes > 2 alpha | Images > 25% lost (%) | Images > 50% lost (%) | 90th pct image loss (%) | 1-3 labels (%) | 4-6 labels (%) | 7-10 labels (%) | 11- labels (%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| native_source | 9.90 | 20.17 | 100.0 | 48.5 | 8.63 | 20.48 | 23.81 | 10.6 | 0 | 11.3 | 2.9 | 27.3 | 12.29 | 11.72 | 9.44 | 7.66 |
| native_frozen | 15.22 | 30.21 | 100.0 | 70.5 | 13.20 | 31.16 | 37.22 | 15.4 | 0 | 20.0 | 6.7 | 40.7 | 22.35 | 18.32 | 13.84 | 11.17 |
| native_replay | 9.91 | 20.57 | 100.0 | 49.6 | 8.45 | 21.50 | 24.10 | 9.7 | 0 | 12.1 | 3.6 | 28.8 | 14.93 | 12.40 | 8.86 | 6.81 |
| anchored_frozen | 9.88 | 16.60 | 100.0 | 39.9 | 8.87 | 15.90 | 18.70 | 12.2 | 0 | 12.4 | 3.6 | 29.0 | 14.96 | 12.62 | 8.87 | 6.44 |

Worst classes (pixel-pooled miss rate, %):

- native_source: buffet, counter, sideboard 100, case, display case, showcase, vitrine 100, base, pedestal, stand 100, pillow 89, hood, exhaust hood 82, blanket, cover 80, earth, ground 78, screen door, screen 77, canopy 76, hovel, hut, hutch, shack, shanty 75
- native_frozen: base, pedestal, stand 100, case, display case, showcase, vitrine 100, buffet, counter, sideboard 100, hovel, hut, hutch, shack, shanty 99, canopy 95, screen door, screen 95, pillow 94, screen, crt screen 92, blanket, cover 92, hood, exhaust hood 89
- native_replay: buffet, counter, sideboard 100, base, pedestal, stand 100, case, display case, showcase, vitrine 100, hovel, hut, hutch, shack, shanty 95, canopy 87, pillow 85, hood, exhaust hood 81, screen door, screen 79, blanket, cover 76, screen, crt screen 76
- anchored_frozen: case, display case, showcase, vitrine 100, buffet, counter, sideboard 100, base, pedestal, stand 100, earth, ground 86, hood, exhaust hood 78, canopy 77, hovel, hut, hutch, shack, shanty 68, step, stair 63, box 61, tray 58

Worst scenes (image-level risk, %):

- native_source: misc 11, dining_room 9, bathroom 8, bedroom 7, living_room 7
- native_frozen: misc 15, bathroom 13, dining_room 13, living_room 10, bedroom 10
- native_replay: misc 10, dining_room 8, bathroom 8, bedroom 7, living_room 6
- anchored_frozen: bathroom 12, misc 10, dining_room 8, kitchen 6, bedroom 5

## alpha = 0.05

| Arm | Marginal risk (%) | Macro (class-mean) risk (%) | Worst class (%) | Classes > 2 alpha | Frequent third (%) | Medium third (%) | Rare third (%) | Worst scene (%) | Scenes > 2 alpha | Images > 25% lost (%) | Images > 50% lost (%) | 90th pct image loss (%) | 1-3 labels (%) | 4-6 labels (%) | 7-10 labels (%) | 11- labels (%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| native_source | 4.89 | 10.86 | 99.9 | 40.7 | 4.20 | 10.60 | 11.12 | 5.2 | 0 | 4.9 | 1.4 | 12.8 | 6.84 | 6.10 | 4.47 | 3.44 |
| native_frozen | 8.38 | 17.69 | 100.0 | 64.2 | 7.11 | 18.52 | 20.24 | 8.2 | 0 | 9.7 | 2.8 | 24.2 | 12.78 | 10.71 | 7.38 | 5.59 |
| native_replay | 4.90 | 11.30 | 100.0 | 42.0 | 4.08 | 11.19 | 12.15 | 4.9 | 0 | 5.3 | 1.6 | 13.5 | 8.35 | 6.49 | 4.11 | 2.99 |
| anchored_frozen | 4.89 | 9.36 | 99.6 | 36.4 | 4.34 | 7.83 | 9.12 | 5.2 | 0 | 5.3 | 1.5 | 13.0 | 8.12 | 6.61 | 4.20 | 2.77 |

Worst classes (pixel-pooled miss rate, %):

- native_source: case, display case, showcase, vitrine 100, buffet, counter, sideboard 99, base, pedestal, stand 99, hood, exhaust hood 63, pillow 62, blanket, cover 57, canopy 55, earth, ground 50, box 47, screen door, screen 47
- native_frozen: case, display case, showcase, vitrine 100, base, pedestal, stand 100, buffet, counter, sideboard 100, hovel, hut, hutch, shack, shanty 90, canopy 86, pillow 79, hood, exhaust hood 75, blanket, cover 72, screen door, screen 70, earth, ground 66
- native_replay: case, display case, showcase, vitrine 100, base, pedestal, stand 99, buffet, counter, sideboard 95, canopy 79, hood, exhaust hood 61, hovel, hut, hutch, shack, shanty 55, box 52, pillow 50, blanket, cover 50, screen door, screen 45
- anchored_frozen: case, display case, showcase, vitrine 99, base, pedestal, stand 99, buffet, counter, sideboard 95, hood, exhaust hood 60, earth, ground 54, box 47, step, stair 45, tank, storage tank 42, tray 42, traffic light, traffic signal, stoplight 40

Worst scenes (image-level risk, %):

- native_source: dining_room 5, misc 5, bathroom 4, bedroom 4, kitchen 3
- native_frozen: misc 8, dining_room 7, bathroom 7, bedroom 6, living_room 4
- native_replay: misc 5, dining_room 5, bathroom 4, bedroom 3, kitchen 2
- anchored_frozen: misc 5, dining_room 5, bathroom 3, kitchen 2, living_room 2

Classes are split into thirds by total sampled-pixel count (frequent third: wall, building, edifice, sky, floor, flooring, tree, ...; rare third: bicycle, bike, wheel, cycle, clock, pier, wharf, wharfage, dock, shower, barrel, cask, ...). Scenes with at least 20 kept images: 10. native_source is the native model before growth (threshold and evaluation at the source vocabulary); native_frozen reuses that threshold after growth; native_replay recalibrates on the grown vocabulary; anchored_frozen calibrates once at the source vocabulary and its per-label scores do not change with growth. Stored scores are float16 logits clamped to [-30, 30].