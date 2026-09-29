"""09 · Card Deck — Apple-style stack of full-frame cards, each in its own colour; the front card is swiped away (up,
left, right) with a spring and the next one rises from the stack behind it. One idea per card."""
from lib import FOOT, adapted, an, assistant, formats, img, ln, logo, models, nodes, page, predictor, progress, st, texts, trends, words

NAME, TITLE = 'deck', 'Card Deck — стопка цветных карточек, свайпы'
T = 39.0
THEME = """
:root { --bg: #e6e6eb; --ink: #111114; --mut: #6e6e76; --panel: #fff; --panel2: #f3f3f6; --line: #e3e3e8; --dot: #e1e1e6; --acc: #0071e3;
  --grad: linear-gradient(90deg, #0071e3, #7c3aed); --r: 18px; --sh: 0 30px 60px -30px rgba(0,0,0,.25); --f-disp: 'Inter Tight'; --f-body: 'Inter'; --f-mono: 'JetBrains Mono';
  --w-disp: 600; --ls-disp: -.045em; --grain: .03; }
.card { position: absolute; left: 80px; top: 60px; width: 1760px; height: 960px; overflow: hidden; border-radius: 48px; background: var(--bg); color: var(--ink);
  box-shadow: 0 50px 100px -50px rgba(0,0,0,.45); transform-origin: 50% 100%; }
.card .shade { position: absolute; inset: 0; z-index: 99; background: #000; pointer-events: none; }
.card .in { position: absolute; left: -80px; top: -60px; width: 1920px; height: 1080px; }
.dark { --bg: #0b0b0f; --ink: #f5f5f7; --mut: #8e8e96; --panel: #151519; --panel2: #1f1f25; --line: rgba(255,255,255,.1); --dot: rgba(255,255,255,.07); --on-ink: #0b0b0f; --acc: #2997ff; --grad: linear-gradient(90deg, #2997ff, #a78bfa); }
.ctr { position: absolute; left: 0; right: 0; text-align: center; } .h1 { font-size: 136px; } .h2 { font-size: 88px; } .h3 { font-size: 62px; }
.lft { position: absolute; left: 190px; }
.tiles { position: absolute; left: 50%; top: 440px; display: flex; gap: 26px; transform: translateX(-50%); }
.tl { width: 330px; padding: 12px; border-radius: 22px; background: var(--panel2); } .tl .im { height: 330px; border-radius: 14px; } .tl b { display: block; margin: 12px 6px 2px; font: 600 24px var(--f-body); }
"""
S = [0, 3.9, 7.6, 11.6, 14.9, 18.0, 22.4, 26.3, 30.0, 34.6]
DIRS = ['up', 'left', 'up', 'right', 'up', 'left', 'up', 'right', 'up']
CARDS = [('dark', ''), ('', '--bg:#ffffff'), ('', '--bg:linear-gradient(140deg,#3a66ff,#1c2fb0);--ink:#fff;--mut:rgba(255,255,255,.75);--grad:linear-gradient(90deg,#fff,#c7d2ff)'),
         ('', '--bg:#f3ece2;--panel2:#ebe2d4;--acc:#b4531f;--grad:linear-gradient(90deg,#d9622b,#b4531f)'), ('dark', ''), ('', '--bg:#ffffff'),
         ('', '--bg:linear-gradient(140deg,#11857a,#0b4f4a);--ink:#fff;--mut:rgba(255,255,255,.75);--grad:linear-gradient(90deg,#fff,#b8f5ea)'),
         ('', '--bg:#efeafd;--acc:#6d28d9;--grad:linear-gradient(90deg,#7c3aed,#db2777)'), ('dark', '--bg:#0b1020;--panel:#121a30;--panel2:#1a2340'), ('', '--bg:#ffffff')]


def card(k, inner):
    cls, style = CARDS[k]
    return f'<div class="card {cls}" style="{style}"><div class="in">{inner}</div><div class="shade"></div></div>'


