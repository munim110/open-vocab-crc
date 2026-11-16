"""CLIPSeg as an existing trained independent-query baseline.

CLIPSeg scores one text query at a time, so its raw per-query logits are candidate-independent without any
change. Same 400 ADE development images, sampled pixels, natural prompts and image-level CRC as the headroom
probe. Released CIDAS/clipseg-rd64-refined weights at their native 352x352 input; nothing fitted.
"""
import argparse
import json
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
from transformers import CLIPSegForImageSegmentation, CLIPSegProcessor

from encode import ADE, sample_phi
from exp_fixed_source import digest
from exp_headroom_sets import ALPHAS, LOGIT_GRID
from exp_headroom_splits import DATASETS, curves
from exp_natural_ranks import true_ranks
from natural_vocab import load_manifest

OUT = Path('results/clipseg_baseline_ade')
NAME = 'CIDAS/clipseg-rd64-refined'
S, ADDITIONS = DATASETS['ade']['source'], DATASETS['ade']['additions']


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--device', default='cuda')
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    ids = json.loads(Path('results/headroom_probe_ade/protocol.json').read_text())['image_ids']
    if a.limit: ids = ids[:a.limit]
    names = [r['prompt'] for r in load_manifest()['rows']]
    processor = CLIPSegProcessor.from_pretrained(NAME)
    model = CLIPSegForImageSegmentation.from_pretrained(NAME).to(a.device).eval()
    tokens = processor.tokenizer(names, padding=True, return_tensors='pt').to(a.device)
    queries = model.get_conditional_embeddings(len(names), tokens['input_ids'], tokens['attention_mask'])                                  # [845,512], computed once
    meta = json.loads(Path('cache/sclip/meta.json').read_text())
    gt = np.load('cache/sclip/gt150.npy')
    grid = torch.from_numpy(LOGIT_GRID).to(a.device); widths = [S+x for x in ADDITIONS]
    loss, size, ranks, seconds = [], [], [], 0.
    confusion = np.zeros((S, S), np.int64)
    for k, index in enumerate(ids):
        info = meta['meta'][index]; H, W = info['H'], info['W']
        img = Image.open(Path(ADE)/'images/validation'/info['file']).convert('RGB')
        flat = np.random.default_rng(meta['pixseed']+index).choice(H*W, meta['npix'], replace=False)
        y, x = torch.from_numpy(flat//W).to(a.device), torch.from_numpy(flat % W).to(a.device)
        target = torch.from_numpy(gt[index].astype(np.int64)).to(a.device); valid = target < S
        pixels = processor.image_processor(img, return_tensors='pt')['pixel_values'].to(a.device)
        if a.device == 'cuda': torch.cuda.synchronize()
        t0 = time.perf_counter()
        hidden = model.clip.vision_model(pixel_values=pixels, output_hidden_states=True).hidden_states
        activations = [hidden[i+1] for i in model.extract_layers]
        out = []
        for i in range(0, len(names), 64):
            q = queries[i:i+64]
            maps = model.decoder([h.expand(len(q), -1, -1) for h in activations], q).logits          # [q,352,352]
            out.append(sample_phi(maps[None], y, x, H, W))
        if a.device == 'cuda': torch.cuda.synchronize()
        seconds += time.perf_counter()-t0
        logits = torch.cat(out, -1).double().clamp(-30, 30)
        l, s = curves(logits, target, grid, S, widths); loss.append(l); size.append(s.astype(np.float32))
        t = target.clamp(max=S-1)
        r0, r1 = true_ranks(logits[:, :S], t)[valid].double(), true_ranks(logits, t)[valid].double()
        ranks.append([r0.mean().item(), r1.mean().item(), (r0 == 1).double().mean().item(), (r1 <= 10).double().mean().item()])
        np.add.at(confusion, (gt[index][valid.cpu().numpy()].astype(int), logits[:, :S].argmax(-1)[valid].cpu().numpy()), 1)
        if k % 20 == 0:
            print(f'{k+1}/{len(ids)} source rank={ranks[-1][0]:.2f} +695 top10={ranks[-1][3]:.3f}', flush=True)
    if a.limit: return
    loss, size = np.stack(loss), np.stack(size)
    np.savez_compressed(OUT/'curves.npz', loss=loss, size=size, ranks=np.array(ranks))
    inter = np.diag(confusion); union = confusion.sum(0)+confusion.sum(1)-inter
    r = np.mean(ranks, 0)
    result = dict(model=NAME, images=len(ids), source_rank=r[0], expanded_rank=r[1], source_top1=r[2], expanded_top10=r[3],
                  sampled_pixel_miou=float(np.mean(inter[union > 0]/union[union > 0])), seconds_per_image=seconds/len(ids), sets={})
    n = len(ids); rng = np.random.default_rng(20261004); perms = [rng.permutation(n) for _ in range(200)]      # same splits as exp_anchor_bank.py
    lines = ['# CLIPSeg independent-query baseline', '', f'{n} ADE development images (the headroom-probe 400), {NAME}, raw per-query logits, threshold calibrated once at the {S} source labels by image-level CRC; mean over 200 random 200/200 splits.', '',
             f"Source rank {r[0]:.2f}; rank at +695 {r[1]:.2f}; source top-1 {100*r[2]:.2f}%; +695 top-10 {100*r[3]:.2f}%; sampled-pixel mIoU {100*result['sampled_pixel_miou']:.2f}; {result['seconds_per_image']:.2f} s/image for 845 queries.", '',
             '| alpha | Risk (%) | '+' | '.join(f'+{x}' for x in ADDITIONS)+' |', '|---:|---:|'+'---:|'*len(ADDITIONS)]
    for alpha in ALPHAS:
        rows = []
        for p in perms:
            cal, ev = p[:200], p[200:]
            g = np.flatnonzero((loss[cal].sum(0)+1)/(len(cal)+1) <= alpha)[-1]
            rows.append(np.concatenate([[loss[ev, g].mean()], size[:, :, g][ev].mean(0)]))
        m = np.mean(rows, 0); result['sets'][str(alpha)] = dict(risk=m[0], mean_size=m[1:].tolist())
        lines.append(f'| {alpha} | {100*m[0]:.2f} | '+' | '.join(f'{v:.2f}' for v in m[1:])+' |')
    lines += ['', 'Compare with results/anchor_bank_ade/REPORT.md (same images and split seed). CLIPSeg was trained on PhraseCut, not COCO-Stuff, at lower resolution; this is a baseline for the independent-query construction, not a matched-training comparison. Development data.']
    result['hashes'] = {p: digest(Path(p)) for p in ['src/exp_clipseg_baseline.py', 'meta/natural_vocab_v1.json']}
    (OUT/'results.json').write_text(json.dumps(result, indent=1))
    (OUT/'REPORT.md').write_text('\n'.join(lines))
    print('\n'.join(lines), flush=True)


if __name__ == '__main__':
    main()
