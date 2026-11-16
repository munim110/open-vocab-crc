#!/usr/bin/env bash
# COCO-Stuff val2017 (5,000 images + 171-class label maps) for src/exp_bank_select_coco.py, the bank-size choice made on
# the model's training domain, and LVIS v1 val (instance masks + the COCO-to-synset table) for the third benchmark
# (docs/COCO_LVIS_BENCHMARK.md), and the COCO instances val2017 boxes for the detection benchmark
# (docs/OVD_DETECTION_BENCHMARK.md). No login needed. Run from the repo root; ~2 GB. Re-runnable.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
EXT="$(dirname "$ROOT")/third_party_probe"
DATA="$ROOT/data/coco-stuff"
mkdir -p "$DATA/images" "$DATA/annotations"
if [ ! -d "$DATA/images/val2017" ]; then
  wget -q --show-progress -c -P "$DATA" http://images.cocodataset.org/zips/val2017.zip
  echo "4f7e2ccb2866ec5041993c9cf2a952bbed69647b115d0f74da7ce8f4bef82f05  $DATA/val2017.zip" | sha256sum -c -
  unzip -q "$DATA/val2017.zip" -d "$DATA/images" && rm "$DATA/val2017.zip"
fi
if [ ! -d "$DATA/annotations/val2017" ]; then
  wget -q --show-progress -c -P "$DATA" http://calvin.inf.ed.ac.uk/wp-content/uploads/data/cocostuffdataset/stuffthingmaps_trainval2017.zip
  unzip -q "$DATA/stuffthingmaps_trainval2017.zip" -d "$DATA/annotations" && rm "$DATA/stuffthingmaps_trainval2017.zip"
fi
# 171 training ids with 255 ignored: CAT-Seg's released preparation script, unchanged (writes train2017 and val2017)
if [ ! -d "$DATA/annotations_detectron2/val2017" ]; then
  DETECTRON2_DATASETS="$(dirname "$DATA")" python "$EXT/CAT-Seg/datasets/prepare_coco_stuff.py"
fi
# LVIS v1 val annotations and the LVIS authors' COCO-class synsets (src/coco_lvis_vocab.py, build_pixel_sample.py --dataset coco)
LVIS="$ROOT/data/lvis"; mkdir -p "$LVIS"
if [ ! -f "$LVIS/lvis_v1_val.json" ]; then
  wget -q --show-progress -c -P "$LVIS" https://dl.fbaipublicfiles.com/LVIS/lvis_v1_val.json.zip
  echo "5cae9a3c79aadb667550c2b5dcf7f4d86e059a41ec91ef690225b667e28e9ba5  $LVIS/lvis_v1_val.json.zip" | sha256sum -c -
  unzip -q "$LVIS/lvis_v1_val.json.zip" -d "$LVIS" && rm "$LVIS/lvis_v1_val.json.zip"
fi
if [ ! -f "$LVIS/coco_to_synset.json" ]; then
  wget -q -P "$LVIS" https://raw.githubusercontent.com/lvis-dataset/lvis-api/master/data/coco_to_synset.json
  echo "e6d4a9ae5c5af4f7ce1258f8a0d65b7409cab832955f1aaa8b21bf80b62f9b40  $LVIS/coco_to_synset.json" | sha256sum -c -
fi
# COCO instances val2017 (the 80-class boxes of the detection benchmark, src/ovd_vocab.py; docs/OVD_DETECTION_BENCHMARK.md)
INST="$ROOT/data/coco/annotations"; mkdir -p "$INST"
if [ ! -f "$INST/instances_val2017.json" ]; then
  wget -q --show-progress -c -P "$ROOT/data/coco" http://images.cocodataset.org/annotations/annotations_trainval2017.zip
  unzip -q -j "$ROOT/data/coco/annotations_trainval2017.zip" annotations/instances_val2017.json -d "$INST" && rm "$ROOT/data/coco/annotations_trainval2017.zip"
fi
echo "e8c7f7908f1d7278341fae127d0da654f102f11bd7b21d8aeefa635b8c810b6f  $INST/instances_val2017.json" | sha256sum -c -
echo "images: $(ls "$DATA/images/val2017" | wc -l)  labels: $(ls "$DATA/annotations_detectron2/val2017" | wc -l)"
