"""Mini interactive prototypes of the ONEFLOW interface, one per module card («Всё для контента — в одном окне»).

Each card carries a small working copy of the real screen (dark app UI, Inter): nodes you can drag, formats you can
switch, a chat that types, trends you can open. Results are canned examples — generation itself happens in the app.
All class names are prefixed with u- so they never clash with the landing's own styles.
"""

ICONS = {
    'canvas': '<circle cx="5" cy="5" r="2.5"/><circle cx="19" cy="12" r="2.5"/><circle cx="5" cy="19" r="2.5"/><path d="M7.5 5h3a5 5 0 015 5M7.5 19h3a5 5 0 005-5"/>',
    'ol': '<path d="M5 19c2-6 6-12 14-14-1 8-7 12-13 15z"/><path d="M9 15l-3-3"/>',
    'cw': '<path d="M6 3h9l4 4v14H6z"/><path d="M9 11h7M9 15h7M9 7h3"/>',
    'tr': '<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
    'pd': '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    'mu': '<path d="M9 18V5l11-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="17" cy="16" r="3"/>',
    'st': '<path d="M3 4h18l-7 8v6l-4 2v-8z"/>',
    'ms': '<circle cx="8" cy="8" r="3.5"/><circle cx="17" cy="10" r="2.5"/><path d="M2 20c0-3.5 3-6 6-6s6 2.5 6 6M14 20c0-2.5 1.5-4.5 3-4.5s4 1.5 4 4.5"/>',
    'img': '<rect x="3" y="4" width="18" height="16" rx="3"/><circle cx="9" cy="10" r="2"/><path d="M21 16l-5-5-8 9"/>',
    'crop': '<path d="M6 2v14a2 2 0 002 2h14"/><path d="M18 22V8a2 2 0 00-2-2H2"/>',
    'out': '<rect x="3" y="3" width="7" height="9" rx="1.5"/><rect x="14" y="3" width="7" height="5" rx="1.5"/><rect x="14" y="12" width="7" height="9" rx="1.5"/><rect x="3" y="16" width="7" height="5" rx="1.5"/>',
}


def ico(k, cls='u-svg'):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[k]}</svg>'


# ---------------------------------------------------------------- 1 · node canvas
def ui_canvas():
    rows = ''.join(f'<button type="button" class="u-row on" aria-pressed="true" data-n="{n}" data-w="{w}" data-h="{h}"><span class="u-f">{n}</span><span class="u-f u-num">{w}</span><i>×</i><span class="u-f u-num">{h}</span></button>'
                   for n, w, h in (('Kaspi', 1125, 330), ('Stories 9:16', 1080, 1920), ('Яндекс РСЯ', 1080, 450)))
    node = lambda k, title, c, body, ports: (f'<div class="u-node u-n-{k}" data-n="{k}">' + ('<i class="u-port i"></i>' if 'i' in ports else '')
                                             + f'<div class="u-nh" title="Перетащите ноду"><span class="u-ni" style="--c:{c}">{ico(dict(img="img", ad="crop", out="out")[k])}</span>{title}</div><div class="u-nb">{body}</div>'
                                             + ('<i class="u-port o"></i>' if 'o' in ports else '') + '</div>')
    return ('<div class="ui u-cv" aria-label="Демо: нодовый холст — нода «Изображение» → «Адаптация» → «Результат»">'
            '<svg class="u-edges" aria-hidden="true"><path class="e1"/><path class="e2"/></svg>'
            + node('img', 'Изображение', '#4fb3c8', '<div class="u-thumb" style="background-image:var(--img-bunny)"></div><span class="u-cap">мягкий-зайка.webp</span>', 'o')
            + node('ad', 'Адаптация', '#d59a55', f'<span class="u-l">Форматы</span><div class="u-rows">{rows}</div><button type="button" class="u-add">+ Добавить формат</button><button type="button" class="u-btn u-go">✦ Сгенерировать</button>', 'io')
            + node('out', 'Результат', '#9b87ff', '<div class="u-res"><p class="u-empty">Нажмите «Сгенерировать»</p></div>', 'i')
            + '<span class="u-tip">перетаскивайте ноды · нажмите на формат, чтобы выключить</span></div>')


# ---------------------------------------------------------------- 2 · One Launch
OL_PHOTOS = [('bunny', 'Мягкий зайка'), ('coffee', 'Кофемашина Aroma One'), ('airbuds', 'Наушники Airbuds X1')]


def ui_onelaunch():
    ph = ''.join(f'<button type="button" class="u-pho" role="radio" aria-checked="{str(i == 0).lower()}" data-i="{k}" data-t="{t}" aria-label="{t}" style="background-image:var(--img-{k})"></button>'
                 for i, (k, t) in enumerate(OL_PHOTOS))
    fm = ''.join(f'<button type="button" class="u-chip" aria-pressed="{str(i == 0).lower()}" data-w="{w}" data-h="{h}">{n}</button>'
                 for i, (n, w, h) in enumerate((('Stories 9:16', 1080, 1920), ('Пост 4:5', 1080, 1350), ('Kaspi', 1125, 330))))
    return ('<div class="ui u-ol" aria-label="Демо: One Launch — фото товара → карточка под формат">'
            '<div class="u-olh"><span class="u-beta">BETA</span><b>ONE LAUNCH</b></div>'
            f'<span class="u-step"><i>1</i>Фото товара</span><div class="u-phos" role="radiogroup" aria-label="Фото товара">{ph}</div>'
            '<span class="u-step"><i>2</i>Название и формат</span><input class="u-in u-name" value="Мягкий зайка" aria-label="Название товара" maxlength="40">'
            f'<div class="u-chips" role="group" aria-label="Формат">{fm}</div><button type="button" class="u-btn u-go">✦ Сгенерировать</button>'
            '<div class="u-prev"><div class="u-card"><span class="u-ph0">карточка появится здесь</span></div><span class="u-bar" aria-hidden="true"><i></i></span></div>'
            '<p class="u-st" aria-live="polite">Выберите фото и нажмите «Сгенерировать»</p></div>')


# ---------------------------------------------------------------- 3 · Copywrite engine
CW = [
    ('Заголовки объявления', 'Напиши 3 заголовка объявления для мягкого зайки',
     ['1. Мягкий зайка — лучший друг для сна', '2. Гипоаллергенный плюш для самых маленьких, 0+', '3. Подарок, который обнимают каждый вечер'], ''),
    ('SEO-описание', 'SEO-описание для Kaspi: мягкий зайка',
     ['Мягкая игрушка «Зайка» из нежного плюша с гипоаллергенным наполнителем. Подходит детям с рождения: безопасные материалы, прочные швы, бант, который не отрывается.'], 'Описание_Kaspi.docx|DOCX'),
    ('Контент-план', 'Контент-план на неделю для магазина игрушек',
     ['Пн — распаковка зайки в Reels', 'Ср — «до/после»: как засыпает малыш', 'Пт — опрос: какой цвет банта выбрать?'], 'Контент-план.xlsx|XLSX'),
    ('Проверить текст', 'Проверь: «Мягкий зайка для сна, гипоалергенный»',
     ['Исправил: «гипоаллергенный» — с двумя «л». Остальное без ошибок.'], ''),
]


def ui_copy():
    hints = ''.join(f'<button type="button" class="u-chip u-hint" data-i="{i}">{h}</button>' for i, (h, _, _, _) in enumerate(CW))
    return ('<div class="ui u-cw" aria-label="Демо: Copywrite engine — чат для текстов">'
            '<div class="u-log" aria-live="polite"><div class="u-hi"><b>Привет! Чем могу помочь?</b><small>ИИ-ассистент для текстов, идей и документов</small></div></div>'
            '<div class="u-box"><span class="u-ph">Спросите о чём угодно…</span><span class="u-meta">ONEFLOW AI</span><span class="u-send" aria-hidden="true">↑</span></div>'
            f'<span class="u-l">Быстрые подсказки — нажмите</span><div class="u-chips">{hints}</div></div>')


