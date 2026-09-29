"""05 · Scroll Story — Stripe-like landing page that scrolls itself: skewed living mesh-gradient band, sticky nav, each
section snaps into view and plays; UI panels ride a parallax layer; the footer band carries the logo."""
from lib import FOOT, adapted, an, assistant, formats, img, ln, logo, mark, models, nodes, page, predictor, progress, st, texts, trends, words
from brand import wordmark  # noqa: E402  (lib puts motion/ on sys.path)

NAME, TITLE = 'scroll', 'Scroll Story — лендинг в стиле Stripe, параллакс'
T = 40.0
THEME = """
:root { --bg: #fff; --ink: #0a2540; --mut: #425466; --panel: #fff; --panel2: #f6f9fc; --line: #e3e8ee; --dot: #dfe6ee; --acc: #635bff;
  --grad: linear-gradient(90deg, #635bff, #00b4ff); --r: 12px; --sh: 0 50px 100px -20px rgba(50,50,93,.25), 0 30px 60px -30px rgba(0,0,0,.3);
  --f-disp: 'Inter Tight'; --f-body: 'Inter'; --f-mono: 'JetBrains Mono'; --w-disp: 600; --ls-disp: -.035em; --grain: .02; }
#page { position: absolute; left: 0; top: 0; width: 1920px; height: 9720px; }
.sec { position: absolute; left: 0; width: 1920px; height: 1080px; }
.band { position: absolute; left: -200px; right: -200px; height: 900px; transform: skewY(-9deg); transform-origin: 0 0; overflow: hidden;
  background: radial-gradient(40% 60% at 20% 30%, #7a73ff, transparent 70%), radial-gradient(35% 55% at 55% 20%, #ff5ab7, transparent 70%),
    radial-gradient(40% 60% at 85% 40%, #ffb86b, transparent 70%), radial-gradient(45% 70% at 60% 80%, #00d4ff, transparent 70%), #a960ee; background-size: 160% 160%; }
.nav { position: absolute; left: 0; right: 0; top: 0; z-index: 50; display: flex; align-items: center; gap: 40px; height: 90px; padding: 0 160px; font: 500 19px var(--f-body); color: var(--ink); }
.nav .mk { width: 38px; } .nav .mk + b { margin-left: -26px; } .nav b { font: 700 24px var(--f-disp); letter-spacing: -.03em; margin-right: 30px; } .nav .btn { margin-left: auto; border-radius: 99px; padding: 11px 22px; }
.nav.solid { background: rgba(255,255,255,.85); box-shadow: 0 1px 0 var(--line); -webkit-backdrop-filter: blur(12px); backdrop-filter: blur(12px); }
.col { position: absolute; left: 160px; width: 700px; } .h1 { font-size: 118px; } .h2 { font-size: 78px; } .h3 { font-size: 60px; }
.kick { font: 600 20px var(--f-body); color: var(--acc); margin-bottom: 22px; }
.cta { display: flex; gap: 16px; margin-top: 40px; } .cta .btn { border-radius: 99px; padding: 16px 28px; font-size: 19px; } .cta .lnk { padding: 16px 8px; font: 600 19px var(--f-body); color: var(--acc); }
.grid4 { position: absolute; left: 980px; top: 190px; display: grid; grid-template-columns: 1fr 1fr; gap: 26px; }
.g4 { width: 360px; padding: 12px; border-radius: 14px; background: #fff; box-shadow: var(--sh); } .g4 .im { height: 270px; border-radius: 8px; } .g4 b { display: block; margin: 12px 6px 2px; font: 600 22px var(--f-body); }
.ctr { position: absolute; left: 0; right: 0; text-align: center; }
"""
SEC = ['hero', 'all', 'adapt', 'models', 'trends', 'texts', 'pred', 'asst', 'foot']
STOPS = [(0, 0, 5.2), (1, 6.0, 8.8), (2, 9.6, 13.2), (3, 14.0, 16.6), (4, 17.4, 21.4), (5, 22.2, 25.6), (6, 26.4, 29.8), (7, 30.6, 34.4), (8, 35.2, 40.0)]


