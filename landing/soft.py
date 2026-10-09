"""oneflow.art in the app's light theme «Soft» (src/ThemeSoft.css in the app repo): light-grey page, soft light
cards with a faint shadow, black pills for the main action and the active item, a flat blue accent #0a6cff, as in the app (marker under the key
words, slider, badges), thin large Geist headings and more air.

A layer over the v5 page (v5_ice.build(theme='soft')): the markup, texts, CMS keys, slider and the animated mode
windows stay the same — only tokens and a few rules change, so the dark «Ice» page can still be built from the same
source. The hero video stays the background of the first screen, under a light haze in the page colour.
"""

SOFT_CSS = """
/* ===================== «Soft» — the app's light theme ===================== */
:root { --bg: #e5e5e5; --ink: #2d2d2d; --ink2: #5b5b5b; --muted: #8f8f8f; --line: rgba(0,0,0,.07); --card: #f1f1f1; --raised: #f7f7f7; --field: #e7e7e7;
  --ac: #2b2b2b; --acink: #ffffff; --acsoft: rgba(10,108,255,.14); --lime: #0a6cff; --limeink: #ffffff; --olive: #0a5fe0;
  --s0: #f4f4f4; --s1: #fafafa; --s2: #ffffff; --s3: #e0e0e0; --dot: #d6d6d6; --ok: var(--olive); --green: var(--olive); --mint: rgba(10,108,255,.14);
  --dim: #ababab; --num: #2d2d2d;
  --sh: 0 1px 0 rgba(255,255,255,.9) inset, 0 22px 44px -30px rgba(0,0,0,.22); --sh-sm: 0 1px 0 rgba(255,255,255,.9) inset, 0 8px 18px -12px rgba(0,0,0,.22);
  --sh2: 0 1px 0 rgba(255,255,255,.9) inset, 0 34px 70px -40px rgba(0,0,0,.3);
  --d: 'Geist', system-ui, -apple-system, 'Segoe UI', sans-serif; --m: 'Geist', system-ui, -apple-system, 'Segoe UI', sans-serif; }
html { color-scheme: light; } body { background: var(--bg); color: var(--ink); }
.bgfx { display: none; } ::selection { background: var(--lime); color: var(--limeink); } :focus-visible { outline-color: var(--ink); }

/* buttons: pills, black for the main action */
.btn { border-radius: 999px; font-weight: 600; }
.btn.p { background: var(--ac); color: #fff; box-shadow: 0 14px 28px -16px rgba(0,0,0,.6); }
.btn.g, .btn.w { background: var(--raised); color: var(--ink); box-shadow: var(--sh-sm); backdrop-filter: none; -webkit-backdrop-filter: none; }
.btn.g:hover, .btn.w:hover { background: #fff; }

/* menu */
.nav .in { background: none; box-shadow: none; backdrop-filter: none; -webkit-backdrop-filter: none; }  /* no plate under the menu */
.nav nav a { color: var(--ink2); } .nav nav a:hover { color: var(--ink); } .nav .btn, .mnav .row .in2, .mnav .row a { border-radius: 999px; }
.lang { background: var(--raised); box-shadow: var(--sh-sm); border-radius: 999px; } .lang a { border-radius: 999px; color: var(--muted); }
.lang a:hover { color: var(--ink); } .lang a[aria-current] { background: var(--ac); color: #fff; }
.mnav { background: rgba(241,241,241,.97); border-radius: 24px; } .mnav a:hover { background: var(--field); }

/* hero: the video stays the background of the first screen; the headline, text and buttons sit on the left, over a
   light haze in the page colour on that side (and a band at the top for the menu) */
.hbg { background: #d4d4d4; }
.hbg::after { background: linear-gradient(180deg, rgba(229,229,229,.75) 0%, rgba(229,229,229,.3) 10%, rgba(229,229,229,0) 22%),
    radial-gradient(ellipse 58% 72% at 18% 64%, rgba(229,229,229,.92) 0%, rgba(229,229,229,.7) 48%, rgba(229,229,229,0) 100%); }
.hero .wrap { text-align: left; }
.hero h1 { max-width: 860px; margin-left: 0; margin-right: 0; font: 200 clamp(40px, 4.9vw, 70px)/1.03 var(--d); letter-spacing: -.045em; color: var(--ink); }
.hero h1 .gr { color: var(--ink); -webkit-text-fill-color: currentColor; font-weight: 300; background: none; }
.hero .sub { max-width: 560px; margin-left: 0; margin-right: 0; font-size: 18px; color: var(--ink2); }
.hero .acts { justify-content: flex-start; }
/* the headline block stays at the bottom of the first screen; the news cards follow right under the hero */
.hero { padding-top: 92px; }
.hero > .wrap { align-self: stretch; display: flex; flex-direction: column; justify-content: flex-end; }
.mrow { padding-top: 40px; } .models span { font-weight: 300; color: #9d9d9d; } .fnote { color: var(--muted); }

/* section heads */
.sh .k { display: inline-block; padding: 6px 13px; border-radius: 999px; background: var(--raised); box-shadow: var(--sh-sm);
  font: 500 13px var(--d); letter-spacing: 0; text-transform: none; color: var(--ink2); }
.sh h2 { margin-top: 16px; font-weight: 200; letter-spacing: -.045em; font-size: clamp(34px, 4.6vw, 60px); } .sh p { color: var(--ink2); }

/* modes: pills like the app, the active one black; the panel is a soft card */
.ed { display: flex; flex-wrap: wrap; justify-content: center; gap: 8px; max-width: 1000px; font: 500 15px/1 var(--d); letter-spacing: 0; }
.ed .dv { display: none; }
.ed button { padding: 13px 18px; border-radius: 999px; background: var(--raised); box-shadow: var(--sh-sm); color: var(--ink2); transition: background .2s, color .2s; }
.ed button:hover { color: var(--ink); background: #fff; }
.ed button[aria-selected="true"] { background: var(--ac); color: #fff; box-shadow: 0 12px 24px -14px rgba(0,0,0,.6); } .ed button[aria-selected="true"]::after { display: none; }
.mpanel { background: var(--card); border-radius: 32px; box-shadow: var(--sh2); }
.lt .eb { background: var(--raised); box-shadow: var(--sh-sm); color: var(--ink2); } .lt .eb i { background: var(--lime); color: var(--limeink); }
.lt h3 { font-weight: 200; letter-spacing: -.045em; } .lt .lead { color: var(--ink2); }
.bens b { font-weight: 600; color: var(--ink); } .bens span { font-weight: 600; color: var(--ink); } .bens small { color: var(--ink2); }

/* the animated app windows, light */
.win { background: var(--s1); box-shadow: 0 0 0 1px rgba(0,0,0,.05), 0 40px 80px -42px rgba(0,0,0,.4); }
.win .bar em { color: var(--ink2); } .win .bar em::before { color: #9cc21f; }
.cv .pb i, .fnl i, .wv i { background: var(--lime); }
.wires .w1, .wires .w2, .wires .w3, .wires .w4 { stroke: #2a80ff; } .wires .w0 { stroke: #2b2b2b; }
.scan { background: #2a80ff; } .pc.p2 { box-shadow: 0 0 0 2px var(--ink), 0 20px 50px -24px rgba(0,0,0,.35); }
.toast { background: var(--ac); color: #fff; box-shadow: 0 14px 30px -12px rgba(0,0,0,.5); } .k2 { background: var(--ac); color: var(--lime); }
.tri b, .pf { background: rgba(0,0,0,.06); } .pf.tiktok { color: #0b8f88; } .pf.instagram { color: #c0307f; } .pf.threads { color: #333; }
.pc .br i, .u em { background: #cfcfcf; } .cv .ty3 i { background: #bdbdbd; }
.card2, .nd, .scn, .tc, .td, .pc, .dcard, .ct, .cm { box-shadow: 0 0 0 1px rgba(0,0,0,.06), 0 8px 18px -14px rgba(0,0,0,.3); }

/* pricing */
.tpc { background: var(--card); border-radius: 32px; box-shadow: var(--sh2); }
.tp-usd { font-weight: 200; color: var(--ink); } .tp-get b { font-weight: 500; } .tp-get span { color: var(--muted); }
.tp-get em { background: var(--lime); color: var(--limeink); }
.tp-sl input::-webkit-slider-runnable-track { background: linear-gradient(90deg, var(--lime) var(--tpp), #d6d6d6 var(--tpp)); }
.tp-sl input::-moz-range-track { background: #d6d6d6; } .tp-sl input::-moz-range-progress { background: var(--lime); }
.tp-sl input::-webkit-slider-thumb { background: #fff; box-shadow: 0 0 0 6px var(--ac), 0 6px 16px rgba(0,0,0,.25); }
.tp-sl input::-moz-range-thumb { background: #fff; box-shadow: 0 0 0 6px var(--ac), 0 6px 16px rgba(0,0,0,.25); }
.tp-sl input:focus-visible::-webkit-slider-thumb { box-shadow: 0 0 0 6px var(--ac), 0 0 0 10px rgba(10,108,255,.3); }
.tp-sl input:focus-visible::-moz-range-thumb { box-shadow: 0 0 0 6px var(--ac), 0 0 0 10px rgba(10,108,255,.3); }
.tp-mk { font-family: var(--d); } .tp-mk .t { color: var(--ink2); } .tp-mk i { color: var(--olive); font-weight: 600; }
.tp-tiers li { background: var(--raised); box-shadow: var(--sh-sm); color: var(--muted); }
.tp-tiers li.on { background: var(--ac); color: rgba(255,255,255,.7); box-shadow: 0 12px 24px -14px rgba(0,0,0,.6); } .tp-tiers li.on b { color: #fff; }
.gens { background: var(--field); } .gens > span { color: var(--muted); font-family: var(--d); } .gens .nw { color: var(--muted); }
.gens .top { background: var(--lime); color: var(--limeink); } .qm { background: rgba(0,0,0,.08); color: var(--ink); } .qm::after { background: var(--ac); color: #fff; }
.tp-pts li { color: var(--ink2); } .tp-pts li::before { color: var(--olive); }
.tp-pts li.hl { background: var(--lime); color: var(--limeink); box-shadow: none; font-size: 15.5px; } .tp-pts li.hl::before { color: var(--limeink); }
.tp-acts .btn.w { background: var(--raised); color: var(--ink); box-shadow: var(--sh-sm); }

/* faq, closing card, footer, documents */
.faq details { background: var(--card); border-radius: 22px; box-shadow: var(--sh-sm); } .faq summary { font-weight: 500; } .faq details p { color: var(--ink2); }
.sup .btn { border-radius: 999px; }
.end { background: var(--ac); color: #fff; border-radius: 36px; box-shadow: 0 50px 90px -50px rgba(0,0,0,.6); }
.end h2 { font-weight: 200; letter-spacing: -.045em; color: #fff; } .end p { color: rgba(255,255,255,.62); }
.end .btn.p { background: var(--lime); color: var(--limeink); box-shadow: none; }
footer { border-top-color: rgba(0,0,0,.08); color: var(--muted); }
dialog.doc { background: var(--raised); color: var(--ink); border-radius: 26px; } dialog.doc .x { background: var(--field); color: var(--ink); border-radius: 50%; }
dialog.doc::backdrop { background: rgba(0,0,0,.35); } .sf input, .sf textarea { background: #fff; border-color: transparent; box-shadow: var(--sh-sm); }
.sf input:focus, .sf textarea:focus { border-color: var(--ink); } .totop { border-radius: 50%; background: var(--ac); color: #fff; } .skip { background: var(--ac); color: #fff; }

/* English headings in Origin Black Display (fonts.css); the Russian page keeps Geist, Origin has no Cyrillic */
html[lang="en"] .hero h1, html[lang="en"] .sh h2, html[lang="en"] .lt h3, html[lang="en"] .end h2 {
  font-family: 'Origin', var(--d); font-weight: 900; letter-spacing: 0; word-spacing: .12em; text-wrap: balance; }
html[lang="en"] .hero h1 { font-size: clamp(32px, 3.9vw, 54px); line-height: .98; text-transform: uppercase; letter-spacing: .01em; }
html[lang="en"] .sh h2 { font-size: clamp(30px, 4vw, 52px); line-height: 1.04; }
html[lang="en"] .lt h3 { font-size: clamp(28px, 3.2vw, 42px); line-height: 1.05; }

@media (max-width: 760px) {
  .hbg::after { background: linear-gradient(180deg, rgba(229,229,229,.7) 0%, rgba(229,229,229,0) 18%),
    linear-gradient(0deg, rgba(229,229,229,.97) 0%, rgba(229,229,229,.9) 38%, rgba(229,229,229,0) 72%); }
  .hero { padding-top: 84px; } .hero h1 { font-size: 10.5vw; } html[lang="en"] .hero h1 { font-size: 8vw; } .hero .acts { flex-direction: column; align-items: stretch; }
  .ed { flex-wrap: nowrap; justify-content: flex-start; gap: 8px; } .ed button { padding: 11px 15px; border-radius: 999px; background: var(--raised); box-shadow: var(--sh-sm); color: var(--ink2); }
  .ed button[aria-selected="true"] { background: var(--ac); color: #fff; }
  .mpanel { border-radius: 26px; } .tpc { border-radius: 26px; } .end { border-radius: 28px; }
}
"""


def apply(head):
    """Put the Soft layer last in the page styles and switch the browser colours to light."""
    head = head.replace('<meta name="theme-color" content="#090e12">', '<meta name="theme-color" content="#e5e5e5">')
    i = head.rindex('</style>')
    return head[:i] + SOFT_CSS + head[i:]