# ---------------------------------------------------------------- 4 · TRENDSWATCHING
TR = [
    ('TikTok', 'Товар в неожиданном масштабе', '@planet.noah', 'Лайков', '318K', 'pyramid',
     'Продукт снят рядом с объектом несопоставимого размера — приём читается за первую секунду и удерживает до конца ролика.',
     'Покажите товар в неожиданном масштабе — это подчёркивает ценность и вызывает эмоцию.',
     ['0–1 с — товар крупно в руке', '1–4 с — камера отъезжает: рядом огромный предмет', '4–7 с — название и цена на экране']),
    ('Instagram', 'Один предмет — три сценария', '@mari.daily', 'Лайков', '132K', 'robot',
     'Один товар в трёх бытовых ситуациях — зритель сам примеряет его к своей жизни.',
     'Снимите товар в трёх сценах — утро, день, вечер — и смонтируйте в один Reels.',
     ['Сцена 1 — утро: товар в деле', 'Сцена 2 — день: неожиданное применение', 'Сцена 3 — вечер: итог и призыв']),
    ('Threads', 'Почему покупатели возвращаются', '@brand_thinker', 'Комментариев', '1.9K', '',
     'Короткий тред с личной историей собирает обсуждение в комментариях.',
     'Расскажите от первого лица, почему клиенты заказывают снова, и закончите вопросом.',
     ['Пост 1 — история одного клиента', 'Пост 2 — что вы сделали иначе', 'Пост 3 — вопрос аудитории']),
    ('TikTok', 'Честный обзор вместо рекламы', '@katya.review', 'Лайков', '174K', 'body',
     'Минусы в начале ролика повышают доверие к плюсам — зритель досматривает до конца.',
     'Начните с честного «что не понравилось», затем покажите главное преимущество.',
     ['0–2 с — «что мне не понравилось»', '2–6 с — главное преимущество крупно', '6–9 с — вывод и ссылка']),
    ('Instagram', 'Распаковка без лица в кадре', '@studio.grain', 'Лайков', '78K', 'speaker',
     'Крупный план рук и живой звук распаковки работают как ASMR и удерживают внимание.',
     'Снимите распаковку сверху: только руки, товар и живой звук.',
     ['Кадр 1 — коробка сверху', 'Кадр 2 — руки открывают упаковку', 'Кадр 3 — товар в свете, без текста']),
]


def ui_trends():
    def row(i, t):
        p, title, a, ml, m, img = t[:6]
        th = (f'<span class="u-th" style="background-image:var(--img-{img})"></span>' if img else '<span class="u-th u-tx">Короткий тред о том, что удерживает…</span>')
        return (f'<div class="u-trr{" on" if i == 0 else ""}" data-p="{p}" data-i="{i}"><button type="button" class="u-trb" aria-pressed="{str(i == 0).lower()}">{th}'
                f'<span class="u-trt"><small>{p}</small><b>{title}</b><em>{a}</em></span><span class="u-trm"><small>{ml}</small><b>{m}</b></span></button>'
                '<button type="button" class="u-bm" aria-pressed="false" aria-label="В избранное">'
                '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M6 3h12v18l-6-4-6 4z"/></svg></button></div>')
    rows = ''.join(row(i, t) for i, t in enumerate(TR))
    flt = ''.join(f'<button type="button" class="u-chip" aria-pressed="{str(i == 0).lower()}" data-f="{f}">{f or "Все площадки"}</button>' for i, f in enumerate(('', 'TikTok', 'Instagram', 'Threads')))
    return ('<div class="ui u-tr" aria-label="Демо: TRENDSWATCHING — тренды с разбором">'
            f'<div class="u-trh"><b>Тренды</b><div class="u-chips" role="group" aria-label="Площадка">{flt}</div></div>'
            f'<div class="u-trl">{rows}</div><div class="u-trd" aria-live="polite"></div></div>')


# ---------------------------------------------------------------- 5 · Creative Predictor
def ui_predictor():
    pl = ''.join(f'<button type="button" class="u-chip" aria-pressed="{str(i == 0).lower()}" data-k="{k}">{n}</button>' for i, (k, n) in enumerate((('any', 'Любая'), ('kaspi', 'Kaspi'), ('ig', 'Instagram'))))
    return ('<div class="ui u-pd" aria-label="Демо: Creative Predictor — оценка вариантов креатива">'
            '<span class="u-l">Варианты креатива</span><div class="u-slots">'
            '<div class="u-slot v1" data-v="0"><i style="background-image:var(--img-bunny)"></i><span>1</span></div>'
            '<div class="u-slot v2" data-v="1"><i style="background-image:var(--img-bunny)"></i><span>2</span></div>'
            '<div class="u-slot v3" data-v="2" hidden><i style="background-image:var(--img-bunny)"></i><span>3</span><button type="button" class="u-x" aria-label="Убрать вариант 3">×</button></div>'
            '<button type="button" class="u-slot u-plus" aria-label="Добавить вариант">+</button></div>'
            f'<span class="u-l">Площадка</span><div class="u-row2"><div class="u-chips" role="group" aria-label="Площадка">{pl}</div><button type="button" class="u-btn u-go">Оценить</button></div>'
            '<div class="u-sc" aria-live="polite"><p class="u-empty">Нажмите «Оценить» — покажем, какой вариант сильнее</p></div></div>')


# ---------------------------------------------------------------- 6 · Music & voice
def ui_music():
    gen = ''.join(f'<button type="button" class="u-chip" aria-pressed="{str(g == "Lo-fi").lower()}">{g}</button>' for g in ('Pop', 'Lo-fi', 'Jazz', 'Ambient', 'Electronic'))
    voi = ''.join(f'<button type="button" class="u-chip" aria-pressed="{str(i == 0).lower()}">{g}</button>' for i, g in enumerate(('Спокойный', 'Энергичный', 'Деловой')))
    return ('<div class="ui u-mu" aria-label="Демо: музыка и озвучка">'
            '<div class="u-tabs" role="tablist"><button type="button" role="tab" aria-selected="true" data-t="m">♫ Музыка</button><button type="button" role="tab" aria-selected="false" data-t="s">◉ Речь</button></div>'
            '<div class="u-pane" data-p="m"><span class="u-l">Промпт (стиль, настроение)</span><input class="u-in" value="Лёгкий лоу-фай для кофейни" aria-label="Промпт">'
            f'<span class="u-l">Жанр</span><div class="u-chips" role="group" aria-label="Жанр">{gen}</div></div>'
            '<div class="u-pane" data-p="s" hidden><span class="u-l">Текст</span><input class="u-in" value="Скидка 20% до воскресенья — успейте!" aria-label="Текст для озвучки">'
            f'<span class="u-l">Голос</span><div class="u-chips" role="group" aria-label="Голос">{voi}</div></div>'
            '<button type="button" class="u-btn u-go">✦ Сгенерировать</button>'
            '<div class="u-pl" hidden><button type="button" class="u-play" aria-label="Воспроизвести">▶</button><div class="u-pw"><b class="u-pt"></b><div class="u-wave" aria-hidden="true"></div></div><span class="u-time">0:00</span></div>'
            '<p class="u-st">превью интерфейса — звук генерируется в приложении</p></div>')


# ---------------------------------------------------------------- 7 · Strategy
def ui_strategy():
    goals = ''.join(f'<button type="button" class="u-opt" aria-pressed="{str(i == 0).lower()}" data-g="{i}">{g}</button>' for i, g in enumerate(('Продажи', 'Лиды', 'Узнаваемость')))
    return ('<div class="ui u-sg" aria-label="Демо: Стратегия — воронка и бюджет">'
            '<span class="u-prog"><i style="width:50%"></i></span><span class="u-l u-sl">◎ Стратегия · <em>1 из 2</em></span>'
            f'<div class="u-q" data-q="1"><b>Какой результат вы хотите получить?</b><div class="u-opts">{goals}</div><button type="button" class="u-btn u-next">Продолжить</button></div>'
            '<div class="u-q" data-q="2" hidden><b>Бюджет на месяц</b><div class="u-bud"><span class="u-bv">$500</span><input type="range" min="100" max="3000" step="50" value="500" aria-label="Бюджет на месяц"></div>'
            '<button type="button" class="u-btn u-next">Показать план</button></div>'
            '<div class="u-q" data-q="3" hidden><b class="u-rt"></b><div class="u-fun"></div><div class="u-chs"></div><button type="button" class="u-link">↺ Изменить ответы</button></div></div>')


# ---------------------------------------------------------------- 8 · Co-authors & messenger
def ui_messenger():
    return ('<div class="ui u-ms" aria-label="Демо: соавторы и мессенджер">'
            '<div class="u-ct"><span class="u-l">Команда</span><ul class="u-cl">'
            '<li><span class="u-av" style="--h:260">А</span><span><b>Аружан</b><small class="u-on">генерирует</small></span></li>'
            '<li><span class="u-av" style="--h:150">Д</span><span><b>Данияр</b><small class="u-on">пишет текст</small></span></li></ul>'
            '<form class="u-inv" novalidate><span class="u-l">Пригласить соавтора</span><input class="u-in" type="email" placeholder="почта коллеги" aria-label="Почта коллеги"><button type="submit" class="u-btn">Пригласить</button><small class="u-msg" aria-live="polite"></small></form></div>'
            '<div class="u-chat"><div class="u-chh"><b>Аружан</b><small>в проекте «Весна»</small></div><div class="u-ml" aria-live="polite">'
            '<div class="u-m"><p>Сторис готовы — глянешь 9:16?</p><span class="u-att" style="background-image:var(--img-bunny)"></span></div>'
            '<div class="u-m me"><p>Супер, беру в работу</p></div></div>'
            '<form class="u-send2"><input class="u-in" placeholder="Сообщение…" aria-label="Сообщение" maxlength="120"><button type="submit" class="u-btn" aria-label="Отправить">↑</button></form></div></div>')


