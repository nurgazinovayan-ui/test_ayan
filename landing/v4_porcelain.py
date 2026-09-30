"""Variant 4 · Porcelain — rebuilt from the delivered production screenshot (sources were lost on a container restart).

Soft porcelain light page: pastel blobs, glass hero panel (One Launch bunny card adapted to 9:16, Discovery, РСЯ, Kaspi),
three budget cards, three steps, 8 modules, «Для бизнеса» templates (before/after SVG illustrations), HoReCa & SMB
comparison, honest AI assistant, One Launch gallery, pricing, FAQ, closing card. Product images: app's One Launch templates.
Images are CSS custom properties (one url each), so the single-file build stores every picture once.
"""
import os

import protos

HERE = os.path.dirname(os.path.abspath(__file__))
APP, REG = '/app', '?auth=register'  # same domain: oneflow.art → landing, oneflow.art/app → app
MARK = ('<svg viewBox="0 0 76 52" aria-hidden="true"><path fill="currentColor" d="M17 0C18.66 0 20 1.34 20 3V14C20 15.1 20.9 16 22 16H32C33.66 16 35 17.34 35 19V30C35 31.1 35.9 32 37 32H38C39.1 32 40 31.1 40 30V19C40 17.34 41.34 16 43 16H57C58.66 16 60 17.34 60 19V30C60 31.1 60.9 32 62 32H73C74.66 32 76 33.34 76 35V49C76 50.66 74.66 52 73 52H59C57.34 52 56 50.66 56 49V38C56 36.9 55.1 36 54 36H51C49.9 36 49 36.9 49 38V49C49 50.66 47.66 52 46 52H32C30.34 52 29 50.66 29 49V38C29 36.9 28.1 36 27 36H24C22.9 36 22 36.9 22 38V49C22 50.66 20.66 52 19 52H5C3.34 52 2 50.66 2 49V35C2 33.34 3.34 32 5 32H13C14.1 32 15 31.1 15 30V22C15 20.9 14.1 20 13 20H3C1.34 20 0 18.66 0 17V3C0 1.34 1.34 0 3 0H17Z"/></svg>')
IMGS = ['bunny', 'pajama', 'coffee', 'body', 'blender', 'pyramid', 'airbuds', 'hoodie', 'watch', 'speaker', 'robot', 'airfryer', 'powerbank', 'toothbrush']
ALT = {'bunny': 'Мягкий зайка', 'pajama': 'Пижама детская', 'coffee': 'Кофемашина Aroma One', 'body': 'Боди для малыша', 'blender': 'Блендер Mix Pro 1200', 'pyramid': 'Деревянная пирамидка',
       'airbuds': 'Наушники Airbuds X1', 'hoodie': 'Худи детское', 'watch': 'Смарт-часы Time X5', 'speaker': 'Колонка Beatbox Mini', 'robot': 'Робот-пылесос Cleanbot S7',
       'airfryer': 'Аэрогриль Crisp Chef 8L', 'powerbank': 'Повербанк Energy Max', 'toothbrush': 'Зубная щётка Smile Care'}


def reg(label='Начать бесплатно', cls='btn p'):
    return f'<a class="{cls}" data-app="register" href="{APP}{REG}">{label}</a>'


