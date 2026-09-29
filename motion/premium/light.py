"""Light look for the premium variants — the palette of the landing promo (oneflow-clean): #f6f6fa with a soft blue glow,
ink #0f1222, blue gradient accent, white panels, Inter, the default wireframes. Each variant keeps its own direction;
only colours are overridden (plus the few variant-specific dark pieces).

apply(html, module_name) → html with the light overrides appended to the page's <style>.
"""
import re

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import wire  # noqa: E402

BASE = """
:root { --bg: radial-gradient(ellipse 70% 60% at 50% 110%, #e9edff, transparent 70%), #f6f6fa !important; --ink: #0f1222 !important; --mut: #8a8fa8 !important;
  --panel: #fff !important; --panel2: #f3f4f9 !important; --line: #e3e7f5 !important; --dot: #dfe3f1 !important; --acc: #3b5cff !important; --on-acc: #fff !important;
  --on-ink: #fff !important; --grad: linear-gradient(90deg, #3b5cff, #6fb6ff) !important; --sh: 0 50px 100px -50px rgba(59,92,255,.32) !important;
  --f-disp: 'Inter' !important; --f-body: 'Inter' !important; --f-mono: 'JetBrains Mono' !important; --w-disp: 500 !important; --ls-disp: -.04em !important; --grain: .018 !important; }
.ub { background: var(--ink) !important; color: #fff !important; } .btn.acc, .pill.acc { background: var(--grad) !important; color: #fff !important; }
"""
SOFT = ['#eef1ff', '#e6f3ff', '#efeaff', '#e8f7f3', '#fff1ea', '#eaf0ff']
EXTRA = {
    'v03_bento': """
.beam { background: radial-gradient(ellipse at center, rgba(59,92,255,.16), rgba(59,92,255,.04) 45%, transparent 70%) !important; }
.lg2 { background: linear-gradient(180deg, #0f1222 35%, #5a6180) !important; -webkit-background-clip: text !important; background-clip: text !important; }
.cell { box-shadow: inset 0 0 0 1px var(--line), 0 30px 60px -40px rgba(59,92,255,.35) !important; } .cell::before { background: radial-gradient(ellipse 60% 70% at 0% 0%, rgba(59,92,255,.07), transparent 70%) !important; }
""",
    'v04_exploded': """
.glow { background: radial-gradient(ellipse at center, rgba(59,92,255,.16), rgba(59,92,255,.04) 45%, transparent 70%) !important; }
.lay { box-shadow: 0 0 0 1px var(--line), 0 60px 120px -50px rgba(59,92,255,.4) !important; }
""",
    'v05_scroll': """
.band { background: radial-gradient(40% 60% at 20% 30%, #c3d0ff, transparent 70%), radial-gradient(35% 55% at 55% 20%, #e2d9ff, transparent 70%),
  radial-gradient(40% 60% at 85% 40%, #cfe8ff, transparent 70%), radial-gradient(45% 70% at 60% 80%, #bfe0ff, transparent 70%), #dde5ff !important; background-size: 160% 160% !important; }
.sec .logo, .sec .ctr { color: var(--ink) !important; } .sec .logo .mk path { fill: url(#mg); } .fnote { color: var(--mut) !important; }
""",
    'v06_masks': """
.g { color: var(--acc) !important; -webkit-text-fill-color: var(--acc) !important; }
.win, .mo, .pc, .adc, .tl { background: rgba(255,255,255,.86) !important; } .fc .im { box-shadow: 0 0 0 1px var(--line) !important; }
""" + ''.join(f'.shot:nth-of-type({len(SOFT)}n+{k + 1}) {{ background: radial-gradient(55% 75% at 18% 22%, {c}, transparent 70%), radial-gradient(50% 70% at 82% 28%, {SOFT[(k + 2) % len(SOFT)]}, transparent 70%), '
                  f'radial-gradient(70% 80% at 55% 105%, {SOFT[(k + 4) % len(SOFT)]}, transparent 70%), #f6f6fa !important; background-size: 140% 140% !important; }}\n' for k, c in enumerate(SOFT)),
    'v07_orbit': """
.rings ellipse { stroke: rgba(15,18,34,.12) !important; } .rings .d { stroke: rgba(59,92,255,.4) !important; }
.core { background: radial-gradient(circle at 35% 30%, #fff, #e6ecff 72%) !important; box-shadow: 0 0 0 1px #d6ddff, 0 0 120px rgba(59,92,255,.3), inset 0 0 30px rgba(111,182,255,.25) !important; }
.chip2 { background: #fff !important; color: var(--ink) !important; box-shadow: 0 0 0 1px var(--line), 0 12px 30px -16px rgba(59,92,255,.4) !important; } .chip2 i.ic { color: #fff !important; }
.chip2.hi { box-shadow: 0 0 0 1.5px #3b5cff, 0 0 40px rgba(59,92,255,.4) !important; } .dt { background: #3b5cff !important; box-shadow: 0 0 10px rgba(59,92,255,.5) !important; }
""",
    'v08_pipeline': ".node { box-shadow: 0 0 0 2px var(--acc), 0 10px 30px -10px rgba(59,92,255,.45) !important; }\n",
    'v09_deck': """
.card, .card.dark { --bg: #fff !important; --ink: #0f1222 !important; --mut: #8a8fa8 !important; --panel: #fff !important; --panel2: #f3f4f9 !important; --line: #e3e7f5 !important;
  --dot: #dfe3f1 !important; --acc: #3b5cff !important; --grad: linear-gradient(90deg, #3b5cff, #6fb6ff) !important; --on-ink: #fff !important; }
.card:nth-child(3n+1) { --bg: #f5f7ff !important; } .card:nth-child(3n+2) { --bg: #ffffff !important; } .card:nth-child(3n) { --bg: #f7f5ff !important; }
.card { box-shadow: 0 0 0 1px #e3e7f5, 0 50px 100px -50px rgba(59,92,255,.35) !important; }
.card .win { --panel: #fff !important; --panel2: #f3f4f9 !important; --ink: #0f1222 !important; --mut: #8a8fa8 !important; --line: #e3e7f5 !important; --acc: #3b5cff !important;
  --grad: linear-gradient(90deg, #3b5cff, #6fb6ff) !important; }
""",
    'v10_palette': """
.pal, .plist { background: rgba(255,255,255,.94) !important; box-shadow: 0 0 0 1px var(--line), 0 60px 120px -40px rgba(59,92,255,.35) !important; }
.pin .k { color: #fff !important; } .sel { background: rgba(59,92,255,.07) !important; box-shadow: inset 0 0 0 1px rgba(59,92,255,.35) !important; }
.kc span { background: #fff !important; color: var(--ink) !important; box-shadow: inset 0 -3px 0 #d6ddff, 0 0 0 1px var(--line), 0 16px 30px -18px rgba(59,92,255,.4) !important; }
""",
}


def apply(html, module):
    css = BASE + EXTRA.get(module, '') + wire.css_vars(':root', None)
    html = html.replace('</style>\n</head>', css + '\n</style>\n</head>', 1)
    stops = iter(('#8fc6ff', '#4d7cff', '#3b5cff'))
    return re.sub(r'(<linearGradient id="mg"[^>]*>)(.*?)(</linearGradient>)',
                  lambda m: m.group(1) + re.sub(r'stop-color="[^"]+"', lambda _: f'stop-color="{next(stops)}"', m.group(2)) + m.group(3), html, count=1)