def sec(i, inner, extra=''):
    return f'<div class="sec" style="top:{i * 1080}px;{extra}">{inner}</div>'


def px(y, f, inner, style=''):
    return f'<div class="px" data-top="{y}" data-f="{f}" style="position:absolute;inset:0;{style}">{inner}</div>'


def build():
    a = {i: s for i, s, _ in STOPS}
    b = ['<div id="page">']
    b.append(sec(0, f'<div class="band" id="b1" style="top:-240px"></div>'
                    f'<div class="col" style="top:250px;width:960px"><div class="disp h1" style="font-size:106px">{ln("Больше контента.", .3)}<br>{ln("До <span class=g>50%</span> дешевле*", .8)}</div>'
                    f'<div class="cap" style="margin-top:34px;color:var(--mut)">{ln("Бюджет не сгорает в конце месяца.", 1.5)}</div>'
                    f'<div class="cta"><span {an(2.0, i="fu", cls="btn")}>oneflow.art</span><span {an(2.15, i="fu", cls="lnk")}>Тарифы от $0 ›</span></div></div>'
                    + px(0, .12, nodes(1.2, 'left:1000px;top:300px;width:1240px;height:700px;transform:perspective(2000px) rotateY(-14deg) scale(.72);transform-origin:0 0;--d:.9s', cls='an'))))
    tiles = ''.join(f'<div {an(a[1] + .3 + k * .12, i="fu")}><div class="g4">{img(p)}<b>{n}</b></div></div>' for k, (n, p) in enumerate((('Фото', 'bunny'), ('Видео', 'hoodie'), ('Тексты', 'body'), ('Баннеры', 'speaker'))))
    b.append(sec(1, f'<div class="col" style="top:330px"><div class="kick">{ln("Всё в одном окне", a[1])}</div><div class="disp h2">{words("Фото. Видео. Тексты. Баннеры.", a[1] + .1, step=.12, accent=(0, 2))}</div>'
                    f'<div class="cap" style="margin-top:28px">{ln("Одна подписка — все инструменты для контента.", a[1] + .5)}</div></div>' + px(1080, .1, f'<div class="grid4">{tiles}</div>')))
    b.append(sec(2, f'<div class="ctr"><div class="kick" style="margin-top:140px">{ln("Адаптация", a[2])}</div><div class="disp h2">{ln("Один товар — <span class=g>4 формата</span>", a[2] + .1)}</div></div>'
                    + px(2160, .08, formats(a[2] + .5, 'left:50%;top:400px;transform:translateX(-50%)', step=.12) + progress(a[2] + .8, 1.5, 'left:300px;right:300px;top:880px'))))
    b.append(sec(3, f'<div class="col" style="top:280px"><div class="kick">{ln("Модели", a[3])}</div><div class="disp" style="font-size:240px;line-height:.9">{ln("<span class=g>30+</span>", a[3] + .1)}</div>'
                    f'<div class="disp h2">{ln("нейросетей", a[3] + .25)}</div></div>' + px(3240, .12, models(a[3] + .4, 'left:880px;top:420px;transform:scale(.95);transform-origin:0 0'))))
    b.append(sec(4, f'<div class="col" style="top:300px;width:600px"><div class="kick">{ln("Тренды", a[4])}</div><div class="disp h3">{ln("Автоматический", a[4] + .1)}<br>{ln("анализ трендов.", a[4] + .2)}</div>'
                    f'<div class="cap" style="margin-top:30px">{ln("Адаптируйте их под себя", a[4] + 1.6)}<br>{ln("<span class=g>автоматически.</span>", a[4] + 1.7)}</div></div>'
                    + px(4320, .12, trends(a[4] + .3, 'left:820px;top:190px;width:1000px;height:600px', click=a[4] + 1.9) + adapted(a[4] + 2.2, 'left:1240px;top:640px;width:520px'))))
    b.append(sec(5, f'<div class="col" style="top:330px;width:600px"><div class="kick">{ln("Тексты", a[5])}</div><div class="disp h3">{ln("Тексты и документы", a[5] + .1)}<br>{ln("<span class=g>за секунды.</span>", a[5] + .2)}</div>'
                    f'<div class="cap" style="margin-top:30px">{ln("Описания, посты, контент-планы —", a[5] + .4)}<br>{ln("сразу в Word, Excel и PowerPoint.", a[5] + .5)}</div></div>'
                    + px(5400, .12, texts(a[5] + .3, 'left:800px;top:240px;width:980px;height:560px'))))
    b.append(sec(6, f'<div class="ctr" style="top:120px"><div class="kick">{ln("Creative Predictor", a[6])}</div><div class="disp h2">{ln("<span class=g>Лучший креатив</span> — ещё до запуска рекламы.", a[6] + .1)}</div></div>'
                    + px(6480, .1, predictor(a[6] + .4, 'left:50%;top:380px;transform:translateX(-50%)'))))
    b.append(sec(7, f'<div class="ctr" style="top:110px"><div class="kick">{ln("ИИ-ассистент", a[7])}</div><div class="disp h2">{ln("Собирает пайплайн <span class=g>за вас.</span>", a[7] + .1)}</div></div>'
                    + px(7560, .1, assistant(a[7] + .3, 'left:210px;top:330px;width:1500px;height:680px'))))
    b.append(sec(8, f'<div class="band" id="b2" style="top:260px;height:1100px"></div>'
                    f'<div class="ctr disp" style="top:200px;font-size:92px">{words("Генерация. Адаптация. Запуск.", a[8] + .2, step=.25)}</div>'
                    + logo(a[8] + 1.3, 'left:50%;top:450px;transform:translateX(-50%);color:#fff').replace('fill="url(#mg)"', 'fill="#fff"')
                    + f'<div class="ctr" style="top:680px;font:600 36px var(--f-body);color:#fff"><span {an(a[8] + 1.8, i="fu")}>oneflow.art</span></div>'
                    f'<p class="fnote an" style="{st(a[8] + 2.0, i="fi")};color:#fff">{FOOT}</p>'))
    b.append('</div>')
    b.append(f'<div class="nav" id="nav">{mark()}<b>{wordmark("wmb")}</b><span>Возможности</span><span>Тарифы</span><span>Архив</span><span class="btn">oneflow.art</span></div>')
    keys = [[0, 0]]
    for (i0, _, l0), (i1, a1, _) in zip(STOPS, STOPS[1:]):
        keys += [[l0, i0 * 1080], [a1, i1 * 1080]]
    js = """
const SCR = %s;
let PG, PX, NAV, B1, B2;
window.FRAME = (t) => {
  if (!PG) { PG = document.getElementById('page'); PX = [...document.querySelectorAll('.px')]; NAV = document.getElementById('nav'); B1 = document.getElementById('b1'); B2 = document.getElementById('b2'); }
  const y = KEY(SCR, t)[0];
  PG.style.transform = `translateY(${-y}px)`;
  PX.forEach((el) => { el.style.translate = `0 ${(+el.dataset.top - y) * +el.dataset.f}px`; });
  NAV.classList.toggle('solid', y > 300 && y < 8400);
  const bp = `${50 + 30 * Math.sin(t * .35)}%% ${50 + 30 * Math.cos(t * .27)}%%`; B1.style.backgroundPosition = bp; B2.style.backgroundPosition = bp;
};
""" % (keys,)
    return page('ONEFLOW — Scroll Story', THEME, '\n'.join(b), T, js, wire_pal=dict(ink='#0a2540', acc='#635bff', bar='#dfe6ee', bg=None, dot='#e3e8ee', fill='#fff', head='#0a2540', sw=2.6),
                grad_stops=('#80e9ff', '#635bff', '#7a73ff'))


SHOTS = [2.6, 5.6, 7.9, 11.6, 15.6, 18.6, 20.9, 24.9, 29.4, 33.9, 36.6, 39.4]
