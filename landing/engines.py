"""«Реклама от идеи до готового ролика» — the modes of Production Engine on the landing (by request, 2026-11-19):
Cinema Engine as one large card with the owner's scene playing in the real window of the app (by itself, silent,
in a loop), UGC, Casting and Atlas Engine as three cards with their whole windows, and the adaptation of one
layout to seven sizes. The section stands between «made in ONEFLOW» and «Почему ONEFLOW».

  python3 engines.py        writes engines_section.html (ru) and engines_section_en.html
  node patch_engines.mjs <built ru.html> <built index.html> [<site public dir>]   puts it into built pages

The styles are engines.css. The pictures are files, not text in the page: assets/pe/ (logos, the scene) and
assets/pe/<ru|en>/ (the windows in that language and the example layout in its sizes); the site serves them
from /pe/. The windows are screenshots of the app's demo build; the scene inside the Cinema window is the
owner's clip; the layout is an example made for this page with a made-up brand — not a customer's work.
"""
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# the hue of the light under each logo: the app's own (src/Cinema.css, --hue), violet for the adaptation
HUE = {'cinema': 212, 'ugc': 326, 'casting': 36, 'atlas': 158, 'adapt': 262}
LOGO = {
    'cinema': ('Cinema Engine', '--lg:url(/pe/cinema-engine.svg);--ar:1359/233;--lh:30px'),
    'ugc': ('UGC Engine', '--lg:url(/pe/ugc-engine.svg);--ar:1198/303;--lh:38px'),
    'casting': ('Casting Engine', '--lg:url(/pe/casting-engine.svg);--ar:640/160;--lh:38px'),
}
# name of a size (by language) and its pixels; the order is the order of the three columns
SIZES = [('src', '1080×1080', 800, 800), ('yt', '1920×1080', 800, 447), ('kaspi', '1125×330', 900, 264), ('st', '1080×1920', 540, 968),
         ('feed', '1080×1350', 720, 894), ('gdn', '1200×628', 800, 419), ('rsya', '1080×450', 800, 333)]
FILE = {'src': 'ad-11', 'yt': 'ad-169', 'kaspi': 'ad-kaspi', 'st': 'ad-916', 'feed': 'ad-45', 'gdn': 'ad-gdn', 'rsya': 'ad-rsya'}

T = {
    'ru': dict(
        h='Реклама от идеи<br>до готового ролика',
        cinema=('Кино по описанию', 'Кинематографичные кадры без специальных знаний: камера, оптика и движение уже настроены.'),
        facts=['Камера, оптика, движение — на барабанах', 'Продолжение и приквел сцены', 'Правка кадра по слоям'],
        ugc=('Ролики с блогером', 'Фото товара и одна реплика — готовый ролик по шаблону.'),
        casting=('Свой герой', 'Один лист с трёх ракурсов. Зовите в любую сцену по имени.'),
        atlas=('Правка без пересъёмки', 'Напишите, что заменить в кадре, — остальное не изменится.'),
        adapt_word='Адаптация', adapt=('Один макет — любой формат', 'Композиция перестраивается под размер, а не обрезается.'),
        names=dict(src='Исходник', yt='YouTube', kaspi='Kaspi', st='Stories', feed='Лента', gdn='GDN', rsya='РСЯ'),
        win=dict(cinema='Окно Cinema Engine: сцена в плеере, настройки камеры на барабанах', ugc='Окно UGC Engine: шаблоны роликов с блогером',
                 casting='Окно Casting Engine: лист персонажа с трёх ракурсов', atlas='Окно Atlas Engine: редактирование видео по слоям'),
        clip='Сцена, снятая в Cinema Engine', ad='Пример макета'),
    'en': dict(
        h='Ads from idea<br>to finished video',
        cinema=('Cinema from a description', 'Cinematic shots with no special skills: camera, lens and movement are already set.'),
        facts=['Camera, lens, movement — on the drums', 'A sequel and a prequel of a scene', 'Edit a shot by layers'],
        ugc=('Videos with a creator', 'A product photo and one line — a finished video from a template.'),
        casting=('Your own character', 'One sheet from three angles. Call them into any scene by name.'),
        atlas=('Edit without a reshoot', 'Say what to replace in the shot — the rest stays the same.'),
        adapt_word='Adaptation', adapt=('One layout — any format', 'The composition is rebuilt for each size, not cropped.'),
        names=dict(src='Source', yt='YouTube', kaspi='Kaspi', st='Stories', feed='Feed', gdn='GDN', rsya='Yandex Ads'),
        win=dict(cinema='The Cinema Engine window: a scene in the player, camera settings on the drums', ugc='The UGC Engine window: templates of videos with a creator',
                 casting='The Casting Engine window: a character sheet from three angles', atlas='The Atlas Engine window: editing a video by layers'),
        clip='A scene shot in Cinema Engine', ad='Example layout'),
}

