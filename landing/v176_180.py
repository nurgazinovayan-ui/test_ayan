"""Variants 176–180 — unusual concepts on the business message (all grotesk).

176 Terminal (market terminal: ticker, cost chart, cabinet status table) · 177 Label (nutrition-facts label: «Состав: только экономия»)
178 Riso (two-colour risograph overprint) · 179 Extrude (3D extruded type that tilts with the cursor) · 180 Price tag (supermarket shelf tag)
"""
from core import T, SUB, ACTS, CABS, cr, page

# ============================================================ 176 · TERMINAL
A_TOK = T('#0b0a07', '#efe6cf', '#ffb000', card='#12100b', muted='#8c8168', line='#2a2417', line2='#463c24', btn='#ffb000', btn_ink='#0b0a07', ac_ink='#0b0a07',
          d="'IBM Plex Mono',monospace", f="'IBM Plex Sans',sans-serif", m="'IBM Plex Mono',monospace", dw='600', dl='-.035em', r='0px', br='0px')
A_CSS = """
.nav { background: #0b0a07; } .logo b { padding: 2px 6px; background: var(--ac); color: #0b0a07; }
.tick { overflow: hidden; border-bottom: 1px solid var(--line2); background: #100e09; font: 500 13px var(--m); white-space: nowrap; }
.tick .t { display: flex; gap: 38px; width: max-content; padding: 9px 0; animation: mq 55s linear infinite; } .tick b { color: var(--ac); font-weight: 600; } .tick .u { color: #52d98b; font-style: normal; }
.term { display: grid; grid-template-columns: minmax(0, 1.12fr) minmax(0, .88fr); gap: 14px; margin-top: 26px; }
.pan { border: 1px solid var(--line2); background: var(--card); min-width: 0; }
.pan .hd { display: flex; justify-content: space-between; gap: 10px; padding: 7px 12px; background: var(--ac); color: #0b0a07; font: 600 12px var(--m); letter-spacing: .06em; text-transform: uppercase; }
.pan .bd { padding: 30px; }
.prompt { font: 500 13.5px var(--m); color: var(--muted); } .prompt b { color: var(--ac); font-weight: 600; }
.cur { display: inline-block; width: .6em; height: 1.1em; margin-left: 4px; background: var(--ac); vertical-align: -.2em; animation: bl 1s steps(1) infinite; } @keyframes bl { 50% { opacity: 0; } }
.term h1 { margin-top: 20px; font: 600 clamp(36px, 4.6vw, 68px)/1.02 var(--d); letter-spacing: -.045em; } .term h1 span { color: var(--ac); }
.term .sub { margin-top: 22px; max-width: 560px; font-size: 17px; }
.fk { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 26px; } .fk span { padding: 5px 8px; background: #1b180f; border: 1px solid var(--line2); font: 500 11.5px var(--m); color: var(--muted); } .fk b { color: var(--ac); }
#chart { display: block; width: 100%; height: 220px; cursor: crosshair; }
.leg { display: flex; flex-wrap: wrap; gap: 16px; padding: 0 16px 10px; font: 500 11.5px var(--m); color: var(--muted); } .leg i { display: inline-block; width: 14px; height: 3px; margin-right: 6px; vertical-align: middle; }
.rdo { display: flex; justify-content: space-between; gap: 10px; padding: 10px 16px; border-top: 1px solid var(--line); font: 500 12px var(--m); color: var(--muted); } .rdo b { color: var(--ink); font-weight: 600; } .rdo .a b { color: var(--ac); }
.tbl { width: 100%; border-collapse: collapse; font: 500 12.5px var(--m); } .tbl th { padding: 8px 16px; border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); color: var(--muted); font-weight: 500; text-align: left; }
.tbl td { padding: 7px 16px; border-bottom: 1px solid var(--line); } .tbl td:last-child { text-align: right; } .tbl .st { color: var(--muted); white-space: nowrap; } .tbl .st.ok { color: #52d98b; }
.card { box-shadow: none; border: 1px solid var(--line2); } .sh .k::before { content: '<'; } .sh .k::after { content: '> GO'; color: var(--muted); }
.big { font-family: var(--m); } .tab.on { background: var(--ac); color: #0b0a07; } .plan.hot { box-shadow: inset 0 0 0 1px var(--ac); border-color: var(--ac); }
.eyebrow { border-radius: 0; } .per div, .per button { border-radius: 0; } .cr { border-radius: 0; }
@media (max-width: 1000px) { .term { grid-template-columns: minmax(0, 1fr); } .pan .bd { padding: 22px; } }
"""
TK = [('KASPI', '1125×330', 'ГОТОВО'), ('ЯНДЕКС РСЯ', '1080×450', 'ГОТОВО'), ('GOOGLE', '1200×628', 'ГОТОВО'), ('ГЕНЕРАЦИЯ', '−50%*', 'ДЕШЕВЛЕ'),
      ('БЮДЖЕТ', 'НЕ СГОРАЕТ', '+ОСТАТОК'), ('GDN', '300×600', 'ГОТОВО'), ('BYYD', '300×250', 'ГОТОВО'), ('STORIES', '1080×1920', 'ГОТОВО'), ('МОДЕЛИ', '30+', 'ОДИН СЧЁТ')]
