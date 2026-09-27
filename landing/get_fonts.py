"""Download grotesk families from Google Fonts (latin, latin-ext for ₸, cyrillic; woff2) into fonts/ and write fonts.css."""
import hashlib
import os
import re
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
FAMILIES = {
    'Inter': '400;500;600;700;800', 'Inter Tight': '500;600;700;800', 'JetBrains Mono': '400;500;700', 'IBM Plex Mono': '400;500;600',
    'IBM Plex Sans': '400;500;600;700', 'Unbounded': '500;700;800;900', 'Onest': '400;500;600;700;800', 'Geologica': '400;500;600;700;800',
    'Golos Text': '400;500;600;700', 'Dela Gothic One': '400', 'Russo One': '400', 'Oswald': '500;600;700', 'Sofia Sans Extra Condensed': '700;800;900',
    'Rubik Mono One': '400', 'Manrope': '500;600;700;800', 'Montserrat': '600;800;900', 'Rubik': '500;700;900',
}


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=60).read()


out, seen = [], {}
for fam, w in FAMILIES.items():
    css = get(f'https://fonts.googleapis.com/css2?family={fam.replace(" ", "+")}:wght@{w}&display=swap').decode()
    for sub, block in re.findall(r'/\* ([\w-]+) \*/\s*(@font-face\s*{[^}]*})', css):
        if sub not in ('latin', 'latin-ext', 'cyrillic'):
            continue
        url = re.search(r'url\((https://[^)]+)\)', block).group(1)
        if url not in seen:
            name = re.sub(r'\W+', '', fam) + '-' + sub + '-' + hashlib.md5(url.encode()).hexdigest()[:6] + '.woff2'
            open(os.path.join(HERE, 'fonts', name), 'wb').write(get(url))
            seen[url] = name
        out.append(f'/* {sub} */\n' + block.replace(url, 'fonts/' + seen[url]))
    print(fam, 'ok')
open(os.path.join(HERE, 'fonts.css'), 'w').write('\n'.join(out) + '\n')
print(len(seen), 'files,', len(out), 'faces')
