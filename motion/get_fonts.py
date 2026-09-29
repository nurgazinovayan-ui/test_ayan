"""Download the extra families the unusual looks need (handwriting, pixel, retro) into fonts/ and write fonts-extra.css."""
import hashlib, os, re, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
FAMILIES = {'Caveat': '500;700', 'Pangolin': '400', 'Pixelify Sans': '400;700', 'Press Start 2P': '400', 'Rubik Mono One': '400', 'Oswald': '500;700',
            'Playfair Display': '400;700;900', 'PT Serif': '400;700', 'Nunito': '700;900', 'Manrope': '200;300;500', 'Russo One': '400', 'Rubik': '500;700;900'}
get = lambda u: urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': UA}), timeout=60).read()
out, seen = [], {}
for fam, w in FAMILIES.items():  # noqa: B007
    css = get(f'https://fonts.googleapis.com/css2?family={fam.replace(" ", "+")}:wght@{w}&display=swap').decode()
    for sub, block in re.findall(r'/\* ([\w-]+) \*/\s*(@font-face\s*{[^}]*})', css):
        if sub not in ('latin', 'latin-ext', 'cyrillic', 'cyrillic-ext'):  # everything the Russian copy needs
            continue
        url = re.search(r'url\((https://[^)]+)\)', block).group(1)
        if url not in seen:
            name = re.sub(r'\W+', '', fam) + '-' + sub + '-' + hashlib.md5(url.encode()).hexdigest()[:6] + '.woff2'
            open(os.path.join(HERE, 'fonts', name), 'wb').write(get(url)); seen[url] = name
        out.append(block.replace(url, 'fonts/' + seen[url]))
    print(fam, 'ok', sum(1 for b in out if fam in b))
open(os.path.join(HERE, 'fonts-extra.css'), 'w').write('\n'.join(out) + '\n')
