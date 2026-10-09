"""oneflow.art in the app's dark theme, behind a ☀/☾ switch next to EN/RU.

The light «Soft» page (soft.py) stays the default: a first visit is always light. The switch sets
<html data-theme="dark"> and stores the choice under the app's own key, 'oneflow-theme', so the site and the app at
/app (same origin) open in the same theme. A one-line script in <head> applies a stored choice before the first paint.

Dark tokens come from the app (App.css «STYLE V2» dark): page #0b0b0d, cards #151517 / #1d1d20, fields #26262a, text
#f2f2f4. Buttons mirror the light page: the main action is the light pill (the light page's black pill, inverted), the
secondary ones are dark pills; the accent is the same flat blue as the light page, a step lighter for small text.
"""

D = 'html[data-theme="dark"]'

_CSS = """
/* ===================== dark theme (the ☀/☾ switch) ===================== */
$ { --bg: #0b0b0d; --ink: #f2f2f4; --ink2: #b4b4bb; --muted: #8f8f97; --line: rgba(255,255,255,.08); --card: #151517; --raised: #1d1d20; --field: #26262a;
  --ac: #f2f2f4; --acink: #111113; --acsoft: rgba(10,108,255,.18); --olive: #4c9bff; --ok: #4c9bff; --green: #4c9bff; --mint: rgba(10,108,255,.18);
  --s0: #151517; --s1: #1d1d20; --s2: #232327; --s3: #2c2c31; --dot: #2c2c31; --dim: #5c5c63; --num: #f2f2f4;
  --sh: 0 1px 0 rgba(255,255,255,.04) inset, 0 22px 44px -30px rgba(0,0,0,.8); --sh-sm: 0 1px 0 rgba(255,255,255,.05) inset, 0 8px 18px -12px rgba(0,0,0,.8);
  --sh2: 0 1px 0 rgba(255,255,255,.04) inset, 0 34px 70px -40px rgba(0,0,0,.9); color-scheme: dark; }
/* buttons: light main pill, dark secondary pills */
$ .btn.p { background: #f2f2f4; color: #111113; box-shadow: 0 14px 28px -16px rgba(0,0,0,.9); } $ .btn.p:hover { background: #fff; }
$ .btn.g, $ .btn.w { background: #1d1d20; color: var(--ink); box-shadow: 0 1px 0 rgba(255,255,255,.06) inset, 0 8px 18px -12px rgba(0,0,0,.8); }
$ .btn.g:hover, $ .btn.w:hover { background: #26262a; }
$ .lang, $ .thm { background: #1d1d20; } $ .lang a[aria-current], $ .toast, $ .totop, $ .skip, $ .qm::after { color: #111113; }
$ .ed button { background: #1d1d20; color: var(--ink2); } $ .ed button:hover { background: #26262a; color: var(--ink); }
$ .ed button[aria-selected="true"] { color: #111113; box-shadow: 0 12px 24px -14px rgba(0,0,0,.9); }
$ .tp-tiers li.on { color: rgba(17,17,19,.7); } $ .tp-tiers li.on b { color: #111113; }
$ .end .btn.p { background: var(--lime); color: var(--limeink); }
$ .end .btn.p:hover { background: #2a80ff; }
/* hero: a dark haze over the video instead of the light one */
$ .hbg { background: #111; }
$ .hbg::after { background: linear-gradient(180deg, rgba(11,11,13,.8) 0%, rgba(11,11,13,.35) 10%, rgba(11,11,13,0) 22%),
    radial-gradient(ellipse 58% 72% at 18% 64%, rgba(11,11,13,.9) 0%, rgba(11,11,13,.65) 48%, rgba(11,11,13,0) 100%),
    linear-gradient(0deg, #0b0b0d 0%, rgba(11,11,13,0) 30%); }
/* surfaces */
$ .win { box-shadow: 0 0 0 1px rgba(255,255,255,.06), 0 40px 80px -42px rgba(0,0,0,.9); }
$ .wires .w0 { stroke: #f2f2f4; } $ .k2 { color: #111113; }
$ .tri b, $ .pf { background: rgba(255,255,255,.07); }
$ .card2, $ .nd, $ .scn, $ .tc, $ .td, $ .pc, $ .dcard, $ .ct, $ .cm { box-shadow: 0 0 0 1px rgba(255,255,255,.06), 0 8px 18px -14px rgba(0,0,0,.8); }
$ .tp-sl input::-webkit-slider-runnable-track { background: linear-gradient(90deg, var(--lime) var(--tpp), #2c2c31 var(--tpp)); }
$ .tp-sl input::-moz-range-track { background: #2c2c31; }
$ .tp-sl input::-webkit-slider-thumb { background: #0b0b0d; } $ .tp-sl input::-moz-range-thumb { background: #0b0b0d; }
$ .qm { background: rgba(255,255,255,.1); }
$ .end { background: #1d1d20; color: var(--ink); box-shadow: 0 0 0 1px rgba(255,255,255,.06), 0 50px 90px -50px rgba(0,0,0,.9); }
$ .end h2 { color: var(--ink); } $ .end p { color: var(--ink2); }
$ footer { border-top-color: rgba(255,255,255,.08); }
$ .mnav { background: rgba(21,21,23,.97); }
$ .sf input, $ .sf textarea { background: var(--field); color: var(--ink); }
$ dialog.doc::backdrop { background: rgba(0,0,0,.6); }
$ .mb-strip, $ .nw-card { background-color: #1d1d20; }
@media (max-width: 760px) {
  $ .hbg::after { background: linear-gradient(180deg, rgba(11,11,13,.75) 0%, rgba(11,11,13,0) 18%),
    linear-gradient(0deg, rgba(11,11,13,1) 0%, rgba(11,11,13,.9) 38%, rgba(11,11,13,0) 72%); }
  $ .ed button[aria-selected="true"] { color: #111113; }
}
/* the switch: a round button next to EN/RU; the moon shows on the light page, the sun on the dark one */
.thm { flex: none; display: inline-grid; place-items: center; width: 36px; height: 36px; margin-left: 8px; padding: 0; border: 0; border-radius: 50%;
  background: var(--raised); box-shadow: var(--sh-sm); color: var(--ink); cursor: pointer; }
.thm:hover { color: var(--ink); background: var(--field); }
.thm svg { width: 17px; height: 17px; }
.thm .sun, .mthm .sun, .mthm .to-light, $ .thm .moon, $ .mthm .moon, $ .mthm .to-dark { display: none; } $ .thm .sun, $ .mthm .sun, $ .mthm .to-light { display: block; }
/* phones: no room in the bar, so the switch is a row in the menu instead */
.mthm { display: flex; align-items: center; gap: 10px; width: 100%; padding: 12px 14px; border: 0; border-radius: 14px; background: none;
  color: var(--ink); font: inherit; text-align: left; cursor: pointer; }
.mthm:hover { background: var(--field); } .mthm svg { width: 18px; height: 18px; flex: none; }
@media (max-width: 760px) { .nav .thm { display: none; } }
"""