tk = ''.join(f'<span><b>{a}</b> {b} <i class="u">▲ {c}</i></span>' for a, b, c in TK)
rows = ''.join(f'<tr><td>{n.upper()}</td><td>{w}×{h}</td><td class="st" data-i="{i}">··· ОЧЕРЕДЬ</td></tr>' for i, (n, w, h) in enumerate(CABS))
A_HERO = f'''<section class="hero"><div class="tick" aria-hidden="true"><div class="t">{tk}{tk}</div></div><div class="wrap"><div class="term">
<div class="pan"><div class="hd"><span>ONEFLOW &lt;GO&gt;</span><span>креативы · все кабинеты</span></div><div class="bd">
<p class="prompt">&gt; <b>oneflow</b> adapt --cabinets all<span class="cur"></span></p><h1>Рынок рекламы.<br>Ваша цена — <span>до&nbsp;−50%*</span></h1><p class="sub">{SUB}</p>{ACTS}
<div class="fk" aria-hidden="true"><span><b>F1</b> ФОТО</span><span><b>F2</b> АССИСТЕНТ</span><span><b>F3</b> ЗАПУСК</span><span><b>F4</b> 6 КАБИНЕТОВ</span></div></div></div>
<div class="pan"><div class="hd"><span>CHRT · стоимость 12 мес</span><span>пример</span></div><canvas id="chart" role="img" aria-label="График: у ONEFLOW стоимость креативов до 50% ниже, чем в отдельных сервисах — пример"></canvas>
<div class="leg"><span><i style="background:#8c8168"></i>ОТДЕЛЬНЫЕ СЕРВИСЫ</span><span><i style="background:#ffb000"></i>ONEFLOW</span></div>
<div class="rdo" id="rdo"><span>МЕС <b>—</b></span><span>СЕРВИСЫ <b>—</b></span><span class="a">ONEFLOW <b>—</b></span></div>
<table class="tbl" aria-label="Статус адаптации по кабинетам — пример"><thead><tr><th>КАБИНЕТ</th><th>ФОРМАТ</th><th>СТАТУС</th></tr></thead><tbody>{rows}</tbody></table></div>
</div>{{LOGOS}}</div></section>'''
A_JS = '''<script>
(function () {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches, cv = document.getElementById('chart'); if (!cv) return;
  const M = ['ЯНВ', 'ФЕВ', 'МАР', 'АПР', 'МАЙ', 'ИЮН', 'ИЮЛ', 'АВГ', 'СЕН', 'ОКТ', 'НОЯ', 'ДЕК'];
  const S = [304, 296, 312, 300, 318, 306, 298, 314, 320, 308, 302, 316], O = S.map((v, i) => Math.round(v * (.52 - (i % 3) * .01)));
  const x = cv.getContext('2d'); let W, H, prog = reduce ? 1 : 0, hover = -1, t0 = performance.now(), auto = !reduce;
  const size = () => { const r = devicePixelRatio || 1; W = cv.clientWidth; H = cv.clientHeight; cv.width = W * r; cv.height = H * r; x.setTransform(r, 0, 0, r, 0, 0); };
  const X = (i) => 34 + i * (W - 50) / 11, Y = (v) => H - 26 - (v / 360) * (H - 44);
  const line = (arr, col, w, n) => { x.strokeStyle = col; x.lineWidth = w; x.beginPath(); for (let i = 0; i <= n; i++) { const k = Math.min(1, n - i + 1); i ? x.lineTo(X(i), Y(arr[i])) : x.moveTo(X(i), Y(arr[i])); } x.stroke(); };
  const draw = () => { x.clearRect(0, 0, W, H); x.font = '500 10px IBM Plex Mono'; x.fillStyle = '#8c8168';
    for (let v = 0; v <= 300; v += 100) { x.strokeStyle = '#2a2417'; x.lineWidth = 1; x.setLineDash([3, 4]); x.beginPath(); x.moveTo(30, Y(v)); x.lineTo(W - 10, Y(v)); x.stroke(); x.setLineDash([]); x.fillText('$' + v, 0, Y(v) + 3); }
    M.forEach((m, i) => { if (i % 2 === 0) x.fillText(m, X(i) - 9, H - 8); });
    const n = Math.max(1, Math.floor(prog * 11)); line(S, '#8c8168', 2, n); line(O, '#ffb000', 2.5, n);
    x.fillStyle = 'rgba(255,176,0,.08)'; x.beginPath(); x.moveTo(X(0), Y(S[0])); for (let i = 0; i <= n; i++) x.lineTo(X(i), Y(S[i])); for (let i = n; i >= 0; i--) x.lineTo(X(i), Y(O[i])); x.fill();
    if (hover >= 0) { x.strokeStyle = '#efe6cf'; x.lineWidth = 1; x.beginPath(); x.moveTo(X(hover), 10); x.lineTo(X(hover), H - 22); x.stroke();
      [[S, '#8c8168'], [O, '#ffb000']].forEach(([a, c]) => { x.fillStyle = c; x.beginPath(); x.arc(X(hover), Y(a[hover]), 4, 0, 7); x.fill(); });
      const b = document.querySelectorAll('#rdo b'); b[0].textContent = M[hover]; b[1].textContent = '$' + S[hover]; b[2].textContent = '$' + O[hover] + ' (−' + Math.round(100 - O[hover] / S[hover] * 100) + '%)'; } };
  const tick = (t) => { if (prog < 1) prog = Math.min(1, (t - t0) / 1400); if (auto) hover = Math.floor(((t - t0) / 900) % 12); draw(); requestAnimationFrame(tick); };
  cv.addEventListener('pointermove', (e) => { auto = false; const r = cv.getBoundingClientRect(); hover = Math.max(0, Math.min(11, Math.round((e.clientX - r.left - 34) / ((W - 50) / 11)))); });
  size(); addEventListener('resize', size); if (reduce) { hover = 8; draw(); } else requestAnimationFrame(tick);
  const st = [...document.querySelectorAll('.tbl .st')]; let k = 0;
  const step = () => { if (k === st.length) { st.forEach((s) => { s.textContent = '··· ОЧЕРЕДЬ'; s.classList.remove('ok'); }); k = 0; return setTimeout(step, 900); }
    st[k].textContent = '✓ ГОТОВО'; st[k].classList.add('ok'); k++; setTimeout(step, k === st.length ? 2600 : 420); };
  if (reduce) st.forEach((s) => { s.textContent = '✓ ГОТОВО'; s.classList.add('ok'); }); else setTimeout(step, 700);
})();
</script>
'''
page('v176-terminal.html', 'ONEFLOW — ваша цена на рекламу до −50%', A_TOK, A_CSS, '<b>OF</b>ONEFLOW', A_HERO,
     'Ваша цена —<br><span class="gt">до −50%*</span>', stage_prod=1, js=A_JS, theme='#0b0a07')

