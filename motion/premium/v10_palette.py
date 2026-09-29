"""10 · Command Palette — Raycast-like: the whole story is driven from a ⌘K palette. Commands are typed, ↵ is pressed
(key caps pop in the corner), the palette slides up and the result unfolds below it. Warm red glow on near-black."""
from lib import FOOT, adapted, an, assistant, formats, img, ln, logo, models, nodes, page, predictor, progress, st, texts, trends, words

NAME, TITLE = 'palette', 'Command Palette — всё из командной строки ⌘K'
T = 41.5
THEME = """
:root { --bg: radial-gradient(ellipse 60% 45% at 50% -5%, rgba(255,99,99,.28), transparent 70%), radial-gradient(ellipse 45% 40% at 85% 105%, rgba(255,159,67,.14), transparent 70%), #0b0b0d;
  --ink: #ededed; --mut: #8f8f95; --panel: #161619; --panel2: #222226; --line: rgba(255,255,255,.09); --dot: rgba(255,255,255,.06); --acc: #ff6363; --on-ink: #0b0b0d;
  --grad: linear-gradient(90deg, #ff6363, #ff9f43); --r: 16px; --sh: 0 50px 100px -40px rgba(0,0,0,.9); --f-disp: 'Golos Text'; --f-body: 'Golos Text'; --f-mono: 'JetBrains Mono';
  --w-disp: 600; --ls-disp: -.04em; --grain: .05; }
.pal { position: absolute; left: 50%; top: 320px; z-index: 50; width: 1000px; margin-left: -500px; border-radius: 18px; background: rgba(30,30,34,.94);
  box-shadow: 0 0 0 1px rgba(255,255,255,.1), 0 60px 120px -40px rgba(0,0,0,.9), 0 0 140px -30px rgba(255,99,99,.4); }
.pin { position: relative; display: flex; align-items: center; gap: 16px; height: 80px; padding: 0 26px; font: 400 27px var(--f-body); }
.pin .k { display: grid; place-items: center; width: 40px; height: 40px; border-radius: 10px; background: var(--grad); color: #0b0b0d; font: 700 18px var(--f-body); flex: none; }
.pin .cmd { position: absolute; left: 92px; top: 0; line-height: 80px; white-space: nowrap; } .pin .ph { color: var(--mut); }
.plist { position: absolute; left: 50%; top: 400px; z-index: 49; width: 1000px; margin-left: -500px; padding: 10px 0 0; border-radius: 0 0 18px 18px; background: rgba(30,30,34,.94);
  box-shadow: 0 0 0 1px rgba(255,255,255,.1); }
.plist .grp { padding: 8px 26px; font: 500 15px var(--f-mono); color: var(--mut); letter-spacing: .06em; text-transform: uppercase; }
.pr { position: relative; z-index: 1; display: flex; align-items: center; gap: 16px; height: 62px; padding: 0 26px; font: 500 22px var(--f-body); }
.pr .im { width: 40px; height: 40px; border-radius: 10px; } .pr kbd { margin-left: auto; font: 500 16px var(--f-mono); color: var(--mut); }
.sel { position: absolute; left: 10px; right: 10px; top: 0; height: 62px; border-radius: 12px; background: rgba(255,255,255,.07); box-shadow: inset 0 0 0 1px rgba(255,99,99,.35); }
.pft { display: flex; gap: 26px; margin-top: 10px; padding: 14px 26px; border-top: 1px solid var(--line); font: 500 15px var(--f-mono); color: var(--mut); }
.kc { position: absolute; right: 70px; bottom: 60px; z-index: 60; display: flex; gap: 10px; }
.kc span { display: grid; place-items: center; min-width: 64px; height: 64px; padding: 0 16px; border-radius: 14px; background: #1d1d21; box-shadow: inset 0 -3px 0 rgba(0,0,0,.6), 0 0 0 1px rgba(255,255,255,.12);
  font: 600 26px var(--f-body); color: var(--ink); }
.ctr { position: absolute; left: 0; right: 0; text-align: center; } .h1 { font-size: 136px; } .cap2 { font-size: 44px; }
"""
CMDS = [(9.0, 'адаптировать «мягкий зайка» под 4 формата'), (14.4, 'модели'), (17.2, 'тренды → адаптировать под мой товар'), (22.4, 'SEO-описание для Kaspi'),
        (27.1, 'creative predictor · Kaspi'), (31.4, 'ассистент: собери пайплайн'), (36.3, 'запуск')]
CPS = 38
OUT = [12.6, 17.0, 22.2, 26.9, 31.2, 36.2]  # nodes, models, trends, texts, predictor, assistant leave


def keycaps(t, keys, dur=.7):
    return f'<div {an(t, t + dur, i="pi", out="fob", idur=.3, odur=.25, cls="kc")}>' + ''.join(f'<span>{k}</span>' for k in keys) + '</div>'


def cap(text, d, o):
    return f'<div class="ctr disp cap2" style="top:175px">{ln(text, d, o)}</div>'


