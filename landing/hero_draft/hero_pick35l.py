"""The hero as chosen on 2026-11-19: mock-up 35 (three windows of the app under the logos of their modes) plus the
top-up slider, drawn like the cards of the engines block below it — no outlines, no round pills, no small type.

What the slider counts (see hero_pick14.py for where each number comes from):
  credits per $1 50 / 55 / 60 · a photo 4 credits (Nano Banana 2.1) · a video 49 credits (Seedance 2.5, 5 s, 480p,
  through Atlas Cloud) · a track 14 credits (Suno V6 through Atlas Cloud, one request, two takes)

python3 -I hero_pick35.py <ru|en> <built page of that language> <out html> <hero_variants7.py> <index.html (en)> <logo svg> <scratch dir>"""
import math, re, sys

lang, src, out, v7, en_page, logo, scratch = sys.argv[1:8]
page = open(src, encoding='utf-8').read()

# mock-up 35 as it was shown: its styles and markup are taken from the script that made it
ns = {'__name__': 'v7'}
argv, sys.argv = sys.argv, [v7, en_page, scratch, logo]
exec(compile(open(v7, encoding='utf-8').read(), v7, 'exec'), ns)
sys.argv = argv
css, hero, glow, REG = ns['V35_CSS'], ns['V35'], ns['glow'], ns['REG']

PHOTO, VIDEO, MUSIC = 4, math.ceil(0.1397 * 5 * 0.7 * 100 - 1e-9), math.ceil(0.132 * 100 - 1e-9)
assert (PHOTO, VIDEO, MUSIC) == (4, 49, 14)
START = 50 * 55
GAP = ' ' if lang == 'ru' else ','
num = lambda n: f'{n:,}'.replace(',', GAP)

T = {
    'ru': dict(h1=('Рекламная студия в вашем браузере', 'Рекламная студия<br><b>в вашем браузере</b>'),
               sub='Фото, видео, музыка и тексты на 30+ нейросетях. Без подписки, до 50% дешевле*',
               go='Начать бесплатно →', how='Как это работает', word='Баланс', t='Бюджет не сгорает',
               p='Пополняете на любую сумму и создаёте, когда нужно. В конце месяца ничего не пропадает: кредиты действуют 12 месяцев.',
               pay='Пополняете', get='Получаете', credits='кредитов', per='кредитов за $1', bonus='бонус', enough='Этого хватит примерно на',
               photo=('фото', 'Nano Banana 2.1'), video=('или видео', 'Seedance 2.5 · 5 с · 480p'), music=('или треков', 'Suno V6 · по 2 варианта'),
               aria='Сумма пополнения в долларах'),
    'en': dict(h1=('The ad studio in your browser', 'The ad studio <b>in your browser</b>'),
               sub='Photos, videos, music and copy from 30+ AI models. No subscription, up to 50% cheaper*',
               go='Start free →', how='How it works', word='Balance', t='Your budget doesn’t burn',
               p='Top up any amount and create when you need to. Nothing is lost at the end of the month: credits stay valid for 12 months.',
               pay='You top up', get='You get', credits='credits', per='credits per $1', bonus='bonus', enough='Enough for about',
               photo=('images', 'Nano Banana 2.1'), video=('or videos', 'Seedance 2.5 · 5 s · 480p'), music=('or tracks', 'Suno V6 · 2 takes each'),
               aria='Top-up amount in dollars'),
}[lang]


def once(s, a, b):
    assert s.count(a) == 1, a
    return s.replace(a, b)


hero = once(hero, '<h1 aria-label="The ad studio in your browser">The ad studio <b>in your browser</b></h1>', f'<h1 aria-label="{T["h1"][0]}">{T["h1"][1]}</h1>')
hero = once(hero, '30+ AI models in one window. No subscription, up to 50% cheaper*', T['sub'])
hero = once(hero, 'Start free →', T['go'])
hero = once(hero, 'How it works', T['how'])
hero = hero.replace('/pe/en/', f'/pe/{lang}/')

