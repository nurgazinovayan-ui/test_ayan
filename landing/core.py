"""Shared base for ONEFLOW landing variants (rebuilt after the scratchpad loss, now kept in the repo).

page() assembles one self-contained design preview: nav (Войти / Регистрация / burger menu), a variant's own hero,
then the shared sections — models marquee, «why» bento, three steps, ad-cabinet adaptation, 9 modules, creatives
gallery, savings calculator, pricing, FAQ, closing band, footer. Everything is styled through CSS tokens, so a variant
supplies tokens + its own CSS (skin) + hero markup.

Ad creatives (adaptation stage, gallery) are drawn in CSS/SVG by cr(): a product illustration, brand, title, price
and badge that re-lay themselves out with container queries for each cabinet's aspect ratio.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
APP = 'https://app.oneflow.art/'
REG = '?auth=register'

SUB = ('Креативы для всех рекламных кабинетов в пару кликов: ассистент готовит — вы запускаете. '
       'Генерация до 50% дешевле*, бюджет не сгорает в конце месяца.')
FOOT = '* До 50% — сравнение с оплатой тех же моделей в отдельных сервисах; итог зависит от моделей и объёма.'
MODELS = ['GPT Image', 'Nano Banana Pro', 'Seedream', 'Veo 3.1', 'Kling', 'Seedance', 'Hailuo', 'Recraft', 'Flux']
PRESETS = [('Stories', 1080, 1920), ('Discovery', 960, 1200), ('Discovery', 1200, 628), ('Kaspi', 1125, 330),
           ('Яндекс РСЯ', 1080, 450), ('GDN', 300, 600), ('BYYD', 300, 250), ('Свой размер', 728, 90)]
CABS = [('Kaspi', 1125, 330), ('Яндекс РСЯ', 1080, 450), ('Google Discovery', 1200, 628), ('GDN', 300, 600), ('BYYD', 300, 250), ('Stories', 1080, 1920)]


def reg(label='Начать бесплатно', cls='btn p'):
    return f'<a class="{cls}" data-app="register" href="{APP}{REG}">{label}</a>'


ACTS = (f'<div class="acts">{reg()}<a class="btn s" href="#calc">Посчитать экономию</a></div>'
        '<p class="tiny">без карты · бесплатный тариф навсегда</p>')


def T(bg, ink, ac, *, card=None, ink2=None, muted=None, line=None, line2=None, btn=None, btn_ink=None, ac_ink=None,
      d="'Inter Tight',sans-serif", f="'Inter',sans-serif", m="'JetBrains Mono',monospace", dw='700', dl='-.04em', r='18px', br='12px'):
    """Design tokens. Colours derive from bg/ink when not given."""
    mix = lambda p: f'color-mix(in srgb, {ink} {p}%, {bg})'
    return (f'--bg:{bg};--ink:{ink};--ac:{ac};--card:{card or mix(4)};--ink2:{ink2 or mix(78)};--muted:{muted or mix(55)};'
            f'--line:{line or mix(12)};--line2:{line2 or mix(22)};--btn:{btn or ink};--btn-ink:{btn_ink or bg};--ac-ink:{ac_ink or bg};'
            f'--d:{d};--f:{f};--m:{m};--dw:{dw};--dl:{dl};--r:{r};--br:{br};')


# ---------------------------------------------------------------- product illustrations (viewBox 0 0 200 200)
PROD = {
    'speaker': '<rect x="58" y="22" width="84" height="160" rx="42" style="fill:var(--pa)"/><rect x="58" y="22" width="84" height="160" rx="42" fill="url(#gl)"/>'
               '<circle cx="100" cy="112" r="30" fill="rgba(0,0,0,.35)"/><circle cx="100" cy="112" r="20" fill="rgba(0,0,0,.35)"/><circle cx="100" cy="112" r="7" fill="rgba(255,255,255,.35)"/>'
               '<rect x="84" y="44" width="32" height="6" rx="3" fill="rgba(255,255,255,.55)"/><rect x="92" y="160" width="16" height="4" rx="2" fill="rgba(255,255,255,.45)"/>',
    'headphones': '<path d="M42 118 V96 a58 58 0 0 1 116 0 V118" fill="none" stroke-width="13" stroke-linecap="round" style="stroke:var(--pa)"/>'
                  '<rect x="26" y="104" width="40" height="66" rx="18" style="fill:var(--pa)"/><rect x="134" y="104" width="40" height="66" rx="18" style="fill:var(--pa)"/>'
                  '<rect x="26" y="104" width="40" height="66" rx="18" fill="url(#gl)"/><rect x="134" y="104" width="40" height="66" rx="18" fill="url(#gl)"/>'
                  '<rect x="54" y="116" width="10" height="42" rx="5" fill="rgba(0,0,0,.3)"/><rect x="136" y="116" width="10" height="42" rx="5" fill="rgba(0,0,0,.3)"/>',
    'watch': '<rect x="74" y="10" width="52" height="54" rx="10" fill="rgba(0,0,0,.55)"/><rect x="74" y="136" width="52" height="54" rx="10" fill="rgba(0,0,0,.55)"/>'
             '<rect x="52" y="48" width="96" height="104" rx="30" style="fill:var(--pa)"/><rect x="62" y="58" width="76" height="84" rx="22" fill="#0b0b0f"/>'
             '<text x="100" y="104" text-anchor="middle" font-family="Inter,sans-serif" font-weight="700" font-size="24" fill="#fff">10:09</text>'
             '<rect x="80" y="114" width="40" height="5" rx="2.5" style="fill:var(--pb)"/><rect x="148" y="84" width="7" height="22" rx="3" style="fill:var(--pa)"/>',
    'bottle': '<rect x="84" y="18" width="32" height="30" rx="5" fill="#1b1b1b"/><rect x="90" y="46" width="20" height="14" style="fill:var(--pa)"/>'
              '<rect x="50" y="58" width="100" height="126" rx="26" style="fill:var(--pa)" opacity=".92"/><rect x="50" y="96" width="100" height="88" rx="26" style="fill:var(--pb)" opacity=".75"/>'
              '<rect x="50" y="58" width="100" height="126" rx="26" fill="url(#gl)"/><rect x="70" y="112" width="60" height="30" rx="4" fill="rgba(255,255,255,.85)"/>'
              '<text x="100" y="132" text-anchor="middle" font-family="Inter,sans-serif" font-weight="800" font-size="13" letter-spacing="2" fill="#111">NOIR</text>',
    'cup': '<path d="M58 60 H142 L130 184 H70 Z" style="fill:var(--pa)"/><path d="M58 60 H142 L130 184 H70 Z" fill="url(#gl)"/>'
           '<rect x="50" y="44" width="100" height="20" rx="8" fill="#f3efe7"/><rect x="62" y="30" width="76" height="18" rx="7" fill="#e6e0d4"/>'
           '<path d="M63 100 H137 L133 146 H67 Z" style="fill:var(--pb)"/><circle cx="100" cy="123" r="11" fill="rgba(255,255,255,.8)"/>',
    'phone': '<rect x="56" y="14" width="88" height="174" rx="22" fill="#121216"/><rect x="61" y="19" width="78" height="164" rx="18" style="fill:var(--pa)"/>'
             '<rect x="61" y="19" width="78" height="164" rx="18" fill="url(#gl)"/><rect x="86" y="26" width="28" height="8" rx="4" fill="#121216"/>'
             '<circle cx="100" cy="104" r="26" fill="rgba(255,255,255,.22)"/><circle cx="100" cy="104" r="14" style="fill:var(--pb)"/>',
}
GL = ('<defs><linearGradient id="gl" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".45"/>'
      '<stop offset=".45" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".28"/></linearGradient></defs>')
P = [  # product creatives: illustration, brand, title, old price, price, badge, bg c1→c2, text, product colours
    dict(prod='speaker', br='SOUNDO', t='Колонка Beat Mini', old='29 990 ₸', pr='24 990 ₸', bd='−18%', c1='#ff5a36', c2='#ffc3a6', ci='#1c0b05', pa='#e8412a', pb='#1c0b05'),
    dict(prod='headphones', br='AIRO', t='Наушники Air Pro', old='59 990 ₸', pr='44 990 ₸', bd='−25%', c1='#2446ff', c2='#9fb3ff', ci='#fff', pa='#101433', pb='#fff'),
    dict(prod='watch', br='PULSE', t='Смарт-часы Fit 3', old='39 990 ₸', pr='31 990 ₸', bd='−20%', c1='#0f7a55', c2='#9ff0c8', ci='#04140d', pa='#d8dde0', pb='#27e08a'),
    dict(prod='bottle', br='NOIR', t='Парфюм Noir 50 мл', old='42 000 ₸', pr='33 600 ₸', bd='−20%', c1='#e8a7c6', c2='#fff0f6', ci='#2a0717', pa='#c2185b', pb='#ffb3d1'),
    dict(prod='cup', br='BREW', t='Кофе с собой', old='1 200 ₸', pr='890 ₸', bd='−26%', c1='#ffd23f', c2='#fff4c2', ci='#1d1500', pa='#8a5a2b', pb='#1d1500'),
    dict(prod='phone', br='NOVA', t='Смартфон Nova X', old='189 990 ₸', pr='159 990 ₸', bd='−16%', c1='#16161c', c2='#4a4a5a', ci='#fff', pa='#6d5dfc', pb='#ffd23f'),
]


def cr(i, w=None, h=None, cls='', idattr=''):
    p = P[i % len(P)]
    size = f'width:{w}px;height:{h}px;' if w else ''
    return (f'<div class="cr {cls}"{idattr} style="--c1:{p["c1"]};--c2:{p["c2"]};--ci:{p["ci"]};--pa:{p["pa"]};--pb:{p["pb"]};{size}">'
            f'<div class="cr-in"><div class="cr-pic"><svg viewBox="0 0 200 200" aria-hidden="true">{GL}{PROD[p["prod"]]}</svg></div>'
            f'<div class="cr-tx"><span class="cr-br">{p["br"]}</span><b class="cr-t">{p["t"]}</b>'
            f'<span class="cr-p"><s>{p["old"]}</s> {p["pr"]}</span><span class="cr-cta">Купить</span></div>'
            f'<span class="cr-bd">{p["bd"]}</span></div></div>')


CR_CSS = """
.cr { container-type: size; position: relative; overflow: hidden; flex: none; border-radius: 10px; color: var(--ci); background: radial-gradient(130% 120% at 72% 28%, var(--c2), var(--c1)); font-family: 'Inter', sans-serif; text-align: left; }
.cr-in { --t: 8.5cqmin; position: absolute; inset: 0; display: grid; grid-template-rows: minmax(0, 1.25fr) auto; gap: 3cqmin; padding: 7cqmin; }
.cr-pic { display: grid; place-items: center; min-height: 0; min-width: 0; } .cr-pic svg { width: 100%; height: 100%; filter: drop-shadow(0 4cqmin 4cqmin rgba(0,0,0,.25)); }
.cr-tx { display: flex; flex-direction: column; justify-content: center; gap: 1.8cqmin; min-width: 0; }
.cr-br { font-size: calc(var(--t) * .42); font-weight: 700; letter-spacing: .16em; opacity: .7; }
.cr-t { font-size: var(--t); font-weight: 800; line-height: 1.02; letter-spacing: -.03em; }
.cr-p { font-size: calc(var(--t) * .62); font-weight: 700; } .cr-p s { font-weight: 500; opacity: .55; margin-right: .3em; }
.cr-cta { align-self: flex-start; margin-top: 1cqmin; padding: .55em 1.1em; border-radius: 99px; background: var(--ci); color: var(--c1); font-size: calc(var(--t) * .45); font-weight: 700; }
.cr-bd { position: absolute; top: 5cqmin; right: 5cqmin; padding: .35em .6em; border-radius: 6px; background: #fff; color: #111; font-size: calc(var(--t) * .55); font-weight: 800; }
@container (min-aspect-ratio: 13/10) { .cr-in { --t: 10cqmin; grid-template-rows: 1fr; grid-template-columns: minmax(0, .9fr) minmax(0, 1.1fr); padding: 6cqmin 8cqmin; } }
@container (min-aspect-ratio: 2/1) { .cr-in { --t: 15cqmin; grid-template-columns: auto minmax(0, 1fr) auto; align-items: center; gap: 6cqmin; } .cr-pic { height: 100%; aspect-ratio: 1; } .cr-bd { position: static; order: 3; } }
@container (min-aspect-ratio: 5/1) { .cr-in { --t: 30cqmin; padding: 8cqmin 4cqmin; grid-template-columns: auto minmax(0, 1fr) auto auto; } .cr-br, .cr-p s { display: none; } .cr-tx { flex-direction: row; align-items: center; gap: 4cqmin; } .cr-cta { margin: 0; } }
@container (max-aspect-ratio: 3/4) { .cr-in { --t: 10cqmin; grid-template-rows: minmax(0, 1.4fr) auto; padding: 9cqmin 8cqmin 10cqmin; } }
@container (max-height: 70px) { .cr-cta { display: none; } }
"""

# ---------------------------------------------------------------- base CSS (token-driven)
BASE = """
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; -webkit-text-size-adjust: 100%; }
body { background: var(--bg); color: var(--ink); font: 400 16px/1.55 var(--f); -webkit-font-smoothing: antialiased; overflow-x: clip; }
main { overflow-x: clip; }  /* decorative bleed (rotated tags, glows) never scrolls the page */
a { color: inherit; text-decoration: none; } img, svg { display: block; max-width: 100%; } button, input { font: inherit; color: inherit; }
.wrap { width: min(1200px, 100% - 48px); margin: 0 auto; } @media (max-width: 640px) { .wrap { width: calc(100% - 32px); } }
:focus-visible { outline: 2px solid var(--ac); outline-offset: 3px; }
.btn { display: inline-flex; align-items: center; justify-content: center; gap: 8px; height: 50px; padding: 0 24px; border: 0; border-radius: var(--br); font: 600 15px/1 var(--f); white-space: nowrap; cursor: pointer; transition: transform .2s, background .2s, box-shadow .2s, color .2s; }
.btn.p { background: var(--btn); color: var(--btn-ink); } .btn.s { background: transparent; color: var(--ink); box-shadow: inset 0 0 0 1.5px var(--line2); } .btn:hover { transform: translateY(-1px); }
.nav { position: sticky; top: 0; z-index: 50; background: color-mix(in srgb, var(--bg) 86%, transparent); backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px); border-bottom: 1px solid var(--line); }
.nav .wrap { display: flex; align-items: center; gap: 26px; height: 64px; font-size: 14px; }
.logo { display: flex; align-items: center; gap: 9px; font: 700 17px var(--d); letter-spacing: -.02em; white-space: nowrap; }
.nav nav { display: flex; gap: 22px; color: var(--muted); } .nav nav a:hover { color: var(--ink); } .nav .sp { flex: 1; }
.nav .lg { color: var(--muted); font-weight: 500; } .nav .lg:hover { color: var(--ink); } .nav .btn { height: 38px; padding: 0 16px; font-size: 14px; }
.burger { display: none; width: 44px; height: 44px; margin-right: -10px; flex: none; border: 0; background: none; color: var(--ink); cursor: pointer; place-items: center; align-content: center; gap: 6px; }
.burger i { display: block; width: 20px; height: 2px; background: currentColor; transition: transform .2s; }
.burger[aria-expanded="true"] i:first-child { transform: translateY(4px) rotate(45deg); } .burger[aria-expanded="true"] i:last-child { transform: translateY(-4px) rotate(-45deg); }
.mnav { position: fixed; left: 12px; right: 12px; top: 72px; z-index: 60; display: grid; gap: 2px; padding: 10px; background: var(--bg); border: 1px solid var(--line2); border-radius: var(--r); box-shadow: 0 30px 60px -20px rgba(0,0,0,.45); }
.mnav[hidden] { display: none; } .mnav a { padding: 13px 14px; border-radius: 10px; font-weight: 500; font-size: 16px; } .mnav a:hover { background: var(--card); }
.mnav .row { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 8px; } .mnav .row a { display: flex; justify-content: center; height: 48px; align-items: center; }
.mnav .row a.in { box-shadow: inset 0 0 0 1.5px var(--line2); }
@media (max-width: 1060px) { .nav nav { display: none; } .burger { display: grid; } }
@media (max-width: 640px) { .nav .lg { display: none; } .nav .wrap { gap: 12px; } }
@media (max-width: 360px) { .nav .btn.p { padding: 0 12px; font-size: 13px; } }
.eyebrow { display: inline-flex; align-items: center; gap: 10px; padding: 5px 14px 5px 5px; border-radius: 99px; box-shadow: inset 0 0 0 1px var(--line2); font-size: 13.5px; }
.eyebrow b { padding: 4px 10px; border-radius: 99px; background: var(--ac); color: var(--ac-ink); font-weight: 600; font-size: 12px; }
.sub { font-size: 18px; color: var(--ink2); } .acts { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 32px; } .tiny { margin-top: 14px; font: 400 12.5px var(--m); color: var(--muted); }
.logos { margin-top: 70px; } .logos p { text-align: center; font-size: 13px; color: var(--muted); }
.mq { overflow: hidden; margin-top: 18px; -webkit-mask-image: linear-gradient(90deg, transparent, #000 12%, #000 88%, transparent); mask-image: linear-gradient(90deg, transparent, #000 12%, #000 88%, transparent); }
.mq .t { display: flex; gap: 56px; width: max-content; animation: mq 40s linear infinite; } .mq span { font: 600 19px var(--d); color: var(--muted); white-space: nowrap; }
@keyframes mq { to { transform: translateX(-50%); } }
.sec { padding-top: 150px; } @media (max-width: 640px) { .sec { padding-top: 100px; } }
.sh { max-width: 780px; } .sh .k { font: 500 12px var(--m); letter-spacing: .1em; text-transform: uppercase; color: var(--ac); }
.sh h2 { margin-top: 14px; font: var(--dw) clamp(34px, 4.6vw, 64px)/1.02 var(--d); letter-spacing: var(--dl); } .sh h2 .gt { color: var(--ac); } .sh p { margin-top: 16px; font-size: 17px; color: var(--ink2); }
.card { background: var(--card); border-radius: var(--r); box-shadow: inset 0 0 0 1px var(--line); }
.bento { display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); gap: 14px; margin-top: 48px; } .bento .card { position: relative; overflow: hidden; padding: 28px; }
.b1, .b2 { grid-column: span 6; } .b3, .b4, .b5 { grid-column: span 4; }
.lb { font: 500 12px var(--m); letter-spacing: .08em; text-transform: uppercase; color: var(--muted); }
.big { margin-top: 16px; font: var(--dw) clamp(40px, 4.4vw, 62px)/1 var(--d); letter-spacing: var(--dl); color: var(--ac); }
.bento h3 { margin-top: 10px; font: 600 19px/1.25 var(--d); } .bento p { margin-top: 8px; font-size: 15px; color: var(--ink2); }
.bars { display: flex; align-items: flex-end; gap: 12px; height: 150px; margin-top: 26px; } .bars .c { flex: 1; align-self: stretch; display: flex; flex-direction: column-reverse; gap: 4px; }
.bars .n { background: var(--line2); border-radius: 6px; } .bars .y { background: var(--ac); border-radius: 6px; } .bars small { order: -1; margin-top: 8px; text-align: center; font: 400 11.5px var(--m); color: var(--muted); }
.cmp div { margin-top: 16px; font: 400 12.5px var(--m); color: var(--muted); } .cmp i { display: block; height: 10px; margin-top: 6px; border-radius: 99px; background: var(--line2); } .cmp .us i { width: 50%; background: var(--ac); }
.frames { display: flex; align-items: flex-end; gap: 8px; margin-top: 22px; } .frames i { border-radius: 4px; box-shadow: inset 0 0 0 1.5px var(--line2); }
.steps { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; margin-top: 48px; } .steps .card { padding: 28px; }
.steps .n { font: 500 13px var(--m); color: var(--ac); } .steps h3 { margin-top: 38px; font: 600 22px/1.2 var(--d); } .steps p { margin-top: 10px; color: var(--ink2); }
.steps .vis { margin-top: 22px; padding: 12px 14px; border-radius: 10px; background: color-mix(in srgb, var(--ink) 5%, transparent); font: 400 12.5px var(--m); color: var(--muted); }
.adapt { display: grid; grid-template-columns: 290px minmax(0, 1fr); gap: 14px; margin-top: 48px; } .tabs { display: grid; gap: 4px; align-content: start; padding: 10px; }
.tab { display: flex; justify-content: space-between; align-items: center; gap: 10px; padding: 12px 14px; border: 0; border-radius: 10px; background: none; color: var(--ink2); font: 500 15px var(--f); text-align: left; cursor: pointer; }
.tab small { font: 400 12px var(--m); color: var(--muted); } .tab:hover { background: color-mix(in srgb, var(--ink) 5%, transparent); } .tab.on { background: var(--ink); color: var(--bg); } .tab.on small { color: inherit; opacity: .7; }
.stage { position: relative; display: grid; place-items: center; min-height: 540px; overflow: hidden; background-image: radial-gradient(color-mix(in srgb, var(--ink) 14%, transparent) 1px, transparent 1.2px); background-size: 18px 18px; }
.stage .cr { transition: width .6s cubic-bezier(.7,0,.2,1), height .6s cubic-bezier(.7,0,.2,1); box-shadow: 0 30px 60px -30px rgba(0,0,0,.45); }
.dims { position: absolute; left: 18px; bottom: 16px; font: 500 13px var(--m); } .ex { position: absolute; right: 18px; bottom: 16px; font: 400 12px var(--m); color: var(--muted); }
.mods { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; margin-top: 48px; } .mods .card { padding: 26px; }
.mods .ic { display: grid; place-items: center; width: 44px; height: 44px; border-radius: 12px; background: color-mix(in srgb, var(--ac) 14%, transparent); color: var(--ac); } .mods .ic svg { width: 22px; height: 22px; }
.mods h3 { margin-top: 18px; font: 600 19px var(--d); } .mods p { margin-top: 8px; font-size: 15px; color: var(--ink2); }
.mods .o { display: inline-block; margin-top: 16px; padding: 6px 10px; border-radius: 8px; background: color-mix(in srgb, var(--ink) 5%, transparent); font: 400 12px var(--m); color: var(--muted); }
.gal { margin-top: 48px; overflow: hidden; } .gal .t { display: flex; align-items: center; gap: 18px; width: max-content; animation: mq 70s linear infinite; }
.gal figure { display: grid; gap: 10px; } .gal figcaption { font: 400 12px var(--m); color: var(--muted); }
.calc { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); margin-top: 48px; } .calc .l, .calc .r { padding: 38px; } .calc .r { border-left: 1px solid var(--line); }
.calc .v { margin: 14px 0 24px; font: var(--dw) clamp(52px, 6vw, 88px)/1 var(--d); letter-spacing: var(--dl); } .calc label { display: block; margin-top: 12px; font-size: 13px; color: var(--muted); }
input[type=range] { -webkit-appearance: none; appearance: none; width: 100%; height: 6px; border-radius: 99px; background: linear-gradient(90deg, var(--ac) var(--p, 30%), var(--line2) var(--p, 30%)); cursor: pointer; }
input[type=range]::-webkit-slider-thumb { -webkit-appearance: none; width: 26px; height: 26px; border-radius: 50%; background: var(--ink); box-shadow: 0 0 0 5px var(--bg), 0 0 0 6px var(--line2); }
input[type=range]::-moz-range-thumb { width: 24px; height: 24px; border: 0; border-radius: 50%; background: var(--ink); }
.row { display: flex; justify-content: space-between; align-items: baseline; gap: 12px; padding: 16px 0; border-bottom: 1px solid var(--line); } .row b { font: 600 24px var(--d); letter-spacing: -.02em; }
.row.s { border: 0; } .row.s b { font-size: 34px; color: var(--ac); }
.fnote { margin-top: 18px; font-size: 12.5px; color: var(--muted); }
.per { display: flex; justify-content: center; margin-top: 36px; } .per div { display: inline-flex; padding: 4px; border-radius: 99px; box-shadow: inset 0 0 0 1px var(--line2); }
.per button { padding: 9px 18px; border: 0; border-radius: 99px; background: none; cursor: pointer; font-weight: 500; font-size: 14px; } .per button.on { background: var(--ink); color: var(--bg); }
.per em { margin-left: 6px; font-style: normal; color: var(--ac); } .per button.on em { color: inherit; opacity: .8; }
.plans { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; margin-top: 26px; } .plan { position: relative; display: flex; flex-direction: column; padding: 30px; }
.plan h3 { font: 600 18px var(--d); } .plan .pr { margin: 16px 0 6px; font: var(--dw) 52px/1 var(--d); letter-spacing: var(--dl); } .plan .pr small { font: 400 15px var(--f); color: var(--muted); letter-spacing: 0; }
.plan > p { color: var(--ink2); font-size: 15px; } .plan ul { flex: 1; margin: 20px 0 26px; list-style: none; display: grid; gap: 10px; align-content: start; font-size: 15px; }
.plan li::before { content: '✓'; margin-right: 10px; color: var(--ac); font-weight: 700; } .plan .btn { width: 100%; }
.plan.hot { box-shadow: inset 0 0 0 2px var(--ac); } .pop { position: absolute; top: 18px; right: 18px; padding: 4px 10px; border-radius: 99px; background: var(--ac); color: var(--ac-ink); font: 600 12px var(--f); }
.faq { max-width: 820px; margin-top: 40px; } .faq details { border-bottom: 1px solid var(--line); } .faq summary { list-style: none; display: flex; justify-content: space-between; gap: 16px; padding: 22px 0; font: 600 19px var(--d); cursor: pointer; }
.faq summary::-webkit-details-marker { display: none; } .faq summary::after { content: '+'; color: var(--muted); font-weight: 400; transition: transform .2s; } .faq details[open] summary::after { transform: rotate(45deg); }
.faq details p { padding-bottom: 22px; color: var(--ink2); max-width: 680px; }
.end { margin-top: 150px; padding: 110px 0; text-align: center; border-top: 1px solid var(--line); } .end h2 { font: var(--dw) clamp(44px, 7vw, 108px)/.96 var(--d); letter-spacing: var(--dl); } .end h2 .gt { color: var(--ac); }
.end p { max-width: 600px; margin: 22px auto 0; color: var(--ink2); font-size: 17px; } .end .acts { justify-content: center; }
footer { padding: 30px 0 40px; border-top: 1px solid var(--line); font-size: 14px; color: var(--muted); } footer .wrap { display: flex; flex-wrap: wrap; gap: 14px 24px; justify-content: space-between; } footer nav { display: flex; gap: 20px; }
.js .rv { opacity: 0; transform: translateY(18px); transition: opacity .7s cubic-bezier(.2,.7,.2,1), transform .7s cubic-bezier(.2,.7,.2,1); } .js .rv.in { opacity: 1; transform: none; }
@media (max-width: 1060px) { .b1, .b2 { grid-column: span 12; } .b3, .b4, .b5 { grid-column: span 4; } .adapt { grid-template-columns: minmax(0, 1fr); } .tabs { grid-template-columns: repeat(4, minmax(0, 1fr)); } .mods { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (max-width: 760px) { .b3, .b4, .b5 { grid-column: span 12; } .steps, .plans, .mods { grid-template-columns: minmax(0, 1fr); } .calc { grid-template-columns: minmax(0, 1fr); } .calc .r { border-left: 0; border-top: 1px solid var(--line); } .calc .l, .calc .r { padding: 26px; }
  .tabs { grid-template-columns: repeat(2, minmax(0, 1fr)); } .tab { padding: 10px 12px; font-size: 14px; } .stage { min-height: 400px; } .end { padding: 80px 0; margin-top: 110px; } .sub { font-size: 17px; } }
@media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation-duration: .001ms !important; animation-iteration-count: 1 !important; transition-duration: .001ms !important; scroll-behavior: auto !important; } .js .rv { opacity: 1; transform: none; } }
""" + CR_CSS

ICONS = [
    '<circle cx="5" cy="5" r="2.5"/><circle cx="19" cy="12" r="2.5"/><circle cx="5" cy="19" r="2.5"/><path d="M7.5 5h3a5 5 0 015 5M7.5 19h3a5 5 0 005-5"/>',
    '<rect x="3" y="3" width="8" height="14" rx="2"/><rect x="13" y="7" width="8" height="10" rx="2"/><path d="M3 21h18"/>',
    '<path d="M5 19c2-6 6-12 14-14-1 8-7 12-13 15z"/><path d="M9 15l-3-3"/>',
    '<path d="M6 3h9l4 4v14H6z"/><path d="M9 11h7M9 15h7M9 7h3"/>',
    '<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
    '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    '<path d="M9 18V5l11-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="17" cy="16" r="3"/>',
    '<path d="M3 4h18l-7 8v6l-4 2v-8z"/>',
    '<circle cx="8" cy="8" r="3.5"/><circle cx="17" cy="10" r="2.5"/><path d="M2 20c0-3.5 3-6 6-6s6 2.5 6 6M14 20c0-2.5 1.5-4.5 3-4.5s4 1.5 4 4.5"/>',
]
MODS = [('Нодовый холст', 'Цепочки генераций; «Запустить пайплайн» проходит всю схему сам.', 'фото → видео → форматы'),
        ('Адаптация', 'Любой размер и пресеты Kaspi, GDN, Discovery, РСЯ, BYYD.', '1 визуал → N размеров'),
        ('One Launch', 'Карточки маркетплейса и рекламные баннеры по шаблонам.', 'фото → карточки'),
        ('Copywrite engine', 'Посты, описания, контент-планы; отдаёт готовые документы.', 'DOCX · XLSX · PPTX'),
        ('TRENDSWATCHING', 'Тренды TikTok, Instagram и Threads — и почему они сработали.', 'тренд → сценарий'),
        ('Creative Predictor', 'Сравнение креативов до запуска рекламы.', 'креатив → разбор'),
        ('Музыка и голос', 'Трек по описанию стиля или озвучка нужным голосом.', 'текст → аудио'),
        ('Стратегия', 'Воронка, бюджет и план — и схема под нужный креатив.', 'бриф → план'),
        ('Соавторы', 'Пригласите коллегу по почте и общайтесь в чате внутри.', 'email → контакт')]
FAQ = [('Что значит «бюджет не сгорает»?', 'Неиспользованный за месяц бюджет переходит на следующий месяц и складывается с новым.'),
       ('Почему генерация до 50% дешевле?', 'Вы платите за генерации по ценам моделей — без наценок посредников и без подписки на каждый сервис.'),
       ('Что делает ассистент?', 'Разбирает нишу, готовит промпты и собирает цепочку нод под задачу. Вы проверяете схему и нажимаете «Запустить».'),
       ('Какие размеры поддерживает адаптация?', 'Любые — от Stories 9:16 до баннеров 728×90, плюс пресеты Kaspi, GDN, Discovery, РСЯ и BYYD.')]
NAV = [('#why', 'Преимущества'), ('#sizes', 'Адаптация'), ('#modules', 'Модули'), ('#calc', 'Экономия'), ('#pricing', 'Тарифы')]
BURGER = '<button class="burger" type="button" aria-label="Открыть меню" aria-expanded="false" aria-controls="mnav"><i></i><i></i></button>'


def nav(logo):
    links = ''.join(f'<a href="{h}">{t}</a>' for h, t in NAV)
    return (f'<header class="nav"><div class="wrap"><a class="logo" href="#top" aria-label="ONEFLOW — наверх">{logo}</a><nav aria-label="Разделы">{links}</nav><span class="sp"></span>'
            f'<a class="lg" data-app="login" href="{APP}">Войти</a>{reg("Регистрация")}{BURGER}</div></header>'
            f'<nav class="mnav" id="mnav" aria-label="Меню" hidden>{links}<a href="#faq">Вопросы</a>'
            f'<div class="row"><a class="in" data-app="login" href="{APP}">Войти</a>{reg("Регистрация")}</div></nav>')


def logos():
    s = ''.join(f'<span>{m}</span>' for m in MODELS)
    return f'<div class="logos"><p>Работает на лучших моделях — без отдельных подписок</p><div class="mq" aria-hidden="true"><div class="t">{s}{s}</div></div></div>'


def sections(stage_prod=0):
    bars = ''.join(f'<div class="c"><small>{m}</small><span class="n" style="height:36%"></span>' + (f'<span class="y" style="height:{y}%"></span>' if y else '') + '</div>'
                   for m, y in (('июл', 0), ('авг', 14), ('сен', 28), ('окт', 44)))
    why = (f'<section class="sec" id="why"><div class="wrap"><div class="sh rv"><span class="k">Экономия</span><h2>Один счёт <span class="gt">вместо пяти</span></h2>'
           '<p>Все модели на одном балансе. Бюджет не сгорает в конце месяца, а переходит дальше.</p></div><div class="bento">'
           f'<article class="card b1 rv"><span class="lb">баланс</span><div class="big">Не сгорает</div><h3>бюджет в конце месяца</h3><p>Остаток переходит на следующий месяц и складывается с новым.</p><div class="bars" aria-hidden="true">{bars}</div></article>'
           '<article class="card b2 rv"><span class="lb">цена</span><div class="big">−50%</div><h3>к цене генерации*</h3><p>Те же модели — без наценок посредников и без подписки на каждый сервис.</p><div class="cmp" aria-hidden="true"><div>Отдельные сервисы<i></i></div><div class="us">ONEFLOW<i></i></div></div></article>'
           '<article class="card b3 rv"><span class="lb">кабинеты</span><div class="big">7</div><h3>пресетов + любой W×H</h3><div class="frames" aria-hidden="true"><i style="width:30px;height:54px"></i><i style="width:44px;height:54px"></i><i style="width:80px;height:42px"></i><i style="width:96px;height:28px"></i></div></article>'
           '<article class="card b4 rv"><span class="lb">модели</span><div class="big">30+</div><h3>нейросетей на одном балансе</h3><p>Фото, видео, тексты, музыка и голос — без пяти подписок.</p></article>'
           '<article class="card b5 rv"><span class="lb">окно</span><div class="big">9</div><h3>модулей в одном окне</h3><p>От нодового холста до Creative Predictor и соавторов.</p></article>'
           f'</div><p class="fnote">{FOOT}</p></div></section>')
    how = ('<section class="sec" id="how"><div class="wrap"><div class="sh rv"><span class="k">Пара кликов</span><h2>От фото до кампании</h2></div><div class="steps">'
           '<article class="card rv"><span class="n">01 · клик</span><h3>Загрузите фото или идею</h3><p>Товар, референс или пара строк — этого достаточно.</p><div class="vis">фото · идея · референс</div></article>'
           '<article class="card rv"><span class="n">02 · ассистент</span><h3>Ассистент соберёт цепочку</h3><p>Разберёт нишу, подготовит промпты и схему нод — вы проверяете.</p><div class="vis">ниша → промпты → ноды</div></article>'
           '<article class="card rv"><span class="n">03 · клик</span><h3>Запустите — и всё готово</h3><p>Креативы для Kaspi, Яндекс, Google, BYYD и Stories одним запуском.</p><div class="vis">1080×1920 · 1200×628 · 1125×330</div></article>'
           '</div></div></section>')
    tabs = ''.join(f'<button type="button" class="tab{" on" if i == 0 else ""}" data-w="{w}" data-h="{h}">{n}<small>{w}×{h}</small></button>' for i, (n, w, h) in enumerate(PRESETS))
    pv = cr(stage_prod, 200, 356, idattr=' id="pv"')
    sizes = ('<section class="sec" id="sizes"><div class="wrap"><div class="sh rv"><span class="k">Рекламные кабинеты</span><h2>Под каждый рекламный кабинет</h2>'
             '<p>Kaspi, Яндекс РСЯ, Google, BYYD, Stories — все размеры одним кликом: макет перестраивается, товар остаётся целым.</p></div>'
             f'<div class="adapt rv"><div class="tabs card" id="tabs" role="group" aria-label="Формат">{tabs}</div>'
             f'<div class="stage card" id="stage">{pv}<span class="dims" id="dims">1080 × 1920</span><span class="ex">макет — пример</span></div></div></div></section>')
    mods = ''.join(f'<article class="card rv"><span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[i]}</svg></span><h3>{t}</h3><p>{d}</p><span class="o">{o}</span></article>'
                   for i, (t, d, o) in enumerate(MODS))
    modules = f'<section class="sec" id="modules"><div class="wrap"><div class="sh rv"><span class="k">Модули</span><h2>9 инструментов — одно окно</h2><p>То, что обычно живёт в разных вкладках и подписках.</p></div><div class="mods">{mods}</div></div></section>'
    figs = ''.join(f'<figure>{cr(i, round(w * k), round(h * k))}<figcaption>{n} · {w}×{h} · пример</figcaption></figure>'
                   for i, (n, w, h, k) in enumerate([('Stories', 1080, 1920, .15), ('Kaspi', 1125, 330, .4), ('BYYD', 300, 250, .9), ('Discovery', 1200, 628, .3),
                                                     ('GDN', 300, 600, .48), ('Яндекс РСЯ', 1080, 450, .34), ('Discovery', 960, 1200, .23), ('Свой', 728, 90, .6)]))
    gal = (f'<section class="sec" aria-label="Примеры креативов"><div class="wrap"><div class="sh rv"><span class="k">Результаты</span><h2>Одно фото — все форматы</h2>'
           f'<p>Так выглядят креативы после адаптации: товар целый, макет под каждый кабинет.</p></div></div><div class="gal" aria-hidden="true"><div class="t">{figs}{figs}</div></div></section>')
    calc = ('<section class="sec" id="calc"><div class="wrap"><div class="sh rv"><span class="k">Калькулятор</span><h2>Посчитайте экономию</h2></div>'
            '<div class="calc card rv"><div class="l"><span class="lb">Бюджет на генерации в месяц</span><div class="v" id="rv">$300</div>'
            '<input type="range" id="budget" min="20" max="1000" step="10" value="300" aria-label="Бюджет на генерации в месяц"><label for="budget">Передвиньте ползунок</label></div>'
            '<div class="r"><div class="row"><span>Сейчас за год</span><b id="now">$3 600</b></div><div class="row"><span>В ONEFLOW за год</span><b id="us">от $1 800</b></div>'
            f'<div class="row s"><span>Экономия до</span><b id="sv">$1 800</b></div><p class="fnote">{FOOT}</p></div></div></div></section>')
    plans = ('<section class="sec" id="pricing"><div class="wrap"><div class="sh rv"><span class="k">Тарифы</span><h2>Бюджет не сгорает в конце месяца</h2>'
             '<p>На любом тарифе неизрасходованный баланс переходит на следующий месяц.</p></div>'
             '<div class="per"><div role="group" aria-label="Период оплаты"><button type="button" class="on" id="pm" aria-pressed="true">Месяц</button><button type="button" id="py" aria-pressed="false">Год<em>−20%</em></button></div></div>'
             '<div class="plans"><article class="card plan rv"><h3>Бесплатный</h3><div class="pr">$0</div><p>Попробовать и понять, подходит ли вам.</p><ul><li>Доступ к ONEFLOW</li><li>Бюджет — по желанию</li><li>30+ нейросетей</li><li>ИИ-ассистент</li></ul>' + reg('Начать', 'btn s') + '</article>'
             '<article class="card plan rv hot"><span class="pop">Популярный</span><h3>Популярный</h3><div class="pr"><span data-m="60" data-y="48">$60</span><small> / мес</small></div><p>Для регулярной работы с генерацией.</p><ul><li>Всё из бесплатного</li><li>LLM-модели</li><li>Адаптация визуалов</li><li>One Launch</li></ul>' + reg('Выбрать') + '</article>'
             '<article class="card plan rv"><h3>Максимальный</h3><div class="pr"><span data-m="200" data-y="160">$200</span><small> / мес</small></div><p>Для команд без ограничений.</p><ul><li>Всё из популярного</li><li>Creative Predictor</li><li>Приоритетная поддержка</li></ul>' + reg('Выбрать', 'btn s') + '</article></div></div></section>')
    faq = ''.join(f'<details{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(FAQ))
    faq = f'<section class="sec" id="faq"><div class="wrap"><div class="sh rv"><span class="k">FAQ</span><h2>Частые вопросы</h2></div><div class="faq">{faq}</div></div></section>'
    return logos(), why + how + sizes + modules + gal + calc + plans + faq


def end(h2):
    return (f'<section class="end"><div class="wrap"><h2>{h2}</h2><p>Креативы для всех рекламных кабинетов в пару кликов. Генерация до 50% дешевле*, бюджет не сгорает в конце месяца.</p>'
            f'<div class="acts">{reg()}<a class="btn s" href="#pricing">Смотреть тарифы</a></div></div></section>')


FOOTER = '<footer><div class="wrap"><span>© 2026 ONEFLOW</span><nav aria-label="Документы"><a href="#">Конфиденциальность</a><a href="#">Условия</a><a href="#">Возврат</a></nav></div></footer>'

JS = """<script>
(function () {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const APP_URL = '__APP__';
  document.querySelectorAll('[data-app]').forEach((a) => { a.href = APP_URL + (a.dataset.app === 'register' ? '__REG__' : ''); });
  const money = (n) => '$' + Math.round(n).toLocaleString('ru-RU');
  const r = document.getElementById('budget');
  if (r) { const up = () => { const v = +r.value; r.style.setProperty('--p', ((v - r.min) / (r.max - r.min) * 100) + '%');
      document.getElementById('rv').textContent = money(v); document.getElementById('now').textContent = money(v * 12);
      document.getElementById('us').textContent = 'от ' + money(v * 6); document.getElementById('sv').textContent = money(v * 6);
      document.dispatchEvent(new CustomEvent('budget', { detail: v })); }; r.addEventListener('input', up); up(); }
  const pm = document.getElementById('pm'), py = document.getElementById('py');
  if (pm && py) { const set = (k) => { pm.classList.toggle('on', k === 'm'); py.classList.toggle('on', k === 'y'); pm.setAttribute('aria-pressed', k === 'm'); py.setAttribute('aria-pressed', k === 'y');
      document.querySelectorAll('[data-m]').forEach((e) => { e.textContent = '$' + e.dataset[k]; }); }; pm.onclick = () => set('m'); py.onclick = () => set('y'); }
  const tabs = [...document.querySelectorAll('#tabs .tab')], st = document.getElementById('stage'), pv = document.getElementById('pv'), dims = document.getElementById('dims');
  if (pv && st) { let i = 0, timer;
    const show = (k) => { i = k; tabs.forEach((t, j) => { t.classList.toggle('on', j === k); t.setAttribute('aria-pressed', j === k); });
      const w = +tabs[k].dataset.w, h = +tabs[k].dataset.h, s = Math.min((st.clientWidth - 60) / w, (st.clientHeight - 90) / h);
      pv.style.width = Math.round(w * s) + 'px'; pv.style.height = Math.round(h * s) + 'px'; dims.textContent = w + ' × ' + h; };
    const auto = () => { clearInterval(timer); if (!reduce) timer = setInterval(() => show((i + 1) % tabs.length), 2600); };
    tabs.forEach((t, k) => t.addEventListener('click', () => { show(k); clearInterval(timer); })); addEventListener('resize', () => show(i)); show(0); auto(); }
  const b = document.querySelector('.burger'), m = document.getElementById('mnav');
  if (b && m) { const set = (o) => { m.hidden = !o; b.setAttribute('aria-expanded', o); b.setAttribute('aria-label', o ? 'Закрыть меню' : 'Открыть меню'); };
    b.addEventListener('click', () => set(m.hidden)); m.addEventListener('click', (e) => { if (e.target.closest('a')) set(false); });
    addEventListener('keydown', (e) => { if (e.key === 'Escape' && !m.hidden) { set(false); b.focus(); } }); addEventListener('resize', () => { if (getComputedStyle(b).display === 'none') set(false); }); }
  const els = document.querySelectorAll('.rv');
  if (!('IntersectionObserver' in window) || reduce) els.forEach((e) => e.classList.add('in'));
  else { const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { threshold: .08 }); els.forEach((e) => io.observe(e)); }
})();
</script>
""".replace('__APP__', APP).replace('__REG__', REG)


def page(path, title, tokens, css, logo, hero, end_h2, *, stage_prod=0, js='', body_cls='', theme='#ffffff', desc=None):
    lg, secs = sections(stage_prod)
    hero = hero.replace('{LOGOS}', lg)
    html = ('<!doctype html>\n<html lang="ru">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<title>{title}</title>\n<meta name="description" content="{desc or SUB}">\n<meta name="theme-color" content="{theme}">\n'
            "<script>document.documentElement.classList.add('js')</script>\n"
            '<link rel="stylesheet" href="fonts.css">\n'
            f'<style>\n:root {{ {tokens} }}\n{BASE}\n{css}\n</style>\n</head>\n'
            f'<body id="top"{f" class={chr(34)}{body_cls}{chr(34)}" if body_cls else ""}>\n{nav(logo)}\n<main id="main">{hero}{secs}{end(end_h2)}</main>\n{FOOTER}\n{JS}{js}</body>\n</html>\n')
    open(os.path.join(HERE, path), 'w', encoding='utf-8').write(html)
    return path
