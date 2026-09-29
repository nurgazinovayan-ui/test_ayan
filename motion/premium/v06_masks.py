"""06 · Mask Reveals — every shot is a living mesh-gradient field in its own colours; the next shot is revealed through a
shape (iris from the point of action, diagonal slice, rising wipe, centre split, rounded window growing to full frame).
White type with italic serif accents, frosted-glass UI."""
from lib import FOOT, adapted, an, assistant, formats, img, ln, logo, models, nodes, page, predictor, progress, st, texts, trends, words

NAME, TITLE = 'masks', 'Mask Reveals — градиентные поля и маски-переходы'
T = 40.0
THEME = """
:root { --bg: #000; --ink: #fff; --mut: rgba(255,255,255,.72); --panel: rgba(255,255,255,.13); --panel2: rgba(255,255,255,.12); --line: rgba(255,255,255,.28);
  --dot: rgba(255,255,255,.14); --acc: #fff; --on-acc: #1b1030; --on-ink: #1b1030; --grad: linear-gradient(90deg, #fff, #fff); --r: 24px; --sh: 0 50px 100px -40px rgba(0,0,0,.45);
  --f-disp: 'Onest'; --f-body: 'Onest'; --f-mono: 'JetBrains Mono'; --w-disp: 600; --ls-disp: -.045em; --grain: .07; }
.g { font-family: 'Playfair Display'; font-style: italic; font-weight: 500; background: none; -webkit-text-fill-color: currentColor; color: inherit; letter-spacing: -.02em; }
.shot { position: absolute; inset: 0; background-size: 140% 140%; animation: var(--rv) .85s var(--e) var(--d) both, drift 12s linear var(--d) both; }
@keyframes drift { from { background-position: 0% 0%; } to { background-position: 100% 60%; } }
@keyframes iris { from { clip-path: circle(0% at var(--cx) var(--cy)); } to { clip-path: circle(150% at var(--cx) var(--cy)); } }
@keyframes diag { from { clip-path: polygon(0 0, 0 0, -40% 100%, -40% 100%); } to { clip-path: polygon(0 0, 140% 0, 100% 100%, -40% 100%); } }
@keyframes wipe { from { clip-path: inset(100% 0 0 0); } to { clip-path: inset(0 0 0 0); } }
@keyframes split { from { clip-path: inset(0 50% 0 50%); } to { clip-path: inset(0 0 0 0); } }
@keyframes grow { 0% { clip-path: inset(38% 36% 38% 36% round 48px); opacity: 0; } 1% { opacity: 1; } 100% { clip-path: inset(0 0 0 0 round 0); opacity: 1; } }
.win, .mo, .pc, .adc, .fc .im { -webkit-backdrop-filter: blur(18px) saturate(1.3); backdrop-filter: blur(18px) saturate(1.3); }
.ub { background: #fff; } .btn.acc, .pill.acc { background: #fff; color: #1b1030; }
.ctr { position: absolute; left: 0; right: 0; text-align: center; } .h1 { font-size: 150px; } .h2 { font-size: 84px; } .h3 { font-size: 64px; }
.tiles { position: absolute; left: 50%; top: 520px; display: flex; gap: 26px; transform: translateX(-50%); }
.tl { width: 300px; padding: 12px; border-radius: 20px; background: var(--panel); box-shadow: 0 0 0 1px var(--line); -webkit-backdrop-filter: blur(18px); backdrop-filter: blur(18px); }
.tl .im { height: 300px; border-radius: 12px; } .tl b { display: block; margin: 12px 6px 2px; font: 600 24px var(--f-body); }
"""
PAL = [('#1e0b4b', '#7c3aed', '#db2777', '#2563eb'), ('#4a0d2e', '#f43f5e', '#f97316', '#a21caf'), ('#062a3a', '#0891b2', '#10b981', '#2563eb'),
       ('#1f1147', '#6366f1', '#ec4899', '#06b6d4'), ('#0b1a4a', '#3b82f6', '#8b5cf6', '#22d3ee'), ('#3b0a2a', '#e11d48', '#7c3aed', '#fb923c'),
       ('#07213b', '#0ea5e9', '#6366f1', '#14b8a6'), ('#2a0f45', '#a855f7', '#f43f5e', '#f59e0b'), ('#062b2b', '#14b8a6', '#0ea5e9', '#84cc16'),
       ('#2b0b3f', '#d946ef', '#6366f1', '#f97316'), ('#0a1440', '#4f46e5', '#06b6d4', '#ec4899'), ('#050509', '#3b1c8c', '#0b3b5c', '#5b1030')]


def shot(k, d, reveal, inner, cx='50%', cy='50%'):
    base, c1, c2, c3 = PAL[k]
    bg = (f'radial-gradient(55% 75% at 18% 22%, {c1}, transparent 70%), radial-gradient(50% 70% at 82% 28%, {c2}, transparent 70%), '
          f'radial-gradient(70% 80% at 55% 105%, {c3}, transparent 70%), {base}')
    return f'<section class="shot" style="--d:{d}s;--rv:{reveal};--cx:{cx};--cy:{cy};background:{bg}">{inner}</section>'


CNT = '<span data-count="3.0,.9,0,50,0" data-suf="%">0%</span>'