# ---------------------------------------------------------------- business template illustrations (symbols, used many times)
SYM = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<symbol id="s-food" viewBox="0 0 200 150"><ellipse cx="100" cy="84" rx="58" ry="56" fill="rgba(0,0,0,.18)"/><circle cx="100" cy="78" r="56" fill="#fdfdfb"/><circle cx="100" cy="78" r="46" fill="#f4efe4"/>
<path d="M62 66a40 40 0 0 1 36-26v38z" fill="#fbfaf6"/><g fill="#ff8a5c"><rect x="96" y="44" width="14" height="12" rx="2"/><rect x="112" y="52" width="13" height="12" rx="2"/><rect x="99" y="58" width="12" height="11" rx="2"/><rect x="116" y="66" width="12" height="11" rx="2"/></g>
<g fill="#8cc152"><path d="M70 92c10-10 24-10 34 0-10 5-24 5-34 0z"/><path d="M74 102c9-7 21-7 30 0-9 4-21 4-30 0z"/></g><g fill="#6fbf4a"><circle cx="118" cy="92" r="5"/><circle cx="128" cy="98" r="5"/><circle cx="112" cy="102" r="5"/><circle cx="124" cy="108" r="4.5"/></g>
<g fill="#9b5fc0"><path d="M84 108c6 8 16 12 24 12-2-8-10-14-24-12z"/></g><g fill="#fff"><circle cx="76" cy="72" r="1.5"/><circle cx="84" cy="64" r="1.5"/><circle cx="90" cy="72" r="1.5"/></g>
<g stroke="#c89b5d" stroke-width="4" stroke-linecap="round"><path d="M128 30l34-22"/><path d="M134 36l32-20"/></g></symbol>
<symbol id="s-room" viewBox="0 0 200 150"><rect width="200" height="150" fill="currentColor"/><rect y="112" width="200" height="38" fill="rgba(0,0,0,.08)"/><rect x="138" y="18" width="46" height="58" rx="2" fill="rgba(255,255,255,.55)"/>
<rect x="24" y="30" width="30" height="36" rx="2" fill="none" stroke="#6b5b4b" stroke-width="3"/><path d="M28 60l8-10 6 6 6-8 4 12z" fill="#b89f84"/>
<rect x="40" y="78" width="96" height="34" rx="10" fill="#8fa896"/><rect x="34" y="88" width="16" height="30" rx="7" fill="#7f9886"/><rect x="126" y="88" width="16" height="30" rx="7" fill="#7f9886"/>
<rect x="48" y="84" width="38" height="18" rx="6" fill="#a5bcaa"/><rect x="90" y="84" width="38" height="18" rx="6" fill="#a5bcaa"/><rect x="46" y="116" width="4" height="8" fill="#5b4a3a"/><rect x="126" y="116" width="4" height="8" fill="#5b4a3a"/>
<path d="M158 58h20l-6 14h-8z" fill="#e8d7b8"/><rect x="167" y="72" width="2" height="44" fill="#6b5b4b"/><rect x="160" y="114" width="16" height="4" rx="2" fill="#6b5b4b"/>
<path d="M150 118c0-10 4-14 4-14s4 4 4 14z" fill="#6f9a5a"/><rect x="146" y="116" width="16" height="10" rx="2" fill="#c7b299"/></symbol>
<symbol id="s-car" viewBox="0 0 200 150"><ellipse cx="100" cy="118" rx="84" ry="8" fill="rgba(0,0,0,.2)"/>
<path d="M18 104c0-12 6-20 18-22l26-4 22-18c6-5 14-7 22-7h28c9 0 16 3 22 9l16 16 18 4c8 2 12 8 12 16v6c0 3-2 5-5 5H23c-3 0-5-2-5-5z" fill="currentColor"/>
<path d="M70 76l18-14c4-3 9-5 15-5h11v19z" fill="rgba(255,255,255,.7)"/><path d="M120 57h8c7 0 12 2 16 7l10 12h-34z" fill="rgba(255,255,255,.7)"/>
<path d="M22 92h160" stroke="rgba(255,255,255,.35)" stroke-width="2"/><rect x="170" y="88" width="10" height="5" rx="2" fill="#ffe9a8"/>
<circle cx="56" cy="110" r="16" fill="#1c1c20"/><circle cx="56" cy="110" r="8" fill="#c9ccd2"/><circle cx="150" cy="110" r="16" fill="#1c1c20"/><circle cx="150" cy="110" r="8" fill="#c9ccd2"/></symbol>
<symbol id="s-spk" viewBox="0 0 200 150"><ellipse cx="100" cy="134" rx="36" ry="6" fill="rgba(0,0,0,.2)"/><rect x="72" y="22" width="56" height="112" rx="26" fill="currentColor"/>
<rect x="72" y="22" width="56" height="112" rx="26" fill="url(#gl4)"/><g fill="rgba(0,0,0,.28)"><circle cx="90" cy="60" r="2.2"/><circle cx="100" cy="60" r="2.2"/><circle cx="110" cy="60" r="2.2"/><circle cx="90" cy="70" r="2.2"/><circle cx="100" cy="70" r="2.2"/><circle cx="110" cy="70" r="2.2"/><circle cx="90" cy="80" r="2.2"/><circle cx="100" cy="80" r="2.2"/><circle cx="110" cy="80" r="2.2"/><circle cx="90" cy="90" r="2.2"/><circle cx="100" cy="90" r="2.2"/><circle cx="110" cy="90" r="2.2"/></g>
<rect x="92" y="34" width="16" height="4" rx="2" fill="rgba(255,255,255,.6)"/><rect x="94" y="112" width="12" height="3" rx="1.5" fill="rgba(255,255,255,.5)"/></symbol>
<linearGradient id="gl4" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".35"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".25"/></linearGradient>
</defs></svg>'''


def ba(key, before='Ваше фото', after='Шаблон'):
    s = {'food': 's-food', 'room': 's-room', 'car': 's-car', 'spk': 's-spk'}[key]
    return (f'<div class="ba"><figure class="bp b-{key}"><svg viewBox="0 0 200 150" aria-hidden="true"><use href="#{s}"/></svg><figcaption>{before}</figcaption></figure>'
            f'<figure class="ap a-{key}"><svg viewBox="0 0 200 150" aria-hidden="true"><use href="#{s}"/></svg><figcaption>{after}</figcaption></figure></div>')


TPL = [('food', 'Рестораны и кафе', 'Фото блюд на белом фоне', 'Для меню, доставки и соцсетей — прямо со снимка на кухне.', 'HoReCa'),
       ('room', 'Риелторы', 'Интерьер в стиле журнала', 'Светлые каталожные фото квартир для объявлений.', 'Квартира'),
       ('car', 'Автодилеры', 'Профессиональное авто-фото', 'Машина как у фотографа — на той же локации.', 'Авто'),
       ('spk', 'Электроника', 'Товар в стиле каталога', 'Техника на белом фоне для карточек и сайта.', 'Техника')]
VS = [('Организация', 'договориться, дождаться свободной даты', 'открыть шаблон — сразу'), ('Сколько ждать', 'дни на съёмку и обработку', 'минуты'),
      ('Новые позиции', 'новая съёмка за отдельные деньги', 'ещё одно фото в тот же день'), ('Размеры', 'кадрировать под каждую площадку', 'любой размер одной кнопкой'),
      ('Бюджет', 'разовые траты на каждую съёмку', 'один баланс, остаток не сгорает')]
FAQ = [('Есть ли шаблоны для моей ниши?', 'Да, в разделе «Для бизнеса»: HoReCa для ресторанов и кафе, Квартира для риелторов, Авто для автодилеров, Техника для магазинов электроники, а также Мебель. Выберите шаблон, загрузите своё фото — получите студийный снимок в высоком разрешении.'),
       ('Нужно ли заказывать фотографа?', 'Для большинства задач — нет: меню и доставка, объявления о продаже авто и квартир, карточки товаров. Снимите на телефон, выберите шаблон — и получите студийное качество без выезда фотографа и аренды студии.'),
       ('Что умеет ИИ-ассистент?', 'Разбирает нишу и подсказывает идеи, пишет и улучшает промпты, а по описанию задачи собирает схему нод на холсте. Запуск пайплайна и финальные решения — за вами.'),
       ('Что значит «бюджет не сгорает»?', 'Неиспользованный за месяц бюджет переходит на следующий месяц и складывается с новым.'),
       ('Почему генерация до 50% дешевле?', 'Вы платите за генерации по ценам моделей — без наценок посредников и без подписки на каждый сервис. Итог зависит от моделей и объёма.'),
       ('Какие размеры поддерживает адаптация?', 'Любые — от сторис 9:16 до баннера 728×90, плюс пресеты Kaspi, GDN, Discovery, Яндекс РСЯ и BYYD.'),
       ('Можно ли работать командой?', 'Да — пригласите соавтора по почте и общайтесь во встроенном мессенджере.')]
NAV = [('#why', 'Преимущества'), ('#business', 'Для бизнеса'), ('#assistant', 'Ассистент'), ('#pricing', 'Цены'), ('#faq', 'Вопросы')]
NICHES = ['магазина на Kaspi', 'вашей кофейни', 'бренда одежды', 'салона красоты', 'вашего стартапа', 'вашего бизнеса']  # hero headline rotates through these (entrepreneur niches)
KLING_5S = 0.084 * 5          # $ per 5-second Kling 3.0 Standard clip, 720p, no audio (OpenRouter)
NBP_1K = 0.067                # $ per 1K Nano Banana Pro image (price confirmed by ONEFLOW)
GPTI_1K = 0.04174             # $ per 1K GPT Image 2.5 image, Sunburst (price confirmed by ONEFLOW)


def gens(budget):
    """Approximate monthly generations for a plan budget; model names shown, the specs live behind the «?»."""
    n = lambda x: f'{int(budget // x):,}'.replace(',', '\u2009')  # noqa: E731
    row = lambda cnt, what, model, tip, top=False: (f'<li{" class=hastop" if top else ""}><span><b>≈ {cnt}</b> {what}</span><span class="nw">'
                                                   f'{"<i class=top>TOP</i>" if top else ""}{model}<span class="qm" tabindex="0" role="note" aria-label="{tip}" data-tip="{tip}">?</span></span></li>')  # noqa: E731
    return ('<div class="gens"><span>Примерно генераций в месяц</span><ul>'
            + row(n(KLING_5S), 'видео', 'Kling 3.0', 'Ролик 5 с, 720p, без звука')
            + row(n(NBP_1K), 'фото', 'Nano Banana Pro', 'Изображение 1K')
            + row(n(GPTI_1K), 'фото', 'GPT Image 2.5', 'Изображение 1K · Sunburst', top=True) + '</ul></div>')


MODELS = ['GPT Image', 'Nano Banana Pro', 'Seedream', 'Veo 3.1', 'Kling', 'Seedance', 'Hailuo', 'Recraft', 'Flux', '+ ещё 20']

CSS = """
:root { --bg: #f7f7fa; --ink: #111114; --ink2: #3c3c46; --muted: #80808c; --line: rgba(17,17,20,.08); --card: #ffffff; --ac: #111114; --mint: #e8f8f0; --green: #16a36a;
  --sh: 0 1px 2px rgba(16,16,24,.04), 0 18px 44px -22px rgba(16,16,40,.2); --sh2: 0 1px 2px rgba(16,16,24,.05), 0 40px 80px -36px rgba(16,16,40,.32);
  --d: 'Onest', sans-serif; --m: 'JetBrains Mono', monospace; --e: cubic-bezier(.2,.7,.2,1); IMGVARS }
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; -webkit-text-size-adjust: 100%; } body { background: var(--bg); color: var(--ink); font: 400 16px/1.55 var(--d); -webkit-font-smoothing: antialiased; }
main { overflow-x: clip; } a { color: inherit; text-decoration: none; } img, svg { display: block; max-width: 100%; } button { font: inherit; color: inherit; }
:focus-visible { outline: 2px solid #3b6cff; outline-offset: 3px; }
.wrap { width: min(1120px, 100% - 48px); margin: 0 auto; } @media (max-width: 640px) { .wrap { width: calc(100% - 32px); } }
.skip { position: absolute; left: 12px; top: -60px; z-index: 100; padding: 10px 14px; border-radius: 10px; background: var(--ink); color: #fff; } .skip:focus { top: 12px; }
.btn { display: inline-flex; align-items: center; justify-content: center; gap: 8px; height: 48px; padding: 0 24px; border: 0; border-radius: 12px; font: 600 15px/1 var(--d); white-space: nowrap; cursor: pointer; transition: transform .25s var(--e), box-shadow .25s; }
.btn.p { background: var(--ink); color: #fff; box-shadow: 0 10px 24px -10px rgba(17,17,20,.55); } .btn.g { background: rgba(255,255,255,.75); box-shadow: inset 0 0 0 1px var(--line), 0 6px 18px -10px rgba(17,17,20,.25); backdrop-filter: blur(10px); }
.btn:hover { transform: translateY(-1px); }
/* nav */
.nav { position: sticky; top: 12px; z-index: 50; margin-top: 12px; transition: opacity .35s var(--e), translate .35s var(--e), visibility .35s; } .nav.gone { opacity: 0; translate: 0 -14px; visibility: hidden; pointer-events: none; }
.totop { position: fixed; right: 20px; bottom: 20px; z-index: 55; display: grid; place-items: center; width: 48px; height: 48px; border: 0; border-radius: 12px; background: var(--ink); color: #fff; font-size: 20px; cursor: pointer; box-shadow: 0 12px 30px -10px rgba(17,17,20,.55); opacity: 0; translate: 0 12px; visibility: hidden; transition: opacity .3s var(--e), translate .3s var(--e), visibility .3s; } .totop.on { opacity: 1; translate: 0 0; visibility: visible; } .totop:hover { translate: 0 -2px; }
@media (max-width: 640px) { .totop { right: 16px; bottom: 16px; width: 44px; height: 44px; } } .nav .in { display: flex; align-items: center; gap: 26px; height: 60px; padding: 0 10px 0 22px; border-radius: 20px; background: transparent; }
.logo { display: flex; align-items: center; gap: 9px; font: 700 16px var(--d); letter-spacing: -.01em; } .logo svg { width: 22px; height: 16px; }
.nav nav { display: flex; gap: 24px; font-size: 14px; color: var(--muted); } .nav nav a:hover { color: var(--ink); } .nav .sp { flex: 1; }
.nav .lg { font-size: 14px; font-weight: 500; } .nav .btn { height: 40px; padding: 0 18px; font-size: 14px; border-radius: 10px; }
.burger { display: none; width: 44px; height: 44px; border: 0; background: none; cursor: pointer; place-items: center; align-content: center; gap: 6px; }
.burger i { display: block; width: 20px; height: 2px; background: currentColor; transition: transform .2s; } .burger[aria-expanded="true"] i:first-child { transform: translateY(4px) rotate(45deg); } .burger[aria-expanded="true"] i:last-child { transform: translateY(-4px) rotate(-45deg); }
.mnav { position: fixed; left: 12px; right: 12px; top: 84px; z-index: 60; display: grid; gap: 2px; padding: 10px; border-radius: 20px; background: rgba(255,255,255,.96); backdrop-filter: blur(18px); box-shadow: var(--sh2); }
.mnav[hidden] { display: none; } .mnav a { padding: 13px 14px; border-radius: 12px; font-weight: 500; font-size: 16px; } .mnav a:hover { background: var(--bg); }
.mnav .row { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 8px; } .mnav .row a { display: flex; align-items: center; justify-content: center; height: 48px; } .mnav .row .in2 { box-shadow: inset 0 0 0 1px var(--line); border-radius: 12px; }
@media (max-width: 960px) { .nav nav { display: none; } .burger { display: grid; } } @media (max-width: 560px) { .nav .lg { display: none; } .nav .in { gap: 10px; padding-left: 16px; } .nav .btn { padding: 0 14px; } }
/* hero */
.hero { position: relative; padding: 70px 0 0; text-align: center; } .blob { position: absolute; z-index: -1; border-radius: 50%; filter: blur(70px); opacity: .75; pointer-events: none; }
.blob.a { width: 520px; height: 420px; left: -8%; top: 40px; background: #dccfff; } .blob.b { width: 520px; height: 440px; right: -8%; top: 120px; background: #c9f2de; } .blob.c { width: 560px; height: 380px; left: 30%; top: 560px; background: #ffe3cf; }
.bgfx { position: fixed; inset: 0; z-index: -1; overflow: hidden; pointer-events: none; }
.bgfx i { position: absolute; border-radius: 50%; filter: blur(80px); opacity: .62; will-change: transform; animation: drift var(--t) ease-in-out infinite alternate; }
.bgfx .a { --t: 22s; width: 46vw; height: 40vw; left: -12vw; top: -8vw; background: #dccfff; } .bgfx .b { --t: 28s; width: 44vw; height: 42vw; right: -12vw; top: 12vh; background: #c9f2de; animation-delay: -9s; }
.bgfx .c { --t: 25s; width: 48vw; height: 36vw; left: 24vw; bottom: -16vw; background: #ffe3cf; animation-delay: -15s; } .bgfx .d { --t: 32s; width: 30vw; height: 30vw; left: 38vw; top: 26vh; background: #d7e6ff; opacity: .45; animation-delay: -4s; }
@keyframes drift { 0% { transform: translate(0, 0) scale(1); } 33% { transform: translate(7vw, 6vh) scale(1.1); } 66% { transform: translate(-5vw, 10vh) scale(.92); } 100% { transform: translate(4vw, -6vh) scale(1.06); } }
@media (max-width: 760px) { .bgfx i { filter: blur(60px); } .bgfx .a { width: 80vw; height: 70vw; } .bgfx .b { width: 80vw; height: 76vw; } .bgfx .c { width: 90vw; height: 70vw; } .bgfx .d { width: 60vw; height: 60vw; } }
.pill { display: inline-flex; align-items: center; gap: 10px; padding: 5px 14px 5px 5px; border-radius: 99px; background: rgba(255,255,255,.75); font-size: 13.5px; color: var(--ink2); transition: background .2s; }
.pill b { padding: 3px 9px; border-radius: 99px; background: var(--ink); color: #fff; font-size: 11.5px; font-weight: 600; } .pill:hover { background: #fff; }
.hero h1 { margin-top: 26px; font: 700 clamp(44px, 6.6vw, 92px)/1 var(--d); letter-spacing: -.05em; } .hero h1 .gr { display: block; background: linear-gradient(95deg, #111114 30%, #3e6d63 70%, #5c5f9a); -webkit-background-clip: text; background-clip: text; color: transparent; }
.rot { position: relative; display: block; height: 1.1em; overflow: hidden; font-size: min(1em, 8.4vw); }
.rw { position: absolute; left: 0; right: 0; top: 0; white-space: nowrap; transform: translateY(105%); opacity: 0; transition: transform .6s var(--e), opacity .5s var(--e); }
.rw.on { transform: none; opacity: 1; } .rw.out { transform: translateY(-105%); opacity: 0; }
@media (prefers-reduced-motion: reduce) { .rw { transition: none; } }
@media (max-width: 760px) { .hero h1 { font-size: 9.4vw; } .rot { font-size: 1em; } }
.hero .sub { max-width: 560px; margin: 24px auto 0; font-size: 18px; color: var(--ink2); } .acts { display: flex; flex-wrap: wrap; justify-content: center; gap: 12px; margin-top: 32px; }
.hvid { position: relative; max-width: 1100px; margin: 56px auto 0; aspect-ratio: 16 / 9; overflow: hidden; border-radius: 26px; background: #f3f3f8;
  box-shadow: inset 0 0 0 1px rgba(255,255,255,.9), var(--sh2); }
.hvid video { display: block; width: 100%; height: 100%; object-fit: cover; pointer-events: none; }
.hvid video::-webkit-media-controls, .hvid video::-webkit-media-controls-start-playback-button { display: none !important; -webkit-appearance: none; }
@media (max-width: 760px) { .hvid { margin-top: 36px; border-radius: 18px; } }
.tiny { margin-top: 16px; font: 400 12.5px var(--m); color: var(--muted); }
.panel { position: relative; margin: 70px auto 0; padding: 34px; border-radius: 30px; background: rgba(255,255,255,.62); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: inset 0 0 0 1px rgba(255,255,255,.9), var(--sh2); text-align: left; }
.pg { display: grid; grid-template-columns: 260px 90px minmax(0, 1fr); align-items: center; gap: 10px; }
.src { overflow: hidden; border-radius: 18px; background: #fff; box-shadow: var(--sh); } .src img { width: 100%; height: auto; aspect-ratio: 3 / 4; object-fit: cover; }
.src figcaption { display: flex; justify-content: space-between; padding: 12px 14px; font-size: 13px; } .src figcaption span:last-child { font: 400 12px var(--m); color: var(--muted); }
.arr { display: grid; justify-items: center; gap: 8px; font: 400 11.5px var(--m); color: var(--muted); } .arr i { width: 60px; height: 2px; background: repeating-linear-gradient(90deg, #b8b8c4 0 5px, transparent 5px 9px); position: relative; }
.arr i::after { content: ''; position: absolute; right: -2px; top: -4px; width: 8px; height: 8px; border-top: 2px solid #b8b8c4; border-right: 2px solid #b8b8c4; rotate: 45deg; }
.fmts { display: grid; grid-template-columns: .42fr 1fr 1fr; grid-template-rows: auto auto; gap: 12px; }
.fm { position: relative; overflow: hidden; border-radius: 14px; background: #eee; box-shadow: var(--sh); opacity: 0; animation: fin .6s var(--e) forwards; }
.fm::before { content: ''; position: absolute; inset: -20px; background: var(--img-bunny) center / cover; filter: blur(16px) saturate(1.1); opacity: .9; }
.fm .ft { position: absolute; inset: 0; background: var(--img-bunny) center / contain no-repeat; } .fm .lb { position: absolute; left: 8px; bottom: 8px; padding: 4px 8px; border-radius: 8px; background: rgba(255,255,255,.88); font: 500 11px var(--m); color: var(--ink); }
.f916 { grid-row: 1 / 3; } .fdis { aspect-ratio: 1200 / 628; animation-delay: .25s; } .frsy { aspect-ratio: 1080 / 450; align-self: end; animation-delay: .4s; } .fksp { grid-column: 2 / 4; aspect-ratio: 1125 / 330; animation-delay: .55s; } .f916 { animation-delay: .1s; }
@keyframes fin { from { opacity: 0; transform: translateY(10px) scale(.97); } to { opacity: 1; transform: none; } }
.chip { position: absolute; display: flex; align-items: center; gap: 10px; padding: 9px 14px 9px 9px; border-radius: 16px; background: rgba(255,255,255,.9); box-shadow: var(--sh); animation: flo 5s ease-in-out infinite; }
.chip i { display: grid; place-items: center; width: 30px; height: 30px; border-radius: 10px; font-style: normal; font-size: 14px; } .chip small { display: block; font-size: 11px; color: var(--muted); } .chip b { font: 700 14px var(--d); }
.chip.c1 { left: -20px; top: -26px; } .chip.c1 i { background: var(--mint); color: var(--green); } .chip.c2 { right: -20px; top: -26px; animation-delay: -1.6s; } .chip.c2 i { background: #efeaff; color: #7c5cff; }
.chip.c3 { left: 50%; bottom: -26px; translate: -50% 0; animation-delay: -3s; } .chip.c3 i { background: #fff0e6; color: #ff7a45; } @keyframes flo { 50% { transform: translateY(-6px); } }
.models { margin-top: 64px; overflow: hidden; -webkit-mask-image: linear-gradient(90deg, transparent, #000 20%, #000 80%, transparent); mask-image: linear-gradient(90deg, transparent, #000 20%, #000 80%, transparent); }
.models .t { display: flex; width: max-content; animation: mq 32s linear infinite; } .models:hover .t { animation-play-state: paused; }
.models span { margin-right: 52px; font: 700 21px var(--d); letter-spacing: -.02em; color: #26262e; white-space: nowrap; }
@media (max-width: 640px) { .models span { margin-right: 36px; font-size: 17px; } .models { -webkit-mask-image: linear-gradient(90deg, transparent, #000 14%, #000 86%, transparent); mask-image: linear-gradient(90deg, transparent, #000 14%, #000 86%, transparent); } }
/* sections */
.sec { padding-top: 130px; } .sh { max-width: 900px; margin: 0 auto; text-align: center; } .sh p { max-width: 640px; margin-left: auto; margin-right: auto; } .sh .k { font: 700 11.5px var(--d); letter-spacing: .14em; text-transform: uppercase; color: var(--muted); }
.sh h2 { margin-top: 12px; font: 700 clamp(32px, 4vw, 48px)/1.08 var(--d); letter-spacing: -.04em; } .sh p { margin-top: 14px; color: var(--ink2); font-size: 16.5px; }
.card { background: var(--card); border-radius: 24px; box-shadow: var(--sh); }
.three { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; margin-top: 48px; } .three .card { position: relative; overflow: hidden; display: flex; flex-direction: column; padding: 28px; }
.three .card::before { content: ''; position: absolute; inset: 0 0 auto; height: 160px; background: linear-gradient(180deg, var(--tint), transparent); pointer-events: none; }
.three .big { position: relative; font: 700 56px/1 var(--d); letter-spacing: -.05em; } .three h3 { position: relative; margin-top: 10px; font: 600 16px var(--d); } .three p { position: relative; margin-top: 8px; font-size: 14.5px; color: var(--muted); }
.three .viz { flex: 1; display: grid; align-items: end; margin-top: 22px; min-height: 130px; } .three .cap { margin-top: 18px; font: 400 11px var(--m); letter-spacing: .06em; text-transform: uppercase; color: var(--muted); }
.ring { justify-self: center; position: relative; width: 120px; height: 120px; border-radius: 50%; background: conic-gradient(var(--green) calc(var(--v, 0) * 1%), #e6f3ec 0); transition: --v 1.4s var(--e); display: grid; place-items: center; }
.ring::before { content: ''; position: absolute; inset: 12px; border-radius: 50%; background: #fff; } .ring span { position: relative; text-align: center; font: 700 20px var(--d); } .ring small { display: block; font: 400 10px var(--m); color: var(--muted); }
@property --v { syntax: '<number>'; inherits: false; initial-value: 0; } .in .ring { --v: 72; }
.cmp div { display: flex; justify-content: space-between; font-size: 12.5px; color: var(--muted); } .cmp div b { color: var(--ink); font-weight: 600; } .cmp i { display: block; height: 10px; margin: 6px 0 14px; border-radius: 99px; }
.cmp .bx { background: repeating-linear-gradient(135deg, #e3e3ea 0 6px, #f0f0f5 6px 12px); } .cmp .by { width: 0; background: linear-gradient(90deg, #111114, #4a4a55); transition: width 1.2s var(--e) .3s; } .in .cmp .by { width: 50%; }
.frames { display: flex; align-items: flex-end; gap: 8px; } .frames span { display: grid; place-items: center; border-radius: 6px; box-shadow: inset 0 0 0 1.5px #d9d9e2; font: 500 10px var(--m); color: var(--muted); background: #fff; }
.steps { position: relative; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 30px; margin-top: 56px; text-align: center; }
.steps::before { content: ''; position: absolute; left: 16%; right: 16%; top: 22px; height: 2px; background: repeating-linear-gradient(90deg, #d9d9e2 0 6px, transparent 6px 12px); }
.steps .n { position: relative; display: grid; place-items: center; width: 46px; height: 46px; margin: 0 auto; border-radius: 50%; background: #fff; box-shadow: var(--sh); font: 500 13px var(--m); }
.steps h3 { margin-top: 18px; font: 600 17px var(--d); } .steps p { max-width: 280px; margin: 8px auto 0; font-size: 14.5px; color: var(--muted); }
.mods { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 14px; margin-top: 48px; } .mods .card { padding: 22px; transition: transform .3s var(--e), box-shadow .3s; } .mods .card:hover { transform: translateY(-3px); box-shadow: var(--sh2); }
.mods .ic { display: grid; place-items: center; width: 38px; height: 38px; border-radius: 12px; background: color-mix(in srgb, var(--c) 13%, #fff); color: var(--c); } .mods .ic svg { width: 19px; height: 19px; }
.mods { align-items: start; } .mod { padding: 0 !important; } .mod.open { box-shadow: var(--sh2); } .mods .card.open:hover { transform: none; }
.mod .mh { display: block; width: 100%; padding: 22px; border: 0; border-radius: 24px; background: none; text-align: left; cursor: pointer; }
.mod .t { display: block; margin-top: 16px; font: 600 16px var(--d); } .mod .d { display: block; margin-top: 6px; font-size: 14px; color: var(--muted); }
.mod .more { display: inline-flex; align-items: center; gap: 6px; margin-top: 14px; font: 600 12.5px var(--d); color: var(--c); } .mod .more i { font-style: normal; font-size: 15px; transition: transform .3s var(--e); } .mod.open .more i { transform: rotate(45deg); }
.mx { display: grid; grid-template-rows: 0fr; transition: grid-template-rows .45s var(--e); } .mod.open .mx { grid-template-rows: 1fr; }
.mxi { min-height: 0; overflow: hidden; visibility: hidden; transition: visibility 0s .45s; } .mod.open .mxi { visibility: visible; transition-delay: 0s; }
.exs { display: grid; gap: 8px; margin: 0 22px 22px; padding-top: 14px; border-top: 1px dashed #e3e3ea; font-size: 13px; }
.flow { display: flex; flex-wrap: wrap; align-items: center; gap: 6px; } .flow span { padding: 5px 9px; border-radius: 8px; background: color-mix(in srgb, var(--c) 10%, #fff); font-size: 12.5px; font-weight: 500; } .flow i { color: var(--muted); font-style: normal; }
.exn { color: var(--muted); font-size: 12.5px; line-height: 1.45; } .exl { justify-self: end; font: 500 10.5px var(--m); letter-spacing: .06em; text-transform: uppercase; color: var(--muted); }
.th { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 6px; } .th span { aspect-ratio: 3 / 4; border-radius: 8px; background: center / cover; box-shadow: var(--sh); }
.li { list-style: none; display: grid; gap: 6px; } .li li { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 2px 8px; padding: 8px 10px; border-radius: 10px; background: var(--bg); }
.li b { font-size: 12.5px; font-weight: 600; } .li small { width: 100%; font-size: 11.5px; color: var(--muted); } .li em { padding: 2px 6px; border-radius: 6px; background: color-mix(in srgb, var(--c) 12%, #fff); color: var(--c); font: 500 10.5px var(--m); font-style: normal; }
.sc, .fn { display: grid; grid-template-columns: 64px minmax(0, 1fr) 30px; align-items: center; gap: 8px; font-size: 12.5px; } .sc i, .fn i { position: relative; height: 8px; overflow: hidden; border-radius: 99px; background: #ececf1; }
.sc i::after, .fn i::after { content: ''; position: absolute; inset: 0 auto 0 0; width: 0; border-radius: 99px; background: var(--c); transition: width .9s var(--e) .2s; } .mod.open .sc i::after, .mod.open .fn i::after { width: var(--w); } .sc b, .fn b { text-align: right; font-weight: 600; }
.wave { display: flex; align-items: center; gap: 3px; height: 34px; } .wave i { flex: 1; border-radius: 2px; background: var(--c); opacity: .7; }
.inv { display: flex; justify-content: space-between; align-items: center; gap: 8px; padding: 6px 6px 6px 12px; border-radius: 12px; background: var(--bg); font-size: 12.5px; color: var(--muted); }
.inv b { padding: 6px 10px; border-radius: 8px; background: var(--ink); color: #fff; font-size: 12px; font-weight: 600; } .msg { justify-self: start; padding: 8px 12px; border-radius: 12px 12px 12px 4px; background: color-mix(in srgb, var(--c) 10%, #fff); font-size: 12.5px; } .msg b { display: block; font-size: 11.5px; color: var(--c); }
@media (max-width: 760px) { .mod.open { grid-column: 1 / -1; } }
/* business */
.tpl { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 14px; margin-top: 48px; } .tpl .card { overflow: hidden; padding: 10px; }
.ba { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; } .ba figure { position: relative; overflow: hidden; border-radius: 14px; aspect-ratio: 4 / 5; }
.ba svg { position: absolute; inset: 0; width: 100%; height: 100%; } .ba figcaption { position: absolute; left: 7px; bottom: 7px; padding: 3px 8px; border-radius: 99px; background: rgba(17,17,20,.82); color: #fff; font: 500 10.5px var(--d); }
.bp svg { filter: saturate(.35) brightness(.72) contrast(.9) blur(.3px); } .b-food { background: radial-gradient(circle at 50% 45%, #6b4a33, #3b2618); } .a-food { background: radial-gradient(circle at 50% 40%, #fff, #eef0f2); }
.b-room { background: #8d8e84; color: #b9b5a8; } .a-room { background: #f1f2ec; color: #eceee6; } .b-car { background: linear-gradient(#9a9ca0, #7d7f83); color: #6d7076; } .a-car { background: linear-gradient(#d7e7ff, #f6f9ff 70%); color: #1f4fd6; }
.b-spk { background: #77787a; color: #34405a; } .a-spk { background: radial-gradient(circle at 50% 40%, #fff, #eceef2); color: #2f5fb3; } .b-food svg, .a-food svg { padding: 6%; }
.tpl .tx { padding: 16px 10px 12px; } .tpl .tn { font: 500 10.5px var(--m); letter-spacing: .1em; text-transform: uppercase; color: var(--muted); } .tpl h3 { margin-top: 8px; font: 600 16px/1.25 var(--d); } .tpl p { margin-top: 6px; font-size: 13.5px; color: var(--muted); }
.how3 { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; margin-top: 14px; } .how3 .card { display: flex; align-items: center; gap: 14px; padding: 16px 18px; border-radius: 18px; }
.how3 .n { display: grid; place-items: center; flex: none; width: 34px; height: 34px; border-radius: 50%; background: var(--ink); color: #fff; font: 600 13px var(--d); } .how3 b { display: block; font-size: 14.5px; } .how3 small { font-size: 13px; color: var(--muted); }
.note { margin-top: 18px; text-align: center; font-size: 12.5px; color: var(--muted); }
.hr { display: grid; grid-template-columns: minmax(0, .9fr) minmax(0, 1.1fr); gap: 16px; margin-top: 48px; align-items: start; }
.food2 { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; } .food2 figure { position: relative; overflow: hidden; border-radius: 20px; aspect-ratio: 1; box-shadow: var(--sh); } .food2 svg { position: absolute; inset: 0; width: 100%; height: 100%; padding: 8%; }
.food2 figcaption { position: absolute; left: 10px; bottom: 10px; padding: 4px 10px; border-radius: 99px; background: rgba(17,17,20,.82); color: #fff; font: 500 11.5px var(--d); } .food2 .bp svg { filter: saturate(.35) brightness(.72) contrast(.9); }
.menu { margin-top: 12px; padding: 18px 20px 8px; } .menu .mh { display: flex; justify-content: space-between; font-weight: 600; } .menu .mh span { font: 400 12px var(--m); color: var(--muted); }
.mi { display: flex; align-items: center; gap: 14px; padding: 12px 0; border-top: 1px solid var(--line); } .mi:first-of-type { margin-top: 10px; } .mi svg { width: 40px; height: 40px; flex: none; border-radius: 50%; background: #fff; box-shadow: var(--sh); }
.mi b { display: block; font-size: 14.5px; font-weight: 600; } .mi small { font-size: 12.5px; color: var(--muted); } .mi em { margin-left: auto; font: 600 14px var(--d); font-style: normal; }
.vs { overflow: hidden; } .vs table { width: 100%; border-collapse: collapse; font-size: 14px; } .vs th, .vs td { padding: 14px 16px; text-align: left; vertical-align: top; border-bottom: 1px solid var(--line); }
.vs th { font-weight: 600; font-size: 13px; } .vs th:last-child { background: var(--ink); color: #fff; } .vs td:first-child { font-weight: 600; width: 28%; } .vs td:nth-child(2) { color: var(--muted); } .vs td:last-child { background: var(--mint); font-weight: 600; } .vs tr:last-child td { border: 0; }
.who3 { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; margin-top: 12px; } .who3 .card { padding: 16px; border-radius: 18px; } .who3 b { display: block; font-size: 14px; } .who3 small { font-size: 12.5px; color: var(--muted); }
/* assistant */
.as { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 16px; margin-top: 48px; align-items: start; }
.chat { padding: 22px; } .chat .ch { display: flex; justify-content: space-between; font: 500 12px var(--m); color: var(--muted); } .chat .me { margin: 14px 0 0 auto; max-width: 88%; padding: 12px 16px; border-radius: 16px 16px 4px 16px; background: var(--ink); color: #fff; font-size: 14px; }
.chat .ai { margin-top: 16px; font-size: 14px; } .chat .ai h4 { margin-top: 14px; font: 500 11.5px var(--m); color: var(--muted); letter-spacing: .06em; text-transform: uppercase; } .chat ul { margin: 6px 0 0 18px; } .chat li { margin-top: 3px; }
.chat .pr { margin-top: 6px; padding: 12px 14px; border-radius: 12px; background: var(--bg); font: 400 13px/1.5 var(--m); } .chat .nodes { display: flex; flex-wrap: wrap; align-items: center; gap: 8px; margin-top: 8px; font-size: 13px; }
.chat .nodes span { padding: 6px 12px; border-radius: 10px; background: #fff; box-shadow: inset 0 0 0 1px var(--line); font-weight: 500; } .chat .nodes i { color: var(--muted); font-style: normal; }
.chat .ft { display: flex; justify-content: space-between; align-items: center; gap: 12px; margin-top: 20px; padding-top: 16px; border-top: 1px solid var(--line); font-size: 13px; color: var(--muted); }
.chat .run { padding: 10px 16px; border-radius: 9px; background: var(--ink); color: #fff; font-weight: 600; font-size: 13px; white-space: nowrap; }
.as4 { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; } .as4 .card { padding: 20px; border-radius: 20px; } .as4 .n { font: 500 11.5px var(--m); color: var(--muted); } .as4 h3 { margin-top: 10px; font: 600 16px var(--d); }
.as4 p { margin-top: 6px; font-size: 13.5px; color: var(--muted); } .as4 .w { display: inline-block; margin-top: 14px; font: 500 11px var(--m); letter-spacing: .06em; text-transform: uppercase; color: var(--muted); }
.as4 .you { background: var(--ink); color: #fff; } .as4 .you p, .as4 .you .n, .as4 .you .w { color: rgba(255,255,255,.7); }
/* gallery */
.gal { margin-top: 44px; overflow: hidden; -webkit-mask-image: linear-gradient(90deg, transparent, #000 8%, #000 92%, transparent); mask-image: linear-gradient(90deg, transparent, #000 8%, #000 92%, transparent); }
.gal .t { display: flex; gap: 16px; width: max-content; animation: mq 80s linear infinite; } .gal .t > div { flex: none; width: 220px; aspect-ratio: 3 / 4; border-radius: 18px; background: center / cover; box-shadow: var(--sh); } @keyframes mq { to { transform: translateX(-50%); } }
/* pricing */
.per { display: flex; justify-content: center; margin-top: 32px; } .per div { display: inline-flex; gap: 4px; padding: 4px; border-radius: 12px; background: #fff; box-shadow: var(--sh); }
.per button { padding: 8px 16px; border: 0; border-radius: 9px; background: none; cursor: pointer; font-weight: 500; font-size: 14px; } .per button.on { background: var(--ink); color: #fff; } .per em { margin-left: 6px; padding: 1px 6px; border-radius: 6px; background: var(--mint); color: var(--green); font-style: normal; font-size: 12px; }
.plans { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px; margin-top: 26px; align-items: center; }
@media (max-width: 1100px) { .plans { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
.gens { margin: 16px 0 0; padding: 12px 14px; border-radius: 14px; background: rgba(17,17,20,.04); font-size: 13.5px; } .gens > span { font: 400 11.5px var(--m); color: var(--muted); }
.gens ul { margin: 8px 0 0 !important; gap: 6px !important; font-size: 13.5px !important; } .gens li::before { display: none; } .gens b { font-weight: 700; } .gens li { display: flex; justify-content: space-between; align-items: center; gap: 8px; white-space: nowrap; } .gens .nw { position: relative; font-size: 12.5px; color: var(--muted); }
.gens .top { position: absolute; right: 21px; top: -8px; padding: 0 3px; border-radius: 2px; background: var(--ink); color: #fff; font: 700 7.5px/10px var(--d); font-style: normal; letter-spacing: .06em; }
.plan.hot .gens .top { background: #fff; color: var(--ink); }
.plan.hot .gens .nw { color: rgba(255,255,255,.7); }
.qm { position: relative; display: inline-grid; place-items: center; width: 16px; height: 16px; margin-left: 6px; border-radius: 50%; background: rgba(17,17,20,.1); color: var(--ink);
  font: 700 10.5px var(--d); vertical-align: 1px; cursor: help; outline: none; }
.qm::after { content: attr(data-tip); position: absolute; left: 50%; bottom: calc(100% + 8px); z-index: 5; padding: 7px 10px; border-radius: 8px; background: #111114; color: #fff;
  font: 500 12px var(--d); white-space: nowrap; opacity: 0; pointer-events: none; transform: translate(-50%, 4px); transition: opacity .15s, transform .15s; }
.qm:hover::after, .qm:focus::after { opacity: 1; transform: translate(-50%, 0); }
.plan.hot .gens { background: rgba(255,255,255,.1); } .plan.hot .qm { background: rgba(255,255,255,.22); color: #fff; } .plan.hot .gens > span { color: rgba(255,255,255,.65); }
.plan.hot .qm::after { background: #fff; color: #111114; } .plan { display: flex; flex-direction: column; padding: 28px; border-radius: 26px; }
.plan h3 { font: 600 16px var(--d); } .plan .pr .dp { display: inline-block; padding: 10px 16px; border-radius: 14px; background: rgba(59,92,255,.1); color: #3b5cff; font: 700 26px/1 var(--d); letter-spacing: -.03em; } .plan .pr { margin: 14px 0 6px; font: 700 50px/1 var(--d); letter-spacing: -.05em; } .plan .pr small { font: 400 14px var(--d); letter-spacing: 0; color: var(--muted); }
.plan > p { font-size: 14px; color: var(--muted); } .plan ul { margin: 18px 0 24px; list-style: none; display: grid; gap: 9px; font-size: 14.5px; } .plan li::before { content: '•'; margin-right: 10px; color: var(--muted); }
.plan .btn { width: 100%; } .plan .btn.w { background: #fff; color: var(--ink); box-shadow: inset 0 0 0 1px var(--line); }
.plan.hot { padding: 36px 28px; background: var(--ink); color: #fff; box-shadow: 0 40px 70px -30px rgba(17,17,20,.6); } .plan.hot > p, .plan.hot .pr small, .plan.hot li::before { color: rgba(255,255,255,.65); }
.plan.hot .btn { background: #fff; color: var(--ink); } .plan .pop { align-self: flex-start; margin-bottom: 12px; padding: 3px 10px; border-radius: 99px; background: #efeaff; color: #5b3fd6; font-size: 11.5px; font-weight: 600; }
/* faq + end */
.faq { max-width: 740px; margin: 40px auto 0; display: grid; gap: 10px; } .faq details { border-radius: 18px; background: #fff; box-shadow: var(--sh); }
.faq summary { list-style: none; display: flex; justify-content: space-between; gap: 16px; padding: 18px 22px; font-weight: 600; font-size: 15.5px; cursor: pointer; } .faq summary::-webkit-details-marker { display: none; }
.faq summary::after { content: '+'; color: var(--muted); font-weight: 400; transition: transform .2s; } .faq details[open] summary::after { transform: rotate(45deg); } .faq details p { padding: 0 22px 18px; font-size: 14.5px; color: var(--ink2); }
.end { margin-top: 130px; padding: 90px 30px; border-radius: 34px; background: #fff; box-shadow: var(--sh2); text-align: center; } .end h2 { font: 700 clamp(36px, 5.2vw, 64px)/1.04 var(--d); letter-spacing: -.045em; }
.end p { max-width: 460px; margin: 18px auto 0; color: var(--muted); } .end .acts { margin-top: 28px; }
footer { margin-top: 90px; padding: 26px 0 36px; border-top: 1px solid var(--line); font-size: 13.5px; color: var(--muted); } footer .wrap { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 14px 24px; }
footer .l { display: flex; align-items: center; gap: 14px; } footer .logo { color: var(--ink); } footer nav { display: flex; gap: 20px; } footer nav a:hover, footer nav button:hover { color: var(--ink); }
footer nav button { border: 0; background: none; font: inherit; color: inherit; cursor: pointer; }
dialog.doc { width: min(680px, calc(100% - 24px)); max-height: min(80vh, 760px); margin: auto; padding: 0; border: 0; border-radius: 24px; background: #fff; color: var(--ink); box-shadow: var(--sh2); }
dialog.doc::backdrop { background: rgba(17,17,20,.35); backdrop-filter: blur(6px); } dialog.doc .in2 { padding: 34px 32px 30px; } dialog.doc h1 { font: 700 26px/1.2 var(--d); letter-spacing: -.03em; }
dialog.doc h2 { margin: 20px 0 6px; font: 600 16px var(--d); } dialog.doc p, dialog.doc li { font-size: 14.5px; color: var(--ink2); } dialog.doc .updated { margin-top: 6px; font-size: 12.5px; color: var(--muted); }
.sup { margin-top: 28px; text-align: center; color: var(--muted); } .sup .btn { margin-left: 10px; }
.sf { display: grid; gap: 14px; margin-top: 18px; } .sf label { display: grid; gap: 6px; font-size: 13px; color: var(--muted); }
.sf input, .sf textarea { width: 100%; padding: 11px 13px; border: 1px solid var(--line); border-radius: 12px; background: var(--bg); color: var(--ink); font: inherit; font-size: 15px; outline: none; }
.sf input:focus, .sf textarea:focus { border-color: var(--ink); } .sf textarea { min-height: 130px; resize: vertical; } .sf .hp { position: absolute; left: -9999px; }
.sf .btn { justify-self: start; } .sf .st { min-height: 20px; font-size: 13.5px; color: var(--ink2); }
dialog.doc .x { position: sticky; top: 0; float: right; width: 40px; height: 40px; margin: 12px 12px 0 0; border: 0; border-radius: 50%; background: var(--bg); font-size: 20px; cursor: pointer; }
.js .rv { opacity: 0; transform: translateY(18px); transition: opacity .8s var(--e), transform .8s var(--e); } .js .rv.in { opacity: 1; transform: none; }
@media (max-width: 1000px) { .pg { grid-template-columns: 200px 60px minmax(0, 1fr); } .mods, .tpl { grid-template-columns: repeat(2, minmax(0, 1fr)); } .hr, .as { grid-template-columns: minmax(0, 1fr); } }
@media (max-width: 760px) { .panel { display: flex; flex-direction: column; padding: 20px; border-radius: 24px; } .chip.c3 { order: 2; position: static; align-self: center; translate: none; margin-top: 18px; } .fm .lb small { display: none; } .pg { grid-template-columns: minmax(0, 1fr); } .src { width: min(240px, 100%); margin: 0 auto; } .arr i { rotate: 90deg; margin: 18px 0; }
  .chip.c1 { left: 8px; } .chip.c2 { right: 8px; } .chip { padding: 7px 10px 7px 7px; } .chip b { font-size: 12.5px; } .chip i { width: 26px; height: 26px; }
  .three, .steps, .plans, .how3, .who3 { grid-template-columns: minmax(0, 1fr); } .steps::before { display: none; } .plan.hot { order: -1; } .end { padding: 64px 22px; } .sec { padding-top: 100px; } .vs th, .vs td { padding: 11px 10px; font-size: 13px; } }
@media (max-width: 460px) { .tpl { grid-template-columns: minmax(0, 1fr); } .mod .mh { padding: 16px; } .mod .t { font-size: 15px; } .mod .d { font-size: 13px; } .exs { margin: 0 16px 16px; } .as4 { grid-template-columns: minmax(0, 1fr); } .chip.c2 { display: none; } .hero .sub { font-size: 16.5px; } }
@media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation-duration: .001ms !important; animation-iteration-count: 1 !important; transition-duration: .001ms !important; scroll-behavior: auto !important; } .js .rv { opacity: 1; transform: none; } }
"""

JS = """<script>
(function () {
  const APP_URL = '__APP__'; // адрес приложения ONEFLOW: все «Войти» / «Регистрация» / «Начать» ведут сюда
  document.querySelectorAll('[data-app]').forEach((a) => { a.href = APP_URL + (a.dataset.app === 'register' ? '__REG__' : a.dataset.app === 'demo' ? '?demo=1' : ''); });
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const pm = document.getElementById('pm'), py = document.getElementById('py');
  const set = (k) => { pm.classList.toggle('on', k === 'm'); py.classList.toggle('on', k === 'y'); pm.setAttribute('aria-pressed', k === 'm'); py.setAttribute('aria-pressed', k === 'y');
    document.querySelectorAll('[data-m]').forEach((e) => { e.textContent = '$' + e.dataset[k]; }); }; pm.onclick = () => set('m'); py.onclick = () => set('y');
  const b = document.querySelector('.burger'), m = document.getElementById('mnav');
  const nav = document.querySelector('.nav'), top = document.getElementById('totop'); let ticking = false;
  const onScroll = () => { ticking = false; const y = scrollY; nav.classList.toggle('gone', y > 80); top.classList.toggle('on', y > 600); if (y > 80 && !m.hidden) open(false); };
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  top.addEventListener('click', () => { scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); document.querySelector('.logo').focus({ preventScroll: true }); });
  const open = (o) => { m.hidden = !o; b.setAttribute('aria-expanded', o); b.setAttribute('aria-label', o ? 'Закрыть меню' : 'Открыть меню'); };
  b.addEventListener('click', () => open(m.hidden)); m.addEventListener('click', (e) => { if (e.target.closest('a')) open(false); });
  addEventListener('keydown', (e) => { if (e.key === 'Escape' && !m.hidden) { open(false); b.focus(); } }); onScroll(); addEventListener('resize', () => { if (getComputedStyle(b).display === 'none') open(false); });
  document.querySelectorAll('.mod .mh').forEach((btn) => btn.addEventListener('click', () => { const card = btn.closest('.mod'), open = !card.classList.contains('open');
    document.querySelectorAll('.mod.open').forEach((x) => { if (x !== card) { x.classList.remove('open'); x.querySelector('.mh').setAttribute('aria-expanded', 'false'); } });
    card.classList.toggle('open', open); btn.setAttribute('aria-expanded', open); }));
  document.querySelectorAll('[data-doc]').forEach((x) => x.addEventListener('click', () => { const d = document.getElementById('doc-' + x.dataset.doc); if (d && d.showModal) d.showModal(); }));
  document.querySelectorAll('dialog.doc').forEach((d) => { d.querySelector('.x').addEventListener('click', () => d.close()); d.addEventListener('click', (e) => { if (e.target === d) d.close(); }); });
  const els = document.querySelectorAll('.rv');
  if (!('IntersectionObserver' in window) || reduce) els.forEach((e) => e.classList.add('in'));
  else { const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { threshold: .1 }); els.forEach((e) => io.observe(e)); }
})();
// hero headline: niche rotates every 2.6 s (stays on the first one for reduced motion)
(() => { const r = document.getElementById('rot'); if (!r) return; const w = [...r.children];
  if (w.length < 2 || matchMedia('(prefers-reduced-motion: reduce)').matches) return; let i = 0;
  setInterval(() => { const a = w[i]; i = (i + 1) % w.length; const b = w[i];
    a.classList.remove('on'); a.classList.add('out'); b.classList.remove('out'); b.classList.add('on'); setTimeout(() => a.classList.remove('out'), 700); }, 2600); })();
// site content from oneflow.art/admin: every leaf text in <header>/<main>/<footer> gets a stable key (section + order);
// an override {t: new text, o: original} applies only while the original is unchanged, so rebuilding the page never
// puts an old override on the wrong element. Cached in localStorage to avoid a flash on the next visit.
(() => {
  const SB = 'https://ayxmfihtrsacfdhszsri.supabase.co', KEY = 'sb_publishable_xfd5nkUu18qvdzoo-dzhHQ_f5RKq4tS';
  const SEL = 'h1 .l1, h1 .rw, h1 .gr, h2, h3, h4, p, li, summary, .btn, .k, .pop, .lg, th, td, figcaption, footer nav button, footer nav a, .nav nav a';
  const SKIP = '.pro-b, .ui, .models, .gens, [data-m], script, style, dialog, .skip, .fnote';
  const txt = (el) => [...el.childNodes].map((n) => n.nodeType === 3 ? n.nodeValue : n.nodeName === 'BR' ? '\\n' : '').join('').replace(/[ \\t]+/g, ' ').replace(/ ?\\n ?/g, '\\n').trim();
  const put = (el, v) => { const parts = []; v.split('\\n').forEach((line, i) => { if (i) parts.push(document.createElement('br')); parts.push(document.createTextNode(line)); }); el.replaceChildren(...parts); };
  const counts = {}, items = [];
  document.querySelectorAll('header, main > section, main > .wrap > section, footer').forEach((sec) => {
    const name = (sec.id || sec.classList[0] || sec.tagName).toLowerCase().replace(/[^a-z0-9-]/g, '');
    const label = (sec.querySelector('h2, h1') ? txt(sec.querySelector('h2, h1')) : '') || name;
    sec.querySelectorAll(SEL).forEach((el) => {
      if (el.closest(SKIP) || [...el.children].some((c) => c.nodeName !== 'BR')) return;
      const t = txt(el); if (t.length < 2) return;
      counts[name] = (counts[name] || 0) + 1;
      items.push({ key: name + '.' + counts[name], section: label.split('\\n')[0].slice(0, 60), tag: el.tagName.toLowerCase(), text: t, el });
    });
  });
  window.__ofCMS = items.map(({ key, section, tag, text }) => ({ key, section, tag, text }));
  const apply = (rows) => { const m = new Map((rows || []).map((r) => [r.key, r.value]));
    items.forEach((it) => { const raw = m.get(it.key); let v = null; try { v = raw && JSON.parse(raw); } catch (e) {}
      put(it.el, v && v.o === it.text && typeof v.t === 'string' ? v.t : it.text); }); };
  try { const c = localStorage.getItem('of-cms'); if (c) apply(JSON.parse(c)); } catch (e) {}
  fetch(SB + '/rest/v1/site_content?select=key,value', { headers: { apikey: KEY } }).then((r) => r.ok ? r.json() : null).then((rows) => {
    if (!rows) return; try { localStorage.setItem('of-cms', JSON.stringify(rows)); } catch (e) {} apply(rows); }).catch(() => {});

  // «Написать в поддержку» → support-submit Edge Function → support_tickets (read in the admin)
  const f = document.getElementById('sf'); if (!f) return;
  f.addEventListener('submit', async (e) => {
    e.preventDefault(); const st = f.querySelector('.st'), b = f.querySelector('button[type=submit]'), d = Object.fromEntries(new FormData(f));
    if ((d.contact || '').trim().length < 3) { st.textContent = 'Укажите email или телефон для ответа.'; return; }
    if ((d.message || '').trim().length < 5) { st.textContent = 'Опишите вопрос чуть подробнее.'; return; }
    b.disabled = true; st.textContent = 'Отправляем…';
    try {
      const r = await fetch(SB + '/functions/v1/support-submit', { method: 'POST', headers: { apikey: KEY, Authorization: 'Bearer ' + KEY, 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...d, page: location.pathname + location.search }) });
      const j = await r.json().catch(() => ({})); if (!r.ok) throw new Error(j.error || 'Не удалось отправить. Попробуйте позже.');
      f.reset(); st.textContent = 'Спасибо! Сообщение отправлено — мы свяжемся с вами.';
    } catch (err) { st.textContent = err.message; } finally { b.disabled = false; }
  });
})();
</script>
""".replace('__APP__', APP).replace('__REG__', REG).replace("  document.querySelectorAll('.mod .mh')", protos.js() + "  document.querySelectorAll('.mod .mh')")


DARK = """
:root { --bg: #0b0b10; --ink: #f3f3f6; --ink2: #c4c4cf; --muted: #8c8c9a; --line: rgba(255,255,255,.08); --card: #14141b; --mint: rgba(61,220,151,.1); --green: #3ddc97;
  --sh: inset 0 0 0 1px rgba(255,255,255,.06), 0 18px 44px -22px rgba(0,0,0,.85); --sh2: inset 0 0 0 1px rgba(255,255,255,.07), 0 40px 80px -36px rgba(0,0,0,.95); }
html { color-scheme: dark; } .totop { background: #f3f3f6; color: #0b0b10; box-shadow: 0 12px 30px -10px rgba(0,0,0,.8); } .totop { border-radius: 6px; } .skip { background: #f3f3f6; color: #0b0b10; }
.bgfx i { opacity: .4; } .bgfx .a { background: #5b3fd6; } .bgfx .b { background: #0e8a64; } .bgfx .c { background: #a8522c; } .bgfx .d { background: #2553c9; opacity: .28; }
.btn.p { background: #f3f3f6; color: #0b0b10; box-shadow: 0 10px 30px -12px rgba(160,140,255,.5); } .btn.g { background: rgba(255,255,255,.06); color: var(--ink); box-shadow: inset 0 0 0 1px rgba(255,255,255,.12); }
.nav .in { background: rgba(20,20,28,.66); backdrop-filter: blur(18px) saturate(160%); -webkit-backdrop-filter: blur(18px) saturate(160%); box-shadow: inset 0 0 0 1px rgba(255,255,255,.08), 0 10px 30px -18px rgba(0,0,0,.8); }
.mnav { background: rgba(20,20,28,.97); } .mnav a:hover { background: rgba(255,255,255,.06); } .mnav .row .in2 { box-shadow: inset 0 0 0 1px rgba(255,255,255,.16); }
.hero h1 .gr { background: linear-gradient(95deg, #ffffff 25%, #9ce8cb 60%, #b3a6ff); -webkit-background-clip: text; background-clip: text; }
.panel { background: rgba(22,22,32,.55); box-shadow: inset 0 0 0 1px rgba(255,255,255,.08), var(--sh2); } .src { background: #1a1a23; } .fm { background: #1a1a23; } .fm .lb { background: rgba(10,10,14,.82); color: #fff; }
.chip { background: rgba(28,28,38,.92); } .chip.c1 i { background: rgba(61,220,151,.15); } .chip.c2 i { background: rgba(124,92,255,.2); color: #b3a6ff; } .chip.c3 i { background: rgba(255,122,69,.16); }
.models span { color: #ececf2; } .three .card::before { opacity: .16; }
.ring { background: conic-gradient(var(--green) calc(var(--v, 0) * 1%), rgba(61,220,151,.14) 0); } .ring::before { background: var(--card); }
.cmp .bx { background: repeating-linear-gradient(135deg, rgba(255,255,255,.09) 0 6px, rgba(255,255,255,.03) 6px 12px); } .cmp .by { background: linear-gradient(90deg, #b3a6ff, #9ce8cb); }
.frames span { background: #1b1b24; box-shadow: inset 0 0 0 1.5px rgba(255,255,255,.14); }
.steps::before { background: repeating-linear-gradient(90deg, rgba(255,255,255,.16) 0 6px, transparent 6px 12px); } .steps .n { background: var(--card); box-shadow: var(--sh); }
.mods .ic { background: color-mix(in srgb, var(--c) 22%, #14141b); } .flow span, .li em, .msg { background: color-mix(in srgb, var(--c) 20%, #14141b); } .exs { border-top-color: rgba(255,255,255,.1); }
.li li, .inv { background: rgba(255,255,255,.05); } .inv b { background: #f3f3f6; color: #0b0b10; } .sc i, .fn i { background: rgba(255,255,255,.08); } .mod .more, .mods .ic { filter: brightness(1.25); }
.how3 .n { background: #f3f3f6; color: #0b0b10; }
.vs th:last-child { background: #f3f3f6; color: #0b0b10; } .vs td:last-child { background: rgba(61,220,151,.1); color: #e8fff5; }
.chat .me { background: #f3f3f6; color: #0b0b10; } .chat .pr { background: rgba(255,255,255,.05); } .chat .nodes span { background: rgba(255,255,255,.06); box-shadow: inset 0 0 0 1px rgba(255,255,255,.09); } .chat .run { background: #f3f3f6; color: #0b0b10; }
.as4 .you { background: linear-gradient(135deg, #2c2356, #103c30); }
.per div { background: var(--card); } .per button.on { background: #f3f3f6; color: #0b0b10; } .per em { background: rgba(61,220,151,.15); }
.plan .btn.w { background: rgba(255,255,255,.06); color: var(--ink); box-shadow: inset 0 0 0 1px rgba(255,255,255,.12); }
.plan.hot { background: linear-gradient(160deg, #f6f4ff, #e8fbf3); color: #0b0b10; box-shadow: 0 40px 80px -30px rgba(140,120,255,.45); } .plan.hot > p, .plan.hot .pr small, .plan.hot li::before { color: rgba(11,11,16,.6); }
.plan.hot .btn { background: #0b0b10; color: #fff; } .gens { background: rgba(255,255,255,.05); } .qm { background: rgba(255,255,255,.14); } .qm::after { background: #f3f3f6; color: #0b0b10; }
.plan.hot .gens { background: rgba(11,11,16,.05); } .plan.hot .qm { background: rgba(11,11,16,.1); color: #0b0b10; } .plan.hot .gens > span { color: rgba(11,11,16,.6); } .plan.hot .qm::after { background: #0b0b10; color: #fff; } .plan.hot .gens .nw { color: rgba(11,11,16,.55); } .gens .top { background: #f3f3f6; color: #0b0b10; } .plan.hot .gens .top { background: #0b0b10; color: #fff; } .plan .pop { background: rgba(124,92,255,.2); color: #b3a6ff; } .plan.hot .pop { background: #e3dcff; color: #5b3fd6; }
.faq details, .end { background: var(--card); } .gal .t > div { box-shadow: 0 18px 44px -22px rgba(0,0,0,.9); }
dialog.doc { background: #15151c; } dialog.doc .x { background: rgba(255,255,255,.08); color: var(--ink); } dialog.doc::backdrop { background: rgba(0,0,0,.6); }
/* smaller corner radii */
.nav .in, .mnav { border-radius: 12px; } .btn { border-radius: 5px; } .nav .btn { border-radius: 5px; } .mnav .row .in2 { border-radius: 5px; } .panel { border-radius: 18px; } .src { border-radius: 10px; }
.fm { border-radius: 8px; } .fm .lb, .ba figcaption, .food2 figcaption { border-radius: 5px; } .chip { border-radius: 10px; } .chip i { border-radius: 7px; } .card, .mod .mh { border-radius: 14px; }
.ba figure { border-radius: 8px; } .how3 .card, .who3 .card, .as4 .card, .food2 figure, .faq details { border-radius: 12px; } .chat .me { border-radius: 10px 10px 3px 10px; } .chat .pr, .li li, .inv { border-radius: 8px; } .chat .run { border-radius: 4px; }
.chat .nodes span, .flow span, .inv b, .th span, .plan .pop { border-radius: 6px; } .gal .t > div { border-radius: 10px; } .per div { border-radius: 5px; } .per button { border-radius: 4px; } .per em { border-radius: 5px; }
.plan { border-radius: 16px; } .end { border-radius: 20px; } dialog.doc { border-radius: 14px; } dialog.doc .x { border-radius: 9px; } .mods .ic { border-radius: 9px; } .frames span { border-radius: 4px; }
"""


def build(docs='', theme='light'):
    """docs: <dialog> markup for the legal pages (added by the single-file build); footer buttons open them."""
    links = ''.join(f'<a href="{h}">{t}</a>' for h, t in NAV)
    nav = (f'<a class="skip" href="#main">К содержанию</a><header class="nav"><div class="wrap in"><a class="logo" href="#top" aria-label="ONEFLOW — наверх">{MARK}ONEFLOW</a>'
           f'<nav aria-label="Разделы">{links}</nav><span class="sp"></span><a class="lg" data-app="login" href="{APP}">Войти</a>{reg("Регистрация")}'
           '<button class="burger" type="button" aria-label="Открыть меню" aria-expanded="false" aria-controls="mnav"><i></i><i></i></button></div></header>'
           f'<nav class="mnav" id="mnav" aria-label="Меню" hidden>{links}<div class="row"><a class="in2" data-app="login" href="{APP}">Войти</a>{reg("Регистрация")}</div></nav>')
    fm = lambda c, lb: f'<div class="fm {c}"><i class="ft"></i><span class="lb">{lb}</span></div>'
    hero = (f'<section class="hero"><div class="wrap">'
            '<h1 aria-label="Больше контента для вашего бизнеса. До 50% дешевле*"><span class="l1">Больше контента для</span><span class="rot" id="rot" aria-hidden="true">'
            + ''.join(f'<span class="rw{" on" if k == 0 else ""}">{n}.</span>' for k, n in enumerate(NICHES)) + '</span><span class="gr">До 50% дешевле*</span></h1>'
            '<p class="sub">Фото, видео и тексты на 30+ нейросетях — и адаптация под любой размер в один клик. Неиспользованный бюджет остаётся с вами.</p>'
            f'<div class="acts">{reg("Начать бесплатно →")}<a class="btn g" href="#how">Как это работает</a></div>'
            '<div class="hvid"><video poster="assets/video/oneflow-promo.jpg" autoplay muted loop playsinline preload="auto" disablepictureinpicture disableremoteplayback '
            'aria-label="Промо-ролик ONEFLOW: генерация, адаптация и запуск контента"><source src="assets/video/oneflow-promo.mp4" type="video/mp4">'
            '<source src="assets/video/oneflow-promo.webm" type="video/webm"></video></div>'
            '<div class="panel" role="img" aria-label="Карточка «Мягкий зайка» адаптирована под Stories 9:16, Google Discovery, Яндекс РСЯ и Kaspi — пример">'
            '<span class="chip c1"><i>↺</i><span><small>Перенесено на октябрь</small><b>+$112 бюджета</b></span></span>'
            '<span class="chip c2"><i>⤢</i><span><small>Адаптация</small><b>1 фото → 4 формата</b></span></span>'
            '<span class="chip c3"><i>★</i><span><small>Пресеты</small><b>Kaspi · РСЯ · Discovery</b></span></span>'
            '<div class="pg"><figure class="src"><img src="assets/ol/bunny.webp" alt="" width="600" height="800"><figcaption><span>Исходник</span><span>3:4</span></figcaption></figure>'
            '<div class="arr" aria-hidden="true"><i></i>адаптация</div>'
            f'<div class="fmts">{fm("f916", "9:16")}{fm("fdis", "1200×628<small> · Discovery</small>")}{fm("frsy", "1080×450<small> · РСЯ</small>")}{fm("fksp", "1125×330<small> · Kaspi</small>")}</div></div></div>'
            f'<div class="models" role="img" aria-label="Модели: {", ".join(MODELS)}"><div class="t">{"".join(f"<span>{m}</span>" for m in MODELS) * 2}</div></div></div></section>')
    frames = ''.join(f'<span style="width:{w}px;height:{h}px">{t}</span>' for t, w, h in (('9:16', 30, 54), ('4:5', 40, 50), ('1:1', 46, 46), ('16:9', 62, 35), ('3:1', 72, 24)))
    why = ('<section class="sec" id="why"><div class="wrap"><div class="sh rv"><span class="k">Почему ONEFLOW</span><h2>Три вещи, которые меняют бюджет</h2>'
           '<p>Один баланс на все модели, форматы под каждую площадку и деньги, которые не пропадают.</p></div><div class="three">'
           '<article class="card rv" style="--tint:#eaf8f0"><div class="big">100%</div><h3>остатка переходит на следующий месяц</h3><p>Бюджет не сгорает в конце месяца — остаток складывается с новым.</p>'
           '<div class="viz"><div class="ring" aria-hidden="true"><span>$112<small>перенесено</small></span></div></div><p class="cap">пример · сентябрь → октябрь</p></article>'
           '<article class="card rv" style="--tint:#f0edff"><div class="big">−50%</div><h3>к цене генерации*</h3><p>Те же модели — без наценок посредников и без подписки на каждый сервис.</p>'
           '<div class="viz"><div class="cmp" aria-hidden="true"><div><span>Отдельные сервисы</span><b>$300</b></div><i class="bx"></i><div><span>ONEFLOW</span><b>от $150</b></div><i class="by"></i></div></div><p class="cap">пример · $300 в месяц</p></article>'
           f'<article class="card rv" style="--tint:#fff1e8"><div class="big">∞</div><h3>любой размер — ресайз делает ONEFLOW</h3><p>Задайте любой размер, и ONEFLOW сам сделает ресайз. Никаких трат времени на адаптацию визуала под разные форматы.</p>'
           f'<div class="viz"><div class="frames" aria-hidden="true">{frames}</div></div><p class="cap">Kaspi · GDN · РСЯ · BYYD · Discovery</p></article></div>'
           '<p class="note">* До 50% — в сравнении с оплатой тех же моделей в отдельных сервисах; итог зависит от моделей и объёма.</p></div></section>')
    steps = ('<section class="sec" id="how"><div class="wrap"><div class="sh rv"><span class="k">Как это работает</span><h2>Три шага от фото до кампании</h2></div><div class="steps">'
             '<div class="rv"><span class="n">01</span><h3>Загрузите фото или идею</h3><p>Товар, референс или пара строк — этого достаточно.</p></div>'
             '<div class="rv"><span class="n">02</span><h3>Ассистент соберёт цепочку</h3><p>Разберёт нишу, подготовит промпты и схему нод — вы проверяете и запускаете.</p></div>'
             '<div class="rv"><span class="n">03</span><h3>Получите все форматы</h3><p>Kaspi, Яндекс РСЯ, Google, BYYD и сторис — одним запуском.</p></div></div></div></section>')
    mods = protos.section()
    tpl = ''.join(f'<article class="card rv" aria-label="Шаблон «{tn}»: {t}">{ba(k, after=tn)}<div class="tx"><span class="tn">{w}</span><h3>{t}</h3><p>{d}</p></div></article>' for k, w, t, d, tn in TPL)
    how3 = ''.join(f'<div class="card rv"><span class="n">{i}</span><span><b>{a}</b><small>{b_}</small></span></div>' for i, (a, b_) in enumerate(
        [('Выберите шаблон', 'HoReCa, Квартира, Авто, Техника или Мебель'), ('Загрузите своё фото', 'снимок на телефон подойдёт'), ('Получите студийный кадр', 'высокое разрешение — и любой размер для площадок')], 1))
    business = ('<section class="sec" id="business"><div class="wrap"><div class="sh rv"><span class="k">Шаблоны для бизнеса</span><h2>Студийные фото без фотографа</h2>'
                '<p>Готовые шаблоны для ресторанов, риелторов, автодилеров и магазинов электроники. Загрузите фото с телефона — получите снимок студийного качества в высоком разрешении.</p></div>'
                f'<div class="tpl">{tpl}</div><div class="how3">{how3}</div><p class="note">Иллюстрации показывают эффект шаблона. Шаблоны — в разделе «Для бизнеса» в приложении.</p></div></section>')
    menu = ''.join(f'<div class="mi"><svg viewBox="0 0 200 150" aria-hidden="true"><use href="#s-food"/></svg><span><b>{n}</b><small>{s}</small></span><em>{p}</em></div>'
                   for n, s, p in (('Поке с лососем', 'рис, авокадо, эдамаме', '3 900 ₸'), ('Поке веган', 'тофу, овощи, кунжут', '3 200 ₸'), ('Поке спайси', 'тунец, чили-майо', '4 100 ₸')))
    vs = ''.join(f'<tr><td>{a}</td><td>{b_}</td><td>{c}</td></tr>' for a, b_, c in VS)
    horeca = ('<section class="sec" id="horeca"><div class="wrap"><div class="sh rv"><span class="k">Для ресторанов и МСБ</span><h2>Меню, доставка и соцсети — с одного телефона</h2>'
              '<p>Снимите блюдо на кухне — шаблон HoReCa сделает аппетитное фото на белом фоне. Каждое новое блюдо, машина или квартира больше не означают новую фотосессию.</p></div>'
              '<div class="hr"><div class="rv"><div class="food2"><figure class="bp b-food"><svg viewBox="0 0 200 150" aria-hidden="true"><use href="#s-food"/></svg><figcaption>Снимок на кухне</figcaption></figure>'
              '<figure class="ap a-food"><svg viewBox="0 0 200 150" aria-hidden="true"><use href="#s-food"/></svg><figcaption>Шаблон HoReCa</figcaption></figure></div>'
              f'<div class="card menu"><div class="mh">Меню<span>доставка</span></div>{menu}</div></div>'
              f'<div class="rv"><div class="card vs"><table><thead><tr><th><span class="sr">Критерий</span></th><th>Фотограф и студия</th><th>Шаблон ONEFLOW</th></tr></thead><tbody>{vs}</tbody></table></div>'
              '<div class="who3"><div class="card"><b>Кафе и рестораны</b><small>меню, доставка, соцсети</small></div><div class="card"><b>Риелторы и автодилеры</b><small>фото для объявлений и каталога</small></div>'
              '<div class="card"><b>Магазины электроники</b><small>карточки товаров и баннеры</small></div></div></div></div></div></section>')
    assistant = ('<section class="sec" id="assistant"><div class="wrap"><div class="sh rv"><span class="k">ИИ-ассистент</span><h2>Помогает с идеями, промптами и схемой</h2>'
                 '<p>Когда нужен не только шаблон: ассистент разберёт нишу, подскажет идеи, напишет промпт и сам соберёт схему нод. Запускаете вы.</p></div><div class="as">'
                 '<div class="card chat rv" role="img" aria-label="Пример диалога с ассистентом: разбор ниши, промпт и схема нод; запуск — за пользователем">'
                 '<div class="ch"><span>ИИ-ассистент</span><span>пример</span></div><p class="me">Кофейня, доставка. Нужны сторис на неделю под новое зимнее меню.</p>'
                 '<div class="ai"><h4>Аудитория</h4><ul><li>студенты и офис — заказывают в обед и вечером</li><li>в сторис лучше заходят крупные планы напитков</li><li>акцент на сезонное меню и доставку до 30 минут</li></ul>'
                 '<h4>Промпт</h4><p class="pr">Зимний латте на тёплом фоне, мягкий утренний свет, крупный план</p>'
                 '<h4>Схема нод</h4><div class="nodes"><span>Фото</span><i>→</i><span>Генерация фото</span><i>→</i><span>Адаптация 9:16</span></div></div>'
                 '<div class="ft"><span>Проверьте схему и нажмите «Запустить»</span><span class="run">Запустить пайплайн ▸</span></div></div>'
                 '<div class="as4"><article class="card rv"><span class="n">01</span><h3>Разбор ниши</h3><p>Аудитория, конкуренты и какой контент нужен именно вам.</p><span class="w">делает ассистент</span></article>'
                 '<article class="card rv"><span class="n">02</span><h3>Промпты</h3><p>Пишет и улучшает промпт под выбранную модель.</p><span class="w">делает ассистент</span></article>'
                 '<article class="card rv"><span class="n">03</span><h3>Схема нод</h3><p>По описанию задачи собирает схему на холсте.</p><span class="w">делает ассистент</span></article>'
                 '<article class="card rv you"><span class="n">04</span><h3>Запуск</h3><p>Вы проверяете схему и жмёте «Запустить пайплайн» — дальше она проходит сама.</p><span class="w">делаете вы</span></article></div></div></div></section>')
    cards = ''.join(f'<div style="background-image:var(--img-{n})"></div>' for n in IMGS)
    gal = ('<section class="sec" aria-label="Примеры работ"><div class="wrap"><div class="sh rv"><span class="k">Результаты</span><h2>Сделано в ONEFLOW</h2><p>Карточки и креативы из одного фото — по шаблонам One Launch.</p></div></div>'
           f'<div class="gal" role="img" aria-label="Примеры карточек: {", ".join(ALT[n] for n in IMGS)}"><div class="t">{cards}{cards}</div></div></section>')
    pricing = ('<section class="sec" id="pricing"><div class="wrap"><div class="sh rv"><span class="k">Тарифы</span><h2>Остаток бюджета — всегда ваш</h2><p>На любом тарифе неизрасходованный бюджет переходит на следующий месяц.</p></div>'
               '<div class="per"><div role="group" aria-label="Период оплаты"><button type="button" class="on" id="pm" aria-pressed="true">Месяц</button><button type="button" id="py" aria-pressed="false">Год<em>−20%</em></button></div></div>'
               '<div class="plans"><article class="card plan demo rv"><h3>Попробовать</h3><div class="pr"><span class="dp">Демо-режим</span></div><p>Откройте ONEFLOW без регистрации и посмотрите всё изнутри: разделы, ноды, Motion Engine.</p><ul><li>Без регистрации и карты</li><li>Все разделы программы</li><li>Генерации показываются на примерах — ничего не списывается</li><li>Перейти на тариф — в любой момент</li></ul>' + f'<a class="btn w" data-app="demo" href="{APP}?demo=1">Открыть демо →</a>' + '</article>'
               '<article class="card plan rv"><h3>Стартовый</h3><div class="pr"><span data-m="20" data-y="16">$20</span><small> / мес</small></div><p>Для первых карточек и тестов рекламы.</p>'
               + gens(20) + '<ul><li>Все разделы ONEFLOW</li><li>LLM-модели</li><li>Адаптация визуалов</li></ul>' + reg('Выбрать', 'btn w') + '</article>'
               '<article class="card plan hot rv"><span class="pop">Популярный</span><h3>Популярный</h3><div class="pr"><span data-m="60" data-y="48">$60</span><small> / мес</small></div><p>Для регулярной работы с генерацией.</p>' + gens(60) + '<ul><li>Все разделы ONEFLOW</li><li>LLM-модели</li><li>Адаптация визуалов</li><li>One Launch</li></ul>' + reg('Выбрать →') + '</article>'
               '<article class="card plan rv"><h3>Максимальный</h3><div class="pr"><span data-m="200" data-y="160">$200</span><small> / мес</small></div><p>Для команд без ограничений.</p>' + gens(200) + '<ul><li>Всё из популярного</li><li>Creative Predictor</li><li>Приоритетная поддержка</li></ul>' + reg('Выбрать', 'btn w') + '</article></div></div></section>')
    faq = ''.join(f'<details{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(FAQ))
    faq = (f'<section class="sec" id="faq"><div class="wrap"><div class="sh rv"><span class="k">Вопросы</span><h2>Коротко о главном</h2></div><div class="faq">{faq}</div>'
           '<p class="sup rv">Не нашли ответ? <button type="button" class="btn g" data-doc="support" aria-haspopup="dialog">Написать в поддержку</button></p></div></section>')
    end = ('<div class="wrap"><section class="end rv"><h2>Создавайте больше.<br>Не теряйте ни доллара.</h2><p>Генерация до 50% дешевле*, любой размер одним кликом, бюджет не сгорает в конце месяца.</p>'
           f'<div class="acts">{reg("Начать бесплатно →")}</div></section></div>')
    fnav = (''.join(f'<button type="button" data-doc="{k}" aria-haspopup="dialog">{t}</button>' for k, t in (('privacy', 'Конфиденциальность'), ('terms', 'Условия'), ('refunds', 'Возврат'), ('support', 'Поддержка')))
            if docs else '<a href="#">Конфиденциальность</a><a href="#">Условия</a><a href="#">Возврат</a>')
    support = ('<dialog class="doc" id="doc-support" aria-label="Поддержка"><button type="button" class="x" aria-label="Закрыть">×</button><div class="in2">'
               '<h1>Написать в поддержку</h1><p class="updated">Оставьте контакт — ответим на email или по телефону, который вы укажете.</p>'
               '<form class="sf" id="sf" novalidate><label>Как к вам обращаться<input name="name" maxlength="100" autocomplete="name"></label>'
               '<label>Email или телефон для ответа<input name="contact" maxlength="200" required autocomplete="email"></label>'
               '<label>Сообщение<textarea name="message" maxlength="4000" required></textarea></label>'
               '<label class="hp" aria-hidden="true">Сайт<input name="website" tabindex="-1" autocomplete="off"></label>'
               '<button type="submit" class="btn p">Отправить</button><p class="st" role="status" aria-live="polite"></p></form></div></dialog>')
    footer = f'<footer><div class="wrap"><div class="l"><span class="logo">{MARK}ONEFLOW</span><span>© 2026</span></div><nav aria-label="Документы">{fnav}</nav></div></footer>{docs}{support}'
    theme_color, dark_css = ('#0b0b10', DARK) if theme == 'dark' else ('#f7f7fa', '')
    imgvars = ' '.join(f'--img-{n}: url(assets/ol/{n}.webp);' for n in IMGS)
    return ('<!doctype html>\n<html lang="ru">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<title>ONEFLOW — больше контента, до 50% дешевле</title>\n'
            '<meta name="description" content="30+ нейросетей в одном окне: фото, видео и тексты для рекламы. Адаптация под любой размер и пресеты Kaspi, РСЯ, Google, BYYD. Генерация до 50% дешевле, бюджет не сгорает в конце месяца.">\n'
            f'<meta name="theme-color" content="{theme_color}">\n<meta property="og:type" content="website">\n<meta property="og:site_name" content="ONEFLOW">\n<meta property="og:locale" content="ru_RU">\n'
            '<meta property="og:title" content="ONEFLOW — больше контента, до 50% дешевле">\n'
            '<link rel="canonical" href="https://oneflow.art/">\n<meta property="og:url" content="https://oneflow.art/">\n'
            "<script>document.documentElement.classList.add('js')</script>\n<link rel=\"stylesheet\" href=\"fonts.css\">\n"
            f'<style>{CSS.replace("IMGVARS", imgvars)}{protos.CSS}{dark_css}{protos.DARK if theme == "dark" else ""}.sr {{ position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); }}</style>\n</head>\n'
            f'<body id="top">\n<div class="bgfx" aria-hidden="true"><i class="a"></i><i class="b"></i><i class="c"></i><i class="d"></i></div>\n{SYM}\n{nav}\n<main id="main">{hero}{why}{steps}{mods}{business}{horeca}{assistant}{gal}{pricing}{faq}{end}</main>\n{footer}\n<button type="button" class="totop" id="totop" aria-label="Наверх">↑</button>\n{JS}</body>\n</html>\n')


if __name__ == '__main__':
    open(os.path.join(HERE, 'v4-porcelain.html'), 'w', encoding='utf-8').write(build())
    open(os.path.join(HERE, 'v4-porcelain-dark.html'), 'w', encoding='utf-8').write(build(theme='dark'))
    print('v4-porcelain.html')
