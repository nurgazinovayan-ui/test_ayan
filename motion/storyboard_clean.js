// node storyboard_clean.js [style …]  →  out/styles-clean/<style>/f<i>.jpg  (9 key frames per look, stitched by storyboard_clean.py)
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path'); const fs = require('fs');
const TS = [2.2, 4.4, 6.0, 12.3, 18.4, 23.6, 27.0, 31.8, 40.5];
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  for (const s of process.argv.slice(2)) {
    await p.goto('file://' + path.join(__dirname, 'oneflow-clean.html') + '?cap=1&s=' + s);
    await p.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map((i) => i.decode().catch(() => {}))); });
    await p.waitForTimeout(600);
    const dir = path.join(__dirname, 'out', 'styles-clean', s); fs.mkdirSync(dir, { recursive: true });
    for (let i = 0; i < TS.length; i++) { await p.evaluate((t) => window.seek(t), TS[i]); await p.screenshot({ path: path.join(dir, `f${i}.jpg`), type: 'jpeg', quality: 88 }); }
    console.log(s);
  }
  await b.close();
})();
