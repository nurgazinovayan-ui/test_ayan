"""English oneflow.art — the Russian v5 page translated node by node.

translate() swaps whole text nodes, a few attributes and the inline-script messages through EN below (exact matches
only, so a short word never leaks into a longer sentence), then checks that no Cyrillic is left outside the names
that are meant to stay. Add a line here whenever the Russian page gets a new text — the check will say which.
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

EN = {
    # head, menu, hero
    'ONEFLOW — больше контента, до 50% дешевле': 'ONEFLOW — more content, up to 50% cheaper',
    '30+ нейросетей в одном окне: фото, видео и тексты для рекламы. Адаптация под любой размер и пресеты Kaspi, РСЯ, Google, BYYD. Генерация до 50% дешевле, бюджет не сгорает в конце месяца.':
        '30+ AI models in one window: photos, videos and copy for ads. Adapt to any size, with presets for Kaspi, Yandex Ads, Google and BYYD. Generation up to 50% cheaper, and unused budget rolls over.',
    'К содержанию': 'Skip to content', 'ONEFLOW — наверх': 'ONEFLOW — back to top', 'Разделы': 'Sections', 'Меню': 'Menu', 'Открыть меню': 'Open menu',
    'Возможности': 'Features', 'Для бизнеса': 'For business', 'Ассистент': 'Assistant', 'Цены': 'Pricing', 'Вопросы': 'FAQ',
    'Войти': 'Log in', 'Регистрация': 'Sign up', 'Язык / Language': 'Language',
    'Больше контента для вашего бизнеса. До 50% дешевле*': 'More content for your business. Up to 50% cheaper*',
    'Больше контента для': 'More content for', 'магазина на Kaspi.': 'your Kaspi store.', 'вашей кофейни.': 'your coffee shop.', 'бренда одежды.': 'your fashion brand.',
    'салона красоты.': 'your beauty salon.', 'вашего стартапа.': 'your startup.', 'вашего бизнеса.': 'your business.', 'До 50% дешевле*': 'Up to 50% cheaper*',
    'Фото, видео и тексты на 30+ нейросетях — и адаптация под любой размер в один клик. Неиспользованный бюджет остаётся с вами.':
        'Photos, videos and copy from 30+ AI models — plus one-click adaptation to any size. Unused budget stays yours.',
    'Начать бесплатно →': 'Start free →', 'Как это работает': 'How it works', 'Real-ESRGAN (апскейлер)': 'Real-ESRGAN (upscaler)',
    'Background Remover (удаление фона)': 'Background Remover (background removal)',
    '* До 50% — в сравнении с оплатой тех же моделей в отдельных сервисах; итог зависит от моделей и объёма.':
        '* Up to 50% compared with paying for the same models in separate services; the final saving depends on the models and volume.',
    # modes: tabs and left columns
    'Всё для контента — в одном окне': 'Everything for content — in one window', 'Режимы ONEFLOW': 'ONEFLOW modes',
    'Ноды и адаптация': 'Nodes & adaptation', 'Генерация': 'Generation', 'Шаблоны для бизнеса': 'Business templates', 'Музыка и голос': 'Music & voice',
    'Стратегия': 'Strategy', 'ИИ-ассистент': 'AI assistant', 'Соавторы': 'Collaborators',
    'Попробовать в демо →': 'Try the demo →', 'Начать бесплатно': 'Start free',
    'Одно фото — все рекламные форматы': 'One photo — every ad format',
    'Соберите цепочку на холсте: фото → адаптация → готовые размеры под каждую площадку. Одним запуском.':
        'Build a chain on the canvas: photo → adaptation → ready sizes for every platform. In one run.',
    'любых размеров': 'any size', 'Свой размер или пресеты Kaspi, GDN, РСЯ, BYYD, Discovery': 'Custom sizes or presets for Kaspi, GDN, Yandex Ads, BYYD, Discovery',
    'с двумя слоями': 'with two layers', 'Чистый фон отдельно, текст и лого — отдельно': 'A clean background, with text and logo on their own layer',
    'нейросетей': 'AI models', 'Фото, видео и вектор на одном холсте': 'Photos, video and vector on one canvas', 'клик': 'click',
    '«Сохранить все» — сразу во всех форматах': '“Save all” — every format at once',
    'Фото и видео по промпту': 'Photos and videos from a prompt',
    'Опишите идею или прикрепите референс — получите фото до 4K или видео со звуком. Модели переключаются в один клик.':
        'Describe an idea or attach a reference — get photos up to 4K or videos with sound. Switch models in one click.',
    'моделей фото': 'image models', 'Nano Banana Pro, GPT Image, Seedream, Recraft и другие': 'Nano Banana Pro, GPT Image, Seedream, Recraft and more',
    'моделей видео': 'video models', 'разрешение': 'resolution', 'Зависит от выбранной модели': 'Depends on the model you pick', 'кадра': 'frames',
    'Начальный и конечный кадр для видео': 'Start and end frame for video',
    'Студийное фото — со снимка на телефон': 'A studio shot — from a phone photo',
    'Выберите шаблон под нишу, загрузите фото — получите кадр как от фотографа. Без студии, выезда и новой съёмки на каждую позицию.':
        'Pick a template for your niche, upload a photo and get a shot that looks professional. No studio, no location trip, no new shoot for every item.',
    'мин': 'min', 'вместо дней': 'instead of days', 'Новое блюдо, машина или квартира — фото в тот же день': 'A new dish, car or apartment — photographed the same day',
    'шаблонов': 'templates', 'HoReCa, Квартира, Авто, Техника, Мебель': 'HoReCa, Apartment, Auto, Electronics, Furniture', 'высокое разрешение': 'high resolution',
    'Для меню, каталога, объявлений и карточек': 'For menus, catalogs, listings and product cards', 'размеров': 'sizes',
    'Сразу подогнать под любую площадку': 'Fit any platform right away',
    'Фото товара → рекламная кампания': 'Product photo → ad campaign',
    'Фото, название и преимущества — на выходе карточки под форматы и готовые тексты постов для Instagram.':
        'A photo, a name and the key benefits — out come product cards in every format and ready-to-post Instagram captions.',
    'шаблонов карточек': 'card templates', 'Техника, бытовые приборы, детские товары': 'Electronics, home appliances, kids’ goods', 'формата': 'formats',
    '1:1, 9:16 и 3:2 — одним запуском': '1:1, 9:16 and 3:2 in one run', 'ИИ': 'AI', 'палитра и тексты': 'palette and copy',
    'Подберёт цвета и напишет посты': 'Picks the colors and writes the posts', 'фото товара': 'product photo', 'Больше ничего не нужно': 'That’s all you need',
    'Рекламный ролик из ваших фото': 'An ad video from your photos',
    'Сначала статичная раскадровка — видно каждую сцену и текст. Понравилось — жмёте «В рендер» и получаете MP4.':
        'First a static storyboard — every scene and line of text is visible. Like it? Hit “Render” and get an MP4.',
    'за рендер': 'to render', 'Видео собирается прямо в браузере': 'The video is built right in your browser', 'любой формат': 'any format',
    'Одна раскадровка → Reels, YouTube, лента, баннер': 'One storyboard → Reels, YouTube, feed, banner', '3–60 с': '3–60 s', 'длительность': 'duration',
    'Ползунком — сцены подстроятся сами': 'Set with a slider — scenes adjust on their own', 'Реф': 'Ref', 'повтор стиля': 'style match',
    'Покажите ролик — повторим ритм и цвета': 'Show a video — we match its rhythm and colors',
    'Тексты и документы — до готового файла': 'Copy and documents — down to the file',
    'Объявления, SEO-описания, контент-планы и проверка текста. Ответ скачивается как Word, Excel или PowerPoint.':
        'Ads, SEO descriptions, content plans and proofreading. Download any answer as Word, Excel or PowerPoint.',
    'формата файлов': 'file formats', 'быстрых подсказок': 'quick prompts', 'Заголовки, SEO, контент-план, проверка': 'Headlines, SEO, content plan, proofreading',
    'файла на вход': 'files in', 'Фото, DOCX, XLSX, PPTX, CSV — до 4 МБ': 'Images, DOCX, XLSX, PPTX, CSV — up to 4 MB', 'Проекты': 'Projects',
    'и история': 'and history', 'Чаты по папкам, поиск, закрепление': 'Chats in folders, search, pinning',
    'Трек по описанию и озвучка голосом': 'A track from a description, a voice-over in any tone',
    'Музыка под ролик — по жанру и настроению, со своими словами. Озвучка фразы — бодро, спокойно или по-деловому.':
        'Music for your video by genre and mood, with your own lyrics. Voice a phrase — upbeat, calm or businesslike.',
    'режима': 'modes', 'Музыка и речь': 'Music and speech', 'языков озвучки': 'voice languages',
    'Русский, английский, казахский, испанский, немецкий': 'English, Russian, Kazakh, Spanish, German', 'и WAV': 'and WAV',
    'Скачать в один клик': 'Download in one click', 'Свои': 'Your', 'слова песни': 'own lyrics', 'Трек на ваш текст': 'A track to your words',
    'Тренды — сразу в идею для бренда': 'Trends — straight into an idea for your brand',
    'Посты TikTok, Instagram и Threads с разбором: почему в подборке и как применить. Одним кликом — в сценарий или ноды.':
        'TikTok, Instagram and Threads posts with a breakdown: why they made the list and how to use them. One click — into a script or the canvas.',
    'площадки': 'platforms', 'дней': 'days', 'Сегодня, 7 и 30 дней': 'Today, 7 and 30 days', 'региона': 'regions',
    'СНГ, Европа, Америка + поиск': 'CIS, Europe, Americas + search', '«Создать сценарий» или «В ноды»': '“Create script” or “To nodes”',
    'Какой креатив сильнее — до запуска': 'Which creative wins — before launch',
    'Загрузите 1–3 варианта и площадку. ONEFLOW оценит каждый и объяснит, что улучшить, — ещё до первого показа.':
        'Upload 1–3 variants and pick a platform. ONEFLOW scores each one and explains what to improve — before the first impression.',
    'оценка': 'score', 'С сильными сторонами и выводом': 'With strengths and a verdict', 'критериев': 'criteria',
    'Контраст, взгляд, текст, CTA, крючок, шум': 'Contrast, focus, text, CTA, hook, noise', 'варианта': 'variants',
    'Сравнение надёжнее одиночной оценки': 'Comparing beats a single score', 'бюджета на слабый': 'budget on weak ads', 'Отсеете до показов': 'Filter them out before they run',
    'Маркетинговая стратегия под нишу': 'A marketing strategy for your niche',
    'Цель, продукт и бюджет — на выходе план: кому продавать, что говорить, где продвигаться и что создавать.':
        'Goal, product and budget in — a plan out: who to sell to, what to say, where to promote and what to create.',
    'шага': 'steps', 'Цель и описание продукта': 'Goal and product description', 'сценария': 'scenarios',
    'Основной, рост, экономный — с CAC и риском': 'Base, growth, lean — with CAC and risk', 'эксперименты': 'experiments',
    'Реестр тестов и расчёт победителя': 'Test log and winner calculation', 'клик до контента': 'click to content',
    '«Создать workflow» — сразу в ноды': '“Create workflow” — straight to the canvas',
    'Ассистент соберёт цепочку — запускаете вы': 'The assistant builds the chain — you hit run',
    'Разберёт нишу, подскажет идеи, напишет промпт и сам построит схему нод на холсте. Финальное решение — за вами.':
        'It researches your niche, suggests ideas, writes the prompt and builds the node graph on the canvas. The final call is yours.',
    'разбор ниши': 'niche research', 'Аудитория, конкуренты, какой контент нужен': 'Audience, competitors, what content you need', 'промпты': 'prompts',
    'Пишет и улучшает под модель': 'Writes and refines them for the model', 'схема нод': 'node graph', 'Строит на холсте по описанию задачи': 'Built on the canvas from your task',
    'запуск': 'launch', 'Вы проверяете и жмёте «Запустить»': 'You check it and press “Run”',
    'Работайте командой в одном окне': 'Work as a team in one window',
    'Пригласите коллегу по почте и обсуждайте работу во встроенном мессенджере — в личных чатах и группах.':
        'Invite a colleague by email and discuss the work in the built-in messenger — in direct chats and groups.',
    'приглашение': 'invite', 'По почте — принял и уже в контактах': 'By email — once accepted, they’re in your contacts', 'Группы': 'Groups', 'под проекты': 'per project',
    'Запуск, кампания или вся команда': 'A launch, a campaign or the whole team', 'Онлайн': 'Online', 'статус': 'status', 'Видно, кто сейчас в сети': 'See who is online right now',
    'лишних чатов': 'extra chat apps', 'Обсуждение рядом с работой': 'Discussion right next to the work',
    # windows
    'Холст · Весна-кампания': 'Canvas · Spring campaign', '4 из 4 готово': '4 of 4 ready', 'Изображение': 'Image', 'Адаптация': 'Adaptation',
    'РСЯ 1080×450': 'Yandex 1080×450', '✦ Сгенерировать': '✦ Generate', 'Генерация · Фото': 'Generation · Photo',
    'Наушники на бетонном подиуме, мягкий свет, минимализм': 'Earbuds on a concrete podium, soft light, minimalism', 'Сгенерировать': 'Generate',
    'Фото': 'Photo', 'Видео': 'Video', '4 варианта': '4 variants', 'Видео из кадра 2': 'Video from frame 2', 'Kling 3.0 · 5 с · 1080p': 'Kling 3.0 · 5 s · 1080p',
    'Шаблоны · Техника': 'Templates · Electronics', 'готово за 40 с': 'ready in 40 s', 'Квартира': 'Apartment', 'Авто': 'Auto', 'Техника': 'Electronics', 'Мебель': 'Furniture',
    'Снимок на телефон': 'Phone photo', 'Шаблон «Техника»': '“Electronics” template', 'Шаблон': 'Template', 'Ваше фото': 'Your photo', 'Студийный кадр': 'Studio shot',
    'One Launch · Кофемашина': 'One Launch · Coffee machine', 'кампания готова': 'campaign ready', 'Анализирую фото': 'Analyzing the photo', 'Генерирую 1:1': 'Generating 1:1',
    'Генерирую 9:16': 'Generating 9:16', 'Пишу тексты': 'Writing the copy', 'Текст для Instagram': 'Instagram caption',
    'Утро с идеальным эспрессо ☕ Aroma One — капучино за минуту, −26% всю неделю.': 'Mornings with the perfect espresso ☕ Aroma One — cappuccino in a minute, 26% off all week.',
    'Motion Engine · 15 с': 'Motion Engine · 15 s', 'рендер в браузере': 'rendered in browser', 'Время — ваше': 'Your time', 'Звук без проводов': 'Wireless sound',
    '03 · текст': '03 · text', 'Громко': 'Loud', 'Каждое утро': 'Every morning', 'Попробовать →': 'Try it →', 'Рендер · вариант 2': 'Render · variant 2', '−20% сегодня': '20% off today',
    'Составь контент-план на октябрь для кофейни: 3 поста в неделю, Instagram и Telegram': 'Make an October content plan for a coffee shop: 3 posts a week, Instagram and Telegram',
    'Неделя 1 · Сезонное меню': 'Week 1 · Seasonal menu', '— пн: тыквенный латте крупным планом': '— Mon: pumpkin latte close-up',
    'ср: рилс «как варим» · пт: опрос «какой сироп»': 'Wed: “how we brew” reel · Fri: “which syrup?” poll', 'Неделя 2 · Доставка': 'Week 2 · Delivery',
    '— до 30 минут, промокод для новых': '— under 30 minutes, a promo code for new customers', 'Контент-план на октябрь.docx': 'October content plan.docx',
    'Документ Word · 12 постов': 'Word document · 12 posts', 'Скачать': 'Download', 'Заголовки': 'Headlines', 'SEO-описание': 'SEO description', 'Контент-план': 'Content plan',
    'Проверить текст': 'Proofread', 'Музыка и аудио': 'Music & audio', 'трек готов': 'track ready', '♫ Музыка': '♫ Music', '◉ Речь': '◉ Speech', 'Промпт': 'Prompt',
    'Энергичный поп-рок с яркими гитарами для рекламы наушников': 'Energetic pop-rock with bright guitars for an earbuds ad',
    'Тренды · Все площадки': 'Trends · All platforms', 'за 7 дней': 'last 7 days', 'Товар в неожиданном масштабе': 'A product at an unexpected scale',
    'Один предмет — три сценария': 'One object — three scenarios', 'Почему покупатели возвращаются': 'Why customers come back', 'Честный обзор вместо рекламы': 'An honest review instead of an ad',
    'Распаковка без лица в кадре': 'Unboxing without showing a face', 'Лайков 318K': '318K likes', 'Почему в подборке': 'Why it made the list',
    'Гигантский товар в обычной сцене — зритель останавливается на первой секунде.': 'A giant product in an ordinary scene — viewers stop in the first second.',
    'Как применить': 'How to use it', 'Покажите свой товар крупнее жизни: наушники размером с диван.': 'Show your product larger than life: earbuds the size of a sofa.',
    'Создать сценарий': 'Create script', 'В ноды': 'To nodes', 'оценено 3 из 3': '3 of 3 scored', 'Сильнее остальных': 'Strongest', 'Контраст': 'Contrast',
    'Фокус взгляда': 'Visual focus', 'Читаемость': 'Readability', 'Заметность CTA': 'CTA visibility', 'Эмоц. крючок': 'Emotional hook', 'Визуальный шум': 'Visual noise',
    'Вывод:': 'Verdict:', 'вариант 2 сильнее — товар крупно, CTA читается в превью. Уберите лишний фон у варианта 1.':
        'variant 2 wins — the product is large and the CTA reads in the preview. Trim the busy background in variant 1.',
    'Стратегия · Кофейня': 'Strategy · Coffee shop', 'оценка 82/100': 'score 82/100', 'Какой результат вы хотите?': 'What result do you want?', 'Продажи': 'Sales',
    'Лиды': 'Leads', 'Узнаваемость': 'Awareness', 'Бюджет на месяц': 'Monthly budget', 'Осведомлённость': 'Awareness', 'Рассмотрение': 'Consideration', 'Конверсия': 'Conversion',
    'Студенты': 'Students', 'обед и вечер · 40%': 'lunch & evening · 40%', 'Офис': 'Office', 'доставка · 35%': 'delivery · 35%', 'Семьи': 'Families', 'выходные · 25%': 'weekends · 25%',
    'Создать workflow →': 'Create workflow →', 'пример': 'example', 'Кофейня, доставка. Нужны сторис на неделю под новое зимнее меню.': 'Coffee shop with delivery. Need a week of stories for the new winter menu.',
    'Аудитория': 'Audience', 'студенты и офис — заказывают в обед и вечером': 'students and office workers — they order at lunch and in the evening',
    'Зимний латте на тёплом фоне, мягкий утренний свет, крупный план': 'Winter latte on a warm background, soft morning light, close-up', 'Схема нод': 'Node graph',
    'Генерация фото': 'Image generation', 'Адаптация 9:16': 'Adaptation 9:16', 'Проверьте схему и нажмите «Запустить»': 'Check the graph and press “Run”',
    'Запустить пайплайн ▸': 'Run pipeline ▸', 'Мессенджер': 'Messenger', '3 в сети': '3 online', 'Контакты': 'Contacts', 'А': 'A', 'Аружан': 'Aruzhan', 'Д': 'D', 'Данияр': 'Daniyar',
    'М': 'M', 'Мадина': 'Madina', 'Айдос': 'Aidos', 'Проект «Весна»': '“Spring” project', 'группа · 4 участника': 'group · 4 members',
    'Сторис готовы — глянешь 9:16?': 'Stories are ready — can you check 9:16?', 'Супер, беру в работу': 'Great, I’m on it',
    'Тексты закинул в проект, проверьте CTA': 'Copy is in the project, please check the CTA', 'Айдос теперь в ваших контактах': 'Aidos is now in your contacts',
    # pricing
    # news cards under the menu (news.py, built-in cards)
    'Новинки ИИ-моделей': 'New AI models', 'Новая модель Google: 4K, в 2 раза дешевле': 'New Google model: 4K at half the price',
    # pricing: top-up slider (v5_ice.pricing_html)
    'Платите только за то, что создаёте': 'Pay only for what you create',
    'Без подписки и тарифов: пополняйте баланс на любую сумму. Кредиты действуют 12 месяцев — чем больше пополнение, тем выгоднее.':
        'No subscription, no plans: top up any amount. Credits stay valid for 12 months — the bigger the top-up, the better the rate.',
    'Вы получите': 'You get', '2\u2009750 кредитов': '2,750 credits', '55 кредитов за $1': '55 credits per $1', '+10% бонус': '+10% bonus',
    'Сумма пополнения': 'Top-up amount', '50 кредитов за $1': '50 credits per $1', '55 кредитов за $1 · +10%': '55 credits per $1 · +10%',
    '60 кредитов за $1 · +20%': '60 credits per $1 · +20%', 'Этого хватит примерно на': 'Enough for about',
    '50 кредитов в подарок при регистрации': '50 free credits when you sign up', 'Все разделы ONEFLOW и 30+ нейросетей': 'Every ONEFLOW mode and 30+ AI models',
    'Кредиты не сгорают 12 месяцев': 'Credits don’t expire for 12 months', 'Открыть демо': 'Open the demo',
    'Количество генераций — примерное: зависит от модели, длительности и разрешения.': 'Generation counts are approximate: they depend on the model, length and resolution.',
    'Тарифы': 'Pricing', 'Остаток бюджета — всегда ваш': 'Your leftover budget is always yours',
    'На любом тарифе неизрасходованный бюджет переходит на следующий месяц.': 'On every plan, unused budget rolls over to the next month.',
    'Период оплаты': 'Billing period', 'Месяц': 'Monthly', 'Год': 'Yearly', 'Попробовать': 'Try it', 'Демо-режим': 'Demo mode',
    'Откройте ONEFLOW без регистрации и посмотрите всё изнутри: разделы, ноды, Motion Engine.': 'Open ONEFLOW without signing up and look around: every section, the nodes, Motion Engine.',
    'Без регистрации и карты': 'No sign-up, no card', 'Все разделы программы': 'Every section of the app', 'Генерации показываются на примерах — ничего не списывается':
        'Generations are shown on examples — nothing is charged', 'Перейти на тариф — в любой момент': 'Switch to a plan anytime', 'Открыть демо →': 'Open the demo →',
    'Стартовый': 'Starter', '/ мес': '/ mo', 'Для первых карточек и тестов рекламы.': 'For your first product cards and ad tests.', 'Примерно генераций в месяц': 'Approx. generations per month',
    'видео': 'videos', 'фото': 'images', 'треков': 'music tracks', 'Музыкальный трек': 'Music track', 'Ролик 5 с, 720p, без звука': '5-second clip, 720p, no sound', 'Изображение 1K': '1K image', 'Изображение 1K · Sunburst': '1K image · Sunburst',
    'Все разделы ONEFLOW': 'Every ONEFLOW section', 'LLM-модели': 'LLM models', 'Адаптация визуалов': 'Visual adaptation', 'Выбрать': 'Choose', 'Популярный': 'Popular',
    'Для регулярной работы с генерацией.': 'For regular work with generation.', 'Выбрать →': 'Choose →', 'Максимальный': 'Max', 'Для команд без ограничений.': 'For teams, without limits.',
    'Всё из популярного': 'Everything in Popular', 'Приоритетная поддержка': 'Priority support',
    # faq, end, footer, support
    'Коротко о главном': 'The short version', 'Есть ли шаблоны для моей ниши?': 'Are there templates for my niche?',
    'Да, в разделе «Для бизнеса»: HoReCa для ресторанов и кафе, Квартира для риелторов, Авто для автодилеров, Техника для магазинов электроники, а также Мебель. Выберите шаблон, загрузите своё фото — получите студийный снимок в высоком разрешении.':
        'Yes, under “For business”: HoReCa for restaurants and cafés, Apartment for realtors, Auto for car dealers, Electronics for electronics stores, plus Furniture. Pick a template, upload your photo and get a high-resolution studio shot.',
    'Какие нейросети входят в ONEFLOW?': 'Which AI models are included in ONEFLOW?',
    'Фото: Nano Banana 2.1, Nano Banana Pro, Nano Banana 2, Nano Banana 2 Lite, GPT Image 2, GPT Image 2.5 Sunburst, GPT Image 2.5 Flare, Seedream 5 Pro, Seedream 5.0 Lite, Recraft V4 Styles Pro, Grok Imagine Image 2.0, Krea 2 Large.':
        'Images: Nano Banana 2.1, Nano Banana Pro, Nano Banana 2, Nano Banana 2 Lite, GPT Image 2, GPT Image 2.5 Sunburst, GPT Image 2.5 Flare, Seedream 5 Pro, Seedream 5.0 Lite, Recraft V4 Styles Pro, Grok Imagine Image 2.0, Krea 2 Large.',
    'Видео: Kling 3.0, Veo 3.1 Fast, Seedance 2.5, Seedance 2.0, Seedance 2.0 Mini, MiniMax Hailuo 3 Max, FLUX.3 Video.':
        'Video: Kling 3.0, Veo 3.1 Fast, Seedance 2.5, Seedance 2.0, Seedance 2.0 Mini, MiniMax Hailuo 3 Max, FLUX.3 Video.',
    'Вектор: Recraft V4 Vector.': 'Vector: Recraft V4 Vector.', 'Музыка: Lyria 3 Pro.': 'Music: Lyria 3 Pro.', 'Голос: Gemini 3.1 Flash TTS.': 'Voice: Gemini 3.1 Flash TTS.',
    'Тексты и аналитика: GPT-5.6, GPT-4.1, GPT-4.1 mini.': 'Copy and analytics: GPT-5.6, GPT-4.1, GPT-4.1 mini.',
    'Инструменты: Real-ESRGAN (апскейлер), Background Remover (удаление фона).': 'Tools: Real-ESRGAN (upscaler), Background Remover (background removal).',
    'Нужно ли заказывать фотографа?': 'Do I need to hire a photographer?',
    'Для большинства задач — нет: меню и доставка, объявления о продаже авто и квартир, карточки товаров. Снимите на телефон, выберите шаблон — и получите студийное качество без выезда фотографа и аренды студии.':
        'For most tasks, no: menus and delivery, car and apartment listings, product cards. Shoot on your phone, pick a template and get studio quality without a photographer or a studio rental.',
    'Что умеет ИИ-ассистент?': 'What can the AI assistant do?',
    'Разбирает нишу и подсказывает идеи, пишет и улучшает промпты, а по описанию задачи собирает схему нод на холсте. Запуск пайплайна и финальные решения — за вами.':
        'It researches your niche and suggests ideas, writes and improves prompts, and builds the node graph on the canvas from your task description. Running the pipeline and the final decisions are yours.',
    'Что значит «бюджет не сгорает»?': 'What does “budget doesn’t expire” mean?',
    'Неиспользованный за месяц бюджет переходит на следующий месяц и складывается с новым.': 'Budget you don’t use in a month rolls over to the next month and adds up with the new one.',
    'Почему генерация до 50% дешевле?': 'Why is generation up to 50% cheaper?',
    'Вы платите за генерации по ценам моделей — без наценок посредников и без подписки на каждый сервис. Итог зависит от моделей и объёма.':
        'You pay for generations at model prices — no reseller markups and no separate subscription for every service. The final saving depends on the models and volume.',
    'Какие размеры поддерживает адаптация?': 'What sizes does adaptation support?',
    'Любые — от сторис 9:16 до баннера 728×90, плюс пресеты Kaspi, GDN, Discovery, Яндекс РСЯ и BYYD.': 'Any — from 9:16 stories to a 728×90 banner, plus presets for Kaspi, GDN, Discovery, Yandex Ads and BYYD.',
    'Можно ли работать командой?': 'Can we work as a team?', 'Да — пригласите соавтора по почте и общайтесь во встроенном мессенджере.': 'Yes — invite a collaborator by email and talk in the built-in messenger.',
    'Не нашли ответ?': 'Didn’t find your answer?', 'Написать в поддержку': 'Contact support', 'Создавайте больше.': 'Create more.', 'Не теряйте ни доллара.': 'Don’t lose a dollar.',
    'Генерация до 50% дешевле*, любой размер одним кликом, бюджет не сгорает в конце месяца.': 'Generation up to 50% cheaper*, any size in one click, a budget that doesn’t expire at month-end.',
    'Конфиденциальность': 'Privacy', 'Условия': 'Terms', 'Возврат': 'Refunds', 'Поддержка': 'Support', 'Документы': 'Documents', 'Закрыть': 'Close', 'Наверх': 'Back to top',
    'Оставьте контакт — ответим на email или по телефону, который вы укажете.': 'Leave a contact — we’ll reply by the email or phone you give us.',
    'Как к вам обращаться': 'Your name', 'Email или телефон для ответа': 'Email or phone for our reply', 'Сообщение': 'Message', 'Сайт': 'Website', 'Отправить': 'Send',
}

JS = {
    'Закрыть меню': 'Close menu', 'Открыть меню': 'Open menu', 'Укажите email или телефон для ответа.': 'Please add an email or phone so we can reply.',
    'Опишите вопрос чуть подробнее.': 'Please describe your question in a little more detail.', 'Отправляем…': 'Sending…',
    'Не удалось отправить. Попробуйте позже.': 'Couldn’t send. Please try again later.', 'Спасибо! Сообщение отправлено — мы свяжемся с вами.': 'Thank you! Your message is on its way — we’ll get back to you.',
}

KEEP = {'Язык / Language'}  # bilingual on purpose
CYR = re.compile('[А-Яа-яЁё]')


def legal_en():
    """The English legal pages from the app (landing/legal_en.json is exported from src/legalContent.ts)."""
    docs = json.load(open(os.path.join(HERE, 'legal_en.json'), encoding='utf-8'))
    out = ''
    for key, src, label in (('privacy', 'privacy', 'Privacy'), ('terms', 'terms', 'Terms'), ('refunds', 'refund', 'Refunds')):
        d = docs[src]
        body = f'<h1>{d["title"]}</h1><p class="updated">{d["updated"]}</p><p>{d["intro"]}</p>' + ''.join(
            f'<h2>{s["heading"]}</h2>' + ''.join(f'<p>{p}</p>' for p in s['paragraphs']) for s in d['sections'])
        out += f'<dialog class="doc" id="doc-{key}" aria-label="{label}"><button type="button" class="x" aria-label="Close">×</button><div class="in2">{body}</div></dialog>'
    return out


def translate(html):
    html = html.replace('<html lang="ru">', '<html lang="en">', 1).replace('content="ru_RU"', 'content="en_US"')
    html = re.sub(r'aria-label="Анимация: как работает ([^"]+)"', lambda m: f'aria-label="Animation: how {EN.get(m.group(1), m.group(1))} works"', html)
    html = re.sub(r'aria-label="Нейросети в ONEFLOW: ([^"]+)"', lambda m: 'aria-label="AI models in ONEFLOW: ' + m.group(1).replace(
        'Real-ESRGAN (апскейлер)', 'Real-ESRGAN (upscaler)').replace('Background Remover (удаление фона)', 'Background Remover (background removal)') + '"', html)

    def node(m):
        raw = m.group(1); t = raw.strip()
        if not t or t not in EN:
            return m.group(0)
        return '>' + raw.replace(t, EN[t]) + '<'

    def attr(m):
        t = m.group(2)
        return f'{m.group(1)}="{EN.get(t, t) if t not in KEEP else t}"'

    parts = re.split(r'(<script>.*?</script>|<style>.*?</style>)', html, flags=re.S)
    for i, p in enumerate(parts):
        if p.startswith('<style>'):
            continue
        if p.startswith('<script>'):
            for a, b in JS.items():
                p = p.replace(f"'{a}'", f"'{b}'")
            parts[i] = p
            continue
        p = re.sub(r'>([^<>]+)<', node, p)
        parts[i] = re.sub(r'(aria-label|title|placeholder|content|alt)="([^"]+)"', attr, p)
    html = ''.join(parts)
    left = sorted({t.strip() for t in re.findall(r'>([^<>]+)<', re.sub(r'<(script|style)>.*?</\1>', '', html, flags=re.S)) if CYR.search(t)}
                  | {a for a in re.findall(r'(?:aria-label|title|placeholder|content|alt)="([^"]+)"', html) if CYR.search(a) and a not in KEEP})
    assert not left, 'untranslated: ' + ' | '.join(left[:20])
    return html