def build():
    b = []
    b.append(f'<div class="ctr disp h1" style="top:300px">{ln("Больше контента.", .3, 5.0)}<br>{ln("До <span class=g>50%</span> дешевле*", .8, 5.05)}</div>')
    b.append(f'<div class="ctr cap" style="top:660px;font-size:34px">{ln("Бюджет не сгорает в конце месяца.", 1.5, 5.1)}</div>')
    b.append(keycaps(5.2, ['⌘', 'K']))
    # palette input: placeholder, then each command typed in its own window
    cmds = ''
    for k, (d, txt) in enumerate(CMDS):
        o = CMDS[k + 1][0] - .05 if k + 1 < len(CMDS) else 37.3
        cmds += f'<span class="cmd an" style="{st(d, o, i="fi", out="fo", idur=.05, odur=.05)}"><span data-type="{d + .05:.2f},{CPS}" data-txt="{txt}"></span></span>'
    b.append(f'<div class="pal an" id="pal" style="{st(5.4, 37.3, i="pi", out="zb", idur=.6)}"><div class="pin"><span class="k">⌘</span>'
             f'<span class="cmd ph an" style="{st(5.4, 8.95, out="fo", odur=.05)}">Что создадим?</span>{cmds}</div></div>')
    rows = ''.join(f'<div class="pr">{img(p)}{n}<kbd>⌘{k + 1}</kbd></div>' for k, (n, p) in enumerate((('Фото', 'bunny'), ('Видео', 'hoodie'), ('Тексты', 'body'), ('Баннеры', 'speaker'))))
    b.append(f'<div class="plist an" style="{st(5.6, 8.8, i="fu", out="fob", idur=.5)}"><div class="grp">Всё в одном окне</div><i class="sel" id="sel"></i>{rows}'
             f'<div class="pft"><span>↵ Открыть</span><span>⌘K Команды</span><span style="margin-left:auto">ONEFLOW</span></div></div>')
    b.append(f'<div class="ctr disp" style="top:880px;font-size:54px">{words("Фото. Видео. Тексты. Баннеры.", 6.0, 8.8, step=.4, accent=(0, 2))}</div>')
    ends = [d + len(txt) / CPS + .25 for d, txt in CMDS]
    for e in ends:
        b.append(keycaps(e, ['↵']))
    r = [e + .3 for e in ends]
    b.append(cap('Адаптация под 4 формата', r[0], 14.2) + nodes(r[0] + .1, f'left:340px;top:250px;width:1240px;height:700px;--d:{r[0]:.2f}s;--o:{OUT[0]}s', cls='an'))
    b.append(formats(12.7, 'left:50%;top:290px;transform:translateX(-50%)', step=.1, o=14.2) + progress(12.9, 1.1, 'left:340px;right:340px;top:840px', o=14.2))
    b.append(f'<div class="ctr disp" style="top:250px;font-size:250px;line-height:1">{ln("<span class=g>30+</span>", r[1], OUT[1])}</div><div class="ctr disp" style="top:520px;font-size:72px">{ln("нейросетей", r[1] + .15, OUT[1])}</div>'
             + models(r[1] + .4, 'left:50%;top:690px;transform:translateX(-50%) scale(.9);transform-origin:50% 0', o=OUT[1]))
    b.append(cap('Автоматический анализ трендов.', r[2], r[2] + 1.8) + cap('Адаптируйте их под себя <span class=g>автоматически.</span>', r[2] + 1.9, OUT[2])
             + f'<div class="an" style="{st(r[2] - .1, OUT[2], i="bi", out="fob", idur=.6)};position:absolute;inset:0">' + trends(r[2] + .1, 'left:150px;top:290px;width:1060px;height:600px', click=r[2] + 1.6)
             + adapted(r[2] + 1.85, 'left:1250px;top:360px;width:520px') + '</div>')
    b.append(cap('Тексты и документы <span class=g>за секунды.</span>', r[3], OUT[3])
             + texts(r[3] + .1, f'left:410px;top:300px;width:1100px;height:560px;--d:{r[3]:.2f}s;--o:{OUT[3]}s', cls='an'))
    b.append(cap('<span class=g>Лучший креатив</span> — ещё до запуска рекламы.', r[4], OUT[4]) + predictor(r[4] + .1, 'left:50%;top:320px;transform:translateX(-50%)', o=OUT[4]))
    b.append(cap('ИИ-ассистент собирает пайплайн <span class=g>за вас.</span>', r[5], OUT[5])
             + assistant(r[5] + .1, f'left:210px;top:270px;width:1500px;height:720px;--d:{r[5]:.2f}s;--o:{OUT[5]}s', cls='an'))
    b.append(f'<div class="ctr disp" style="top:250px;font-size:92px">{words("Генерация. Адаптация. Запуск.", 37.5, step=.25, accent=(0, 2))}</div>')
    b.append(logo(38.5, 'left:50%;top:430px;transform:translateX(-50%)'))
    b.append(f'<div class="ctr" style="top:650px;font:500 34px var(--f-body)"><span {an(39.0, i="fu")}>oneflow.art</span></div>')
    b.append(f'<p class="fnote an" style="{st(39.2, i="fi")}">{FOOT}</p>')
    js = """
let PAL, SEL;
window.FRAME = (t) => {
  if (!PAL) { PAL = document.getElementById('pal'); SEL = document.getElementById('sel'); }
  PAL.style.top = KEY([[8.8, 320], [9.3, 60]], t)[0] + 'px';
  const i = KEY([[6.0, 0], [6.3, 0], [6.5, 1], [6.8, 1], [7.0, 2], [7.3, 2], [7.5, 3]], t)[0];
  SEL.style.transform = `translateY(${46 + i * 62}px)`;
};
"""
    return page('ONEFLOW — Command Palette', THEME, '\n'.join(b), T, js, wire_pal=dict(ink='#ffb3a8', acc='#ff6363', bar='#2c2c31', bg='#1a1a1e', dot='#26262b', fill='#1a1a1e', head='#ffb3a8', sw=2.6),
                grad_stops=('#ffc58f', '#ff8a5c', '#ff5c5c'))


SHOTS = [2.2, 5.5, 7.2, 10.2, 11.9, 13.6, 16.3, 21.4, 25.9, 30.6, 35.6, 40.3]
