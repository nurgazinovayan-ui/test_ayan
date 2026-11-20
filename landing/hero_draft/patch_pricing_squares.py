"""The pricing section of the landing gets the same control as the strip under the hero: a row of squares over an
invisible range input, and numbers that roll like a drum. The strip's script now gives both blocks the same two
helpers (window.ofRoll, window.ofSquares).   python3 -I patch_pricing_squares.py <ru.html> <index.html>"""
import re, sys

STRIP_JS = r"""
/* The squares and the rolling numbers, shared by the strip under the hero and the pricing section. The squares
   light up to the chosen sum and the last lit ones pulse — the larger the sum, the stronger; a number rolls to
   its new value like a drum. In the strip: credits per $1 as in the pricing section; a photo is Nano Banana 2.1
   (4 credits), a video Seedance 2.5, 5 s at 480p (48), a track Suno V6 (14). */
(function () {
  var HUES = [326, 300, 262, 236, 212, 190, 158, 110, 70, 36], PULSE = 7;
  var narrow = window.matchMedia('(max-width: 720px)');
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
  /* the squares of one .hs-px block; returns paint(part of the scale 0..1, strength of the pulse 0..1).
     Half as many squares on a phone, rebuilt when the width crosses that line. */
  function squares(px) {
    var box = px.querySelector('.hs-cells'), cells = [], last = [0, 0];
    function build() {
      var N = narrow.matches ? 24 : 48; box.textContent = ''; cells = [];
      for (var i = 0; i < N; i++) {
        var c = document.createElement('i');
        c.style.setProperty('--c', 'hsl(' + HUES[Math.min(HUES.length - 1, Math.floor(i * HUES.length / N))] + ' 100% 62%)');
        box.appendChild(c); cells.push(c);
      }
    }
    function paint(part, amp) {
      last = [part, amp];
      var N = cells.length, lit = Math.max(1, Math.round(part * (N - 1)) + 1);
      box.style.setProperty('--amp', amp.toFixed(3));
      box.style.setProperty('--beat', (1.5 - amp * 0.85).toFixed(2) + 's');
      cells.forEach(function (c, i) {
        var back = lit - 1 - i; /* 0 is the square under the thumb */
        c.className = i < lit - 1 ? 'on' : i === lit - 1 ? 'on at' : '';
        /* the last lit squares pulse, the nearer to the end the more */
        if (back > 0 && back <= PULSE) { c.classList.add('beat'); c.style.setProperty('--near', (1 - (back - 1) / PULSE).toFixed(2)); c.style.animationDelay = (-back * 0.09).toFixed(2) + 's'; }
      });
    }
    build();
    var again = function () { build(); paint(last[0], last[1]); };
    if (narrow.addEventListener) narrow.addEventListener('change', again); else if (narrow.addListener) narrow.addListener(again);
    return paint;
  }
  window.ofRoll = roll; window.ofSquares = squares;

  var root = document.getElementById('topup'); if (!root) return;
  var COST = { photo: 4, video: 48, music: 14 }, GAP = '@GAP@';
  var r = root.querySelector('input'), paint = squares(root.querySelector('.hs-px'));
  function sp(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, GAP); }
  function draw() {
    var usd = Number(r.value), credits = usd * (usd < 50 ? 50 : usd < 200 ? 55 : 60);
    roll(root.querySelector('[data-o=usd]'), '$' + usd);
    roll(root.querySelector('[data-o=credits]'), sp(credits));
    for (var k in COST) roll(root.querySelector('[data-o=' + k + ']'), sp(Math.floor(credits / COST[k])));
    paint((usd - 10) / 490, usd / 500);
  }
  r.addEventListener('input', draw); draw();
  /* a tap on «?» opens its note and a tap anywhere else closes it (a phone has no hover) */
  document.addEventListener('click', function (e) {
    var q = e.target && e.target.closest ? e.target.closest('#topup .hs-q') : null;
    [].forEach.call(root.querySelectorAll('.hs-q.open'), function (x) { if (x !== q) x.classList.remove('open'); });
    if (q) q.classList.toggle('open');
  });
})();
"""

CSS = """
/* the pricing section: the same squares and rolling numbers as the strip under the hero (the owner, 2026-11-20) */
#pricing .tp-px { margin: 34px 0 30px; }
#pricing .tp-usd.hs-roll { display: flex; min-width: 0; }
#pricing .tp-usd .hs-col u, #pricing .tp-usd .hs-ch { line-height: 1; }
#pricing .tp-get b { display: flex; align-items: center; gap: .3em; line-height: 1.1; }
#pricing .tp-get b span { font: inherit; color: inherit; }
#pricing .gens ul { gap: 11px !important; }
#pricing .gens li > span:first-child { display: flex; align-items: center; gap: .32em; line-height: 1; }
"""


