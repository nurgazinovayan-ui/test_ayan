"""01 · Keynote — kinetic type on black. One statement per shot, lines rise out of masks, hard cuts; the product shows as a
single floating window that tilts up into place with a light sweep and a slow push-in."""
from lib import FOOT, adapted, an, assistant, formats, ln, logo, models, nodes, page, predictor, progress, st, texts, trends, words

NAME, TITLE = 'keynote', 'Keynote — кинетическая типографика на чёрном'
T = 42.0
THEME = """
:root { --bg: #000; --ink: #f5f5f7; --mut: #86868b; --panel: #111113; --panel2: #1c1c1f; --line: rgba(255,255,255,.1); --dot: rgba(255,255,255,.08);
  --acc: #2997ff; --grad: linear-gradient(90deg, #2997ff, #a78bfa 60%, #f472b6); --r: 22px; --sh: 0 80px 160px -60px rgba(41,151,255,.25), 0 40px 80px -40px rgba(0,0,0,.9);
  --f-disp: 'Inter Tight'; --f-body: 'Inter'; --f-mono: 'JetBrains Mono'; --w-disp: 600; --grain: .06; }
.ctr { position: absolute; left: 0; right: 0; text-align: center; }
.h1 { font-size: 150px; } .h2 { font-size: 104px; } .h3 { font-size: 76px; }
.big { font-size: 330px; letter-spacing: -.06em; line-height: .9; }
.shot { position: absolute; left: 50%; top: 250px; animation: rise 1.1s var(--e2) var(--d) both, push 4s linear var(--d) both, zb .45s var(--e) var(--o) forwards; }
.shot::after { content: ''; position: absolute; inset: 0; border-radius: var(--r); pointer-events: none; background: linear-gradient(105deg, transparent 40%, rgba(255,255,255,.1) 50%, transparent 60%) no-repeat;
  background-size: 250% 100%; animation: sweep 1.6s var(--e2) calc(var(--d) + .4s) both; } @keyframes sweep { from { background-position: 130% 0; } to { background-position: -30% 0; } }
.chips { display: flex; justify-content: center; gap: 14px; }
"""


def headline_top(lines, d, o):
    return '<div class="ctr disp h3" style="top:80px">' + '<br>'.join(ln(x, d + k * .12, o) for k, x in enumerate(lines)) + '</div>'