def _scope(css):
    # every «$» is the dark-theme root; in a selector list each item carries its own «$»
    return css.replace('$', D)


DARK_CSS = _scope(_CSS)

SUN = ('<svg class="sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">'
       '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>')
MOON = ('<svg class="moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/></svg>')
SWITCH = f'<button type="button" class="thm" aria-pressed="false" aria-label="Тёмная тема">{MOON}{SUN}</button>'
MENU_SWITCH = f'<button type="button" class="mthm">{MOON}{SUN}<span class="to-dark">Тёмная тема</span><span class="to-light">Светлая тема</span></button>'

# applied in <head> before the first paint, so a stored dark choice never flashes light
EARLY = "try{if(localStorage.getItem('oneflow-theme')==='dark')document.documentElement.dataset.theme='dark'}catch(e){}"

JS = """<script>
// ☀/☾: light by default; the choice is stored under the app's key so /app opens in the same theme
(() => {
  const root = document.documentElement, meta = document.querySelector('meta[name="theme-color"]');
  const sync = () => { const dark = root.dataset.theme === 'dark';
    document.querySelectorAll('.thm').forEach((b) => b.setAttribute('aria-pressed', String(dark)));
    if (meta) meta.content = dark ? '#0b0b0d' : '#e5e5e5'; };
  document.querySelectorAll('.thm, .mthm').forEach((b) => b.addEventListener('click', () => {
    const dark = root.dataset.theme !== 'dark';
    if (dark) root.dataset.theme = 'dark'; else delete root.dataset.theme;
    try { localStorage.setItem('oneflow-theme', dark ? 'dark' : 'light'); } catch (e) {}
    sync(); }));
  sync();
})();
</script>
"""