css += """
/* 35 as chosen: the top-up slider as one more card of the page — no outlines, no pills, no small type */
.hero.hq35 { padding-bottom: 50px; overflow: visible; }
.hero.hq35 .hq-desk { height: 420px; margin-top: 60px; }
.hero.hq35 .w-l .hq-logo { left: 30%; }
.hero.hq35 .w-r .hq-logo { left: 70%; }
.hero.hq35 .hq-bal { z-index: 4; margin-top: -64px; display: grid; grid-template-columns: 350px 1fr; text-align: left; }
.hero.hq35 .hq-bal .hq-glow { left: 0; margin-left: -90px; top: -96px; }
.hero.hq35 .hq-bal .hq-word { left: 34px; transform: translateY(-50%); }
.hero.hq35 .hq-copy { position: relative; padding: 56px 20px 38px 34px; }
.hero.hq35 .hq-copy h3 { margin: 0; font: 200 34px/1.08 var(--d); letter-spacing: -.04em; color: var(--ink); }
.hero.hq35 .hq-copy p { margin: 14px 0 0; font: 400 16px/1.5 var(--d); color: var(--muted); }
.hero.hq35 .hq-calc { position: relative; padding: 44px 38px 38px 30px; }
.hero.hq35 .hq-top { display: flex; justify-content: space-between; align-items: flex-end; gap: 30px; }
.hero.hq35 .hq-top > div:last-child { text-align: right; }
.hero.hq35 .hq-lab { display: block; font: 400 16px/1 var(--d); color: var(--muted); }
.hero.hq35 .hq-val { margin-top: 10px; font: 200 62px/1 var(--d); letter-spacing: -.055em; color: var(--ink); white-space: nowrap; }
.hero.hq35 .hq-val small { margin-left: 10px; font: 400 19px/1 var(--d); letter-spacing: 0; color: var(--ink2); }
.hero.hq35 input[type=range] { -webkit-appearance: none; appearance: none; display: block; width: 100%; height: 8px; margin: 22px 0 0; border: 0; border-radius: 3px; background: linear-gradient(90deg, hsl(158 72% 56%) var(--hqpos, 8.16%), var(--field, #26262a) var(--hqpos, 8.16%)); outline-offset: 8px; cursor: pointer; }
.hero.hq35 input[type=range]::-webkit-slider-thumb { -webkit-appearance: none; width: 14px; height: 34px; border-radius: 4px; background: #f2f2f4; box-shadow: 0 6px 16px rgba(0,0,0,.55); }
.hero.hq35 input[type=range]::-moz-range-thumb { width: 14px; height: 34px; border: 0; border-radius: 4px; background: #f2f2f4; }
.hero.hq35 .hq-rate { margin-top: 18px; font: 400 16px/1.2 var(--d); color: var(--muted); text-align: right; }
.hero.hq35 .hq-enough { margin-top: 4px; font: 400 16px/1.2 var(--d); color: var(--muted); }
.hero.hq35 .hq-for { margin-top: 14px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }
.hero.hq35 .hq-for b { display: block; font: 200 48px/1 var(--d); letter-spacing: -.05em; color: var(--ink); white-space: nowrap; }
.hero.hq35 .hq-for span { display: block; margin-top: 10px; font: 500 18px/1.2 var(--d); letter-spacing: -.01em; color: var(--ink); }
.hero.hq35 .hq-for em { display: block; margin-top: 5px; font: 400 16px/1.3 var(--d); font-style: normal; color: var(--muted); white-space: nowrap; }
"""


def cell(key, n):
    name, model = T[key]
    return f'<div><b data-o="{key}">≈ {num(n)}</b><span>{name}</span><em>{model}</em></div>'


# the «Баланс» card is gone altogether (the owner, 2026-11-20)
slider = ''

