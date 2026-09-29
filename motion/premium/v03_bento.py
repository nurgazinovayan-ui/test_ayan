"""03 · Bento — dark, Linear-like. The offer, then a bento grid assembles; each tile in turn morphs to full screen (its
cover cross-fades into the live feature), plays, and folds back into the grid; the grid collapses into the logo."""
from lib import FOOT, adapted, an, assistant, formats, img, ln, logo, models, nodes, page, predictor, progress, st, texts, trends, words

NAME, TITLE = 'bento', 'Bento — сетка плиток, каждая раскрывается на весь экран'
T = 42.0
THEME = """
:root { --bg: #08090a; --ink: #f7f8f8; --mut: #8a8f98; --panel: #0f1011; --panel2: #18191c; --line: #222328; --dot: #1d1e22; --acc: #7c86ff;
  --grad: linear-gradient(90deg, #7c86ff, #c3c8ff); --r: 16px; --sh: 0 40px 80px -40px rgba(0,0,0,.9); --f-disp: 'Inter Tight'; --f-body: 'Inter'; --f-mono: 'JetBrains Mono';
  --w-disp: 600; --ls-disp: -.04em; --grain: .05; }
.beam { position: absolute; left: 50%; top: -420px; width: 1800px; height: 900px; margin-left: -900px; border-radius: 50%;
  background: radial-gradient(ellipse at center, rgba(124,134,255,.28), rgba(124,134,255,.06) 45%, transparent 70%); }
.lg2 { background: linear-gradient(180deg, #fff 30%, #7d828b); -webkit-background-clip: text; background-clip: text; color: transparent; }
.ctr { position: absolute; left: 0; right: 0; text-align: center; }
.cell { position: absolute; overflow: hidden; border-radius: 18px; background: var(--panel); box-shadow: inset 0 0 0 1px var(--line); }
.cell::before { content: ''; position: absolute; inset: 0; background: radial-gradient(ellipse 60% 70% at 0% 0%, rgba(124,134,255,.12), transparent 70%); pointer-events: none; }
.mini { position: absolute; inset: 0; padding: 26px 30px; } .mini .lbl { display: block; margin-bottom: 14px; }
.mini .big { font: 600 110px/1 var(--f-disp); letter-spacing: -.05em; } .mini .t { font: 600 34px var(--f-disp); letter-spacing: -.03em; } .mini .s { font: 400 19px var(--f-body); color: var(--mut); margin-top: 8px; }
.full { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; }
.hl { position: absolute; left: 0; right: 0; top: 70px; text-align: center; font-size: 66px; }
.row3 { display: flex; gap: 10px; margin-top: 18px; } .row3 .im { border-radius: 8px; }
.ml { display: block; height: 10px; margin-top: 12px; border-radius: 5px; background: var(--panel2); }
.ck2 { display: flex; align-items: center; gap: 10px; margin-top: 12px; font: 500 18px var(--f-body); } .ck2 i { display: grid; place-items: center; width: 22px; height: 22px; border-radius: 50%; background: var(--acc); color: #fff; font: 700 12px var(--f-body); font-style: normal; }
"""
CELLS = [  # key, x, y, w, h
    ('adapt', 80, 230, 1060, 470), ('models', 1160, 230, 680, 230), ('pred', 1160, 470, 680, 230),
    ('trends', 80, 720, 580, 310), ('texts', 680, 720, 560, 310), ('asst', 1260, 720, 580, 310)]
EXP = {'adapt': (8.8, 14.0), 'models': (14.6, 17.2), 'trends': (17.8, 22.2), 'texts': (22.8, 26.8), 'pred': (27.4, 31.1), 'asst': (31.7, 36.4)}


