"""Header buttons with small corner radii like the hero's, and the pricing calculator counted by the same models
as the strip under the hero (Seedance 2.5 480p 5 s = 48 credits, Suno V6 = 14).   python3 -I … <ru.html> <index.html>"""
import sys
CSS = """
/* the header (the owner, 2026-11-20): no round pills — small corner radii, as on the hero's buttons */
html[lang] .nav .btn, html[lang] .mnav .row .in2, html[lang] .mnav .row a { border-radius: 8px; }
/* the footer links did not fit one line on a phone in Russian and made the whole page slide sideways */
footer nav { flex-wrap: wrap; gap: 10px 20px; }
html[lang] .lang { border-radius: 8px; } html[lang] .lang a { border-radius: 6px; } html[lang] .thm { border-radius: 8px; }
"""
SW = {
 'ru': [('<b data-c="63">≈ 43</b> видео</span><span class="nw">Kling 3.0<span class="qm" tabindex="0" role="note" aria-label="Ролик 5 с, 720p, без звука" data-tip="Ролик 5 с, 720p, без звука">',
         '<b data-c="48">≈ 57</b> видео</span><span class="nw">Seedance 2.5<span class="qm" tabindex="0" role="note" aria-label="Ролик 5 с, 480p, со звуком" data-tip="Ролик 5 с, 480p, со звуком">'),
        ('<b data-c="8">≈ 343</b> треков</span><span class="nw">Lyria 3 Pro<span class="qm" tabindex="0" role="note" aria-label="Музыкальный трек" data-tip="Музыкальный трек">',
         '<b data-c="14">≈ 196</b> треков</span><span class="nw">Suno V6<span class="qm" tabindex="0" role="note" aria-label="Два варианта трека за запрос" data-tip="Два варианта трека за запрос">')],
 'en': [('<b data-c="63">≈ 43</b> videos</span><span class="nw">Kling 3.0<span class="qm" tabindex="0" role="note" aria-label="5-second clip, 720p, no sound" data-tip="5-second clip, 720p, no sound">',
         '<b data-c="48">≈ 57</b> videos</span><span class="nw">Seedance 2.5<span class="qm" tabindex="0" role="note" aria-label="5-second clip, 480p, with sound" data-tip="5-second clip, 480p, with sound">'),
        ('<b data-c="8">≈ 343</b> music tracks</span><span class="nw">Lyria 3 Pro<span class="qm" tabindex="0" role="note" aria-label="Music track" data-tip="Music track">', '<b data-c="14">≈ 196</b> music tracks</span><span class="nw">Suno V6<span class="qm" tabindex="0" role="note" aria-label="Two takes per request" data-tip="Two takes per request">')],
}
for lang, path in zip(('ru', 'en'), sys.argv[1:3]):
    s = open(path, encoding='utf-8').read()
    for a, b in SW[lang]:
        assert s.count(a) == 1, a
        s = s.replace(a, b)
    end = s.rfind('</style>', 0, s.index('</head>'))
    s = s[:end] + CSS + s[end:]
    open(path, 'w', encoding='utf-8').write(s)
    print(lang, 'ok')
