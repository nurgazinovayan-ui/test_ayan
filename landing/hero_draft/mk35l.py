"""Makes hero_pick35l.py from hero_pick35k.py: the same hero and strip, made fit for the site — colours that
follow the page theme, a phone and tablet layout, the player bar of the screenshot covered by the video."""
import sys
k, l = sys.argv[1:3]
s = open(k, encoding='utf-8').read()
def once(a, b):
    global s
    assert s.count(a) == 1, a
    s = s.replace(a, b)
# colours from the page theme instead of fixed light-on-dark ones
once("background: transparent; color: #f2f2f4; padding: 0 16px;", "background: transparent; color: var(--ink); padding: 0 16px;")
once("text-decoration-color: rgba(255,255,255,.35); }", "text-decoration-color: color-mix(in srgb, var(--ink) 35%, transparent); }")
once(".acts .btn.g:hover { text-decoration-color: #fff; }", ".acts .btn.g:hover { text-decoration-color: var(--ink); }")
once("border-radius: 2px; background: rgba(255,255,255,.08);", "border-radius: 2px; background: color-mix(in srgb, var(--ink) 9%, transparent);")
once(".hs .hs-cells i.at { background: #f2f2f4;", ".hs .hs-cells i.at { background: var(--ink);")
once("border-radius: 50%; background: rgba(255,255,255,.14); color: #d6d7de;", "border-radius: 50%; background: color-mix(in srgb, var(--ink) 14%, transparent); color: var(--ink2);")
once(".hs .hs-q:hover i, .hs .hs-q:focus i {", ".hs .hs-q:hover i, .hs .hs-q:focus i, .hs .hs-q.open i {")
once(".hs .hs-sum b { display: block;", ".hs .hs-sum b { display: flex; white-space: nowrap;")
# the squares: half as many on a phone, rebuilt when the width crosses that line
once("""  for (var i = 0; i < N; i++) {
    var c = document.createElement('i');
    c.style.setProperty('--c', 'hsl(' + HUES[Math.min(HUES.length - 1, Math.floor(i * HUES.length / N))] + ' 100% 62%)');
    box.appendChild(c); cells.push(c);
  }
""", """  var narrow = window.matchMedia('(max-width: 720px)');
  function build() {
    N = narrow.matches ? 24 : 48; box.textContent = ''; cells = [];
    for (var i = 0; i < N; i++) {
      var c = document.createElement('i');
      c.style.setProperty('--c', 'hsl(' + HUES[Math.min(HUES.length - 1, Math.floor(i * HUES.length / N))] + ' 100% 62%)');
      box.appendChild(c); cells.push(c);
    }
  }
  build();
""")
once("  r.addEventListener('input', draw); draw();\n", """  r.addEventListener('input', draw); draw();
  var again = function () { build(); draw(); };
  if (narrow.addEventListener) narrow.addEventListener('change', again); else if (narrow.addListener) narrow.addListener(again);
  /* a tap on «?» opens its note and a tap anywhere else closes it (a phone has no hover) */
  document.addEventListener('click', function (e) {
    var q = e.target && e.target.closest ? e.target.closest('#topup .hs-q') : null;
    [].forEach.call(root.querySelectorAll('.hs-q.open'), function (x) { if (x !== q) x.classList.remove('open'); });
    if (q) q.classList.toggle('open');
  });
""")
once("\n\nassert hero.endswith('</div></div></section>')", '''
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

assert hero.endswith('</div></div></section>')''')
open(l, 'w', encoding='utf-8').write(s)
