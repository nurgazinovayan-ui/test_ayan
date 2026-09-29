"""02 · Infinite Canvas — one continuous camera over a Figma-like board: every feature is a frame on the board, the
camera glides frame to frame (pulling back between them), multiplayer cursors «Вы» and «ИИ-ассистент» click through
the UI, a live zoom readout in the toolbar; ends on a pull-back to the whole board and the logo."""
from lib import FOOT, adapted, an, assistant, formats, img, ln, logo, mark, models, nodes, page, predictor, progress, st, texts, trends, words
from brand import wordmark  # noqa: E402  (lib puts motion/ on sys.path)

NAME, TITLE = 'canvas', 'Infinite Canvas — одна камера по доске, курсоры'
T = 42.5
THEME = """
:root { --bg: #efefec; --ink: #121212; --mut: #7c7c78; --panel: #fff; --panel2: #f4f4f1; --line: #e2e2dd; --dot: #d2d2cc; --acc: #0d99ff;
  --grad: linear-gradient(90deg, #0d99ff, #7b61ff); --r: 14px; --sh: 0 30px 60px -34px rgba(0,0,0,.28); --f-disp: 'Inter Tight'; --f-body: 'Inter'; --f-mono: 'JetBrains Mono';
  --w-disp: 600; --ls-disp: -.04em; --grain: .03; }
#world { position: absolute; left: 0; top: 0; width: 5600px; height: 3500px; transform-origin: 0 0;
  background: radial-gradient(#d4d4ce 1.6px, transparent 2px) 0 0 / 36px 36px; }
.frm { position: absolute; width: 1600px; height: 900px; background: var(--panel); border-radius: 6px; box-shadow: 0 0 0 1px var(--line), 0 40px 80px -50px rgba(0,0,0,.25); }
.frm > .fl2 { position: absolute; left: 0; top: -40px; font: 500 20px var(--f-mono); color: var(--mut); } .frm > .fl2 b { color: var(--acc); font-weight: 500; }
.in { position: absolute; }
.h { font-size: 118px; } .h2 { font-size: 76px; } .h3 { font-size: 54px; }
.tile4 { position: absolute; left: 90px; top: 250px; display: flex; gap: 30px; }
.tl4 { width: 335px; padding: 12px; border-radius: 16px; background: var(--panel2); box-shadow: inset 0 0 0 1px var(--line); }
.tl4 .im { height: 380px; border-radius: 10px; } .tl4 b { display: block; margin: 14px 6px 4px; font: 600 26px var(--f-body); }
.cur { position: absolute; left: 0; top: 0; z-index: 30; } .cur svg { width: 34px; display: block; } .cur span { position: absolute; left: 26px; top: 28px; padding: 5px 11px; border-radius: 8px;
  font: 600 16px var(--f-body); color: #fff; white-space: nowrap; }
.tb { position: absolute; left: 24px; right: 24px; top: 20px; z-index: 50; display: flex; align-items: center; gap: 14px; height: 60px; padding: 0 18px; border-radius: 14px;
  background: rgba(255,255,255,.86); box-shadow: 0 0 0 1px var(--line), 0 20px 40px -30px rgba(0,0,0,.3); -webkit-backdrop-filter: blur(14px); backdrop-filter: blur(14px); font: 500 17px var(--f-body); }
.tb .mk { width: 30px; } .tb b { font-weight: 600; } .tb .mut { margin-right: auto; }
.av { display: grid; place-items: center; width: 34px; height: 34px; border-radius: 50%; color: #fff; font: 600 14px var(--f-body); }
.zoom { font: 500 16px var(--f-mono); color: var(--mut); min-width: 70px; text-align: right; }
.veil { position: absolute; inset: 0; z-index: 60; background: rgba(239,239,236,.82); -webkit-backdrop-filter: blur(10px); backdrop-filter: blur(10px); }
.fin { position: absolute; inset: 0; z-index: 61; }
"""
ARROW = '<svg viewBox="0 0 24 24"><path d="M3 2 L20 11 L12 13 L9 21 Z" fill="{c}" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/></svg>'
F = {1: (0, 0), 2: (1900, 0), 3: (3800, 0), 4: (3800, 1200), 5: (1900, 1200), 6: (0, 1200), 7: (0, 2400), 8: (1900, 2400), 9: (3800, 2400)}
STOPS = [(1, 0.0, 4.4), (2, 5.3, 8.2), (3, 9.1, 12.2), (4, 13.0, 15.8), (5, 16.6, 19.0), (6, 19.8, 23.8), (7, 24.6, 28.2), (8, 29.0, 32.6), (9, 33.4, 37.4)]