def build():
    s = S
    c = []
    c.append(f'<div class="lft disp h1" style="top:250px">{ln("Больше контента.", .3)}<br>{ln("До <span class=g>50%</span> дешевле*", .8)}</div>'
             f'<div class="lft cap" style="top:620px;font-size:36px">{ln("Бюджет не сгорает в конце месяца.", 1.5)}</div>')
    tiles = ''.join(f'<div {an(s[1] + .5 + k * .12, i="pi")}><div class="tl">{img(p)}<b>{n}</b></div></div>' for k, (n, p) in enumerate((('Фото', 'bunny'), ('Видео', 'hoodie'), ('Тексты', 'body'), ('Баннеры', 'speaker'))))
    c.append(f'<div class="ctr disp h2" style="top:150px">{words("Фото. Видео. Тексты. Баннеры.", s[1] + .1, step=.1, accent=(0, 2))}</div>'
             f'<div class="ctr disp h3" style="top:270px"><span class="mut">{ln("Всё в одном окне.", s[1] + .4)}</span></div><div class="tiles">{tiles}</div>')
    c.append(f'<div class="ctr disp h3" style="top:130px">{ln("Адаптация под <span class=g>4 формата</span>", s[2] + .2)}</div>'
             + nodes(s[2] + .4, 'left:340px;top:250px;width:1240px;height:700px;--panel:#fff;--panel2:#f3f4f9;--ink:#111;--mut:#777;--line:#e3e5ee;--acc:#3a66ff;--grad:linear-gradient(90deg,#3a66ff,#7c3aed)'))
    c.append(f'<div class="ctr disp h3" style="top:130px">{ln("Один товар — все форматы.", s[3] + .2)}</div>' + formats(s[3] + .4, 'left:50%;top:270px;transform:translateX(-50%)', step=.12)
             + progress(s[3] + .7, 1.4, 'left:340px;right:340px;top:800px'))
    c.append(f'<div class="ctr disp" style="top:140px;font-size:280px;line-height:1">{ln("<span class=g>30+</span>", s[4] + .2)}</div><div class="ctr disp h2" style="top:450px">{ln("нейросетей", s[4] + .35)}</div>'
             + models(s[4] + .6, 'left:50%;top:640px;transform:translateX(-50%)'))
    c.append(f'<div class="ctr disp h3" style="top:120px">{ln("Автоматический анализ трендов.", s[5] + .2, s[5] + 2.2)}</div><div class="ctr disp h3" style="top:120px">{ln("Адаптируйте их под себя <span class=g>автоматически.</span>", s[5] + 2.3)}</div>'
             + trends(s[5] + .3, 'left:190px;top:250px;width:1000px;height:600px', click=s[5] + 2.0) + adapted(s[5] + 2.25, 'left:1230px;top:320px;width:500px'))
    c.append(f'<div class="ctr disp h3" style="top:120px">{ln("Тексты и документы <span class=g>за секунды.</span>", s[6] + .2)}</div>'
             f'<div class="ctr cap" style="top:210px">{ln("Описания, посты, контент-планы — сразу в Word, Excel и PowerPoint", s[6] + .35)}</div>'
             + texts(s[6] + .4, 'left:410px;top:300px;width:1100px;height:540px;--panel:#fff;--panel2:#eef7f5;--ink:#0b2e2b;--mut:#5b7d78;--line:#d9ebe7;--acc:#11857a;--grad:linear-gradient(90deg,#11857a,#0b4f4a)'))
    c.append(f'<div class="ctr" style="top:110px"><span {an(s[7] + .2, i="pi", cls="pill acc")}>Creative Predictor</span></div>'
             f'<div class="ctr disp h3" style="top:180px">{ln("<span class=g>Лучший креатив</span> — ещё до запуска рекламы.", s[7] + .3)}</div>' + predictor(s[7] + .5, 'left:50%;top:340px;transform:translateX(-50%)'))
    c.append(f'<div class="ctr disp h3" style="top:120px">{ln("ИИ-ассистент собирает пайплайн <span class=g>за вас.</span>", s[8] + .2)}</div>' + assistant(s[8] + .4, 'left:210px;top:240px;width:1500px;height:700px'))
    c.append(f'<div class="ctr disp h2" style="top:230px">{words("Генерация. Адаптация. Запуск.", s[9] + .2, step=.25, accent=(0, 2))}</div>' + logo(s[9] + 1.2, 'left:50%;top:430px;transform:translateX(-50%)')
             + f'<div class="ctr" style="top:650px;font:500 34px var(--f-body)"><span {an(s[9] + 1.7, i="fu")}>oneflow.art</span></div><p class="fnote an" style="{st(s[9] + 1.9, i="fi")};bottom:90px">{FOOT}</p>')
    body = '\n'.join(card(k, x) for k, x in reversed(list(enumerate(c))))
    fk = [[0, 0]]
    for k in range(1, len(S)):
        fk += [[S[k] - .75, k - 1], [S[k], k]]
    js = """
const F = %s, DIR = %s;
let CS;
const spring = (x) => 1 - Math.pow(1 - x, 3);
window.FRAME = (t) => {
  if (!CS) CS = [...document.querySelectorAll('.card')].reverse();
  const f = KEY(F, t, (x) => x);
  CS.forEach((el, i) => {
    const d = i - f, sh = el.lastChild;
    if (d > 3.2 || d < -1) { el.style.visibility = 'hidden'; return; }
    el.style.visibility = 'visible';
    if (d >= 0) { const e = Math.min(d, 3); el.style.transform = `translateY(${-26 * e}px) scale(${1 - .045 * e})`; sh.style.opacity = Math.min(.45, e * .16); el.style.zIndex = 50 - i; }
    else { const u = spring(-d), dir = DIR[i];
      const tr = dir === 'up' ? `translateY(${-1250 * u}px) rotate(${-7 * u}deg)` : dir === 'left' ? `translateX(${-2150 * u}px) rotate(${-9 * u}deg)` : `translateX(${2150 * u}px) rotate(${9 * u}deg)`;
      el.style.transform = tr; sh.style.opacity = 0; el.style.zIndex = 60; }
  });
};
""" % (fk, DIRS + ['up'])
    return page('ONEFLOW — Card Deck', THEME, body, T, js, wire_pal=dict(ink='#3a3a42', acc='#0071e3', bar='#e3e3e8', bg=None, dot='#e6e6ec', fill='#fff', head='#3a3a42', sw=2.6),
                grad_stops=('#7cc4ff', '#0071e3', '#7c3aed'))


SHOTS = [2.2, 3.5, 5.6, 9.6, 13.3, 16.4, 21.1, 25.4, 28.9, 29.7, 33.8, 38.0]
