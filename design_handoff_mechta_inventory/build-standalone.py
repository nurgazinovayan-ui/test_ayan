#!/usr/bin/env python3
"""Собирает автономную Mechta Inventory 2026.html из .dc.html.

Запускать после любой правки .dc.html — иначе файл, который уходит в Тильду,
расходится с прототипом (ровно это и случилось с прежней сборкой: она
предшествовала бриф-квизу и не содержала его вовсе).

    python3 build-standalone.py
"""
import io, os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "Mechta Inventory 2026.dc.html")
OUT = os.path.join(HERE, "Mechta Inventory 2026.html")

# Блок настройки идёт первым в <head>, чтобы ключ правился в одном видном
# месте, а не внутри HTML-экранированного data-props где-то в середине файла.
CONFIG = """
<!-- ==========================================================================
     НАСТРОЙКА ОТПРАВКИ БРИФА

     1. Получите Access Key на https://web3forms.com — укажите почту, ключ
        придёт письмом (подтвердите адрес по ссылке из него).
     2. Вставьте ключ в web3formsKey ниже и сохраните файл.
     3. Загрузите файл в Тильду: Настройки сайта -> Файлы, затем вставьте
        iframe из tilda-embed-iframe.txt в блок T123.

     Пока web3formsKey пуст, кнопка «Отправить бриф» открывает почтовый
     клиент с готовым письмом вместо автоматической отправки.
     ========================================================================== -->
<script>
window.MECHTA_CONFIG = {
  web3formsKey: '',                      // <- Access Key от web3forms.com
  emailTo: 'aidyn.argyn@mechta.kz',      // получатель письма и Reply-To
  webhookUrl: ''                         // необязательно: Make.com / свой эндпоинт
};
</script>
"""


def inline(path):
    js = io.open(path, encoding="utf-8").read()
    # </script> внутри строки закрыл бы тег и оборвал скрипт.
    return "<script>\n" + js.replace("</script>", "<\\/script>") + "\n</script>"


def main():
    html = io.open(SRC, encoding="utf-8").read()

    # support.js требует window.React / window.ReactDOM — инлайним обе перед ним,
    # чтобы файл открывался офлайн и с file://, без CDN.
    scripts = "\n".join([
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
    html = html.replace(head, head + CONFIG, 1)

    io.open(OUT, "w", encoding="utf-8").write(html)
    print("собрано: %s (%.0f КБ)" % (os.path.basename(OUT), len(html.encode()) / 1024))


if __name__ == "__main__":
    main()
