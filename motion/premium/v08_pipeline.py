"""08 · Pipeline — the AI assistant assembles a production line (seen from far away), you press «Запустить», and the camera
rides along the track with the product card through six stations: trends → generation → adaptation → texts →
predictor → launch; the card collects each result on the way. Light, calm, emerald accent."""
from lib import FOOT, adapted, an, formats, img, ln, logo, models, page, predictor, progress, st, texts, trends, words

NAME, TITLE = 'pipeline', 'Pipeline — конвейер со станциями, камера едет с товаром'
T = 39.0
THEME = """
:root { --bg: #fafaf9; --ink: #1c1917; --mut: #78716c; --panel: #fff; --panel2: #f5f5f4; --line: #e7e5e4; --dot: #e7e5e4; --acc: #059669;
  --grad: linear-gradient(90deg, #059669, #0891b2); --r: 16px; --sh: 0 40px 80px -40px rgba(28,25,23,.25); --f-disp: 'Inter Tight'; --f-body: 'IBM Plex Sans'; --f-mono: 'IBM Plex Mono';
  --w-disp: 600; --ls-disp: -.04em; --grain: .025; }
#wr { position: absolute; left: 0; top: 0; width: 12600px; height: 1080px; transform-origin: 0 0; }
.trk { position: absolute; left: 400px; right: 400px; top: 928px; height: 4px; border-radius: 2px; background: repeating-linear-gradient(90deg, var(--line) 0 26px, transparent 26px 40px); transform-origin: 0 50%; }
.stn { position: absolute; top: 0; width: 1900px; height: 1080px; }
.stn .t { position: absolute; left: 0; right: 0; top: 70px; text-align: center; font-size: 62px; }
.node { position: absolute; top: 890px; width: 80px; height: 80px; margin-left: -40px; border-radius: 50%; display: grid; place-items: center; background: var(--panel);
  box-shadow: 0 0 0 2px var(--acc), 0 10px 30px -10px rgba(5,150,105,.5); font: 600 28px var(--f-mono); color: var(--acc); }
.tok { position: absolute; left: 0; top: 0; z-index: 30; display: flex; align-items: center; gap: 14px; width: 380px; padding: 10px 18px 10px 10px; border-radius: 18px;
  background: var(--panel); box-shadow: 0 0 0 1px var(--line), 0 30px 60px -30px rgba(28,25,23,.45); }
.tok .im { width: 76px; height: 76px; border-radius: 12px; } .tok b { display: block; font: 600 20px var(--f-body); } .tok .tg { position: relative; height: 22px; font: 500 16px var(--f-mono); color: var(--acc); }
.tok .tg span { position: absolute; left: 0; top: 0; white-space: nowrap; }
.ctr { position: absolute; left: 0; right: 0; text-align: center; } .h1 { font-size: 128px; }
@keyframes pin { from { opacity: 0; transform: scale(.72); } to { opacity: 1; transform: none; } }
.ov { position: absolute; z-index: 5; top: 150px; width: 1560px; height: 640px; padding: 90px 110px; border-radius: 70px; background: var(--panel); box-shadow: 0 0 0 6px var(--line), 0 120px 200px -100px rgba(28,25,23,.35); }
.ov em { display: block; font: 600 130px var(--f-mono); color: var(--acc); font-style: normal; } .ov b { display: block; margin-top: 40px; font: 600 190px/1 var(--f-disp); letter-spacing: -.04em; }
.chans { position: absolute; left: 50%; top: 520px; display: flex; gap: 16px; transform: translateX(-50%); }
.launch { position: absolute; left: 50%; top: 330px; transform: translateX(-50%); font-size: 30px; padding: 26px 46px; border-radius: 20px; }
"""
X = [1500, 3500, 5500, 7500, 9500, 11500]
STOP = [(9.4, 13.2), (14.0, 16.6), (17.4, 20.4), (21.2, 24.6), (25.4, 28.6), (29.4, 32.4)]
TAGS = [(9.0, 'исходное фото'), (12.9, '+ тренд «неожиданный масштаб»'), (16.3, '+ сгенерировано · 30+ моделей'), (20.1, '+ 4 формата готовы'),
        (24.3, '+ SEO-описание .docx'), (28.3, 'прогноз 91/100 для Kaspi'), (31.6, 'запущено ✓')]


OVT = ('Тренды', 'Генерация', 'Адаптация', 'Тексты', 'Predictor', 'Запуск')


def stn(k, title, inner):
    ov = (f'<div class="ov" style="left:{X[k] - 780}px;animation:pi .55s var(--po) {5.7 + k * .28:.2f}s both, fob .4s var(--e) 8.75s forwards, '
          f'pin .55s var(--po) {32.9 + k * .08:.2f}s forwards"><em>{k + 1:02d}</em><b>{OVT[k]}</b></div>')
    return (f'<div class="stn" style="left:{X[k] - 950}px"><div class="t disp">{ln(title, STOP[k][0] - .3)}</div>{inner}</div>'
            f'<div class="node an" style="{st(5.6 + k * .25, i="pi", idur=.5)};left:{X[k] - 700}px">{k + 1:02d}</div>' + ov)