# ============================================================ 177 · LABEL (nutrition facts)
B_TOK = T('#ffffff', '#0a0a0a', '#e10600', card='#ffffff', line='#0a0a0a', line2='#0a0a0a', ac_ink='#ffffff',
          d="'Inter',sans-serif", f="'Inter',sans-serif", m="'JetBrains Mono',monospace", dw='800', dl='-.05em', r='0px', br='0px')
B_CSS = """
.nav { border-bottom: 3px solid #000; background: #fff; }
.lh { display: grid; grid-template-columns: minmax(0, 1.05fr) minmax(0, .95fr); gap: 50px; align-items: center; padding: 60px 0 10px; }
.lh .ey { font: 600 13px var(--m); text-transform: uppercase; letter-spacing: .08em; } .lh .ey b { background: #000; color: #fff; padding: 3px 7px; margin-right: 8px; }
.lh h1 { margin-top: 22px; font: 800 clamp(60px, 8.4vw, 132px)/.86 var(--d); letter-spacing: -.06em; } .lh h1 em { font-style: normal; color: var(--ac); }
.lh .sub { margin-top: 28px; max-width: 520px; color: #222; }
.box { position: relative; justify-self: center; width: min(420px, 100%); rotate: -2deg; }
.box::before { content: ''; position: absolute; inset: 18px -18px -18px 18px; background: var(--ac); }
.lbl { position: relative; padding: 10px 12px 12px; background: #fff; border: 2.5px solid #000; font-family: 'Inter', sans-serif; color: #000; box-shadow: 0 40px 60px -30px rgba(0,0,0,.4); }
.lbl .nf { font: 800 40px/1 'Inter', sans-serif; letter-spacing: -.035em; } .lbl .sv { font-size: 15px; line-height: 1.35; } .lbl .sv b { font-weight: 800; }
.lbl .b10 { height: 12px; margin: 6px 0; background: #000; } .lbl .b5 { height: 6px; margin: 5px 0; background: #000; }
.lbl .cal { display: flex; justify-content: space-between; align-items: flex-end; gap: 12px; } .lbl .cal small { display: block; font-size: 12px; font-weight: 700; }
.lbl .cal b { display: block; font: 800 20px/1.05 'Inter', sans-serif; letter-spacing: -.02em; } .lbl .cal em { font: 800 36px/.9 'Inter', sans-serif; font-style: normal; letter-spacing: -.04em; text-align: right; color: var(--ac); }
.lbl .dv { text-align: right; font-size: 12px; font-weight: 800; padding-bottom: 3px; border-bottom: 1px solid #000; }
.lbl .r { display: flex; justify-content: space-between; gap: 10px; padding: 4px 0; border-bottom: 1px solid #000; font-size: 15px; opacity: 0; animation: rin .35s forwards; }
.lbl .r b { font-weight: 800; } .lbl .r em { font-style: normal; font-weight: 800; } .lbl .r.i { padding-left: 16px; font-size: 14px; }
.lbl .vit { display: grid; grid-template-columns: 1fr 1fr; column-gap: 14px; } .lbl .vit .r { font-size: 13.5px; }
.lbl .fine { margin-top: 6px; font-size: 11px; line-height: 1.35; } .lbl .bc { height: 34px; margin-top: 8px; background: repeating-linear-gradient(90deg, #000 0 2px, #fff 2px 3px, #000 3px 6px, #fff 6px 8px, #000 8px 9px, #fff 9px 12px); }
@keyframes rin { to { opacity: 1; } }
.sh .k { display: inline-block; padding: 3px 8px; background: #000; color: #fff; } .sh h2 { letter-spacing: -.055em; }
.card { box-shadow: none; border: 2px solid #000; } .big { color: #000; } .bento .b1 .big, .bento .b2 .big { color: var(--ac); } .bars .y { background: var(--ac); } .bars .n { background: #000; }
.tab { border-radius: 0; } .tab.on { background: #000; } .row b { font-weight: 800; } .plan .pr { font-weight: 800; } .plan.hot { box-shadow: none; border: 4px solid #000; } .pop { border-radius: 0; background: var(--ac); }
.end { border-top: 12px solid #000; } .eyebrow { border-radius: 0; }
@media (max-width: 960px) { .lh { grid-template-columns: minmax(0, 1fr); gap: 60px; } .box { rotate: -1deg; } }
@media (max-width: 460px) { .box::before { inset: 10px -8px -10px 8px; } .lbl .nf { font-size: 32px; } .lbl .cal em { font-size: 28px; } .lbl .vit { grid-template-columns: minmax(0, 1fr); } }
"""
RW = [('Генерация', 'до −50%*'), ('Нейросети', '30+'), ('Модули', '9'), ('Кликов до запуска', '2')]
rw = ''.join(f'<div class="r" style="animation-delay:{.5 + i * .12:.2f}s"><span><b>{a}</b></span><em>{b}</em></div>' for i, (a, b) in enumerate(RW))
vit = ''.join(f'<div class="r" style="animation-delay:{1 + i * .09:.2f}s"><span>{n} {w}×{h}</span><em>100%</em></div>' for i, (n, w, h) in enumerate(CABS))
B_HERO = f'''<section class="hero"><div class="wrap"><div class="lh"><div><p class="ey"><b>ONEFLOW</b>креативы для рекламных кабинетов</p><h1>Состав:<br>только<br><em>экономия.</em></h1><p class="sub">{SUB}</p>{ACTS}</div>
<div class="box"><div class="lbl" role="img" aria-label="Этикетка ONEFLOW: генерация до −50%, бюджет не сгорает в конце месяца, 30+ нейросетей, 9 модулей, 2 клика, 6 рекламных кабинетов">
<div class="nf">Ценность для бизнеса</div><p class="sv">Порция: <b>1 кампания</b></p><p class="sv">Кабинетов в упаковке: <b>6</b></p><div class="b10"></div>
<div class="cal"><span><small>В конце месяца</small><b>Бюджет</b></span><em>не сгорает</em></div><div class="b5"></div><p class="dv">% выгоды*</p>{rw}<div class="b10"></div>
<div class="vit">{vit}</div><div class="b5"></div><p class="fine">* До 50% — в сравнении с оплатой тех же моделей в отдельных сервисах; итог зависит от моделей и объёма. Не содержит: подписок на каждый сервис и сгоревших остатков.</p><div class="bc"></div></div></div>
</div>{{LOGOS}}</div></section>'''
page('v177-label.html', 'ONEFLOW — состав: только экономия', B_TOK, B_CSS, '<span style="width:18px;height:18px;background:#000;box-shadow:inset 0 -6px 0 #e10600"></span>ONEFLOW', B_HERO,
     'Состав:<br><span class="gt">только экономия.</span>', stage_prod=4, theme='#ffffff')

