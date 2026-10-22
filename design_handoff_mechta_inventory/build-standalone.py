#!/usr/bin/env python3
"""Собирает автономную Mechta Inventory 2026.html из .dc.html.

Запускать после любой правки .dc.html — иначе файл, который уходит в Тильду,
расходится с прототипом (ровно это и случилось с прежней сборкой: она
предшествовала бриф-квизу и не содержала его вовсе).

    python3 build-standalone.py
"""
import base64, io, json, os, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "Mechta Inventory 2026.dc.html")
OUT = os.path.join(HERE, "Mechta Inventory 2026.html")

# Блок настройки идёт первым в <head>, чтобы ключ правился в одном видном
# месте, а не внутри HTML-экранированного data-props где-то в середине файла.
CONFIG = """
<!-- ==========================================================================
     НАСТРОЙКА ОТПРАВКИ БРИФА

     Схема: страница -> вебхук Make.com -> Gmail -> ящик.
     Страница знает только про вебхук; чем Make отправляет письмо, ей
     неизвестно, поэтому способ отправки меняется без правки кода.

     Значения ниже подставляются при сборке из site.config.json. Править
     лучше там: тогда при следующей версии дизайна ничего не придётся
     вводить заново. Править прямо здесь тоже можно — до следующей сборки.

     Пока webhookUrl пуст, кнопка «Отправить бриф» открывает почтовый
     клиент с готовым письмом вместо автоматической отправки.
     Подробности и разбор ошибок — в README.md.
     ========================================================================== -->
<script>
window.MECHTA_CONFIG = {
  webhookUrl: '%(webhookUrl)s',          // <- URL вебхука Make.com: основной канал
  emailTo: '%(emailTo)s',                // адрес на странице и для письма-фоллбэка
  web3formsKey: '%(web3formsKey)s'       // запасной канал, если вебхука нет
};
</script>
"""






# support.js (строка ~158) при отсутствии window.__resources до-загружает
# собственный URL ещё раз и перезаписывает шаблон результатом разбора —
# механика hot-reload редактора. В автономной сборке это ломает страницу:
# по file:// запрос рубит CORS и всё работает случайно, а по http(s) —
# то есть на любом реальном хостинге — fetch удаётся, разбор инлайненного
# файла даёт пустой шаблон, и страница рендерится пустой.
# Пустой объект отключает это и безопасен: все обращения к __resources
# в рантайме — это res ? res[url] : undefined.
RESOURCES_GUARD = """
<script>window.__resources = {};</script>
"""

# Полосы прокрутки. Страница живёт в iframe высотой в экран и прокручивается
# внутри него, поэтому у правого края iframe появлялась стандартная светлая
# полоса (на Windows ~15 px) — на тёмном дизайне она бросалась в глаза.
# Полосу страницы прячем: колесо, тачпад, свайп и клавиши продолжают работать.
# Во внутренних блоках (панель брифа на невысоких экранах) полосу не прячем —
# по ней видно, что блок прокручивается, — а делаем тонкой и тёмной.
# Стоит в сборке, а не в файле дизайна, чтобы пережить следующие его версии.
SCROLLBAR_STYLE = """
<style>
  html, body { scrollbar-width: none; }
  html::-webkit-scrollbar, body::-webkit-scrollbar { display: none; }
  * { scrollbar-width: thin; scrollbar-color: #3F3F46 transparent; }
  *::-webkit-scrollbar { width: 6px; height: 6px; }
  *::-webkit-scrollbar-thumb { background: #3F3F46; border-radius: 3px; }
  *::-webkit-scrollbar-track { background: transparent; }
</style>
"""

def inline(path):
    js = io.open(path, encoding="utf-8").read()
    # </script> внутри строки закрыл бы тег и оборвал скрипт.
    return "<script>\n" + js.replace("</script>", "<\\/script>") + "\n</script>"