def frame(k, label, inner):
    x, y = F[k]
    return f'<div class="frm" style="left:{x + 100}px;top:{y + 100}px"><span class="fl2"><b>#</b> Frame {k:02d} — {label}</span>{inner}</div>'


def camera_keys():
    z = 1.1
    c = lambda k: (F[k][0] + 900, F[k][1] + 550)  # noqa: E731  frame centre in world coords
    keys = [[0, *c(1), .55], [1.2, *c(1), z]]
    for (a, _, l0), (b, a1, _) in zip(STOPS, STOPS[1:]):
        (x0, y0), (x1, y1) = c(a), c(b)
        keys += [[l0, x0, y0, z], [(l0 + a1) / 2, (x0 + x1) / 2, (y0 + y1) / 2, .62], [a1, x1, y1, z]]
    keys += [[37.4, *c(9), z], [38.5, 2900, 1750, .33], [42.5, 2900, 1750, .31]]
    return keys


def build():
    b = ['<div id="world">']
    b.append(frame(1, 'Оффер', f'<div class="in disp h" style="left:110px;top:120px">{ln("Больше контента.", .7)}</div>'
                                f'<div class="in disp h" style="left:110px;top:290px">{ln("До <span class=g>50%</span> дешевле*", 1.4)}</div>'
                                f'<div class="in disp h3 mut" style="left:114px;top:520px">{ln("Бюджет не сгорает в конце месяца.", 2.3)}</div>'
                                f'<div class="in" style="left:114px;top:700px"><span {an(3.0, i="pi", cls="pill acc")}>oneflow.art</span></div>'))
    tiles = ''.join(f'<div {an(5.6 + k * .15, i="pi")}><div class="tl4">{img(p)}<b>{n}</b></div></div>' for k, (n, p) in enumerate((('Фото', 'bunny'), ('Видео', 'hoodie'), ('Тексты', 'body'), ('Баннеры', 'speaker'))))
    b.append(frame(2, 'Всё в одном окне', f'<div class="in disp h2" style="left:90px;top:80px">{words("Фото. Видео. Тексты. Баннеры.", 5.4, step=.12, accent=(0, 2))}</div>'
                                           f'<div class="tile4">{tiles}</div><div class="in disp h3" style="left:90px;top:760px">{ln("<span class=g>Всё в одном окне.</span>", 6.6)}</div>'))
    b.append(frame(3, 'Холст', nodes(9.25, 'left:180px;top:110px;width:1240px;height:700px', attrs='id="nw"')))
    b.append(frame(4, 'Адаптация', f'<div class="in disp h2" style="left:90px;top:70px">{ln("Адаптация под 4 формата", 13.0)}</div>'
                                    + formats(13.3, 'left:90px;top:230px', step=.12) + progress(13.5, 1.5, 'left:90px;right:90px;top:720px')))
    b.append(frame(5, 'Модели', f'<div class="in disp" style="left:90px;top:60px;font-size:230px">{ln("<span class=g>30+</span>", 16.7)}</div>'
                                 f'<div class="in disp h2" style="left:560px;top:150px">{ln("нейросетей", 16.9)}</div>' + models(17.2, 'left:90px;top:420px')))
    b.append(frame(6, 'Тренды', f'<div class="in disp h3" style="left:90px;top:60px">{ln("Автоматический анализ трендов.", 19.9, 21.8)}</div>'
                                 f'<div class="in disp h3" style="left:90px;top:60px">{ln("Адаптируйте их под себя <span class=g>автоматически.</span>", 21.9)}</div>'
                                 + trends(20.0, 'left:90px;top:190px;width:900px;height:620px', click=21.45, attrs='id="tw"') + adapted(21.7, 'left:1030px;top:250px;width:480px')))
    b.append(frame(7, 'Тексты', f'<div class="in disp h3" style="left:90px;top:60px">{ln("Тексты и документы <span class=g>за секунды.</span>", 24.7)}</div>'
                                 f'<div class="in cap" style="left:92px;top:140px">{ln("Описания, посты, контент-планы — сразу в Word, Excel и PowerPoint", 24.9)}</div>'
                                 + texts(25.0, 'left:90px;top:230px;width:1420px;height:600px')))
    b.append(frame(8, 'Creative Predictor', f'<div class="in" style="left:90px;top:56px"><span {an(29.0, i="pi", cls="pill acc")}>Creative Predictor</span></div>'
                                             f'<div class="in disp h3" style="left:90px;top:120px">{ln("<span class=g>Лучший креатив</span> — ещё до запуска рекламы.", 29.1)}</div>'
                                             + predictor(29.3, 'left:320px;top:280px')))
    b.append(frame(9, 'ИИ-ассистент', f'<div class="in disp h3" style="left:90px;top:56px">{ln("ИИ-ассистент собирает пайплайн <span class=g>за вас.</span>", 33.4)}</div>'
                                       + assistant(33.6, 'left:50px;top:160px;width:1500px;height:700px', attrs='id="aw"')))
    b.append(f'<div class="cur" id="c1">{ARROW.format(c="#121212")}<span style="background:#121212">Вы</span></div>')
    b.append(f'<div class="cur" id="c2">{ARROW.format(c="#7b61ff")}<span style="background:#7b61ff">ИИ-ассистент</span></div>')
    b.append('</div>')
    b.append(f'<div class="tb">{mark()}<b>{wordmark("wmb")}</b><span class="mut">· Доска запуска «Мягкий зайка»</span>'
             '<span class="av" style="background:#121212">Вы</span><span class="av" style="background:#7b61ff">ИИ</span><span class="zoom" id="zm">55%</span></div>')
    b.append(f'<div class="veil an" style="{st(38.6, i="fi", idur=.6)}"></div><div class="fin">'
             f'<div class="disp" style="position:absolute;left:0;right:0;top:300px;text-align:center;font-size:92px">{words("Генерация. Адаптация. Запуск.", 38.8, 40.2, step=.25, accent=(0, 2))}</div>'
             + logo(40.3, 'left:50%;top:410px;transform:translateX(-50%)')
             + f'<div style="position:absolute;left:0;right:0;top:620px;text-align:center;font:500 34px var(--f-body)"><span {an(40.8, i="fu")}>oneflow.art</span></div>'
             f'<p class="fnote an" style="{st(41.0, i="fi")}">{FOOT}</p></div>')
    js = """
const CAM = %s;
let W, C1, C2, ZM, P = {};
const pos = (el) => { let x = el.offsetWidth / 2, y = el.offsetHeight / 2; while (el && el.id !== 'world') { x += el.offsetLeft; y += el.offsetTop; el = el.offsetParent; } return [x, y]; };
window.FRAME = (t) => {
  if (!W) { W = document.getElementById('world'); C1 = document.getElementById('c1'); C2 = document.getElementById('c2'); ZM = document.getElementById('zm');
    const q = (s) => pos(document.querySelector(s));
    P.gen = q('#nw .btn.acc'); P.adapt = q('#tw .trw .btn:not(.ghost)'); P.run = q('#aw .stp.hint'); P.n1 = q('#aw .acv2 .nd:nth-of-type(1)'); P.n4 = q('#aw .acv2 .nd:nth-of-type(4)'); }
  const [cx, cy, z] = KEY(CAM, t);
  W.style.transform = `translate(${960 - cx * z}px, ${540 - cy * z}px) scale(${z})`;
  ZM.textContent = Math.round(z * 100) + '%%';
  const [x1, y1] = KEY([[9.3, 4300, 950], [10.5, ...P.gen], [11.3, ...P.gen], [13.0, 4200, 1500], [19.8, 900, 1600], [21.3, ...P.adapt], [22.4, ...P.adapt], [24.6, 800, 2900]], t);
  C1.style.transform = `translate(${x1 - 4}px, ${y1 - 2}px)`;
  const [x2, y2] = KEY([[33.4, 4500, 2700], [35.3, ...P.n1], [36.3, ...P.n4], [37.1, ...P.run], [42, ...P.run]], t);
  C2.style.transform = `translate(${x2 - 4}px, ${y2 - 2}px)`;
  C2.style.opacity = t > 33.2 ? 1 : 0;
  C1.style.opacity = t > 9.0 && t < 23.9 ? 1 : 0;
};
""" % (camera_keys(),)
    return page('ONEFLOW — Infinite Canvas', THEME, '\n'.join(b), T, js, wire_pal=dict(ink='#3d3d3a', acc='#0d99ff', bar='#e3e3de', bg='#f7f7f4', dot='#e1e1dc', fill='#fff', head='#3d3d3a', sw=2.6),
                grad_stops=('#7cc4ff', '#0d99ff', '#7b61ff'))


SHOTS = [0.4, 3.3, 4.9, 7.6, 11.0, 14.9, 18.4, 22.9, 27.5, 31.9, 36.9, 41.5]
