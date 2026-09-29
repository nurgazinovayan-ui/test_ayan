"""Shared engine and UI components for the ten premium-SaaS ONEFLOW promos (motion/premium/pNN-*.html).

Every animation is a CSS animation on one absolute timeline (paused, scrubbed by window.seek(t)); camera moves that are
easier as math live in window.FRAME(t) and use KEY(keys, t) — eased keyframe interpolation. Components take absolute
start times, so each variant places the same product story on its own storyboard.

Timing helper: an(d, o, i=…, out=…) → 'class="an" style="--d:…"' — element enters with keyframes `i` at d and leaves
with `out` at o. Line reveals: ln(text, d, o) — text slides up out of a mask.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'landing'))
import v4_porcelain as v  # noqa: E402
import wire  # noqa: E402
from brand import wordmark  # noqa: E402

MARK_D = re.search(r'd="([^"]+)"', v.MARK).group(1)


# ---------------------------------------------------------------- timing helpers
def st(d=None, o=None, i=None, out=None, idur=None, odur=None, ie=None, extra=''):
    s = []
    if d is not None:
        s.append(f'--d:{d:.2f}s')
    if o is not None:
        s.append(f'--o:{o:.2f}s')
    if i:
        s.append(f'--in:{i}')
    if out:
        s.append(f'--out:{out}')
    if idur:
        s.append(f'--id:{idur}s')
    if odur:
        s.append(f'--od:{odur}s')
    if ie:
        s.append(f'--ie:{ie}')
    if extra:
        s.append(extra.strip(';'))
    return ';'.join(s)


def an(d=None, o=None, cls='', **kw):
    return f'class="an {cls}" style="{st(d, o, **kw)}"'


def ln(text, d, o=None, cls='', i='lu', out='lo', idur=.8):
    """One line of type that rises out of a mask (and leaves upward)."""
    return f'<span class="ln {cls}"><span {an(d, o, i=i, out=out, idur=idur)}>{text}</span></span>'


def words(text, d, o=None, step=.08, cls='', i='wb', out='fob', accent=()):
    out_html = []
    for k, wd in enumerate(text.split(' ')):
        c = 'g' if k in accent else ''
        out_html.append(f'<span {an(d + k * step, o, cls=c, i=i, out=out, idur=.7)}>{wd}</span>')
    return f'<span class="wds {cls}">' + ' '.join(out_html) + '</span>'


def mark(cls='mk', fill='url(#mg)'):
    return f'<svg class="{cls}" viewBox="0 0 76 52" aria-hidden="true"><path fill="{fill}" d="{MARK_D}"/></svg>'


def img(n, style=''):
    return f'<i class="im" style="background-image:var(--w-{n});{style}"></i>'


# ---------------------------------------------------------------- base CSS (themed through custom properties)
BASE_CSS = r"""
@property --d { syntax: '<time>'; inherits: false; initial-value: 0s; }
@property --o { syntax: '<time>'; inherits: false; initial-value: 999s; }
@property --in { syntax: '<custom-ident>'; inherits: false; initial-value: fu; }
@property --out { syntax: '<custom-ident>'; inherits: false; initial-value: fo; }
@property --id { syntax: '<time>'; inherits: false; initial-value: .8s; }
@property --od { syntax: '<time>'; inherits: false; initial-value: .45s; }
:root { --e: cubic-bezier(.7,0,.2,1); --e2: cubic-bezier(.16,.84,.24,1); --po: cubic-bezier(.2,1.35,.35,1); }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: 100%; height: 100%; overflow: hidden; background: #000; }
#st { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; overflow: hidden; background: var(--bg); color: var(--ink); font-family: var(--f-body);
  -webkit-font-smoothing: antialiased; transform-origin: 0 0; }
