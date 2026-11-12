// Puts the current «made in ONEFLOW» row script (made_band.js) into built landing pages, in place of
// the one that is there. A full rebuild of the landing is not possible everywhere (it needs the fonts
// and the legal texts), so the built pages are patched; everything else in them stays byte for byte.
//   node patch_made.mjs <page.html> [<page.html> …]
// The address of the API and the publishable key are taken from the page itself (its news script
// already carries them), never from this repository.
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const band = readFileSync(join(dirname(fileURLToPath(import.meta.url)), 'made_band.js'), 'utf8');
const START = '<script>\n// made in ONEFLOW: the curved row';

for (const page of process.argv.slice(2)) {
  const html = readFileSync(page, 'utf8');
  const from = html.indexOf(START);
  if (from < 0 || html.indexOf(START, from + 1) >= 0) throw new Error(`${page}: the row's script was not found exactly once`);
  const to = html.indexOf('</script>', from);
  const keys = /const SB = '(https:\/\/[^']+)', KEY = '([A-Za-z0-9._-]+)'/.exec(html);
  if (to < 0 || !keys) throw new Error(`${page}: the end of the script or the page's API settings were not found`);
  const script = band.replace('__SB__', keys[1]).replace('__KEY__', keys[2]);
  if (script.includes('__SB__') || script.includes('__KEY__')) throw new Error('made_band.js: a placeholder was left unfilled');
  writeFileSync(page, html.slice(0, from) + '<script>\n' + script + html.slice(to));
  console.log(`${page}: the row's script replaced (${to - from} → ${script.length + 9} bytes)`);
}
