"""python3 story.py [nn …] → ../out/premium/NN-<name>.jpg: captioned 4×3 storyboard of each variant's SHOTS."""
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

import build

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'out', 'premium')
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
W, H, HEAD, COLS = 640, 360, 74, 4
LT = '-light' if '--light' in sys.argv else ''
for k in [int(a) for a in sys.argv[1:] if a != '--light'] or range(1, 11):
    m = build.load(k)
    html = os.path.join(HERE, f'p{k:02d}-{m.NAME}{LT}.html'); d = os.path.join(OUT, f'{k:02d}{LT}')
    subprocess.run(['node', os.path.join(HERE, 'story.js'), html, d, *map(str, m.SHOTS)], check=True, stderr=subprocess.DEVNULL)
    rows = (len(m.SHOTS) + COLS - 1) // COLS
    im = Image.new('RGB', (W * COLS, HEAD + H * rows), '#0d0d0f'); dr = ImageDraw.Draw(im); f = ImageFont.truetype(F, 30); fs = ImageFont.truetype(F, 17)
    for i, t in enumerate(m.SHOTS):
        x, y = (i % COLS) * W, HEAD + (i // COLS) * H
        im.paste(Image.open(os.path.join(d, f's{i}.jpg')).resize((W, H), Image.LANCZOS), (x, y))
        dr.rectangle((x + 8, y + 8, x + 70, y + 32), fill='#0d0d0f'); dr.text((x + 14, y + 10), f'{t:.1f}s', fill='#fff', font=fs)
    dr.text((24, 20), f'{k:02d}  {m.TITLE}  ·  {m.T:.0f} с', fill='#fff', font=f)
    im.save(os.path.join(OUT, f'{k:02d}-{m.NAME}{LT}.jpg'), quality=86)
    print(f'{k:02d}-{m.NAME}{LT}.jpg')