e = lambda s: html.escape(s, quote=True)


def glow(key):
    return f'<span class="eng-cut"><span class="eng-glow" style="--h:{HUE[key]}"><i></i><i></i><i></i></span></span>'


def logo(key):
    if key == 'atlas':
        return '<span class="eng-logo eng-word" role="img" aria-label="Atlas Engine">Atlas <i>Engine</i></span>'
    name, style = LOGO[key]
    return f'<span class="eng-logo" role="img" aria-label="{name}" style="{style}"></span>'


def window(lang, key, t):
    img = f'<img src="/pe/{lang}/{"cine" if key == "cinema" else key}.webp" width="1440" height="900" loading="lazy" decoding="async" alt="{e(t["win"][key])}">'
    if key != 'cinema':
        return f'<div class="eng-win">{img}</div>'
    clip = (f'<video class="eng-clip" autoplay muted loop playsinline preload="metadata" poster="/pe/scene.jpg" aria-label="{e(t["clip"])}">'
            '<source src="/pe/scene.mp4" type="video/mp4"><source src="/pe/scene.webm" type="video/webm"></video>')
    return f'<div class="eng-win">{img}{clip}</div>'


def card(lang, key, t):
    title, text = t[key]
    return (f'<div class="eng-card">{glow(key)}{logo(key)}<h3 class="eng-t">{e(title)}</h3><p class="eng-p">{e(text)}</p>'
            f'{window(lang, key, t)}</div>')


def figure(lang, key, t):
    size, w, h = next((s, w, h) for k, s, w, h in SIZES if k == key)
    name = t['names'][key]
    return (f'<figure class="eng-fig"><img src="/pe/{lang}/{FILE[key]}.webp" width="{w}" height="{h}" loading="lazy" decoding="async" '
            f'alt="{e(t["ad"])}: {e(name)}, {size}"><figcaption>{e(name)} <span>{size}</span></figcaption></figure>')


def section(lang):
    t = T[lang]
    title, text = t['cinema']
    facts = ''.join(f'<li>{e(x)}</li>' for x in t['facts'])
    f = lambda k: figure(lang, k, t)
    return f"""<section class="sec eng" id="engines"><div class="wrap">
  <h2 class="eng-h rv">{t['h']}</h2>
  <div class="eng-card eng-big rv">{glow('cinema')}{logo('cinema')}
    <div><h3 class="eng-t">{e(title)}</h3><p class="eng-p">{e(text)}</p><ul class="eng-facts">{facts}</ul></div>
    {window(lang, 'cinema', t)}
  </div>
  <div class="eng-three rv">{card(lang, 'ugc', t)}{card(lang, 'casting', t)}{card(lang, 'atlas', t)}</div>
  <div class="eng-card eng-ad rv">{glow('adapt')}<span class="eng-logo eng-word" role="img" aria-label="{e(t['adapt_word'])}">{e(t['adapt_word'])}</span>
    <div class="eng-ad-copy"><h3 class="eng-t">{e(t['adapt'][0])}</h3><p class="eng-p">{e(t['adapt'][1])}</p></div>
    <div class="eng-ad-cols"><div>{f('src')}{f('yt')}{f('kaspi')}</div><div>{f('st')}</div><div>{f('feed')}{f('gdn')}{f('rsya')}</div></div>
  </div>
</div>
<script>
/* the scene of the Cinema card: plays only while it is on the screen, and not at all for a visitor who asked for less motion */
(function () {{
  var v = document.querySelector('#engines .eng-clip');
  if (!v) return;
  if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) {{ v.removeAttribute('autoplay'); v.pause(); return; }}
  if (!('IntersectionObserver' in window)) return;
  new IntersectionObserver(function (seen) {{
    if (seen[0].isIntersecting) {{ var p = v.play(); if (p && p.catch) p.catch(function () {{}}); }} else v.pause();
  }}, {{ threshold: 0.1 }}).observe(v);
}})();
</script>
</section>"""


def engines_css():
    return '\n/* engines:start */\n' + open(os.path.join(HERE, 'engines.css'), encoding='utf-8').read() + '/* engines:end */\n'


if __name__ == '__main__':
    for lang, name in (('ru', 'engines_section.html'), ('en', 'engines_section_en.html')):
        open(os.path.join(HERE, name), 'w', encoding='utf-8').write(section(lang) + '\n')
        print(name, len(section(lang)))
