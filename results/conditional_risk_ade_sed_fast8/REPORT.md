# Conditional risk under source-calibrated thresholds: sed_fast8

2000 ADE validation images (0 without a source-labelled sampled pixel excluded), 150 source labels, 845 after growth, 500 random 1000/1000 calibration/evaluation splits; configuration sed_fast8. Development data; nothing is fitted; the confirmation reserve is untouched.
The CRC guarantee is on the marginal mean of the image loss (fraction of source-labelled sampled pixels whose label is missing from the set). Every stratum below is outside the guarantee for every arm; the table shows how the frozen thresholds behave inside them relative to recalibration. Per-class risk pools the evaluation pixels of the class; scene and label-count rows average the image loss over the evaluation images of the stratum; all numbers are means over splits (nan-skipped splits where the stratum is empty).

## alpha = 0.1

| Arm | Marginal risk (%) | Macro (class-mean) risk (%) | Worst class (%) | Classes > 2 alpha | Frequent third (%) | Medium third (%) | Rare third (%) | Worst scene (%) | Scenes > 2 alpha | Images > 25% lost (%) | Images > 50% lost (%) | 90th pct image loss (%) | 1-3 labels (%) | 4-6 labels (%) | 7-10 labels (%) | 11- labels (%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| native_source | 9.90 | 19.77 | 100.0 | 41.7 | 8.71 | 18.82 | 25.31 | 11.0 | 0 | 11.2 | 3.1 | 27.4 | 14.70 | 13.18 | 8.53 | 6.38 |
| native_frozen | 12.84 | 25.82 | 100.0 | 58.8 | 11.05 | 26.20 | 32.74 | 13.0 | 0 | 16.2 | 5.8 | 36.8 | 21.86 | 17.34 | 10.68 | 7.57 |
| native_replay | 9.91 | 20.70 | 100.0 | 46.0 | 8.45 | 20.26 | 27.13 | 9.9 | 0 | 12.5 | 4.3 | 29.9 | 17.41 | 13.90 | 8.00 | 5.43 |
| anchored_frozen | 9.90 | 14.86 | 100.0 | 31.8 | 9.16 | 13.79 | 18.79 | 16.9 | 0 | 12.2 | 3.4 | 28.4 | 13.43 | 11.98 | 8.84 | 7.74 |

Worst classes (pixel-pooled miss rate, %):

- native_source: case, display case, showcase, vitrine 100, earth, ground 100, base, pedestal, stand 100, buffet, counter, sideboard 99, ashcan, trash can, garbage can, wastebin, ash bin, ash-bin, ashbin, dustbin, trash barrel, trash bin 98, pillow 94, screen door, screen 91, step, stair 82, land, ground, soil 78, bannister, banister, balustrade, balusters, handrail 77
- native_frozen: base, pedestal, stand 100, ashcan, trash can, garbage can, wastebin, ash bin, ash-bin, ashbin, dustbin, trash barrel, trash bin 100, case, display case, showcase, vitrine 100, earth, ground 100, booth, cubicle, stall, kiosk 99, buffet, counter, sideboard 98, pillow 96, screen door, screen 95, tank, storage tank 92, step, stair 89
- native_replay: ashcan, trash can, garbage can, wastebin, ash bin, ash-bin, ashbin, dustbin, trash barrel, trash bin 100, earth, ground 100, case, display case, showcase, vitrine 100, base, pedestal, stand 100, screen door, screen 92, tank, storage tank 88, pillow 86, buffet, counter, sideboard 85, booth, cubicle, stall, kiosk 75, tray 74
- anchored_frozen: earth, ground 100, case, display case, showcase, vitrine 100, base, pedestal, stand 99, ashcan, trash can, garbage can, wastebin, ash bin, ash-bin, ashbin, dustbin, trash barrel, trash bin 94, buffet, counter, sideboard 82, screen, crt screen 73, pillow 73, tray 61, bannister, banister, balustrade, balusters, handrail 60, blind, screen 60

Worst scenes (image-level risk, %):

- native_source: misc 11, bathroom 10, dining_room 9, bedroom 6, living_room 5
- native_frozen: misc 13, bathroom 12, dining_room 10, bedroom 8, living_room 6
- native_replay: misc 10, bathroom 9, dining_room 7, bedroom 6, building_facade 5
- anchored_frozen: bathroom 17, dining_room 15, kitchen 10, living_room 9, bedroom 9

## alpha = 0.05

| Arm | Marginal risk (%) | Macro (class-mean) risk (%) | Worst class (%) | Classes > 2 alpha | Frequent third (%) | Medium third (%) | Rare third (%) | Worst scene (%) | Scenes > 2 alpha | Images > 25% lost (%) | Images > 50% lost (%) | 90th pct image loss (%) | 1-3 labels (%) | 4-6 labels (%) | 7-10 labels (%) | 11- labels (%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| native_source | 4.90 | 9.69 | 99.3 | 33.7 | 4.38 | 7.65 | 12.19 | 5.3 | 0 | 6.3 | 1.6 | 13.8 | 8.41 | 7.30 | 3.84 | 2.43 |
| native_frozen | 6.98 | 14.60 | 100.0 | 52.4 | 6.00 | 13.22 | 18.87 | 6.6 | 0 | 8.8 | 2.9 | 21.2 | 13.30 | 10.36 | 5.15 | 3.44 |
| native_replay | 4.91 | 10.50 | 100.0 | 37.4 | 4.26 | 8.30 | 13.59 | 5.2 | 0 | 6.6 | 2.0 | 13.8 | 9.58 | 7.82 | 3.22 | 2.26 |
| anchored_frozen | 4.89 | 7.76 | 98.6 | 29.1 | 4.55 | 6.02 | 8.78 | 4.9 | 0 | 6.2 | 1.5 | 14.0 | 8.53 | 7.20 | 3.76 | 2.55 |

Worst classes (pixel-pooled miss rate, %):

- native_source: earth, ground 99, case, display case, showcase, vitrine 97, base, pedestal, stand 95, buffet, counter, sideboard 58, ashcan, trash can, garbage can, wastebin, ash bin, ash-bin, ashbin, dustbin, trash barrel, trash bin 56, bannister, banister, balustrade, balusters, handrail 53, screen door, screen 50, box 49, tank, storage tank 47, ship 42
- native_frozen: earth, ground 100, base, pedestal, stand 99, case, display case, showcase, vitrine 99, ashcan, trash can, garbage can, wastebin, ash bin, ash-bin, ashbin, dustbin, trash barrel, trash bin 98, tank, storage tank 81, screen door, screen 75, bannister, banister, balustrade, balusters, handrail 67, box 63, tray 62, screen, crt screen 59
- native_replay: earth, ground 100, base, pedestal, stand 92, case, display case, showcase, vitrine 92, ashcan, trash can, garbage can, wastebin, ash bin, ash-bin, ashbin, dustbin, trash barrel, trash bin 91, tank, storage tank 73, bannister, banister, balustrade, balusters, handrail 65, screen door, screen 58, box 56, screen, crt screen 52, glass, drinking glass 46
- anchored_frozen: earth, ground 98, case, display case, showcase, vitrine 96, base, pedestal, stand 88, ashcan, trash can, garbage can, wastebin, ash bin, ash-bin, ashbin, dustbin, trash barrel, trash bin 49, buffet, counter, sideboard 48, tank, storage tank 45, ship 40, box 40, bannister, banister, balustrade, balusters, handrail 38, tray 33

Worst scenes (image-level risk, %):

- native_source: misc 5, dining_room 3, bathroom 3, bedroom 2, building_facade 2
- native_frozen: misc 7, bathroom 5, dining_room 4, bedroom 3, building_facade 3
- native_replay: misc 5, bathroom 3, building_facade 2, highway 2, dining_room 2
- anchored_frozen: misc 5, bathroom 5, dining_room 4, kitchen 3, bedroom 2

Classes are split into thirds by total sampled-pixel count (frequent third: wall, building, edifice, sky, floor, flooring, tree, ...; rare third: bicycle, bike, wheel, cycle, clock, pier, wharf, wharfage, dock, shower, barrel, cask, ...). Scenes with at least 20 kept images: 10. native_source is the native model before growth (threshold and evaluation at the source vocabulary); native_frozen reuses that threshold after growth; native_replay recalibrates on the grown vocabulary; anchored_frozen calibrates once at the source vocabulary and its per-label scores do not change with growth. Stored scores are float16 logits clamped to [-30, 30].