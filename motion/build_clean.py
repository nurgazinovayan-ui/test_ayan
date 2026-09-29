"""ONEFLOW promo in the clean SaaS style of the reference (light, airy, one blue gradient, focus-pull words, 3D UI, cursor clicks).

49.8 s, 1920×1080. Offer first: «Больше контента → До 50% дешевле* → Остаток [+$112] не сгорает», click into the tile,
tilted app, 3D corridor of cards, ribbon → progress bar, «Готово» + confetti, formats carousel, archive + card zoom,
«30+ нейросетей» with flying model cards, auto trend analysis → «Адаптировать» click, «Тексты и документы», Creative Predictor
scores, AI assistant builds the node scheme → «Запустить пайплайн» click, brand mark flies off,
«Генерация. Адаптация. Запуск.», logo lockup + oneflow.art + footnote.

Same engine as oneflow-motion.html: every animation is a CSS animation on one absolute timeline; window.seek(t) scrubs it.
python3 build_clean.py  →  oneflow-clean.html     (render: node render.js clean)
"""
import math
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'landing'))
import v4_porcelain as v  # noqa: E402

MARK_D = re.search(r'd="([^"]+)"', v.MARK).group(1)
IMG = '../landing/assets/ol/'
PRODUCTS = ['bunny', 'coffee', 'airbuds', 'watch', 'speaker', 'blender', 'pajama', 'robot', 'hoodie', 'pyramid', 'airfryer', 'powerbank', 'toothbrush', 'body']
T = 49.8
AI_SHIFT = 11.3  # the assistant scene plays 11.3 s later (trends grew, «Тексты» and «Creative Predictor» were added before it)
SHIFT = 18.7  # scenes K–N (launch, brand mark, words, logo) play 18.7 s later: assistant scene + the scenes above
HJ, HP = (1100, 388), (1152, 911)  # cursor targets: «Адаптировать» (trends), «Оценить» (predictor)


def mark(cls='mk', fill='url(#bg1)'):
    return f'<svg class="{cls}" viewBox="0 0 76 52" aria-hidden="true"><path fill="{fill}" d="{MARK_D}"/></svg>'


HAND = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#fff" stroke="#0f1222" stroke-width="1.5" stroke-linejoin="round" stroke-linecap="round" '
        'd="M9 11V4.5a1.5 1.5 0 0 1 3 0V10m0-1.5a1.5 1.5 0 0 1 3 0V10m0-.5a1.5 1.5 0 0 1 3 0V11m0-.5a1.5 1.5 0 0 1 3 0V15a7 7 0 0 1-7 7h-1.2a6 6 0 0 1-4.6-2.2L3.6 15.4'
        'a1.6 1.6 0 0 1 2.4-2.1L9 16z"/></svg>')


def hand(x0, y0, x1, y1, d, c, o):
    """Cursor moving (x0,y0)→(x1,y1) from d, clicking at c, gone at o (seconds)."""
    return (f'<div class="hand" style="--x0:{x0}px;--y0:{y0}px;--x1:{x1}px;--y1:{y1}px;--d:{d}s;--o:{o}s"><i style="--c:{c}s">{HAND}</i></div>'
            f'<span class="rip" style="left:{x1 + 9}px;top:{y1 + 5}px;--c:{c}s"></span>')


def w(text, d, o, cls=''):
    return f'<span class="wi {cls}" style="--d:{d}s;--o:{o}s">{text}</span>'


def img(n, cls='', extra=''):
    return f'<i class="im {cls}" style="background-image:url({IMG}{n}.webp){extra}"></i>'


# ---------------------------------------------------------------- scene helpers
def corridor():
    rnd = random.Random(3)

    def tiles(count, vertical=False):
        out = ''
        for k in range(count):
            if rnd.random() < .55:
                out += f'<div class="tl">{img(PRODUCTS[k % len(PRODUCTS)])}</div>'
            else:
                bars = ''.join(f'<b style="width:{rnd.randint(40, 92)}%"></b>' for _ in range(rnd.randint(3, 5)))
                out += f'<div class="tl ui"><em></em>{bars}<u></u></div>'
        return out
    return (f'<div class="wall wl">{tiles(33)}</div><div class="wall wr">{tiles(33)}</div>'
            f'<div class="wall wt">{tiles(30, True)}</div><div class="wall wb">{tiles(30, True)}</div>')


def app_window():
    fm = ''.join(f'<div class="fm"><span>{n}</span><span>{a}</span><em>×</em><span>{b}</span></div>' for n, a, b in
                 (('Stories 9:16', 1080, 1920), ('Пост 1:1', 1080, 1080), ('Discovery', 1200, 628), ('Kaspi', 1125, 330)))
    tabs = ''.join(f'<span class="{"on" if i == 0 else ""}">{t}</span>' for i, t in enumerate(('Ноды и адаптация', 'Генерация', 'Copywrite', 'One Launch', 'Тренды', 'Стратегия')))
    outs = ''.join(f'<span class="ofr" style="width:{wd}px;height:{ht}px"><i></i></span>' for wd, ht in ((70, 124), (100, 100), (150, 78), (170, 50)))
    return (f'<div class="aw"><div class="atb">{mark("amk")}<b>ONEFLOW</b><div class="tabs">{tabs}</div><span class="bud">$0.00 / $50</span></div>'
            '<div class="acv"><svg class="aed" viewBox="0 0 1500 780"><path d="M420 380 C 480 380, 480 330, 540 330"/><path d="M960 330 C 1010 330, 1010 380, 1060 380"/></svg>'
            f'<div class="nd n1"><div class="h"><b>▣</b>Изображение</div>{img("bunny", "nim")}<small>мягкий-зайка.webp</small></div>'
            f'<div class="nd n2"><div class="h"><b style="background:#fff1e3;color:#d98a2b">⌗</b>Адаптация</div><span class="lb">ФОРМАТЫ</span>{fm}<div class="gob">✦ Сгенерировать</div></div>'
            f'<div class="nd n3"><div class="h"><b style="background:#efeaff;color:#6b4dff">▦</b>Результат</div><div class="outs">{outs}</div></div></div></div>')


def carousel():
    cards = [('bunny', 'Stories 9:16', '1080×1920'), ('coffee', 'Пост 1:1', '1080×1080'), ('airbuds', 'Kaspi', '1125×330'), ('watch', 'Discovery', '1200×628'),
             ('speaker', 'Яндекс РСЯ', '1080×450'), ('blender', 'Пост 4:5', '1080×1350'), ('pajama', 'GDN', '300×250')]
    return ''.join(f'<div class="cc">{img(p, "cim")}<div class="cm"><b>{t}</b><i class="dot" style="background:{c}"></i><small>{s} · готово</small></div><span class="dots">•••</span></div>'
                   for (p, t, s), c in zip(cards, ('#3b5cff', '#16a36a', '#ff7a45', '#8b5cf6', '#e5484d', '#0ea5a4', '#3b5cff')))


def archive():
    items = [('bunny', 'Мягкий зайка'), ('coffee', 'Кофемашина'), ('airbuds', 'Наушники X1'), ('watch', 'Часы Time X5'), ('speaker', 'Колонка Mini'), ('pajama', 'Пижама детская'),
             ('robot', 'Робот-пылесос'), ('blender', 'Блендер Pro')]
    grid = ''.join(f'<div class="ac">{img(p)}<b>{t}</b><small>4 формата · сегодня</small></div>' for p, t in items)
    side = ''.join(f'<span class="{"on" if t == "Архив" else ""}"><i></i>{t}</span>' for t in ('Холст', 'Генерация', 'One Launch', 'Тренды', 'Архив'))
    return (f'<div class="dash"><aside>{mark("amk")}<b>ONEFLOW</b>{side}</aside><main><div class="dh"><b>Архив проекта</b><span class="sr">Поиск…</span><span class="nw">+ Новый</span></div>'
            '<div class="dt"><span class="on">Все</span><span>Фото</span><span>Видео</span><span>Тексты</span></div>'
            f'<div class="ag">{grid}</div></main></div>')


