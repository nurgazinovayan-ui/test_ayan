"""07 · Orbit — a glowing ONEFLOW core on tilted orbits. Formats fly into the inner orbit, thirty model dots fill the
outer one, feature satellites circle the core; the camera dives through the orbit into each satellite's screen and
pulls back out; at the end everything spirals into the core, which becomes the logo."""
from lib import FOOT, adapted, an, assistant, img, ln, logo, mark, models, nodes, page, predictor, progress, st, texts, trends, words

NAME, TITLE = 'orbit', 'Orbit — ядро и функции на орбитах, нырки внутрь'
T = 39.0
THEME = """
:root { --bg: radial-gradient(ellipse 60% 60% at 50% 50%, #120d24, #000 72%); --ink: #fff; --mut: #8d8d98; --panel: #0e0e14; --panel2: #181822; --line: rgba(255,255,255,.1);
  --dot: rgba(255,255,255,.06); --acc: #9b7bff; --on-ink: #0b0b10; --grad: linear-gradient(90deg, #a78bfa, #22d3ee); --r: 20px; --sh: 0 50px 100px -40px rgba(0,0,0,.9);
  --f-disp: 'Manrope'; --f-body: 'Inter'; --f-mono: 'JetBrains Mono'; --w-disp: 700; --ls-disp: -.05em; --grain: .05; }
#orbw { position: absolute; left: 960px; top: 540px; width: 0; height: 0; }
.rings { position: absolute; left: -900px; top: -400px; width: 1800px; height: 800px; overflow: visible; }
.rings ellipse { fill: none; stroke: rgba(255,255,255,.11); stroke-width: 1.2; } .rings .d { stroke-dasharray: 3 9; stroke: rgba(167,139,250,.35); }
.core { position: absolute; left: -110px; top: -110px; width: 220px; height: 220px; z-index: 50; border-radius: 50%; display: grid; place-items: center;
  background: radial-gradient(circle at 35% 30%, #3b2d7a, #120c2b 70%); box-shadow: 0 0 0 1px rgba(167,139,250,.4), 0 0 120px rgba(139,92,246,.55), inset 0 0 40px rgba(34,211,238,.25); }
.core .mk { width: 110px; }
.sat { position: absolute; left: 0; top: 0; white-space: nowrap; }
.chip2 { display: flex; align-items: center; gap: 12px; padding: 8px 18px 8px 8px; border-radius: 99px; background: rgba(20,20,30,.9); box-shadow: 0 0 0 1px var(--line); font: 600 20px var(--f-body); }
.chip2 .im { width: 44px; height: 44px; border-radius: 50%; } .chip2 i.ic { display: grid; place-items: center; width: 40px; height: 40px; border-radius: 50%; background: var(--grad); color: #0b0b10; font-style: normal; font-size: 18px; }
.chip2.hi { box-shadow: 0 0 0 1.5px #a78bfa, 0 0 40px rgba(167,139,250,.7); }
.dt { width: 10px; height: 10px; border-radius: 50%; background: #a78bfa; box-shadow: 0 0 12px rgba(167,139,250,.8); }
.ctr { position: absolute; left: 0; right: 0; text-align: center; z-index: 60; } .h1 { font-size: 140px; } .h3 { font-size: 64px; }
.scene { position: absolute; inset: 0; z-index: 70; }
"""
SCENES = [(12.5, 16.0), (17.2, 21.0), (21.7, 25.2), (25.9, 29.2), (29.9, 33.8)]
FEAT = (('⌗', 'Адаптация'), ('↗', 'Тренды'), ('¶', 'Тексты'), ('★', 'Predictor'), ('✦', 'Ассистент'))
NAMED = {0: 'Nano Banana Pro', 8: 'Veo 3.1', 15: 'Kling', 23: 'Seedream'}


def scene(k, inner):
    s, e = SCENES[k]
    return f'<div {an(s, e - .05, i="bi", out="zo", idur=.7, cls="scene")}>{inner}</div>'


CNT30 = '<span class="g"><span data-count="8.5,1.6,0,30,0" data-suf="+">0</span></span> нейросетей'


