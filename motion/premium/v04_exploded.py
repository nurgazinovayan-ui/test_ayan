"""04 · Exploded 3D — an isometric stack of the product's screens floats in volumetric light; it explodes into layers,
and each layer in turn lifts out of the stack, turns to face the camera and plays; at the end the stack collapses
into the logo. Dark glass, warm orange accent."""
from lib import FOOT, adapted, an, assistant, ln, logo, models, nodes, page, predictor, progress, st, texts, trends, win, words

NAME, TITLE = 'exploded', 'Exploded 3D — изометрический стек экранов'
T = 38.5
THEME = """
:root { --bg: radial-gradient(ellipse 70% 70% at 60% 45%, #171a2b, #05060a 70%); --ink: #f4f4f6; --mut: #8d90a3; --panel: #13151f; --panel2: #1d2030; --line: rgba(255,255,255,.1);
  --dot: rgba(255,255,255,.06); --acc: #ff6a3d; --grad: linear-gradient(90deg, #ff6a3d, #ffb36b); --r: 18px; --sh: 0 50px 100px -40px rgba(0,0,0,.9);
  --f-disp: 'Geologica'; --f-body: 'Inter'; --f-mono: 'JetBrains Mono'; --w-disp: 600; --ls-disp: -.045em; --grain: .05; --on-ink: #0b0c10; }
#scene { position: absolute; inset: 0; perspective: 2600px; perspective-origin: 50% 42%; }
#iso { position: absolute; left: 0; top: 0; width: 0; height: 0; transform-style: preserve-3d; }
.lay { position: absolute; box-shadow: 0 0 0 1px var(--line), 0 0 80px -20px rgba(255,106,61,.18), 0 60px 120px -50px rgba(0,0,0,.95); }
.glow { position: absolute; left: 50%; top: 50%; width: 1500px; height: 1100px; margin: -550px 0 0 -750px; border-radius: 50%;
  background: radial-gradient(ellipse at center, rgba(255,106,61,.2), rgba(255,106,61,.05) 45%, transparent 70%); }
.hl { position: absolute; left: 0; right: 0; top: 64px; z-index: 40; text-align: center; font-size: 66px; }
.side { position: absolute; left: 130px; z-index: 40; }
"""
FOC = [(8.8, 12.6, 0, 0), (15.8, 20.2, -230, 0), (20.4, 24.2, 0, 0), (24.4, 28.2, 0, 0), (28.4, 32.6, 0, 0)]


