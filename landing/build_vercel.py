"""Single-file Vercel build: inline fonts (only rendered family/weight pairs and the unicode subsets the text needs),
images (assets/… → data URIs, each stored once via CSS variables), favicon and legal-document dialogs.

python3 build_vercel.py 4   →  site/4-porcelain/index.html + out/ONEFLOW-4-Porcelain-vercel.zip
"""
import base64, json, os, re, subprocess, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
APPREPO = '/home/user/oneflow'
DOCS = [('privacy', 'Конфиденциальность'), ('terms', 'Условия'), ('refunds', 'Возврат')]


def uri(path, mime):
    return f'data:{mime};base64,' + base64.b64encode(open(path, 'rb').read()).decode()


def legal_dialogs():
    out = ''
    for k, t in DOCS:
        src = open(os.path.join(APPREPO, 'checkout-page', f'{k}.html'), encoding='utf-8').read()
        body = re.search(r'<div class="doc">(.*?)</div>\s*</body>', src, re.S).group(1).strip()
        out += f'<dialog class="doc" id="doc-{k}" aria-label="{t}"><button type="button" class="x" aria-label="Закрыть">×</button><div class="in2">{body}</div></dialog>'
    return out


def inline_fonts(html, used):
    blocks = re.findall(r'@font-face\s*{[^}]*}', open(os.path.join(HERE, 'fonts.css'), encoding='utf-8').read())
    text = set(re.sub(r'<[^>]+>', '', html))
    def covers(b):
        m = re.search(r'unicode-range:\s*([^;]+);', b)
        if not m:
            return True
        for part in m.group(1).split(','):
            a, _, z = part.strip()[2:].partition('-')
            lo, hi = int(a, 16), int(z or a, 16)
            if any(lo <= ord(c) <= hi for c in text):
                return True
        return False
    key = lambda b: re.search(r"font-family:\s*'([^']+)'", b).group(1) + '|' + re.search(r'font-weight:\s*(\d+)', b).group(1)
    keep = [b for b in blocks if key(b) in used and covers(b)]
    # variable fonts: one file per subset serves every weight → one @font-face with a weight range, file stored once
    byfile = {}
    for b in keep:
        f = re.search(r'url\((fonts/[^)]+)\)', b).group(1)
        byfile.setdefault(f, []).append(b)
    merged = []
    for f, bs in byfile.items():
        ws = sorted(int(re.search(r'font-weight:\s*(\d+)', b).group(1)) for b in bs)
        merged.append(re.sub(r'font-weight:\s*\d+;', f'font-weight: {ws[0]} {ws[-1]};' if ws[0] != ws[-1] else f'font-weight: {ws[0]};', bs[0]))
    keep = merged
    faces = '\n'.join(re.sub(r'url\((fonts/[^)]+)\)', lambda m: 'url(' + uri(os.path.join(HERE, m.group(1)), 'font/woff2') + ')', b) for b in keep)
    return html.replace('<link rel="stylesheet" href="fonts.css">', '<style>\n' + faces + '\n</style>', 1), len(keep)


def build4():
    sys.path.insert(0, HERE)
    import v4_porcelain as v
    html = v.build(docs=legal_dialogs())
    tmp = os.path.join(HERE, 'v4-porcelain.full.html'); open(tmp, 'w', encoding='utf-8').write(html)
    used = set(json.loads(subprocess.check_output(['node', os.path.join(HERE, 'fontsused.js'), tmp], cwd=HERE)))
    os.remove(tmp)
    html, nf = inline_fonts(html, used)
    for n in sorted(set(re.findall(r'assets/ol/([\w-]+)\.webp', html))):
        html = html.replace(f'assets/ol/{n}.webp', uri(os.path.join(HERE, 'assets', 'ol', f'{n}.webp'), 'image/webp'))
    html = html.replace('<meta name="theme-color"', f'<link rel="icon" href="{uri(os.path.join(APPREPO, "public", "favicon.svg"), "image/svg+xml")}" type="image/svg+xml">\n<meta name="theme-color"', 1)
    assert 'assets/' not in html and 'fonts/' not in html
    bad = r'(?<![\w-])(?:src|href)="(?!data:|#|https://oneflow\.kz/)'
    assert not re.search(bad, html), re.findall(r'.{40}' + bad + r'.{30}', html)[:3]
    d = os.path.join(HERE, 'site', '4-porcelain'); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(html)
    os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
    with zipfile.ZipFile(os.path.join(HERE, 'out', 'ONEFLOW-4-Porcelain-vercel.zip'), 'w', zipfile.ZIP_DEFLATED) as z:
        z.write(os.path.join(d, 'index.html'), 'index.html')
    print(f'site/4-porcelain/index.html {len(html.encode()) // 1024} KB, {nf} font faces, fonts used {sorted(used)}')


if __name__ == '__main__':
    {'4': build4}[sys.argv[1] if len(sys.argv) > 1 else '4']()