# Ассеты дизайна. Шрифты и SVG вшиваются в файл: логотип читается в canvas
# через getImageData, и data:-картинка, в отличие от отдельного файла при
# открытии с диска, canvas не «загрязняет». Видео (1,9 МБ) остаётся рядом:
# вшитое в base64 оно раздуло бы HTML втрое и не могло бы грузиться потоком,
# а интро-анимация и так переживает его отсутствие по таймауту.
INLINE_ASSETS = [
    ("url('fonts/FormaDJRCyrillicMicro-Regular.otf')", "fonts/FormaDJRCyrillicMicro-Regular.otf", "font/otf", "url('%s')"),
    ("url('fonts/FormaDJRCyrillicDisplay-Bold.otf')", "fonts/FormaDJRCyrillicDisplay-Bold.otf", "font/otf", "url('%s')"),
    ('src="./mechta-logo-hero.svg"', "mechta-logo-hero.svg", "image/svg+xml", 'src="%s"'),
    ('src="./mechta-logo-small.svg"', "mechta-logo-small.svg", "image/svg+xml", 'src="%s"'),
    ("src: './ticker.svg'", "ticker.svg", "image/svg+xml", "src: '%s'"),
]
# MP4 (H.264) идёт первым источником: его аппаратно декодирует любой iPhone.
# Исходный WebM — VP9 2206 px с объявленным, но не используемым альфа-каналом:
# Safari WebM с альфой не поддерживает, а VP9 такого размера на старых
# iPhone декодируется программно. WebM остаётся запасным для браузеров без H.264.
SIDE_FILES = ["hero-video.mp4", "hero-video.webm"]

# Настройки отправки живут отдельно от вёрстки: при новой версии дизайна
# их не нужно вводить заново — сборка подставит их сама.
SITE_CONFIG = os.path.join(HERE, "site.config.json")
DEFAULTS = {"webhookUrl": "", "emailTo": "aidyn.argyn@mechta.kz", "web3formsKey": ""}

DIST = os.path.join(HERE, "dist")
# Обе копии: какой бы адрес ни стоял в iframe на Тильде — корень сайта
# или имя файла, — после повторной выкладки папки он продолжит работать.
DIST_NAMES = ["index.html", "Mechta Inventory 2026.html"]


def site_config():
    cfg = dict(DEFAULTS)
    if os.path.isfile(SITE_CONFIG):
        cfg.update(json.load(io.open(SITE_CONFIG, encoding="utf-8")))
    for k, v in cfg.items():
        # значение уходит в JS-строку в одинарных кавычках
        if not isinstance(v, str) or any(c in v for c in "'\\\n\r<"):
            raise SystemExit("недопустимое значение %s в site.config.json" % k)
    return cfg


def data_uri(path, mime):
    raw = io.open(os.path.join(HERE, path), "rb").read()
    return "data:%s;base64,%s" % (mime, base64.b64encode(raw).decode("ascii"))


def main():
    html = io.open(SRC, encoding="utf-8").read()

    for needle, path, mime, fmt in INLINE_ASSETS:
        if html.count(needle) != 1:
            raise SystemExit("ссылка на ассет не найдена ровно один раз: " + needle)
        html = html.replace(needle, fmt % data_uri(path, mime))

    # support.js требует window.React / window.ReactDOM — инлайним обе перед ним,
    # чтобы файл открывался офлайн и с file://, без CDN.
    scripts = "\n".join([
        RESOURCES_GUARD,
        inline(os.path.join(HERE, "vendor", "react.js")),
        inline(os.path.join(HERE, "vendor", "react-dom.js")),
        inline(os.path.join(HERE, "support.js")),
    ])

    tag = '<script src="./support.js"></script>'
    if tag not in html:
        raise SystemExit("не найден тег support.js в " + SRC)
    html = html.replace(tag, scripts)

    head = "<head>"
    if head not in html:
        raise SystemExit("не найден <head> в " + SRC)
    cfg = site_config()
    # Замера высоты для родительской страницы здесь больше нет: новый дизайн —
    # полноэкранная страница со своей прокруткой (липкая панель брифа,
    # прокрутка к форме, прелоадер position: fixed). В iframe, растянутом по
    # высоте контента, всё это ломается, а fixed-прелоадер ещё и возвращает
    # замеру его же высоту — iframe рос без остановки. Поэтому iframe теперь
    # высотой в экран, и страница прокручивается внутри него (см.
    # tilda-embed-iframe.txt).
    html = html.replace(head, head + (CONFIG % cfg) + SCROLLBAR_STYLE, 1)

    # Рядом с исходником — для просмотра: видео лежит в той же папке.
    io.open(OUT, "w", encoding="utf-8").write(html)

    # dist/ — то, что выкладывается на хостинг целиком.
    os.makedirs(DIST, exist_ok=True)
    for name in DIST_NAMES:
        io.open(os.path.join(DIST, name), "w", encoding="utf-8").write(html)
    for name in SIDE_FILES:
        shutil.copyfile(os.path.join(HERE, name), os.path.join(DIST, name))

    print("собрано: %s (%.0f КБ) + %s" % (
        ", ".join(DIST_NAMES), len(html.encode()) / 1024, ", ".join(SIDE_FILES)))
    print("webhookUrl: %s" % (cfg["webhookUrl"] or "(пусто — заполнить в site.config.json)"))


if __name__ == "__main__":
    main()
