// Lays real screenshots out as phones with Telegram's own header, the way the mock-ups were shown.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const [dir, outFile, ...specs] = process.argv.slice(2);
const backs = JSON.parse(fs.readFileSync(path.join(dir, 'backs.json'), 'utf8'));
const LG = '<svg viewBox="0 0 76 52"><path fill="#fff" d="M17 0a3 3 0 0 1 3 3v11a2 2 0 0 0 2 2h10a3 3 0 0 1 3 3v11a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2V19a3 3 0 0 1 3-3h14a3 3 0 0 1 3 3v11a2 2 0 0 0 2 2h11a3 3 0 0 1 3 3v14a3 3 0 0 1-3 3H59a3 3 0 0 1-3-3V38a2 2 0 0 0-2-2h-3a2 2 0 0 0-2 2v11a3 3 0 0 1-3 3H32a3 3 0 0 1-3-3V38a2 2 0 0 0-2-2h-3a2 2 0 0 0-2 2v11a3 3 0 0 1-3 3H5a3 3 0 0 1-3-3V35a3 3 0 0 1 3-3h8a2 2 0 0 0 2-2v-8a2 2 0 0 0-2-2H3a3 3 0 0 1-3-3V3a3 3 0 0 1 3-3z"/></svg>';
const cols = specs.map((s, i) => {
  const [file, n, cap, sub] = s.split('|');
  const img = fs.readFileSync(path.join(dir, `${file}.png`)).toString('base64');
  const en = /-en$/.test(file);
  const left = backs[file] ? (en ? '‹ Back' : '‹ Назад') : en ? 'Close' : 'Закрыть';
  return `<div class="col"><div class="cap"><i>${n}</i>${cap}</div><div class="sub">${sub ?? ''}</div><div class="ph"><div class="st"><span>9:41</span><span><u></u></span></div><div class="th"><a>${left}</a><b><span class="logo">${LG}</span>ONEFLOW</b><span class="more"></span></div><img src="data:image/png;base64,${img}"></div></div>`;
});
const html = `<!doctype html><meta charset="utf-8"><style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#26272b;color:#f2f2f4;font:15px/1.35 -apple-system,"Inter","Segoe UI",Roboto,Arial,sans-serif;-webkit-font-smoothing:antialiased}
.board{display:inline-flex;gap:44px;padding:40px 44px 44px;background:#26272b}
.col{width:390px}
.cap{font-size:21px;font-weight:700;margin-bottom:6px;display:flex;align-items:center;gap:10px}
.cap i{font-style:normal;min-width:32px;height:32px;padding:0 6px;border-radius:16px;background:#fff;color:#000;display:grid;place-items:center;font-size:17px;font-weight:800}
.sub{color:#b3b4bb;font-size:15px;margin-bottom:16px;min-height:40px}
.ph{width:390px;height:800px;border-radius:44px;background:#000;overflow:hidden;box-shadow:0 0 0 9px #0b0b0d,0 0 0 11px #3a3b40,0 30px 70px rgba(0,0,0,.5);display:flex;flex-direction:column}
.ph img{display:block;width:390px;height:708px}
.st{height:44px;flex:none;display:flex;align-items:flex-end;justify-content:space-between;padding:0 30px 6px;font-size:15px;font-weight:600;background:#1c1c1e}
.st u{display:block;width:24px;height:11px;border-radius:3px;border:1.5px solid rgba(255,255,255,.5);position:relative}
.st u:after{content:"";position:absolute;inset:1.5px 5px 1.5px 1.5px;background:#fff;border-radius:1px}
.th{height:48px;flex:none;background:#1c1c1e;display:grid;grid-template-columns:1fr auto 1fr;align-items:center;padding:0 14px;border-bottom:1px solid rgba(255,255,255,.09)}
.th a{color:#3e88f7;font-size:16px}
.th b{font-size:16px;font-weight:600;display:flex;align-items:center;gap:7px}
.th .more{justify-self:end;width:30px;height:30px;border-radius:50%;background:rgba(255,255,255,.1);display:grid;place-items:center}
.th .more:before{content:"";width:3.5px;height:3.5px;border-radius:50%;background:#fff;box-shadow:-6.5px 0 #fff,6.5px 0 #fff}
.logo{width:22px;height:22px;border-radius:6px;background:#0e0e11;display:grid;place-items:center;border:1px solid rgba(255,255,255,.16)}
.logo svg{width:15px;height:15px}
</style><div class="board" id="board">${cols.join('')}</div>`;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1400, height: 1000 }, deviceScaleFactor: 2 });
  await p.setContent(html);
  await (await p.$('#board')).screenshot({ path: outFile });
  await b.close();
})();