def build():
    b = ['<div class="glow an" style="--in:fi;--id:2s"></div><div id="scene"><div id="iso">']
    L = [nodes(9.4, 'left:-620px;top:-350px;width:1240px;height:700px', cls='lay'),  # noqa: N806
         trends(16.3, 'left:-530px;top:-300px;width:1060px;height:600px', click=18.1, cls='lay'),
         texts(20.9, 'left:-550px;top:-280px;width:1100px;height:560px', cls='lay'),
         win(predictor(25.0, 'left:120px;top:110px'), 'left:-600px;top:-330px;width:1200px;height:660px', 'Creative Predictor', 'Kaspi', 'lay'),
         assistant(28.9, 'left:-750px;top:-350px;width:1500px;height:700px', cls='lay')]
    b += L
    b.append('</div></div>')
    # screen-space type
    b.append(f'<div class="side disp" style="top:330px;font-size:118px">{ln("Больше контента.", .3, 5.7)}<br>{ln("До <span class=g>50%</span> дешевле*", .9, 5.75)}</div>')
    b.append(f'<div class="side cap" style="top:640px;font-size:34px">{ln("Бюджет не сгорает в конце месяца.", 1.7, 5.8)}</div>')
    b.append(f'<div class="hl disp">{words("Фото. Видео. Тексты. Баннеры.", 6.1, 8.45, step=.1, accent=(0, 2))}</div>')
    b.append(f'<div class="hl disp" style="top:150px;font-size:44px"><span class="mut">{ln("Всё в одном окне.", 6.6, 8.45)}</span></div>')
    b.append(f'<div class="hl disp">{ln("Адаптация под 4 формата", 9.0, 12.5)}</div>')
    b.append(progress(10.9, 1.4, 'left:340px;right:340px;top:935px;z-index:40', o=12.5))
    b.append(f'<div class="side disp" style="top:250px;font-size:250px">{ln("<span class=g>30+</span>", 13.0, 15.5)}</div>'
             f'<div class="side disp" style="top:520px;font-size:80px">{ln("нейросетей", 13.2, 15.5)}</div>')
    b.append(models(13.5, 'left:130px;top:680px;z-index:40;transform:scale(.8);transform-origin:0 0', o=15.5))
    b.append(f'<div class="hl disp">{ln("Автоматический анализ трендов.", 15.9, 17.95)}</div><div class="hl disp">{ln("Адаптируйте их под себя <span class=g>автоматически.</span>", 18.05, 20.1)}</div>')
    b.append(f'<div style="position:absolute;inset:0;z-index:40;pointer-events:none">{adapted(18.3, "left:1360px;top:330px;width:480px", o=20.1)}</div>')
    b.append(f'<div class="hl disp">{ln("Тексты и документы <span class=g>за секунды.</span>", 20.5, 24.1)}</div>')
    b.append(f'<div class="hl cap" style="top:150px;z-index:40;font-size:30px">{ln("Описания, посты, контент-планы — сразу в Word, Excel и PowerPoint", 20.7, 24.1)}</div>')
    b.append(f'<div class="hl disp">{ln("<span class=g>Лучший креатив</span> — ещё до запуска рекламы.", 24.5, 28.1)}</div>')
    b.append(f'<div class="hl disp">{ln("ИИ-ассистент собирает пайплайн <span class=g>за вас.</span>", 28.5, 32.5)}</div>')
    b.append(f'<div class="hl disp" style="top:420px;font-size:100px">{words("Генерация. Адаптация. Запуск.", 33.2, 35.0, step=.28, accent=(0, 2))}</div>')
    b.append(logo(35.2, 'left:50%;top:400px;transform:translateX(-50%);z-index:40'))
    b.append(f'<div class="hl" style="top:620px;font:500 34px var(--f-body)"><span {an(35.7, i="fu")}>oneflow.art</span></div>')
    b.append(f'<p class="fnote an" style="{st(36.0, i="fi")};z-index:40">{FOOT}</p>')
    iso = [[0, 1330, 560, .5, 0, -44], [5.8, 1330, 560, .52, .35, -38], [7.0, 960, 600, .62, 1, -34], [8.8, 960, 590, .62, 1, -32],
           [12.6, 960, 590, .62, 1, -30], [13.2, 1380, 600, .5, 1.1, -26], [15.4, 1380, 600, .5, 1.1, -22], [15.8, 960, 590, .62, 1, -20],
           [32.6, 960, 590, .62, 1, -44], [33.4, 960, 600, .3, 0, -70], [34.2, 960, 600, .02, 0, -110]]
    js = """
const ISO_KEYS = %s, FOC = %s;
let ISO, L;
window.FRAME = (t) => {
  if (!ISO) { ISO = document.getElementById('iso'); L = [...ISO.querySelectorAll(':scope > .lay')]; }
  const [x, y, s, e, rz] = KEY(ISO_KEYS, t);
  ISO.style.transform = `translate(${x}px, ${y}px) scale(${s}) rotateX(56deg) rotateZ(${rz}deg)`;
  const P = FOC.map(([a, b]) => KEY([[a - .05, 0], [a + .85, 1], [b - .2, 1], [b + .5, 0]], t)[0]), any = Math.max(...P);
  L.forEach((el, i) => {
    const p = P[i], z = (i - 2) * 170 * e, dx = FOC[i][2] * p / s, dy = 60 * p / s;
    el.style.transform = `translateZ(${z * (1 - p) + 260 * p}px) rotateZ(${-rz * p}deg) rotateX(${-56 * p}deg) translate(${dx}px, ${dy}px) scale(${1 + (1 / s - 1) * p})`;
    el.style.opacity = t > 33.6 ? Math.max(0, 1 - (t - 33.6) / .5) : (p > .01 ? 1 : 1 - .65 * any);
  });
};
""" % (iso, [list(f) for f in FOC])
    return page('ONEFLOW — Exploded 3D', THEME, '\n'.join(b), T, js, wire_pal=dict(ink='#ffb08f', acc='#ff6a3d', bar='#2a2d40', bg='#171a28', dot='#232638', fill='#171a28', head='#ffb08f', sw=2.6),
                grad_stops=('#ffc58f', '#ff8a4d', '#ff5a3d'))


SHOTS = [2.4, 6.9, 8.4, 11.3, 14.4, 17.2, 19.6, 23.5, 27.4, 31.8, 33.4, 37.5]