def model_cards():
    cards = [('Nano Banana Pro', 'coffee', 150, 60, -8, -420, -300, -30), ('Veo 3.1', 'watch', 1400, 40, 11, 460, -320, 34),
             ('Kling', 'airbuds', 120, 650, 9, -460, 360, 28), ('Seedream', 'robot', 1420, 660, -7, 440, 360, -26)]
    out = ''
    for i, (name, p, x, y, r, fx, fy, fr) in enumerate(cards):
        out += (f'<div class="mc" style="left:{x}px;top:{y}px;--r:{r}deg;--fx:{fx}px;--fy:{fy}px;--fr:{fr}deg;--d:{18.05 + i * .09:.2f}s">'
                f'{img(p, "mim")}<div class="mm"><b>{name}</b><small>генерация · 4 сек</small></div></div>')
    return out


def trends():
    rows = [('pyramid', 'TikTok', 'Товар в неожиданном масштабе', '318K'), ('robot', 'Instagram', 'Один предмет — три сценария', '132K'),
            ('body', 'TikTok', 'Честный обзор вместо рекламы', '174K'), ('speaker', 'Instagram', 'Распаковка без лица', '78K')]
    out = ''.join(f'<div class="trw">{img(p)}<div><small>{pl}</small><b>{t}</b></div><em>{m}</em><span class="adb{"" if i == 0 else " ghost"}">✦ Адаптировать</span></div>'
                  for i, (p, pl, t, m) in enumerate(rows))
    steps = ''.join(f'<span class="ln2" style="--d:{d}s"><em>{a}</em>{b}</span>' for d, a, b in
                    ((22.1, '0–1 с', 'зайка крупно в ладони'), (22.3, '1–4 с', 'камера отъезжает: рядом огромная кровать'), (22.5, '4–7 с', 'название и цена на экране')))
    card = (f'<div class="adc"><span class="pill">✦ Адаптировано под ваш товар</span><div class="hd">{img("bunny")}<div><b>Мягкий зайка</b><small>по тренду «Товар в неожиданном масштабе»</small></div></div>{steps}</div>')
    return ('<div class="tp"><div class="th"><b>Тренды</b><span>Все площадки</span><span>За 7 дней</span></div>' + out + '</div>' + card)


def confetti():
    rnd = random.Random(11)
    cols = ['#3b5cff', '#6fb6ff', '#9ce8ff', '#ff9ad5', '#7c5cff', '#2bd9ff']
    out = ''
    for k in range(46):
        a = rnd.uniform(0, 6.283)
        dist = rnd.uniform(260, 820)
        x, y = math.cos(a) * dist * 1.25, math.sin(a) * dist * .75 - 120
        out += (f'<i class="cf" style="--x:{x:.0f}px;--y:{y:.0f}px;--r:{rnd.randint(-540, 540)}deg;--fall:{rnd.randint(160, 420)}px;--d:{12.55 + rnd.uniform(0, .12):.2f}s;'
                f'background:{rnd.choice(cols)};width:{rnd.randint(14, 34)}px;height:{rnd.randint(10, 22)}px"></i>')
    return out


HTML = r"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ONEFLOW — clean promo</title>
<link rel="stylesheet" href="../landing/fonts.css">
<style>
:root { --bg: #f6f6fa; --ink: #0f1222; --mut: #8a8fa8; --b1: #3b5cff; --b2: #6fb6ff; --e: cubic-bezier(.7,0,.2,1); --e2: cubic-bezier(.16,.84,.24,1); --po: cubic-bezier(.2,1.4,.35,1); }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: 100%; height: 100%; overflow: hidden; background: #000; }
#st { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; overflow: hidden; background: radial-gradient(ellipse 70% 60% at 50% 110%, #e9edff, transparent 70%), var(--bg); transform-origin: 0 0;
  font-family: 'Inter', sans-serif; color: var(--ink); -webkit-font-smoothing: antialiased; }
