"""Fine-tune released CAT-Seg so that reference-anchored class aggregation is what it was trained for.

Standalone PyTorch (no detectron2). Starts from the released checkpoint. Each step samples a reference bank R
from the training vocabulary, runs R natively to record its class-attention context, and scores every training
label against that context plus itself, exactly as src/catseg_probe_model.py does at deployment. The loss is the
released one (per-label BCE, ignored pixels as all-negative) on the anchored logits, plus the same loss on the
bank's own logits so the context stays a good segmenter. Only the cost aggregator is trained in this version;
CLIP and the guidance upsamplers stay frozen, so text embeddings are fixed and image features need no gradient.

Labels: PNGs of training ids 0..K-1 with 255 ignored (CAT-Seg's datasets/prepare_coco_stuff.py output).
"""
import argparse
import json
import random
import time
from pathlib import Path, PureWindowsPath

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image

from catseg_probe_model import CATSegProbe, CATSEG, bank_context

CROP = 384


class Crops(torch.utils.data.Dataset):
    """Released recipe without colour jitter: short side 384, random 384 crop, horizontal flip."""

    def __init__(self, images, labels, skip=()):
        labels = {p.stem: p for p in Path(labels).glob('*.png')}
        self.items = [(p, labels[p.stem]) for p in sorted(Path(images).glob('*.jpg')) if p.stem in labels and p.name not in set(skip)]
        assert self.items, 'no image/label pairs found'

    def __len__(self):
        return len(self.items)

    def __getitem__(self, i):
        img, lab = Image.open(self.items[i][0]).convert('RGB'), Image.open(self.items[i][1])
        w, h = img.size; s = CROP/min(w, h)
        size = (max(CROP, int(w*s+.5)), max(CROP, int(h*s+.5)))
        img, lab = np.array(img.resize(size, Image.BILINEAR)), np.array(lab.resize(size, Image.NEAREST))
        y, x = random.randint(0, size[1]-CROP), random.randint(0, size[0]-CROP)
        img, lab = img[y:y+CROP, x:x+CROP], lab[y:y+CROP, x:x+CROP]
        if random.random() < .5: img, lab = img[:, ::-1], lab[:, ::-1]
        return torch.from_numpy(img.copy()).permute(2, 0, 1).float(), torch.from_numpy(lab.copy()).long()