# three plain buttons (the owner, 2026-11-20): a demo beside the two, small corner radii, no arrow, no glow
DEMO = {'ru': 'Демо', 'en': 'Demo'}[lang]
GO = {'ru': 'Начать бесплатно', 'en': 'Start free'}[lang]
hero = once(hero, T['go'] + '</a>', GO + '</a>')
hero = once(hero, T['how'] + '</a>', T['how'] + f'</a><a class="btn g" href="/app?demo=1">{DEMO}</a>')
css += """
/* buttons, style C (the owner, 2026-11-20): one blue main button, the other two as underlined words */
html[lang] .hero.hq35 .acts { position: relative; z-index: 3; gap: 10px; margin-top: 30px; }
html[lang] .hero.hq35 .acts .btn { height: 52px; padding: 0 26px; border-radius: 8px; font: 500 16px/1 var(--d); letter-spacing: 0; box-shadow: none; transform: none; transition: background .15s, text-decoration-color .15s; }
html[lang] .hero.hq35 .acts .btn.p { background: #0a6cff; color: #fff; }
html[lang] .hero.hq35 .acts .btn.p:hover { background: #2a80ff; }
html[lang] .hero.hq35 .acts .btn.g { background: transparent; color: var(--ink); padding: 0 16px; backdrop-filter: none; -webkit-backdrop-filter: none; text-decoration: underline; text-underline-offset: 6px; text-decoration-thickness: 1px; text-decoration-color: color-mix(in srgb, var(--ink) 35%, transparent); }
html[lang] .hero.hq35 .acts .btn.g:hover { text-decoration-color: var(--ink); }
/* the light behind the windows (the owner, 2026-11-20): never cut by an edge — the block reaches up behind the
   buttons and fades out on every side — and it drifts and changes its tint slowly */
html[lang] .hero.hq35 .hq-desk { height: 540px; margin-top: -60px; pointer-events: none;
  -webkit-mask-image: linear-gradient(180deg, transparent 0, #000 120px, #000 73%, transparent 100%), linear-gradient(90deg, transparent 0, #000 5%, #000 95%, transparent 100%);
  mask-image: linear-gradient(180deg, transparent 0, #000 120px, #000 73%, transparent 100%), linear-gradient(90deg, transparent 0, #000 5%, #000 95%, transparent 100%);
  -webkit-mask-composite: source-in; mask-composite: intersect; }
html[lang] .hero.hq35 .w-c { top: 140px; }
html[lang] .hero.hq35 .w-l, html[lang] .hero.hq35 .w-r { top: 216px; }
html[lang] .hero.hq35 .hq-w .hq-blob { left: -4%; right: -4%; top: -96px; height: 210px; background: hsl(var(--h) 100% 62% / .5); filter: blur(64px); animation: hq-drift 11s ease-in-out infinite alternate; will-change: transform, opacity; }
html[lang] .hero.hq35 .hq-w .hq-blob::after { content: ""; position: absolute; inset: 0; border-radius: 50%; background: hsl(calc(var(--h) + 56) 100% 64% / .6); opacity: 0; animation: hq-tint 7s ease-in-out infinite alternate; }
html[lang] .hero.hq35 .w-l .hq-blob { animation-delay: -4s; animation-duration: 13s; }
html[lang] .hero.hq35 .w-l .hq-blob::after { animation-delay: -2.5s; }
html[lang] .hero.hq35 .w-r .hq-blob { animation-delay: -8s; animation-duration: 15s; }
html[lang] .hero.hq35 .w-r .hq-blob::after { animation-delay: -5s; }
@keyframes hq-drift { 0% { transform: translate(-9%, 6px) scale(.9, .92); opacity: .7; } 50% { transform: translate(5%, -10px) scale(1.08, 1.12); opacity: 1; } 100% { transform: translate(10%, 4px) scale(.96, 1); opacity: .8; } }
@keyframes hq-tint { 0% { opacity: 0; } 100% { opacity: 1; } }
@media (prefers-reduced-motion: reduce) { html[lang] .hero.hq35 .hq-w .hq-blob, html[lang] .hero.hq35 .hq-w .hq-blob::after { animation: none; } }
"""

# a narrow strip under the hero (the owner, 2026-11-20): a top-up slider and how many generations it buys.
# Credits per $1 as in the pricing section; a photo is Nano Banana 2.1 (4 credits), a video is Seedance 2.5,
# 5 s at 480p (Atlas $0.1348 a second, counted from 70%: 48 credits), a track is Suno V6 (14 credits).
import math as _m
SP, SV, SM = 4, _m.ceil(0.1348 * 5 * 0.7 * 100 - 1e-9), 14
assert (SP, SV, SM) == (4, 48, 14)
HINT = {'ru': dict(photo='Nano Banana 2.1 · 1K · 4 кредита за фото', video='Seedance 2.5 · 480p · 5 секунд со звуком · 48 кредитов', music='Suno V6 · два варианта трека за запрос · 14 кредитов', q='Как посчитано'),
        'en': dict(photo='Nano Banana 2.1 · 1K · 4 credits per image', video='Seedance 2.5 · 480p · 5 seconds with sound · 48 credits', music='Suno V6 · two takes per request · 14 credits', q='How it is counted')}[lang]
def q(key, side=''):
    return f'<button type="button" class="hs-q{side}" aria-label="{HINT["q"]}: {HINT[key]}">?<i role="tooltip">{HINT[key]}</i></button>'
