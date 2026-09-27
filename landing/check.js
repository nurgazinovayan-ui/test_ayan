// node check.js page.html [...] — overflow at 1440/1024/390/360, console errors, external requests, calculator ($3 000 at $500), yearly toggle, menu
const { chromium } = require('/opt/node22/lib/node_modules/playwright'); const path = require('path');
(async () => { const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  for (const f of process.argv.slice(2)) { const file = path.resolve(f), res = [];
    for (const w of [1440, 1024, 390, 360]) { const p = await b.newPage({ viewport: { width: w, height: 860 } }); const errs = [], ext = [];
      p.on('pageerror', (e) => errs.push(e.message)); p.on('console', (m) => m.type() === 'error' && errs.push(m.text()));
      p.on('request', (r) => { const u = r.url(); if (!u.startsWith('data:') && !u.startsWith('file://')) ext.push(u.slice(0, 60)); });
      await p.goto('file://' + file, { waitUntil: 'load' }); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500);
      const sw = await p.evaluate(() => document.documentElement.scrollWidth);
      let extra = '';
      if (w === 1440) { const calc = await p.evaluate(() => { const i = document.getElementById('budget'); i.value = 500; i.dispatchEvent(new Event('input')); return document.getElementById('sv').textContent.replace(/\s+/g, ''); });
        await p.click('#py'); const y = await p.$eval('[data-y]', (e) => e.textContent); extra = ` calc=${calc} yearly=${y}`; }
      if (w === 390) { await p.click('.burger'); const o = await p.isVisible('#mnav'); await p.click('#mnav a[href="#pricing"]'); await p.waitForTimeout(150); extra = ` menu=${o && await p.isHidden('#mnav')}`; }
      res.push(`${w}:${sw === w ? 'ok' : 'SCROLL ' + sw}${extra}${errs.length ? ' ERR ' + errs.join(';').slice(0, 160) : ''}${ext.length ? ' EXT ' + ext.join(',') : ''}`);
      await p.close(); }
    console.log(path.basename(f), res.join(' | ')); }
  await b.close(); })();