CARDS = [  # (key, title, description, accent, icon, builder, span)
    ('canvas', 'Нодовый холст', 'Цепочки генераций в один пайплайн: фото → адаптация → все форматы.', '#3b6cff', 'canvas', ui_canvas, 's2'),
    ('ol', 'One Launch', 'Фото товара → карточки и баннеры по шаблонам.', '#ff7a45', 'ol', ui_onelaunch, ''),
    ('tr', 'TRENDSWATCHING', 'Тренды TikTok, Instagram и Threads с разбором — и сразу в сценарий.', '#16a36a', 'tr', ui_trends, 's2'),
    ('cw', 'Copywrite engine', 'Тексты и документы: Word, Excel, PowerPoint.', '#8b5cf6', 'cw', ui_copy, ''),
    ('pd', 'Creative Predictor', 'Сравнение креативов до запуска рекламы.', '#0ea5a4', 'pd', ui_predictor, ''),
    ('mu', 'Музыка и голос', 'Трек по описанию или озвучка нужным голосом.', '#a855f7', 'mu', ui_music, ''),
    ('st', 'Стратегия', 'Воронка, бюджет и план под вашу нишу.', '#ef4444', 'st', ui_strategy, ''),
    ('ms', 'Соавторы', 'Пригласите коллегу по почте и работайте вместе.', '#2563eb', 'ms', ui_messenger, 's3'),
]


def section():
    cards = ''.join(f'<article class="card pro rv {sp}" style="--c:{c}"><button type="button" class="pro-h" aria-expanded="false" aria-controls="pb-{k}"><span class="ic">{ico(i, "")}</span>'
                    f'<span class="pro-t"><b>{t}</b><span>{d}</span></span><span class="more">Подробно<i aria-hidden="true">+</i></span></button>'
                    f'<div class="pro-b" id="pb-{k}" role="region" aria-label="Демо: {t}" hidden>{b()}</div></article>'
                    for k, t, d, c, i, b, sp in CARDS)
    return ('<section class="sec" id="modules"><div class="wrap"><div class="sh rv"><span class="k">Возможности</span><h2>Всё для контента — в одном окне</h2>'
            '<p>Нажмите на инструмент — откроется его мини-версия: можно нажимать, переключать, запускать.</p></div>'
            f'<div class="pros">{cards}</div><p class="note">Демо на странице: результаты — примеры. Настоящая генерация — в приложении.</p></div></section>')