def build():
    b = ['<div id="orbw"><svg class="rings" viewBox="-900 -400 1800 800">'
         + ''.join(f'<ellipse class="{c}" rx="{r}" ry="{r * .4:.0f}"/>' for r, c in ((230, ''), (370, 'd'), (520, ''), (690, 'd'), (860, ''))) + '</svg>']
    b.append(f'<div class="core an" style="{st(5.3, i="pi", idur=.8)}">{mark()}</div>')
    for k, (n, p) in enumerate((('Фото', 'bunny'), ('Видео', 'hoodie'), ('Тексты', 'body'), ('Баннеры', 'speaker'))):
        b.append(f'<div class="sat s1"><div class="chip2">{img(p)}{n}</div></div>')
    for k, (ic, n) in enumerate(FEAT):
        b.append(f'<div class="sat s2"><div class="chip2"><i class="ic">{ic}</i>{n}</div></div>')
    for k in range(30):
        inner = f'<div class="chip2" style="font-size:17px;padding:6px 14px"><span class="dt"></span>{NAMED[k]}</div>' if k in NAMED else '<span class="dt" style="display:block"></span>'
        b.append(f'<div class="sat s3">{inner}</div>')
    b.append('</div>')
    b.append(f'<div class="ctr disp h1" style="top:300px">{ln("Больше контента.", .3, 5.1)}<br>{ln("До <span class=g>50%</span> дешевле*", .9, 5.15)}</div>')
    b.append(f'<div class="ctr cap" style="top:680px;font-size:34px">{ln("Бюджет не сгорает в конце месяца.", 1.7, 5.2)}</div>')
    b.append(f'<div class="ctr disp h3" style="top:80px">{words("Фото. Видео. Тексты. Баннеры.", 5.7, 8.3, step=.1, accent=(0, 2))}</div>')
    b.append(f'<div class="ctr disp h3" style="top:880px"><span class="mut">{ln("Всё в одном окне.", 6.4, 8.3)}</span></div>')
    b.append(f'<div class="ctr disp h3" style="top:80px">{ln(CNT30, 8.45, 11.9)}</div>')
    b.append(scene(0, f'<div class="ctr disp h3" style="top:70px">{ln("Адаптация под 4 формата", 12.7)}</div>'
                      + nodes(12.9, 'left:340px;top:190px;width:1240px;height:700px') + progress(14.5, 1.3, 'left:340px;right:340px;top:925px')))
    b.append(scene(1, f'<div class="ctr disp h3" style="top:70px">{ln("Автоматический анализ трендов.", 17.4, 19.0)}</div><div class="ctr disp h3" style="top:70px">{ln("Адаптируйте их под себя <span class=g>автоматически.</span>", 19.1)}</div>'
                      + trends(17.5, 'left:150px;top:220px;width:1060px;height:600px', click=18.9) + adapted(19.15, 'left:1250px;top:300px;width:520px')))
    b.append(scene(2, f'<div class="ctr disp h3" style="top:70px">{ln("Тексты и документы <span class=g>за секунды.</span>", 21.9)}</div>'
                      f'<div class="ctr cap" style="top:165px">{ln("Описания, посты, контент-планы — сразу в Word, Excel и PowerPoint", 22.05)}</div>' + texts(22.1, 'left:410px;top:260px;width:1100px;height:560px')))
    b.append(scene(3, f'<div class="ctr" style="top:60px"><span {an(26.0, i="pi", cls="pill acc")}>Creative Predictor</span></div>'
                      f'<div class="ctr disp h3" style="top:130px">{ln("<span class=g>Лучший креатив</span> — ещё до запуска рекламы.", 26.1)}</div>' + predictor(26.3, 'left:50%;top:310px;transform:translateX(-50%)')))
    b.append(scene(4, f'<div class="ctr disp h3" style="top:70px">{ln("ИИ-ассистент собирает пайплайн <span class=g>за вас.</span>", 30.0)}</div>' + assistant(30.2, 'left:210px;top:210px;width:1500px;height:720px')))
    b.append(f'<div class="ctr disp h3" style="top:120px">{words("Генерация. Адаптация. Запуск.", 34.3, 36.0, step=.25, accent=(0, 2))}</div>')
    b.append(logo(36.1, 'left:50%;top:420px;transform:translateX(-50%);z-index:80'))
    b.append(f'<div class="ctr" style="top:640px;font:500 34px var(--f-body)"><span {an(36.6, i="fu")}>oneflow.art</span></div>')
    b.append(f'<p class="fnote an" style="{st(36.8, i="fi")}">{FOOT}</p>')
    orb = [[0, .9, .45], [5.2, 1, 1]]
    for s, e in SCENES:
        orb += [[s - .5, 1, 1], [s + .25, 3.6, 0], [e, 3.6, 0], [e + .6, 1, 1]]
    orb += [[35.2, 1, 1], [35.9, .2, 0]]
    js = """
const ORB = %s, SC = %s;
let W, S1, S2, S3;
const place = (els, r, ph, sp, t, rr) => els.forEach((el, k) => {
  const a = ph + k * 2 * Math.PI / els.length + sp * t, x = r * Math.cos(a), y = r * .4 * Math.sin(a), dp = (Math.sin(a) + 1) / 2;
  el.style.transform = `translate(${x}px, ${y}px) translate(-50%%, -50%%) scale(${.78 + .34 * dp})`; el.style.zIndex = Math.round(dp * 100);
});
window.FRAME = (t) => {
  if (!W) { W = document.getElementById('orbw'); S1 = [...W.querySelectorAll('.s1')]; S2 = [...W.querySelectorAll('.s2')]; S3 = [...W.querySelectorAll('.s3')]; }
  const [sc, op] = KEY(ORB, t);
  W.style.transform = `scale(${sc})`; W.style.opacity = op;
  const fall = KEY([[34.2, 1], [35.3, 0]], t)[0];
  place(S1, KEY([[5.4, 1400], [6.5, 230]], t)[0] * fall, .3, .22, t);
  place(S2, KEY([[11.0, 1600], [11.9, 370]], t)[0] * fall, 1.2, -.12, t);
  place(S3, 520 * fall + 40 * (1 - fall) * 0, 2.0, .06, t);
  S3.forEach((el, k) => { el.style.opacity = t > 8.5 + k * .055 ? 1 : 0; });
  S1.forEach((el) => { el.style.opacity = t > 5.45 ? 1 : 0; }); S2.forEach((el) => { el.style.opacity = t > 11.05 ? 1 : 0; });
  S2.forEach((el, k) => { const [s] = SC[k]; el.firstChild.classList.toggle('hi', t > s - 1.3 && t < s + .3); });
};
""" % (orb, [list(x) for x in SCENES])
    return page('ONEFLOW — Orbit', THEME, '\n'.join(b), T, js, wire_pal=dict(ink='#c4b5fd', acc='#22d3ee', bar='#2a2640', bg='#15122a', dot='#221e3a', fill='#15122a', head='#c4b5fd', sw=2.6),
                grad_stops=('#a5f3fc', '#a78bfa', '#7c3aed'))


SHOTS = [2.2, 7.0, 9.9, 11.7, 12.3, 15.2, 20.2, 24.4, 28.6, 33.1, 34.8, 38.0]
