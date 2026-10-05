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

     Схема: страница -> вебхук Make.com -> отправка письма -> ящик.
     Страница знает только про вебхук; чем именно Make отправляет письмо,
     ей неизвестно, поэтому способ отправки меняется без правки кода.

     1. В Make.com создать сценарий: Webhooks -> Custom webhook,
        скопировать его URL.
     2. Вторым шагом добавить Gmail -> Send an email.
        Подключение по OAuth: пароля нет, доступ выдаётся в браузере.
        Поля модуля:
            To          адрес, куда приходят брифы
            Subject     поле subject
            Content     поле brief_text
            Reply-To    поле contact_email (почта вендора из брифа)
     3. Вставить URL вебхука в webhookUrl ниже.
     4. Проверить связку через tools/send-test.html до правки лендинга.

     Почему не SMTP Яндекса, хотя почта на нём: доступ по протоколам
     IMAP/SMTP закрыт политикой организации (535 5.7.8 "This user does
     not have access rights to this service"). Gmail тут не костыль:
     проблема была не в том, что отправитель внешний, а в том, что
     Web3Forms подставлял mechta.kz в Reply-To — для антиспуфинга это
     подделка своего домена. Gmail ничем не притворяется.
     Если доступ по протоколам откроют, шаг Gmail меняется на
     Email -> Send an email с smtp.yandex.ru:465 SSL и паролем
     приложения из Яндекс ID. Остальная цепочка не трогается.

     Пока webhookUrl пуст, кнопка «Отправить бриф» открывает почтовый
     клиент с готовым письмом вместо автоматической отправки.
     ========================================================================== -->
<script>
window.MECHTA_CONFIG = {
  webhookUrl: '',                        // <- URL вебхука Make.com: основной канал
  emailTo: 'aidyn.argyn@mechta.kz',      // получатель письма-фоллбэка
  web3formsKey: ''                       // запасной канал, если вебхука нет
};
</script>
"""




# Хост-страница (Тильда) не может прочитать contentDocument чужого домена,
# поэтому высоту сообщаем сами через postMessage. Парный слушатель —
# в tilda-embed-iframe.txt.
HEIGHT_REPORTER = """
<script>
(function () {
  if (window.parent === window) return;   // открыт напрямую, не в iframe

  // Мерить documentElement.scrollHeight нельзя: рантайм ставит
  // html,body,#dc-root{height:100%} (support.js, FULL_PAGE_CSS), поэтому
  // scrollHeight не может стать меньше высоты самого iframe — высота росла
  // бы и не возвращалась назад, когда контента становится меньше (поиск,
  // смена категории). Поэтому измеряем реальный контент: низ самого
  // нижнего из блоков страницы.
  function contentHeight() {
    var host = document.querySelector('#dc-root > .sc-host')
            || document.getElementById('dc-root');
    var max = 0;
    if (host) {
      for (var i = 0; i < host.children.length; i++) {
        var bottom = host.children[i].getBoundingClientRect().bottom;
        if (bottom > max) max = bottom;
      }
      max += window.scrollY || 0;
    }
    // Разметка ещё не смонтирована — отдаём хоть что-то, чтобы не схлопнуть блок.
    if (max < 1) max = document.documentElement.scrollHeight;
    return Math.ceil(max);
  }

  var last = 0;
  function send() {
    var h = contentHeight();
    if (!h || Math.abs(h - last) < 8) return;   // дребезг на ±1px не слать
    last = h;
    // targetOrigin '*': наружу уходит только число высоты, домен хоста
    // заранее неизвестен (Тильда, кастомный домен, превью).
    window.parent.postMessage({ __mechtaHeight: h }, '*');
  }

  window.addEventListener('load', send);
  window.addEventListener('resize', send);
  if (window.ResizeObserver) new ResizeObserver(send).observe(document.documentElement);
  setInterval(send, 500);   // перерисовки React-рантайма ResizeObserver не всегда ловит
})();
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

def inline(path):
    js = io.open(path, encoding="utf-8").read()
    # </script> внутри строки закрыл бы тег и оборвал скрипт.
    return "<script>\n" + js.replace("</script>", "<\\/script>") + "\n</script>"


def main():
    html = io.open(SRC, encoding="utf-8").read()

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
    html = html.replace(head, head + CONFIG + HEIGHT_REPORTER, 1)

    io.open(OUT, "w", encoding="utf-8").write(html)
    print("собрано: %s (%.0f КБ)" % (os.path.basename(OUT), len(html.encode()) / 1024))


if __name__ == "__main__":
    main()