CSS = """
/* ---------- mini prototypes (module cards) ---------- */
.pros { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); grid-auto-flow: row dense; gap: 14px; margin-top: 48px; align-items: start; }
.pro { display: flex; flex-direction: column; padding: 0; overflow: hidden; } .pro.open { grid-column: span 2; } .pro.s2.open, .pro.s3.open { grid-column: 1 / -1; }
.pro-h { display: grid; grid-template-columns: auto minmax(0, 1fr); grid-template-rows: 1fr auto; gap: 12px 12px; width: 100%; min-height: 156px; padding: 20px; border: 0; background: none; text-align: left; cursor: pointer; }
.pro-h .ic { display: grid; place-items: center; width: 40px; height: 40px; border-radius: 11px; background: color-mix(in srgb, var(--c) 12%, #fff); color: var(--c); } .pro-h .ic svg { width: 20px; height: 20px; }
.pro-t b { display: block; font: 600 16px/1.25 var(--d); } .pro-t span { display: block; margin-top: 4px; font-size: 13.5px; line-height: 1.45; color: var(--muted); }
.pro-h .more { grid-column: 1 / -1; display: inline-flex; align-items: center; gap: 8px; font: 700 11.5px var(--d); letter-spacing: .14em; text-transform: uppercase; color: var(--muted); }
.pro-h .more i { display: grid; place-items: center; width: 20px; height: 20px; border-radius: 50%; background: color-mix(in srgb, var(--ink) 7%, transparent); color: var(--ink2); letter-spacing: 0; font-style: normal; font-size: 14px; transition: rotate .3s var(--e); }
.pro.open .pro-h .more i { rotate: 45deg; } .pro-h:hover .more { color: var(--ink2); } .pro-h:hover .more i { background: color-mix(in srgb, var(--ink) 13%, transparent); } .pro.open { box-shadow: 0 0 0 1.5px color-mix(in srgb, var(--c) 45%, transparent), var(--sh); }
.pro-b { display: flex; flex-direction: column; padding: 0 16px 16px; animation: uin .4s var(--e) both; } .pro-b[hidden] { display: none; }
.ui { --ub: #0f0f12; --up: #1b1b20; --up2: #24242a; --ul: rgba(255,255,255,.08); --ut: #ececf1; --um: #8e8e99; --ug: #3ddc97;
  position: relative; flex: 1; display: flex; flex-direction: column; gap: 8px; min-height: 300px; padding: 12px; overflow: hidden; border-radius: 14px; background: var(--ub); color: var(--ut);
  font: 400 12.5px/1.4 'Inter', var(--d); box-shadow: inset 0 0 0 1px rgba(255,255,255,.06); -webkit-font-smoothing: antialiased; text-align: left; }
.ui button { font: inherit; color: inherit; } .ui :focus-visible { outline: 2px solid #9b87ff; outline-offset: 2px; }
.u-l { font: 500 9.5px/1.2 'Inter', var(--d); letter-spacing: .07em; text-transform: uppercase; color: var(--um); }
.u-in, .u-f { width: 100%; min-width: 0; padding: 7px 10px; border: 1px solid var(--ul); border-radius: 9px; background: var(--up2); color: var(--ut); font: 500 12px 'Inter', var(--d); }
.u-in:focus { outline: none; border-color: rgba(155,135,255,.7); }
.u-btn { display: inline-flex; align-items: center; justify-content: center; gap: 7px; padding: 8px 14px; border: 0; border-radius: 99px; background: #ececf1; color: #111 !important; font: 600 12px 'Inter', var(--d) !important; cursor: pointer; transition: transform .15s, opacity .2s; white-space: nowrap; }
.u-btn:hover { transform: translateY(-1px); } .u-btn:disabled { opacity: .55; cursor: default; transform: none; }
.u-chips { display: flex; flex-wrap: wrap; gap: 5px; } .u-chip { padding: 5px 10px; border: 1px solid var(--ul); border-radius: 99px; background: var(--up2); font-size: 11.5px !important; cursor: pointer; transition: background .2s, color .2s; }
.u-chip:hover { background: #2d2d35; } .u-chip[aria-pressed="true"] { background: #ececf1; color: #111 !important; border-color: transparent; }
.u-spin { width: 10px; height: 10px; border: 2px solid currentColor; border-right-color: transparent; border-radius: 50%; animation: uspin .7s linear infinite; } @keyframes uspin { to { rotate: 360deg; } }
.u-empty { margin: auto; padding: 12px; text-align: center; color: var(--um); font-size: 11.5px; } .u-st { font-size: 11px; color: var(--um); text-align: center; }
@keyframes uin { from { opacity: 0; transform: translateY(5px); } }
/* 1 canvas */
.u-cv { padding: 0; min-height: 330px; background: var(--ub) radial-gradient(rgba(255,255,255,.08) 1px, transparent 1.3px) 0 0 / 16px 16px; }
.u-edges { position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none; } .u-edges path { fill: none; stroke: rgba(255,255,255,.5); stroke-width: 1.6; }
.u-edges path.flow { stroke: #b3a6ff; stroke-dasharray: 6 6; animation: uflow .5s linear infinite; } @keyframes uflow { to { stroke-dashoffset: -12; } }
.u-node { position: absolute; left: 0; top: 0; border: 1px solid rgba(255,255,255,.1); border-radius: 13px; background: var(--up); box-shadow: 0 14px 30px -12px rgba(0,0,0,.7); }
.u-node.drag { box-shadow: 0 0 0 1.5px rgba(155,135,255,.7), 0 20px 40px -12px rgba(0,0,0,.8); } .u-n-img { width: 132px; } .u-n-ad { width: 238px; } .u-n-out { width: 170px; }
.u-nh { display: flex; align-items: center; gap: 8px; padding: 8px 10px; border-bottom: 1px solid var(--ul); border-radius: 13px 13px 0 0; background: linear-gradient(90deg, rgba(255,255,255,.05), transparent); font-weight: 600; font-size: 12.5px; cursor: grab; touch-action: none; user-select: none; -webkit-user-select: none; }
.u-node.drag .u-nh { cursor: grabbing; } .u-ni { display: grid; place-items: center; width: 22px; height: 22px; border-radius: 7px; background: color-mix(in srgb, var(--c) 28%, #1b1b20); color: var(--c); } .u-ni svg { width: 13px; height: 13px; }
.u-nb { display: flex; flex-direction: column; gap: 6px; padding: 9px 10px 10px; } .u-thumb { height: 100px; border-radius: 8px; background: center 30% / cover; } .u-cap { font-size: 10.5px; color: var(--um); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.u-port { position: absolute; top: 50%; z-index: 1; width: 10px; height: 10px; margin-top: -5px; border: 2px solid var(--ub); border-radius: 50%; background: #ececf1; } .u-port.o { right: -6px; } .u-port.i { left: -6px; }
.u-rows { display: grid; gap: 5px; } .u-row { display: grid; grid-template-columns: minmax(0, 1fr) 46px 8px 46px; align-items: center; gap: 4px; padding: 0; border: 0; background: none; cursor: pointer; text-align: left; transition: opacity .2s; }
.u-row .u-f { padding: 5px 8px; font-size: 11.5px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; } .u-row i { font-style: normal; font-size: 10px; color: var(--um); text-align: center; }
.u-row:not(.on) { opacity: .35; } .u-row:not(.on) .u-f:first-child { text-decoration: line-through; } .u-row:hover .u-f { border-color: rgba(255,255,255,.2); }
.u-add { align-self: flex-start; padding: 5px 10px; border: 1px solid var(--ul); border-radius: 99px; background: transparent; font-size: 11px !important; cursor: pointer; } .u-add:hover { background: var(--up2); }
.u-go { width: 100%; margin-top: 2px; } .u-res { display: flex; flex-direction: column; gap: 7px; min-height: 60px; } .u-res .u-empty { padding: 10px 0; }
.u-ri { display: flex; align-items: center; gap: 8px; animation: uin .4s both; } .u-ri small { font-size: 10.5px; color: var(--um); line-height: 1.25; } .u-ri small b { display: block; color: var(--ut); font-weight: 600; }
.u-fr { position: relative; flex: none; overflow: hidden; border-radius: 4px; background: #2a2a31; } .u-fr::before { content: ''; position: absolute; inset: -8px; background: var(--img-bunny) center / cover; filter: blur(8px); opacity: .9; } .u-fr::after { content: ''; position: absolute; inset: 0; background: var(--img-bunny) center / contain no-repeat; }
.u-fw { display: grid; place-items: center; width: 70px; flex: none; }
.u-tip { position: absolute; left: 12px; bottom: 10px; font-size: 10.5px; color: var(--um); pointer-events: none; }
/* 2 one launch */
.u-olh { display: flex; align-items: center; gap: 8px; } .u-olh b { font: 800 15px 'Inter', var(--d); letter-spacing: -.01em; } .u-beta { padding: 2px 7px; border-radius: 99px; background: #ececf1; color: #111; font-size: 9px; font-weight: 700; }
.u-step { display: flex; align-items: center; gap: 7px; font-size: 11.5px; font-weight: 600; } .u-step i { display: grid; place-items: center; width: 17px; height: 17px; border-radius: 50%; background: #ececf1; color: #111; font-size: 10px; font-style: normal; }
.u-phos { display: flex; gap: 6px; } .u-pho { width: 54px; height: 54px; padding: 0; border: 1px solid var(--ul); border-radius: 10px; background: #fff 50% 78% / 190% no-repeat; cursor: pointer; opacity: .6; transition: opacity .2s, box-shadow .2s; }
.u-pho[aria-checked="true"] { opacity: 1; box-shadow: 0 0 0 2px #ececf1; } .u-pho:hover { opacity: 1; }
.u-prev { position: relative; display: grid; place-items: center; flex: 1; min-height: 170px; border-radius: 10px; background: #0a0a0c; box-shadow: inset 0 0 0 1px var(--ul); overflow: hidden; }
.u-card { position: relative; display: grid; place-items: center; overflow: hidden; border-radius: 6px; border: 1px dashed rgba(255,255,255,.18); transition: width .45s cubic-bezier(.2,.7,.2,1), height .45s cubic-bezier(.2,.7,.2,1); }
.u-card::before, .u-card::after { content: ''; position: absolute; opacity: 0; transition: opacity .4s; } .u-card::before { inset: -14px; background: var(--im) center / cover; filter: blur(12px); } .u-card::after { inset: 0; background: var(--im) center / contain no-repeat; }
.u-card.done { border-color: transparent; } .u-card.done::before { opacity: .85; } .u-card.done::after { opacity: 1; } .u-card.done .u-ph0 { opacity: 0; } .u-ph0 { padding: 6px; font-size: 10.5px; color: var(--um); text-align: center; transition: opacity .2s; }
.u-bar { position: absolute; left: 12px; right: 12px; bottom: 10px; height: 3px; border-radius: 3px; background: rgba(255,255,255,.08); opacity: 0; transition: opacity .2s; } .u-bar i { display: block; width: 0; height: 100%; border-radius: inherit; background: linear-gradient(90deg, #9b87ff, #3ddc97); }
.u-bar.run { opacity: 1; } .u-bar.run i { animation: ubar 1.3s ease-in-out forwards; } @keyframes ubar { to { width: 100%; } }
/* 3 copywrite */
.u-log { flex: 1; display: flex; flex-direction: column; gap: 8px; min-height: 150px; } .u-hi { margin: auto 0; text-align: center; } .u-hi b { display: block; font-size: 15px; font-weight: 700; } .u-hi small { color: var(--um); font-size: 11px; }
.u-me { align-self: flex-end; max-width: 88%; padding: 8px 11px; border-radius: 12px 12px 3px 12px; background: #ececf1; color: #111; font-size: 12px; animation: uin .3s both; }
.u-ai { display: grid; gap: 3px; max-width: 96%; font-size: 12px; color: #dcdce3; animation: uin .3s both; } .u-ai p { min-height: 1em; }
.u-dots { display: inline-flex; gap: 4px; padding: 9px 11px; border-radius: 12px; background: var(--up2); } .u-dots i { width: 5px; height: 5px; border-radius: 50%; background: var(--um); animation: udot 1s infinite; } .u-dots i:nth-child(2) { animation-delay: .15s; } .u-dots i:nth-child(3) { animation-delay: .3s; }
@keyframes udot { 30% { opacity: 1; transform: translateY(-2px); } 0%, 60%, 100% { opacity: .35; } }
.u-file { display: inline-flex; align-items: center; gap: 8px; margin-top: 4px; padding: 6px 9px; border: 1px solid var(--ul); border-radius: 9px; background: var(--up); font-size: 11.5px; animation: uin .3s both; } .u-file em { padding: 1px 6px; border-radius: 5px; background: rgba(61,220,151,.14); color: var(--ug); font: 600 9.5px 'Inter', var(--d); font-style: normal; }
.u-box { display: flex; align-items: center; gap: 8px; padding: 9px 9px 9px 12px; border: 1px solid var(--ul); border-radius: 14px; background: var(--up); } .u-box .u-ph { flex: 1; min-width: 0; color: var(--um); overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }
.u-box .u-ph.typing { color: var(--ut); } .u-box .u-ph.typing::after { content: '|'; margin-left: 1px; animation: ublink .8s steps(1) infinite; } @keyframes ublink { 50% { opacity: 0; } }
.u-meta { font-size: 9.5px; font-weight: 600; letter-spacing: .04em; color: var(--um); } .u-send { display: grid; place-items: center; width: 24px; height: 24px; border-radius: 50%; background: #ececf1; color: #111; font-size: 12px; font-weight: 700; }
.u-hint:disabled { opacity: .5; cursor: default; }
/* 4 trends */
.u-tr { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, .95fr); grid-template-rows: auto 1fr; gap: 10px; min-height: 340px; } .u-trh { grid-column: 1 / -1; display: flex; flex-wrap: wrap; align-items: center; gap: 8px 12px; } .u-trh > b { font-size: 17px; font-weight: 700; margin-right: auto; }
.u-trl { display: flex; flex-direction: column; gap: 3px; } .u-trr { position: relative; animation: uin .3s both; } .u-trr[hidden] { display: none; }
.u-trb { display: grid; grid-template-columns: 38px minmax(0, 1fr) auto; align-items: center; gap: 9px; width: 100%; padding: 6px 30px 6px 6px; border: 1px solid transparent; border-radius: 10px; background: none; text-align: left; cursor: pointer; }
.u-trb:hover { background: rgba(255,255,255,.03); } .u-trr.on .u-trb { border-color: rgba(61,220,151,.45); background: rgba(61,220,151,.06); }
.u-th { width: 38px; height: 38px; border-radius: 7px; background: #fff center / cover; } .u-th.u-tx { display: grid; place-items: center; padding: 3px; background: #2a2a31; color: var(--um); font-size: 6.5px; line-height: 1.2; }
.u-trt { min-width: 0; } .u-trt small, .u-trt em { display: block; font-size: 9.5px; color: var(--um); font-style: normal; } .u-trt b { display: block; font-size: 12px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.u-trm { text-align: right; } .u-trm small { display: block; font-size: 9px; color: var(--um); } .u-trm b { font-size: 14px; font-weight: 700; color: var(--ug); }
.u-bm { position: absolute; right: 6px; top: 50%; translate: 0 -50%; width: 22px; height: 22px; padding: 3px; border: 0; background: none; color: var(--um); cursor: pointer; } .u-bm svg { width: 100%; height: 100%; } .u-bm[aria-pressed="true"] { color: var(--ug); } .u-bm[aria-pressed="true"] path { fill: currentColor; }
.u-trd { display: flex; flex-direction: column; gap: 6px; min-width: 0; padding: 10px; border-radius: 12px; background: #16161a; box-shadow: inset 0 0 0 1px var(--ul); animation: uin .3s both; }
.u-tri { height: 100px; border-radius: 8px; background: #fff center 40% / cover; } .u-tri.u-tx { display: grid; place-items: center; padding: 12px; background: #24242a; color: #c9c9d2; font-size: 12px; text-align: center; }
.u-trd h4 { font-size: 13.5px; font-weight: 700; } .u-trd h5 { margin-top: 2px; font-size: 11px; font-weight: 700; } .u-trd p { font-size: 11px; color: #a9a9b4; } .u-trd .u-by { font-size: 10px; color: var(--um); }
.u-trbt { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 4px; } .u-ghost { background: transparent !important; color: var(--ut) !important; box-shadow: inset 0 0 0 1px rgba(255,255,255,.18); }
.u-scn { display: grid; gap: 4px; margin-top: 2px; padding: 8px; border-radius: 9px; background: rgba(155,135,255,.1); } .u-scn li { list-style: none; font-size: 11px; animation: uin .3s both; } .u-scn li::before { content: '▸ '; color: #b3a6ff; }
.u-toast { position: absolute; left: 50%; bottom: 12px; translate: -50% 0; padding: 7px 12px; border-radius: 99px; background: #ececf1; color: #111; font-size: 11.5px; font-weight: 600; animation: uin .3s both; white-space: nowrap; }
/* 5 predictor */
.u-slots { display: flex; gap: 8px; } .u-slot { position: relative; width: 64px; height: 64px; flex: none; padding: 0; border: 1px solid var(--ul); border-radius: 10px; background: var(--up2); overflow: hidden; }
.u-slot[hidden] { display: none; } .u-slot > i { position: absolute; inset: 0; background: #fff center / cover; } .u-slot.v2 > i { background-size: 62%; background-color: #cfcfd4; filter: saturate(.45) brightness(.82); background-repeat: no-repeat; } .u-slot.v3 > i { background-size: 170%; background-position: 50% 78%; }
.u-slot > span { position: absolute; left: 4px; bottom: 4px; padding: 0 5px; border-radius: 5px; background: rgba(0,0,0,.7); font-size: 9.5px; font-weight: 700; } .u-slot.win { box-shadow: 0 0 0 2px var(--ug); }
.u-slot.win::after { content: 'сильнее'; position: absolute; right: 3px; top: 3px; padding: 1px 5px; border-radius: 5px; background: var(--ug); color: #06291b; font-size: 8.5px; font-weight: 700; }
.u-plus { display: grid; place-items: center; color: var(--um); font-size: 20px; cursor: pointer; border-style: dashed; } .u-x { position: absolute; right: 3px; top: 3px; width: 18px; height: 18px; padding: 0; border: 0; border-radius: 50%; background: rgba(0,0,0,.7); color: #fff; font-size: 12px; line-height: 1; cursor: pointer; }
.u-row2 { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 8px; } .u-sc { flex: 1; display: flex; flex-direction: column; gap: 8px; min-height: 110px; padding-top: 4px; }
.u-sr { display: grid; grid-template-columns: 70px minmax(0, 1fr) 30px; align-items: center; gap: 8px; animation: uin .3s both; } .u-sr > span { font-size: 11px; font-weight: 600; } .u-sr > b { font-size: 13px; text-align: right; }
.u-sb { height: 6px; border-radius: 6px; background: rgba(255,255,255,.08); overflow: hidden; } .u-sb i { display: block; height: 100%; width: 0; border-radius: inherit; background: linear-gradient(90deg, #0ea5a4, #3ddc97); transition: width .9s cubic-bezier(.2,.7,.2,1); }
.u-sr small { grid-column: 2 / 4; margin-top: -3px; font-size: 10.5px; color: var(--um); } .u-sr.best > span, .u-sr.best > b { color: var(--ug); }
/* 6 music */
.u-tabs { display: flex; gap: 4px; align-self: center; padding: 3px; border-radius: 99px; background: var(--up); } .u-tabs button { padding: 5px 12px; border: 0; border-radius: 99px; background: none; font-size: 11.5px !important; cursor: pointer; color: var(--um) !important; }
.u-tabs [aria-selected="true"] { background: #ececf1; color: #111 !important; } .u-pane { display: flex; flex-direction: column; gap: 7px; } .u-pane[hidden] { display: none; }
.u-pl { display: flex; align-items: center; gap: 10px; padding: 9px; border-radius: 12px; background: var(--up); animation: uin .35s both; } .u-pl[hidden] { display: none; }
.u-play { display: grid; place-items: center; width: 34px; height: 34px; flex: none; border: 0; border-radius: 50%; background: #ececf1; color: #111 !important; font-size: 12px !important; cursor: pointer; }
.u-pw { flex: 1; min-width: 0; } .u-pt { display: block; margin-bottom: 4px; font-size: 11px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; } .u-wave { display: flex; align-items: center; gap: 2px; height: 26px; }
.u-wave i { flex: 1; min-width: 1px; border-radius: 2px; background: rgba(255,255,255,.22); } .u-wave i.on { background: #b3a6ff; } .u-time { font-size: 10.5px; color: var(--um); font-variant-numeric: tabular-nums; }
/* 7 strategy */
.u-prog { height: 3px; border-radius: 3px; background: rgba(255,255,255,.1); } .u-prog i { display: block; height: 100%; border-radius: inherit; background: #ececf1; transition: width .4s; } .u-sl em { font-style: normal; }
.u-q { display: flex; flex-direction: column; gap: 10px; flex: 1; animation: uin .35s both; } .u-q[hidden] { display: none; } .u-q > b { font-size: 14px; font-weight: 700; } .u-q .u-btn, .u-q .u-link { align-self: flex-end; margin-top: auto; }
.u-opts { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 6px; } .u-opt { padding: 16px 6px; border: 1px solid var(--ul); border-radius: 11px; background: var(--up); font-size: 12px !important; font-weight: 600 !important; cursor: pointer; transition: background .2s, border-color .2s; }
.u-opt[aria-pressed="true"] { background: #2b2b33; border-color: rgba(255,255,255,.4); } .u-opt:hover { background: #26262d; }
.u-bud { display: grid; gap: 8px; padding: 12px; border-radius: 11px; background: var(--up); } .u-bv { font-size: 22px; font-weight: 700; } .u-bud input { width: 100%; accent-color: #ececf1; }
.u-fun { display: grid; gap: 6px; } .u-fr2 { display: grid; grid-template-columns: 86px minmax(0, 1fr) 46px; align-items: center; gap: 8px; font-size: 11px; animation: uin .35s both; } .u-fr2 b { text-align: right; font-size: 11.5px; }
.u-fr2 i { display: block; height: 16px; border-radius: 5px; background: linear-gradient(90deg, #ef4444, #ff8a5c); transition: width .8s cubic-bezier(.2,.7,.2,1); } .u-chs { display: flex; flex-wrap: wrap; gap: 5px; } .u-chs span { padding: 3px 9px; border-radius: 99px; background: var(--up2); font-size: 10.5px; }
.u-link { padding: 4px 0; border: 0; background: none; color: var(--um) !important; font-size: 11.5px !important; cursor: pointer; } .u-link:hover { color: var(--ut) !important; }
/* 8 messenger */
.u-ms { display: grid; grid-template-columns: 240px minmax(0, 1fr); gap: 10px; min-height: 250px; } .u-ct { display: flex; flex-direction: column; gap: 8px; }
.u-cl { display: grid; gap: 4px; list-style: none; } .u-cl li { display: flex; align-items: center; gap: 9px; padding: 6px; border-radius: 9px; animation: uin .3s both; } .u-cl li:first-child { background: var(--up); }
.u-av { position: relative; display: grid; place-items: center; width: 28px; height: 28px; flex: none; border-radius: 50%; background: hsl(var(--h) 55% 45%); font-size: 11.5px; font-weight: 700; } .u-cl b { display: block; font-size: 12px; } .u-cl small { font-size: 10.5px; color: var(--um); }
.u-on { color: var(--ug) !important; } .u-on::before { content: '● '; font-size: 8px; } .u-inv { display: grid; gap: 6px; margin-top: auto; } .u-msg { min-height: 14px; font-size: 10.5px; color: var(--ug); } .u-msg.err { color: #ff8a8a; }
.u-chat { display: flex; flex-direction: column; gap: 8px; min-width: 0; padding: 10px; border-radius: 12px; background: #16161a; box-shadow: inset 0 0 0 1px var(--ul); } .u-chh { display: flex; align-items: baseline; gap: 8px; } .u-chh b { font-size: 13px; } .u-chh small { font-size: 10.5px; color: var(--um); }
.u-ml { flex: 1; display: flex; flex-direction: column; gap: 6px; max-height: 170px; overflow-y: auto; scrollbar-width: thin; } .u-m { align-self: flex-start; display: flex; align-items: flex-end; gap: 6px; max-width: 80%; animation: uin .3s both; }
.u-m p { padding: 7px 10px; border-radius: 11px 11px 11px 3px; background: var(--up2); font-size: 12px; } .u-m.me { align-self: flex-end; } .u-m.me p { border-radius: 11px 11px 3px 11px; background: #ececf1; color: #111; }
.u-att { width: 30px; height: 52px; flex: none; border-radius: 5px; background: #fff center / cover; } .u-send2 { display: flex; gap: 6px; } .u-send2 .u-btn { width: 34px; padding: 0; }
@media (max-width: 1000px) { .pros { grid-template-columns: repeat(2, minmax(0, 1fr)); } .pro.open { grid-column: 1 / -1; } }
@media (max-width: 680px) { .pros { grid-template-columns: minmax(0, 1fr); } .pro.open { grid-column: auto; } .pro-h { min-height: 0; padding: 16px; } .pro-b { padding: 0 10px 10px; } .u-tr { grid-template-columns: minmax(0, 1fr); } .u-trh { grid-column: auto; } .u-ms { grid-template-columns: minmax(0, 1fr); } .u-ct { order: 2; } .u-tip { display: none; } .pro { padding: 12px; } .ui { padding: 10px; } }
"""