ST = {'ru': dict(pay='Пополняете', get='кредитов', photo='фото', video='видео по 5 с', music='треков', aria='Сумма пополнения в долларах', tp='Nano Banana 2.1', tv='Seedance 2.5, 480p', tm='Suno V6'),
      'en': dict(pay='You top up', get='credits', photo='images', video='5 s videos', music='tracks', aria='Top-up amount in dollars', tp='Nano Banana 2.1', tv='Seedance 2.5, 480p', tm='Suno V6')}[lang]
STRIP_HTML = r"""<section class="hs" id="topup"><div class="wrap">
<div class="hs-top"><div class="hs-sum"><label for="hsTop">@PAY@</label><b class="hs-roll" data-o="usd"></b></div>
<div class="hs-out"><span><b class="hs-roll" data-o="credits"></b> @GET@</span><span><b class="hs-roll" data-o="photo"></b> @PHOTO@@QP@</span><span><b class="hs-roll" data-o="video"></b> @VIDEO@@QV@</span><span><b class="hs-roll" data-o="music"></b> @MUSIC@@QM@</span></div></div>
<div class="hs-px"><div class="hs-cells" aria-hidden="true"></div><input id="hsTop" type="range" min="10" max="500" step="10" value="50" aria-label="@ARIA@"></div>
</div><script>
/* The top-up strip: the squares light up to the chosen sum and the last lit ones pulse — the larger the sum, the
   stronger; every number rolls to its new value like a drum. Credits per $1 as in the pricing section; a photo
   is Nano Banana 2.1 (4 credits), a video Seedance 2.5, 5 s at 480p (48), a track Suno V6 (14). */
(function () {
  var root = document.getElementById('topup'); if (!root) return;
  var COST = { photo: @SP@, video: @SV@, music: @SM@ }, GAP = '@GAP@', N = 48, PULSE = 7;
  var HUES = [326, 300, 262, 236, 212, 190, 158, 110, 70, 36];
  var r = root.querySelector('input'), box = root.querySelector('.hs-cells'), cells = [];
  var narrow = window.matchMedia('(max-width: 720px)');
  function build() {
    N = narrow.matches ? 24 : 48; box.textContent = ''; cells = [];
    for (var i = 0; i < N; i++) {
      var c = document.createElement('i');
      c.style.setProperty('--c', 'hsl(' + HUES[Math.min(HUES.length - 1, Math.floor(i * HUES.length / N))] + ' 100% 62%)');
      box.appendChild(c); cells.push(c);
    }
  }
  build();
  function sp(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, GAP); }
  /* a number as columns of digits: a column slides to its digit; columns are added and taken away on the left */
  function roll(el, text) {
    var want = text.split(''), have = [].slice.call(el.children);
    while (have.length > want.length) el.removeChild(have.shift());
    while (have.length < want.length) { var s = document.createElement('span'); el.insertBefore(s, el.firstChild); have.unshift(s); }
    want.forEach(function (ch, k) {
      var s = have[k], digit = ch >= '0' && ch <= '9';
      if (!digit) { s.className = 'hs-ch'; s.textContent = ch; return; }
      if (s.className !== 'hs-col') { s.className = 'hs-col'; s.innerHTML = '<u>0<br>1<br>2<br>3<br>4<br>5<br>6<br>7<br>8<br>9</u>'; }
      s.firstChild.style.transform = 'translateY(' + (-Number(ch) * 10) + '%)';
    });
    el.setAttribute('aria-label', text);
  }
  function draw() {
    var usd = Number(r.value), credits = usd * (usd < 50 ? 50 : usd < 200 ? 55 : 60), part = (usd - 10) / 490;
    var lit = Math.max(1, Math.round(part * (N - 1)) + 1), amp = usd / 500;
    roll(root.querySelector('[data-o=usd]'), '$' + usd);
    roll(root.querySelector('[data-o=credits]'), sp(credits));
    for (var k in COST) roll(root.querySelector('[data-o=' + k + ']'), sp(Math.floor(credits / COST[k])));
    box.style.setProperty('--amp', amp.toFixed(3));
    box.style.setProperty('--beat', (1.5 - amp * 0.85).toFixed(2) + 's');
    cells.forEach(function (c, i) {
      var back = lit - 1 - i; /* 0 is the square under the thumb */
      c.className = i < lit - 1 ? 'on' : i === lit - 1 ? 'on at' : '';
      /* the last lit squares pulse, the nearer to the end the more */
      if (back > 0 && back <= PULSE) { c.classList.add('beat'); c.style.setProperty('--near', (1 - (back - 1) / PULSE).toFixed(2)); c.style.animationDelay = (-back * 0.09).toFixed(2) + 's'; }
    });
  }
  r.addEventListener('input', draw); draw();
  var again = function () { build(); draw(); };
  if (narrow.addEventListener) narrow.addEventListener('change', again); else if (narrow.addListener) narrow.addListener(again);
  /* a tap on «?» opens its note and a tap anywhere else closes it (a phone has no hover) */
  document.addEventListener('click', function (e) {
    var q = e.target && e.target.closest ? e.target.closest('#topup .hs-q') : null;
    [].forEach.call(root.querySelectorAll('.hs-q.open'), function (x) { if (x !== q) x.classList.remove('open'); });
    if (q) q.classList.toggle('open');
  });
})();
</script></section>"""
strip = STRIP_HTML
for k, v in {'@PAY@': ST['pay'], '@GET@': ST['get'], '@PHOTO@': ST['photo'], '@VIDEO@': ST['video'], '@MUSIC@': ST['music'], '@ARIA@': ST['aria'],
             '@QP@': q('photo'), '@QV@': q('video', ' r'), '@QM@': q('music', ' r'), '@SP@': str(SP), '@SV@': str(SV), '@SM@': str(SM), '@GAP@': GAP}.items():
    strip = strip.replace(k, v)
