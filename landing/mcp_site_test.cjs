// The ONEFLOW MCP page inside the built site (the app repo's dist/), walked through like a visitor would:
//   node mcp_site_test.cjs <dist dir> <out dir for pictures>
// A small local server gives out dist/ the way the site's server is set up to (an address without .html is the file
// with .html; a folder is never taken for a page) — it stands in for the real server, it does not prove its settings.
const { chromium } = require('playwright'); const http = require('http'); const fs = require('fs'); const path = require('path');
const [dist, out] = process.argv.slice(2);
const TYPES = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.svg': 'image/svg+xml', '.webp': 'image/webp', '.png': 'image/png', '.jpg': 'image/jpeg', '.woff2': 'font/woff2', '.mp4': 'video/mp4', '.webm': 'video/webm' };
const isFile = (f) => { try { return fs.statSync(f).isFile(); } catch (e) { return false; } };
const server = http.createServer((req, res) => {
  const p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
  const root = path.resolve(dist); let f = path.resolve(root, '.' + (p === '/' ? '/index.html' : p));
  if (!f.startsWith(root + path.sep)) { res.writeHead(400); return res.end(); }
  if (!isFile(f)) f += '.html';
  if (!isFile(f)) { res.writeHead(404, { 'content-type': 'text/plain' }); return res.end('not found'); }
  res.writeHead(200, { 'content-type': TYPES[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(res);
});
(async () => {
  fs.mkdirSync(out, { recursive: true });
  await new Promise((r) => server.listen(0, '127.0.0.1', r)); const base = 'http://127.0.0.1:' + server.address().port;
  const b = await chromium.launch(); const notes = []; let checks = 0;
  const ok = (cond, what) => { checks++; if (!cond) notes.push(what); };
  const ctx = await b.newContext({ viewport: { width: 1440, height: 900 } });
  await ctx.route('**/*', (r) => r.request().url().startsWith(base) ? r.continue() : r.abort());
  const p = await ctx.newPage(); const errors = []; p.on('pageerror', (e) => errors.push(String(e)));
  const at = () => new URL(p.url()).pathname + new URL(p.url()).hash;
  for (const [home, mcp, otherMcp, lang, docTitle] of [['/ru', '/ru/mcp', '/mcp', 'ru', 'Политика'], ['/', '/mcp', '/ru/mcp', 'en', 'Privacy']]) {
    // the landing: still the landing, with the new menu item
    await p.goto(base + home); await p.waitForTimeout(500);
    ok((await p.evaluate(() => document.documentElement.lang)) === lang && await p.locator('#pricing').count() === 1, `${home}: not the ${lang} landing`);
    const item = p.locator('header.nav nav a', { hasText: /^MCP$/ });
    ok(await item.count() === 1 && (await item.getAttribute('href')) === mcp, `${home}: no MCP in the menu`);
    ok((await p.locator('header.nav nav a').allTextContents()).indexOf('MCP') === 2, `${home}: MCP is not the third item`);
    await p.screenshot({ path: path.join(out, `landing-${lang}-menu.png`), clip: { x: 0, y: 0, width: 1440, height: 420 } });
    // menu → the MCP page
    await item.click(); await p.waitForLoadState('load');
    ok(at() === mcp && (await p.locator('h1').textContent()).includes('ONEFLOW MCP'), `${home}: MCP opens ${at()}`);
    ok((await p.evaluate(() => document.documentElement.lang)) === lang, `${mcp}: lang`);
    // the links of the page lead where they say
    const hrefs = await p.evaluate(() => [...document.querySelectorAll('a[href]')].map((a) => a.getAttribute('href')));
    for (const h of [...new Set(hrefs)].filter((h) => h.startsWith('/'))) {
      const r = await ctx.request.get(base + h.split('#')[0]); ok(r.status() === 200, `${mcp}: link ${h} → ${r.status()}`); }
    ok(hrefs.every((h) => h.startsWith('/') || h.startsWith('#')), `${mcp}: a link leaves the site`);
    // the menu of the MCP page → back to a section of the landing
    await p.locator('header.nav nav a').first().click(); await p.waitForLoadState('load');
    ok(at() === home + '#why', `${mcp}: the first menu item opens ${at()}`);
    await p.goBack(); await p.waitForLoadState('load');
    // the footer → a document window of the landing opens by its address
    await p.locator('footer nav a').first().click(); await p.waitForLoadState('load'); await p.waitForTimeout(400);
    ok(at() === home + '#doc-privacy', `${mcp}: the footer opens ${at()}`);
    ok(await p.evaluate(() => document.getElementById('doc-privacy').open), `${home}#doc-privacy: the window did not open`);
    ok((await p.locator('#doc-privacy h1').textContent()).includes(docTitle), `${home}#doc-privacy: not the privacy text`);
    await p.goto(base + home + '#doc-support'); await p.reload(); await p.waitForTimeout(400);
    ok(await p.evaluate(() => document.getElementById('doc-support').open), `${home}#doc-support: the window did not open`);
    await p.goto(base + home + '#doc-<img src=x onerror=window.__x=1>'); await p.reload(); await p.waitForTimeout(300);
    ok(await p.evaluate(() => !window.__x && ![...document.querySelectorAll('dialog')].some((d) => d.open)), `${home}: a made-up address opened something`);
    // the language switch keeps the page
    await p.goto(base + mcp); await p.locator('.lang a:not([aria-current])').click(); await p.waitForLoadState('load');
    ok(at() === otherMcp, `${mcp}: the language switch opens ${at()}`);
  }
  ok((await ctx.request.get(base + '/ru')).status() === 200 && (await (await ctx.request.get(base + '/ru')).text()).includes('id="pricing"'), '/ru is not the landing');
  ok(!errors.length, 'script errors: ' + JSON.stringify(errors.slice(0, 3)));
  await b.close(); server.close();
  console.log(notes.length ? notes.join('\n') : `ok: ${checks} checks, no problems`); process.exit(notes.length ? 1 : 0);
})();
