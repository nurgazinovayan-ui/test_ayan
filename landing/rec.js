// node rec.js page.html out.webm seconds ["x,y,x,y..." mouse path] — 1280×800 hero video
const { chromium } = require('/opt/node22/lib/node_modules/playwright'); const path = require('path'); const fs = require('fs');
(async () => { const [f, out, secs, moves] = process.argv.slice(2); const dir = path.resolve('shots', 'vid-' + Date.now());
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const c = await b.newContext({ viewport: { width: 1280, height: 800 }, recordVideo: { dir, size: { width: 1280, height: 800 } } }); const p = await c.newPage();
  await p.goto('file://' + path.resolve(f)); const pts = (moves || '').split(',').filter(Boolean).map(Number); const t0 = Date.now();
  while (Date.now() - t0 < +secs * 1000) { if (pts.length >= 2) { for (let i = 0; i < pts.length; i += 2) await p.mouse.move(pts[i], pts[i + 1], { steps: 25 }); } else await p.waitForTimeout(250); }
  const v = p.video(); await c.close(); fs.copyFileSync(await v.path(), path.resolve(out)); await b.close(); console.log(out); })();