DARK = """
.pro-h .ic { background: color-mix(in srgb, var(--c) 22%, #14141b); filter: brightness(1.25); } .ui { box-shadow: inset 0 0 0 1px rgba(255,255,255,.08); }
.pro-h .ic { border-radius: 9px; } .ui { border-radius: 10px; }
"""

JS = r"""
  const W8 = (ms) => (reduce ? 0 : ms);
  // feature cards: closed by default, one open at a time; the open card widens to fit its demo
  const pros = [...document.querySelectorAll('.pro')];
  pros.forEach((c) => { const h = c.querySelector('.pro-h'), b = c.querySelector('.pro-b');
    h.addEventListener('click', () => { const open = !c.classList.contains('open');
      pros.forEach((x) => { if (x !== c && x.classList.contains('open')) { x.classList.remove('open'); x.querySelector('.pro-h').setAttribute('aria-expanded', 'false'); x.querySelector('.pro-b').hidden = true; } });
      c.classList.toggle('open', open); h.setAttribute('aria-expanded', open); b.hidden = !open;
      if (open) requestAnimationFrame(() => { const r = c.getBoundingClientRect(); if (r.top < 70 || r.bottom > innerHeight) c.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: r.height > innerHeight - 90 ? 'start' : 'nearest' }); }); }); });
  // 1 · node canvas: drag nodes, toggle / add formats, run «Сгенерировать»
  document.querySelectorAll('.u-cv').forEach((cv) => {
    const N = { img: cv.querySelector('[data-n=img]'), ad: cv.querySelector('[data-n=ad]'), out: cv.querySelector('[data-n=out]') }, e1 = cv.querySelector('.e1'), e2 = cv.querySelector('.e2');
    const res = cv.querySelector('.u-res'), go = cv.querySelector('.u-go'), add = cv.querySelector('.u-add'), rowsEl = cv.querySelector('.u-rows');
    let moved = false, z = 2; const more = [['Discovery', 1200, 628], ['GDN', 300, 250], ['Пост 4:5', 1080, 1350]];
    const pos = (n, x, y) => { n.style.left = Math.round(x) + 'px'; n.style.top = Math.round(y) + 'px'; };
    const port = (n, s) => { const r = n.querySelector('.u-port.' + s).getBoundingClientRect(), c = cv.getBoundingClientRect(); return [r.left + r.width / 2 - c.left, r.top + r.height / 2 - c.top]; };
    const curve = (a, b) => { const dx = Math.max(36, Math.abs(b[0] - a[0]) / 2); return 'M' + a[0] + ',' + a[1] + ' C' + (a[0] + dx) + ',' + a[1] + ' ' + (b[0] - dx) + ',' + b[1] + ' ' + b[0] + ',' + b[1]; };
    const draw = () => { e1.setAttribute('d', curve(port(N.img, 'o'), port(N.ad, 'i'))); e2.setAttribute('d', curve(port(N.ad, 'o'), port(N.out, 'i'))); };
    const fit = () => { const b = Math.max(...Object.values(N).map((n) => n.offsetTop + n.offsetHeight)); cv.style.minHeight = Math.max(330, b + 34) + 'px'; };
    const layout = () => { if (!moved) { const w = cv.clientWidth;
      if (w >= 600) { const g = (w - 132 - 238 - 170 - 28) / 2, H = cv.clientHeight - 30, cy = (n) => Math.max(12, (H - n.offsetHeight) / 2); pos(N.img, 14, cy(N.img)); pos(N.ad, 14 + 132 + g, cy(N.ad)); pos(N.out, w - 170 - 14, cy(N.out)); }
      else { pos(N.img, 10, 12); pos(N.out, w - 170 - 10, 12); pos(N.ad, Math.max(10, (w - 238) / 2), Math.max(N.img.offsetHeight, N.out.offsetHeight) + 34); } }
      fit(); draw(); };
    cv.querySelectorAll('.u-nh').forEach((h) => h.addEventListener('pointerdown', (e) => { const n = h.parentElement, sx = e.clientX, sy = e.clientY, x0 = n.offsetLeft, y0 = n.offsetTop;
      h.setPointerCapture(e.pointerId); n.classList.add('drag'); n.style.zIndex = ++z;
      const mv = (ev) => { moved = true; pos(n, Math.min(Math.max(0, x0 + ev.clientX - sx), cv.clientWidth - n.offsetWidth), Math.min(Math.max(0, y0 + ev.clientY - sy), cv.clientHeight - n.offsetHeight)); draw(); };
      const up = () => { h.removeEventListener('pointermove', mv); h.removeEventListener('pointerup', up); h.removeEventListener('pointercancel', up); n.classList.remove('drag'); };
      h.addEventListener('pointermove', mv); h.addEventListener('pointerup', up); h.addEventListener('pointercancel', up); }));
    const bindRow = (r) => r.addEventListener('click', () => { const on = !r.classList.contains('on'); r.classList.toggle('on', on); r.setAttribute('aria-pressed', on); });
    rowsEl.querySelectorAll('.u-row').forEach(bindRow);
    add.addEventListener('click', () => { const m = more.shift(); if (!m) return; const r = document.createElement('button'); r.type = 'button'; r.className = 'u-row on'; r.setAttribute('aria-pressed', 'true');
      r.dataset.n = m[0]; r.dataset.w = m[1]; r.dataset.h = m[2]; r.innerHTML = '<span class="u-f">' + m[0] + '</span><span class="u-f u-num">' + m[1] + '</span><i>×</i><span class="u-f u-num">' + m[2] + '</span>';
      rowsEl.appendChild(r); bindRow(r); if (!more.length) add.hidden = true; fit(); draw(); });
    go.addEventListener('click', () => { const on = [...rowsEl.querySelectorAll('.u-row.on')];
      if (!on.length) { res.innerHTML = '<p class="u-empty">Включите хотя бы один формат</p>'; fit(); draw(); return; }
      go.disabled = true; go.innerHTML = '<i class="u-spin"></i>Генерация…'; e2.classList.add('flow'); res.innerHTML = '<p class="u-empty">Адаптация под ' + on.length + ' формат(а)…</p>'; fit(); draw();
      setTimeout(() => { res.innerHTML = on.map((r, i) => { const w = +r.dataset.w, h = +r.dataset.h, k = Math.min(64 / w, 40 / h);
          return '<div class="u-ri" style="animation-delay:' + i * 110 + 'ms"><span class="u-fw"><span class="u-fr" style="width:' + Math.max(8, Math.round(w * k)) + 'px;height:' + Math.max(8, Math.round(h * k)) + 'px"></span></span><small><b>' + r.dataset.n + '</b>' + w + '×' + h + '</small></div>'; }).join('');
        go.disabled = false; go.textContent = '✦ Сгенерировать снова'; e2.classList.remove('flow'); layout(); }, W8(1400)); });
    layout(); if ('ResizeObserver' in window) new ResizeObserver(layout).observe(cv); else addEventListener('resize', layout);
  });
  // 2 · One Launch: pick a photo and a format, generate the card
  document.querySelectorAll('.u-ol').forEach((u) => {
    const ph = [...u.querySelectorAll('.u-pho')], fm = [...u.querySelectorAll('.u-chip')], name = u.querySelector('.u-name'), go = u.querySelector('.u-go'), card = u.querySelector('.u-card'), bar = u.querySelector('.u-bar'), st = u.querySelector('.u-st');
    let img = 'bunny';
    const frame = () => { const b = fm.find((x) => x.getAttribute('aria-pressed') === 'true'), box = card.parentElement, w = +b.dataset.w, h = +b.dataset.h, k = Math.min((box.clientWidth - 30) / w, (box.clientHeight - 34) / h);
      card.style.width = Math.round(w * k) + 'px'; card.style.height = Math.round(h * k) + 'px'; };
    ph.forEach((p) => p.addEventListener('click', () => { ph.forEach((x) => x.setAttribute('aria-checked', x === p)); img = p.dataset.i; name.value = p.dataset.t; card.classList.remove('done'); st.textContent = 'Нажмите «Сгенерировать»'; }));
    fm.forEach((b) => b.addEventListener('click', () => { fm.forEach((x) => x.setAttribute('aria-pressed', x === b)); frame(); }));
    go.addEventListener('click', () => { go.disabled = true; card.classList.remove('done'); bar.classList.remove('run'); void bar.offsetWidth; bar.classList.add('run'); st.textContent = 'Собираю карточку по шаблону…';
      setTimeout(() => { card.style.setProperty('--im', 'var(--img-' + img + ')'); card.classList.add('done'); bar.classList.remove('run'); go.disabled = false;
        st.textContent = (name.value.trim() || 'Товар') + ' · ' + fm.find((x) => x.getAttribute('aria-pressed') === 'true').textContent + ' — готово'; }, W8(1300)); });
    frame(); if ('ResizeObserver' in window) new ResizeObserver(frame).observe(card.parentElement);
  });
  // 3 · Copywrite engine: a hint types a request, the answer streams in
  const CW = __CW__;
  document.querySelectorAll('.u-cw').forEach((u) => {
    const log = u.querySelector('.u-log'), inp = u.querySelector('.u-ph'), hs = [...u.querySelectorAll('.u-hint')];
    hs.forEach((b, i) => b.addEventListener('click', () => { const c = CW[i]; hs.forEach((x) => { x.disabled = true; }); inp.classList.add('typing'); let k = 0;
      const done = () => { hs.forEach((x) => { x.disabled = false; }); };
      const stream = (ai) => { ai.innerHTML = ''; let li = 0; const line = () => { if (li >= c.a.length) { if (c.f) { const f = c.f.split('|'); ai.insertAdjacentHTML('beforeend', '<span class="u-file">' + f[0] + '<em>' + f[1] + '</em></span>'); } done(); return; }
        const p = document.createElement('p'); ai.appendChild(p); const t = c.a[li++]; let j = 0; const ch = () => { j = Math.min(t.length, j + 3); p.textContent = t.slice(0, j); if (j < t.length) setTimeout(ch, W8(14)); else setTimeout(line, W8(120)); }; ch(); }; line(); };
      const send = () => { inp.classList.remove('typing'); inp.textContent = 'Спросите о чём угодно…'; log.innerHTML = '<p class="u-me"></p><div class="u-ai"><span class="u-dots"><i></i><i></i><i></i></span></div>';
        log.querySelector('.u-me').textContent = c.q; setTimeout(() => stream(log.querySelector('.u-ai')), W8(700)); };
      const type = () => { k = Math.min(c.q.length, k + 2); inp.textContent = c.q.slice(0, k); if (k < c.q.length) setTimeout(type, W8(22)); else setTimeout(send, W8(260)); }; type(); }));
  });
  // 4 · TRENDSWATCHING: filter, open a trend, build a scenario, send to nodes
  const TR = __TR__;
  document.querySelectorAll('.u-tr').forEach((u) => {
    const rows = [...u.querySelectorAll('.u-trr')], det = u.querySelector('.u-trd'), fl = [...u.querySelectorAll('.u-trh .u-chip')];
    const toast = (t) => { const o = u.querySelector('.u-toast'); if (o) o.remove(); const d = document.createElement('span'); d.className = 'u-toast'; d.textContent = t; u.appendChild(d); setTimeout(() => d.remove(), 2200); };
    const show = (i) => { const t = TR[i]; rows.forEach((r) => { const on = +r.dataset.i === i; r.classList.toggle('on', on); r.querySelector('.u-trb').setAttribute('aria-pressed', on); });
      det.style.animation = 'none'; void det.offsetWidth; det.style.animation = '';
      det.innerHTML = (t[5] ? '<div class="u-tri" style="background-image:var(--img-' + t[5] + ')"></div>' : '<div class="u-tri u-tx">«Короткий тред о том, что удерживает покупателей»</div>')
        + '<h4></h4><span class="u-by">' + t[2] + ' · ' + t[0] + '</span><h5>Почему в подборке</h5><p class="w"></p><h5>Как применить</h5><p class="h"></p>'
        + '<div class="u-trbt"><button type="button" class="u-btn u-mk">Создать сценарий →</button><button type="button" class="u-btn u-ghost u-nd">В ноды</button></div>';
      det.querySelector('h4').textContent = t[1]; det.querySelector('.w').textContent = t[6]; det.querySelector('.h').textContent = t[7];
      det.querySelector('.u-mk').addEventListener('click', (e) => { const b = e.currentTarget; b.disabled = true; b.innerHTML = '<i class="u-spin"></i>Пишу…';
        setTimeout(() => { b.remove(); const ul = document.createElement('ul'); ul.className = 'u-scn'; t[8].forEach((s, j) => { const li = document.createElement('li'); li.textContent = s; li.style.animationDelay = j * 120 + 'ms'; ul.appendChild(li); });
          det.querySelector('.u-trbt').before(ul); }, W8(900)); });
      det.querySelector('.u-nd').addEventListener('click', () => toast('Добавлено на холст: 3 ноды')); };
    rows.forEach((r) => { r.querySelector('.u-trb').addEventListener('click', () => show(+r.dataset.i));
      const bm = r.querySelector('.u-bm'); bm.addEventListener('click', () => { const on = bm.getAttribute('aria-pressed') !== 'true'; bm.setAttribute('aria-pressed', on); toast(on ? 'Сохранено в избранное' : 'Убрано из избранного'); }); });
    fl.forEach((b) => b.addEventListener('click', () => { fl.forEach((x) => x.setAttribute('aria-pressed', x === b)); const f = b.dataset.f; let first = -1;
      rows.forEach((r) => { const ok = !f || r.dataset.p === f; r.hidden = !ok; if (ok && first < 0) first = +r.dataset.i; }); if (first >= 0) show(first); }));
    show(0);
  });
  // 5 · Creative Predictor: variants, platform, «Оценить»
  document.querySelectorAll('.u-pd').forEach((u) => {
    const S = { any: [8.4, 6.1, 7.2], kaspi: [8.8, 5.7, 7.9], ig: [7.3, 7.9, 6.6] };
    const NOTE = { any: ['Товар крупно, название читается сразу', 'Товар мелкий, мало контраста', 'Чистый кадр, но не видно преимуществ'],
      kaspi: ['Как в каталоге: товар и преимущества', 'На белой витрине теряется', 'Хороший крупный план для карточки'],
      ig: ['Много текста для ленты', 'Атмосферный кадр — в ленте сильнее', 'Не хватает эмоции'] };
    const sc = u.querySelector('.u-sc'), go = u.querySelector('.u-go'), pl = [...u.querySelectorAll('.u-chip')], v3 = u.querySelector('.v3'), plus = u.querySelector('.u-plus'), slots = [...u.querySelectorAll('.u-slot[data-v]')];
    let k = 'any', rated = false;
    const clear = () => { rated = false; slots.forEach((s) => s.classList.remove('win')); sc.innerHTML = '<p class="u-empty">Нажмите «Оценить» — покажем, какой вариант сильнее</p>'; };
    const rate = () => { const vs = slots.filter((s) => !s.hidden).map((s) => +s.dataset.v), best = vs.reduce((a, b) => (S[k][b] > S[k][a] ? b : a), vs[0]);
      sc.innerHTML = vs.map((v, j) => '<div class="u-sr' + (v === best ? ' best' : '') + '" style="animation-delay:' + j * 90 + 'ms"><span>Вариант ' + (v + 1) + '</span><span class="u-sb"><i data-w="' + S[k][v] * 10 + '"></i></span><b>' + S[k][v].toFixed(1) + '</b><small>' + NOTE[k][v] + '</small></div>').join('');
      requestAnimationFrame(() => requestAnimationFrame(() => sc.querySelectorAll('.u-sb i').forEach((i) => { i.style.width = i.dataset.w + '%'; })));
      slots.forEach((s) => s.classList.toggle('win', +s.dataset.v === best)); rated = true; };
    go.addEventListener('click', () => { go.disabled = true; go.innerHTML = '<i class="u-spin"></i>Оцениваю…'; slots.forEach((s) => s.classList.remove('win')); sc.innerHTML = '<p class="u-empty">Анализ визуальной силы…</p>';
      setTimeout(() => { go.disabled = false; go.textContent = 'Оценить'; rate(); }, W8(1100)); });
    pl.forEach((b) => b.addEventListener('click', () => { pl.forEach((x) => x.setAttribute('aria-pressed', x === b)); k = b.dataset.k; if (rated) rate(); }));
    plus.addEventListener('click', () => { v3.hidden = false; plus.hidden = true; if (rated) rate(); });
    v3.querySelector('.u-x').addEventListener('click', () => { v3.hidden = true; plus.hidden = false; if (rated) rate(); else clear(); });
  });
  // 6 · Music & voice: tabs, chips, generate → player
  document.querySelectorAll('.u-mu').forEach((u) => {
    const tabs = [...u.querySelectorAll('.u-tabs button')], panes = [...u.querySelectorAll('.u-pane')], go = u.querySelector('.u-go'), pl = u.querySelector('.u-pl'), play = u.querySelector('.u-play'), wave = u.querySelector('.u-wave'), tm = u.querySelector('.u-time'), pt = u.querySelector('.u-pt');
    let mode = 'm', dur = 30, t0 = 0, el = 0, raf = 0, on = false;
    const fmt = (s) => Math.floor(s / 60) + ':' + String(Math.floor(s % 60)).padStart(2, '0');
    const paint = () => { const bars = wave.children, p = el / dur; for (let i = 0; i < bars.length; i++) bars[i].classList.toggle('on', i / bars.length < p); tm.textContent = fmt(el) + ' / ' + fmt(dur); };
    const stop = () => { on = false; cancelAnimationFrame(raf); play.textContent = '▶'; play.setAttribute('aria-label', 'Воспроизвести'); };
    const tick = (now) => { el = Math.min(dur, el + (now - t0) / 1000); t0 = now; paint(); if (el >= dur) { stop(); el = 0; return; } raf = requestAnimationFrame(tick); };
    play.addEventListener('click', () => { if (on) return stop(); on = true; play.textContent = '❚❚'; play.setAttribute('aria-label', 'Пауза'); t0 = performance.now(); raf = requestAnimationFrame(tick); });
    const chipset = (g) => g.querySelectorAll('.u-chip').forEach((b, _, all) => b.addEventListener('click', () => all.forEach((x) => x.setAttribute('aria-pressed', x === b))));
    panes.forEach(chipset);
    tabs.forEach((t) => t.addEventListener('click', () => { mode = t.dataset.t; tabs.forEach((x) => x.setAttribute('aria-selected', x === t)); panes.forEach((p) => { p.hidden = p.dataset.p !== mode; }); stop(); pl.hidden = true; go.textContent = mode === 'm' ? '✦ Сгенерировать' : '✦ Озвучить'; }));
    go.addEventListener('click', () => { stop(); pl.hidden = true; go.disabled = true; const lbl = go.textContent; go.innerHTML = '<i class="u-spin"></i>' + (mode === 'm' ? 'Генерация трека…' : 'Озвучка…');
      const pane = panes.find((p) => p.dataset.p === mode), txt = pane.querySelector('.u-in').value.trim() || (mode === 'm' ? 'Трек' : 'Озвучка'), ch = pane.querySelector('.u-chip[aria-pressed="true"]').textContent;
      setTimeout(() => { dur = mode === 'm' ? 30 : 4; el = 0; let seed = [...(txt + ch)].reduce((a, c) => a + c.charCodeAt(0), 7); const rnd = () => ((seed = (seed * 9301 + 49297) % 233280) / 233280);
        wave.innerHTML = Array.from({ length: 48 }, (_, i) => '<i style="height:' + Math.round(18 + rnd() * 70 * (mode === 'm' ? 1 : Math.sin(Math.PI * i / 48) + .3)) + '%"></i>').join('');
        pt.textContent = txt + ' · ' + ch; paint(); pl.hidden = false; go.disabled = false; go.textContent = lbl; }, W8(1200)); });
  });
  // 7 · Strategy: two questions → funnel and channels
  document.querySelectorAll('.u-sg').forEach((u) => {
    const P = [{ t: 'Воронка продаж', st: [['Охват', 30], ['Интерес', 30], ['Покупка', 40]], ch: ['Kaspi', 'Instagram', 'Яндекс РСЯ'] },
      { t: 'Воронка лидов', st: [['Охват', 35], ['Заявка', 40], ['Квалификация', 25]], ch: ['Instagram', 'TikTok', 'Яндекс РСЯ'] },
      { t: 'Воронка узнаваемости', st: [['Охват', 55], ['Вовлечение', 30], ['Запоминание', 15]], ch: ['TikTok', 'Instagram', 'Threads'] }];
    const qs = [...u.querySelectorAll('.u-q')], bar = u.querySelector('.u-prog i'), step = u.querySelector('.u-sl em'), opts = [...u.querySelectorAll('.u-opt')], rng = u.querySelector('input[type=range]'), bv = u.querySelector('.u-bv');
    let g = 0; const go = (n) => { qs.forEach((q) => { q.hidden = +q.dataset.q !== n; }); bar.style.width = (n === 1 ? 50 : 100) + '%'; step.textContent = n === 3 ? 'план готов' : n + ' из 2'; };
    opts.forEach((o) => o.addEventListener('click', () => { opts.forEach((x) => x.setAttribute('aria-pressed', x === o)); g = +o.dataset.g; }));
    rng.addEventListener('input', () => { bv.textContent = '$' + (+rng.value).toLocaleString('ru-RU'); });
    qs[0].querySelector('.u-next').addEventListener('click', () => go(2));
    qs[1].querySelector('.u-next').addEventListener('click', () => { const p = P[g], b = +rng.value; u.querySelector('.u-rt').textContent = p.t + ' · $' + b.toLocaleString('ru-RU') + ' в месяц';
      const fun = u.querySelector('.u-fun'); fun.innerHTML = p.st.map((s, j) => '<div class="u-fr2" style="animation-delay:' + j * 100 + 'ms"><span>' + s[0] + '</span><i style="width:0" data-w="' + (s[1] / Math.max(...p.st.map((x) => x[1]))) * 100 + '"></i><b>$' + Math.round(b * s[1] / 100).toLocaleString('ru-RU') + '</b></div>').join('');
      u.querySelector('.u-chs').innerHTML = p.ch.map((c) => '<span>' + c + '</span>').join(''); go(3);
      requestAnimationFrame(() => requestAnimationFrame(() => fun.querySelectorAll('i').forEach((i) => { i.style.width = i.dataset.w + '%'; }))); });
    u.querySelector('.u-link').addEventListener('click', () => go(1));
  });
  // 8 · Co-authors: invite by e-mail, chat
  document.querySelectorAll('.u-ms').forEach((u) => {
    const inv = u.querySelector('.u-inv'), msg = u.querySelector('.u-msg'), cl = u.querySelector('.u-cl'), ml = u.querySelector('.u-ml'), sf = u.querySelector('.u-send2');
    const R = ['Отлично, запускаю адаптацию под Kaspi', 'Добавила в проект, глянь холст', 'Готово — все форматы в архиве проекта']; let ri = 0;
    const bubble = (t, me) => { const d = document.createElement('div'); d.className = 'u-m' + (me ? ' me' : ''); const p = document.createElement('p'); p.textContent = t; d.appendChild(p); ml.appendChild(d); ml.scrollTop = ml.scrollHeight; };
    inv.addEventListener('submit', (e) => { e.preventDefault(); const i = inv.querySelector('input'), v = i.value.trim();
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v)) { msg.textContent = 'Введите почту, например colleague@company.kz'; msg.classList.add('err'); return; }
      msg.classList.remove('err'); msg.textContent = 'Приглашение отправлено'; i.value = ''; const li = document.createElement('li'), n = v.split('@')[0];
      li.innerHTML = '<span class="u-av" style="--h:' + (n.length * 47 % 360) + '"></span><span><b></b><small>приглашение отправлено</small></span>'; li.querySelector('.u-av').textContent = n[0].toUpperCase(); li.querySelector('b').textContent = n; cl.appendChild(li); });
    sf.addEventListener('submit', (e) => { e.preventDefault(); const i = sf.querySelector('input'), v = i.value.trim(); if (!v) return; bubble(v, true); i.value = '';
      setTimeout(() => bubble(R[ri++ % R.length], false), W8(900)); });
  });
"""


def js():
    import json
    cw = [{'q': q, 'a': a, 'f': f} for _, q, a, f in CW]
    return JS.replace('__CW__', json.dumps(cw, ensure_ascii=False)).replace('__TR__', json.dumps(TR, ensure_ascii=False))
