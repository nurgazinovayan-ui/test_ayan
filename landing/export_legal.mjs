// Exports the app's legal texts (src/legalContent.ts in the app repo) for the landing's dialogs:
// legal_en.json (English page, index.html) and legal_ru.json (Russian page, ru.html).
// Run after the texts change, then rebuild:  node export_legal.mjs && python3 build_vercel.py 5
// node export_legal.mjs --draft <dir>  writes a preview copy to <dir> and lets placeholders ({{…}}) through.
import { writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const draft = process.argv[2] === '--draft' ? process.argv[3] : null;
if (process.argv[2] === '--draft' && !draft) throw new Error('usage: node export_legal.mjs --draft <dir>');
const { LEGAL_CONTENT, LEGAL_VERSION } = await import('/home/user/oneflow/src/legalContent.ts');

for (const lang of ['en', 'ru']) {
  const text = JSON.stringify(LEGAL_CONTENT[lang], null, 1);
  // a placeholder ({{…}}) means the text is not ready to publish
  if (!draft && /\{\{[^}]*\}\}/.test(text)) throw new Error(`${lang}: unfilled placeholder ${text.match(/\{\{[^}]*\}\}/)[0]}`);
  writeFileSync(join(draft ?? HERE, `legal_${lang}.json`), text + '\n');
}
console.log('legal edition', LEGAL_VERSION);
