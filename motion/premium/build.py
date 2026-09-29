"""python3 build.py [nn …] → pNN-<name>.html for the premium variants (all by default)."""
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
VARIANTS = ['v01_keynote', 'v02_canvas', 'v03_bento', 'v04_exploded', 'v05_scroll', 'v06_masks', 'v07_orbit', 'v08_pipeline', 'v09_deck', 'v10_palette']


def load(k):
    return importlib.import_module(VARIANTS[k - 1])


if __name__ == '__main__':
    pick = [int(a) for a in sys.argv[1:]] or range(1, 11)
    for k in pick:
        if not os.path.exists(os.path.join(HERE, VARIANTS[k - 1] + '.py')):
            continue
        m = load(k)
        fn = f'p{k:02d}-{m.NAME}.html'
        open(os.path.join(HERE, fn), 'w', encoding='utf-8').write(m.build())
        print(fn, f'{m.T:.1f}s')
