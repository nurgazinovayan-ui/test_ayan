// Puts the «Почему ONEFLOW» section (why.py) into the pages already built for oneflow.art, changing nothing else:
// the tabbed #modes section gives way to #why, its styles are added, the menu and the hero link point to it.
// Used when a full rebuild (build_vercel.py 5) is not possible on this machine (no Origin font files, no legal export):
//   python3 v5_ice.py soft && node patch_why.mjs <built ru.html> <built index.html>
// The new markup and menu are taken from the fresh previews (v6-soft.html, v6-soft-en.html), so both ways give the same section.
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const SECTION = /<section class="sec vh" id="why">[\s\S]*?<\/section>/;
const OLD = /<section class="sec" id="modes">[\s\S]*?<\/section>/;
const NAV = /(<nav aria-label="[^"]*">)([\s\S]*?)(<\/nav>)/;
const MNAV = /(<nav class="mnav" id="mnav"[^>]*>)([\s\S]*?)(<div class="row">)/;
const one = (s, re, what) => { const m = s.match(re); if (!m) throw new Error('not found: ' + what); return m; };
const css = '\n/* «Почему ONEFLOW»: the advantages, a bento grid */\n' + readFileSync(join(HERE, 'why.css'), 'utf8');

for (const [file, preview] of [[process.argv[2], 'v6-soft.html'], [process.argv[3], 'v6-soft-en.html']]) {
  const fresh = readFileSync(join(HERE, preview), 'utf8');
  let s = readFileSync(file, 'utf8');
  const before = s.length;
  if (SECTION.test(s)) { console.log(file, 'already has the section'); continue; }
  const section = one(fresh, SECTION, 'new section in ' + preview)[0];
  const links = one(fresh, NAV, 'menu in ' + preview)[2];
  // the links the preview's phone menu starts with (before the theme switch and the buttons)
  const mlinks = one(fresh, MNAV, 'phone menu in ' + preview)[2];
  one(s, OLD, '#modes in ' + file);
  s = s.replace(OLD, () => section);
  s = s.replace(NAV, (_, a, _old, z) => a + links + z);
  s = s.replace(MNAV, (_, a, _old, z) => a + mlinks + z);
  s = s.replace(/href="#modes"/g, 'href="#why"');
  const at = s.indexOf('</style>', s.indexOf('<head'));
  if (at < 0) throw new Error('no <style> in ' + file);
  const end = s.lastIndexOf('</style>', s.indexOf('</head>'));
  s = s.slice(0, end) + css + s.slice(end);
  if (/href="#(modes|tpl|ai)"/.test(s)) throw new Error('a link to a removed anchor is left in ' + file);
  writeFileSync(file, s);
  console.log(file, before, '→', s.length);
}
