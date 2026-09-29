// node story.js <file.html> <outdir> t1 t2 …  → outdir/s<i>.jpg (frames for the storyboard)
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path'); const fs = require('fs');
const [file, dir, ...ts] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('file://' + path.resolve(file) + '?cap=1');
  await p.evaluate(async () => { await document.fonts.ready; });
  await p.waitForTimeout(500);
  fs.mkdirSync(dir, { recursive: true });
  for (let i = 0; i < ts.length; i++) { await p.evaluate((t) => window.seek(t), +ts[i]); await p.screenshot({ path: path.join(dir, `s${i}.jpg`), type: 'jpeg', quality: 88 }); }
  await b.close();
})();