def build():
    b = []
    b.append(shot(0, 0, 'fi', f'<div class="ctr disp h1" style="top:430px">{ln("Больше <span class=g>контента.</span>", .35)}</div>'))
    b.append(shot(1, 2.6, 'iris', f'<div class="ctr disp" style="top:120px;font-size:84px">{ln("До", 2.9)}</div><div class="ctr disp" style="top:200px;font-size:360px;line-height:1">'
                                   f'{ln(CNT, 2.95)}</div><div class="ctr disp h2" style="top:600px">{ln("<span class=g>дешевле*</span>", 3.3)}</div>'))
    b.append(shot(2, 5.2, 'diag', f'<div class="ctr disp h2" style="top:380px">{ln("Бюджет не сгорает", 5.5)}<br>{ln("<span class=g>в конце месяца.</span>", 5.65)}</div>'))
    tiles = ''.join(f'<div {an(8.1 + k * .3, i="pi")}><div class="tl">{img(p)}<b>{n}</b></div></div>' for k, (n, p) in enumerate((('Фото', 'bunny'), ('Видео', 'hoodie'), ('Тексты', 'body'), ('Баннеры', 'speaker'))))
    b.append(shot(3, 7.6, 'wipe', f'<div class="ctr disp h2" style="top:220px">{words("Фото. Видео. Тексты. Баннеры.", 8.0, step=.3, accent=(1, 3))}</div><div class="tiles">{tiles}</div>'))
    b.append(shot(4, 9.9, 'split', f'<div class="ctr disp h3" style="top:70px">{ln("Всё в <span class=g>одном окне.</span>", 10.2)}</div>'
                                    + nodes(10.4, 'left:340px;top:220px;width:1240px;height:700px;--d:10.2s', cls='an')))
    b.append(shot(5, 13.4, 'iris', f'<div class="ctr disp h3" style="top:80px">{ln("Адаптация под <span class=g>4 формата</span>", 13.7)}</div>'
                                   + formats(13.9, 'left:50%;top:250px;transform:translateX(-50%)', step=.12) + progress(14.2, 1.4, 'left:300px;right:300px;top:790px'), cx='50%', cy='44%'))
    b.append(shot(6, 16.4, 'grow', f'<div class="ctr disp" style="top:110px;font-size:260px;line-height:1">{ln("30+", 16.7)}</div><div class="ctr disp h2" style="top:400px">{ln("<span class=g>нейросетей</span>", 16.85)}</div>'
                                   + models(17.1, 'left:50%;top:600px;transform:translateX(-50%)')))
    b.append(shot(7, 19.3, 'diag', f'<div class="ctr disp h3" style="top:70px">{ln("Автоматический анализ трендов.", 19.6, 21.3)}</div>'
                                   f'<div class="ctr disp h3" style="top:70px">{ln("Адаптируйте их под себя <span class=g>автоматически.</span>", 21.4)}</div>'
                                   + trends(19.8, 'left:150px;top:220px;width:1060px;height:600px', click=21.2) + adapted(21.45, 'left:1250px;top:300px;width:520px')))
    b.append(shot(8, 23.5, 'wipe', f'<div class="ctr disp h3" style="top:70px">{ln("Тексты и документы <span class=g>за секунды.</span>", 23.8)}</div>'
                                   f'<div class="ctr cap" style="top:165px">{ln("Описания, посты, контент-планы — сразу в Word, Excel и PowerPoint", 24.0)}</div>'
                                   + texts(24.1, 'left:410px;top:260px;width:1100px;height:560px')))
    b.append(shot(9, 27.5, 'iris', f'<div class="ctr" style="top:60px"><span {an(27.8, i="pi", cls="pill acc")}>Creative Predictor</span></div>'
                                   f'<div class="ctr disp h3" style="top:130px">{ln("<span class=g>Лучший креатив</span> — ещё до запуска рекламы.", 27.9)}</div>'
                                   + predictor(28.1, 'left:50%;top:310px;transform:translateX(-50%)'), cx='50%', cy='60%'))
    b.append(shot(10, 31.3, 'split', f'<div class="ctr disp h3" style="top:70px">{ln("ИИ-ассистент собирает пайплайн <span class=g>за вас.</span>", 31.6)}</div>'
                                     + assistant(31.8, 'left:210px;top:210px;width:1500px;height:720px')))
    b.append(shot(11, 35.6, 'iris', f'<div class="ctr disp h2" style="top:250px">{words("Генерация. Адаптация. Запуск.", 35.9, step=.25, accent=(1,))}</div>'
                                    + logo(36.9, 'left:50%;top:470px;transform:translateX(-50%)')
                                    + f'<div class="ctr" style="top:690px;font:500 34px var(--f-body)"><span {an(37.4, i="fu")}>oneflow.art</span></div>'
                                    f'<p class="fnote an" style="{st(37.6, i="fi")}">{FOOT}</p>', cy='60%'))
    return page('ONEFLOW — Mask Reveals', THEME, '\n'.join(b), T, wire_pal=dict(ink='#ffffff', acc='#ffe3f3', bar='rgba(255,255,255,.35)', bg='rgba(255,255,255,.08)',
                                                                                 dot='rgba(255,255,255,.16)', fill='rgba(255,255,255,.1)', head='#ffffff', sw=2.6),
                grad_stops=('#ffffff', '#e9dcff', '#c7b8ff'))


SHOTS = [1.4, 3.0, 4.6, 5.6, 9.0, 12.3, 14.2, 18.4, 22.9, 26.9, 30.4, 38.6]
