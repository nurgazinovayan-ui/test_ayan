"""Переносит логику отправки брифа в новую версию .dc.html от дизайнера.

    python3 tools/port-send-logic.py "Mechta Inventory 2026.dc.html"

Нужен, когда дизайнер присылает новую вёрстку, сделанную от своей старой
копии, а не от .dc.html из репозитория: в такой версии отправка снова
исходная (старый вебхук, мёртвая форма Тильды, нет почты вендора).

Каждая правка привязана к точному фрагменту кода и проверяется: если
дизайн поменялся так, что фрагмент не найден ровно столько раз, сколько
ожидается, скрипт падает с указанием фрагмента и ничего не записывает.
Это и есть сигнал, что перенос нужно делать руками.

Заодно переносит правки вёрстки, сделанные поверх дизайна (бегущая строка
без фона). Они не обязательные: если фрагмент изменился, правка
пропускается с предупреждением.

Надёжнее, чтобы дизайнер работал от .dc.html из репозитория — тогда
переносить ничего не придётся.
"""
import io, sys
p = sys.argv[1]
s = io.open(p, encoding="utf-8").read()
def sub(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, ("не найдено ровно %d раз (%d): %r" % (n, c, a[:80]))
    s = s.replace(a, b)

# A. props: старый вебхук по умолчанию убираем, добавляем ключ и адрес
sub('&quot;default&quot;:&quot;https://hook.eu1.make.com/285o3j38x0rahlrkdtrd9agza589edat&quot;,&quot;tsType&quot;:&quot;string&quot;,&quot;section&quot;:&quot;Отправка брифа&quot;}}',
    '&quot;default&quot;:&quot;&quot;,&quot;tsType&quot;:&quot;string&quot;,&quot;section&quot;:&quot;Отправка брифа&quot;},'
    '&quot;web3formsKey&quot;:{&quot;editor&quot;:&quot;text&quot;,&quot;default&quot;:&quot;&quot;,&quot;tsType&quot;:&quot;string&quot;,&quot;section&quot;:&quot;Отправка брифа&quot;},'
    '&quot;emailTo&quot;:{&quot;editor&quot;:&quot;text&quot;,&quot;default&quot;:&quot;aidyn.argyn@mechta.kz&quot;,&quot;tsType&quot;:&quot;string&quot;,&quot;section&quot;:&quot;Отправка брифа&quot;}}')

# B. мёртвая форма Тильды (в iframe tilda-forms.js недоступен)
sub('          <form ref="{{ formRef }}" class="js-form-proccess t-form" method="POST" action="" data-formactiontype="2" data-formsuccess="popup" style="display: none"></form>\n', '')
sub('      formRef: el => { this._tildaForm = el; },\n', '')

# C. состояние: письмо открыто в клиенте ≠ отправлено
sub("sending: false, sent: false, sendError: '',", "sending: false, sent: false, mailed: false, sendError: '',")

# D. почта вендора для Reply-To
sub("    { id: 'owner', req: true, label: 'Ответственный', placeholder: 'имя / контакт' },",
    "    { id: 'owner', req: true, label: 'Ответственный', placeholder: 'имя / контакт' },\n"
    "    { id: 'contact_email', label: 'Email для связи', type: 'email', hint: 'на него менеджер ответит по брифу', placeholder: 'name@company.kz' },")

# E+F. отправка: проверка обязательных полей из нового дизайна сохраняется,
#      сама отправка — очередь каналов
start = s.index("    const text = this.briefText();\n    const v = this.state.brief;\n    const payload")
end = s.index("  copyText = (text) => {")
new = '''    const cfg = this.sendConfig();
    const v = this.state.brief;
    const subject = this.briefSubject();

    const payload = Object.assign({}, v, {
      services: this.state.picked.join('; '),
      brief_text: this.briefText(),
      Name: v.owner || '',
      subject: subject,
      formservices: 'Mechta Inventory 2026'
    });

    this.setState({ sending: true, sent: false, mailed: false, sendError: '' });

    // Каналы в порядке приоритета: первый успешный решает исход.
    // «Отправлено ✓» ставит только канал, который реально доставляет письмо.
    const channels = [];

    // 1. Вебхук (Make.com или свой сервер) — основной канал.
    if (cfg.webhookUrl) {
      channels.push(() => this.postJson(cfg.webhookUrl, payload));
    }

    // 2. Web3Forms — запас, если вебхука нет.
    if (cfg.web3formsKey) {
      channels.push(() => {
        // Служебные поля поверх payload, иначе одноимённое поле брифа их перетрёт.
        const w3 = Object.assign({}, payload, {
          access_key: cfg.web3formsKey,
          subject: subject,
          from_name: 'Mechta Inventory 2026'
        });
        // Web3Forms кладёт email в Reply-To. Адрес получателя туда ставить
        // нельзя: письмо на свой же домен от стороннего сервера антиспуфинг
        // считает подделкой. Только адрес вендора.
        const replyTo = String(v.contact_email || '').trim();
        if (replyTo) w3.email = replyTo;
        return this.postJson('https://api.web3forms.com/submit', w3)
          .then(r => r.json())
          .then(d => {
            // 200 с success: false — отказ (лимит, неподтверждённый адрес).
            if (!d || d.success !== true) throw new Error((d && d.message) || 'web3forms');
          });
      });
    }

    if (!channels.length) { this.openMailto(); return; }

    const attempt = (i) => {
      if (i >= channels.length) {
        this.setState(
          { sending: false, sendError: 'Письмо не ушло — открываем почтовый клиент, текст брифа в буфере.' },
          this.openMailto
        );
        return;
      }
      channels[i]().then(
        () => this.setState({ sending: false, sent: true }),
        () => attempt(i + 1)
      );
    };
    attempt(0);
  };

  // Конфиг из window.MECHTA_CONFIG (блок в начале автономной сборки),
  // иначе из props. Ключ правится в одном видном месте.
  sendConfig() {
    const c = (typeof window !== 'undefined' && window.MECHTA_CONFIG) || {};
    const pick = (a, b) => String(a !== undefined && a !== null && a !== '' ? a : (b || '')).trim();
    return {
      web3formsKey: pick(c.web3formsKey, this.props.web3formsKey),
      webhookUrl: pick(c.webhookUrl, this.props.webhookUrl),
      emailTo: pick(c.emailTo, this.props.emailTo) || 'aidyn.argyn@mechta.kz'
    };
  }

  postJson(url, body) {
    return fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify(body)
    }).then(r => {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r;
    });
  }

  openMailto = () => {
    this.copyToClipboard(this.briefText());
    try { window.location.href = this.mailtoHref(); } catch (e) {}
    this.setState({ sending: false, mailed: true });
  };

  briefSubject() {
    const c = this.state.brief.campaign;
    return 'Бриф кампании — Mechta Inventory 2026' + (c ? ': ' + c : '');
  }

  mailtoHref() {
    const full = this.briefText();
    // mailto в Windows/Outlook обрезается примерно на 2000 символах — режем сами.
    const body = full.length > 1600
      ? full.slice(0, 1600) + '\\n\\n…(полный текст брифа скопирован в буфер обмена — вставьте его сюда)'
      : full;
    return 'mailto:' + this.sendConfig().emailTo
      + '?subject=' + encodeURIComponent(this.briefSubject())
      + '&body=' + encodeURIComponent(body);
  }

  // В iframe navigator.clipboard есть, но writeText отклоняется permissions
  // policy. Поэтому сначала execCommand через временную textarea, затем API.
  copyToClipboard(text) {
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.cssText = 'position:fixed;top:-1000px;left:-1000px;opacity:0';
    document.body.appendChild(ta);
    let ok = false;
    try {
      ta.select();
      ta.setSelectionRange(0, ta.value.length);
      ok = document.execCommand('copy');
    } catch (e) { ok = false; }
    document.body.removeChild(ta);
    if (ok) return Promise.resolve(true);
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text).then(() => true, () => false);
    }
    return Promise.resolve(false);
  }

'''
s = s[:start] + new + s[end:]

# G. копирование списка и адреса — через общий помощник
start = s.index("  copyText = (text) => {")
# конец метода — его собственная закрывающая скобка: порядок методов
# в файлах дизайна разный, привязываться к соседям нельзя
end = s.index("\n  };\n", start) + len("\n  };\n")
s = s[:start] + '''  copyText = (text) => {
    this.copyToClipboard(text).then(() => {
      this.setState({ listCopied: true });
      clearTimeout(this._t2);
      this._t2 = setTimeout(() => this.setState({ listCopied: false }), 2000);
    });
  };
''' + s[end:]
start = s.index("  copyEmail = () => {")
end = s.index("\n  }", s.index("  copyEmail = () => {")) 
# найти конец метода copyEmail по закрывающему "  };"
end = s.index("\n  };\n", s.index("  copyEmail = () => {")) + len("\n  };\n")
s = s[:start] + '''  copyEmail = () => {
    this.copyToClipboard(this.sendConfig().emailTo).then(() => {
      this.setState({ copied: true });
      clearTimeout(this._t);
      this._t = setTimeout(() => this.setState({ copied: false }), 2000);
    });
  };
''' + s[end:]

# H. подписи кнопки: три исхода вместо двух
sub("      sendLabel: this.state.sent ? 'Отправлено ✓' : (this.state.sending ? 'Отправляем…' : 'Отправить бриф'),",
    "      sendLabel: this.state.sent ? 'Отправлено ✓'\n        : this.state.mailed ? 'Открыли письмо ✓'\n        : this.state.sending ? 'Отправляем…'\n        : 'Отправить бриф',")
sub("      sendBg: this.state.sent ? '#323237' : '#FF0080',", "      sendBg: (this.state.sent || this.state.mailed) ? '#323237' : '#FF0080',")
sub("      sendBg: s.sent ? '#3A3A40' : P,", "      sendBg: (s.sent || s.mailed) ? '#3A3A40' : P,")
sub("      sendBg: s.sent ? '#262626' : P,", "      sendBg: (s.sent || s.mailed) ? '#262626' : P,")

# I. возврат к вопросам обнуляет исход прошлой отправки
sub("      onBriefEdit: () => this.setState({ briefDone: false }),",
    "      onBriefEdit: () => this.setState({ briefDone: false, sent: false, mailed: false, sendError: '' }),")

# J. адрес на странице — из конфига, а не зашит
sub("      mailLabel: s.copied ? 'Скопировано ✓' : 'aidyn.argyn@mechta.kz'",
    "      mailLabel: s.copied ? 'Скопировано ✓' : this.sendConfig().emailTo")
sub("      copyLabel: this.state.copied ? 'Скопировано ✓' : 'aidyn.argyn@mechta.kz',",
    "      copyLabel: this.state.copied ? 'Скопировано ✓' : this.sendConfig().emailTo,")
sub("      headLabel: this.state.copied ? 'Скопировано ✓' : 'aidyn.argyn@mechta.kz',",
    "      headLabel: this.state.copied ? 'Скопировано ✓' : this.sendConfig().emailTo,")

# --- Правки вёрстки, сделанные поверх дизайна по просьбе заказчика ----------
# Не обязательные: если дизайнер сам изменил это место, правка пропускается
# с предупреждением и не мешает переносу отправки.
def soft_group(pairs, what):
    """Применяет набор правок только целиком: если хоть один фрагмент
    не найден ровно один раз, не трогает ни один."""
    global s
    if all(s.count(a) == 1 for a, _ in pairs):
        for a, b in pairs:
            s = s.replace(a, b)
    else:
        print("ПРОПУЩЕНО (фрагмент изменился, проверить вручную): " + what)

# Бегущая строка без фона: строка поверх видео хиро, а не отдельной тёмной
# полосой над ним. Хиро поднимается под строку, но отступ сверху и высота
# растут на её высоту (50 px = 22 px логотипы + 2 x 14 px), поэтому всё
# содержимое хиро и каталог остаются на прежних местах. Две правки связаны:
# без поднятой строки лишние 50 px у хиро дали бы пустой отступ сверху.
soft_group([
    ('<div style="position: relative; z-index: 2; overflow: hidden; padding: 14px 0">{{ ticker }}</div>',
     '<div style="position: absolute; top: 0; left: 0; right: 0; z-index: 2; overflow: hidden; padding: 14px 0">{{ ticker }}</div>'),
    ('min-height: clamp(480px, 72vh, 760px); display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px; padding: 64px 32px"',
     'min-height: calc(clamp(480px, 72vh, 760px) + 50px); display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px; padding: 114px 32px 64px"'),
], "бегущая строка без фона (строка поверх видео + отступ хиро)")

# Панель брифа на узких телефонах (320 px): min-width 320px плюс отступы
# страницы по 32 px не помещались — правый край панели и кнопка «Далее»
# уходили за экран. min(320px, 100%) не даёт панели стать шире экрана.
soft_group([
    ('<aside id="brief" ref="{{ asideRef }}" style="flex: 0 1 400px; min-width: 320px; max-width: 100%;',
     '<aside id="brief" ref="{{ asideRef }}" style="flex: 0 1 400px; min-width: min(320px, 100%); max-width: 100%;'),
], "панель брифа на экранах 320 px")

# Видео хиро для iPhone: MP4 (H.264) первым источником, исходный WebM —
# запасным. WebM у дизайнера — VP9 2206 px с объявленным, но не используемым
# альфа-каналом: Safari WebM с альфой не поддерживает, а VP9 такого размера
# на старых iPhone декодируется программно. Файл hero-video.mp4 делается из
# WebM так:
#   ffmpeg -c:v libvpx-vp9 -i hero-video.webm -an \
#     -vf "scale=1920:-2:flags=lanczos,format=yuv420p" -c:v libx264 \
#     -profile:v high -level:v 4.1 -preset slow -crf 23 -movflags +faststart \
#     hero-video.mp4
soft_group([
    ("h('video', { src: './hero-video.webm', autoPlay: true,", "h('video', { autoPlay: true,"),
    ("filter: 'brightness(0.92) saturate(1.15)' } })",
     "filter: 'brightness(0.92) saturate(1.15)' } },\n"
     "        h('source', { src: './hero-video.mp4', type: 'video/mp4' }),\n"
     "        h('source', { src: './hero-video.webm', type: 'video/webm' }))"),
], "видео хиро: MP4 для iPhone")

io.open(p, "w", encoding="utf-8").write(s)
print("перенос выполнен")