.bl { background: linear-gradient(90deg, #3b5cff, #5d8bff 55%, #6fb6ff); -webkit-background-clip: text; background-clip: text; color: transparent; }
.sc { position: absolute; inset: 0; }
.wi { display: inline-block; animation: wIn .6s var(--e2) var(--d) both, wOut .38s var(--e) var(--o) forwards; }
@keyframes wIn { from { opacity: 0; filter: blur(20px); transform: scale(1.2); } } @keyframes wOut { to { opacity: 0; filter: blur(18px); transform: scale(.94); } }
.row { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; gap: 28px; font: 400 96px/1.1 'Inter', sans-serif; letter-spacing: -.035em; }
.fin { animation: fin .45s linear var(--d) both; } @keyframes fin { from { opacity: 0; } } .fo { animation: fo .35s linear var(--o) forwards; } @keyframes fo { to { opacity: 0; } }
.im { display: block; background: #fff center / cover no-repeat; }
.mk { display: block; }
/* cursor */
.hand { position: absolute; left: 0; top: 0; z-index: 40; width: 64px; animation: hMove .7s var(--e) var(--d) both, fo .3s linear var(--o) forwards; filter: drop-shadow(0 8px 14px rgba(15,18,34,.25)); }
.hand i { display: block; transform-origin: 30% 20%; animation: hClk .24s ease-out var(--c) both; } .hand svg { display: block; width: 64px; }
@keyframes hMove { from { transform: translate(var(--x0), var(--y0)); opacity: 0; } 25% { opacity: 1; } to { transform: translate(var(--x1), var(--y1)); } } @keyframes hClk { 50% { scale: .82; } }
.rip { position: absolute; z-index: 39; width: 30px; height: 30px; margin: -15px 0 0 -15px; border-radius: 50%; border: 4px solid var(--b1); opacity: 0; animation: rip .6s ease-out var(--c) both; }
@keyframes rip { from { opacity: 0; transform: scale(.3); } 20% { opacity: .9; } to { opacity: 0; transform: scale(4.2); } }
/* A · offer words + tile */
.r3 .l { position: absolute; right: calc(50% + 118px); } .r3 .r { position: absolute; left: calc(50% + 118px); }
.tile { position: absolute; left: 50%; top: 50%; width: 170px; height: 170px; margin: -85px 0 0 -85px; animation: tIn .7s var(--po) 3.12s both, tPress .22s ease-out 4.02s both, tThru .45s cubic-bezier(.6,0,.9,.4) 4.22s forwards; }
@keyframes tIn { from { opacity: 0; transform: scale(.3) rotate(-24deg); filter: blur(12px); } } @keyframes tPress { 50% { scale: .9; } }
@keyframes tThru { to { transform: scale(11); opacity: 0; filter: blur(24px); } }
.tile .back { position: absolute; inset: 0; border-radius: 38px; background: linear-gradient(150deg, #8fbcff, #3b5cff 70%); box-shadow: 0 34px 60px -22px rgba(59,92,255,.7), inset 0 2px 0 rgba(255,255,255,.5); }
.tile .doc { position: absolute; left: 22px; right: 22px; top: -26px; height: 118px; padding: 16px 16px; border-radius: 16px; background: #fff; box-shadow: 0 10px 24px -10px rgba(15,18,34,.3); rotate: -5deg; }
.tile .doc b { display: block; font: 700 38px/1 'Inter', sans-serif; color: var(--b1); letter-spacing: -.03em; } .tile .doc small { display: block; margin-top: 8px; font: 500 15px 'Inter', sans-serif; color: var(--mut); }
.tile .front { position: absolute; left: 0; right: 0; bottom: 0; height: 104px; padding: 16px 18px; border-radius: 26px 26px 38px 38px; background: linear-gradient(160deg, rgba(143,188,255,.92), rgba(59,92,255,.96)); -webkit-backdrop-filter: blur(6px); backdrop-filter: blur(6px);
  box-shadow: inset 0 2px 0 rgba(255,255,255,.55); color: #fff; font: 600 20px 'Inter', sans-serif; }
.tile .front small { display: block; font: 400 14px 'Inter', sans-serif; opacity: .85; }
/* B · app window */
.sB { perspective: 1600px; } .aw { position: absolute; left: 210px; top: 110px; width: 1500px; height: 860px; border-radius: 30px; background: #fff; box-shadow: 0 0 0 2px #d6ddff, 0 60px 120px -40px rgba(59,92,255,.45); overflow: hidden;
  animation: awIn .9s var(--e2) 4.35s both, awOut .5s var(--e) 5.62s forwards; }
@keyframes awIn { from { opacity: 0; transform: rotateX(40deg) scale(1.6); filter: blur(24px); } to { transform: rotateX(16deg) rotateZ(-2.5deg); } }
@keyframes awOut { from { transform: rotateX(16deg) rotateZ(-2.5deg); } to { opacity: 0; transform: rotateX(72deg) scale(.55) translateY(-260px); filter: blur(14px); } }
.atb { display: flex; align-items: center; gap: 14px; height: 78px; padding: 0 28px; border-bottom: 1.5px solid #eceef6; } .atb .amk { width: 34px; } .atb > b { font: 700 22px 'Inter', sans-serif; }
.tabs { display: flex; gap: 6px; margin-left: 40px; padding: 5px; border-radius: 14px; background: #f3f4f9; } .tabs span { padding: 9px 16px; border-radius: 10px; font: 500 17px 'Inter', sans-serif; color: #6d7290; }
.tabs .on { background: #fff; color: var(--b1); box-shadow: 0 2px 8px rgba(59,92,255,.18); } .bud { margin-left: auto; font: 500 17px 'JetBrains Mono', monospace; color: var(--mut); }
.acv { position: relative; height: 782px; background: radial-gradient(#dde1ee 1.5px, transparent 2px) 0 0 / 28px 28px, #f3f4f9; } .aed { position: absolute; inset: 0; width: 100%; height: 100%; }
.aed path { fill: none; stroke: #9aa8ff; stroke-width: 3.5; } .nd { position: absolute; border-radius: 22px; background: #fff; font-family: 'Inter', sans-serif; }
.nd .h { display: flex; align-items: center; gap: 12px; padding: 16px 20px; border-bottom: 1.5px solid #eef0f7; font: 600 22px 'Inter', sans-serif; }
.nd .h b { display: grid; place-items: center; width: 34px; height: 34px; border-radius: 10px; background: #e8f3ff; color: #3b8bff; font-size: 18px; }
.n1 { left: 120px; top: 170px; width: 300px; padding-bottom: 16px; } .nim { height: 240px; margin: 16px 18px 10px; border-radius: 14px; background-position: center 25%; } .n1 small { margin-left: 20px; font: 400 16px 'JetBrains Mono', monospace; color: var(--mut); }
.n2 { left: 540px; top: 120px; width: 420px; padding-bottom: 20px; } .lb { display: block; margin: 16px 20px 4px; font: 600 14px 'Inter', sans-serif; letter-spacing: .12em; color: var(--mut); }
.fm { display: grid; grid-template-columns: 1fr 76px 16px 76px; gap: 6px; align-items: center; margin: 8px 20px 0; font: 500 18px 'Inter', sans-serif; }
.fm span { padding: 9px 12px; border-radius: 10px; background: #f4f5fa; box-shadow: inset 0 0 0 1px #e6e8f2; } .fm em { font-style: normal; color: var(--mut); text-align: center; }
.gob { margin: 18px 20px 0; padding: 16px; border-radius: 99px; background: linear-gradient(90deg, #3b5cff, #6fb6ff); color: #fff; text-align: center; font: 600 20px 'Inter', sans-serif; }
.n3 { left: 1060px; top: 190px; width: 330px; padding-bottom: 20px; } .outs { display: flex; flex-wrap: wrap; align-items: flex-end; gap: 12px; padding: 20px; }
.ofr { position: relative; overflow: hidden; border-radius: 8px; background: #fff; } .ofr::before { content: ''; position: absolute; inset: -10px; background: url(../landing/assets/ol/bunny.webp) center / cover; filter: blur(8px); opacity: .8; }
.ofr i { position: absolute; inset: 0; background: url(../landing/assets/ol/bunny.webp) center / contain no-repeat; }
/* C · corridor */
.sC { perspective: 720px; perspective-origin: 50% 50%; animation: scIn .4s var(--e2) 5.85s both, scOut .45s var(--e) 9.2s forwards; }
@keyframes scIn { from { opacity: 0; filter: blur(20px); } } @keyframes scOut { to { opacity: 0; filter: blur(22px); transform: scale(1.15); } }
.wld { position: absolute; left: 50%; top: 50%; width: 0; height: 0; transform-style: preserve-3d; animation: fly 3.9s cubic-bezier(.3,.1,.3,1) 5.85s both; } @keyframes fly { from { transform: translateZ(-700px); } to { transform: translateZ(1700px); } }
.wall { position: absolute; display: flex; flex-wrap: wrap; align-content: flex-start; gap: 26px; padding: 26px; transform-style: preserve-3d; }
.wl, .wr { width: 3600px; height: 860px; left: -1800px; top: -430px; flex-direction: column; } .wl { transform: translateX(-760px) translateZ(-1800px) rotateY(90deg); } .wr { transform: translateX(760px) translateZ(-1800px) rotateY(-90deg); }
.wt, .wb { width: 1520px; height: 3600px; left: -760px; top: -1800px; } .wt { transform: translateY(-430px) translateZ(-1800px) rotateX(-90deg); } .wb { transform: translateY(430px) translateZ(-1800px) rotateX(90deg); }
.tl { width: 250px; height: 250px; flex: none; overflow: hidden; border-radius: 28px; background: #fff; }
.tl .im { width: 100%; height: 100%; } .tl.ui { padding: 24px; } .tl.ui em { display: block; width: 60px; height: 60px; border-radius: 16px; background: linear-gradient(150deg, #8fbcff, #3b5cff); margin-bottom: 18px; }
.tl.ui b { display: block; height: 14px; margin-top: 12px; border-radius: 7px; background: #e6e9f4; } .tl.ui u { display: block; width: 70%; height: 36px; margin-top: 18px; border-radius: 18px; background: #0f1222; }
.cglow { position: absolute; left: 50%; top: 50%; width: 1400px; height: 520px; margin: -260px 0 0 -700px; border-radius: 50%; background: radial-gradient(ellipse at center, rgba(246,246,250,.96) 35%, rgba(246,246,250,.7) 55%, transparent 72%); }
.sC .row { font-size: 84px; }
/* D/E · ribbon → progress */
.rib { position: absolute; left: 0; top: 380px; width: 1920px; height: 300px; border-radius: 150px; background: linear-gradient(90deg, #b8b4ff, #3b5cff 45%, #5d8bff 70%, #7ec7ff);
  box-shadow: 0 30px 80px -30px rgba(59,92,255,.6); animation: ribA .45s var(--e2) 9.22s both, ribB .6s var(--e) 9.75s forwards, ribC 1.75s cubic-bezier(.4,0,.2,1) 10.45s forwards, fo .35s linear 12.25s forwards; }
@keyframes ribA { from { clip-path: inset(0 100% 0 0 round 150px); transform: skewY(-10deg) scaleY(1.4); } to { clip-path: inset(0 0 0 0 round 150px); } }
@keyframes ribB { from { left: 0; top: 380px; width: 1920px; height: 300px; border-radius: 150px; } to { left: 360px; top: 600px; width: 260px; height: 72px; border-radius: 36px; } }
@keyframes ribC { from { left: 360px; top: 600px; width: 260px; height: 72px; border-radius: 36px; } to { left: 360px; top: 600px; width: 1200px; height: 72px; border-radius: 36px; } }
.trk { position: absolute; left: 352px; top: 592px; width: 1216px; height: 88px; border-radius: 44px; background: #fff; box-shadow: 0 30px 60px -30px rgba(59,92,255,.35), 0 0 0 1.5px #e3e7f5; animation: fin .3s linear 10.1s both, fo .35s linear 12.25s forwards; }
.pl { position: absolute; left: 360px; top: 470px; font: 500 34px 'Inter', sans-serif; color: var(--mut); animation: wIn .5s var(--e2) 10.3s both, wOut .35s var(--e) 12.2s forwards; }
.pn { position: absolute; right: 352px; top: 400px; font: 400 150px/1 'Inter', sans-serif; letter-spacing: -.05em; animation: wIn .5s var(--e2) 10.3s both, wOut .35s var(--e) 12.22s forwards; }
.pn small { font-size: 64px; color: #b9c2ec; letter-spacing: -.03em; }
/* F · done */
.done { position: absolute; left: 0; right: 0; top: 230px; text-align: center; font: 400 128px/1 'Inter', sans-serif; letter-spacing: -.04em; }
.ck { position: absolute; left: 50%; top: 470px; width: 250px; height: 250px; margin-left: -125px; border-radius: 50%; background: radial-gradient(circle at 35% 30%, #fff, #eef2ff); box-shadow: 0 0 0 3px #cfd9ff, 0 40px 80px -30px rgba(59,92,255,.55);
  animation: ckIn .65s var(--po) 12.5s both, wOut .38s var(--e) 13.95s forwards; } @keyframes ckIn { from { opacity: 0; transform: scale(.3); filter: blur(10px); } }
.ck svg { position: absolute; inset: 55px; } .ck path { fill: none; stroke: #4d7cff; stroke-width: 9; stroke-linecap: round; stroke-linejoin: round; stroke-dasharray: 1; stroke-dashoffset: 1; animation: draw .45s var(--e2) 12.78s forwards; } @keyframes draw { to { stroke-dashoffset: 0; } }
.cf { position: absolute; left: 50%; top: 560px; border-radius: 3px; opacity: 0; animation: cf 1.5s cubic-bezier(.1,.7,.3,1) var(--d) both; }
@keyframes cf { 0% { opacity: 0; transform: translate(0, 0) rotate(0) scale(.2); } 4% { opacity: 1; } 55% { opacity: 1; transform: translate(var(--x), var(--y)) rotate(var(--r)) scale(1); } 100% { opacity: 0; transform: translate(var(--x), calc(var(--y) + var(--fall))) rotate(calc(var(--r) * 1.6)) scale(1); } }
/* G · carousel */
.car { position: absolute; left: 0; top: 330px; display: flex; gap: 40px; padding-left: 1920px; animation: carM 2.4s cubic-bezier(.25,.1,.25,1) 13.95s both, wOut .38s var(--e) 16.05s forwards; }
@keyframes carM { from { transform: translateX(-200px); filter: blur(14px); opacity: 0; } 15% { filter: blur(0); opacity: 1; } to { transform: translateX(-2980px); } }
.cc { position: relative; width: 400px; flex: none; padding: 16px; border-radius: 28px; background: #fff; }
.cim { height: 280px; border-radius: 18px; } .cm { display: grid; grid-template-columns: auto 1fr; align-items: center; gap: 4px 10px; margin: 18px 6px 4px; } .cm b { font: 600 26px 'Inter', sans-serif; }
.cm .dot { width: 14px; height: 14px; border-radius: 50%; } .cm small { grid-column: 1 / -1; font: 400 19px 'Inter', sans-serif; color: var(--mut); } .cc .dots { position: absolute; right: 24px; bottom: 26px; color: var(--mut); letter-spacing: 2px; }
/* H · archive dashboard */
.sH { perspective: 1800px; } .dash { position: absolute; left: 150px; top: 110px; width: 1620px; height: 880px; display: grid; grid-template-columns: 290px 1fr; overflow: hidden; border-radius: 30px; background: #fff;
  box-shadow: 0 0 0 2px #d6ddff, 0 60px 120px -40px rgba(59,92,255,.4); animation: dIn .8s var(--e2) 16.05s both, dOut .45s var(--e) 17.3s forwards; }
@keyframes dIn { from { opacity: 0; filter: blur(20px); transform: rotateY(-30deg) rotateX(18deg) scale(1.3); } to { transform: rotateY(-12deg) rotateX(9deg); } }
@keyframes dOut { from { transform: rotateY(-12deg) rotateX(9deg); } to { opacity: .0; filter: blur(16px); transform: rotateY(-12deg) rotateX(9deg) scale(1.08); } }
.dash aside { padding: 30px 24px; border-right: 1.5px solid #eceef6; } .dash aside .amk { display: inline-block; width: 34px; vertical-align: middle; } .dash aside > b { margin-left: 10px; font: 700 22px 'Inter', sans-serif; vertical-align: middle; }
.dash aside span { display: flex; align-items: center; gap: 12px; margin-top: 16px; padding: 12px 14px; border-radius: 12px; font: 500 19px 'Inter', sans-serif; color: #6d7290; } .dash aside span:first-of-type { margin-top: 34px; }
.dash aside span i { width: 18px; height: 18px; border-radius: 5px; background: #e3e7f5; } .dash aside .on { background: #eef2ff; color: var(--b1); } .dash aside .on i { background: var(--b1); }
.dash main { padding: 30px 34px; } .dh { display: flex; align-items: center; gap: 18px; } .dh b { font: 700 32px 'Inter', sans-serif; margin-right: auto; } .dh .sr { width: 320px; padding: 12px 18px; border-radius: 12px; background: #f4f5fa; color: var(--mut); font: 400 18px 'Inter', sans-serif; }
.dh .nw { padding: 12px 20px; border-radius: 12px; background: var(--ink); color: #fff; font: 600 18px 'Inter', sans-serif; } .dt { display: flex; gap: 24px; margin-top: 22px; padding-bottom: 14px; border-bottom: 1.5px solid #eceef6; font: 500 19px 'Inter', sans-serif; color: var(--mut); }
.dt .on { color: var(--b1); } .ag { display: grid; grid-template-columns: repeat(4, 1fr); gap: 22px; margin-top: 24px; } .ac .im { height: 230px; border-radius: 16px; } .ac b { display: block; margin-top: 12px; font: 600 20px 'Inter', sans-serif; }
.ac small { font: 400 16px 'Inter', sans-serif; color: var(--mut); }
.zc { position: absolute; left: 610px; top: 160px; width: 700px; padding: 22px; border-radius: 34px; background: #fff; animation: zIn .6s var(--e2) 17.32s both, wOut .38s var(--e) 17.95s forwards; }
@keyframes zIn { from { opacity: 0; transform: translate(-190px, -40px) scale(.36); } 30% { opacity: 1; } } .zc .im { height: 520px; border-radius: 22px; } .zc b { display: block; margin: 18px 6px 0; font: 600 34px 'Inter', sans-serif; } .zc small { margin-left: 6px; font: 400 24px 'Inter', sans-serif; color: var(--mut); }
/* I · models */
.sI .row { font-size: 96px; } .mc { position: absolute; width: 380px; padding: 16px; border-radius: 26px; background: #fff; rotate: var(--r);
  animation: mcIn .8s var(--e2) var(--d) both, mcDrift 2s linear var(--d) both, wOut .38s var(--e) 19.85s forwards; }
@keyframes mcIn { from { opacity: 0; filter: blur(16px); translate: var(--fx) var(--fy); rotate: var(--fr); } } @keyframes mcDrift { to { transform: translateY(-18px); } }
.mim { height: 230px; border-radius: 16px; } .mm { margin: 14px 4px 2px; } .mm b { font: 600 26px 'Inter', sans-serif; } .mm small { display: block; font: 400 18px 'Inter', sans-serif; color: var(--mut); }
/* J · trends list */
/* headline over a UI scene (J, T, P) */
.hl { position: absolute; left: 0; right: 0; top: 64px; display: flex; justify-content: center; gap: 20px; font: 400 72px/1.1 'Inter', sans-serif; letter-spacing: -.035em; }
.sub { position: absolute; left: 0; right: 0; top: 162px; text-align: center; font: 400 30px 'Inter', sans-serif; color: var(--mut); }
.pill { display: inline-block; padding: 10px 22px; border-radius: 99px; background: linear-gradient(90deg, #3b5cff, #6fb6ff); color: #fff; font: 600 24px 'Inter', sans-serif; }
.tyc::after { content: '▍'; color: #8fbcff; }
.sJ { perspective: 1600px; } .tp { position: absolute; left: 180px; top: 250px; width: 1100px; padding: 30px 36px; border-radius: 30px; background: #fff; box-shadow: 0 0 0 2px #d6ddff, 0 60px 120px -40px rgba(59,92,255,.4);
  animation: tpIn .8s var(--e2) 20.2s both, tpOut .45s var(--e) 23.9s forwards; }
@keyframes tpIn { from { opacity: 0; filter: blur(18px); transform: rotateX(30deg) rotateZ(3deg) scale(1.25); } to { transform: rotateX(10deg) rotateZ(-1.5deg); } }
@keyframes tpOut { from { transform: rotateX(10deg) rotateZ(-1.5deg); } to { opacity: 0; filter: blur(16px); transform: rotateX(8deg) scale(1.2) translateY(-40px); } }
.adb { padding: 12px 18px; border-radius: 12px; background: var(--ink); color: #fff; font: 600 19px 'Inter', sans-serif; white-space: nowrap; animation: adGo .3s var(--e2) 21.7s both; } @keyframes adGo { to { background: linear-gradient(90deg, #3b5cff, #6fb6ff); } }
.trw .adb.ghost { visibility: hidden; }
.adc { position: absolute; left: 1270px; top: 330px; width: 560px; padding: 26px 28px; border-radius: 28px; background: #fff; box-shadow: 0 0 0 2px #d6ddff, 0 50px 100px -40px rgba(59,92,255,.5);
  animation: adIn .6s var(--po) 21.9s both, wOut .38s var(--e) 23.9s forwards; } @keyframes adIn { from { opacity: 0; transform: translateX(-140px) scale(.6); filter: blur(12px); } }
.adc .pill { font-size: 19px; padding: 8px 16px; } .adc .hd { display: flex; align-items: center; gap: 16px; margin: 20px 0 16px; } .adc .hd .im { width: 84px; height: 84px; border-radius: 16px; }
.adc .hd b { display: block; font: 600 27px 'Inter', sans-serif; } .adc .hd small { font: 400 19px 'Inter', sans-serif; color: var(--mut); }
.adc .ln2 { display: block; margin-top: 10px; padding: 13px 16px; border-radius: 14px; background: #f4f5fa; font: 500 20px 'Inter', sans-serif; animation: wIn .4s var(--e2) var(--d) both; } .adc .ln2 em { font-style: normal; color: var(--b1); font-weight: 600; margin-right: 8px; }
.th { display: flex; align-items: center; gap: 14px; margin-bottom: 18px; } .th b { font: 700 36px 'Inter', sans-serif; margin-right: auto; } .th span { padding: 10px 18px; border-radius: 12px; background: #f4f5fa; font: 500 18px 'Inter', sans-serif; color: #6d7290; }
.trw { display: grid; grid-template-columns: 90px 1fr auto auto; gap: 22px; align-items: center; padding: 16px; border-radius: 18px; } .trw:nth-child(2) { background: #eef2ff; }
.trw .im { width: 90px; height: 90px; border-radius: 14px; } .trw small { font: 500 18px 'Inter', sans-serif; color: var(--mut); } .trw b { display: block; font: 600 28px 'Inter', sans-serif; } .trw em { font: 700 34px 'Inter', sans-serif; font-style: normal; color: #16a36a; }
/* K · row + launch button */
.kr { position: absolute; left: 380px; top: 440px; width: 1160px; height: 200px; display: flex; align-items: center; gap: 30px; padding: 0 40px; border-radius: 34px; background: #fff;
  animation: wIn .6s var(--e2) 21.85s both, krOut .55s var(--e) 22.55s forwards; } @keyframes krOut { to { transform: translateX(-560px); opacity: .0; filter: blur(10px); } }
.kr .cb { width: 34px; height: 34px; border-radius: 9px; box-shadow: inset 0 0 0 2.5px #c7cde2; } .kr .im { width: 130px; height: 130px; border-radius: 20px; } .kr b { font: 600 44px 'Inter', sans-serif; } .kr small { display: block; margin-top: 6px; font: 400 26px 'Inter', sans-serif; color: var(--mut); }
.kb { position: absolute; left: 50%; top: 470px; width: 620px; height: 140px; margin-left: -310px; display: grid; place-items: center; border-radius: 30px; font: 600 44px 'Inter', sans-serif; letter-spacing: -.01em;
  animation: kbIn .6s var(--e2) 22.6s both, kbGo .4s var(--e2) 23.3s both, wOut .38s var(--e) 24.05s forwards; background: var(--ink); color: #fff; box-shadow: 0 30px 60px -30px rgba(15,18,34,.6); }
@keyframes kbIn { from { opacity: 0; transform: translateX(520px); filter: blur(12px); } } @keyframes kbGo { to { background: linear-gradient(90deg, #3b5cff, #6fb6ff); transform: scale(1.08); box-shadow: 0 40px 80px -30px rgba(59,92,255,.8); } }
.kbw { position: absolute; left: 50%; top: 470px; width: 620px; height: 140px; margin-left: -310px; border-radius: 30px; background: #fff; box-shadow: 0 0 0 2px #e3e7f5; animation: kbIn .6s var(--e2) 22.5s both, wOut .38s var(--e) 24.05s forwards; transform-origin: center; scale: 1.18 1.4; }
/* L · mark flies */
.bm { position: absolute; left: 50%; top: 50%; width: 420px; margin: -150px 0 0 -210px; filter: drop-shadow(0 40px 60px rgba(59,92,255,.45)); animation: bmIn .6s var(--po) 24.15s both, bmSpin .5s var(--e) 24.8s forwards, bmFly .7s cubic-bezier(.5,0,.2,1) 25.3s forwards; }
@keyframes bmIn { from { opacity: 0; transform: scale(.2) rotate(-40deg); filter: blur(14px); } } @keyframes bmSpin { to { transform: scale(.28) rotate(200deg); } }
@keyframes bmFly { from { transform: scale(.28) rotate(200deg); } to { transform: translate(720px, -330px) scale(.2) rotate(420deg); opacity: 0; } }
.trail { position: absolute; left: 960px; top: 540px; width: 900px; height: 90px; margin-top: -45px; border-radius: 45px; background: linear-gradient(90deg, transparent, rgba(111,182,255,.55)); filter: blur(18px); transform-origin: 0 50%; rotate: -24deg;
  animation: trl .8s var(--e) 25.3s both; } @keyframes trl { 0% { opacity: 0; transform: scaleX(0); } 45% { opacity: 1; } 100% { opacity: 0; transform: scaleX(1) translateX(300px); } }
/* M · words + sparkle */
.sM .row { font-size: 88px; gap: 22px; } .spk { width: 54px; animation: spk .5s var(--po) var(--d) both, wOut .38s var(--e) 27.95s forwards; } @keyframes spk { from { opacity: 0; transform: scale(.2) rotate(-90deg); } }

/* A2 · AI assistant: chat builds the node scheme, user runs it */
.sX .row { font-size: 88px; }
.aiw { position: absolute; left: 130px; top: 175px; width: 1660px; height: 730px; display: grid; grid-template-columns: 560px 1fr; overflow: hidden; border-radius: 32px; background: #fff;
  box-shadow: 0 0 0 2px #d6ddff, 0 60px 120px -40px rgba(59,92,255,.45); animation: aiIn .8s var(--e2) 23.3s both, aiOut .45s var(--e) 28.95s forwards; }
@keyframes aiIn { from { opacity: 0; filter: blur(20px); transform: perspective(1600px) rotateX(24deg) scale(1.25); } to { transform: perspective(1600px) rotateX(6deg); } }
@keyframes aiOut { from { transform: perspective(1600px) rotateX(6deg); } to { opacity: 0; filter: blur(16px); transform: perspective(1600px) rotateX(6deg) scale(1.1); } }
.ch { display: flex; flex-direction: column; gap: 18px; padding: 30px 30px; border-right: 1.5px solid #eceef6; background: #fbfbfe; }
.chh { display: flex; align-items: center; gap: 14px; padding-bottom: 18px; border-bottom: 1.5px solid #eceef6; } .ava { display: grid; place-items: center; width: 54px; height: 54px; border-radius: 50%; background: linear-gradient(150deg, #8fbcff, #3b5cff); }
.ava .mk { width: 28px; } .chh b { display: block; font: 700 26px 'Inter', sans-serif; } .chh small { font: 500 18px 'Inter', sans-serif; color: #16a36a; }
.ub { align-self: flex-end; max-width: 92%; padding: 18px 22px; border-radius: 22px 22px 6px 22px; background: var(--ink); color: #fff; font: 400 25px/1.35 'Inter', sans-serif; animation: wIn .45s var(--e2) 23.65s both; min-height: 64px; }
.ub .tc.tyc::after { content: '▍'; color: #8fbcff; }
.ar { font: 500 24px 'Inter', sans-serif; color: var(--ink); animation: wIn .45s var(--e2) 25.0s both; }
.st { display: flex; align-items: center; gap: 14px; padding: 14px 18px; border-radius: 16px; background: #fff; box-shadow: 0 0 0 1.5px #e3e7f5; font: 500 23px 'Inter', sans-serif; animation: wIn .45s var(--e2) var(--d) both; }
.st .sp { position: relative; width: 30px; height: 30px; flex: none; } .st .sp::before { content: ''; position: absolute; inset: 0; border-radius: 50%; border: 3.5px solid #cfd9ff; border-top-color: var(--b1); animation: spin .7s linear 0s infinite, fo .15s linear var(--k) forwards; }
.st .sp::after { content: '✓'; position: absolute; inset: 0; display: grid; place-items: center; border-radius: 50%; background: linear-gradient(150deg, #6fb6ff, #3b5cff); color: #fff; font: 700 17px 'Inter', sans-serif; animation: ckPop .35s var(--po) var(--k) both; }
@keyframes spin { to { rotate: 360deg; } } @keyframes ckPop { from { opacity: 0; transform: scale(.3); } }
.st.hint { background: #eef2ff; box-shadow: inset 0 0 0 2px #cfd9ff; color: var(--b1); } .st.hint .sp::before { display: none; } .st.hint .sp::after { content: '▸'; animation: ckPop .35s var(--po) var(--d) both; }
.cvs { position: relative; background: radial-gradient(#dde1ee 1.5px, transparent 2px) 0 0 / 28px 28px, #f3f4f9; } .cvh { position: absolute; left: 34px; top: 26px; font: 600 22px 'Inter', sans-serif; color: var(--mut); }
.auto { position: absolute; right: 30px; top: 22px; padding: 10px 18px; border-radius: 99px; background: linear-gradient(90deg, #3b5cff, #6fb6ff); color: #fff; font: 600 19px 'Inter', sans-serif; animation: ckPop .45s var(--po) 27.25s both; }
.aed2 { position: absolute; inset: 0; width: 100%; height: 100%; } .aed2 path { fill: none; stroke: #6f8dff; stroke-width: 4; stroke-dasharray: 1; stroke-dashoffset: 1; animation: draw .4s var(--e2) var(--d) forwards; }
.xn { position: absolute; top: 215px; width: 238px; border-radius: 20px; background: #fff; animation: nIn .55s var(--po) var(--d) both; }
@keyframes nIn { from { opacity: 0; transform: scale(.4) translateY(30px); filter: blur(8px); } }
.xn .h { display: flex; align-items: center; gap: 10px; padding: 14px 16px; border-bottom: 1.5px solid #eef0f7; font: 600 19px 'Inter', sans-serif; }
.xn .h b { display: grid; place-items: center; width: 30px; height: 30px; border-radius: 9px; font-size: 15px; } .xn .bd { padding: 14px 16px; }
.xn .im { height: 175px; border-radius: 12px; } .xn .tp3 { display: flex; gap: 8px; } .xn .tp3 .im { flex: 1; height: 120px; border-radius: 10px; }
.xn .r { display: flex; justify-content: space-between; margin-top: 8px; padding: 9px 12px; border-radius: 10px; background: #f4f5fa; font: 500 16px 'Inter', sans-serif; } .xn .r:first-child { margin-top: 0; }
.xn .ln { display: block; height: 12px; margin-top: 10px; border-radius: 6px; background: #e6e9f4; } .xn .ln:first-child { margin-top: 0; width: 90%; background: #cfd9ff; }

/* T · texts & documents */
.cww { position: absolute; left: 360px; top: 280px; width: 1200px; height: 530px; display: flex; flex-direction: column; gap: 22px; padding: 30px 36px; border-radius: 32px; background: #fff;
  box-shadow: 0 0 0 2px #d6ddff, 0 60px 120px -40px rgba(59,92,255,.45); animation: aiIn .8s var(--e2) 24.35s both, aiOut .45s var(--e) 28.4s forwards; }
.cwh { display: flex; align-items: center; gap: 14px; padding-bottom: 20px; border-bottom: 1.5px solid #eceef6; } .cwh b { font: 700 28px 'Inter', sans-serif; margin-right: auto; }
.cwh .ava { width: 50px; height: 50px; } .cwh span:not(.ava) { padding: 9px 16px; border-radius: 10px; background: #f4f5fa; font: 600 17px 'JetBrains Mono', monospace; color: #6d7290; }
.cww .ub { animation-delay: 24.75s; font-size: 27px; } .ans { max-width: 92%; padding: 22px 26px; border-radius: 22px 22px 22px 6px; background: #f4f5fa; font: 400 27px/1.45 'Inter', sans-serif; animation: wIn .4s var(--e2) 26.0s both; }
.fch { display: flex; align-items: center; gap: 16px; align-self: flex-start; padding: 14px 22px 14px 14px; border-radius: 18px; background: #eef2ff; animation: ckPop .45s var(--po) 27.65s both; }
.fch i { display: grid; place-items: center; width: 52px; height: 52px; border-radius: 12px; background: #3b5cff; color: #fff; font: 700 15px 'Inter', sans-serif; font-style: normal; }
.fch b { font: 600 23px 'Inter', sans-serif; } .fch small { display: block; font: 400 18px 'Inter', sans-serif; color: var(--mut); }
.sT .hl > *, .sT .sub { animation-fill-mode: both; } .sT .sub { animation: wIn .5s var(--e2) 24.6s both, wOut .38s var(--e) 28.35s forwards; }
/* P · Creative Predictor */
.sP .hl { top: 128px; } .ptop { position: absolute; left: 0; right: 0; top: 52px; text-align: center; animation: ckPop .45s var(--po) 28.65s both, wOut .38s var(--e) 33.05s forwards; }
.pcs { position: absolute; left: 0; right: 0; top: 270px; display: flex; justify-content: center; gap: 44px; }
.pc { position: relative; width: 380px; padding: 14px 14px 22px; border-radius: 28px; background: #fff; animation: nIn .55s var(--po) var(--d) both, pcDim .4s var(--e2) 31.35s both, wOut .38s var(--e) 33.05s forwards; }
@keyframes pcDim { to { opacity: .45; filter: saturate(.4); } } .pc.win { animation: nIn .55s var(--po) var(--d) both, pcWin .5s var(--po) 31.35s both, wOut .38s var(--e) 33.05s forwards; } @keyframes pcWin { to { transform: scale(1.06); } }
.pc .pim { position: relative; height: 380px; border-radius: 18px; overflow: hidden; } .pc .pim .im { position: absolute; inset: 0; }
.pc .cap { position: absolute; left: 14px; right: 14px; bottom: 14px; padding: 10px 14px; border-radius: 12px; background: rgba(15,18,34,.78); color: #fff; font: 600 20px 'Inter', sans-serif; }
.pc .tag { position: absolute; left: 14px; top: 14px; padding: 8px 14px; border-radius: 10px; background: #ff5a4e; color: #fff; font: 700 20px 'Inter', sans-serif; }
.pc .sc2 { display: flex; align-items: baseline; justify-content: space-between; margin: 18px 8px 10px; } .pc .sc2 > span { font: 500 21px 'Inter', sans-serif; color: var(--mut); }
.pc .sc2 b { font: 700 46px/1 'Inter', sans-serif; letter-spacing: -.03em; } .pc .sc2 b small { font-size: 22px; color: #b9c2ec; }
.pc .bar { height: 12px; margin: 0 8px; border-radius: 6px; background: #eceef6; overflow: hidden; } .pc .bar i { display: block; height: 100%; border-radius: 6px; background: linear-gradient(90deg, #3b5cff, #6fb6ff); transform-origin: 0 50%; animation: barF 1s cubic-bezier(.3,.7,.3,1) 30.2s both; }
@keyframes barF { from { transform: scaleX(0); } }
.pc .best { position: absolute; left: 50%; top: -24px; padding: 10px 20px; border-radius: 99px; background: linear-gradient(90deg, #16a36a, #34c98a); color: #fff; font: 600 21px 'Inter', sans-serif; white-space: nowrap; transform: translateX(-50%); animation: ckPop .45s var(--po) 31.4s both; }
.pctl { position: absolute; left: 0; right: 0; top: 890px; display: flex; justify-content: center; align-items: center; gap: 14px; animation: wIn .5s var(--e2) 29.35s both, wOut .38s var(--e) 33.05s forwards; }
.pctl span { padding: 14px 22px; border-radius: 14px; background: #fff; font: 500 22px 'Inter', sans-serif; color: #6d7290; } .pctl span.on { background: #eef2ff; color: var(--b1); }
.pctl .go { margin-left: 26px; padding: 16px 40px; border-radius: 16px; background: var(--ink); color: #fff; font: 600 24px 'Inter', sans-serif; animation: adGo .3s var(--e2) 30.0s both; }
/* N · logo */
.lg { position: absolute; left: 50%; top: 440px; display: flex; align-items: center; gap: 30px; transform: translateX(-50%); }
.lg .mk { width: 150px; animation: lgM .6s var(--po) 28.2s both; } @keyframes lgM { from { opacity: 0; transform: scale(.2); filter: blur(10px); } }
.lg b { font: 500 134px/1 'Inter', sans-serif; letter-spacing: -.04em; clip-path: inset(0 0 0 0); animation: lgW .7s var(--e2) 28.55s both; } @keyframes lgW { from { clip-path: inset(0 100% 0 0); transform: translateX(-60px); opacity: 0; } }
.url { position: absolute; left: 0; right: 0; top: 700px; text-align: center; font: 500 34px 'Inter', sans-serif; color: var(--ink); animation: wIn .6s var(--e2) 29.05s both; }
.fn { position: absolute; left: 0; right: 0; bottom: 60px; text-align: center; font: 400 20px 'Inter', sans-serif; color: #9ba0b8; animation: fin .5s linear 29.4s both; }
</style>
</head>
<body>
<div id="st">
  <svg width="0" height="0" style="position:absolute"><defs><linearGradient id="bg1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8fc6ff"/><stop offset=".55" stop-color="#4d7cff"/><stop offset="1" stop-color="#3b5cff"/></linearGradient></defs></svg>

  <section class="sc sA">
    <div class="row">__A1__</div>
    <div class="row">__A2__</div>
    <div class="row r3"><span class="l">__A3L__</span><span class="r">__A3R__</span></div>
    <div class="tile"><i class="back"></i><div class="doc"><b data-count="3.3,1.0,0,112,0" data-pre="+$">+$0</b><small>перенесено на следующий месяц</small></div><div class="front">Бюджет<small>остаток сохраняется</small></div></div>
    __HAND_A__
  </section>

  <section class="sc sB">__APP__</section>

  <section class="sc sC"><div class="wld">__CORRIDOR__</div><div class="cglow"></div><div class="row">__C1__</div><div class="row">__C2__</div></section>

  <section class="sc sE"><div class="trk"></div><div class="rib"></div><div class="pl">Адаптация под 4 формата</div><div class="pn"><span class="bl" data-count="10.45,1.75,20,100,0">20</span><small>/100</small></div></section>

  <section class="sc sF"><div class="done">__F1__</div><div class="ck"><svg viewBox="0 0 100 100"><path pathLength="1" d="M22 52 L42 72 L80 30"/></svg></div>__CONFETTI__</section>

  <section class="sc sG"><div class="car">__CAROUSEL__</div></section>

  <section class="sc sH">__ARCHIVE__<div class="zc"><i class="im" style="background-image:url(../landing/assets/ol/coffee.webp)"></i><b>Кофемашина Aroma One</b><small>Stories · Пост · Kaspi · Discovery — готово</small></div>__HAND_H__</section>

  <section class="sc sI">__MODELS__<div class="row">__I1__</div></section>

  <section class="sc sJ"><div class="hl">__J1__</div><div class="hl">__J2__</div>__TRENDS__ __HAND_J__</section>


  <section class="sc sT"><div class="hl">__T1__</div><p class="sub">Описания, посты, контент-планы — сразу в Word, Excel и PowerPoint</p>
    <div class="cww"><div class="cwh"><span class="ava">__AVA__</span><b>Тексты</b><span>DOCX</span><span>XLSX</span><span>PPTX</span></div>
      <div class="ub"><span class="tc" data-type="24.9,34" data-txt="SEO-описание для Kaspi: мягкий зайка"></span></div>
      <div class="ans"><span data-type="26.05,90" data-txt="Мягкая игрушка «Зайка» из нежного плюша с гипоаллергенным наполнителем. Подходит детям с рождения: безопасные материалы, прочные швы."></span></div>
      <div class="fch"><i>DOCX</i><div><b>Описание_Kaspi.docx</b><small>готово к скачиванию</small></div></div></div></section>

  <section class="sc sP"><div class="ptop"><span class="pill">Creative Predictor</span></div><div class="hl">__P1__</div>
    <div class="pcs">
      <div class="pc" style="--d:29.1s"><div class="pim">__PIM1__</div><div class="sc2"><span>Вариант 1</span><b><span data-count="30.2,1,0,64,0">0</span><small>/100</small></b></div><div class="bar"><i style="width:64%"></i></div></div>
      <div class="pc win" style="--d:29.2s"><div class="pim">__PIM2__<span class="cap">Мягкий зайка · 0+</span></div><div class="sc2"><span>Вариант 2</span><b><span data-count="30.2,1,0,91,0">0</span><small>/100</small></b></div><div class="bar"><i style="width:91%"></i></div><span class="best">★ Лучший для Kaspi</span></div>
      <div class="pc" style="--d:29.3s"><div class="pim">__PIM3__<span class="cap">Хит продаж</span></div><div class="sc2"><span>Вариант 3</span><b><span data-count="30.2,1,0,77,0">0</span><small>/100</small></b></div><div class="bar"><i style="width:77%"></i></div></div>
    </div>
    <div class="pctl"><span class="on">Kaspi</span><span>Instagram</span><span>TikTok</span><span class="go">Оценить</span></div>__HAND_P__</section>

  <section class="sc sX" data-off="__AI_SHIFT__"><div class="row">__X1__</div>
    <div class="aiw"><div class="ch"><div class="chh"><span class="ava">__AVA__</span><div><b>Floko</b><small>● ИИ-ассистент</small></div></div>
      <div class="ub"><span class="tc" data-type="23.8,34" data-txt="Сделай карточки мягкого зайки для Kaspi и сторис"></span></div>
      <div class="ar">Готово, собрал схему:</div>
      <div class="st" style="--d:25.2s;--k:25.6s"><i class="sp"></i>Разобрал аудиторию и нишу</div>
      <div class="st" style="--d:25.8s;--k:26.2s"><i class="sp"></i>Подобрал шаблон и промпт</div>
      <div class="st" style="--d:26.4s;--k:26.8s"><i class="sp"></i>Собрал 4 ноды на холсте</div>
      <div class="st hint" style="--d:27.4s"><i class="sp"></i>Проверьте и нажмите «Запустить»</div></div>
    <div class="cvs"><span class="cvh">Холст · Проект «Зайка»</span><span class="auto">✦ Собрано ассистентом</span>
      <svg class="aed2" viewBox="0 0 1100 730" preserveAspectRatio="none"><path pathLength="1" style="--d:25.6s" d="M268 345 C 284 345, 284 345, 300 345"/><path pathLength="1" style="--d:26.2s" d="M538 345 C 554 345, 554 345, 570 345"/><path pathLength="1" style="--d:26.8s" d="M808 345 C 824 345, 824 345, 840 345"/></svg>
      <div class="xn" style="left:30px;--d:25.3s"><div class="h"><b style="background:#e8f3ff;color:#3b8bff">▣</b>Фото товара</div><div class="bd"><i class="im" style="background-image:url(../landing/assets/ol/bunny.webp);background-position:center 30%"></i></div></div>
      <div class="xn" style="left:300px;--d:25.9s"><div class="h"><b style="background:#fff1e3;color:#d98a2b">✦</b>Шаблон One Launch</div><div class="bd"><div class="tp3"><i class="im" style="background-image:url(../landing/assets/ol/pajama.webp)"></i><i class="im" style="background-image:url(../landing/assets/ol/body.webp)"></i></div></div></div>
      <div class="xn" style="left:570px;--d:26.5s"><div class="h"><b style="background:#efeaff;color:#6b4dff">⌗</b>Адаптация</div><div class="bd"><span class="r"><span>Kaspi</span><span>1125×330</span></span><span class="r"><span>Stories</span><span>1080×1920</span></span><span class="r"><span>Пост</span><span>1080×1080</span></span></div></div>
      <div class="xn" style="left:840px;--d:27.1s"><div class="h"><b style="background:#e9f8f0;color:#16a36a">¶</b>Текст карточки</div><div class="bd"><i class="ln"></i><i class="ln"></i><i class="ln" style="width:70%"></i><i class="ln" style="width:85%"></i></div></div>
    </div></div></section>
  <section class="sc sK" data-off="__SHIFT__"><div class="kr"><span class="cb"></span><i class="im" style="background-image:url(../landing/assets/ol/bunny.webp)"></i><div><b>Мягкий зайка · 4 формата</b><small>Kaspi · Яндекс РСЯ · Stories · Discovery</small></div></div>
    <div class="kb">Запустить пайплайн ▸</div>__HAND_K__</section>

  <section class="sc sL" data-off="__SHIFT__"><div class="trail"></div>__BIGMARK__</section>

  <section class="sc sM" data-off="__SHIFT__"><div class="row">__M1__</div></section>

  <section class="sc sN" data-off="__SHIFT__"><div class="lg">__LOGOMARK__<b>ONEFLOW</b></div><div class="url">oneflow.art</div>
    <p class="fn">* до 50% — в сравнении с оплатой тех же моделей в отдельных сервисах; итог зависит от моделей и объёма. Неизрасходованный бюджет переходит на следующий месяц.</p></section>
</div>
<script>
(function () {
  const T = __T__, q = new URLSearchParams(location.search), st = document.getElementById('st');
  const counters = [...document.querySelectorAll('[data-count]')], typers = [...document.querySelectorAll('[data-type]')];
  const offOf = (el) => { const s = el && el.closest && el.closest('[data-off]'); return s ? +s.dataset.off : 0; };
  counters.forEach((el) => { el._o = offOf(el); }); typers.forEach((el) => { el._o = offOf(el); });
  let AN = null;
  window.seek = (t) => {
    if (!AN) { AN = document.getAnimations(); AN.forEach((a) => { a.pause(); a._o = offOf(a.effect && a.effect.target); }); }
    AN.forEach((a) => { a.currentTime = (t - a._o) * 1000; });
    counters.forEach((el) => { const [s, d, a, b, dec] = el.dataset.count.split(',').map(Number), p = Math.min(1, Math.max(0, (t - el._o - s) / d)), e = 1 - Math.pow(1 - p, 3);
      el.textContent = (el.dataset.pre || '') + (a + (b - a) * e).toFixed(dec || 0) + (el.dataset.suf || ''); });
    typers.forEach((el) => { const [s, cps] = el.dataset.type.split(',').map(Number), n = Math.max(0, Math.min(el.dataset.txt.length, Math.floor((t - el._o - s) * cps)));
      el.textContent = el.dataset.txt.slice(0, n); el.classList.toggle('tyc', n > 0 && n < el.dataset.txt.length); });
  };
  const fit = () => { const k = Math.min(innerWidth / 1920, innerHeight / 1080); st.style.transform = 'translate(' + (innerWidth - 1920 * k) / 2 + 'px,' + (innerHeight - 1080 * k) / 2 + 'px) scale(' + k + ')'; };
  if (q.get('cap')) { window.seek(0); return; }
  fit(); addEventListener('resize', fit);
  let t0 = null; const loop = (now) => { if (t0 === null) t0 = now; window.seek(((now - t0) / 1000) % T); requestAnimationFrame(loop); };
  document.fonts.ready.then(() => requestAnimationFrame(loop));
})();
</script>
</body>
</html>
"""


def build():
    rep = {
        '__A1__': w('Больше', .15, 1.35, 'bl') + w('контента.', .42, 1.38),
        '__A2__': w('До', 1.5, 2.75) + f'<span class="wi bl" style="--d:1.62s;--o:2.78s" data-count="1.66,.8,0,50,0" data-suf="%">0%</span>' + w('дешевле*', 1.88, 2.8),
        '__A3L__': w('Остаток', 2.9, 3.92), '__A3R__': w('не сгорает', 3.42, 3.95, 'bl'),
        '__HAND_A__': hand(1500, 980, 952, 520, 3.45, 4.02, 4.3),
        '__APP__': app_window(), '__CORRIDOR__': corridor(),
        '__C1__': w('Фото.', 6.25, 7.75, 'bl') + w('Видео.', 6.5, 7.78) + w('Тексты.', 6.75, 7.8, 'bl') + w('Баннеры.', 7.0, 7.82),
        '__C2__': w('Всё', 7.95, 9.1) + w('в одном', 8.1, 9.12) + w('окне', 8.25, 9.14, 'bl'),
        '__F1__': w('Готово', 12.42, 13.95, 'bl'), '__CONFETTI__': confetti(), '__CAROUSEL__': carousel(),
        '__ARCHIVE__': archive(), '__HAND_H__': hand(1560, 980, 700, 360, 16.6, 17.2, 17.45),
        '__MODELS__': model_cards(), '__I1__': w('30+', 18.2, 19.85, 'bl') + w('нейросетей', 18.42, 19.88),
        '__TRENDS__': trends(), '__HAND_J__': hand(1500, 1000, *HJ, 21.05, 21.7, 22.0),
        '__J1__': w('Автоматический', 19.95, 22.45) + w('анализ', 20.1, 22.47, 'bl') + w('трендов', 20.25, 22.49, 'bl'),
        '__J2__': w('Адаптируйте', 22.55, 23.95) + w('их под себя', 22.7, 23.97) + w('автоматически', 22.85, 23.99, 'bl'),
        '__T1__': w('Тексты', 24.15, 28.35) + w('и документы', 24.3, 28.37) + w('за секунды', 24.45, 28.39, 'bl'),
        '__P1__': w('Лучший креатив', 28.75, 33.05, 'bl') + w('— ещё до запуска рекламы', 28.9, 33.07),
        '__PIM1__': img('bunny', '', ';background-position:center 20%;filter:saturate(.55) brightness(1.06)'),
        '__PIM2__': img('bunny', '', ';background-position:center 30%'),
        '__PIM3__': img('bunny', '', ';background-size:170%;background-position:50% 35%'),
        '__HAND_P__': hand(1560, 1060, *HP, 29.45, 30.0, 30.3),
        '__HAND_K__': hand(1560, 980, 1010, 548, 22.75, 23.25, 23.7),
        '__BIGMARK__': mark('bm'),
        '__M1__': w('Генерация.', 26.0, 27.95, 'bl') + w('Адаптация.', 26.5, 27.97) + w('Запуск.', 27.0, 28.0, 'bl')
                  + ''.join(f'<span class="spk" style="--d:{d}s;display:inline-block">{mark("mk")}</span>' for d in (27.25,)),
        '__LOGOMARK__': mark(), '__T__': str(T), '__SHIFT__': str(SHIFT), '__AI_SHIFT__': str(AI_SHIFT), '__AVA__': mark('mk', '#fff'),
        '__X1__': w('ИИ-ассистент', 22.05, 23.3, 'bl') + w('собирает', 22.3, 23.32) + w('пайплайн', 22.5, 23.34, 'bl') + w('за вас', 22.7, 23.36),
    }
    html = HTML
    for k, val in rep.items():
        html = html.replace(k, val)
    assert '__' not in re.sub(r'__proto__', '', html.split('<script>')[0]), re.findall(r'__[A-Z0-9_]+__', html)
    open(os.path.join(HERE, 'oneflow-clean.html'), 'w', encoding='utf-8').write(html)
    print('oneflow-clean.html')


if __name__ == '__main__':
    build()