def cover(key):
    if key == 'adapt':
        th = ''.join(img(p, f'width:{w}px;height:{h}px') for p, w, h in (('bunny', 80, 142), ('coffee', 130, 130), ('airbuds', 200, 60), ('watch', 200, 105)))
        return f'<span class="lbl">01 · Адаптация</span><div class="t">Один товар — <span class="g">4 формата</span></div><div class="s">Stories · Пост · Kaspi · Discovery</div><div class="row3" style="align-items:flex-end;margin-top:40px">{th}</div>'
    if key == 'models':
        return '<span class="lbl">02 · Модели</span><div class="big g">30+</div><div class="s">нейросетей в одном окне</div>'
    if key == 'pred':
        return '<span class="lbl">05 · Creative Predictor</span><div class="big">91<span class="mut" style="font-size:44px">/100</span></div><div class="s">лучший креатив — ещё до запуска</div>'
    if key == 'trends':
        return '<span class="lbl">03 · Тренды</span><div class="t">Анализ трендов</div><i class="ml" style="width:90%"></i><i class="ml" style="width:70%"></i><i class="ml" style="width:80%"></i><div class="s" style="margin-top:22px">TikTok · Instagram · Threads</div>'
    if key == 'texts':
        return '<span class="lbl">04 · Тексты</span><div class="t">Тексты и документы</div><div class="s">DOCX · XLSX · PPTX</div><i class="ml" style="width:85%;margin-top:26px"></i><i class="ml" style="width:60%"></i>'
    return ('<span class="lbl">06 · ИИ-ассистент</span><div class="t">Пайплайн за вас</div>'
            + ''.join(f'<div class="ck2"><i>✓</i>{s}</div>' for s in ('Разобрал аудиторию и нишу', 'Подобрал шаблон и промпт', 'Собрал 4 ноды на холсте')))


def full(key, te, tc):
    a = te + .45
    H = lambda text, d, o=None: f'<div class="hl disp">{ln(text, d, o)}</div>'  # noqa: E731
    if key == 'adapt':
        return (H('Адаптация под 4 формата', a) + nodes(a + .2, 'left:340px;top:230px;width:1240px;height:700px;--d:{:.2f}s;--o:{:.2f}s'.format(a, 11.9), cls='an')
                + formats(12.0, 'left:50%;top:260px;transform:translateX(-50%)', step=.1) + progress(12.2, 1.3, 'left:300px;right:300px;top:800px'))
    if key == 'models':
        return (f'<div class="ctr disp" style="top:170px;font-size:260px">{ln("<span class=g>30+</span>", a)}</div><div class="ctr disp" style="top:470px;font-size:76px">{ln("нейросетей", a + .15)}</div>'
                + models(a + .5, 'left:50%;top:640px;transform:translateX(-50%)'))
    if key == 'trends':
        return (f'<div class="hl disp">{ln("Автоматический анализ трендов.", a, 19.9)}</div><div class="hl disp">{ln("Адаптируйте их под себя <span class=g>автоматически.</span>", 20.0)}</div>'
                + trends(a + .1, 'left:150px;top:230px;width:1060px;height:600px', click=19.7) + adapted(19.95, 'left:1250px;top:300px;width:520px'))
    if key == 'texts':
        return (f'<div class="hl disp">{ln("Тексты и документы <span class=g>за секунды.</span>", a)}</div>'
                f'<div class="ctr cap" style="top:170px">{ln("Описания, посты, контент-планы — сразу в Word, Excel и PowerPoint", a + .15)}</div>'
                + texts(a + .3, 'left:410px;top:270px;width:1100px;height:560px'))
    if key == 'pred':
        return (f'<div class="ctr" style="top:60px"><span {an(a, i="pi", cls="pill acc")}>Creative Predictor</span></div>'
                f'<div class="hl disp" style="top:130px">{ln("<span class=g>Лучший креатив</span> — ещё до запуска рекламы.", a + .1)}</div>'
                + predictor(a + .3, 'left:50%;top:310px;transform:translateX(-50%)'))
    return (f'<div class="hl disp">{ln("ИИ-ассистент собирает пайплайн <span class=g>за вас.</span>", a)}</div>'
            + assistant(a + .2, 'left:210px;top:220px;width:1500px;height:720px'))


