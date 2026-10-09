"""«made in ONEFLOW» — a section under the hero: the logo from madein.zip and a curved row of ads made in ONEFLOW.

The row is the TiltedGridHero component (a React + Tailwind + shadcn snippet) ported to plain JS/CSS, since the
landing is a static page with no React: the same cylinder math (`arc`, `measure`), the same SLICES vertical strips
per tile, each turned round the cylinder's axis, one rotateY animation per tile, a static fade mask at both ends,
and a tile taking its next image each time it wraps out of sight. The only JS is a ResizeObserver that sizes the
loop and that wrap handler; motion is CSS transforms on the compositor, paused for prefers-reduced-motion.

Images are referenced once each as CSS custom properties (--mi0…), which build_vercel turns into data URIs, so a
strip only names a variable instead of repeating an image.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# the user's ads, in the order they play
MADE_IMAGES = ['hot-vision', 'pop-off', 'feel-the-sound', 'make-a-scene', 'pendant']


def logo_svg():
    svg = open(os.path.join(HERE, 'assets', 'made', 'made-in-oneflow.svg'), encoding='utf-8').read().strip()
    return svg.replace('<svg ', '<svg class="mb-logo" role="img" aria-label="made in ONEFLOW" focusable="false" ', 1)


def made_html():
    return ('<section class="made" id="made" aria-labelledby="made-h">'
            f'<div class="mb-band" id="madeBand" aria-hidden="true" data-count="{len(MADE_IMAGES)}"></div>'
            f'<div class="mb-head"><h2 id="made-h">{logo_svg()}</h2></div>'
            '</section>')


MADE_CSS = """
/* made in ONEFLOW: a curved row of ads (TiltedGridHero, ported) */
:root { """ + ' '.join(f'--mi{i}: url(assets/made/{n}.webp);' for i, n in enumerate(MADE_IMAGES)) + """ }
.made { position: relative; height: clamp(580px, 50vw, 720px); margin-top: 56px; overflow: hidden; container-type: size; }
.made .mb-head { position: relative; z-index: 2; display: grid; justify-items: center; padding: 128px 24px 0; text-align: center; }
.made .mb-head h2 { margin: 0; }
.made .mb-logo { display: block; width: min(220px, 50vw); height: auto; color: var(--ink); }
.mb-band { position: absolute; inset: 0; pointer-events: none; opacity: 0; transition: opacity .5s; }
.mb-band.on { opacity: 1; }
.mb-tile { position: absolute; transform-style: preserve-3d; }
.mb-strip { position: absolute; top: 0; overflow: hidden; background-color: #d6d6d6; background-repeat: no-repeat; }
.mb-strip.l { border-radius: 14px 0 0 14px; } .mb-strip.r { border-radius: 0 14px 14px 0; }
@media (max-width: 760px) { .made { height: 500px; margin-top: 40px; } .made .mb-head { padding-top: 92px; } }
"""

JS_MADE = """<script>
// made in ONEFLOW: the curved row (TiltedGridHero ported to plain JS — see made.py)
(() => {
  const root = document.getElementById('madeBand'); if (!root) return;
  const host = root.parentElement, N = +root.dataset.count || 1;
  const SLICES = 16, CAMERA = 1.6, MAX_WIDTH = 55;
  const speed = 4, aspect = 1, gap = 6, axis = 63, curve = 80, fade = 12;
  let tileHeight = 38;  // % of the section height; smaller on phones (set per resize)
  const bend = (Math.min(85, Math.max(5, curve)) * Math.PI) / 180;
  const arc = (b) => (CAMERA - 1 + Math.cos(b)) / (2 * CAMERA * Math.sin(b));
  const deg = (rad) => (rad * 180) / Math.PI, round = (n) => +n.toFixed(4);
  const measure = (width, height) => {
    const h = Math.min((tileHeight / 100) * height, ((MAX_WIDTH / 100) * width) / aspect);
    const radius = width * arc(bend);
    if (!(h > 0) || !(radius > 0)) return null;
    const unit = deg(h / radius), pitch = (aspect + gap / 100) * unit, limit = deg(bend) + (aspect * unit) / 2;
    const columns = Math.min(60, Math.max(2, Math.ceil((2 * limit) / pitch)));
    const sweep = round((columns * pitch) / 2);
    return { columns, sweep, unit: round(unit), limit: round(Math.min(sweep, limit)) };
  };
  const u = (n) => `calc(${round(n)} * min(${tileHeight}cqh, ${round(MAX_WIDTH / aspect)}cqw))`;
  const r = 100 * arc(bend), radius = `${+r.toFixed(3)}cqw`;
  const turn = (d) => `translateZ(${radius}) rotateY(${round(d)}deg) translateZ(-${radius})`;
  const mask = `linear-gradient(90deg,transparent,#000 ${fade}%,#000 ${100 - fade}%,transparent)`;
  Object.assign(root.style, { perspective: `${+(r * CAMERA).toFixed(3)}cqw`, perspectiveOrigin: `50% ${axis}%`, maskImage: mask, webkitMaskImage: mask });
  const style = document.createElement('style'); document.head.appendChild(style);
  const share = aspect / SLICES;
  const paint = (tile, n) => { const v = `var(--mi${((n % N) + N) % N})`; for (const s of tile.children) s.style.backgroundImage = v; };
  let cur = null;
  const render = (L) => {
    const { columns, sweep, unit, limit } = L, duration = columns * speed;
    const hide = round(((sweep - limit) / (2 * sweep || 1)) * 100);
    style.textContent = `@keyframes mbOrbit{from{transform:${turn(-sweep)}}to{transform:${turn(sweep)}}` +
      `0%,${hide}%,${100 - hide}%,100%{visibility:hidden}${hide + 0.001}%,${100 - hide - 0.001}%{visibility:visible}}` +
      `@media(prefers-reduced-motion:reduce){.mb-tile{animation-play-state:paused}}`;
    root.textContent = '';
    for (let t = 0; t < columns; t++) {
      const first = columns - 1 - t;  // numbers tiles in the order they come on
      const tile = document.createElement('div'); tile.className = 'mb-tile';
      Object.assign(tile.style, { left: `calc(50% - ${u(aspect / 2)})`, top: `calc(${axis}% - ${u(0.5)})`, width: u(aspect), height: u(1),
        animation: `mbOrbit ${duration}s linear ${-t * speed}s infinite` });
      for (let k = 0; k < SLICES; k++) {
        const s = document.createElement('div'); s.className = 'mb-strip' + (k === 0 ? ' l' : k === SLICES - 1 ? ' r' : '');
        Object.assign(s.style, { left: u((aspect - share) / 2), width: k === SLICES - 1 ? u(share) : `calc(${u(share)} + 1px)`, height: u(1),
          transform: turn((aspect / 2 - (k + 0.5) * share) * unit), backgroundSize: `${u(aspect)} ${u(1)}`, backgroundPosition: `${u(-k * share)} 0` });
        tile.appendChild(s);
      }
      paint(tile, first);
      // a tile takes its next image when it wraps, out of sight; elapsedTime counts whole loops
      tile.addEventListener('animationiteration', (e) => paint(tile, Math.round(e.elapsedTime / duration) * columns + first));
      root.appendChild(tile);
    }
    root.classList.add('on');
  };
  new ResizeObserver(([entry]) => {
    const { width, height } = entry.contentRect;
    tileHeight = width < 760 ? 30 : 38;
    const next = measure(width, height);
    if (!next || (cur && cur.columns === next.columns && cur.sweep === next.sweep && cur.unit === next.unit)) return;
    cur = next; render(next);
  }).observe(host);
})();
</script>
"""
