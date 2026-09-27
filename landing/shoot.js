// node shoot.js page.html out.png width ["extra css"] [waitMs] — full-page screenshot after fonts + reveal
const { chromium } = require('/opt/node22/lib/node_modules/playwright'); const path = require('path');
(async () => { const [f, out, w, extra, wait] = process.argv.slice(2);
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }); const p = await b.newPage({ viewport: { width: +w, height: 900 } });
  await p.goto('file://' + path.resolve(f), { waitUntil: 'load' }); await p.evaluate(() => document.fonts.ready);
  await p.evaluate(() => document.querySelectorAll('.rv').forEach((e) => e.classList.add('in'))); if (extra) await p.addStyleTag({ content: extra });
  await p.waitForTimeout(+(wait || 1600)); await p.screenshot({ path: out, fullPage: true }); await b.close(); })();