def build():
    b = ['<div class="beam an" style="--in:fi;--id:1.4s"></div>']
    b.append(f'<div class="ctr" style="top:230px"><span {an(.2, 5.6, i="pi", out="uo", cls="pill")}><b style="width:8px;height:8px;border-radius:50%;background:var(--acc);display:inline-block"></b>ONEFLOW · AI-студия контента</span></div>')
    b.append(f'<div class="ctr disp" style="top:330px;font-size:140px">{ln("<span class=lg2>Больше контента.</span>", .4, 5.6)}<br>{ln("До <span class=g>50%</span> дешевле*", 1.0, 5.65)}</div>')
    b.append(f'<div class="ctr cap" style="top:700px;font-size:34px">{ln("Бюджет не сгорает в конце месяца.", 1.8, 5.7)}</div>')
    b.append(f'<div class="ctr disp" style="top:70px;font-size:70px">{ln("<span class=lg2>Всё в одном окне.</span>", 6.0, 8.5)}</div>')
    b.append(f'<div class="ctr cap" style="top:160px">{words("Фото. Видео. Тексты. Баннеры.", 6.2, 8.5, step=.1)}</div>')
    kf, cells = [], []
    order = sorted(EXP, key=lambda k: EXP[k][0])
    for i, (key, x, y, w, h) in enumerate(CELLS):
        te, tc = EXP[key]
        z = 10 + order.index(key)
        kf.append(f'@keyframes ex{i} {{ from {{ left:{x}px; top:{y}px; width:{w}px; height:{h}px; border-radius:18px; z-index:{z}; }} to {{ left:0; top:0; width:1920px; height:1080px; border-radius:0; z-index:{z}; }} }}'
                  f'@keyframes co{i} {{ from {{ left:0; top:0; width:1920px; height:1080px; border-radius:0; z-index:{z}; }} to {{ left:{x}px; top:{y}px; width:{w}px; height:{h}px; border-radius:18px; z-index:{z}; }} }}')
        anim = (f'pi .7s var(--po) {6.4 + i * .09:.2f}s both, ex{i} .75s var(--e) {te}s forwards, co{i} .6s var(--e) {tc}s forwards, zb .5s var(--e) {36.9 + i * .05:.2f}s forwards')
        cells.append(f'<div class="cell" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;animation:{anim}">'
                     f'<div class="mini" style="animation:fo .25s linear {te}s forwards, fi .35s linear {tc + .35:.2f}s forwards">{cover(key)}</div>'
                     f'<div class="full" style="animation:fi .35s linear {te + .35:.2f}s both, fo .25s linear {tc}s forwards">{full(key, te, tc)}</div></div>')
    b.append('<style>' + '\n'.join(kf) + '</style>')
    b += cells
    b.append(f'<div class="ctr disp" style="top:420px;font-size:100px">{words("Генерация. Адаптация. Запуск.", 37.4, 39.0, step=.28, accent=(0, 2))}</div>')
    b.append(logo(39.2, 'left:50%;top:400px;transform:translateX(-50%)'))
    b.append(f'<div class="ctr" style="top:620px;font:500 34px var(--f-body)"><span {an(39.7, i="fu")}>oneflow.art</span></div>')
    b.append(f'<p class="fnote an" style="{st(40.0, i="fi")}">{FOOT}</p>')
    return page('ONEFLOW — Bento', THEME, '\n'.join(b), T, wire_pal=dict(ink='#aab0ff', acc='#7c86ff', bar='#26283a', bg='#121320', dot='#20223a', fill='#121320', head='#aab0ff', sw=2.6),
                grad_stops=('#c3c8ff', '#7c86ff', '#5e6ad2'))


SHOTS = [1.6, 4.4, 7.6, 9.1, 10.9, 13.2, 16.3, 20.8, 25.9, 30.2, 35.5, 40.6]
