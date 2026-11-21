const { chromium } = require('playwright'); const path = require('path');
const dir = process.argv[2];
(async () => {
  const b = await chromium.launch(); const notes = [];
  for (const v of (process.argv[3] || 'a,b,c').split(',')) for (const [name, w, h, scale] of [['desk', 1440, 900, 1], ['phone', 390, 844, 2]]) {
    const ctx = await b.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: scale }); const p = await ctx.newPage();
    await p.goto('file://' + path.join(dir, v + '.html')); await p.waitForTimeout(700);
    const wide = await p.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    const small = await p.evaluate(() => [...document.querySelectorAll('main *, header *, footer *')].filter((e) => e.children.length === 0 && e.textContent.trim() && parseFloat(getComputedStyle(e).fontSize) < 16).map((e) => e.textContent.trim().slice(0, 20)).slice(0, 4));
    const clipped = await p.evaluate(() => [...document.querySelectorAll('main h1, main h2, main h3, main p, main q, main code, main .btn')].filter((e) => { const r = e.getBoundingClientRect(); return r.right > window.innerWidth + 1 || r.left < -1; }).map((e) => e.textContent.trim().slice(0, 24)).slice(0, 4));
    if (wide > 0 || small.length || clipped.length) notes.push(`${v} ${name}: wide ${wide}, small ${JSON.stringify(small)}, clipped ${JSON.stringify(clipped)}`);
    await p.screenshot({ path: path.join(dir, `${v}-${name}.png`), fullPage: true });
    if (name === 'desk') await p.screenshot({ path: path.join(dir, `${v}-top.png`) });
    await ctx.close();
  }
  await b.close(); console.log(notes.length ? notes.join('\n') : 'no layout problems');
})();
