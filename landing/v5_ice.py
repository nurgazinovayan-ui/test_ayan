"""Variant 5 · Ice — the dark oneflow.art landing.

Hero (headline, buttons, models line, the «до 50%» footnote), then every product mode as a tab (editorial
«Ноды / Генерация / …» line, mockup D9): the left column states the mode's benefits, the right window plays a short
looping animation of how the mode works. Pricing, FAQ and the closing card follow. Pricing data, FAQ, the support
form, legal dialogs, the CMS hook and the header/footer come from v4_porcelain so both versions stay in sync.
Images are CSS custom properties (one url each), so the single-file build stores every picture once.
"""
import os
import re

import protos
import v4_porcelain as v

HERE = os.path.dirname(os.path.abspath(__file__))
APP, REG, MARK, IMGS = v.APP, v.REG, v.MARK, v.IMGS
reg = v.reg

NAV = [('#modes', 'Возможности'), ('#tpl', 'Для бизнеса'), ('#ai', 'Ассистент'), ('#pricing', 'Цены'), ('#faq', 'Вопросы')]

# ------------------------------------------------------------------------------------------------ tabs content
# key, tab label, eyebrow-free headline, lead, four benefits (big value, label, detail)
TABS = [
    ('nodes', 'Ноды и адаптация', 'Одно фото — все рекламные форматы',
     'Соберите цепочку на холсте: фото → адаптация → готовые размеры под каждую площадку. Одним запуском.',
     [('∞', 'любых размеров', 'Свой размер или пресеты Kaspi, GDN, РСЯ, BYYD, Discovery'), ('PSD', 'с двумя слоями', 'Чистый фон отдельно, текст и лого — отдельно'),
      ('30+', 'нейросетей', 'Фото, видео и вектор на одном холсте'), ('1', 'клик', '«Сохранить все» — сразу во всех форматах')]),
    ('gen', 'Генерация', 'Фото и видео по промпту',
     'Опишите идею или прикрепите референс — получите фото до 4K или видео со звуком. Модели переключаются в один клик.',
     [('11', 'моделей фото', 'Nano Banana Pro, GPT Image, Seedream, Recraft и другие'), ('7', 'моделей видео', 'Kling 3.0, Veo 3.1, Seedance, Hailuo, FLUX'),
      ('4K', 'разрешение', 'Зависит от выбранной модели'), ('2', 'кадра', 'Начальный и конечный кадр для видео')]),
    ('tpl', 'Шаблоны для бизнеса', 'Студийное фото — со снимка на телефон',
     'Выберите шаблон под нишу, загрузите фото — получите кадр как от фотографа. Без студии, выезда и новой съёмки на каждую позицию.',
     [('мин', 'вместо дней', 'Новое блюдо, машина или квартира — фото в тот же день'), ('5', 'шаблонов', 'HoReCa, Квартира, Авто, Техника, Мебель'),
      ('2K', 'высокое разрешение', 'Для меню, каталога, объявлений и карточек'), ('∞', 'размеров', 'Сразу подогнать под любую площадку')]),
    ('launch', 'One Launch', 'Фото товара → рекламная кампания',
     'Фото, название и преимущества — на выходе карточки под форматы и готовые тексты постов для Instagram.',
     [('14', 'шаблонов карточек', 'Техника, бытовые приборы, детские товары'), ('3', 'формата', '1:1, 9:16 и 3:2 — одним запуском'),
      ('ИИ', 'палитра и тексты', 'Подберёт цвета и напишет посты'), ('1', 'фото товара', 'Больше ничего не нужно')]),
    ('motion', 'Motion Engine', 'Рекламный ролик из ваших фото',
     'Сначала статичная раскадровка — видно каждую сцену и текст. Понравилось — жмёте «В рендер» и получаете MP4.',
     [('$0', 'за рендер', 'Видео собирается прямо в браузере'), ('4K', 'любой формат', 'Одна раскадровка → Reels, YouTube, лента, баннер'),
      ('3–60 с', 'длительность', 'Ползунком — сцены подстроятся сами'), ('Реф', 'повтор стиля', 'Покажите ролик — повторим ритм и цвета')]),
    ('copy', 'Copywrite engine', 'Тексты и документы — до готового файла',
     'Объявления, SEO-описания, контент-планы и проверка текста. Ответ скачивается как Word, Excel или PowerPoint.',
     [('3', 'формата файлов', 'Word, Excel, PowerPoint'), ('6', 'быстрых подсказок', 'Заголовки, SEO, контент-план, проверка'),
      ('4', 'файла на вход', 'Фото, DOCX, XLSX, PPTX, CSV — до 4 МБ'), ('Проекты', 'и история', 'Чаты по папкам, поиск, закрепление')]),
    ('music', 'Музыка и голос', 'Трек по описанию и озвучка голосом',
     'Музыка под ролик — по жанру и настроению, со своими словами. Озвучка фразы — бодро, спокойно или по-деловому.',
     [('2', 'режима', 'Музыка и речь'), ('5', 'языков озвучки', 'Русский, английский, казахский, испанский, немецкий'),
      ('MP3', 'и WAV', 'Скачать в один клик'), ('Свои', 'слова песни', 'Трек на ваш текст')]),
    ('trend', 'Trendswatching', 'Тренды — сразу в идею для бренда',
     'Посты TikTok, Instagram и Threads с разбором: почему в подборке и как применить. Одним кликом — в сценарий или ноды.',
     [('3', 'площадки', 'TikTok, Instagram, Threads'), ('30', 'дней', 'Сегодня, 7 и 30 дней'),
      ('3', 'региона', 'СНГ, Европа, Америка + поиск'), ('1', 'клик', '«Создать сценарий» или «В ноды»')]),
    ('pred', 'Creative Predictor', 'Какой креатив сильнее — до запуска',
     'Загрузите 1–3 варианта и площадку. ONEFLOW оценит каждый и объяснит, что улучшить, — ещё до первого показа.',
     [('1–10', 'оценка', 'С сильными сторонами и выводом'), ('6', 'критериев', 'Контраст, взгляд, текст, CTA, крючок, шум'),
      ('3', 'варианта', 'Сравнение надёжнее одиночной оценки'), ('0', 'бюджета на слабый', 'Отсеете до показов')]),
    ('strat', 'Стратегия', 'Маркетинговая стратегия под нишу',
     'Цель, продукт и бюджет — на выходе план: кому продавать, что говорить, где продвигаться и что создавать.',
     [('2', 'шага', 'Цель и описание продукта'), ('3', 'сценария', 'Основной, рост, экономный — с CAC и риском'),
      ('A/B', 'эксперименты', 'Реестр тестов и расчёт победителя'), ('1', 'клик до контента', '«Создать workflow» — сразу в ноды')]),
    ('ai', 'ИИ-ассистент', 'Ассистент соберёт цепочку — запускаете вы',
     'Разберёт нишу, подскажет идеи, напишет промпт и сам построит схему нод на холсте. Финальное решение — за вами.',
     [('01', 'разбор ниши', 'Аудитория, конкуренты, какой контент нужен'), ('02', 'промпты', 'Пишет и улучшает под модель'),
      ('03', 'схема нод', 'Строит на холсте по описанию задачи'), ('04', 'запуск', 'Вы проверяете и жмёте «Запустить»')]),
    ('team', 'Соавторы', 'Работайте командой в одном окне',
     'Пригласите коллегу по почте и обсуждайте работу во встроенном мессенджере — в личных чатах и группах.',
     [('@', 'приглашение', 'По почте — принял и уже в контактах'), ('Группы', 'под проекты', 'Запуск, кампания или вся команда'),
      ('Онлайн', 'статус', 'Видно, кто сейчас в сети'), ('0', 'лишних чатов', 'Обсуждение рядом с работой')]),
]

ICONS = {
    'nodes': '<circle cx="5" cy="6" r="2.5"/><circle cx="19" cy="6" r="2.5"/><circle cx="12" cy="18" r="2.5"/><path d="M7.5 6h9M6.5 8l4.3 7.8M17.5 8l-4.3 7.8"/>',
    'gen': '<path d="M12 3l1.8 4.7L18.5 9.5l-4.7 1.8L12 16l-1.8-4.7L5.5 9.5l4.7-1.8z"/>',
    'tpl': '<rect x="3" y="5" width="18" height="14" rx="3"/><circle cx="9" cy="10" r="2"/><path d="M21 16l-5-5-8 8"/>',
    'launch': '<path d="M5 15c-1.5 1.5-2 5-2 5s3.5-.5 5-2"/><path d="M9 15l-3-3 7-8c2.5-1.5 5.5-1 5.5-1s.5 3-1 5.5z"/>',
    'motion': '<rect x="3" y="6" width="13" height="12" rx="2.5"/><path d="M16 10.5l5-3v9l-5-3"/>',
    'copy': '<path d="M5 4h10l4 4v12H5z"/><path d="M8 11h8M8 14.5h8M8 18h5"/>',
    'music': '<path d="M9 18V5l11-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="17" cy="16" r="3"/>',
    'trend': '<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
    'pred': '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    'strat': '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.2"/>',
    'ai': '<path d="M4 6a2 2 0 012-2h12a2 2 0 012 2v9a2 2 0 01-2 2H9l-5 4z"/><path d="M9 10h.01M15 10h.01"/>',
    'team': '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.8-3.6 3.4-5.5 6.5-5.5s5.7 1.9 6.5 5.5"/><circle cx="17.5" cy="9" r="2.5"/><path d="M17 14.5c2.4.2 4 1.8 4.5 4.5"/>',
}


