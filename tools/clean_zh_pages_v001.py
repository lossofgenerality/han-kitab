#!/usr/bin/env python3
"""Clean the page images of 天方至聖實錄 (1924 printing, juan 1-10; NLC scan on Wikimedia Commons).
Pages are NOT altered in content: only (1) removal of isolated specks <= 6 px, (2) trimming to the printed
area with an even margin, (3) centring on one common page size. © Computational Classnotes · CC BY-NC-SA 4.0"""
import glob, numpy as np, json
from PIL import Image
from scipy import ndimage
fs = sorted(glob.glob('pages/p-*.png'))
boxes = []; arrs = []
for f in fs:
    a = np.array(Image.open(f).convert('L')) < 128          # True = ink
    lab, n = ndimage.label(a)
    sizes = ndimage.sum(a, lab, range(1, n + 1))
    small = np.isin(lab, np.where(sizes <= 6)[0] + 1)
    a = a & ~small
    # trim: ignore a thin border strip (scanner edge shadows)
    h, w = a.shape; m = 25
    inner = a[m:h - m, m:w - m]
    ys, xs = np.where(inner)
    if len(ys) < 50: box = None
    else:
        box = (xs.min() + m, ys.min() + m, xs.max() + m + 1, ys.max() + m + 1)
    boxes.append(box); arrs.append(a)
W = max(b[2] - b[0] for b in boxes if b) + 160
H = max(b[3] - b[1] for b in boxes if b) + 200
log = []
for i, (f, a, b) in enumerate(zip(fs, arrs, boxes), 1):
    canvas = Image.new('1', (W, H), 1)
    if b:
        crop = Image.fromarray((~a[b[1]:b[3], b[0]:b[2]]).astype(np.uint8) * 255).convert('1')
        canvas.paste(crop, ((W - crop.width) // 2, (H - crop.height) // 2))
    canvas.save(f'clean/page_{i:03d}.png', optimize=True)
    log.append({'page': i, 'src': f, 'box': [int(v) for v in b] if b else None})
json.dump({'W': int(W), 'H': int(H), 'pages': log}, open('clean_log_v001.json', 'w'), indent=0)
print(W, H)