def build():
    s = [a for a, _ in STOP]
    b = ['<div id="wr" class="an" style="--d:4.9s;--in:fi;--id:.6s">']
    b.append(f'<div class="trk an" style="{st(5.4, i="grow", idur=1.8)}"></div>')
    b.append(stn(0, 'Автоматический анализ трендов.', trends(s[0] + .1, 'left:170px;top:190px;width:1060px;height:600px', click=s[0] + 1.6) + adapted(s[0] + 1.85, 'left:1270px;top:250px;width:520px')))
    b.append(stn(1, '<span class=g>30+</span> нейросетей', models(s[1] + .2, 'left:50%;top:300px;transform:translateX(-50%)')))
    b.append(stn(2, 'Адаптация под 4 формата', formats(s[2] + .2, 'left:50%;top:220px;transform:translateX(-50%)', step=.12) + progress(s[2] + .5, 1.4, 'left:300px;right:300px;top:740px')))
    b.append(stn(3, 'Тексты и документы <span class=g>за секунды.</span>', texts(s[3] + .1, 'left:400px;top:190px;width:1100px;height:560px')))
    b.append(stn(4, '<span class=g>Лучший креатив</span> — ещё до запуска рекламы.', predictor(s[4] + .1, 'left:50%;top:230px;transform:translateX(-50%)')))
    chans = ''.join(f'<span {an(s[5] + .9 + k * .1, i="pi", cls="pill")}>{c}</span>' for k, c in enumerate(('Kaspi', 'Instagram', 'TikTok', 'Яндекс РСЯ', 'Discovery')))
    b.append(stn(5, 'Генерация. Адаптация. <span class=g>Запуск.</span>', f'<span class="btn launch an" style="{st(s[5] + .2, i="pi", idur=.5)};animation:pi .5s var(--po) {s[5] + .2:.2f}s both, toacc .3s var(--e2) {s[5] + .8:.2f}s both">Запустить пайплайн ▸</span><div class="chans">{chans}</div>'))
    tags = ''.join(f'<span {an(a, TAGS[k + 1][0] if k + 1 < len(TAGS) else None, i="fu", out="uo", idur=.4, odur=.3)}>{txt}</span>' for k, (a, txt) in enumerate(TAGS))
    b.append(f'<div class="tok" id="tok">{img("bunny")}<div><b>Мягкий зайка</b><div class="tg">{tags}</div></div></div>')
    b.append('</div>')
    # screen-space: offer, assistant build, finale
    b.append(f'<div style="position:absolute;left:160px;top:260px" class="disp h1">{ln("Больше контента.", .3, 4.7)}<br>{ln("До <span class=g>50%</span> дешевле*", .8, 4.75)}</div>')
    b.append(f'<div class="cap" style="position:absolute;left:164px;top:600px;font-size:34px">{ln("Бюджет не сгорает в конце месяца.", 1.5, 4.8)}</div>')
    b.append(f'<div class="ctr disp" style="top:120px;font-size:72px">{ln("ИИ-ассистент собирает пайплайн <span class=g>за вас.</span>", 5.1, 8.5)}</div>')
    b.append(f'<div class="ctr" style="top:800px"><span {an(7.3, 8.6, i="fu", cls="pill")}>Проверьте и нажмите «Запустить»</span></div>')
    b.append(f'<div class="ctr" style="top:880px"><span class="btn an" style="animation:pi .5s var(--po) 7.5s both, toacc .25s var(--e2) 8.15s both, fob .4s var(--e) 8.6s forwards">Запустить ▸</span></div>')
    b.append(f'<div class="ctr disp" style="top:110px;font-size:70px">{words("Фото. Видео. Тексты. Баннеры.", 33.2, 35.3, step=.1, accent=(0, 2))}</div>'
             f'<div class="ctr disp" style="top:200px;font-size:44px"><span class="mut">{ln("Всё в одном окне.", 33.6, 35.3)}</span></div>')
    b.append(logo(35.8, 'left:50%;top:410px;transform:translateX(-50%)'))
    b.append(f'<div class="ctr" style="top:630px;font:500 34px var(--f-body)"><span {an(36.3, i="fu")}>oneflow.art</span></div>')
    b.append(f'<p class="fnote an" style="{st(36.5, i="fi")}">{FOOT}</p>')
    cam = [[5.0, 6300, 560, .148], [8.6, 6300, 560, .148], [9.4, X[0], 560, 1]]
    for (a0, l0), (a1, _), x0, x1 in zip(STOP, STOP[1:], X, X[1:]):
        cam += [[l0, x0, 560, 1], [a1, x1, 560, 1]]
    cam += [[32.4, X[5], 560, 1], [33.4, 6300, 700, .148], [35.3, 6300, 700, .148], [35.9, 6300, 700, .12]]
    js = """
const CAM = %s;
let WR, TK;
window.FRAME = (t) => {
  if (!WR) { WR = document.getElementById('wr'); TK = document.getElementById('tok'); }
  const [cx, cy, z] = KEY(CAM, t);
  WR.style.transform = `translate(${960 - cx * z}px, ${540 - cy * z}px) scale(${z})`;
  WR.style.opacity = t > 35.4 ? Math.max(0, 1 - (t - 35.4) / .5) : '';
  TK.style.transform = `translate(${cx - 190}px, 870px)`; TK.style.opacity = t > 8.9 && t < 32.9 ? 1 : 0;
};
""" % (cam,)
    return page('ONEFLOW — Pipeline', THEME, '\n'.join(b), T, js, wire_pal=dict(ink='#44403c', acc='#059669', bar='#e7e5e4', bg='#f5f5f4', dot='#e7e5e4', fill='#fff', head='#44403c', sw=2.6),
                grad_stops=('#6ee7b7', '#10b981', '#0891b2'))


SHOTS = [2.2, 6.4, 8.2, 11.8, 13.6, 15.9, 19.4, 23.9, 27.9, 31.4, 34.4, 38.0]
