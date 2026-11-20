"""The landing and the login screen, 2026-11-20: no demo button anywhere, and Recraft and Krea are no longer named
(a vector names no model at all). Run from the root of the main repo."""
import re
for path, lang in (('landing/ru.html', 'ru'), ('landing/index.html', 'en')):
    s = open(path, encoding='utf-8').read()

    def once(a, b, n=1):
        global s
        assert s.count(a) == n, (path, a[:70], s.count(a))
        s = s.replace(a, b)

    demo = {'ru': ('Демо', 'Открыть демо'), 'en': ('Demo', 'Open the demo')}[lang]
    once(f'<a class="btn g" href="/app?demo=1">{demo[0]}</a>', '')
    once(f'<a class="btn w" data-app="demo" href="/app?demo=1">{demo[1]}</a>', '')
    for name in ('Krea 2 Large', 'Recraft V4 Styles Pro', 'Recraft V4 Vector'):
        once(f'<span>{name}</span>', '', 2)
    once('Recraft V4 Styles Pro, Grok Imagine Image 2.0, Krea 2 Large, Kling 3.0', 'Grok Imagine Image 2.0, Kling 3.0')
    once('Recraft V4 Styles Pro, Grok Imagine Image 2.0, Krea 2 Large.', 'Grok Imagine Image 2.0.')
    once('Recraft V4 Vector, Lyria 3 Pro', 'Lyria 3 Pro')
    once({'ru': '<br>Вектор: Recraft V4 Vector.', 'en': '<br>Vector: Recraft V4 Vector.'}[lang], '')
    assert 'Recraft' not in s and 'Krea' not in s and 'demo=1"' not in s, path
    open(path, 'w', encoding='utf-8').write(s)
    print(path, 'ok')
