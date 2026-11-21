// Lays screenshots out side by side with captions, on one sheet.
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const [dir, outFile, title, ...specs] = process.argv.slice(2);
const cols = specs.map((s) => {
  const [file, n, cap, sub, width] = s.split('|');
  const img = fs.readFileSync(path.join(dir, `${file}.png`)).toString('base64');
  return `<div class="col" style="width:${width || 560}px"><div class="cap"><i>${n}</i>${cap}</div><div class="sub">${sub ?? ''}</div><img src="data:image/png;base64,${img}"></div>`;
});
const html = `<!doctype html><meta charset="utf-8"><style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#26272b;color:#f2f2f4;font:16px/1.4 -apple-system,"Inter","Segoe UI",Roboto,Arial,sans-serif;-webkit-font-smoothing:antialiased}
.sheet{display:inline-block;padding:36px 44px 44px;background:#26272b}
h1{font-size:26px;font-weight:750;margin-bottom:22px}
.board{display:flex;gap:40px;align-items:flex-start}
.cap{font-size:20px;font-weight:700;margin-bottom:6px;display:flex;align-items:center;gap:10px}
.cap i{font-style:normal;min-width:30px;height:30px;padding:0 6px;border-radius:15px;background:#fff;color:#000;display:grid;place-items:center;font-size:16px;font-weight:800}
.sub{color:#b3b4bb;font-size:15.5px;margin-bottom:14px;min-height:44px}
img{display:block;width:100%;border-radius:14px;box-shadow:0 0 0 1px rgba(255,255,255,.1),0 20px 50px rgba(0,0,0,.4)}
</style><div class="sheet" id="sheet"><h1>${title}</h1><div class="board">${cols.join('')}</div></div>`;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 2000, height: 1200 }, deviceScaleFactor: 2 });
  await p.setContent(html);
  await (await p.$('#sheet')).screenshot({ path: outFile });
  await b.close();
})();
