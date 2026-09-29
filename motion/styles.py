"""Alternative looks for the ONEFLOW motion video. Same timeline and scenes, different art direction.

Enabled with ?s=<name> (adds body class s-<name>). Each block only overrides colours, type, textures and shapes.
"""

NAMES = {
    'swiss': 'Swiss — светлая типографика, красный акцент, жёсткие тени',
    'neon': 'Neon — чёрный фон, лайм и маджента, широкий шрифт, сканлайны',
    'pastel': 'Pastel — светлая, как лендинг: лаванда, мята, мягкие тени',
    'acid': 'Acid — яркий градиент, жёлтые акценты, стикерные карточки',
    'blue': 'Blueprint — техно-чертёж: синяя сетка, циан, моноширинный',
}

HEAD = '.s1 .wm, .s2 .w, .s2 .all, .s3 .num, .s3 .lbl, .s4 .ttl, .s5 h2, .s6 .ttl, .s7 .big, .s7 .sub, .s7 h3, .s8 .wm, .s8 h2, .ring .c b'


def scoped(name, css):
    return css.replace('@', '.s-' + name + ' ')


CSS = scoped('swiss', """
/* ---------- Swiss ---------- */
.s-swiss { --bg: #f2f0eb; --t: #111; --m: #6d6a63; --gr: none; --d-: 'Inter Tight', sans-serif; }
@.bg, @.grain, @.vig { display: none; } .s-swiss #st::before { content: ''; position: absolute; inset: 0; background: repeating-linear-gradient(90deg, rgba(17,17,17,.08) 0 1px, transparent 1px 160px); }
@.gt { background: none; color: #ff3b1f; } @.mk path { fill: #111; } @.s1 .glow { background: radial-gradient(circle, rgba(255,59,31,.28), transparent 60%); }
@.s2 .w { font-size: 300px; letter-spacing: -.075em; } @.s2 .all { letter-spacing: -.07em; }
@.hud { color: rgba(17,17,17,.6); } @.hud .l { color: #111; } @.hud .p { background: rgba(0,0,0,.12); border-radius: 0; } @.hud .p i { background: #ff3b1f; }
@.fl { background: #ff3b1f !important; } @.bar { height: 16px; border-radius: 0; background: #111; }
@.chip { background: #fff; color: #111; border-radius: 0; box-shadow: inset 0 0 0 2px #111; } @.chip i { border-radius: 0; background: #ff3b1f !important; } @.r0, @.r3 { opacity: .3; filter: none; }
@.s3 .ctr { background: radial-gradient(ellipse 62% 58% at center, rgba(242,240,235,.98) 40%, rgba(242,240,235,.78) 60%, transparent 80%); }
@.s4 .grid { background: linear-gradient(rgba(0,0,0,.07) 1px, transparent 1px) 0 0 / 60px 60px, linear-gradient(90deg, rgba(0,0,0,.07) 1px, transparent 1px) 0 0 / 60px 60px; }
@.nd, @.pn { background: #fff; color: #111; border-radius: 0; box-shadow: 0 0 0 3px #111, 12px 12px 0 #111; } @.nd .h { border-bottom-color: #111; } @.nd .h b, @.pn .k i { border-radius: 0; }
@.fm span { background: #f2f0eb; border-radius: 0; box-shadow: inset 0 0 0 1.5px #111; } @.go { background: #ff3b1f; color: #fff; border-radius: 0; }
@.edg path { stroke: #111; } @.edg .e2 { stroke: #ff3b1f; filter: none; } @.port0 { box-shadow: none; }
@.fr { border-radius: 0; box-shadow: 0 0 0 3px #111, 10px 10px 0 #111; } @.fl2 { background: #111; color: #fff; border-radius: 0; } @.pill { background: #111; color: #fff; border-radius: 0; box-shadow: none; }
@.s5 .sh { background: linear-gradient(90deg, rgba(242,240,235,.98) 24%, rgba(242,240,235,.62) 50%, transparent 72%); } @.s5 .k { color: #ff3b1f; } @.s5 p { color: #333; } @.wc { border-radius: 0; box-shadow: 0 0 0 3px #111; }
@.tr small { color: #6d6a63; } @.tr em { color: #ff3b1f; } @.tr > i, @.cp2 i { border-radius: 0; } @.bub { background: #111; color: #fff; border-radius: 0; } @.ty { color: #111; } @.ty.tyc::after { color: #ff3b1f; }
@.win { background: #ff3b1f; color: #fff; border-radius: 0; } @.sr .t { background: rgba(0,0,0,.1); border-radius: 0; } @.sr .t i { background: #111; border-radius: 0; } @.sr.best b, @.sr.best span { color: #ff3b1f; }
@.ring .bgc { stroke: rgba(0,0,0,.1); } @.ring .fg { stroke: #ff3b1f; stroke-linecap: butt; } @.ring .c small { color: #6d6a63; } @.s7 .rt2 p { color: #333; }
@.s8 .btn { background: #ff3b1f; color: #fff; border-radius: 0; } @.s8 .url { border-radius: 0; box-shadow: inset 0 0 0 3px #111; } @.s8 .fn { color: rgba(0,0,0,.5); } @.end { background: #f2f0eb; }
""") + scoped('neon', """
/* ---------- Neon ---------- */
.s-neon { --bg: #040404; --t: #effff0; --m: #7d8a7f; --gr: linear-gradient(95deg, #d7ff3d 20%, #3dffc8 60%, #3dc8ff); --d-: 'Unbounded', sans-serif; }
@.bg .a { background: #2c4d00 !important; } @.bg .b { background: #5a0a4c !important; } @.bg .c { background: #003a44 !important; }
@.vig { background: repeating-linear-gradient(0deg, rgba(0,0,0,.3) 0 2px, transparent 2px 5px), radial-gradient(ellipse at center, transparent 50%, rgba(0,0,0,.75)); }
@.mk path { fill: #d7ff3d; } @.s1 .glow { background: radial-gradient(circle, rgba(215,255,61,.45), transparent 60%); }
@.s1 .wm, @.s8 .wm { font-size: 118px; } @.s2 .w { font-size: 190px; } @.s2 .all { font-size: 118px; } @.s3 .num { font-size: 300px; } @.s3 .lbl { font-size: 50px; } @.s4 .ttl { font-size: 62px; }
@.s5 h2 { font-size: 128px; } @.s6 .ttl { font-size: 58px; } @.s7 .big { font-size: 320px; } @.s7 .sub { font-size: 48px; } @.s7 .rt2 h3 { font-size: 82px; } @.s8 h2 { font-size: 70px; } @.ring .c b { font-size: 96px; }
@.hud { color: #b6ff3d; } @.hud .p i { background: #d7ff3d; } @.s2 .fl:nth-of-type(odd) { background: #d7ff3d !important; } @.s2 .fl:nth-of-type(even) { background: #ff2bd6 !important; }
@.bar { background: linear-gradient(90deg, #d7ff3d, #3dffc8); box-shadow: 0 0 30px #d7ff3d; }
@.chip { background: transparent; color: #d7ff3d; border-radius: 6px; box-shadow: inset 0 0 0 2px rgba(215,255,61,.5); font-family: 'JetBrains Mono', monospace; } @.chip i { background: #ff2bd6 !important; }
@.s3 .ctr { background: radial-gradient(ellipse 62% 58% at center, rgba(4,4,4,.98) 38%, rgba(4,4,4,.7) 58%, transparent 80%); } @.s4 .grid { background: radial-gradient(rgba(215,255,61,.2) 1.6px, transparent 2px) 0 0 / 36px 36px; }
@.nd, @.pn { background: #070907; border-radius: 8px; box-shadow: inset 0 0 0 2px #d7ff3d, 0 0 50px rgba(215,255,61,.22); font-family: 'JetBrains Mono', monospace; } @.nd .h { border-bottom-color: rgba(215,255,61,.25); font-family: 'JetBrains Mono', monospace; }
@.fm span { background: #0f140a; border-radius: 4px; box-shadow: inset 0 0 0 1px rgba(215,255,61,.35); font-family: 'JetBrains Mono', monospace; } @.go { background: #d7ff3d; color: #050505; border-radius: 6px; font-family: 'JetBrains Mono', monospace; }
@.edg path { stroke: #d7ff3d; } @.edg .e2 { stroke: #ff2bd6; filter: drop-shadow(0 0 12px #ff2bd6); }
@.fr { border-radius: 6px; box-shadow: 0 0 0 2px #ff2bd6, 0 0 40px rgba(255,43,214,.45); } @.fl2 { background: #050505; color: #d7ff3d; } @.pill { background: transparent; color: #d7ff3d; box-shadow: inset 0 0 0 2px #d7ff3d; font-family: 'JetBrains Mono', monospace; }
@.s5 .sh { background: linear-gradient(90deg, rgba(4,4,4,.97) 24%, rgba(4,4,4,.5) 52%, transparent 72%); } @.s5 .k { color: #ff2bd6; } @.wc { border-radius: 8px; box-shadow: 0 0 0 2px rgba(215,255,61,.6); }
@.pn .k { font-family: 'JetBrains Mono', monospace; } @.tr em { color: #d7ff3d; } @.bub { background: #d7ff3d; color: #050505; border-radius: 6px; } @.ty.tyc::after { color: #ff2bd6; }
@.win { background: #ff2bd6; color: #fff; } @.sr .t i { background: linear-gradient(90deg, #3dffc8, #d7ff3d); } @.sr.best b, @.sr.best span { color: #d7ff3d; }
@.ring .bgc { stroke: rgba(215,255,61,.12); } @.ring .fg { stroke: #d7ff3d; filter: drop-shadow(0 0 14px #d7ff3d); }
@.s8 .btn { background: #d7ff3d; color: #050505; border-radius: 8px; } @.s8 .url { color: #ff2bd6; border-radius: 8px; box-shadow: inset 0 0 0 2px #ff2bd6; }
""") + scoped('pastel', """
/* ---------- Pastel ---------- */
.s-pastel { --bg: #f7f5fb; --t: #15151a; --m: #7b7b88; --gr: linear-gradient(95deg, #15151a 20%, #3e6d63 58%, #5c5f9a); }
@.bg i { mix-blend-mode: multiply; filter: blur(120px); opacity: .95 !important; } @.bg .a { background: #dccfff !important; } @.bg .b { background: #c9f2de !important; } @.bg .c { background: #ffe3cf !important; }
@.grain { opacity: .035; } @.vig { display: none; } @.mk path { fill: #15151a; } @.s1 .glow { background: radial-gradient(circle, rgba(190,170,255,.55), transparent 60%); }
@.hud { color: rgba(21,21,26,.55); } @.hud .l { color: #15151a; } @.hud .p { background: rgba(0,0,0,.08); }
@.s2 .fl:nth-of-type(1) { background: #b9a6ff !important; } @.s2 .fl:nth-of-type(2) { background: #8fe3bf !important; } @.s2 .fl:nth-of-type(3) { background: #ffc3a0 !important; } @.s2 .fl:nth-of-type(4) { background: #a9c6ff !important; }
@.chip { background: #fff; color: #15151a; box-shadow: 0 12px 30px -14px rgba(20,20,40,.35), inset 0 0 0 1px rgba(0,0,0,.05); } @.r0, @.r3 { opacity: .45; }
@.s3 .ctr { background: radial-gradient(ellipse 62% 58% at center, rgba(247,245,251,.97) 38%, rgba(247,245,251,.7) 58%, transparent 80%); } @.s4 .grid { background: radial-gradient(rgba(0,0,0,.13) 1.6px, transparent 2px) 0 0 / 36px 36px; }
@.nd, @.pn { background: rgba(255,255,255,.9); color: #15151a; box-shadow: 0 1px 2px rgba(0,0,0,.05), 0 40px 80px -30px rgba(40,40,80,.35); } @.nd .h { border-bottom-color: rgba(0,0,0,.06); }
@.fm span { background: #f3f2f7; box-shadow: inset 0 0 0 1px rgba(0,0,0,.06); } @.fm em { color: #999; } @.go { background: #15151a; color: #fff; }
@.edg path { stroke: rgba(0,0,0,.35); } @.edg .e2 { stroke: #8b6cff; filter: none; } @.port0 { background: #15151a; box-shadow: 0 0 0 4px #fff; }
@.fr { box-shadow: 0 30px 60px -20px rgba(40,40,80,.45); } @.fl2 { background: rgba(255,255,255,.92); color: #15151a; } @.pill { background: #fff; color: #15151a; box-shadow: 0 12px 30px -14px rgba(20,20,40,.35); }
@.s5 .sh { background: linear-gradient(90deg, rgba(247,245,251,.97) 24%, rgba(247,245,251,.6) 52%, transparent 72%); } @.s5 .k { color: #e0612b; } @.s5 p { color: #3c3c46; }
@.tr small { color: #8a8a96; } @.tr em { color: #16a36a; } @.bub { background: #15151a; color: #fff; } @.ty { color: #15151a; } @.sr .t { background: rgba(0,0,0,.07); } @.sr.best b, @.sr.best span { color: #16a36a; }
@.ring .bgc { stroke: #e2f1e9; } @.ring .c small { color: #7b7b88; } @.s7 .rt2 p { color: #3c3c46; }
@.s8 .btn { background: #15151a; color: #fff; } @.s8 .url { box-shadow: inset 0 0 0 2px rgba(0,0,0,.15); } @.s8 .fn { color: rgba(0,0,0,.45); } @.end { background: #f7f5fb; }
""") + scoped('acid', f"""
/* ---------- Acid ---------- */
.s-acid {{ --bg: #ff4d1f; --t: #fff; --m: rgba(255,255,255,.8); --gr: none; --d-: 'Dela Gothic One', sans-serif; }}
.s-acid #st {{ background: linear-gradient(120deg, #ff5a1f, #ff2e88 50%, #6b2bff); }}
@.bg i {{ opacity: .6 !important; }} @.bg .a {{ background: #ffe14d !important; }} @.bg .b {{ background: #2bd9ff !important; }} @.bg .c {{ background: #ff2e88 !important; }} @.vig {{ display: none; }} @.grain {{ opacity: .12; }}
{', '.join('.s-acid ' + h for h in HEAD.split(', '))} {{ font-weight: 400; }}
@.s1 .wm, @.s8 .wm {{ font-size: 124px; }} @.s2 .w {{ font-size: 210px; }} @.s2 .all {{ font-size: 128px; }} @.s3 .num {{ font-size: 320px; }} @.s3 .lbl {{ font-size: 50px; }} @.s4 .ttl {{ font-size: 66px; }}
@.s5 h2 {{ font-size: 136px; }} @.s6 .ttl {{ font-size: 60px; }} @.s7 .big {{ font-size: 330px; }} @.s7 .sub {{ font-size: 50px; }} @.s7 .rt2 h3 {{ font-size: 86px; }} @.s8 h2 {{ font-size: 76px; }} @.ring .c b {{ font-size: 100px; }}
@.gt {{ background: none; color: #ffe14d; }} @.mk path {{ fill: #fff; }} @.s1 .glow {{ background: radial-gradient(circle, rgba(255,225,77,.6), transparent 60%); }}
@.hud {{ color: #fff; }} @.hud .p {{ background: rgba(255,255,255,.3); }} @.hud .p i {{ background: #ffe14d; }}
@.s2 .fl:nth-of-type(1) {{ background: #ffe14d !important; }} @.s2 .fl:nth-of-type(2) {{ background: #2bd9ff !important; }} @.s2 .fl:nth-of-type(3) {{ background: #fff !important; }} @.s2 .fl:nth-of-type(4) {{ background: #111 !important; }}
@.bar {{ background: #ffe14d; height: 14px; }} @.chip {{ background: #fff; color: #111; border-radius: 99px; box-shadow: 0 8px 0 #111; }} @.r0, @.r3 {{ opacity: .55; filter: none; }}
@.s3 .ctr {{ background: radial-gradient(ellipse 62% 58% at center, rgba(255,46,136,.96) 38%, rgba(255,46,136,.6) 58%, transparent 80%); }} @.s4 .grid {{ background: radial-gradient(rgba(255,255,255,.3) 1.6px, transparent 2px) 0 0 / 36px 36px; }}
@.nd, @.pn {{ background: #fff; color: #111; border-radius: 36px; box-shadow: 0 14px 0 #111; }} @.nd .h {{ border-bottom-color: rgba(0,0,0,.08); }} @.fm span {{ background: #f1f1f1; box-shadow: none; }} @.fm em {{ color: #888; }}
@.go {{ background: #111; color: #ffe14d; }} @.edg path {{ stroke: #fff; }} @.edg .e2 {{ stroke: #ffe14d; filter: none; }}
@.fr {{ border-radius: 24px; box-shadow: 0 12px 0 #111; }} @.fl2 {{ background: #111; color: #ffe14d; }} @.pill {{ background: #ffe14d; color: #111; box-shadow: 0 8px 0 #111; }}
@.s5 .sh {{ background: linear-gradient(90deg, rgba(255,70,60,.95) 22%, rgba(255,60,110,.55) 50%, transparent 72%); }} @.s5 .k {{ color: #ffe14d; }} @.s5 p {{ color: #fff; }} @.wc {{ border-radius: 28px; box-shadow: 0 12px 0 #111; }}
@.tr small {{ color: #777; }} @.tr em {{ color: #ff2e88; }} @.bub {{ background: #111; color: #fff; }} @.ty {{ color: #111; }} @.win {{ background: #ffe14d; color: #111; }}
@.sr .t {{ background: #eee; }} @.sr .t i {{ background: linear-gradient(90deg, #ff5a1f, #ff2e88); }} @.sr span, @.sr b {{ color: #111; }} @.sr.best b, @.sr.best span {{ color: #ff2e88; }}
@.ring .bgc {{ stroke: rgba(255,255,255,.25); }} @.ring .fg {{ stroke: #ffe14d; }} @.ring .c small {{ color: #fff; }} @.s7 .rt2 p {{ color: #fff; }}
@.s8 .btn {{ background: #ffe14d; color: #111; box-shadow: 0 10px 0 #111; }} @.s8 .url {{ box-shadow: inset 0 0 0 3px #fff; }} @.s8 .fn {{ color: rgba(255,255,255,.75); }}
""") + scoped('blue', """
/* ---------- Blueprint ---------- */
.s-blue { --bg: #0a1a3a; --t: #e8f0ff; --m: #7f9bd1; --gr: linear-gradient(95deg, #ffffff 30%, #5ce1ff); --d-: 'IBM Plex Sans', sans-serif; }
.s-blue #st::before { content: ''; position: absolute; inset: 0; background: linear-gradient(rgba(92,225,255,.18) 1px, transparent 1px) 0 0 / 240px 240px, linear-gradient(90deg, rgba(92,225,255,.18) 1px, transparent 1px) 0 0 / 240px 240px,
  linear-gradient(rgba(92,225,255,.07) 1px, transparent 1px) 0 0 / 48px 48px, linear-gradient(90deg, rgba(92,225,255,.07) 1px, transparent 1px) 0 0 / 48px 48px; }
@.bg { display: none; } @.grain { opacity: .03; } @.vig { background: radial-gradient(ellipse at center, transparent 55%, rgba(3,10,26,.7)); }
@.mk path { fill: #5ce1ff; } @.s1 .glow { background: radial-gradient(circle, rgba(92,225,255,.35), transparent 60%); }
@.hud { color: #5ce1ff; font-family: 'IBM Plex Mono', monospace; } @.hud .p { border-radius: 0; } @.hud .p i { background: #5ce1ff; }
@.fl { background: #5ce1ff !important; } @.bar { background: #5ce1ff; height: 4px; border-radius: 0; }
@.chip { background: rgba(10,26,58,.85); color: #e8f0ff; border-radius: 2px; box-shadow: inset 0 0 0 1.5px #5ce1ff; font-family: 'IBM Plex Mono', monospace; } @.chip i { border-radius: 0; background: #5ce1ff !important; }
@.s3 .ctr { background: radial-gradient(ellipse 62% 58% at center, rgba(10,26,58,.97) 38%, rgba(10,26,58,.7) 58%, transparent 80%); } @.s4 .grid { display: none; }
@.nd, @.pn { background: rgba(10,26,58,.88); border-radius: 4px; box-shadow: inset 0 0 0 1.5px #5ce1ff, 0 30px 60px -30px rgba(0,0,0,.8); font-family: 'IBM Plex Mono', monospace; }
@.nd .h { border-bottom: 1.5px dashed rgba(92,225,255,.4); font-family: 'IBM Plex Mono', monospace; } @.nd .h b { border-radius: 2px; }
@.fm span { background: transparent; border-radius: 2px; box-shadow: inset 0 0 0 1px rgba(92,225,255,.45); font-family: 'IBM Plex Mono', monospace; } @.go { background: #5ce1ff; color: #0a1a3a; border-radius: 2px; }
@.edg path { stroke: #5ce1ff; } @.edg .e2 { stroke: #fff; filter: drop-shadow(0 0 8px #5ce1ff); }
@.fr { border-radius: 2px; box-shadow: 0 0 0 1.5px #5ce1ff, 0 30px 60px -30px rgba(0,0,0,.8); } @.fl2 { background: #0a1a3a; color: #5ce1ff; border-radius: 0; }
@.pill { background: rgba(10,26,58,.8); border-radius: 2px; box-shadow: inset 0 0 0 1.5px #5ce1ff; font-family: 'IBM Plex Mono', monospace; }
@.s5 .sh { background: linear-gradient(90deg, rgba(10,26,58,.97) 24%, rgba(10,26,58,.55) 52%, transparent 72%); } @.s5 .k { color: #5ce1ff; } @.wc { border-radius: 4px; box-shadow: 0 0 0 1.5px #5ce1ff; }
@.pn .k { font-family: 'IBM Plex Mono', monospace; } @.tr em { color: #5ce1ff; } @.tr > i, @.cp2 i { border-radius: 2px; } @.bub { background: #5ce1ff; color: #0a1a3a; border-radius: 2px; }
@.win { background: #5ce1ff; color: #0a1a3a; border-radius: 2px; } @.sr .t { border-radius: 0; } @.sr .t i { background: #5ce1ff; border-radius: 0; } @.sr.best b, @.sr.best span { color: #5ce1ff; }
@.ring .bgc { stroke: rgba(92,225,255,.15); } @.ring .fg { stroke: #5ce1ff; stroke-linecap: butt; }
@.s8 .btn { background: #5ce1ff; color: #0a1a3a; border-radius: 2px; } @.s8 .url { color: #5ce1ff; border-radius: 2px; box-shadow: inset 0 0 0 1.5px #5ce1ff; } @.end { background: #0a1a3a; }
""")
