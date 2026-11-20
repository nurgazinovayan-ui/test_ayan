"""A section with the node flow (idea → photo, copy → video, adaptation → done) on the landing, right after
«made in ONEFLOW» (the owner, 2026-11-20). The drawing is hero mock-up 14 of 2026-11-19, with colours taken from
the page theme, no outlines and no round pills; below 760 px the nodes stand in a column.
python3 -I patch_flow_section.py <ru.html> <index.html>"""
import sys

T = {
    'ru': dict(k='Ноды и адаптация', h='От идеи до рекламы — одним потоком',
               p='Соедините ноды в цепочку: из одного описания получаются фото, текст, видео и форматы под каждую площадку.',
               idea=('Идея', 'ваш текст', 'Кроссовки на чёрном фоне, лаймовые акценты, слоган «Беги быстрее»'),
               photo='Фото', text=('Текст', 'Беги быстрее', 'Заголовок, подпись и призыв — под каждую площадку.'),
               video=('Видео', '7 с', '♪ музыка'), adapt=('Адаптация', 'любой формат', 'Лента'),
               done=('Готово', 'Реклама готова', 'Скачать'), aria='Схема: как из идеи получается реклама'),
    'en': dict(k='Nodes & adaptation', h='From idea to ad — in one flow',
               p='Link nodes into a chain: one brief turns into a photo, copy, a video and formats for every platform.',
               idea=('Idea', 'your text', 'Sneakers on a black background, lime accents, the slogan “Run faster”'),
               photo='Photo', text=('Copy', 'Run faster', 'Headline, caption and call to action — for every platform.'),
               video=('Video', '7 s', '♪ music'), adapt=('Adaptation', 'any format', 'Feed'),
               done=('Done', 'Your ad is ready', 'Download'), aria='Diagram: how an idea becomes an ad'),
}

EDGES = ['M236,235 C276,235 276,125 316,125', 'M236,235 C276,235 276,376 316,376', 'M528,125 L612,125', 'M528,212 C572,212 568,330 612,330',
         'M528,376 C570,376 570,396 612,396', 'M912,125 L968,125']
PORTS = [(236, 235), (316, 125), (316, 376), (528, 125), (612, 125), (528, 212), (612, 330), (528, 376), (612, 396), (912, 125), (968, 125)]
SVG = ('<svg viewBox="0 0 1120 452" aria-hidden="true">' + ''.join(f'<path d="{d}"/><path class="run" d="{d}"/>' for d in EDGES)
       + ''.join(f'<circle cx="{x}" cy="{y}" r="4.5"/>' for x, y in PORTS) + '</svg>')
SCENE = ('<video autoplay muted loop playsinline preload="metadata" poster="/pe/scene.jpg" tabindex="-1">'
         '<source src="/pe/scene.mp4" type="video/mp4"><source src="/pe/scene.webm" type="video/webm"></video>')


def node(cls, color, title, model, body):
    return (f'<div class="fl-n {cls}"><div class="fl-nh"><i style="background:{color}"></i><b>{title}</b><span>{model}</span></div>'
            f'<div class="fl-nb">{body}</div></div>')


