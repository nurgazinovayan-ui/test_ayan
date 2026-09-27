// node fontsused.js page.html — font family+weight pairs actually rendered (1440 + 390, whole page scrolled, menu and dialogs opened)
const { chromium } = require('/opt/node22/lib/node_modules/playwright'); const path = require('path');
(async () => { const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }); const all = new Set();
  for (const w of [1440, 390]) { const p = await b.newPage({ viewport: { width: w, height: 900 } }); await p.goto('file://' + path.resolve(process.argv[2]));
    await p.evaluate(async () => { document.querySelectorAll('.rv').forEach((e) => e.classList.add('in')); for (let y = 0; y < document.body.scrollHeight; y += 600) { scrollTo(0, y); await new Promise((r) => setTimeout(r, 50)); }
      document.querySelectorAll('dialog').forEach((x) => { x.showModal(); x.close(); }); const m = document.getElementById('mnav'); if (m) m.hidden = false; document.querySelectorAll('details').forEach((d) => d.open = true); await document.fonts.ready; });
    await p.waitForTimeout(600); (await p.evaluate(() => [...document.fonts].filter((f) => f.status === 'loaded').map((f) => f.family.replace(/"/g, '') + '|' + f.weight))).forEach((x) => all.add(x)); await p.close(); }
  console.log(JSON.stringify([...all].sort())); await b.close(); })();