#st::after { content: ''; position: absolute; inset: 0; z-index: 90; pointer-events: none; opacity: var(--grain, .045);
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .5 0 0 0 0 .5 0 0 0 0 .5 0 0 0 1 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>"); }
.sc { position: absolute; inset: 0; }
.an { animation: var(--in) var(--id) var(--ie, var(--e2)) var(--d) both, var(--out) var(--od) var(--e) var(--o) forwards; }
@keyframes fu { from { opacity: 0; transform: translateY(40px); filter: blur(10px); } }
@keyframes fi { from { opacity: 0; } }
@keyframes bi { from { opacity: 0; transform: scale(1.08); filter: blur(24px); } }
@keyframes wb { from { opacity: 0; transform: translateY(.25em); filter: blur(14px); } }
@keyframes pi { from { opacity: 0; transform: scale(.72); filter: blur(8px); } }
@keyframes zi { from { opacity: 0; transform: scale(.9); } }
@keyframes lu { from { transform: translateY(135%); } }
@keyframes wr { from { clip-path: inset(0 100% 0 0); } }
@keyframes sr { from { opacity: 0; transform: translateX(140px); filter: blur(10px); } }
@keyframes sl { from { opacity: 0; transform: translateX(-140px); filter: blur(10px); } }
@keyframes rise { from { opacity: 0; transform: perspective(1600px) rotateX(26deg) translateY(160px) scale(.94); filter: blur(12px); } }
@keyframes grow { from { transform: scaleX(0); } }
@keyframes fo { to { opacity: 0; } }
@keyframes fob { to { opacity: 0; filter: blur(16px); } }
@keyframes lo { to { transform: translateY(-135%); opacity: 0; } }
@keyframes zo { to { opacity: 0; transform: scale(1.06); filter: blur(12px); } }
@keyframes zb { to { opacity: 0; transform: scale(.92); filter: blur(12px); } }
@keyframes uo { to { opacity: 0; transform: translateY(-60px); filter: blur(10px); } }
@keyframes spin { to { rotate: 360deg; } }
@keyframes ckp { from { opacity: 0; transform: scale(.3); } }
@keyframes toacc { to { background: var(--acc); color: var(--on-acc, #fff); } }
@keyframes dr { to { stroke-dashoffset: 0; } }
@keyframes push { from { scale: 1; } to { scale: 1.05; } }
.ln { display: inline-block; overflow: hidden; vertical-align: top; padding: .04em 0 .1em; margin: -.04em 0 -.1em; } .ln > span { display: inline-block; }
.wds > span { display: inline-block; }
.g { background: var(--grad); -webkit-background-clip: text; background-clip: text; color: transparent; }
.mut { color: var(--mut); } .mono { font-family: var(--f-mono); }
.disp { font-family: var(--f-disp); font-weight: var(--w-disp, 600); letter-spacing: var(--ls-disp, -.045em); line-height: 1.02; }
.cap { font: 500 30px/1.3 var(--f-body); color: var(--mut); letter-spacing: -.01em; }
.lbl { font: 500 16px var(--f-mono); letter-spacing: .08em; text-transform: uppercase; color: var(--mut); }
.pill { display: inline-flex; align-items: center; gap: 10px; padding: 9px 18px; border-radius: 99px; font: 500 19px var(--f-body); background: var(--panel2); color: var(--ink); box-shadow: inset 0 0 0 1px var(--line); }
.pill.acc { background: var(--grad); color: var(--on-acc, #fff); box-shadow: none; }
.im { display: block; background: var(--panel2) center / cover no-repeat; }
.mk { display: block; }
/* windows */
.win { position: absolute; overflow: hidden; color: var(--ink); background: var(--panel); border-radius: var(--r); box-shadow: 0 0 0 1px var(--line), var(--sh); }
.wbar { display: flex; align-items: center; gap: 8px; height: 50px; padding: 0 20px; border-bottom: 1px solid var(--line); font: 500 16px var(--f-body); color: var(--mut); }
.wbar i { width: 11px; height: 11px; border-radius: 50%; background: var(--line); } .wbar span { margin-left: 12px; color: var(--ink); }
.wbar em { margin-left: auto; font: 500 14px var(--f-mono); font-style: normal; }
.cv { position: absolute; left: 0; right: 0; top: 50px; bottom: 0; background: radial-gradient(var(--dot) 1.2px, transparent 1.7px) 0 0 / 26px 26px; }
.nd { position: absolute; background: var(--panel); border-radius: calc(var(--r) * .75); box-shadow: 0 0 0 1px var(--line), 0 24px 48px -28px rgba(0,0,0,.45); font: 500 17px var(--f-body); color: var(--ink); }
.ndh { display: flex; align-items: center; gap: 10px; padding: 13px 16px; border-bottom: 1px solid var(--line); }
.ndh b { display: grid; place-items: center; width: 28px; height: 28px; border-radius: 8px; background: var(--panel2); color: var(--acc); font-size: 14px; }
.nd small { display: block; margin: 0 16px 14px; font: 400 13px var(--f-mono); color: var(--mut); }
.fr { display: grid; grid-template-columns: 1fr auto; margin: 8px 16px 0; padding: 9px 12px; border-radius: 10px; background: var(--panel2); font: 500 15px var(--f-body); }
.fr em { font: 400 13px var(--f-mono); color: var(--mut); font-style: normal; }
.btn { display: inline-flex; align-items: center; justify-content: center; gap: 8px; padding: 13px 20px; border-radius: 12px; background: var(--ink); color: var(--on-ink, var(--bg)); font: 600 17px var(--f-body); white-space: nowrap; }
.btn.acc { background: var(--grad); color: var(--on-acc, #fff); }
.edges { position: absolute; inset: 0; width: 100%; height: 100%; overflow: visible; }
.edges path { fill: none; stroke: var(--acc); stroke-width: 2.2; stroke-dasharray: 1; stroke-dashoffset: 1; animation: dr .6s var(--e2) var(--d) forwards; }
.outs { display: flex; flex-wrap: wrap; align-items: flex-end; gap: 10px; padding: 16px; }
.outs .im { border-radius: 6px; background-size: cover; }
/* formats */
.fmts { position: absolute; display: flex; align-items: flex-end; gap: 34px; }
.fc { display: flex; flex-direction: column; gap: 14px; } .fc .im { border-radius: calc(var(--r) * .6); box-shadow: 0 0 0 1px var(--line); }
.fl { display: flex; align-items: center; gap: 10px; font: 600 20px var(--f-body); } .fl em { font: 400 15px var(--f-mono); color: var(--mut); font-style: normal; }
.ok { display: grid; place-items: center; width: 24px; height: 24px; margin-left: auto; border-radius: 50%; background: var(--acc); color: var(--on-acc, #fff); font: 700 13px var(--f-body); }
/* progress */
.prog { position: absolute; } .prog .pb { position: relative; height: 10px; border-radius: 5px; background: var(--panel2); box-shadow: inset 0 0 0 1px var(--line); overflow: hidden; }
.prog .pb i { position: absolute; inset: 0; border-radius: 5px; background: var(--grad); transform-origin: 0 50%; }
.prog .ph { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 18px; font: 500 24px var(--f-body); color: var(--mut); }
.prog .ph b { font: 600 64px/1 var(--f-disp); letter-spacing: -.04em; color: var(--ink); } .prog .ph b small { font-size: 28px; color: var(--mut); }
/* models */
.mods { position: absolute; display: flex; gap: 24px; }
.mo { width: 250px; padding: 12px; border-radius: calc(var(--r) * .8); background: var(--panel); box-shadow: 0 0 0 1px var(--line), var(--sh); }
.mo .im { height: 170px; border-radius: calc(var(--r) * .55); } .mo b { display: block; margin: 12px 4px 2px; font: 600 20px var(--f-body); } .mo small { margin: 0 4px; font: 400 14px var(--f-mono); color: var(--mut); }
/* trends */
.trh { display: flex; align-items: center; gap: 10px; padding: 22px 26px 10px; } .trh b { font: 600 26px var(--f-body); margin-right: auto; }
.trh span, .chip { padding: 7px 13px; border-radius: 9px; background: var(--panel2); font: 500 14px var(--f-body); color: var(--mut); }
.trw { display: grid; grid-template-columns: 64px 1fr auto auto; gap: 18px; align-items: center; margin: 0 14px; padding: 12px; border-radius: 14px; }
.trw.on { background: var(--panel2); } .trw .im { width: 64px; height: 64px; border-radius: 10px; }
.trw small { font: 500 13px var(--f-mono); color: var(--mut); } .trw b { display: block; font: 600 20px var(--f-body); } .trw em { font: 600 22px var(--f-body); font-style: normal; color: var(--acc); }
.trw .btn { padding: 9px 14px; font-size: 14px; border-radius: 9px; } .trw .ghost { visibility: hidden; }
.adc { position: absolute; padding: 22px; border-radius: var(--r); background: var(--panel); box-shadow: 0 0 0 1px var(--line), var(--sh); }
.adc .hd { display: flex; align-items: center; gap: 14px; margin: 16px 0 12px; } .adc .hd .im { width: 70px; height: 70px; border-radius: 12px; }
.adc .hd b { display: block; font: 600 22px var(--f-body); } .adc .hd small { font: 400 15px var(--f-body); color: var(--mut); }
.adc .st2 { display: block; margin-top: 8px; padding: 11px 14px; border-radius: 12px; background: var(--panel2); font: 500 16px var(--f-body); } .adc .st2 em { font: 500 14px var(--f-mono); color: var(--acc); font-style: normal; margin-right: 8px; }
/* texts */
.chat { position: absolute; left: 0; right: 0; top: 50px; bottom: 0; display: flex; flex-direction: column; gap: 18px; padding: 26px 30px; }
.ub { align-self: flex-end; max-width: 86%; min-height: 58px; padding: 16px 20px; border-radius: 20px 20px 6px 20px; background: var(--ink); color: var(--on-ink, var(--bg)); font: 400 22px/1.4 var(--f-body); }
.ab { align-self: flex-start; max-width: 92%; padding: 18px 22px; border-radius: 20px 20px 20px 6px; background: var(--panel2); font: 400 22px/1.5 var(--f-body); }
.tyc::after { content: '▍'; color: var(--acc); }
.doc { display: flex; align-items: center; gap: 14px; align-self: flex-start; padding: 12px 20px 12px 12px; border-radius: 16px; background: var(--panel2); box-shadow: inset 0 0 0 1px var(--line); }
.doc i { display: grid; place-items: center; width: 48px; height: 48px; border-radius: 11px; background: var(--acc); color: var(--on-acc, #fff); font: 700 13px var(--f-body); font-style: normal; }
.doc b { font: 600 20px var(--f-body); } .doc small { display: block; font: 400 15px var(--f-body); color: var(--mut); }
/* predictor */
.pcs { position: absolute; display: flex; gap: 30px; }
.pc { position: relative; width: 300px; padding: 12px 12px 18px; border-radius: var(--r); background: var(--panel); box-shadow: 0 0 0 1px var(--line), var(--sh); }
.pc .im { height: 300px; border-radius: calc(var(--r) * .7); } .pc .sc2 { display: flex; justify-content: space-between; align-items: baseline; margin: 16px 6px 10px; }
.pc .sc2 span { font: 500 17px var(--f-body); color: var(--mut); } .pc .sc2 b { font: 600 40px/1 var(--f-disp); letter-spacing: -.03em; } .pc .sc2 b small { font-size: 18px; color: var(--mut); }
.pc .bar { height: 8px; margin: 0 6px; border-radius: 4px; background: var(--panel2); overflow: hidden; } .pc .bar i { display: block; height: 100%; border-radius: 4px; background: var(--grad); transform-origin: 0 50%; }
.pc .best { position: absolute; left: 50%; top: -18px; transform: translateX(-50%); white-space: nowrap; }
.pc .cap2 { position: absolute; left: 24px; right: 24px; top: 262px; padding: 8px 12px; border-radius: 10px; background: rgba(15,18,34,.8); color: #fff; font: 600 16px var(--f-body); }
@keyframes dim { to { opacity: .4; filter: saturate(.2); } } @keyframes win { to { transform: scale(1.06); } }
/* assistant */
.asw { display: grid; grid-template-columns: 470px 1fr; }
.asc { display: flex; flex-direction: column; gap: 14px; padding: 24px; border-right: 1px solid var(--line); background: var(--panel2); }
.ash { display: flex; align-items: center; gap: 12px; padding-bottom: 16px; border-bottom: 1px solid var(--line); } .ash b { display: block; font: 600 20px var(--f-body); } .ash small { font: 500 14px var(--f-body); color: #22c55e; }
.ava { display: grid; place-items: center; width: 44px; height: 44px; border-radius: 50%; background: var(--grad); } .ava .mk { width: 24px; }
.asc .ub { font-size: 19px; padding: 14px 16px; min-height: 50px; } .asc .ar { font: 500 18px var(--f-body); }
.stp { display: flex; align-items: center; gap: 12px; padding: 11px 14px; border-radius: 12px; background: var(--panel); box-shadow: inset 0 0 0 1px var(--line); font: 500 17px var(--f-body); }
.stp .sp { position: relative; width: 24px; height: 24px; flex: none; }
.stp .sp::before { content: ''; position: absolute; inset: 0; border-radius: 50%; border: 3px solid var(--line); border-top-color: var(--acc); animation: spin .7s linear 0s infinite, fo .12s linear var(--k) forwards; }
.stp .sp::after { content: '✓'; position: absolute; inset: 0; display: grid; place-items: center; border-radius: 50%; background: var(--acc); color: var(--on-acc, #fff); font: 700 13px var(--f-body); animation: ckp .35s var(--po) var(--k) both; }
.stp.hint { color: var(--acc); box-shadow: inset 0 0 0 1.5px var(--acc); } .stp.hint .sp::before { display: none; } .stp.hint .sp::after { content: '▸'; animation-delay: var(--d); }
.acv2 { position: relative; background: radial-gradient(var(--dot) 1.2px, transparent 1.7px) 0 0 / 26px 26px; }
.acv2 .nd { top: 190px; width: 190px; font-size: 15px; } .acv2 .ndh { padding: 11px 12px; } .acv2 .nd .im { height: 130px; margin: 10px; border-radius: 8px; }
.acv2 .fr { margin: 6px 10px 0; padding: 7px 9px; font-size: 13px; } .acv2 .fr:last-child { margin-bottom: 10px; }
.lnx { display: block; height: 10px; margin: 10px 12px 0; border-radius: 5px; background: var(--panel2); } .lnx:last-child { margin-bottom: 12px; width: 60%; }
.auto { position: absolute; right: 22px; top: 18px; }
/* logo */
.logo { position: absolute; display: flex; align-items: center; gap: 34px; color: var(--ink); } .logo .mk { width: 130px; } .logo b { display: block; } .logo b .wm { display: block; height: 101px; width: auto; }
.wmb { display: block; height: 20px; width: auto; }
.fnote { position: absolute; left: 0; right: 0; bottom: 48px; text-align: center; font: 400 18px var(--f-body); color: var(--mut); opacity: .8; }
"""

ENGINE_JS = r"""
(function () {
  const st = document.getElementById('st'), q = new URLSearchParams(location.search), T = __T__;
  window.DUR = T;
  const counters = [...document.querySelectorAll('[data-count]')], typers = [...document.querySelectorAll('[data-type]')];
  const io = (x) => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
  // KEY([[t, a, b, …], …], t) → eased values between keyframes (holds before the first / after the last)
  window.KEY = (keys, t, ease = io) => {
    if (t <= keys[0][0]) return keys[0].slice(1);
    for (let i = 1; i < keys.length; i++) if (t <= keys[i][0]) { const a = keys[i - 1], b = keys[i], p = ease((t - a[0]) / (b[0] - a[0] || 1)); return a.slice(1).map((v, j) => v + (b[j + 1] - v) * p); }
    return keys[keys.length - 1].slice(1);
  };
  let AN = null;
  window.seek = (t) => {
    if (!AN) { AN = document.getAnimations(); AN.forEach((a) => a.pause()); }
    AN.forEach((a) => { a.currentTime = t * 1000; });
    counters.forEach((el) => { const [s, d, a, b, dec] = el.dataset.count.split(',').map(Number), p = Math.min(1, Math.max(0, (t - s) / d)), e = 1 - Math.pow(1 - p, 3);
      el.textContent = (el.dataset.pre || '') + (a + (b - a) * e).toFixed(dec || 0) + (el.dataset.suf || ''); });
    typers.forEach((el) => { const [s, cps] = el.dataset.type.split(',').map(Number), n = Math.max(0, Math.min(el.dataset.txt.length, Math.floor((t - s) * cps)));
      el.textContent = el.dataset.txt.slice(0, n); el.classList.toggle('tyc', n > 0 && n < el.dataset.txt.length); });
    if (window.FRAME) window.FRAME(t);
  };
  const fit = () => { const k = Math.min(innerWidth / 1920, innerHeight / 1080); st.style.transform = 'translate(' + (innerWidth - 1920 * k) / 2 + 'px,' + (innerHeight - 1080 * k) / 2 + 'px) scale(' + k + ')'; };
  if (q.get('cap')) { window.seek(+(q.get('t') || 0)); return; }
  fit(); addEventListener('resize', fit);
  let t0 = null; const loop = (now) => { if (t0 === null) t0 = now; window.seek(((now - t0) / 1000) % T); requestAnimationFrame(loop); };
  document.fonts.ready.then(() => requestAnimationFrame(loop));
})();
"""

FOOT = '* до 50% — в сравнении с оплатой тех же моделей в отдельных сервисах; итог зависит от моделей и объёма. Неизрасходованный бюджет переходит на следующий месяц.'


def page(title, theme_css, body, T, frame_js='', wire_pal=None, grad_stops=('#8fc6ff', '#4d7cff', '#3b5cff')):
    a, b, c = grad_stops
    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="../../landing/fonts.css">
<link rel="stylesheet" href="../fonts-extra.css">
<style>
{BASE_CSS}
{wire.css_vars(':root', wire_pal)}
{theme_css}
</style>
</head>
<body>
<div id="st">
<svg width="0" height="0" style="position:absolute"><defs><linearGradient id="mg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a}"/><stop offset=".55" stop-color="{b}"/><stop offset="1" stop-color="{c}"/></linearGradient></defs></svg>
{body}
</div>
<script>{frame_js}</script>
<script>{ENGINE_JS.replace('__T__', f'{T:.3f}')}</script>
</body>
</html>
"""


# ---------------------------------------------------------------- components (absolute start times)
def win(inner, style, title='ONEFLOW', right='', cls='', attrs=''):
    return (f'<div class="win {cls}" style="{style}" {attrs}><div class="wbar"><i></i><i></i><i></i><span>{title}</span><em>{right}</em></div>{inner}</div>')


def nodes(t, style='', cls='', attrs=''):
    """Node canvas: image → adaptation → result (1240×700)."""
    rows = ''.join(f'<div class="fr"><span>{a}</span><em>{b}</em></div>' for a, b in (('Stories 9:16', '1080×1920'), ('Пост 1:1', '1080×1080'), ('Kaspi', '1125×330'), ('Discovery', '1200×628')))
    outs = ''.join(f'<i {an(t + 1.5 + k * .1, i="pi", idur=.5, cls="im")[:-1]};width:{w}px;height:{h}px;background-image:var(--w-bunny)"></i>'
                   for k, (w, h) in enumerate(((66, 118), (100, 100), (150, 78), (170, 50))))
    inner = (f'<div class="cv"><svg class="edges" viewBox="0 0 1240 650"><path pathLength="1" style="--d:{t + .75:.2f}s" d="M320 300 C 370 300 370 270 420 270"/>'
             f'<path pathLength="1" style="--d:{t + 1.05:.2f}s" d="M820 270 C 870 270 870 300 920 300"/></svg>'
             f'<div {an(t + .1, i="pi", idur=.6, cls="nd")[:-1]};left:50px;top:120px;width:270px"><div class="ndh"><b>▣</b>Изображение</div>{img("bunny", "height:210px;margin:14px 16px 10px;border-radius:10px")}<small>мягкий-зайка.webp</small></div>'
             f'<div {an(t + .4, i="pi", idur=.6, cls="nd")[:-1]};left:420px;top:95px;width:400px"><div class="ndh"><b>⌗</b>Адаптация</div>{rows}<div class="btn acc" style="margin:16px;width:calc(100% - 32px)">✦ Сгенерировать</div></div>'
             f'<div {an(t + .7, i="pi", idur=.6, cls="nd")[:-1]};left:920px;top:150px;width:270px"><div class="ndh"><b>▦</b>Результат</div><div class="outs">{outs}</div></div></div>')
    return win(inner, style, 'Холст · Мягкий зайка', '$0.00 / $50', cls, attrs)


FORMATS = (('Stories 9:16', '1080×1920', 180, 320, 'bunny'), ('Пост 1:1', '1080×1080', 280, 280, 'coffee'), ('Kaspi', '1125×330', 400, 118, 'airbuds'), ('Discovery', '1200×628', 400, 210, 'watch'))


def formats(t, style='', step=.14, scale=1.0, o=None):
    out = ''
    for k, (a, b, w, h, p) in enumerate(FORMATS):
        out += (f'<div {an(t + k * step, o, i="pi", out="fob", idur=.6)}><div class="fc">{img(p, f"width:{w * scale:.0f}px;height:{h * scale:.0f}px")}'
                f'<div class="fl">{a}<em>{b}</em><span class="ok an" style="{st(t + .9 + k * step, i="ckp", idur=.4)}">✓</span></div></div></div>')
    return f'<div class="fmts" style="{style}">{out}</div>'


def progress(t, dur, style='', label='Адаптация под 4 формата', o=None):
    return (f'<div class="prog an" style="{st(t - .25, o, i="fu", out="fob", idur=.5)};{style}"><div class="ph"><span>{label}</span><b><span data-count="{t},{dur},0,100,0">0</span><small>/100</small></b></div>'
            f'<div class="pb"><i class="an" style="{st(t, i="grow", idur=dur, ie="cubic-bezier(.3,.6,.3,1)")}"></i></div></div>')


MODELS = (('Nano Banana Pro', 'coffee'), ('Veo 3.1', 'watch'), ('Kling', 'airbuds'), ('Seedream', 'robot'))


def models(t, style='', step=.1, o=None):
    return (f'<div class="mods" style="{style}">' + ''.join(f'<div {an(t + k * step, o, i="pi", out="fob", idur=.6)}><div class="mo">{img(p)}<b>{n}</b><small>генерация · 4 сек</small></div></div>'
                                                          for k, (n, p) in enumerate(MODELS)) + '</div>')


TRENDS = (('pyramid', 'TikTok', 'Товар в неожиданном масштабе', '318K'), ('robot', 'Instagram', 'Один предмет — три сценария', '132K'),
          ('body', 'TikTok', 'Честный обзор вместо рекламы', '174K'), ('speaker', 'Instagram', 'Распаковка без лица', '78K'))


def trends(t, style='', click=None, cls='', attrs=''):
    """Trends list (1060×520); the first row's «Адаптировать» turns accent at `click`."""
    click = click if click is not None else t + 1.4
    rows = ''
    for k, (p, pl, ti, m) in enumerate(TRENDS):
        btn = (f'<span class="btn an" style="{st(click, i="toacc", idur=.25)}">✦ Адаптировать</span>' if k == 0 else '<span class="btn ghost">✦ Адаптировать</span>')
        rows += f'<div {an(t + .2 + k * .1, i="fu", idur=.6, cls="trw" + (" on" if k == 0 else ""))}>{img(p)}<div><small>{pl}</small><b>{ti}</b></div><em>{m}</em>{btn}</div>'
    inner = f'<div style="position:absolute;inset:50px 0 0">{"<div class=trh><b>Тренды</b><span>Все площадки</span><span>За 7 дней</span></div>"}{rows}</div>'
    return win(inner, style, 'Тренды', 'обновлено сегодня', cls, attrs)


def adapted(t, style='', o=None):
    steps = ''.join(f'<span {an(t + .25 + k * .2, i="fu", idur=.5, cls="st2")}><em>{a}</em>{b}</span>'
                    for k, (a, b) in enumerate((('0–1 с', 'зайка крупно в ладони'), ('1–4 с', 'камера отъезжает: рядом огромная кровать'), ('4–7 с', 'название и цена на экране'))))
    return (f'<div {an(t, o, i="pi", out="fob", idur=.6, cls="adc")[:-1]};{style}"><span class="pill acc">✦ Адаптировано под ваш товар</span>'
            f'<div class="hd">{img("bunny")}<div><b>Мягкий зайка</b><small>по тренду «Товар в неожиданном масштабе»</small></div></div>{steps}</div>')


ANSWER = 'Мягкая игрушка «Зайка» из нежного плюша с гипоаллергенным наполнителем. Подходит детям с рождения: безопасные материалы, прочные швы.'


def texts(t, style='', cls='', attrs=''):
    """Chat for texts & documents (1100×520): typed request, streamed answer, .docx."""
    inner = (f'<div class="chat"><div {an(t + .3, i="fu", idur=.4, cls="ub")}><span data-type="{t + .45:.2f},40" data-txt="SEO-описание для Kaspi: мягкий зайка"></span></div>'
             f'<div {an(t + 1.45, i="fu", idur=.4, cls="ab")}><span data-type="{t + 1.5:.2f},95" data-txt="{ANSWER}"></span></div>'
             f'<div {an(t + 3.0, i="ckp", idur=.45, cls="doc")}><i>DOCX</i><div><b>Описание_Kaspi.docx</b><small>готово к скачиванию</small></div></div></div>')
    return win(inner, style, 'Тексты', 'DOCX · XLSX · PPTX', cls, attrs)


def predictor(t, style='', step=.1, o=None):
    """Three creative variants; scores count up at t+1.0, the winner is picked at t+2.1."""
    V = ((64, 'filter:saturate(.5) brightness(1.05)', ''), (91, '', '<span class="cap2">Мягкий зайка · 0+</span>'), (77, 'background-size:170%;background-position:50% 35%', ''))  # noqa: N806
    out = ''
    for k, (sc, fx, cap) in enumerate(V):
        winr = k == 1
        anim = (f'pi .6s var(--po) {t + k * step:.2f}s both, ' + (f'win .5s var(--po) {t + 2.1:.2f}s both' if winr else f'dim .4s var(--e2) {t + 2.1:.2f}s both'))
        best = f'<span class="pill acc best an" style="{st(t + 2.15, i="ckp", idur=.45)}">★ Лучший для Kaspi</span>' if winr else ''
        if o is not None:
            anim += f', fob .45s var(--e) {o:.2f}s forwards'
        out += (f'<div class="pc" style="animation:{anim}">{img("bunny", fx)}<div class="sc2"><span>Вариант {k + 1}</span><b><span data-count="{t + 1.0:.2f},.9,0,{sc},0">0</span><small>/100</small></b></div>'
                f'<div class="bar"><i class="an" style="{st(t + 1.0, i="grow", idur=.9)};width:{sc}%"></i></div>{best}</div>')
    return f'<div class="pcs" style="{style}">{out}</div>'


def assistant(t, style='', cls='', attrs=''):
    """AI assistant (1500×700): request → steps with spinners → nodes appear → «Проверьте и нажмите «Запустить»»."""
    steps = ''.join(f'<div {an(t + d, i="fu", idur=.4, cls="stp")[:-1]};--k:{t + k2:.2f}s"><i class="sp"></i>{s}</div>'
                    for d, k2, s in ((1.75, 2.1, 'Разобрал аудиторию и нишу'), (2.15, 2.5, 'Подобрал шаблон и промпт'), (2.55, 2.9, 'Собрал 4 ноды на холсте')))
    chat = (f'<div class="asc"><div class="ash"><span class="ava">{mark("mk", "#fff")}</span><div><b>Floko</b><small>● ИИ-ассистент</small></div></div>'
            f'<div {an(t + .2, i="fu", idur=.4, cls="ub")}><span data-type="{t + .3:.2f},42" data-txt="Сделай карточки мягкого зайки для Kaspi и сторис"></span></div>'
            f'<div {an(t + 1.5, i="fu", idur=.4, cls="ar")}>Готово, собрал схему:</div>{steps}'
            f'<div {an(t + 3.1, i="fu", idur=.4, cls="stp hint")[:-1]};--k:{t + 3.1:.2f}s"><i class="sp"></i>Проверьте и нажмите «Запустить»</div></div>')
    N = ((f'<b>▣</b>Фото товара', img('bunny')), ('<b>✦</b>Шаблон', '<div style="display:flex;gap:6px;margin:10px">' + img('pajama', 'flex:1;height:110px;border-radius:6px') + img('body', 'flex:1;height:110px;border-radius:6px') + '</div>'),  # noqa: N806
         ('<b>⌗</b>Адаптация', ''.join(f'<div class="fr"><span>{a}</span><em>{b}</em></div>' for a, b in (('Kaspi', '1125×330'), ('Stories', '1080×1920'), ('Пост', '1080×1080')))),
         ('<b>¶</b>Текст', '<i class="lnx"></i><i class="lnx"></i><i class="lnx"></i>'))
    nd = ''.join(f'<div {an(t + 1.85 + k * .4, i="pi", idur=.55, cls="nd")[:-1]};left:{30 + k * 250}px"><div class="ndh">{h}</div>{b}</div>' for k, (h, b) in enumerate(N))
    edges = ''.join(f'<path pathLength="1" style="--d:{t + 2.15 + k * .4:.2f}s" d="M{220 + k * 250} 290 L{280 + k * 250} 290"/>' for k in range(3))
    canvas = (f'<div class="acv2"><span class="lbl" style="position:absolute;left:28px;top:24px">Холст · Проект «Зайка»</span>'
              f'<span class="pill acc auto an" style="{st(t + 3.1, i="ckp", idur=.45)}">✦ Собрано ассистентом</span>'
              f'<svg class="edges" viewBox="0 0 1030 650" preserveAspectRatio="none">{edges}</svg>{nd}</div>')
    return win(f'<div class="asw" style="position:absolute;inset:50px 0 0">{chat}{canvas}</div>', style, 'ИИ-ассистент', '', cls, attrs)


def logo(t, style='', o=None, big=1.0):
    return (f'<div class="logo" style="{style}"><span {an(t, o, i="pi", idur=.7)}>{mark("mk", "currentColor")}</span>'
            f'<b class="an" style="{st(t + .25, o, i="wr", idur=.8)}">{wordmark()}</b></div>')