assert '@' not in strip.replace('@keyframes', '')
css += """
/* the strip under the hero (variant L, chosen 2026-11-20): a top-up slider drawn as a row of squares and what
   the sum buys — no card, no outlines */
.hs { padding: 6px 0 50px; }
.hs .hs-top { display: flex; align-items: flex-end; justify-content: space-between; gap: 40px; margin-bottom: 24px; }
.hs .hs-sum label { display: block; margin-bottom: 10px; font: 400 16px/1 var(--d); color: var(--muted); }
.hs .hs-sum b { display: flex; white-space: nowrap; font: 200 56px/1 var(--d); letter-spacing: -.05em; color: var(--ink); }
.hs .hs-out { display: flex; gap: 34px; }
.hs .hs-out > span { display: flex; align-items: center; gap: 8px; min-height: 22px; font: 400 18px/1 var(--d); color: var(--muted); white-space: nowrap; }
.hs .hs-out > span > b { font: 500 18px/1 var(--d); color: var(--ink); }
/* a number that rolls: each digit is a column of ten */
.hs .hs-roll { display: inline-flex; font-variant-numeric: tabular-nums; }
.hs .hs-col { display: inline-block; height: 1em; overflow: hidden; }
.hs .hs-col u { display: block; text-decoration: none; line-height: 1; transition: transform .55s cubic-bezier(.2, .9, .25, 1); will-change: transform; }
.hs .hs-ch { display: inline-block; white-space: pre; }
/* the squares; the real range input lies over them, invisible, so the keyboard and touch work as usual */
.hs .hs-px { position: relative; }
.hs .hs-cells { display: flex; gap: 4px; }
.hs .hs-cells i { flex: 1; aspect-ratio: 1; border-radius: 2px; background: color-mix(in srgb, var(--ink) 9%, transparent); transition: background .2s; }
.hs .hs-cells i.on { background: var(--c); }
.hs .hs-cells i.at { background: var(--ink); transform: scale(1.35); }
.hs .hs-cells i.beat { animation: hs-beat var(--beat, 1.4s) ease-in-out infinite; }
@keyframes hs-beat {
  0%, 100% { transform: scale(1); filter: brightness(1); box-shadow: 0 0 0 0 transparent; }
  50% { transform: scale(calc(1 + .5 * var(--amp, 0) * var(--near, 0))); filter: brightness(calc(1 + .7 * var(--amp, 0) * var(--near, 0))); box-shadow: 0 0 calc(22px * var(--amp, 0) * var(--near, 0)) var(--c); }
}
.hs .hs-px input { position: absolute; inset: -10px 0; width: 100%; height: calc(100% + 20px); margin: 0; opacity: 0; cursor: pointer; -webkit-appearance: none; appearance: none; }
.hs .hs-px:has(input:focus-visible) .hs-cells i.at { box-shadow: 0 0 0 3px #0a6cff; }
/* the small «?» beside a name: what model, size and price the number is counted by */
.hs .hs-q { position: relative; flex: none; width: 20px; height: 20px; padding: 0; border: 0; border-radius: 50%; background: color-mix(in srgb, var(--ink) 14%, transparent); color: var(--ink2); font: 600 12px/20px var(--d); text-align: center; cursor: help; }
.hs .hs-q:hover, .hs .hs-q:focus-visible { background: #0a6cff; color: #fff; outline: 0; }
.hs .hs-q i { position: absolute; z-index: 5; left: 50%; bottom: 30px; transform: translateX(-50%); width: max-content; max-width: 280px; padding: 12px 14px; border-radius: 8px; background: #1f2026; color: #f2f2f4; font: 400 15px/1.4 var(--d); font-style: normal; text-align: left; white-space: normal; box-shadow: 0 14px 30px rgba(0,0,0,.5); opacity: 0; visibility: hidden; transition: opacity .12s; pointer-events: none; }
.hs .hs-q.r i { left: auto; right: -12px; transform: none; }
.hs .hs-q:hover i, .hs .hs-q:focus i, .hs .hs-q.open i { opacity: 1; visibility: visible; }
@media (prefers-reduced-motion: reduce) { .hs .hs-cells i.beat { animation: none; } .hs .hs-col u { transition: none; } }
"""

