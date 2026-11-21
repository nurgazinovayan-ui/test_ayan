// Adds what the ONEFLOW MCP page (mcp_page.py) needs to the landing pages already built for oneflow.art, changing
// nothing else:
//   1. the menu item «MCP» (→ /ru/mcp on the Russian page, /mcp on the English one), in the header and in the phone
//      menu, between the prices and the questions;
//   2. opening a document window by address (/ru#doc-privacy, /#doc-support …) — the MCP page's footer links to the
//      documents this way instead of carrying its own copies of them.
// Used like patch_why.mjs, when a full rebuild (build_vercel.py 5) is not possible on this machine:
//   node patch_mcp_nav.mjs <built ru.html> <built index.html>
// Running it twice changes nothing. After a full rebuild of the landing run it again.
import { readFileSync, writeFileSync } from 'node:fs';

const NAV = /(<nav aria-label="[^"]*">)(<a href="#why">[^<]*<\/a><a href="#pricing">[^<]*<\/a>)(<a href="#faq">[^<]*<\/a><\/nav>)/;
const MNAV = /(<nav class="mnav" id="mnav"[^>]*>)(<a href="#why">[^<]*<\/a><a href="#pricing">[^<]*<\/a>)(<a href="#faq">[^<]*<\/a>)/;
const DOCS = "document.querySelectorAll('[data-doc]').forEach((x) => x.addEventListener('click', () => { const d = document.getElementById('doc-' + x.dataset.doc); if (d && d.showModal) d.showModal(); }));";
// only the four known windows, by exact name: the address never becomes a selector or markup
const BY_HASH = "\n  { const byHash = () => { const m = /^#doc-(privacy|terms|refunds|support)$/.exec(location.hash); const d = m && document.getElementById('doc-' + m[1]); if (d && d.showModal && !d.open) d.showModal(); }; byHash(); addEventListener('hashchange', byHash); }";

for (const [file, href] of [[process.argv[2], '/ru/mcp'], [process.argv[3], '/mcp']]) {
  if (!file) throw new Error('usage: node patch_mcp_nav.mjs <built ru.html> <built index.html>');
  let s = readFileSync(file, 'utf8'); const before = s; const done = [];
  const link = `<a href="${href}">MCP</a>`;
  if (!s.includes(link)) {
    for (const [re, what] of [[NAV, 'header menu'], [MNAV, 'phone menu']]) {
      if (!re.test(s)) throw new Error(`${file}: ${what} not found`);
      s = s.replace(re, (_, a, b, c) => a + b + link + c);
    }
    done.push('menu item');
  }
  if (!s.includes('const byHash = ')) {
    if (s.split(DOCS).length !== 2) throw new Error(`${file}: the documents script not found`);
    s = s.replace(DOCS, DOCS + BY_HASH);
    done.push('documents by address');
  }
  if (s.split(link).length !== 3) throw new Error(`${file}: the menu item must be there twice`);
  if (s !== before) writeFileSync(file, s);
  console.log(file, done.length ? '+ ' + done.join(', ') : 'already patched', `(${s.length - before.length} bytes)`);
}
