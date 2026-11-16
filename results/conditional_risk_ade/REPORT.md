# Conditional risk under source-calibrated thresholds: vitb_coco171

2000 ADE validation images (0 without a source-labelled sampled pixel excluded), 150 source labels, 845 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration vitb_coco171. Development data; nothing is fitted; the confirmation reserve is untouched.
The CRC guarantee is on the marginal mean of the image loss (fraction of source-labelled sampled pixels whose label is missing from the set). Every stratum below is outside the guarantee for every arm; the table shows how the frozen thresholds behave inside them relative to recalibration. Per-class risk pools the evaluation pixels of the class; scene and label-count rows average the image loss over the evaluation images of the stratum; all numbers are means over splits (nan-skipped splits where the stratum is empty).

## alpha = 0.1

| Arm | Marginal risk (%) | Macro (class-mean) risk (%) | Worst class (%) | Classes > 2 alpha | Frequent third (%) | Medium third (%) | Rare third (%) | Worst scene (%) | Scenes > 2 alpha | Images > 25% lost (%) | Images > 50% lost (%) | 90th pct image loss (%) | 1-3 labels (%) | 4-6 labels (%) | 7-10 labels (%) | 11- labels (%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| native_source | 9.88 | 23.29 | 100.0 | 55.3 | 8.25 | 22.96 | 32.53 | 10.8 | 0 | 10.8 | 2.8 | 26.6 | 11.62 | 11.62 | 9.24 | 8.19 |
| native_frozen | 15.38 | 32.97 | 100.0 | 80.2 | 13.03 | 34.64 | 43.51 | 18.7 | 0 | 20.1 | 6.2 | 39.9 | 20.50 | 18.65 | 13.72 | 12.13 |
| native_replay | 9.90 | 23.30 | 100.0 | 54.3 | 8.12 | 23.71 | 32.24 | 11.1 | 0 | 11.7 | 3.4 | 28.0 | 14.06 | 12.59 | 8.66 | 7.09 |
| anchored_frozen | 9.88 | 17.20 | 99.9 | 38.5 | 8.81 | 17.61 | 22.64 | 20.7 | 1 | 12.1 | 3.0 | 28.0 | 11.93 | 11.52 | 9.15 | 8.29 |

Worst classes (pixel-pooled miss rate, %):

- native_source: base, pedestal, stand 100, hood, exhaust hood 100, buffet, counter, sideboard 99, case, display case, showcase, vitrine 97, ashcan, trash can, garbage can, wastebin, ash bin, ash-bin, ashbin, dustbin, trash barrel, trash bin 96, screen door, screen 91, screen, crt screen 90, canopy 88, earth, ground 86, blanket, cover 83
- native_frozen: case, display case, showcase, vitrine 100, base, pedestal, stand 100, ashcan, trash can, garbage can, wastebin, ash bin, ash-bin, ashbin, dustbin, trash barrel, trash bin 100, screen, crt screen 100, hood, exhaust hood 100, buffet, counter, sideboard 100, screen door, screen 99, earth, ground 98, blanket, cover 94, canopy 93
- native_replay: base, pedestal, stand 100, ashcan, trash can, garbage can, wastebin, ash bin, ash-bin, ashbin, dustbin, trash barrel, trash bin 100, hood, exhaust hood 100, buffet, counter, sideboard 99, screen, crt screen 98, case, display case, showcase, vitrine 95, canopy 91, screen door, screen 90, earth, ground 87, blanket, cover 85
- anchored_frozen: hood, exhaust hood 100, base, pedestal, stand 99, ashcan, trash can, garbage can, wastebin, ash bin, ash-bin, ashbin, dustbin, trash barrel, trash bin 98, buffet, counter, sideboard 97, earth, ground 83, canopy 77, case, display case, showcase, vitrine 73, screen door, screen 70, blanket, cover 67, blind, screen 63

Worst scenes (image-level risk, %):

- native_source: bathroom 11, misc 9, dining_room 9, living_room 8, bedroom 7
- native_frozen: bathroom 19, misc 15, dining_room 13, bedroom 11, living_room 11
- native_replay: bathroom 11, misc 10, dining_room 8, bedroom 6, living_room 6
- anchored_frozen: bathroom 21, dining_room 13, kitchen 12, living_room 10, misc 8

## alpha = 0.05

| Arm | Marginal risk (%) | Macro (class-mean) risk (%) | Worst class (%) | Classes > 2 alpha | Frequent third (%) | Medium third (%) | Rare third (%) | Worst scene (%) | Scenes > 2 alpha | Images > 25% lost (%) | Images > 50% lost (%) | 90th pct image loss (%) | 1-3 labels (%) | 4-6 labels (%) | 7-10 labels (%) | 11- labels (%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| native_source | 4.88 | 12.13 | 99.1 | 45.9 | 4.04 | 11.62 | 15.46 | 5.7 | 0 | 5.4 | 1.1 | 13.0 | 5.78 | 6.31 | 4.45 | 3.54 |
| native_frozen | 8.15 | 19.69 | 100.0 | 68.5 | 6.64 | 19.65 | 27.34 | 9.0 | 0 | 9.7 | 2.6 | 24.2 | 11.51 | 10.63 | 7.10 | 5.59 |
| native_replay | 4.90 | 12.28 | 99.8 | 45.5 | 4.01 | 11.47 | 16.28 | 5.3 | 0 | 5.9 | 1.2 | 13.8 | 6.71 | 6.92 | 4.12 | 3.04 |
| anchored_frozen | 4.89 | 9.42 | 95.4 | 34.2 | 4.33 | 9.04 | 10.92 | 8.3 | 0 | 5.5 | 1.0 | 14.7 | 6.17 | 6.31 | 4.47 | 3.41 |

Worst classes (pixel-pooled miss rate, %):

- native_source: base, pedestal, stand 99, buffet, counter, sideboard 96, hood, exhaust hood 91, ashcan, trash can, garbage can, wastebin, ash bin, ash-bin, ashbin, dustbin, trash barrel, trash bin 74, case, display case, showcase, vitrine 67, earth, ground 64, screen door, screen 62, canopy 61, pillow 54, bannister, banister, balustrade, balusters, handrail 43
- native_frozen: base, pedestal, stand 100, ashcan, trash can, garbage can, wastebin, ash bin, ash-bin, ashbin, dustbin, trash barrel, trash bin 100, hood, exhaust hood 100, buffet, counter, sideboard 99, canopy 90, case, display case, showcase, vitrine 89, screen, crt screen 88, screen door, screen 84, earth, ground 81, blanket, cover 75
- native_replay: ashcan, trash can, garbage can, wastebin, ash bin, ash-bin, ashbin, dustbin, trash barrel, trash bin 100, base, pedestal, stand 99, hood, exhaust hood 93, buffet, counter, sideboard 89, canopy 80, earth, ground 67, case, display case, showcase, vitrine 67, screen door, screen 60, box 52, pillow 44
- anchored_frozen: base, pedestal, stand 94, hood, exhaust hood 87, buffet, counter, sideboard 85, ashcan, trash can, garbage can, wastebin, ash bin, ash-bin, ashbin, dustbin, trash barrel, trash bin 71, earth, ground 67, canopy 50, case, display case, showcase, vitrine 49, screen door, screen 47, box 39, pillow 35

Worst scenes (image-level risk, %):

- native_source: bathroom 6, dining_room 5, misc 5, kitchen 4, living_room 3
- native_frozen: bathroom 9, misc 8, dining_room 7, bedroom 5, kitchen 5
- native_replay: bathroom 5, dining_room 4, misc 4, kitchen 3, bedroom 2
- anchored_frozen: bathroom 8, dining_room 6, misc 4, living_room 4, kitchen 4

Classes are split into thirds by total sampled-pixel count (frequent third: wall, building, edifice, sky, floor, flooring, tree, ...; rare third: bicycle, bike, wheel, cycle, clock, pier, wharf, wharfage, dock, shower, barrel, cask, ...). Scenes with at least 20 kept images: 10. native_source is the native model before growth (threshold and evaluation at the source vocabulary); native_frozen reuses that threshold after growth; native_replay recalibrates on the grown vocabulary; anchored_frozen calibrates once at the source vocabulary and its per-label scores do not change with growth. Stored scores are float16 logits clamped to [-30, 30].