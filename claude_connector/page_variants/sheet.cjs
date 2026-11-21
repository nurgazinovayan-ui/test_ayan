// One sheet per variant: the whole desktop page beside the whole phone page, with a title.
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const [dir, v, title, sub] = process.argv.slice(2);
const b64 = (f) => fs.readFileSync(path.join(dir, f)).toString('base64');
const html = `<!doctype html><meta charset="utf-8"><style>*{box-sizing:border-box;margin:0;padding:0}body{background:#26272b;color:#f2f2f4;font:16px/1.4 -apple-system,"Segoe UI",Roboto,Arial,sans-serif}
.sheet{display:inline-block;padding:34px 40px 44px}h1{font-size:28px;font-weight:750;margin-bottom:6px}p{color:#b3b4bb;font-size:17px;margin-bottom:24px;max-width:1100px}
.row{display:flex;gap:36px;align-items:flex-start}.d{width:1000px}.m{width:280px}.lab{font-size:15px;color:#b3b4bb;margin-bottom:10px}
img{display:block;width:100%;border-radius:12px;box-shadow:0 0 0 1px rgba(255,255,255,.1),0 24px 60px rgba(0,0,0,.45)}</style>
<div class="sheet" id="s"><h1>${title}</h1><p>${sub}</p><div class="row"><div class="d"><div class="lab">Компьютер</div><img src="data:image/png;base64,${b64(v + '-desk.png')}"></div><div class="m"><div class="lab">Телефон</div><img src="data:image/png;base64,${b64(v + '-phone.png')}"></div></div></div>`;
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1500, height: 1000 }, deviceScaleFactor: 1.5 }); await p.setContent(html); await p.waitForTimeout(300);
  await (await p.$('#s')).screenshot({ path: path.join(dir, `variant-${v}.jpg`), type: 'jpeg', quality: 88 }); await b.close(); })();