def section(lang):
    t = T[lang]
    pe = f'/pe/{lang}'
    return (f'<section class="sec flow" id="flow"><div class="wrap"><div class="sh rv"><span class="k">{t["k"]}</span><h2>{t["h"]}</h2><p>{t["p"]}</p></div>'
            f'<div class="fl-fit rv" role="img" aria-label="{t["aria"]}"><div class="fl-stage">{SVG}'
            + node('n-idea', 'var(--ink)', t['idea'][0], t['idea'][1], f'<p>{t["idea"][2]}</p><div class="fl-tags"><em>1:1</em><em>2K</em></div>')
            + node('n-photo', '#4c9bff', t['photo'], 'Nano Banana 2.1', f'<img src="{pe}/ad-11.webp" alt="" loading="lazy">')
            + node('n-text', '#c58bff', t['text'][0], 'Copywrite', f'<p><b>{t["text"][1]}</b>{t["text"][2]}</p>')
            + node('n-video', '#ff8a5c', t['video'][0], 'Cinema Engine', f'{SCENE}<div class="fl-tags"><em>{t["video"][1]}</em><em>21:9</em><em>{t["video"][2]}</em></div>')
            + node('n-adapt', '#6fe3a5', t['adapt'][0], t['adapt'][1],
                   f'<div class="fl-fm"><figure><img src="{pe}/ad-916.webp" alt="" loading="lazy"><figcaption>Stories</figcaption></figure>'
                   f'<figure><img src="{pe}/ad-45.webp" alt="" loading="lazy"><figcaption>{t["adapt"][2]}</figcaption></figure>'
                   f'<figure><img src="{pe}/ad-169.webp" alt="" loading="lazy"><figcaption>YouTube</figcaption></figure>'
                   f'<figure class="k"><img src="{pe}/ad-kaspi.webp" alt="" loading="lazy"><figcaption>Kaspi</figcaption></figure></div>')
            + node('n-done', '#6fe3a5', t['done'][0], '', f'<span class="fl-ok">✓</span><p>{t["done"][1]}</p><span class="fl-dl">{t["done"][2]}</span>')
            + '</div></div></div>'
            '<script>\n'
            '/* the node flow is drawn 1120 px wide; on a narrower page it is scaled to fit (a phone gets a column instead, see the styles) */\n'
            "(function () { var fit = document.querySelector('#flow .fl-fit'); if (!fit) return;\n"
            "  function size() { fit.style.setProperty('--fs', Math.min(1, fit.clientWidth / 1120).toFixed(4)); }\n"
            "  size(); if (window.ResizeObserver) new ResizeObserver(size).observe(fit); else window.addEventListener('resize', size);\n"
            '})();\n</script></section>')


