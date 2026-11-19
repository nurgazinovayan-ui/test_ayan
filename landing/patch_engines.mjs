// Puts the «Реклама от идеи до готового ролика» section (engines.py) into the pages already built for
// oneflow.art, changing nothing else: the section goes in front of #why, its styles are added to the page's
// own <style>, and its files are copied to the site's public folder (served from /pe/).
//   python3 engines.py && node patch_engines.mjs <built ru.html> <built index.html> [<site public dir>]
// Running it again replaces the section and the styles with the current ones (no second copy).
import { cpSync, existsSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const BEFORE = '<section class="sec vh" id="why">';
const SECTION = /<section class="sec eng" id="engines">[\s\S]*?<\/section>/;
const STYLES = /\n\/\* engines:start \*\/[\s\S]*?\/\* engines:end \*\/\n/;
const css = '\n/* engines:start */\n' + readFileSync(join(HERE, 'engines.css'), 'utf8') + '/* engines:end */\n';
const count = (s, part) => s.split(part).length - 1;

const [ru, en, pub] = process.argv.slice(2);
if (!ru || !en) throw new Error('usage: node patch_engines.mjs <built ru.html> <built index.html> [<site public dir>]');
for (const [file, part] of [[ru, 'engines_section.html'], [en, 'engines_section_en.html']]) {
  const section = readFileSync(join(HERE, part), 'utf8').trim();
  if (!SECTION.test(section)) throw new Error(part + ' is not the section');
  let s = readFileSync(file, 'utf8');
  const before = s.length;
  if (SECTION.test(s)) s = s.replace(SECTION, () => section);
  else {
    if (count(s, BEFORE) !== 1) throw new Error('#why not found once in ' + file);
    s = s.replace(BEFORE, () => section + BEFORE);
  }
  if (STYLES.test(s)) s = s.replace(STYLES, () => css);
  else {
    const end = s.lastIndexOf('</style>', s.indexOf('</head>'));
    if (end < 0) throw new Error('no <style> in the head of ' + file);
    s = s.slice(0, end) + css + s.slice(end);
  }
  if (count(s, 'id="engines"') !== 1 || count(s, '/* engines:start */') !== 1) throw new Error('the section is not in ' + file + ' exactly once');
  writeFileSync(file, s);
  console.log(file, before, '→', s.length);
}
if (pub) {
  if (!existsSync(pub)) throw new Error('no such folder: ' + pub);
  cpSync(join(HERE, 'assets', 'pe'), join(pub, 'pe'), { recursive: true });
  console.log('files →', join(pub, 'pe'));
}