# ============================================================ 178 · RISO (two-colour overprint)
C_TOK = T('#f3eee2', '#1d2a86', '#ff48a5', card='#eee7d8', ink2='#2d3470', muted='#6a6f96', line='rgba(29,42,134,.2)', line2='rgba(29,42,134,.4)', btn='#1d2a86', btn_ink='#f3eee2', ac_ink='#1d2a86',
          d="'Montserrat',sans-serif", f="'Onest',sans-serif", m="'IBM Plex Mono',monospace", dw='900', dl='-.03em', r='4px', br='99px')
NOISE = "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='220' height='220'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 .55 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E\")"
C_CSS = """
.hero { position: relative; overflow: hidden; padding: 56px 0 20px; } .hero::after, .end::after { content: ''; position: absolute; inset: 0; pointer-events: none; background: NOISE; opacity: .32; mix-blend-mode: multiply; }
.rg { position: relative; z-index: 1; display: grid; grid-template-columns: minmax(0, 1.15fr) minmax(0, .85fr); gap: 30px; align-items: center; }
.ov { position: relative; display: grid; margin-top: 18px; } .ov span { grid-area: 1 / 1; font: 900 clamp(54px, 8.6vw, 142px)/.84 var(--d); letter-spacing: -.035em; text-transform: uppercase; mix-blend-mode: multiply; }
.ov .l1 { color: #ff48a5; } .ov .l2 { color: #0078bf; transform: translate(var(--mx, 6px), var(--my, 4px)); transition: transform .5s cubic-bezier(.2,.8,.2,1); }
.rg .sub { margin-top: 28px; max-width: 540px; }
.comp { position: relative; height: 560px; } .dot { position: absolute; border-radius: 50%; mix-blend-mode: multiply; }
.dot.a { width: 380px; height: 380px; right: -20px; top: 10px; background: radial-gradient(#ff48a5 42%, transparent 44%) 0 0 / 11px 11px; }
.dot.b { width: 190px; height: 190px; left: 0; bottom: 20px; background: #0078bf; opacity: .9; }
.sq { position: absolute; left: 70px; top: 70px; width: 250px; height: 330px; background: #ffe800; mix-blend-mode: multiply; rotate: -6deg; }
.comp .cr { position: absolute; left: 110px; top: 90px; rotate: 4deg; filter: grayscale(1) contrast(1.25) brightness(1.05); mix-blend-mode: multiply; }
.stamp { position: absolute; right: 20px; bottom: 60px; display: grid; place-items: center; width: 150px; height: 150px; border: 4px solid #1d2a86; border-radius: 50%; rotate: 14deg; font: 900 22px/1 var(--d); text-align: center; text-transform: uppercase; color: #1d2a86; mix-blend-mode: multiply; }
.sh h2, .end h2 { text-shadow: 4px 3px 0 rgba(255,72,165,.75); } .sh h2 .gt { color: #0078bf; } .sh .k { color: #ff48a5; } .big { color: #ff48a5; text-shadow: 3px 2px 0 rgba(0,120,191,.6); }
.card { box-shadow: inset 0 0 0 2px var(--line2); } .bars .y { background: #ff48a5; } .bars .n { background: rgba(0,120,191,.35); } .tab.on { background: #1d2a86; }
.end { position: relative; overflow: hidden; background: #ff48a5; color: #1d2a86; border: 0; } .end h2 { text-shadow: 5px 4px 0 rgba(0,120,191,.7); } .end p { color: #1d2a86; } .end .gt { color: #1d2a86; }
@media (max-width: 960px) { .rg { grid-template-columns: minmax(0, 1fr); } .comp { height: 480px; max-width: 460px; } }
@media (max-width: 460px) { .comp { height: 430px; } .dot.a { width: 280px; height: 280px; } .sq { left: 30px; } .comp .cr { left: 60px; } .stamp { width: 118px; height: 118px; font-size: 17px; right: 0; } }
""".replace('NOISE', NOISE)
C_HERO = f'''<section class="hero"><div class="wrap"><div class="rg"><div><a class="eyebrow" href="#why"><b>ONEFLOW</b>все рекламные кабинеты</a>
<h1 class="ov" id="ov" aria-label="Реклама. До 50% дешевле*"><span class="l1" aria-hidden="true">Реклама.<br>До&nbsp;50%<br>дешевле*</span><span class="l2" aria-hidden="true">Реклама.<br>До&nbsp;50%<br>дешевле*</span></h1>
<p class="sub">{SUB}</p>{ACTS}</div>
<div class="comp" aria-hidden="true"><span class="dot a"></span><span class="sq"></span>{cr(0, 230, 360)}<span class="dot b"></span><span class="stamp">два<br>клика</span></div></div>{{LOGOS}}</div></section>'''
C_JS = '''<script>
(function () { const ov = document.getElementById('ov'); if (!ov || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  addEventListener('pointermove', (e) => { const x = (e.clientX / innerWidth - .5) * 16, y = (e.clientY / innerHeight - .5) * 12; ov.style.setProperty('--mx', x.toFixed(1) + 'px'); ov.style.setProperty('--my', y.toFixed(1) + 'px'); }); })();
</script>
'''
page('v178-riso.html', 'ONEFLOW — реклама до 50% дешевле', C_TOK, C_CSS, '<span style="width:20px;height:20px;border-radius:50%;background:#ff48a5;box-shadow:6px 3px 0 -2px #0078bf"></span>ONEFLOW',
     C_HERO, 'Реклама.<br><span class="gt">До 50% дешевле*</span>', stage_prod=3, js=C_JS, theme='#f3eee2')