css += """
/* the video lies over the player bar that is drawn in the screenshot under it */
html[lang] .hero.hq35 .w-c video { height: 55.6%; }
/* light theme: a dark logo cannot be read over a dark window, so it stands on the window instead of across its edge */
html:not([data-theme="dark"]) .hero.hq35 .hq-logo { transform: translate(-50%, -118%); }
/* a digit sits in the middle of its column (a «1» is narrower than the column) */
.hs .hs-col u { text-align: center; }
/* narrower screens: the numbers go above the squares in rows */
@media (max-width: 1100px) {
  .hs .hs-top { flex-direction: column; align-items: flex-start; gap: 22px; }
  .hs .hs-out { flex-wrap: wrap; gap: 14px 34px; }
}
/* a tablet and a phone: one window, as wide as the page */
@media (max-width: 900px) {
  html[lang] .hero.hq35 .w-l, html[lang] .hero.hq35 .w-r { display: none; }
  html[lang] .hero.hq35 .hq-desk { height: auto; padding-top: 140px; }
  html[lang] .hero.hq35 .w-c { position: relative; left: auto; top: auto; width: min(100%, 740px); margin: 0 auto; }
}
@media (max-width: 720px) {
  html[lang] .hero.hq35 { padding-bottom: 34px; }
  html[lang] .hero.hq35 .acts { flex-direction: row; flex-wrap: wrap; justify-content: center; gap: 6px 10px; }
  html[lang] .hero.hq35 .acts .btn.p { flex: 1 1 100%; }
  html[lang] .hero.hq35 .acts .btn.g { flex: 0 0 auto; width: auto; height: 46px; }
  html[lang] .hero.hq35 .hq-desk { padding-top: 122px; }
  .hs { padding-bottom: 40px; }
  .hs .hs-sum b { font-size: 48px; }
  .hs .hs-top { position: relative; }
  .hs .hs-out { display: grid; grid-template-columns: 1fr 1fr; gap: 16px 14px; width: 100%; }
  .hs .hs-out > span, .hs .hs-out > span > b { font-size: 16px; }
  .hs .hs-cells { gap: 3px; }
  .hs .hs-q { position: static; }
  .hs .hs-q::before { content: ""; position: absolute; width: 44px; height: 44px; margin: -12px 0 0 -12px; }
  .hs .hs-q i, .hs .hs-q.r i { left: 0; right: 0; bottom: calc(100% + 12px); width: auto; max-width: none; transform: none; }
}
"""

assert hero.endswith('</div></div></section>')
hero = hero[:-len('</div></section>')] + slider + '</div></section>'

HERO = re.compile(r'<section class="hero">.*?</section>', re.S)
NEWS = re.compile(r'<div class="news" id="news".*?(?=<div class="mrow">)', re.S)
assert len(HERO.findall(page)) == 1 and len(NEWS.findall(page)) == 1
s = HERO.sub(lambda m: hero + strip, page)
# the banners of what is new stay under the hero (the owner, 2026-11-20)
end = s.rfind('</style>', 0, s.index('</head>'))
s = s[:end] + css + s[end:]
open(out, 'w', encoding='utf-8').write(s)
print(lang, 'ok: $50 →', START, 'credits →', START // PHOTO, START // VIDEO, START // MUSIC)