CSS = """
/* the node flow after «made in ONEFLOW» (the owner, 2026-11-20): colours from the page theme, no outlines, no pills */
.flow .fl-fit { position: relative; margin-top: 52px; height: calc(452px * var(--fs, 1)); }
.flow .fl-fit::before { content: ""; position: absolute; z-index: 0; inset: -40px -24px; background-image: radial-gradient(color-mix(in srgb, var(--ink) 16%, transparent) 1px, transparent 1.4px); background-size: 24px 24px; -webkit-mask-image: radial-gradient(ellipse at center, #000 40%, transparent 78%); mask-image: radial-gradient(ellipse at center, #000 40%, transparent 78%); pointer-events: none; }
.flow .fl-stage { position: relative; z-index: 1; width: 1120px; height: 452px; margin: 0 auto; transform-origin: 0 0; transform: scale(var(--fs, 1)); text-align: left; }
.flow .fl-stage svg { position: absolute; inset: 0; width: 100%; height: 100%; overflow: visible; }
.flow .fl-stage path { fill: none; stroke: color-mix(in srgb, var(--ink) 24%, transparent); stroke-width: 1.5; }
.flow .fl-stage path.run { stroke: #0a6cff; stroke-width: 2; stroke-linecap: round; stroke-dasharray: 5 13; animation: fl-dash 1.6s linear infinite; }
html[data-theme="dark"] .flow .fl-stage path.run { stroke: #5aa2ff; }
@keyframes fl-dash { to { stroke-dashoffset: -36; } }
.flow .fl-stage circle { fill: var(--bg); stroke: #0a6cff; stroke-width: 2; }
html[data-theme="dark"] .flow .fl-stage circle { stroke: #5aa2ff; }
.flow .fl-n { position: absolute; display: flex; flex-direction: column; border-radius: 14px; background: var(--card); box-shadow: 0 26px 50px -30px rgba(0,0,0,.45); }
html[data-theme="dark"] .flow .fl-n { box-shadow: 0 30px 60px -30px rgba(0,0,0,.9); }
.flow .fl-nh { flex: none; height: 40px; padding: 0 13px; display: flex; align-items: center; gap: 8px; }
.flow .fl-nh i { width: 8px; height: 8px; border-radius: 50%; }
.flow .fl-nh b { font: 500 14px/1 var(--d); color: var(--ink); }
.flow .fl-nh span { margin-left: auto; font: 400 13px/1 var(--d); color: var(--muted); white-space: nowrap; }
.flow .fl-nb { flex: 1; min-height: 0; padding: 2px 12px 12px; display: flex; flex-direction: column; }
.flow .fl-nb p { margin: 0; font: 400 14px/1.42 var(--d); color: var(--ink2); }
.flow .fl-nb img, .flow .fl-nb video { display: block; width: 100%; border-radius: 8px; object-fit: cover; }
.flow .fl-tags { margin-top: auto; padding-top: 10px; display: flex; flex-wrap: wrap; gap: 5px; }
.flow .fl-tags em { height: 24px; padding: 0 8px; border-radius: 5px; display: inline-flex; align-items: center; font: 500 12px/1 var(--d); font-style: normal; color: var(--ink2); background: var(--field); }
.flow .n-idea { left: 0; top: 140px; width: 236px; height: 190px; }
.flow .n-photo { left: 316px; top: 0; width: 212px; height: 250px; }
.flow .n-photo img { height: 100%; min-height: 0; flex: 1; }
.flow .n-text { left: 316px; top: 300px; width: 212px; height: 152px; }
.flow .n-text p b { display: block; margin-bottom: 4px; font: 600 17px/1.15 var(--d); letter-spacing: -.02em; color: var(--ink); }
.flow .n-video { left: 612px; top: 0; width: 300px; height: 214px; }
.flow .n-video video { aspect-ratio: 992 / 432; }
.flow .n-adapt { left: 612px; top: 262px; width: 508px; height: 190px; }
.flow .n-adapt .fl-fm { flex: 1; display: flex; align-items: flex-end; gap: 12px; }
.flow .n-adapt figure { margin: 0; }
.flow .n-adapt figure img { width: auto; height: 104px; border-radius: 6px; }
.flow .n-adapt figure.k img { height: 44px; }
.flow .n-adapt figcaption { margin-top: 5px; font: 400 12px/1 var(--d); color: var(--muted); }
.flow .n-done { left: 968px; top: 40px; width: 152px; height: 170px; }
.flow .n-done .fl-nb { align-items: flex-start; gap: 8px; }
.flow .n-done .fl-ok { width: 30px; height: 30px; border-radius: 6px; display: grid; place-items: center; font: 600 15px/1 var(--d); color: #0b0b0d; background: #6fe3a5; }
.flow .n-done .fl-dl { margin-top: auto; align-self: stretch; height: 32px; border-radius: 6px; display: grid; place-items: center; font: 600 13px/1 var(--d); color: #fff; background: #0a6cff; }
/* a phone: the nodes in a column, a dashed line between them */
@media (max-width: 760px) {
  .flow .fl-fit { height: auto; margin-top: 36px; }
  .flow .fl-stage { width: auto; height: auto; transform: none; display: flex; flex-direction: column; gap: 28px; }
  .flow .fl-stage svg { display: none; }
  .flow .fl-n { position: relative; left: auto; top: auto; width: auto; height: auto; }
  .flow .fl-n + .fl-n::before { content: ""; position: absolute; left: 50%; top: -28px; height: 28px; border-left: 2px dashed #0a6cff; }
  .flow .fl-nh { height: 46px; } .flow .fl-nh b { font-size: 16px; } .flow .fl-nh span { font-size: 16px; }
  .flow .fl-nb p { font-size: 16px; } .flow .fl-tags em { height: 28px; font-size: 14px; }
  .flow .n-photo img { height: auto; aspect-ratio: 1; flex: none; }
  .flow .n-adapt .fl-fm { gap: 8px; } .flow .n-adapt figure img { height: 68px; } .flow .n-adapt figure.k img { height: 29px; }
  .flow .n-adapt figcaption { font-size: 13px; }
  .flow .n-done .fl-nb { flex-direction: row; align-items: center; gap: 12px; } .flow .n-done .fl-dl { margin: 0 0 0 auto; align-self: center; height: 40px; padding: 0 18px; font-size: 16px; }
}
@media (prefers-reduced-motion: reduce) { .flow .fl-stage path.run { animation: none; } }
"""

for lang, path in zip(('ru', 'en'), sys.argv[1:3]):
    s = open(path, encoding='utf-8').read()
    mark = '<section class="sec eng" id="engines">'
    assert s.count(mark) == 1 and 'id="flow"' not in s, path
    s = s.replace(mark, section(lang) + mark)
    end = s.rfind('</style>', 0, s.index('</head>'))
    s = s[:end] + CSS + s[end:]
    open(path, 'w', encoding='utf-8').write(s)
    print(lang, 'ok')
