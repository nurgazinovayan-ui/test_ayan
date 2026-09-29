"""Stitch out/styles-clean/<style>/f0..f8.jpg into one captioned 3×3 storyboard per look: out/styles-clean/NN-<style>.jpg."""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

import styles_clean

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
W, H, HEAD = 640, 360, 70
for n, (name, (caption, _)) in enumerate(styles_clean.LOOKS.items(), 1):
    if len(sys.argv) > 1 and name not in sys.argv[1:]:
        continue
    d = os.path.join(HERE, 'out', 'styles-clean', name)
    im = Image.new('RGB', (W * 3, H * 3 + HEAD), '#111')
    for i in range(9):
        im.paste(Image.open(os.path.join(d, f'f{i}.jpg')).resize((W, H), Image.LANCZOS), ((i % 3) * W, HEAD + (i // 3) * H))
    ImageDraw.Draw(im).text((24, 18), f'{n:02d}  {caption}', fill='#fff', font=ImageFont.truetype(FONT, 30))
    im.save(os.path.join(HERE, 'out', 'styles-clean', f'{n:02d}-{name}.jpg'), quality=86)
    print(f'{n:02d}-{name}.jpg')