# ============================================================ 179 · EXTRUDE (3D type)
D_TOK = T('#fff4e6', '#1a0a04', '#ff4d1c', card='#fff9f1', ac_ink='#fff4e6', d="'Unbounded',sans-serif", f="'Onest',sans-serif", m="'JetBrains Mono',monospace", dw='900', dl='-.03em', r='22px', br='99px')
ext = ', '.join(f'{i}px {i}px 0 {c}' for i, c in enumerate(['#ff6a3d', '#f25a2c', '#e44c20', '#d64016', '#c7360f', '#b62e0b', '#a42708', '#912106', '#7e1b05', '#6c1604', '#5b1203', '#4b0e02', '#3d0b02', '#310902'], 1)) + ', 18px 26px 40px rgba(60,10,0,.45)'
D_CSS = """
.nav { background: #ff4d1c; border-bottom: 0; color: #fff4e6; } .nav nav a, .nav .lg { color: rgba(255,244,230,.8); } .nav nav a:hover, .nav .lg:hover { color: #fff; }
.nav .btn.p { background: #fff4e6; color: #1a0a04; } .burger { color: #fff4e6; }
.hero { position: relative; overflow: hidden; padding: 70px 0 30px; background: #ff4d1c; color: #fff4e6; text-align: center; }
.stg { perspective: 1100px; margin-top: 26px; }
.x3d { display: inline-block; font: 900 clamp(46px, 10vw, 164px)/.9 var(--d); letter-spacing: -.02em; text-transform: uppercase; color: #fff4e6; text-shadow: EXT;
  transform: rotateX(var(--rx, 14deg)) rotateY(var(--ry, -10deg)); transition: transform .6s cubic-bezier(.2,.8,.2,1); }
.hero .eyebrow { box-shadow: inset 0 0 0 1.5px rgba(255,244,230,.6); color: #fff4e6; } .hero .eyebrow b { background: #fff4e6; color: #ff4d1c; }
.hero .sub { max-width: 620px; margin: 34px auto 0; color: #fff4e6; } .hero .acts { justify-content: center; } .hero .tiny { color: rgba(255,244,230,.75); }
.hero .btn.p { background: #fff4e6; color: #1a0a04; } .hero .btn.s { color: #fff4e6; box-shadow: inset 0 0 0 1.5px rgba(255,244,230,.7); }
.chips { display: flex; flex-wrap: wrap; justify-content: center; gap: 12px; margin-top: 42px; }
.chips span { padding: 12px 18px; border-radius: 14px; background: #fff4e6; color: #1a0a04; font: 800 14px var(--d); box-shadow: 0 1px 0 #d64016, 0 2px 0 #c7360f, 0 3px 0 #b62e0b, 0 4px 0 #a42708, 0 5px 0 #912106, 0 6px 0 #7e1b05, 0 14px 22px rgba(60,10,0,.35); animation: bob 3.2s ease-in-out infinite; }
.chips small { margin-left: 8px; font: 500 11.5px var(--m); color: #8a5a44; } @keyframes bob { 50% { transform: translateY(-6px); } }
.hero .logos p, .hero .mq span { color: rgba(255,244,230,.75); }
.big { text-shadow: 1px 1px 0 #d64016, 2px 2px 0 #b62e0b, 3px 3px 0 #912106, 4px 4px 0 #6c1604; color: #ff6a3d; }
.card { box-shadow: inset 0 0 0 1.5px var(--line), 0 6px 0 #f1dcc6; } .tab.on { background: #ff4d1c; color: #fff4e6; }
.end { background: #ff4d1c; color: #fff4e6; border: 0; } .end h2 { text-shadow: 2px 2px 0 #c7360f, 4px 4px 0 #a42708, 6px 6px 0 #7e1b05, 8px 8px 0 #5b1203; } .end .gt { color: #fff4e6; } .end p { color: #fff4e6; }
.end .btn.p { background: #fff4e6; color: #1a0a04; } .end .btn.s { color: #fff4e6; box-shadow: inset 0 0 0 1.5px rgba(255,244,230,.7); }
@media (max-width: 640px) { .x3d { text-shadow: 1px 1px 0 #f25a2c, 2px 2px 0 #d64016, 3px 3px 0 #b62e0b, 4px 4px 0 #912106, 5px 5px 0 #6c1604, 6px 6px 0 #4b0e02, 10px 14px 22px rgba(60,10,0,.4); } .chips span { padding: 10px 14px; font-size: 13px; } }
""".replace('EXT', ext)
chips = ''.join(f'<span style="animation-delay:{i * .25:.2f}s">{n}<small>{w}×{h}</small></span>' for i, (n, w, h) in enumerate(CABS))
D_HERO = f'''<section class="hero"><div class="wrap"><a class="eyebrow" href="#sizes"><b>1 запуск</b>6 рекламных кабинетов</a><div class="stg"><h1 class="x3d" id="x3d">Все<br>кабинеты.<br>Сразу.</h1></div>
<p class="sub">{SUB}</p>{ACTS}<div class="chips" aria-label="Кабинеты: Kaspi, Яндекс РСЯ, Google Discovery, GDN, BYYD, Stories">{chips}</div>{{LOGOS}}</div></section>'''
D_JS = '''<script>
(function () { const h = document.getElementById('x3d'); if (!h || matchMedia('(prefers-reduced-motion: reduce)').matches) return; let idle = true, t0 = performance.now();
  addEventListener('pointermove', (e) => { idle = false; h.style.setProperty('--ry', ((e.clientX / innerWidth - .5) * 34).toFixed(1) + 'deg'); h.style.setProperty('--rx', (18 - (e.clientY / innerHeight) * 26).toFixed(1) + 'deg'); });
  const loop = (t) => { if (idle) { const k = (t - t0) / 1000; h.style.setProperty('--ry', (Math.sin(k * .8) * 14).toFixed(1) + 'deg'); h.style.setProperty('--rx', (10 + Math.cos(k * .6) * 5).toFixed(1) + 'deg'); } requestAnimationFrame(loop); };
  requestAnimationFrame(loop); })();
</script>
'''
page('v179-extrude.html', 'ONEFLOW — все кабинеты сразу', D_TOK, D_CSS, '<span style="width:18px;height:18px;border-radius:5px;background:#fff4e6;box-shadow:2px 2px 0 #b62e0b,4px 4px 0 #7e1b05"></span>ONEFLOW',
     D_HERO, 'Все кабинеты.<br><span class="gt">Сразу.</span>', stage_prod=2, js=D_JS, theme='#ff4d1c')