def patch(path, lang):
    s = open(path, encoding='utf-8').read()

    def once(a, b):
        nonlocal s
        assert s.count(a) == 1, (path, a[:70], s.count(a))
        s = s.replace(a, b)

    # 1. the strip's script: helpers for both blocks
    m = re.search(r'(<input id="hsTop"[^>]*></div>\n</div><script>).*?(</script></section>)', s, re.S)
    assert m and "GAP = '" in m.group(0)
    gap = re.search(r"GAP = '(.)'", m.group(0)).group(1)
    s = s[:m.start()] + m.group(1) + STRIP_JS.replace('@GAP@', gap) + m.group(2) + s[m.end():]
    # 2. `.hs` as a plain class may now stand on blocks of the pricing card: its own padding is the strip's only
    once('.hs { padding: 6px 0 50px; }', 'section.hs { padding: 6px 0 50px; }')
    once('  .hs { padding-bottom: 40px; }', '  section.hs { padding-bottom: 40px; }')
    # 3. the pricing card: squares instead of the slider, rolled numbers
    once('<div class="tp-l tp-calc">', '<div class="tp-l tp-calc hs">')
    once('<div class="gens tp-calc">', '<div class="gens tp-calc hs">')
    once('<div class="tp-usd" id="tpUsd">$50</div>', '<div class="tp-usd hs-roll" id="tpUsd"></div>')
    m = re.search(r'<b id="tpCr">([\d\s, ]+) ([^<]+)</b>', s)
    assert m, path
    s = s[:m.start()] + f'<b id="tpCr"><span class="hs-roll" id="tpCrN"></span><span id="tpCrW">{m.group(2)}</span></b>' + s[m.end():]
    m = re.search(r'<div class="tp-sl" style="--tpp:37\.5%">(<input type="range" id="tpR"[^>]*>)<div class="tp-mk" aria-hidden="true">.*?</div></div>', s, re.S)
    assert m, path
    s = s[:m.start()] + '<div class="tp-px hs-px"><div class="hs-cells" aria-hidden="true"></div>' + m.group(1) + '</div>' + s[m.end():]
    n = len(re.findall(r'<b data-c="(\d+)">≈ [\d\s, ]+</b>', s))
    assert n == 3, (path, n)
    s = re.sub(r'<b data-c="(\d+)">≈ [\d\s, ]+</b>', r'<b class="hs-roll" data-c="\1"></b>', s)
    # 4. the pricing script paints the squares and rolls the numbers
    once("const $ = (id) => document.getElementById(id), sl = r.parentElement, base = tiers[0][1];",
         "const $ = (id) => document.getElementById(id), base = tiers[0][1];\n"
         "  const roll = window.ofRoll || ((el, t) => { el.textContent = t; }), paint = window.ofSquares ? window.ofSquares(r.parentElement) : () => {};")
    once("$('tpUsd').textContent = '$' + usd; $('tpCr').textContent = crs;", "roll($('tpUsd'), '$' + usd); roll($('tpCrN'), num(cr)); $('tpCrW').textContent = word(cr);")
    once("sl.style.setProperty('--tpp', (i / (stops.length - 1)) * 100 + '%'); r.setAttribute(", "paint(i / (stops.length - 1), usd / 500); r.setAttribute(")
    once("document.querySelectorAll('#pricing [data-c]').forEach((b) => { b.textContent = '≈ ' + num(Math.floor(cr / +b.dataset.c)); });",
         "document.querySelectorAll('#pricing [data-c]').forEach((b) => { roll(b, '≈ ' + num(Math.floor(cr / +b.dataset.c))); });")
    once("// pricing slider: same stops and tiers as the app's top-up window; numbers are formatted for the page language",
         "// pricing: same stops and tiers as the app's top-up window, drawn as the squares of the strip under the hero;\n// numbers are formatted for the page language and roll to their new value")
    end = s.rfind('</style>', 0, s.index('</head>'))
    s = s[:end] + CSS + s[end:]
    open(path, 'w', encoding='utf-8').write(s)
    print(lang, 'ok')


patch(sys.argv[1], 'ru'); patch(sys.argv[2], 'en')