def icon(k, s=14):
    return (f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true">{ICONS[k]}</svg>')


def im(name, cls='im', extra=''):
    return f'<i class="{cls}" style="background-image:var(--img-{name}){extra}"></i>'


CUR = '<svg class="cur" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 2l15 9-6.5 1.5L10 20z" fill="#04141b" stroke="#fff" stroke-width="1.5"/></svg>'


def steps(n):
    return '<div class="stp">' + ''.join(f'<b class="s{i}"></b>' for i in range(n)) + '</div>'


# Each window: (title, status, inner html). Inner canvas is 520×440, scaled to the column by CSS/JS.
WIN = {
    'nodes': ('Холст · Весна-кампания', '4 из 4 готово',
              '<div class="dots"></div>'
              '<svg class="wires" width="520" height="440" viewBox="0 0 520 440" aria-hidden="true"><path class="w0" d="M146 128 C170 128,166 168,186 168"/>'
              '<path class="w1" d="M336 210 C380 210,400 79,442 79"/><path class="w2" d="M336 210 C356 210,354 176,374 176"/><path class="w3" d="M336 210 C356 210,354 245,374 245"/>'
              '<path class="w4" d="M336 210 C356 210,354 299,374 299"/></svg>'
              f'<div class="nd n1"><h6>Изображение</h6>{im("bunny")}</div>'
              '<div class="nd n2"><h6>Адаптация</h6><ul><li>Stories 9:16<b class="t1">✓</b></li><li>1200×628<b class="t2">✓</b></li><li>РСЯ 1080×450<b class="t3">✓</b></li>'
              '<li>Kaspi 1125×330<b class="t4">✓</b></li></ul><span class="go">✦ Сгенерировать</span></div>'
              f'<figure class="rf r1">{im("bunny")}<figcaption>9:16</figcaption></figure><figure class="rf r2">{im("bunny")}<figcaption>1200×628</figcaption></figure>'
              f'<figure class="rf r3">{im("bunny")}<figcaption>1080×450</figcaption></figure><figure class="rf r4">{im("bunny")}<figcaption>1125×330</figcaption></figure>' + CUR),
    'gen': ('Генерация · Фото', 'Nano Banana Pro · 2K',
            '<div class="pr"><span class="ty">Наушники на бетонном подиуме, мягкий свет, минимализм</span><span class="go">Сгенерировать</span></div>'
            '<div class="gmods"><span class="on">Фото</span><span>Видео</span><span>4 варианта</span><span>1:1</span><span>2K</span></div>'
            '<div class="g4">' + ''.join(f'<figure class="gi g{i}">{im(n)}</figure>' for i, n in enumerate(['airbuds', 'speaker', 'watch', 'powerbank'])) + '</div>'
            f'<div class="vid">{im("airbuds", "im vt")}<div><b>Видео из кадра 2</b><small>Kling 3.0 · 5 с · 1080p</small><span class="pb"><i></i></span></div></div>'),
    'tpl': ('Шаблоны · Техника', 'готово за 40 с',
            '<div class="chips"><span>HoReCa</span><span>Квартира</span><span>Авто</span><span class="on">Техника</span><span>Мебель</span></div>'
            f'<div class="bf"><div class="bb">{im("coffee")}<em>Снимок на телефон</em></div><div class="aa">{im("coffee")}<em>Шаблон «Техника»</em></div><span class="hd"></span></div>'
            '<span class="k2">2K · 2048×2048</span>'
            '<div class="tri"><span class="a1"><b>1</b>Шаблон</span><span class="a2"><b>2</b>Ваше фото</span><span class="a3"><b>3</b>Студийный кадр</span></div>'),
    'launch': ('One Launch · Кофемашина', 'кампания готова',
               '<ul class="ls"><li class="l1">Анализирую фото<b>✓</b></li><li class="l2">Генерирую 1:1<b>✓</b></li><li class="l3">Генерирую 9:16<b>✓</b></li><li class="l4">Пишу тексты<b>✓</b></li></ul>'
               f'<figure class="oc c1">{im("coffee")}<figcaption>1:1</figcaption></figure><figure class="oc c2">{im("blender")}<figcaption>9:16</figcaption></figure>'
               f'<figure class="oc c3">{im("airfryer")}<figcaption>3:2</figcaption></figure>'
               '<div class="ocap"><b>Текст для Instagram</b>Утро с идеальным эспрессо ☕ Aroma One — капучино за минуту, −26% всю неделю.</div>'
               '<div class="ogal"><div class="gt">' + ''.join(im(n, 'gc') for n in IMGS) * 2 + '</div></div>'),
    'motion': ('Motion Engine · 15 с', 'рендер в браузере',
               '<div class="ms">'
               + ''.join(f'<div class="scn x{i}"><div class="si">{im(n) if n else ""}<b>{t}</b></div><p>{m}</p></div>' for i, (n, t, m) in enumerate(
                   [('watch', 'Время — ваше', '01 · zoom-in'), ('airbuds', 'Звук без проводов', '02 · pan'), ('', 'ONEFLOW', '03 · текст'),
                    ('speaker', 'Громко', '04 · glitch'), ('coffee', 'Каждое утро', '05 · drift'), ('', 'Попробовать →', '06 · CTA')])) + '</div>'
               '<div class="tl"><i></i><i></i><i></i><i></i><i></i><i></i><span class="ph"></span></div>'
               '<div class="rn">Рендер · вариант 2<small>9:16 · 1080×1920 · 30 fps · MP4</small><span class="pb"><i></i></span></div>'
               f'<div class="ph9">{im("airbuds", "im p1")}{im("watch", "im p2")}{im("speaker", "im p3")}<b>Звук без проводов</b><small>−20% сегодня</small></div>'
               '<div class="ok"><span class="o1">✓ 16:9 · 4K</span><span class="o2">✓ 1:1 · 1080</span><span class="o3">✓ 9:16 · 1080</span></div>'),
    'copy': ('Copywrite engine', 'ONEFLOW AI',
             '<p class="me">Составь контент-план на октябрь для кофейни: 3 поста в неделю, Instagram и Telegram</p>'
             '<div class="ty3"><i></i><i></i><i></i></div>'
             '<div class="ans"><p class="a1"><b>Неделя 1 · Сезонное меню</b> — пн: тыквенный латте крупным планом</p><p class="a2">ср: рилс «как варим» · пт: опрос «какой сироп»</p>'
             '<p class="a3"><b>Неделя 2 · Доставка</b> — до 30 минут, промокод для новых</p></div>'
             '<div class="dcard"><span class="dw">W</span><span><b>Контент-план на октябрь.docx</b><small>Документ Word · 12 постов</small></span><em>Скачать</em></div>'
             '<div class="qp"><span>Заголовки</span><span>SEO-описание</span><span>Контент-план</span><span>Проверить текст</span></div>'),
    'music': ('Музыка и аудио', 'трек готов',
              '<div class="tg"><span class="on">♫ Музыка</span><span>◉ Речь</span></div>'
              '<div class="fl"><small>Промпт</small>Энергичный поп-рок с яркими гитарами для рекламы наушников</div>'
              '<div class="gn"><span>Pop</span><span class="on">Rock</span><span>Lo-fi</span><span>Jazz</span><span>Ambient</span><span>Electronic</span></div>'
              '<div class="wv">' + ''.join(f'<i style="--h:{h}%;--d:{(i * 37) % 900}ms"></i>' for i, h in enumerate(
                  [30, 55, 80, 45, 90, 60, 35, 70, 95, 50, 40, 75, 85, 30, 65, 90, 55, 45, 80, 60, 35, 70, 50, 85, 40, 65, 95, 55, 30, 75, 60, 45, 80, 50, 70, 35])) + '</div>'
              '<div class="pl"><span class="pp">▶</span><span class="pb"><i></i></span><small>0:30 · MP3</small></div>'),
    'trend': ('Тренды · Все площадки', 'за 7 дней',
              '<div class="tf"><div class="tt">'
              + ''.join(f'<div class="tc"><span class="pf {p.lower()}">{p}</span><b>{t}</b><small>{a}</small><em>{m}</em></div>' for p, t, a, m in (
                  ('TikTok', 'Товар в неожиданном масштабе', '@planet.noah', '318K'), ('Instagram', 'Один предмет — три сценария', '@mari.daily', '132K'),
                  ('Threads', 'Почему покупатели возвращаются', '@brand_thinker', '1.9K'), ('TikTok', 'Честный обзор вместо рекламы', '@katya.review', '174K'),
                  ('Instagram', 'Распаковка без лица в кадре', '@studio.grain', '78K')) * 2) + '</div></div>'
              '<div class="td"><span class="pf tiktok">TikTok</span><b>Товар в неожиданном масштабе</b><small>Лайков 318K</small>'
              '<h6>Почему в подборке</h6><p>Гигантский товар в обычной сцене — зритель останавливается на первой секунде.</p>'
              '<h6>Как применить</h6><p>Покажите свой товар крупнее жизни: наушники размером с диван.</p><span class="go">Создать сценарий</span><span class="g2">В ноды</span></div>'),
    'pred': ('Creative Predictor · Kaspi', 'оценено 3 из 3',
             f'<div class="pc p1"><div class="pi">{im("speaker")}</div><div class="ps">6.8<small>/10</small></div><span class="br"><i style="--w:68%"></i></span></div>'
             f'<div class="pc p2"><span class="wb">Сильнее остальных</span><div class="pi">{im("airbuds")}</div><div class="ps">8.9<small>/10</small></div><span class="br"><i style="--w:89%"></i></span></div>'
             f'<div class="pc p3"><div class="pi">{im("watch")}</div><div class="ps">7.4<small>/10</small></div><span class="br"><i style="--w:74%"></i></span></div>'
             '<span class="scan"></span>'
             '<div class="cr">' + ''.join(f'<span class="k{i}">{a}<b{" class=w" if b == "6" else ""}>{b}</b></span>' for i, (a, b) in enumerate(
                 [('Контраст', '9'), ('Фокус взгляда', '9'), ('Читаемость', '8'), ('Заметность CTA', '9'), ('Эмоц. крючок', '8'), ('Визуальный шум', '6')])) + '</div>'
             '<div class="vd"><b>Вывод:</b> вариант 2 сильнее — товар крупно, CTA читается в превью. Уберите лишний фон у варианта 1.</div>'),
    'strat': ('Стратегия · Кофейня', 'оценка 82/100',
              '<div class="sq"><small>Какой результат вы хотите?</small><span class="on">Продажи</span><span>Лиды</span><span>Узнаваемость</span>'
              '<small>Бюджет на месяц</small><div class="sl"><i></i><b>$500</b></div></div>'
              '<div class="ring2"><span>82<small>/100</small></span></div>'
              '<div class="fnl"><div><small>Осведомлённость</small><i style="--w:100%"></i></div><div><small>Рассмотрение</small><i style="--w:62%"></i></div><div><small>Конверсия</small><i style="--w:28%"></i></div></div>'
              '<div class="sg"><span class="e1"><b>Студенты</b>обед и вечер · 40%</span><span class="e2"><b>Офис</b>доставка · 35%</span><span class="e3"><b>Семьи</b>выходные · 25%</span></div>'
              '<span class="go">Создать workflow →</span>'),
    'ai': ('ИИ-ассистент', 'пример',
           '<p class="me">Кофейня, доставка. Нужны сторис на неделю под новое зимнее меню.</p>'
           '<div class="ab"><h6 class="h1">Аудитория</h6><p class="q1">студенты и офис — заказывают в обед и вечером</p>'
           '<h6 class="h2">Промпт</h6><p class="q2 pp">Зимний латте на тёплом фоне, мягкий утренний свет, крупный план</p>'
           '<h6 class="h3">Схема нод</h6><div class="nn"><span class="z1">Фото</span><i class="z2">→</i><span class="z3">Генерация фото</span><i class="z4">→</i><span class="z5">Адаптация 9:16</span></div></div>'
           '<div class="rnb"><span>Проверьте схему и нажмите «Запустить»</span><b>Запустить пайплайн ▸</b></div>' + CUR),
    'team': ('Мессенджер', '3 в сети',
             '<div class="ct"><small>Контакты</small><span class="u on"><i>А</i>Аружан<em></em></span><span class="u on"><i>Д</i>Данияр<em></em></span>'
             '<span class="u"><i>М</i>Мадина<em></em></span><span class="u new"><i>А</i>Айдос<em></em></span></div>'
             '<div class="cm"><div class="mh">Проект «Весна»<small>группа · 4 участника</small></div>'
             f'<p class="m1"><b>Аружан</b>Сторис готовы — глянешь 9:16?{im("bunny", "im mt")}</p><p class="m2 mine">Супер, беру в работу</p>'
             '<p class="m3"><b>Данияр</b>Тексты закинул в проект, проверьте CTA</p><div class="ty3"><i></i><i></i><i></i></div></div>'
             '<div class="toast">Айдос теперь в ваших контактах</div>'),
}


def kf(name, a, b=92, hide='opacity:0;transform:translateY(8px) scale(.97)', show='opacity:1;transform:none'):
    """Looping reveal: hidden until a%, shown from a+4% to b%, hidden again for the loop restart."""
    return f'@keyframes {name}{{0%,{a}%{{{hide}}}{a + 4}%,{b}%{{{show}}}{min(b + 4, 100)}%,100%{{{hide}}}}}'


ANIM = [
    # nodes
    kf('nd-t1', 14), kf('nd-t2', 19), kf('nd-t3', 24), kf('nd-t4', 29),
    kf('nd-r1', 50), kf('nd-r2', 56), kf('nd-r3', 62), kf('nd-r4', 68),
    '@keyframes nd-w{0%,8%{stroke-dashoffset:120}16%,92%{stroke-dashoffset:0}96%,100%{stroke-dashoffset:120}}',
    '@keyframes nd-wo{0%,44%{stroke-dashoffset:220}54%,92%{stroke-dashoffset:0}96%,100%{stroke-dashoffset:220}}',
    '@keyframes cur-n{0%,30%{transform:translate(440px,400px)}40%,46%{transform:translate(296px,258px)}43%{transform:translate(296px,258px) scale(.82)}70%,100%{transform:translate(470px,400px)}}',
    '@keyframes go-p{0%,41%,47%,100%{box-shadow:0 0 0 0 rgba(155,232,255,0)}43%{box-shadow:0 0 0 8px rgba(155,232,255,.25)}}',
    # gen
    '@keyframes ty{0%{clip-path:inset(0 100% 0 0)}24%,92%{clip-path:inset(0 0 0 0)}100%{clip-path:inset(0 100% 0 0)}}',
    kf('gi0', 30), kf('gi1', 35), kf('gi2', 40), kf('gi3', 45), kf('gv', 55),
    '@keyframes pb{0%,58%{width:0}84%,100%{width:100%}}',
    # tpl
    '@keyframes hd{0%,8%{left:88%}38%{left:12%}62%,92%{left:50%}100%{left:88%}}',
    '@keyframes aa{0%,8%{clip-path:inset(0 0 0 88%)}38%{clip-path:inset(0 0 0 12%)}62%,92%{clip-path:inset(0 0 0 50%)}100%{clip-path:inset(0 0 0 88%)}}',
    kf('k2', 62), '@keyframes tri{0%,100%{background:var(--s2);color:var(--muted)}5%,30%{background:var(--ac);color:var(--acink)}35%{background:var(--s2);color:var(--muted)}}',
    # launch
    kf('l1', 6), kf('l2', 18), kf('l3', 30), kf('l4', 42), kf('oc1', 20), kf('oc2', 32), kf('oc3', 40), kf('cap', 50),
    '@keyframes mq{to{transform:translateX(-50%)}}',
    # motion
    '@keyframes sc-on{0%,100%{box-shadow:0 0 0 1px var(--line)}2%,14%{box-shadow:0 0 0 2px var(--ac)}16%{box-shadow:0 0 0 1px var(--line)}}',
    '@keyframes ph{0%{left:2%}60%,100%{left:98%}}', '@keyframes rpb{0%,58%{width:0}88%,100%{width:100%}}',
    kf('o1', 66), kf('o2', 74), kf('o3', 84),
    '@keyframes p1{0%,30%{opacity:1}33%,96%{opacity:0}100%{opacity:1}}', '@keyframes p2{0%,30%{opacity:0}33%,63%{opacity:1}66%,100%{opacity:0}}',
    '@keyframes p3{0%,63%{opacity:0}66%,96%{opacity:1}100%{opacity:0}}',
    # copy
    kf('me', 3), '@keyframes ty3{0%,10%{opacity:0}12%,26%{opacity:1}28%,100%{opacity:0}}', kf('a1', 28), kf('a2', 34), kf('a3', 40), kf('dcard', 50),
    '@keyframes dot{50%{transform:translateY(-4px);opacity:.4}}',
    # music
    '@keyframes wv{0%,100%{transform:scaleY(.25)}50%{transform:scaleY(1)}}', '@keyframes mpb{0%{width:0}92%,100%{width:100%}}',
    # trend
    '@keyframes tv{to{transform:translateY(-50%)}}', kf('td', 20), '@keyframes tg{0%,58%,66%,100%{box-shadow:0 0 0 0 rgba(155,232,255,0)}62%{box-shadow:0 0 0 8px rgba(155,232,255,.22)}}',
    # pred
    kf('pc1', 2), kf('pc2', 6), kf('pc3', 10), '@keyframes scan{0%,14%{left:0;opacity:0}16%{opacity:1}40%{left:100%;opacity:1}42%,100%{left:100%;opacity:0}}',
    kf('ps', 44), '@keyframes br{0%,44%{width:0}56%,92%{width:var(--w)}100%{width:0}}',
    '@keyframes win{0%,58%,100%{box-shadow:0 0 0 1px var(--line)}62%,92%{box-shadow:0 0 0 2px var(--ac),0 20px 50px -20px rgba(155,232,255,.45)}}', kf('wb', 60),
    kf('k0', 64), kf('k1', 66), kf('kk2', 68), kf('k3', 70), kf('k4', 72), kf('k5', 74), kf('vd', 80),
    # strat
    '@property --p{syntax:"<number>";inherits:false;initial-value:0}', '@keyframes ring{0%,10%{--p:0}50%,92%{--p:82}100%{--p:0}}',
    '@keyframes fn{0%,20%{width:0}50%,92%{width:var(--w)}100%{width:0}}', kf('e1', 52), kf('e2', 58), kf('e3', 64), '@keyframes sl{0%,4%{width:10%}24%,100%{width:50%}}',
    # ai
    kf('h1', 8), kf('q1', 11), kf('h2', 20), kf('q2', 23), kf('h3', 34), kf('z1', 38), kf('z2', 42), kf('z3', 45), kf('z4', 49), kf('z5', 52), kf('rnb', 58),
    '@keyframes cur-a{0%,58%{transform:translate(470px,420px)}68%,74%{transform:translate(420px,388px)}71%{transform:translate(420px,388px) scale(.82)}86%,100%{transform:translate(500px,430px)}}',
    '@keyframes run{0%,70%,78%,100%{box-shadow:0 0 0 0 rgba(155,232,255,0)}72%{box-shadow:0 0 0 8px rgba(155,232,255,.3)}}',
    # team
    kf('m1', 8), kf('m2', 26), kf('m3', 44), '@keyframes ty3b{0%,54%{opacity:0}56%,74%{opacity:1}76%,100%{opacity:0}}', kf('toast', 64, 88), kf('nw', 64),
]

TABS_CSS = """
/* ---------- tabs: the modes as one editorial line (D9) */
#modes .sh { margin-bottom: 34px; }
.ed { max-width: 1040px; margin: 0 auto; text-align: center; font: 700 31px/1.42 var(--d); letter-spacing: -.03em; }
.ed button { border: 0; padding: 0; background: none; font: inherit; letter-spacing: inherit; color: var(--dim); cursor: pointer; white-space: nowrap; position: relative; transition: color .25s; }
.ed button:hover { color: var(--ink2); } .ed button[aria-selected="true"] { color: var(--ink); }
.ed button[aria-selected="true"]::after { content: ''; position: absolute; left: 0; right: 0; bottom: -2px; height: 3px; border-radius: 2px; background: var(--ac); box-shadow: 0 0 14px var(--ac); }
.ed .sl { margin: 0 .32em; color: var(--s3); font-style: normal; }
.mpanel { margin-top: 44px; padding: 44px; border-radius: 28px; background: rgba(155,232,255,.028); box-shadow: inset 0 0 0 1px var(--line), 0 40px 90px -40px rgba(0,0,0,.8); }
.tp[hidden] { display: none; }
.stage { display: grid; grid-template-columns: minmax(0, 1fr) 520px; gap: 48px; align-items: center; min-height: 600px; }
.lt .eb { display: inline-flex; align-items: center; gap: 8px; padding: 6px 12px 6px 7px; border-radius: 99px; background: rgba(255,255,255,.05); box-shadow: inset 0 0 0 1px var(--line); font: 600 13px var(--d); color: var(--ink2); }
.lt .eb i { display: grid; place-items: center; width: 24px; height: 24px; border-radius: 7px; background: var(--ac); color: var(--acink); }
.lt h3 { margin-top: 18px; font: 700 clamp(34px, 3.9vw, 50px)/1.03 var(--d); letter-spacing: -.045em; }
.lt .lead { margin-top: 16px; max-width: 480px; font-size: 17.5px; color: var(--ink2); }
.bens { margin: 28px 0 0; padding: 0; list-style: none; display: grid; grid-template-columns: 1fr 1fr; gap: 22px 28px; }
.bens b { display: block; font: 700 34px/1 var(--d); letter-spacing: -.04em; color: var(--num); } .bens span { display: block; margin-top: 7px; font: 600 14.5px var(--d); }
.bens small { display: block; margin-top: 3px; font-size: 13.5px; line-height: 1.4; color: var(--muted); }
.lt .acts { justify-content: flex-start; margin-top: 30px; }
/* ---------- window */
.win { border-radius: 20px; background: var(--s1); box-shadow: inset 0 0 0 1px var(--line), 0 40px 90px -36px rgba(0,0,0,.9); overflow: hidden; }
.win .bar { display: flex; align-items: center; gap: 7px; height: 42px; padding: 0 16px; border-bottom: 1px solid var(--line); font: 400 12px var(--m); color: var(--muted); }
.win .bar i { width: 10px; height: 10px; border-radius: 50%; background: var(--s3); } .win .bar span { margin-left: 10px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.win .bar em { margin-left: auto; font-style: normal; white-space: nowrap; color: var(--ac); } .win .bar em::before { content: '● '; }
.vw { position: relative; height: calc(440px * var(--k, 1)); overflow: hidden; background: var(--s0); }
.cv { position: absolute; left: 0; top: 0; width: 520px; height: 440px; transform: scale(var(--k, 1)); transform-origin: 0 0; font-size: 12px; color: var(--ink); }
.cv * { box-sizing: border-box; } .cv .im { display: block; width: 100%; height: 100%; background: center / cover no-repeat; }
.cv h6 { font: 600 11.5px var(--d); margin: 0; } .cv p { margin: 0; }
.cur { position: absolute; left: 0; top: 0; width: 20px; height: 20px; z-index: 9; transform: translate(470px, 400px); }
.cv .go { display: inline-grid; place-items: center; height: 28px; padding: 0 12px; border-radius: 8px; background: var(--ac); color: var(--acink); font: 600 11.5px var(--d); }
.cv .pb { display: block; height: 5px; border-radius: 3px; background: var(--s3); overflow: hidden; } .cv .pb i { display: block; height: 100%; width: 100%; border-radius: 3px; background: var(--ac); }
.cv .ty3 { display: flex; gap: 4px; } .cv .ty3 i { width: 6px; height: 6px; border-radius: 50%; background: var(--muted); }
.card2, .nd, .scn, .tc, .td, .pc, .dcard, .ct, .cm { background: var(--s2); box-shadow: 0 0 0 1px var(--line); }
/* nodes */
.w-nodes .dots { position: absolute; inset: 0; background-image: radial-gradient(var(--dot) 1px, transparent 1px); background-size: 18px 18px; }
.wires { position: absolute; inset: 0; } .wires path { fill: none; stroke-width: 2; } .wires .w0 { stroke: #b79cff; stroke-dasharray: 120; }
.wires .w1, .wires .w2, .wires .w3, .wires .w4 { stroke: var(--ac); stroke-dasharray: 220; }
.nd { position: absolute; border-radius: 14px; overflow: hidden; } .nd h6 { padding: 8px 10px; border-bottom: 1px solid var(--line); }
.nd.n1 { left: 16px; top: 56px; width: 130px; } .nd.n1 .im { height: 110px; }
.nd.n2 { left: 186px; top: 126px; width: 150px; } .nd ul { margin: 0; padding: 6px 10px 4px; list-style: none; } .nd li { display: flex; justify-content: space-between; padding: 3px 0; font: 400 10.5px var(--m); color: var(--muted); }
.nd li b { color: var(--ok); } .nd .go { display: grid; margin: 4px 10px 10px; }
.rf { position: absolute; margin: 0; border-radius: 8px; overflow: hidden; box-shadow: 0 10px 24px -12px #000; }
.rf figcaption { position: absolute; left: 5px; bottom: 4px; padding: 1px 5px; border-radius: 5px; background: rgba(4,20,27,.82); color: #fff; font: 400 9px var(--m); }
.rf.r1 { left: 442px; top: 24px; width: 62px; height: 110px; } .rf.r2 { left: 374px; top: 142px; width: 130px; height: 68px; }
.rf.r3 { left: 374px; top: 218px; width: 130px; height: 54px; } .rf.r4 { left: 374px; top: 280px; width: 130px; height: 38px; }
/* gen */
.w-gen .pr { position: absolute; left: 16px; right: 16px; top: 16px; display: flex; align-items: center; gap: 10px; padding: 10px 10px 10px 14px; border-radius: 12px; background: var(--s2); box-shadow: 0 0 0 1px var(--line); font-size: 12.5px; }
.w-gen .ty { flex: 1; white-space: nowrap; overflow: hidden; } .gmods { position: absolute; left: 16px; top: 70px; display: flex; gap: 6px; }
.gmods span, .chips span, .gn span, .tg span, .qp span { padding: 5px 10px; border-radius: 99px; background: var(--s2); box-shadow: 0 0 0 1px var(--line); font: 600 11px var(--d); color: var(--ink2); }
.gmods span.on, .chips span.on, .gn span.on, .tg span.on { background: var(--ac); color: var(--acink); box-shadow: none; }
.g4 { position: absolute; left: 16px; top: 106px; width: 300px; display: grid; grid-template-columns: 1fr 1fr; gap: 8px; } .gi { margin: 0; height: 146px; border-radius: 10px; overflow: hidden; }
.vid { position: absolute; left: 330px; right: 16px; top: 106px; bottom: 16px; border-radius: 12px; overflow: hidden; background: var(--s2); box-shadow: 0 0 0 1px var(--ac); }
.vid .vt { height: 214px; } .vid div { padding: 10px 12px; } .vid b { display: block; font: 600 12px var(--d); } .vid small { display: block; margin: 2px 0 8px; font: 400 10px var(--m); color: var(--muted); }
/* tpl */
.chips { position: absolute; left: 16px; top: 16px; display: flex; gap: 6px; }
.bf { position: absolute; left: 16px; right: 16px; top: 54px; height: 300px; border-radius: 14px; overflow: hidden; }
.bf .bb, .bf .aa { position: absolute; inset: 0; } .bf .bb { background: linear-gradient(160deg, #7d6b58, #4c4138); }
.bf .bb .im { position: absolute; width: 56%; height: 82%; left: 22%; top: 10%; background-size: contain; transform: rotate(-6deg); filter: brightness(.75) contrast(.85) saturate(.65) sepia(.3); }
.bf .aa { background: #fff; clip-path: inset(0 0 0 50%); } .bf .aa .im { position: absolute; width: 56%; height: 82%; left: 22%; top: 8%; background-size: contain; }
.bf em { position: absolute; top: 10px; padding: 3px 9px; border-radius: 7px; font: 600 11px var(--d); font-style: normal; } .bf .bb em { left: 10px; background: rgba(0,0,0,.55); color: #fff; } .bf .aa em { right: 10px; background: #04141b; color: #fff; }
.bf .hd { position: absolute; top: 0; bottom: 0; left: 50%; width: 3px; margin-left: -1.5px; background: #fff; box-shadow: 0 0 12px rgba(0,0,0,.4); }
.bf .hd::after { content: '⟷'; position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); width: 32px; height: 32px; border-radius: 50%; background: #fff; color: #04141b; display: grid; place-items: center; font-size: 14px; }
.k2 { position: absolute; right: 28px; top: 316px; padding: 4px 9px; border-radius: 7px; background: #04141b; color: var(--ac); font: 600 11px var(--m); }
.tri { position: absolute; left: 16px; right: 16px; bottom: 16px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
.tri span { display: flex; align-items: center; gap: 8px; padding: 9px 10px; border-radius: 10px; background: var(--s2); color: var(--muted); font: 600 11.5px var(--d); }
.tri b { display: grid; place-items: center; width: 20px; height: 20px; border-radius: 6px; background: rgba(255,255,255,.08); font-size: 10.5px; }
/* launch */
.ls { position: absolute; left: 16px; top: 16px; width: 150px; margin: 0; padding: 0; list-style: none; display: grid; gap: 6px; }
.ls li { display: flex; justify-content: space-between; padding: 8px 10px; border-radius: 9px; background: var(--s2); box-shadow: 0 0 0 1px var(--line); font: 500 11px var(--d); color: var(--ink2); } .ls b { color: var(--ok); }
.oc { position: absolute; margin: 0; border-radius: 10px; overflow: hidden; box-shadow: 0 14px 30px -14px #000; }
.oc figcaption { position: absolute; left: 6px; bottom: 6px; padding: 1px 6px; border-radius: 5px; background: rgba(4,20,27,.82); color: #fff; font: 400 9.5px var(--m); }
.oc.c1 { left: 182px; top: 16px; width: 150px; height: 150px; } .oc.c2 { left: 344px; top: 16px; width: 96px; height: 170px; } .oc.c3 { left: 182px; top: 176px; width: 150px; height: 100px; }
.ocap { position: absolute; left: 16px; top: 176px; width: 150px; padding: 10px; border-radius: 10px; background: var(--acsoft); box-shadow: inset 0 0 0 1px var(--line); font-size: 10.5px; line-height: 1.4; color: var(--ink2); }
.ocap b { display: block; margin-bottom: 4px; color: var(--ac); font: 600 10.5px var(--d); }
.w-launch .ocap { left: 344px; top: 196px; width: 160px; } .w-launch .ogal { position: absolute; left: 0; right: 0; bottom: 16px; overflow: hidden; }
.w-launch .gt { display: flex; gap: 8px; width: max-content; } .gc { display: block; flex: none; width: 78px; height: 92px; border-radius: 9px; background: center / cover; }
/* motion */
.ms { position: absolute; left: 16px; top: 16px; width: 324px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
.scn { border-radius: 10px; overflow: hidden; } .si { position: relative; height: 82px; background: #04141b; } .si b { position: absolute; left: 7px; right: 7px; bottom: 6px; z-index: 1; color: #fff; font: 700 11px/1.1 var(--d); }
.si::after { content: ''; position: absolute; inset: 40% 0 0; background: linear-gradient(transparent, rgba(0,0,0,.75)); } .scn.x5 .si { background: var(--ac); } .scn.x5 b { color: #04141b; } .scn.x5 .si::after { display: none; }
.scn p { padding: 5px 8px; font: 400 9.5px var(--m); color: var(--muted); }
.tl { position: absolute; left: 16px; top: 262px; width: 324px; height: 36px; display: flex; gap: 3px; padding: 5px; border-radius: 9px; background: var(--s2); box-shadow: 0 0 0 1px var(--line); }
.tl i { flex: 1; border-radius: 5px; background: var(--s3); } .tl i:nth-child(-n+2) { background: var(--acsoft); } .tl .ph { position: absolute; top: -4px; bottom: -4px; left: 41%; width: 2px; border-radius: 2px; background: var(--ac); }
.rn { position: absolute; left: 16px; top: 312px; width: 324px; padding: 12px 14px; border-radius: 12px; background: var(--s2); box-shadow: 0 0 0 1px var(--line); font: 600 12.5px var(--d); }
.rn small { display: block; margin: 2px 0 9px; font: 400 10.5px var(--m); color: var(--muted); }
.ph9 { position: absolute; right: 18px; top: 16px; width: 146px; height: 260px; border-radius: 20px; overflow: hidden; background: #000; box-shadow: 0 0 0 5px #000, 0 0 0 6px var(--line), 0 20px 40px -14px #000; }
.ph9 .im { position: absolute; inset: 0; background-position: 50% 85%; transform: scale(1.5); } .ph9 .p2, .ph9 .p3 { opacity: 0; }
.ph9::after { content: ''; position: absolute; inset: 45% 0 0; background: linear-gradient(transparent, rgba(0,0,0,.85)); }
.ph9 b { position: absolute; z-index: 1; left: 12px; right: 12px; bottom: 40px; color: #fff; font: 800 19px/1.02 var(--d); letter-spacing: -.03em; }
.ph9 small { position: absolute; z-index: 1; left: 12px; bottom: 16px; padding: 3px 8px; border-radius: 6px; background: var(--ac); color: var(--acink); font: 700 10px var(--d); }
.ok { position: absolute; right: 16px; top: 292px; width: 150px; display: grid; gap: 6px; }
.ok span { padding: 7px 10px; border-radius: 9px; background: var(--s2); box-shadow: 0 0 0 1px var(--line); font: 400 10.5px var(--m); color: var(--ink2); }
/* copy */
.w-copy .me, .w-ai .me { position: absolute; right: 16px; top: 16px; max-width: 330px; padding: 10px 13px; border-radius: 14px 14px 4px 14px; background: var(--ac); color: var(--acink); font-size: 12.5px; line-height: 1.45; }
.w-copy .ty3 { position: absolute; left: 20px; top: 98px; } .ans { position: absolute; left: 16px; right: 60px; top: 92px; display: grid; gap: 8px; }
.ans p { padding: 9px 12px; border-radius: 10px; background: var(--s2); box-shadow: 0 0 0 1px var(--line); font-size: 12px; line-height: 1.45; color: var(--ink2); } .ans b { color: var(--ink); }
.dcard { position: absolute; left: 16px; top: 250px; width: 330px; display: flex; align-items: center; gap: 12px; padding: 12px; border-radius: 12px; }
.dcard .dw { display: grid; place-items: center; width: 38px; height: 44px; border-radius: 8px; background: #2b5797; color: #fff; font: 700 16px var(--d); }
.dcard b { display: block; font: 600 12.5px var(--d); } .dcard small { font: 400 10.5px var(--m); color: var(--muted); } .dcard em { margin-left: auto; padding: 6px 10px; border-radius: 8px; background: var(--ac); color: var(--acink); font: 600 11px var(--d); font-style: normal; }
.qp { position: absolute; left: 16px; right: 16px; bottom: 16px; display: flex; flex-wrap: wrap; gap: 6px; }
/* music */
.tg { position: absolute; left: 16px; top: 16px; display: flex; gap: 6px; }
.fl { position: absolute; left: 16px; right: 16px; top: 58px; padding: 10px 13px; border-radius: 12px; background: var(--s2); box-shadow: 0 0 0 1px var(--line); font-size: 12.5px; }
.fl small { display: block; margin-bottom: 3px; font: 400 10px var(--m); color: var(--muted); } .gn { position: absolute; left: 16px; top: 122px; display: flex; gap: 6px; }
.wv { position: absolute; left: 16px; right: 16px; top: 172px; height: 150px; display: flex; align-items: center; gap: 4px; padding: 0 14px; border-radius: 14px; background: linear-gradient(180deg, var(--acsoft), transparent); box-shadow: inset 0 0 0 1px var(--line); }
.wv i { flex: 1; height: var(--h); border-radius: 3px; background: linear-gradient(var(--ac), #7ee0c3); transform-origin: 50% 50%; }
.pl { position: absolute; left: 16px; right: 16px; top: 340px; display: flex; align-items: center; gap: 12px; padding: 12px 14px; border-radius: 12px; background: var(--s2); box-shadow: 0 0 0 1px var(--line); }
.pl .pp { display: grid; place-items: center; width: 34px; height: 34px; border-radius: 50%; background: var(--ac); color: var(--acink); font-size: 12px; } .pl .pb { flex: 1; } .pl small { font: 400 10.5px var(--m); color: var(--muted); }
/* trend */
.tf { position: absolute; left: 16px; top: 16px; bottom: 16px; width: 220px; overflow: hidden; -webkit-mask-image: linear-gradient(transparent, #000 8%, #000 92%, transparent); mask-image: linear-gradient(transparent, #000 8%, #000 92%, transparent); }
.tt { display: grid; gap: 8px; } .tc { position: relative; padding: 10px 12px; border-radius: 12px; } .tc b { display: block; margin-top: 6px; font: 600 12px/1.3 var(--d); }
.tc small { font: 400 10px var(--m); color: var(--muted); } .tc em { position: absolute; right: 12px; top: 10px; font: 600 11px var(--m); font-style: normal; color: var(--ac); }
.pf { display: inline-block; padding: 2px 7px; border-radius: 5px; font: 600 9.5px var(--d); background: rgba(255,255,255,.08); } .pf.tiktok { color: #7ef0e8; } .pf.instagram { color: #ff9ad5; } .pf.threads { color: #e6e6e6; }
.td { position: absolute; left: 248px; right: 16px; top: 16px; bottom: 16px; padding: 16px; border-radius: 14px; } .td > b { display: block; margin-top: 8px; font: 700 16px/1.2 var(--d); }
.td > small { font: 400 10.5px var(--m); color: var(--ac); } .td h6 { margin-top: 14px; color: var(--muted); font: 600 10px var(--d); text-transform: uppercase; letter-spacing: .06em; }
.td p { margin-top: 4px; font-size: 12px; line-height: 1.45; color: var(--ink2); } .td .go { position: absolute; left: 16px; bottom: 16px; } .td .g2 { position: absolute; left: 146px; bottom: 16px; padding: 6px 12px; border-radius: 8px; box-shadow: inset 0 0 0 1px var(--line); font: 600 11.5px var(--d); }
/* pred */
.pc { position: absolute; top: 16px; width: 156px; border-radius: 14px; overflow: hidden; } .pc.p1 { left: 16px; } .pc.p2 { left: 182px; } .pc.p3 { left: 348px; }
.pi { height: 150px; padding: 10px; background: var(--s3); } .pi .im { background-size: contain; }
.ps { padding: 9px 11px 2px; font: 700 26px/1 var(--d); letter-spacing: -.03em; } .ps small { font: 400 12px var(--m); color: var(--muted); }
.pc .br { display: block; margin: 6px 11px 11px; height: 5px; border-radius: 3px; background: var(--s3); } .pc .br i { display: block; height: 100%; width: var(--w); border-radius: 3px; background: #55606a; } .pc.p2 .br i { background: var(--ac); }
.pc.p2 { box-shadow: 0 0 0 2px var(--ac), 0 20px 50px -20px rgba(155,232,255,.45); } .wb { position: absolute; z-index: 1; left: 8px; top: 8px; padding: 3px 8px; border-radius: 7px; background: var(--ac); color: var(--acink); font: 600 10px var(--d); }
.scan { position: absolute; top: 16px; height: 212px; left: 100%; width: 3px; background: var(--ac); box-shadow: 0 0 18px 4px rgba(155,232,255,.5); opacity: 0; }
.cr { position: absolute; left: 16px; right: 16px; top: 262px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; }
.cr span { display: flex; justify-content: space-between; padding: 7px 10px; border-radius: 9px; background: var(--s2); box-shadow: 0 0 0 1px var(--line); font: 500 11px var(--d); color: var(--ink2); } .cr b { font: 600 10.5px var(--m); color: var(--ok); } .cr b.w { color: #f0b46a; }
.vd { position: absolute; left: 16px; right: 16px; top: 352px; padding: 11px 13px; border-radius: 12px; background: var(--acsoft); box-shadow: inset 0 0 0 1px var(--line); font-size: 12px; line-height: 1.45; } .vd b { color: var(--ac); }
/* strat */
.sq { position: absolute; left: 16px; top: 16px; width: 210px; display: flex; flex-wrap: wrap; gap: 6px; padding: 14px; border-radius: 14px; background: var(--s2); box-shadow: 0 0 0 1px var(--line); }
.sq small { width: 100%; font: 400 10px var(--m); color: var(--muted); } .sq small + small, .sq span + small { margin-top: 6px; }
.sq span { padding: 5px 10px; border-radius: 99px; box-shadow: inset 0 0 0 1px var(--line); font: 600 11px var(--d); color: var(--ink2); } .sq span.on { background: var(--ac); color: var(--acink); box-shadow: none; }
.sl { position: relative; width: 100%; height: 22px; } .sl::before { content: ''; position: absolute; left: 0; right: 0; top: 9px; height: 4px; border-radius: 2px; background: var(--s3); }
.sl i { position: absolute; left: 0; top: 9px; height: 4px; width: 50%; border-radius: 2px; background: var(--ac); } .sl b { position: absolute; right: 0; top: -14px; font: 600 11px var(--m); color: var(--ac); }
.ring2 { position: absolute; left: 248px; top: 16px; width: 120px; height: 120px; border-radius: 50%; --p: 82; background: conic-gradient(var(--ac) calc(var(--p) * 1%), var(--s3) 0); display: grid; place-items: center; }
.ring2::before { content: ''; position: absolute; inset: 10px; border-radius: 50%; background: var(--s0); } .ring2 span { position: relative; font: 700 28px var(--d); } .ring2 small { font: 400 11px var(--m); color: var(--muted); }
.fnl { position: absolute; left: 248px; right: 16px; top: 150px; display: grid; gap: 8px; } .fnl small { display: block; margin-bottom: 3px; font: 400 10px var(--m); color: var(--muted); }
.fnl i { display: block; height: 14px; width: var(--w); border-radius: 4px; background: linear-gradient(90deg, var(--ac), #7ee0c3); }
.sg { position: absolute; left: 16px; right: 16px; top: 262px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
.sg span { padding: 10px 12px; border-radius: 12px; background: var(--s2); box-shadow: 0 0 0 1px var(--line); font: 400 10.5px var(--m); color: var(--muted); } .sg b { display: block; margin-bottom: 3px; font: 600 13px var(--d); color: var(--ink); }
.w-strat .go { position: absolute; left: 16px; bottom: 18px; }
/* ai */
.ab { position: absolute; left: 16px; right: 16px; top: 74px; display: grid; gap: 4px; } .ab h6 { margin-top: 6px; color: var(--muted); font: 600 10px var(--d); text-transform: uppercase; letter-spacing: .06em; }
.ab p { font-size: 12px; color: var(--ink2); } .ab .pp { padding: 9px 12px; border-radius: 10px; background: var(--s2); box-shadow: 0 0 0 1px var(--line); color: var(--ink); }
.nn { display: flex; align-items: center; gap: 8px; margin-top: 2px; } .nn span { padding: 7px 11px; border-radius: 8px; background: var(--s2); box-shadow: 0 0 0 1px var(--line); font: 600 11.5px var(--d); } .nn i { color: var(--ac); font-style: normal; }
.rnb { position: absolute; left: 16px; right: 16px; bottom: 16px; display: flex; align-items: center; justify-content: space-between; padding: 10px 10px 10px 14px; border-radius: 12px; background: var(--s2); box-shadow: 0 0 0 1px var(--line); font-size: 11.5px; color: var(--muted); }
.rnb b { padding: 7px 12px; border-radius: 8px; background: var(--ac); color: var(--acink); font: 600 11.5px var(--d); }
/* team */
.ct { position: absolute; left: 16px; top: 16px; bottom: 16px; width: 150px; padding: 12px; border-radius: 14px; display: grid; align-content: start; gap: 4px; }
.ct small { font: 400 10px var(--m); color: var(--muted); margin-bottom: 4px; } .u { position: relative; display: flex; align-items: center; gap: 8px; padding: 6px; border-radius: 9px; font: 500 12px var(--d); }
.u i { display: grid; place-items: center; width: 26px; height: 26px; border-radius: 50%; background: var(--s3); font: 600 11px var(--d); font-style: normal; } .u em { position: absolute; left: 26px; top: 24px; width: 9px; height: 9px; border-radius: 50%; background: #55606a; box-shadow: 0 0 0 2px var(--s2); }
.u.on em { background: var(--ok); } .u.new { background: var(--acsoft); }
.cm { position: absolute; left: 178px; right: 16px; top: 16px; bottom: 16px; padding: 12px; border-radius: 14px; display: grid; align-content: start; gap: 8px; }
.cm .mh { font: 600 12.5px var(--d); padding-bottom: 8px; border-bottom: 1px solid var(--line); } .cm .mh small { display: block; font: 400 10px var(--m); color: var(--muted); }
.cm p { max-width: 240px; padding: 8px 11px; border-radius: 12px 12px 12px 4px; background: var(--s3); font-size: 12px; line-height: 1.4; } .cm p b { display: block; font: 600 10.5px var(--d); color: var(--ac); }
.cm p.mine { justify-self: end; border-radius: 12px 12px 4px 12px; background: var(--ac); color: var(--acink); } .cm .mt { width: 60px; height: 96px; margin-top: 6px; border-radius: 7px; }
.cm .ty3 { padding: 8px 11px; } .toast { position: absolute; left: 50%; bottom: 22px; transform: translateX(-50%); padding: 9px 14px; border-radius: 10px; background: #04141b; color: var(--ink); box-shadow: 0 0 0 1px var(--line), 0 14px 30px -10px #000; font: 500 11.5px var(--d); white-space: nowrap; }
.toast::before { content: '✓ '; color: var(--ok); } .w-team .toast { left: auto; right: 24px; transform: none; }
@media (prefers-reduced-motion: no-preference) {
  .tp .cv * { animation-timing-function: cubic-bezier(.2,.7,.2,1); animation-iteration-count: infinite; animation-fill-mode: both; }
  .w-nodes .w0 { animation: nd-w 10s infinite; } .w-nodes .w1, .w-nodes .w2, .w-nodes .w3, .w-nodes .w4 { animation: nd-wo 10s infinite; }
  .w-nodes .t1 { animation: nd-t1 10s infinite; } .w-nodes .t2 { animation: nd-t2 10s infinite; } .w-nodes .t3 { animation: nd-t3 10s infinite; } .w-nodes .t4 { animation: nd-t4 10s infinite; }
  .w-nodes .r1 { animation: nd-r1 10s infinite; } .w-nodes .r2 { animation: nd-r2 10s infinite; } .w-nodes .r3 { animation: nd-r3 10s infinite; } .w-nodes .r4 { animation: nd-r4 10s infinite; }
  .w-nodes .cur { animation: cur-n 10s infinite; } .w-nodes .go { animation: go-p 10s infinite; }
  .w-gen .ty { animation: ty 10s steps(48) infinite; } .w-gen .g0 { animation: gi0 10s infinite; } .w-gen .g1 { animation: gi1 10s infinite; } .w-gen .g2 { animation: gi2 10s infinite; } .w-gen .g3 { animation: gi3 10s infinite; }
  .w-gen .vid { animation: gv 10s infinite; } .w-gen .pb i { animation: pb 10s infinite; }
  .w-tpl .hd { animation: hd 9s infinite; } .w-tpl .aa { animation: aa 9s infinite; } .w-tpl .k2 { animation: k2 9s infinite; }
  .w-tpl .tri span { animation: tri 9s infinite; } .w-tpl .tri .a2 { animation-delay: 3s; } .w-tpl .tri .a3 { animation-delay: 6s; }
  .w-launch .l1 { animation: l1 10s infinite; } .w-launch .l2 { animation: l2 10s infinite; } .w-launch .l3 { animation: l3 10s infinite; } .w-launch .l4 { animation: l4 10s infinite; }
  .w-launch .c1 { animation: oc1 10s infinite; } .w-launch .c2 { animation: oc2 10s infinite; } .w-launch .c3 { animation: oc3 10s infinite; } .w-launch .ocap { animation: cap 10s infinite; }
  .w-launch .gt { animation: mq 40s linear infinite; }
  .w-motion .scn { animation: sc-on 12s infinite; } .w-motion .x1 { animation-delay: 2s; } .w-motion .x2 { animation-delay: 4s; } .w-motion .x3 { animation-delay: 6s; } .w-motion .x4 { animation-delay: 8s; } .w-motion .x5 { animation-delay: 10s; }
  .w-motion .ph { animation: ph 12s linear infinite; } .w-motion .pb i { animation: rpb 12s infinite; } .w-motion .o1 { animation: o1 12s infinite; } .w-motion .o2 { animation: o2 12s infinite; } .w-motion .o3 { animation: o3 12s infinite; }
  .w-motion .p1 { animation: p1 6s infinite; } .w-motion .p2 { animation: p2 6s infinite; } .w-motion .p3 { animation: p3 6s infinite; }
  .w-copy .me { animation: me 10s infinite; } .w-copy .ty3 { animation: ty3 10s infinite; } .cv .ty3 i { animation: dot 1s ease-in-out infinite; } .cv .ty3 i:nth-child(2) { animation-delay: .15s; } .cv .ty3 i:nth-child(3) { animation-delay: .3s; }
  .w-copy .a1 { animation: a1 10s infinite; } .w-copy .a2 { animation: a2 10s infinite; } .w-copy .a3 { animation: a3 10s infinite; } .w-copy .dcard { animation: dcard 10s infinite; }
  .w-music .wv i { animation: wv 1.1s ease-in-out infinite; animation-delay: var(--d); } .w-music .pb i { animation: mpb 12s linear infinite; }
  .w-trend .tt { animation: tv 24s linear infinite; } .w-trend .td { animation: td 10s infinite; } .w-trend .go { animation: tg 10s infinite; }
  .w-pred .p1 { animation: pc1 10s infinite; } .w-pred .p2 { animation: pc2 10s infinite, win 10s infinite; } .w-pred .p3 { animation: pc3 10s infinite; } .w-pred .scan { animation: scan 10s infinite; }
  .w-pred .ps { animation: ps 10s infinite; } .w-pred .br i { animation: br 10s infinite; } .w-pred .wb { animation: wb 10s infinite; } .w-pred .vd { animation: vd 10s infinite; }
  .w-pred .k0 { animation: k0 10s infinite; } .w-pred .k1 { animation: k1 10s infinite; } .w-pred .k2 { animation: kk2 10s infinite; } .w-pred .k3 { animation: k3 10s infinite; } .w-pred .k4 { animation: k4 10s infinite; } .w-pred .k5 { animation: k5 10s infinite; }
  .w-strat .ring2 { animation: ring 10s infinite; } .w-strat .fnl i { animation: fn 10s infinite; } .w-strat .e1 { animation: e1 10s infinite; } .w-strat .e2 { animation: e2 10s infinite; } .w-strat .e3 { animation: e3 10s infinite; }
  .w-strat .sl i { animation: sl 10s infinite; } .w-strat .go { animation: tg 10s infinite; }
  .w-ai .h1 { animation: h1 10s infinite; } .w-ai .q1 { animation: q1 10s infinite; } .w-ai .h2 { animation: h2 10s infinite; } .w-ai .q2 { animation: q2 10s infinite; } .w-ai .h3 { animation: h3 10s infinite; }
  .w-ai .z1 { animation: z1 10s infinite; } .w-ai .z2 { animation: z2 10s infinite; } .w-ai .z3 { animation: z3 10s infinite; } .w-ai .z4 { animation: z4 10s infinite; } .w-ai .z5 { animation: z5 10s infinite; }
  .w-ai .rnb { animation: rnb 10s infinite; } .w-ai .cur { animation: cur-a 10s infinite; } .w-ai .rnb b { animation: run 10s infinite; }
  .w-team .m1 { animation: m1 10s infinite; } .w-team .m2 { animation: m2 10s infinite; } .w-team .m3 { animation: m3 10s infinite; } .w-team .cm .ty3 { animation: ty3b 10s infinite; }
  .w-team .toast { animation: toast 10s infinite; } .w-team .new { animation: nw 10s infinite; }
  ANIM
}
@media (prefers-reduced-motion: reduce) { .ed button::after { box-shadow: none; } }
@media (max-width: 1060px) { .stage { grid-template-columns: minmax(0, 1fr); min-height: 0; } .win { max-width: 560px; } }
@media (max-width: 760px) {
  .ed { display: flex; gap: 8px; overflow-x: auto; scroll-snap-type: x mandatory; margin: 0 -16px; padding: 4px 16px 10px; font-size: 15px; letter-spacing: -.01em; scrollbar-width: none; }
  .ed::-webkit-scrollbar { display: none; } .ed .sl { display: none; }
  .ed button { flex: none; scroll-snap-align: start; padding: 10px 14px; border-radius: 12px; background: rgba(255,255,255,.04); box-shadow: inset 0 0 0 1px var(--line); color: var(--ink2); }
  .ed button[aria-selected="true"] { background: var(--ac); color: var(--acink); box-shadow: 0 10px 24px -10px rgba(155,232,255,.5); } .ed button[aria-selected="true"]::after { display: none; }
  .mpanel { margin-top: 18px; padding: 22px 18px; border-radius: 22px; } .lt .lead { font-size: 15.5px; }
  .bens { gap: 18px; } .bens b { font-size: 27px; } .bens small { font-size: 12.5px; } .lt .acts { flex-direction: column; align-items: stretch; } .win { margin-top: 8px; border-radius: 16px; }
}
"""

ICE = """
:root { --bg: #090e12; --ink: #eef7fb; --ink2: #a9bcc6; --muted: #6f818b; --line: rgba(155,232,255,.1); --card: #111a20; --green: #7ee0c3; --mint: rgba(126,224,195,.12);
  --ac: #9be8ff; --acink: #04141b; --acsoft: rgba(155,232,255,.1); --s0: #0c1318; --s1: #111a20; --s2: #17222a; --s3: #213039; --dot: #16222a; --ok: #7ee0c3; --dim: #2e3e48; --num: #d6f6ff;
  --sh: inset 0 0 0 1px rgba(155,232,255,.07), 0 18px 44px -22px rgba(0,0,0,.85); --sh2: inset 0 0 0 1px rgba(155,232,255,.08), 0 40px 80px -36px rgba(0,0,0,.95); }
html { color-scheme: dark; } body { background: var(--bg); }
.bgfx i { opacity: .5; } .bgfx .a { background: #123a4e; } .bgfx .b { background: #1d2a3e; } .bgfx .c { background: #0e3a3a; } .bgfx .d { background: #16314a; opacity: .35; }
.btn.p { background: var(--ac); color: var(--acink); box-shadow: 0 12px 30px -12px rgba(155,232,255,.5); } .btn.g { background: rgba(255,255,255,.05); }
.nav .in { background: none; box-shadow: none; backdrop-filter: none; -webkit-backdrop-filter: none; }
.fnote { margin-top: 26px; text-align: center; font-size: 12.5px; color: var(--muted); } .mnav { background: rgba(12,19,24,.97); }
.hero h1 .gr { background: linear-gradient(95deg, #ffffff 20%, #9be8ff 58%, #7ee0c3); -webkit-background-clip: text; background-clip: text; }
.pill { background: rgba(255,255,255,.06); color: var(--ink2); } .pill b { background: var(--ac); color: var(--acink); }
.panel { background: rgba(17,26,32,.6); } .src, .fm { background: var(--s2); } .chip { background: rgba(23,34,42,.95); }
.chip.c1 i { background: rgba(126,224,195,.14); color: var(--ok); } .chip.c2 i { background: var(--acsoft); color: var(--ac); } .chip.c3 i { background: rgba(240,180,106,.14); color: #f0b46a; }
.models span { color: #c8dbe4; } .hvid { background: var(--s1); box-shadow: inset 0 0 0 1px var(--line), var(--sh2); }
.three .card { background: var(--card); } .ring { background: conic-gradient(var(--ac) calc(var(--v, 0) * 1%), rgba(155,232,255,.12) 0); }
.cmp .by { background: linear-gradient(90deg, var(--ac), var(--ok)); } .big { color: var(--num); }
.per div { background: var(--card); } .per button.on { background: var(--ac); color: var(--acink); } .per em { background: rgba(126,224,195,.15); color: var(--ok); }
.plan { background: var(--card); } .plan.hot { background: linear-gradient(160deg, #e9fbff, #c6f0fb); color: #04141b; box-shadow: 0 40px 80px -30px rgba(155,232,255,.4); }
.plan.hot .btn { background: #04141b; color: #fff; } .plan.hot .pop { background: #04141b; color: var(--ac); } .plan .pop { background: var(--acsoft); color: var(--ac); }
.plan .pr .dp { background: var(--acsoft); color: var(--ac); } .gens .top { background: var(--ac); color: var(--acink); }
.faq details, .end { background: var(--card); } .end { box-shadow: inset 0 0 0 1px var(--line), 0 0 120px -40px rgba(155,232,255,.25); }
.totop { background: var(--ac); color: var(--acink); } .skip { background: var(--ac); color: var(--acink); }
dialog.doc { background: var(--card); } .sf input, .sf textarea { background: var(--bg); } .sf input:focus, .sf textarea:focus { border-color: var(--ac); }
:focus-visible { outline-color: var(--ac); }
"""

FNOTE = '* До 50% — в сравнении с оплатой тех же моделей в отдельных сервисах; итог зависит от моделей и объёма.'

JS_TABS = """<script>
// modes: one tab open at a time; arrows/Home/End move between tabs; #nodes … #team (or a nav link to one) opens it
(() => {
  const tabs = [...document.querySelectorAll('.ed [role=tab]')]; if (!tabs.length) return;
  const show = (t, focus) => { tabs.forEach((x) => { const on = x === t; x.setAttribute('aria-selected', on); x.tabIndex = on ? 0 : -1;
      document.getElementById(x.getAttribute('aria-controls')).hidden = !on; });
    if (focus) t.focus(); if (matchMedia('(max-width: 760px)').matches) t.scrollIntoView({ block: 'nearest', inline: 'center', behavior: 'smooth' }); fit(); };
  tabs.forEach((t, i) => { t.addEventListener('click', () => { show(t); history.replaceState(null, '', '#' + t.id); });
    t.addEventListener('keydown', (e) => { const k = { ArrowRight: i + 1, ArrowLeft: i - 1, Home: 0, End: tabs.length - 1 }[e.key];
      if (k === undefined) return; e.preventDefault(); show(tabs[(k + tabs.length) % tabs.length], true); }); });
  const fromHash = () => { const t = tabs.find((x) => '#' + x.id === location.hash); if (!t) return; show(t);
    document.getElementById('modes').scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' }); };
  // windows are drawn on a 520×440 canvas and scaled to the column
  const fit = () => document.querySelectorAll('.tp:not([hidden]) .vw').forEach((w) => w.style.setProperty('--k', Math.min(1, w.clientWidth / 520)));
  addEventListener('resize', fit); addEventListener('hashchange', fromHash); fromHash(); fit();
})();
</script>
"""


def tab_panel(i, key, label, h, lead, bens):
    title, status, inner = WIN[key]
    ben = ''.join(f'<li><b>{a}</b><span>{b}</span><small>{c}</small></li>' for a, b, c in bens)
    return (f'<div class="tp" id="p-{key}" role="tabpanel" aria-labelledby="{key}" tabindex="0"{"" if i == 0 else " hidden"}><div class="stage">'
            f'<div class="lt"><span class="eb"><i>{icon(key)}</i>{label}</span><h3>{h}</h3><p class="lead">{lead}</p><ul class="bens">{ben}</ul>'
            f'<div class="acts"><a class="btn p" data-app="demo" href="{APP}?demo=1">Попробовать в демо →</a>{reg("Начать бесплатно", "btn g")}</div></div>'
            f'<div class="win w-{key}" role="img" aria-label="Анимация: как работает {label}"><div class="bar"><i></i><i></i><i></i><span>{title}</span><em>{status}</em></div>'
            f'<div class="vw"><div class="cv">{inner}</div></div></div></div></div>')


def build(docs=''):
    html = v.build(docs=docs, theme='dark')
    head, rest = html.split('<main id="main">', 1)
    main_old, tail = rest.split('</main>', 1)
    # keep v4's hero, why, pricing, faq and closing card; everything in between becomes the modes tabs
    sections = re.split(r'(?=<section class="sec"|<div class="wrap"><section class="end)', main_old)
    hero = sections[0].replace('href="#how"', 'href="#modes"')
    # no promo video and no adaptation panel under the headline — the models line follows the buttons, then the footnote
    hero = re.sub(r'<div class="hvid">.*?(?=<div class="models")', '', hero, count=1, flags=re.S)
    hero = hero.replace('</div></div></section>', f'</div><p class="fnote">{FNOTE}</p></div></section>', 1)
    pick = lambda pat: next(s for s in sections if pat in s)  # noqa: E731
    pricing, faq, end = pick('id="pricing"'), pick('id="faq"'), pick('class="end')
    buttons = '<i class="sl" aria-hidden="true">/</i>'.join(
        f'<button type="button" role="tab" id="{k}" aria-controls="p-{k}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{lb}</button>'
        for i, (k, lb, *_x) in enumerate(TABS))
    modes = ('<section class="sec" id="modes"><div class="wrap"><div class="sh rv"><span class="k">Возможности</span><h2>Всё для контента — в одном окне</h2></div>'
             f'<div class="ed" role="tablist" aria-label="Режимы ONEFLOW">{buttons}</div>'
             '<div class="mpanel">' + ''.join(tab_panel(i, *t) for i, t in enumerate(TABS)) + '</div></div></section>')
    main = f'<main id="main">{hero}{modes}{pricing}{faq}{end}</main>'
    # nav: new anchors; theme colour; styles; no v4 feature-card demos
    links = ''.join(f'<a href="{h}">{t}</a>' for h, t in NAV)
    head = re.sub(r'(<nav aria-label="Разделы">).*?(</nav>)', lambda m: m.group(1) + links + m.group(2), head, count=1, flags=re.S)
    head = re.sub(r'(<nav class="mnav" id="mnav" aria-label="Меню" hidden>).*?(<div class="row">)', lambda m: m.group(1) + links + m.group(2), head, count=1, flags=re.S)
    head = head.replace('<meta name="theme-color" content="#0b0b10">', '<meta name="theme-color" content="#090e12">')
    head = head.replace(protos.CSS, '').replace(protos.DARK, '')
    head = head.replace('</style>', ICE + TABS_CSS.replace('ANIM', '\n  '.join(ANIM)) + '</style>', 1)
    tail = tail.replace(protos.js(), '').replace('</body>', JS_TABS + '</body>')
    return head + main + tail


if __name__ == '__main__':
    open(os.path.join(HERE, 'v5-ice.html'), 'w', encoding='utf-8').write(build())
    print('v5-ice.html')