# ============================================================ 180 · PRICE TAG
E_TOK = T('#f3f0e8', '#111111', '#e30613', card='#ffffff', ac_ink='#ffffff', d="'Inter Tight',sans-serif", f="'Inter',sans-serif", m="'JetBrains Mono',monospace", dw='800', dl='-.045em', r='10px', br='8px')
E_CSS = """
.ph { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 40px; align-items: center; padding: 50px 0 10px; }
.ph h1 { margin-top: 22px; font: 800 clamp(48px, 6.6vw, 104px)/.92 var(--d); letter-spacing: -.055em; } .ph h1 span { position: relative; color: var(--ac); white-space: nowrap; }
.ph h1 span::after { content: ''; position: absolute; left: -2%; right: -2%; bottom: .08em; height: .12em; background: #ffe600; z-index: -1; transform: skewX(-12deg); }
.ph .sub { margin-top: 26px; max-width: 520px; }
.tw { position: relative; justify-self: center; width: min(460px, 100%); padding-top: 70px; }
.tw .pin { position: absolute; left: 50%; top: 0; width: 18px; height: 18px; margin-left: -9px; border-radius: 50%; background: radial-gradient(circle at 35% 35%, #fff, #9a9a9a); box-shadow: 0 2px 4px rgba(0,0,0,.3); }
.tag { position: relative; padding: 34px 30px 26px; border-radius: 16px; background: #ffe600; color: #111; transform-origin: 50% -60px; animation: sway 5s ease-in-out infinite; box-shadow: 0 40px 60px -30px rgba(80,60,0,.55); }
.tag::before { content: ''; position: absolute; left: 50%; top: -62px; width: 2px; height: 70px; background: #555; transform: translateX(-50%); }
.tag .hole { position: absolute; left: 50%; top: 10px; width: 16px; height: 16px; margin-left: -8px; border-radius: 50%; background: #f3f0e8; box-shadow: inset 0 2px 3px rgba(0,0,0,.35); }
@keyframes sway { 0%, 100% { rotate: -2.5deg; } 50% { rotate: 2deg; } }
.tg-top { padding: 0 64px 12px 0; border-bottom: 2px dashed rgba(0,0,0,.35); } .tg-top b { display: block; font: 800 20px/1.15 var(--d); letter-spacing: -.02em; } .tg-top span { font: 500 12px var(--m); color: #444; }
.tg-mid { display: flex; align-items: flex-end; justify-content: space-between; gap: 16px; padding: 16px 0 8px; }
.tg-mid small { display: block; font: 700 12px var(--m); text-transform: uppercase; letter-spacing: .08em; color: #444; }
.tg-mid s { font: 800 48px/1 'Sofia Sans Extra Condensed', sans-serif; color: #555; text-decoration-color: var(--ac); text-decoration-thickness: 5px; }
.tg-mid .nw { text-align: right; } .tg-mid .nw b { font: 900 clamp(96px, 11vw, 150px)/.8 'Sofia Sans Extra Condensed', sans-serif; letter-spacing: -.01em; } .tg-mid .nw i { font-style: normal; font: 800 22px 'Sofia Sans Extra Condensed', sans-serif; vertical-align: top; }
.tg-mid .nw em { margin-right: 6px; font: 800 30px 'Sofia Sans Extra Condensed', sans-serif; font-style: normal; }
.tg-bot { display: flex; justify-content: space-between; align-items: flex-end; gap: 14px; padding-top: 12px; border-top: 2px dashed rgba(0,0,0,.35); }
.tg-bot span { font: 700 14px/1.25 var(--f); } .tg-bot .bc { width: 120px; height: 40px; background: repeating-linear-gradient(90deg, #111 0 2px, transparent 2px 3px, #111 3px 6px, transparent 6px 8px, #111 8px 9px, transparent 9px 12px); }
.rib { position: absolute; top: 18px; right: -8px; padding: 6px 14px; background: var(--ac); color: #fff; font: 800 13px var(--d); letter-spacing: .08em; rotate: 6deg; box-shadow: 0 6px 12px -4px rgba(120,0,0,.5); }
.stk { position: absolute; left: -48px; top: -4px; display: grid; place-items: center; width: 108px; height: 108px; border-radius: 50%; background: var(--ac); color: #fff; font: 800 20px/1 var(--d); text-align: center; rotate: -12deg; box-shadow: 0 10px 20px -8px rgba(120,0,0,.6); }
.tsl { display: block; margin-top: 30px; font: 500 12.5px var(--m); color: #555; } .tsl input { margin-top: 10px; }
.sh .k { display: inline-block; padding: 3px 8px; border-radius: 4px; background: #ffe600; color: #111; } .plan .pr { display: inline-block; padding: 8px 14px 6px; border-radius: 8px; background: #ffe600; }
.bars .y { background: var(--ac); } .tab.on { background: var(--ac); }
@media (max-width: 960px) { .ph { grid-template-columns: minmax(0, 1fr); gap: 20px; } }
@media (max-width: 460px) { .tag { padding: 30px 20px 22px; } .tg-top { padding-right: 56px; } .rib { right: -4px; } .tg-mid s { font-size: 38px; } .stk { width: 80px; height: 80px; font-size: 15px; left: -4px; top: 0; } .tg-bot .bc { width: 80px; } }
"""
E_HERO = f'''<section class="hero"><div class="wrap"><div class="ph"><div><a class="eyebrow" href="#calc"><b>Акция</b>каждый месяц</a><h1>Цена на рекламу <span>снижена.</span></h1><p class="sub">{SUB}</p>{ACTS}</div>
<div class="tw"><span class="pin" aria-hidden="true"></span><div class="tag" role="img" aria-label="Ценник: креативы для всех кабинетов — было $300, стало от $150 в месяц, бюджет не сгорает в конце месяца — пример">
<span class="hole"></span><div class="tg-top"><b>Креативы для всех рекламных кабинетов</b><span>ONEFLOW · генерация · 1 месяц · пример</span></div>
<div class="tg-mid"><div><small>Было</small><s id="told">$300</s></div><div class="nw"><small>Стало</small><em>от</em><b id="tnew">$150</b><i>*</i></div></div>
<div class="tg-bot"><span>Бюджет не сгорает<br>в конце месяца</span><i class="bc"></i></div><span class="rib">ВЫГОДА</span></div><span class="stk" aria-hidden="true">до<br>−50%*</span>
<label class="tsl">Ваш бюджет на генерации в месяц<input type="range" id="tb" min="20" max="1000" step="10" value="300"></label></div></div>{{LOGOS}}</div></section>'''
E_JS = '''<script>
(function () { const tb = document.getElementById('tb'), o = document.getElementById('told'), n = document.getElementById('tnew'); if (!tb) return;
  const up = (v) => { o.textContent = '$' + v; n.textContent = '$' + Math.round(v / 2); tb.style.setProperty('--p', ((v - 20) / 980 * 100) + '%'); };
  tb.addEventListener('input', () => up(+tb.value)); document.addEventListener('budget', (e) => { tb.value = e.detail; up(e.detail); }); up(300); })();
</script>
'''
page('v180-pricetag.html', 'ONEFLOW — цена на рекламу снижена', E_TOK, E_CSS, '<span style="width:20px;height:14px;border-radius:3px;background:#ffe600;box-shadow:inset 0 0 0 1.5px #111"></span>ONEFLOW',
     E_HERO, 'Цена на рекламу<br><span class="gt">снижена.</span>', stage_prod=5, js=E_JS, theme='#f3f0e8')
print('done 176-180')