def released_loss(logits, target, labels):
    """cat_seg_model.py training loss for the label subset `labels` (tensor of training ids, in logit order)."""
    logits = F.interpolate(logits, size=target.shape[-2:], mode='bilinear', align_corners=False)
    onehot = (target[:, None] == labels[None, :, None, None]).float()              # ignored pixels are all-negative, as released
    return F.binary_cross_entropy_with_logits(logits, onehot)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--images', required=True); ap.add_argument('--labels', required=True)
    ap.add_argument('--classes', default=str(CATSEG/'datasets/coco.json'))
    ap.add_argument('--skip', default='', help='JSON manifest with a "files" list of images that must not be read')
    ap.add_argument('--out', default='runs/anchored_vitb')
    ap.add_argument('--iters', type=int, default=10000); ap.add_argument('--batch', type=int, default=4)
    ap.add_argument('--lr', type=float, default=1e-4); ap.add_argument('--weight-decay', type=float, default=1e-4)
    ap.add_argument('--bank-min', type=int, default=32); ap.add_argument('--bank-max', type=int, default=0, help='0 = all training labels')
    ap.add_argument('--bank-weight', type=float, default=.5)
    ap.add_argument('--bank-pool', default='', help='JSON with a "names" list the per-step bank is drawn from instead of the training labels (names outside the training labels are all-negative)')
    ap.add_argument('--size', default='base', choices=['base', 'large'])
    ap.add_argument('--distractors', default='', help='JSON with a "names" list (src/build_distractors.py): labels scored as all-negative candidates')
    ap.add_argument('--distractor-count', type=int, default=64, help='distractors per step; as many COCO negatives are dropped, so memory is unchanged')
    ap.add_argument('--distractor-max-sim', type=float, default=.8, help='drop distractors whose text is this close to any training label (likely present under another name)')
    ap.add_argument('--distractor-near', type=float, default=.5, help='share of distractors drawn from those closest in text to the labels in the batch')
    ap.add_argument('--workers', type=int, default=8); ap.add_argument('--save-every', type=int, default=1000)
    ap.add_argument('--seed', type=int, default=0); ap.add_argument('--device', default='cuda'); ap.add_argument('--tf32', action='store_true')
    ap.add_argument('--resume', default='')
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    random.seed(a.seed); np.random.seed(a.seed); torch.manual_seed(a.seed)
    torch.backends.cuda.matmul.allow_tf32 = torch.backends.cudnn.allow_tf32 = a.tf32
    names = json.loads(Path(a.classes).read_text()); K = len(names); bank_max = a.bank_max or K
    skip = [PureWindowsPath(f).name for f in json.loads(Path(a.skip).read_text())['files']] if a.skip else []
    data = Crops(a.images, a.labels, skip)
    loader = torch.utils.data.DataLoader(data, batch_size=a.batch, shuffle=True, num_workers=a.workers, drop_last=True, persistent_workers=a.workers > 0)
    (out/'config.json').write_text(json.dumps(dict(vars(a), pairs=len(data), labels=K), indent=1))

    model = CATSegProbe(size=a.size).to(a.device)
    text = model.encode_text(names)
    pool_text, pool_ids = text, torch.arange(K, device=a.device)
    if a.bank_pool:   # bank names that are training labels keep their id; the others get -1 (never a target)
        pool = json.loads(Path(a.bank_pool).read_text())['names']; lookup = {n: i for i, n in enumerate(names)}
        pool_text, pool_ids = model.encode_text(pool), torch.tensor([lookup.get(n, -1) for n in pool], device=a.device)
        bank_max = a.bank_max or len(pool)
    extra = None
    if a.distractors:
        extra = model.encode_text(json.loads(Path(a.distractors).read_text())['names'])
        sim = extra@text.T
        extra, sim = extra[sim.max(1).values < a.distractor_max_sim], sim[sim.max(1).values < a.distractor_max_sim]
        print(len(extra), 'distractors kept', flush=True)
    for p in model.parameters(): p.requires_grad_(False)
    params = list(model.transformer.parameters())
    for p in params: p.requires_grad_(True)
    opt = torch.optim.AdamW(params, lr=a.lr, weight_decay=a.weight_decay)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, a.iters)
    step = 0
    if a.resume:
        state = torch.load(a.resume, map_location=a.device)
        model.transformer.load_state_dict(state['aggregator']); opt.load_state_dict(state['optimizer']); sched.load_state_dict(state['scheduler']); step = state['step']
    context, anchored = CATSegProbe.context.__wrapped__, CATSegProbe.anchored.__wrapped__      # the deployment code paths, with gradients
    model.eval()                                                  # no dropout or batch norm in the aggregator; keeps CLIP deterministic
    log = (out/'log.jsonl').open('a'); t0 = time.perf_counter()
    while step < a.iters:
        for image, target in loader:
            image, target = image.to(a.device), target.to(a.device)
            feats = model.image_features(image)
            bank = torch.randperm(len(pool_ids), device=a.device)[:random.randint(a.bank_min, bank_max)]
            ctx = context(model, feats, pool_text[bank]) if len(bank) < model.transformer.layers[0].attention.pad_len else bank_context.__wrapped__(model, feats, pool_text[bank])
            every, cand_text = torch.arange(K, device=a.device), text
            if extra is not None:   # keep the labels in the batch, drop random absent ones, add distractors (target: absent everywhere)
                D = a.distractor_count; present = torch.unique(target[target < K])
                absent = every[~torch.isin(every, present)]
                every = torch.cat([present, absent[torch.randperm(len(absent), device=a.device)[:max(K-D-len(present), 0)]]])
                n_near = int(D*a.distractor_near)
                near = sim[:, present].max(1).values.topk(4*n_near).indices[torch.randperm(4*n_near, device=a.device)[:n_near]] if n_near and len(present) else every[:0]
                pick = torch.cat([near, torch.randint(len(extra), (D-len(near),), device=a.device)])
                cand_text = torch.cat([text[every], extra[pick]])
                every = torch.cat([every, torch.full((D,), -1, device=a.device)])      # -1 never equals a target id
            loss_anchor = released_loss(anchored(model, feats, ctx, cand_text, chunk=len(cand_text)), target, every)
            loss_bank = released_loss(ctx['ref_logits'], target, pool_ids[bank])
            loss = loss_anchor+a.bank_weight*loss_bank
            opt.zero_grad(set_to_none=True); loss.backward()
            torch.nn.utils.clip_grad_norm_(params, .01)             # released CLIP_GRADIENTS: full-model norm 0.01
            opt.step(); sched.step(); step += 1
            if step % 20 == 0 or step == 1:
                row = dict(step=step, loss=loss.item(), anchored=loss_anchor.item(), bank=loss_bank.item(), bank_size=len(bank), lr=sched.get_last_lr()[0],
                           seconds_per_step=(time.perf_counter()-t0)/step, peak_gb=torch.cuda.max_memory_allocated()/2**30 if a.device == 'cuda' else 0)
                log.write(json.dumps(row)+'\n'); log.flush(); print(row, flush=True)
            if step % a.save_every == 0 or step == a.iters:
                torch.save(dict(aggregator=model.transformer.state_dict(), optimizer=opt.state_dict(), scheduler=sched.state_dict(), step=step), out/f'step{step}.pt')
            if step >= a.iters: break


if __name__ == '__main__':
    main()