def build():
    b = []
    # 1 · offer
    b.append(f'<div class="ctr disp h1" style="top:440px">{ln("Больше контента.", .25, 2.75)}</div>')
    b.append(f'<div class="ctr" style="top:130px"><div {an(2.95, 5.75, i="fu", out="fob", cls="disp h3 mut")}>До</div>'
             f'<div class="disp big" style="animation:push 3s linear 2.95s both"><span class="ln"><span {an(3.0, 5.75, i="lu", out="lo", idur=.9)}>'
             f'<span class="g" data-count="3.05,1.0,0,50,0" data-suf="%">0%</span></span></span></div>'
             f'<div class="disp h2" style="margin-top:10px">{ln("дешевле*", 3.35, 5.75)}</div></div>')
    b.append(f'<div class="ctr disp h2" style="top:380px">{ln("Бюджет не сгорает", 6.0, 8.75)}<br><span class="mut">{ln("в конце месяца.", 6.15, 8.75)}</span></div>')
    # 2 · all in one — rapid word swap, then the line
    for k, w in enumerate(('Фото.', 'Видео.', 'Тексты.', 'Баннеры.')):
        d = 8.95 + k * .5
        b.append(f'<div class="ctr disp h1" style="top:440px">{ln(f"<span class={chr(34)}g{chr(34)}>{w}</span>" if k % 2 == 0 else w, d, d + .42, idur=.4)}</div>')
    b.append(f'<div class="ctr disp h1" style="top:440px">{ln("Всё в одном окне.", 11.05, 12.9)}</div>')
    # 3 · adaptation: floating window, then formats + progress
    b.append(f'<div class="ctr cap" style="top:1000px"><span {an(13.5, 15.4, i="fu")}>Адаптация под 4 формата</span></div>')
    b.append(nodes(13.2, style=f'width:1240px;height:700px;margin-left:-620px;--d:13.0s;--o:15.45s', cls='shot'))
    b.append(formats(15.55, 'left:50%;top:250px;transform:translateX(-50%)', step=.12, o=17.55))
    b.append(progress(15.8, 1.4, 'left:260px;right:260px;top:760px', o=17.55))
    # 4 · models
    b.append(f'<div class="ctr" style="top:120px"><div class="disp big"><span class="ln"><span {an(17.75, 20.45, i="lu", out="lo")}><span class="g">30+</span></span></span></div>'
             f'<div class="disp h2">{ln("нейросетей", 17.95, 20.45)}</div></div>')
    b.append(models(18.4, 'left:50%;top:660px;transform:translateX(-50%)', o=20.4))
    # 5 · trends
    b.append(headline_top(['Автоматический анализ трендов.'], 20.6, 22.45))
    b.append(headline_top(['Адаптируйте их под себя <span class="g">автоматически.</span>'], 22.55, 24.5))
    b.append(trends(20.8, style='left:170px;top:280px;width:1060px;height:560px;--d:20.7s;--o:24.5s', click=22.2, cls='shot', attrs=''))
    b.append(f'<div class="an" style="{st(None, 24.5, out="fob")};position:absolute;inset:0">{adapted(22.4, "left:1270px;top:380px;width:500px")}</div>')
    # 6 · texts
    b.append(headline_top(['Тексты и документы <span class="g">за секунды.</span>'], 24.75, 28.6))
    b.append(f'<div class="ctr cap" style="top:196px"><span {an(25.0, 28.6, i="fu")}>Описания, посты, контент-планы — сразу в Word, Excel и PowerPoint</span></div>')
    b.append(texts(25.2, style='width:1100px;height:560px;margin-left:-550px;top:300px;--d:25.0s;--o:28.6s', cls='shot'))
    # 7 · predictor
    b.append(f'<div class="ctr" style="top:70px"><span {an(28.8, 32.6, i="pi", cls="pill acc")}>Creative Predictor</span></div>')
    b.append(headline_top(['<span class="g">Лучший креатив</span> — ещё до запуска рекламы.'], 28.9, 32.6).replace('top:80px', 'top:140px'))
    b.append(f'<div class="an" style="{st(None, 32.6, out="fob")};position:absolute;inset:0">{predictor(29.2, "left:50%;top:330px;transform:translateX(-50%)")}</div>')
    # 8 · assistant
    b.append(headline_top(['ИИ-ассистент собирает пайплайн <span class="g">за вас.</span>'], 32.8, 37.0))
    b.append(assistant(33.1, style='width:1500px;height:700px;margin-left:-750px;top:240px;--d:32.9s;--o:37.0s', cls='shot'))
    # 9 · finale
    b.append(f'<div class="ctr disp h2" style="top:420px">{words("Генерация. Адаптация. Запуск.", 37.2, 38.9, step=.3, accent=(0, 2))}</div>')
    b.append(logo(39.1, 'left:50%;top:400px;transform:translateX(-50%)'))
    b.append(f'<div class="ctr" style="top:620px;font:500 34px var(--f-body)"><span {an(39.6, i="fu")}>oneflow.art</span></div>')
    b.append(f'<p class="fnote an" style="{st(39.9, i="fi")}">{FOOT}</p>')
    return page('ONEFLOW — Keynote', THEME, '\n'.join(b), T, wire_pal=dict(ink='#b9c3d6', acc='#2997ff', bar='#2a2d35', bg='#16171b', dot='#24262c', fill='#16171b', head='#b9c3d6', sw=2.6),
                grad_stops=('#7cc4ff', '#2997ff', '#a78bfa'))


SHOTS = [1.5, 4.4, 7.6, 11.9, 14.6, 16.9, 19.3, 23.8, 27.6, 31.9, 36.2, 40.5]
