# Third-party code and data

The MIT licence in `LICENSE` covers the code written for this paper. It does not
cover the vendored components below, which keep their own terms.

## Vendored source

| Path | Origin | Licence |
|---|---|---|
| `src/sclip_clip/` | OpenAI CLIP, as modified by [SCLIP](https://github.com/wangf3014/SCLIP) (correlative self-attention) | MIT |
| `src/naclip_clip/` | OpenAI CLIP, as modified by [NACLIP](https://github.com/sinahmr/NACLIP) (neighbourhood attention) | MIT |
| `src/imagenet_template.py` | The 80 ImageNet prompt templates from OpenAI CLIP | MIT |
| `meta/register_ade20k_full.py` | Detectron2 / Mask2Former, the ADE20K-847 category register | Apache-2.0 |

`meta/pascal_59_labels.txt` is committed for the same reason the register is:
Stanford publishes the 459- and 33-class lists but not the 59, so there is no URL
to fetch it from.

`meta/register_ade20k_full.py` is never imported. `src/labels.py` reads it as
text and parses out the `ADE20K_SEM_SEG_FULL_CATEGORIES` literal, so detectron2
is not a dependency.

Both vendored CLIP copies are byte-identical to upstream except for the
attention modification each paper describes. They are included rather than
pip-installed because the modification is the object of study: the cached
factorisation in `src/encode.py` depends on exactly where the attention change
sits relative to the text projection.

## Datasets

None are redistributed here. `scripts/fetch_*.sh` downloads them from source and
checksum-verifies each one; `make check-data` reports what is present.

The ADE20K full release is distributed by MIT behind a registration wall. We
fetch it from `1aurent/ADE20K`, a public BSD-licensed parquet mirror on the
Hugging Face Hub. That is a convenience, not a relicensing: the underlying MIT
CSAIL terms still apply, and the source images remain non-commercial.

| Dataset | Source | Terms |
|---|---|---|
| ADE20K SceneParse150 | MIT CSAIL, `scripts/fetch_ade.sh` | BSD-3-Clause, research use |
| ADE20K full (`ADE20K_2021_17_01`) | MIT CSAIL; fetched from the public HF mirror [`1aurent/ADE20K`](https://huggingface.co/datasets/1aurent/ADE20K) by `scripts/fetch_ade.sh` | research use; images non-commercial |
| Pascal Context 59 / 459 | Oxford VGG + Stanford, `scripts/fetch_pascal.sh` | Pascal VOC terms; annotations CC-BY |
| COCO val2017 images, COCO instances val2017 | cocodataset.org, `scripts/fetch_coco_val.sh` | CC-BY 4.0 annotations; Flickr image terms |
| COCO-Stuff val2017 | Caesar et al., `scripts/fetch_coco_val.sh` | CC-BY 4.0 annotations |
| LVIS v1 val | lvisdataset.org, `scripts/fetch_coco_val.sh` | CC-BY 4.0 annotations |
