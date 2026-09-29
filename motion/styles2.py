"""Unusual looks for the ONEFLOW motion video: hand-drawn, retro OS, risograph, CRT terminal, paper collage.

Same timeline as the base video; ?s=<name>. On top of colour/type overrides these use SVG filters (#rough — "boiling"
hand-drawn lines, re-seeded by seek() at 8 fps; #torn — ripped paper edges), a doodle layer drawn on stroke by stroke
(hand-drawn only), duotone / phosphor image treatments, bevels, scanlines and ransom-note lettering.
"""

NAMES = {
    'hand': 'Hand-drawn — тетрадный лист, маркер, рисованные дудлы, «дрожащие» линии',
    'os': 'Retro OS — окна старой системы, бевел-кнопки, пиксельный шрифт, синий экран вместо вспышек',
    'riso': 'Risograph — двухцветная печать розовый + синий, сдвиг слоёв, растр, зерно',
    'crt': 'CRT terminal — зелёный люминофор, пиксельный шрифт, сканлайны, мерцание',
    'collage': 'Collage — крафт-бумага, рваные края, скотч, буквы-вырезки',
}

HEAD = ['.s1 .wm', '.s2 .w', '.s2 .all', '.s3 .num', '.s3 .lbl', '.s4 .ttl', '.s5 h2', '.s6 .ttl', '.s7 .big', '.s7 .sub', '.s7 h3', '.s8 .wm', '.s8 h2', '.ring .c b']


def sizes(name, px):
    """px: dict selector → font-size."""
    return '\n'.join(f'.s-{name} {k} {{ font-size: {v}px; }}' for k, v in px.items())


def heads(name, rule):
    return ', '.join(f'.s-{name} {h}' for h in HEAD) + ' { ' + rule + ' }'


def sc(name, css):
    return css.replace('@', '.s-' + name + ' ')


SZ = lambda **kw: {'.s1 .wm': kw.get('wm'), '.s8 .wm': kw.get('wm'), '.s2 .w': kw['w'], '.s2 .all': kw['all'], '.s3 .num': kw['num'], '.s3 .lbl': kw['lbl'], '.s4 .ttl': kw['ttl'],  # noqa: E731
                   '.s5 h2': kw['h2'], '.s6 .ttl': kw['ttl2'], '.s7 .big': kw['big'], '.s7 .sub': kw['sub'], '.s7 .rt2 h3': kw['h3'], '.s8 h2': kw['end'], '.ring .c b': kw['ring']}

INK = '#1d1d1f'

HAND = sc('hand', f"""
/* ---------- Hand-drawn ---------- */
.s-hand {{ --bg: #fbf8f1; --t: {INK}; --m: #6b6558; --gr: none; --d-: 'Caveat', cursive; }}
.s-hand #st::before {{ content: ''; position: absolute; inset: 0; background: linear-gradient(90deg, transparent 150px, rgba(226,85,62,.5) 150px 153px, transparent 153px), linear-gradient(rgba(80,130,200,.17) 1.5px, transparent 1.5px) 0 0 / 100% 44px; }}
@.bg, @.vig, @.s1 .glow, @.s4 .grid {{ display: none; }} @.grain {{ opacity: .14; mix-blend-mode: multiply; }} @.dds {{ display: block; }}
@.gt {{ background: linear-gradient(transparent 56%, #ffe45c 56%, #ffe45c 90%, transparent 90%); -webkit-background-clip: border-box; background-clip: border-box; color: {INK}; padding: 0 .06em; }}
@.mk {{ filter: url(#rough); }} @.mk path {{ fill: #ffe45c; stroke: {INK}; stroke-width: 2.4; stroke-linejoin: round; }} @.s1 .tg {{ font: 400 34px 'Pangolin', cursive; color: #6b6558; }}
@.nd, @.pn, @.chip, @.pill, @.fm, @.go, @.bub, @.tr, @.sr, @.fl2, @.hud, @.s5 p, @.s5 .k, @.s7 .rt2 p, @.s8 .btn, @.s8 .url, @.ring .c small, @.s8 .fn {{ font-family: 'Pangolin', cursive; }}
@.nd, @.pn {{ background: transparent; color: {INK}; box-shadow: none; isolation: isolate; }}
@.nd::before, @.pn::before {{ content: ''; position: absolute; inset: 0; z-index: -1; border-radius: 22px 18px 26px 16px; background: #fffdf8; box-shadow: 0 0 0 3.5px {INK}, 11px 11px 0 rgba(29,29,31,.16); filter: url(#rough); }}
@.nd .h {{ background: none; border-bottom: 3px solid {INK}; }} @.nd .h b {{ background: #fff !important; color: {INK} !important; box-shadow: 0 0 0 2.5px {INK}; }}
@.fm span {{ background: #fff; border-radius: 10px; box-shadow: inset 0 0 0 2.5px {INK}; }} @.fm em {{ color: #6b6558; }}
@.go {{ background: #ffe45c; color: {INK}; box-shadow: inset 0 0 0 3.5px {INK}; filter: url(#rough); }}
@.edg {{ filter: url(#rough); }} @.edg path {{ stroke: {INK}; stroke-width: 4.5; }} @.edg .e2 {{ stroke: #e2553e; filter: none; }} @.port0 {{ background: {INK}; box-shadow: none; }}
@.chip {{ background: #fff; color: {INK}; border-radius: 30px 22px 28px 20px; box-shadow: inset 0 0 0 3px {INK}; filter: url(#rough); }} @.chip i {{ background: #ffe45c !important; box-shadow: 0 0 0 2px {INK}; }}
@.r0, @.r3 {{ opacity: .35; filter: url(#rough); }}
@.s3 .ctr {{ background: radial-gradient(ellipse 58% 52% at center, rgba(251,248,241,.98) 40%, rgba(251,248,241,.8) 60%, transparent 80%); }}
@.fr {{ overflow: hidden; border-radius: 3px; box-shadow: 0 0 0 10px #fff, 0 0 0 12px rgba(0,0,0,.1), 8px 16px 22px 10px rgba(0,0,0,.18); rotate: -2deg; }} @.fr:nth-child(even) {{ rotate: 2.5deg; }}
@.fl2 {{ background: #fff; color: {INK}; box-shadow: 0 0 0 2px {INK}; }}
@.pill {{ background: #9ef0c7; color: {INK}; box-shadow: inset 0 0 0 3px {INK}; filter: url(#rough); }}
@.wc {{ position: relative; border-radius: 3px; box-shadow: 0 0 0 10px #fff, 10px 18px 26px 10px rgba(0,0,0,.22); }} @.wc::after {{ content: ''; position: absolute; left: 50%; top: -24px; width: 110px; height: 34px; margin-left: -55px; background: rgba(158,240,199,.8); rotate: 4deg; }}
@.col:nth-child(even) .wc::after {{ background: rgba(255,228,92,.8); rotate: -5deg; }}
@.s5 .sh {{ background: linear-gradient(90deg, rgba(251,248,241,.98) 28%, rgba(251,248,241,.7) 50%, transparent 72%); }} @.s5 .k {{ color: #e2553e; font-size: 34px; }} @.s5 p {{ color: #3a3a3a; font-size: 46px; }}
@.pn .k i {{ box-shadow: 0 0 0 2px {INK}; }} @.tr small {{ color: #6b6558; }} @.tr em {{ color: #e2553e; font: 700 46px 'Caveat', cursive; }} @.tr > i, @.cp2 i {{ box-shadow: 0 0 0 5px #fff, 0 0 0 7.5px {INK}; border-radius: 4px; }}
@.bub {{ background: #ffe45c; color: {INK}; box-shadow: inset 0 0 0 3px {INK}; }} @.ty {{ color: {INK}; font: 700 40px/1.15 'Caveat', cursive; }} @.ty.tyc::after {{ content: ' ✎'; color: #e2553e; }}
@.win {{ background: #e2553e; color: #fff; font: 700 26px 'Caveat', cursive; }} @.sr .t {{ background: transparent; box-shadow: inset 0 0 0 2.5px {INK}; }}
@.sr .t i {{ background: repeating-linear-gradient(45deg, {INK} 0 3px, transparent 3px 8px); }} @.sr.best .t i {{ background: repeating-linear-gradient(45deg, #e2553e 0 3px, transparent 3px 8px); }} @.sr.best b, @.sr.best span {{ color: #e2553e; }}
@.ring svg {{ filter: url(#rough); }} @.ring .bgc {{ stroke: rgba(29,29,31,.1); }} @.ring .fg {{ stroke: {INK}; }} @.ring .c small {{ color: #6b6558; }} @.s7 .rt2 p {{ color: #3a3a3a; font-size: 44px; }}
@.s8 .btn {{ background: #ffe45c; color: {INK}; box-shadow: inset 0 0 0 3.5px {INK}; filter: url(#rough); }} @.s8 .url {{ box-shadow: inset 0 0 0 3.5px {INK}; filter: url(#rough); }} @.s8 .fn {{ color: rgba(0,0,0,.5); }} @.end {{ background: #fbf8f1; }}
@.hud {{ color: #6b6558; }} @.hud .l {{ color: {INK}; font: 700 38px 'Caveat', cursive; }} @.hud .p {{ background: rgba(0,0,0,.1); filter: url(#rough); }} @.hud .p i {{ background: {INK}; }}
@.fl {{ background: #ffe45c !important; }} @.bar {{ height: 9px; background: {INK}; filter: url(#rough); }}
""") + heads('hand', 'letter-spacing: -.005em; font-weight: 700;') + '\n' + sizes('hand', SZ(wm=210, w=330, all=210, num=440, lbl=90, ttl=112, h2=210, ttl2=104, big=470, sub=84, h3=150, end=128, ring=150))

BEV = 'inset -3px -3px 0 #404040, inset 3px 3px 0 #fff, inset -6px -6px 0 #808080, inset 6px 6px 0 #dfdfdf'
OS = sc('os', f"""
/* ---------- Retro OS ---------- */
.s-os {{ --bg: #008080; --t: #fff; --m: #d7f0f0; --gr: none; --d-: 'OSDigits', 'Pixelify Sans', sans-serif; }}
.s-os #st::before {{ content: ''; position: absolute; inset: 0; background: radial-gradient(rgba(255,255,255,.07) 1px, transparent 1.5px) 0 0 / 8px 8px; }}
@.bg, @.vig, @.s1 .glow {{ display: none; }} @.grain {{ opacity: .04; }} @.mk {{ filter: drop-shadow(8px 8px 0 #004040); }} @.mk path {{ fill: #fff; }}
@.gt {{ background: none; color: #fff200; }}
@.nd, @.pn, @.chip, @.pill, @.fm, @.go, @.bub, @.tr, @.sr, @.fl2, @.hud, @.s5 p, @.s5 .k, @.s7 .rt2 p, @.s8 .btn, @.s8 .url, @.ring .c small, @.s1 .tg, @.ty, @.s8 .fn {{ font-family: 'OSDigits', 'Pixelify Sans', sans-serif; }}
@.nd, @.pn {{ background: #c0c0c0; color: #000; border-radius: 0; box-shadow: {BEV}, 14px 14px 0 rgba(0,0,0,.35); }}
@.nd .h {{ margin: 6px 6px 0; padding: 10px 14px; border: 0; background: linear-gradient(90deg, #000080, #1084d0); color: #fff; }}
@.pn .k {{ margin: -24px -24px 20px; padding: 10px 14px; background: linear-gradient(90deg, #000080, #1084d0); color: #fff; }}
@.nd .h::after, @.pn .k::after {{ content: '_ □ ×'; margin-left: auto; padding: 0 8px; background: #c0c0c0; color: #000; box-shadow: inset -2px -2px 0 #404040, inset 2px 2px 0 #fff; letter-spacing: 6px; font-size: 18px; }}
@.nd .h b {{ background: #c0c0c0 !important; color: #000080 !important; border-radius: 0; }} @.pn .k i {{ border-radius: 0; box-shadow: 0 0 0 2px #fff; }}
@.fm span {{ background: #fff; border-radius: 0; box-shadow: inset 2px 2px 0 #808080, inset 3px 3px 0 #404040, inset -2px -2px 0 #dfdfdf; }} @.fm em {{ color: #000; }}
@.go {{ background: #c0c0c0; color: #000; border-radius: 0; box-shadow: {BEV}; }}
@.edg path {{ stroke: #fff; }} @.edg .e2 {{ stroke: #fff200; filter: none; }}
@.chip {{ background: #c0c0c0; color: #000; border-radius: 0; box-shadow: {BEV}; }} @.chip i {{ border-radius: 0; }} @.r0, @.r3 {{ opacity: .5; filter: none; }}
@.s3 .ctr {{ background: radial-gradient(ellipse 58% 52% at center, rgba(0,128,128,.97) 40%, rgba(0,128,128,.75) 60%, transparent 80%); }} @.s4 .grid {{ background: radial-gradient(rgba(255,255,255,.18) 1.5px, transparent 2px) 0 0 / 32px 32px; }}
@.fr {{ border-radius: 0; box-shadow: 0 0 0 6px #c0c0c0, 0 0 0 8px #404040, 14px 14px 0 8px rgba(0,0,0,.35); }} @.fl2 {{ background: #000080; color: #fff; border-radius: 0; }}
@.pill {{ background: #c0c0c0; color: #000; border-radius: 0; box-shadow: {BEV}; }}
@.s5 .sh {{ background: linear-gradient(90deg, rgba(0,128,128,.97) 24%, rgba(0,128,128,.55) 52%, transparent 72%); }} @.s5 .k {{ color: #fff200; }} @.s5 p {{ color: #fff; }} @.wc {{ border-radius: 0; box-shadow: 0 0 0 6px #c0c0c0, 14px 14px 0 6px rgba(0,0,0,.35); }}
@.tr small {{ color: #404040; }} @.tr em {{ color: #000080; }} @.tr > i, @.cp2 i {{ border-radius: 0; box-shadow: inset 2px 2px 0 #808080; }}
@.bub {{ background: #ffffe1; color: #000; border-radius: 0; box-shadow: 0 0 0 2px #000; }} @.ty {{ color: #000; }} @.ty.tyc::after {{ color: #000; }}
@.win {{ background: #000080; color: #fff; border-radius: 0; }} @.sr span, @.sr b {{ color: #000; }} @.sr .t {{ background: #fff; border-radius: 0; box-shadow: inset 2px 2px 0 #808080; }}
@.sr .t i {{ border-radius: 0; background: repeating-linear-gradient(90deg, #000080 0 18px, transparent 18px 22px); }} @.sr.best b, @.sr.best span {{ color: #000080; }}
@.ring .bgc {{ stroke: rgba(255,255,255,.2); }} @.ring .fg {{ stroke: #fff200; stroke-linecap: butt; }} @.ring .c small {{ color: #fff; }} @.s7 .rt2 p {{ color: #fff; }}
@.s8 .btn {{ background: #c0c0c0; color: #000; border-radius: 0; box-shadow: {BEV}; }} @.s8 .url {{ border-radius: 0; box-shadow: inset 0 0 0 3px #fff; }} @.s8 .fn {{ color: rgba(255,255,255,.75); }} @.end {{ background: #008080; }}
@.hud {{ color: #fff; }} @.hud .l {{ font-family: 'OSDigits', 'Pixelify Sans', sans-serif; }} @.hud .p {{ height: 18px; border-radius: 0; background: #fff; box-shadow: inset 2px 2px 0 #808080; }} @.hud .p i {{ background: repeating-linear-gradient(90deg, #000080 0 14px, transparent 14px 18px); }}
@.fl {{ background: #0000aa !important; }} @.bar {{ height: 18px; border-radius: 0; background: repeating-linear-gradient(90deg, #fff200 0 20px, transparent 20px 26px); }}
""") + heads('os', 'letter-spacing: 0; font-weight: 700; text-shadow: 7px 7px 0 rgba(0,50,50,.85);') + '\n' + sizes('os', SZ(wm=150, w=250, all=150, num=330, lbl=60, ttl=80, h2=160, ttl2=74, big=360, sub=58, h3=104, end=90, ring=110))

PK, BL = '#ff4fa3', '#1f4fd8'
TONE_P = 'grayscale(1) sepia(1) hue-rotate(285deg) saturate(3.2) contrast(1.15)'
TONE_B = 'grayscale(1) sepia(1) hue-rotate(180deg) saturate(3) contrast(1.1)'
RISO = sc('riso', f"""
/* ---------- Risograph ---------- */
.s-riso {{ --bg: #f3ecdc; --t: {BL}; --m: #5d63a3; --gr: none; --d-: 'Rubik', sans-serif; }}
.s-riso #st::before {{ content: ''; position: absolute; inset: 0; background: radial-gradient(circle, rgba(255,79,163,.45) 3px, transparent 3.5px) 0 0 / 16px 16px;
  -webkit-mask: radial-gradient(circle at 12% 18%, #000 0 20%, transparent 38%), radial-gradient(circle at 90% 85%, #000 0 22%, transparent 40%); mask: radial-gradient(circle at 12% 18%, #000 0 20%, transparent 38%), radial-gradient(circle at 90% 85%, #000 0 22%, transparent 40%); }}
@.bg, @.vig, @.s1 .glow {{ display: none; }} @.grain {{ opacity: .3; mix-blend-mode: multiply; }}
@.gt {{ background: none; color: {PK}; text-shadow: -7px 5px 0 rgba(31,79,216,.8); }} @.mk {{ filter: drop-shadow(7px 5px 0 rgba(255,79,163,.9)); }} @.mk path {{ fill: {BL}; }}
@.nd, @.pn {{ background: #f3ecdc; color: {BL}; border-radius: 6px; box-shadow: 0 0 0 3px {BL}, 14px 12px 0 rgba(255,79,163,.8); }}
@.nd .h {{ border-bottom: 3px solid {BL}; }} @.nd .h b {{ background: {PK} !important; color: #fff !important; }}
@.fm span {{ background: rgba(255,79,163,.16); border-radius: 4px; box-shadow: inset 0 0 0 2px {BL}; }} @.fm em {{ color: {BL}; }}
@.go {{ background: {PK}; color: #fff; border-radius: 6px; box-shadow: 6px 5px 0 {BL}; }} @.edg path {{ stroke: {BL}; }} @.edg .e2 {{ stroke: {PK}; filter: none; }}
@.chip {{ background: transparent; color: {BL}; border-radius: 8px; box-shadow: inset 0 0 0 3px {BL}; }} @.chip i {{ background: {PK} !important; }} @.r0, @.r3 {{ opacity: .4; filter: none; }}
@.s3 .ctr {{ background: radial-gradient(ellipse 58% 52% at center, rgba(243,236,220,.97) 40%, rgba(243,236,220,.75) 60%, transparent 80%); }} @.s4 .grid {{ background: radial-gradient(rgba(31,79,216,.22) 1.8px, transparent 2.2px) 0 0 / 22px 22px; }}
@.fr > i, @.wc {{ filter: {TONE_P}; }} @.fr::before {{ filter: blur(18px) {TONE_P}; }} @.tr > i, @.cp2 i, @.n1 .im {{ filter: {TONE_B}; }}
@.fr {{ border-radius: 6px; box-shadow: 0 0 0 3px {BL}, 10px 9px 0 3px rgba(31,79,216,.25); }} @.fl2 {{ background: {BL}; color: #fff; }}
@.pill {{ background: {PK}; color: #fff; box-shadow: 6px 5px 0 {BL}; }}
@.s5 .sh {{ background: linear-gradient(90deg, rgba(243,236,220,.97) 24%, rgba(243,236,220,.6) 52%, transparent 72%); }} @.s5 .k {{ color: {PK}; }} @.s5 p {{ color: {BL}; }} @.wc {{ border-radius: 6px; }}
@.tr small {{ color: #5d63a3; }} @.tr em {{ color: {PK}; }} @.bub {{ background: {BL}; color: #fff; box-shadow: 6px 5px 0 {PK}; }} @.ty {{ color: {BL}; }} @.win {{ background: {PK}; color: #fff; }}
@.sr span, @.sr b {{ color: {BL}; }} @.sr .t {{ background: rgba(31,79,216,.12); }} @.sr .t i {{ background: radial-gradient({PK} 2.2px, transparent 2.6px) 0 0 / 8px 8px, rgba(255,79,163,.35); }} @.sr.best b, @.sr.best span {{ color: {PK}; }}
@.ring .bgc {{ stroke: rgba(31,79,216,.15); }} @.ring .fg {{ stroke: {PK}; }} @.ring .c small {{ color: {BL}; }} @.s7 .rt2 p {{ color: {BL}; }}
@.s8 .btn {{ background: {PK}; color: #fff; box-shadow: 7px 6px 0 {BL}; }} @.s8 .url {{ color: {BL}; box-shadow: inset 0 0 0 3px {BL}; }} @.s8 .fn {{ color: rgba(31,63,191,.7); }} @.end {{ background: #f3ecdc; }}
@.hud {{ color: {BL}; }} @.hud .l {{ color: {BL}; }} @.hud .p {{ background: rgba(31,79,216,.15); }} @.hud .p i {{ background: {PK}; }}
@.fl {{ background: {PK} !important; }} @.bar {{ background: {PK}; box-shadow: 7px 6px 0 {BL}; }}
""") + heads('riso', f'font-weight: 900; mix-blend-mode: multiply; text-shadow: 8px 6px 0 rgba(255,79,163,.85);') + '\n'

G = '#39ff7a'
PHOS = 'grayscale(1) sepia(1) hue-rotate(75deg) saturate(4) brightness(.85) contrast(1.2)'
CRT = sc('crt', f"""
/* ---------- CRT terminal ---------- */
.s-crt {{ --bg: #020a04; --t: {G}; --m: #1f9a4a; --gr: none; --d-: 'Press Start 2P', monospace; }}
.s-crt #st {{ text-shadow: 0 0 12px rgba(57,255,122,.55); }} .s-crt #st::after {{ content: ''; position: absolute; inset: 0; z-index: 50; pointer-events: none; background: rgba(57,255,122,.035); animation: flick .14s steps(2) 0s infinite; }}
@.bg {{ display: none; }} @.grain {{ opacity: .08; }} @.vig {{ z-index: 40; background: repeating-linear-gradient(0deg, rgba(0,0,0,.38) 0 2px, transparent 2px 5px), radial-gradient(ellipse at center, transparent 55%, rgba(0,0,0,.88)); }}
@.gt {{ background: none; color: #d6ffe4; }} @.mk {{ filter: drop-shadow(0 0 14px rgba(57,255,122,.8)); }} @.mk path {{ fill: {G}; }} @.s1 .glow {{ background: radial-gradient(circle, rgba(57,255,122,.22), transparent 60%); }}
@.s4 .ttl::before, @.s6 .ttl::before {{ content: '> '; color: #d6ffe4; }}
@.nd, @.pn, @.chip, @.pill, @.fm, @.bub, @.tr, @.sr, @.fl2, @.hud, @.s5 p, @.s5 .k, @.s7 .rt2 p, @.s8 .url, @.ring .c small, @.s1 .tg, @.ty, @.s8 .fn {{ font-family: 'JetBrains Mono', monospace; }}
@.nd, @.pn {{ background: rgba(2,20,8,.92); color: {G}; border-radius: 0; box-shadow: 0 0 0 2px {G}, 0 0 34px rgba(57,255,122,.25); }}
@.nd .h {{ border-bottom: 2px dashed rgba(57,255,122,.5); }} @.nd .h b {{ background: transparent !important; color: {G} !important; box-shadow: 0 0 0 2px {G}; border-radius: 0; }}
@.fm span {{ background: transparent; border-radius: 0; box-shadow: inset 0 0 0 1px rgba(57,255,122,.5); }} @.fm em {{ color: #1f9a4a; }}
@.go {{ background: {G}; color: #021; border-radius: 0; font: 400 18px 'Press Start 2P', monospace; text-shadow: none; }} @.edg path {{ stroke: {G}; }} @.edg .e2 {{ stroke: #d6ffe4; filter: drop-shadow(0 0 10px {G}); }}
@.chip {{ background: transparent; color: {G}; border-radius: 0; box-shadow: inset 0 0 0 2px rgba(57,255,122,.6); }} @.chip i {{ background: {G} !important; border-radius: 0; }} @.r0, @.r3 {{ opacity: .35; }}
@.s3 .ctr {{ background: radial-gradient(ellipse 58% 52% at center, rgba(2,10,4,.97) 40%, rgba(2,10,4,.75) 60%, transparent 80%); }} @.s4 .grid {{ background: radial-gradient(rgba(57,255,122,.18) 1.5px, transparent 2px) 0 0 / 32px 32px; }}
@.fr > i, @.wc, @.tr > i, @.cp2 i, @.n1 .im {{ filter: {PHOS}; }} @.fr::before {{ filter: blur(18px) {PHOS} brightness(.6); }}
@.fr {{ border-radius: 0; box-shadow: 0 0 0 2px {G}, 0 0 30px rgba(57,255,122,.3); }} @.fl2 {{ background: #021; color: {G}; border-radius: 0; }}
@.pill {{ background: transparent; color: {G}; border-radius: 0; box-shadow: inset 0 0 0 2px {G}; }}
@.s5 .sh {{ background: linear-gradient(90deg, rgba(2,10,4,.97) 24%, rgba(2,10,4,.55) 52%, transparent 72%); }} @.s5 .k {{ color: #d6ffe4; }} @.s5 p {{ color: {G}; font-size: 40px; }} @.wc {{ border-radius: 0; box-shadow: 0 0 0 2px {G}; }}
@.tr small {{ color: #1f9a4a; }} @.tr em {{ color: #d6ffe4; }} @.tr > i, @.cp2 i {{ border-radius: 0; }}
@.bub {{ background: transparent; color: {G}; border-radius: 0; box-shadow: 0 0 0 2px {G}; }} @.bub::before {{ content: '> '; }} @.ty {{ color: {G}; }} @.ty.tyc::after {{ content: '█'; color: {G}; }}
@.win {{ background: {G}; color: #021; border-radius: 0; text-shadow: none; }} @.sr .t {{ border-radius: 0; background: rgba(57,255,122,.12); }} @.sr .t i {{ border-radius: 0; background: repeating-linear-gradient(90deg, {G} 0 10px, transparent 10px 14px); }} @.sr.best b, @.sr.best span {{ color: #d6ffe4; }}
@.ring .bgc {{ stroke: rgba(57,255,122,.15); }} @.ring .fg {{ stroke: {G}; stroke-linecap: butt; filter: drop-shadow(0 0 10px {G}); }} @.ring .c small {{ color: #1f9a4a; }} @.s7 .rt2 p {{ color: {G}; font-size: 36px; }}
@.s8 .btn {{ background: {G}; color: #021; border-radius: 0; text-shadow: none; font: 400 24px 'Press Start 2P', monospace; }} @.s8 .url {{ border-radius: 0; color: {G}; box-shadow: inset 0 0 0 2px {G}; }} @.s8 .fn {{ color: #1f9a4a; }} @.end {{ background: #000; }}
@.hud {{ color: {G}; }} @.hud .l {{ font: 400 18px 'Press Start 2P', monospace; color: {G}; }} @.hud .p {{ border-radius: 0; background: rgba(57,255,122,.15); }} @.hud .p i {{ background: {G}; }}
@.fl {{ background: {G} !important; }} @.bar {{ height: 12px; border-radius: 0; background: {G}; box-shadow: 0 0 22px {G}; }}
""") + heads('crt', 'letter-spacing: 0; font-weight: 400; line-height: 1.3;') + '\n' + sizes('crt', SZ(wm=100, w=124, all=84, num=230, lbl=34, ttl=44, h2=78, ttl2=38, big=230, sub=30, h3=60, end=52, ring=64))

K = '#cdb68e'
TORN = 'url(#torn)'
COL = sc('collage', f"""
/* ---------- Paper collage ---------- */
.s-collage {{ --bg: {K}; --t: #161616; --m: #5a4a34; --gr: none; --d-: 'Oswald', sans-serif; }}
@.bg, @.vig, @.s1 .glow, @.s4 .grid {{ display: none; }} @.grain {{ opacity: .38; mix-blend-mode: multiply; }} @.mk path {{ fill: #161616; }}
@.gt {{ background: #e2402f; -webkit-background-clip: border-box; background-clip: border-box; color: #fff; }}
@.wd, @.s2 .all .up, @.s4 .ttl .up, @.s6 .ttl .up, @.s5 h2 .up, @.s8 h2 .up, @.s7 .rt2 h3 .up, @.s3 .lbl, @.s7 .sub, @.s3 .num, @.s7 .big {{ background: #fbfaf6; padding: 0 .16em; box-shadow: 5px 7px 0 rgba(0,0,0,.25); filter: {TORN}; }}
@.gt, #st @.gt {{ background: #e2402f !important; color: #fff; }} @.s2 .all .ln:nth-child(1) .up, @.s5 h2 .up:first-child, @.s8 h2 .ln:first-child .up {{ rotate: -1.8deg; }} @.s2 .all .ln:nth-child(2) .up, @.s5 h2 .up:last-child, @.s8 h2 .ln:last-child .up {{ rotate: 1.5deg; }}
@.s1 .wm .up, @.s8 .wm .up {{ margin: 0 3px; padding: 0 .08em; background: #fbfaf6; box-shadow: 4px 6px 0 rgba(0,0,0,.25); filter: {TORN}; }}
@.s1 .wm .up:nth-child(3n+1), @.s8 .wm .up:nth-child(3n+1) {{ background: #ffd23f; rotate: -4deg; }} @.s1 .wm .up:nth-child(3n+2), @.s8 .wm .up:nth-child(3n+2) {{ background: #e2402f; color: #fff; rotate: 3deg; }}
@.s1 .wm .up:nth-child(3n), @.s8 .wm .up:nth-child(3n) {{ background: #161616; color: #fbfaf6; rotate: -2deg; }}
@.nd, @.pn {{ background: transparent; color: #161616; border-radius: 0; box-shadow: none; isolation: isolate; }} @.n1 {{ rotate: -2deg; }} @.n2 {{ rotate: 1deg; }} @.p1 {{ rotate: -2deg; }} @.p2 {{ rotate: 1.5deg; }} @.p3 {{ rotate: -1deg; }}
@.nd::before, @.pn::before {{ content: ''; position: absolute; inset: 0; z-index: -1; background: #fbfaf6; filter: {TORN} drop-shadow(7px 11px 0 rgba(0,0,0,.24)); }}
@.nd::after, @.pn::after {{ content: ''; position: absolute; top: -18px; left: 50%; width: 140px; height: 38px; margin-left: -70px; background: rgba(244,235,200,.78); box-shadow: 0 1px 3px rgba(0,0,0,.18); rotate: -3deg; }}
@.nd .h {{ background: none; border-bottom: 2px dashed rgba(0,0,0,.25); font-family: 'Oswald', sans-serif; text-transform: uppercase; letter-spacing: .04em; }} @.nd .h b {{ border-radius: 0; }} @.pn .k {{ font-family: 'Oswald', sans-serif; letter-spacing: .08em; }}
@.fm span {{ background: #fff; border-radius: 0; box-shadow: inset 0 0 0 1.5px rgba(0,0,0,.2); }} @.go {{ background: #161616; color: #fff; border-radius: 0; font-family: 'Oswald', sans-serif; text-transform: uppercase; letter-spacing: .06em; filter: {TORN}; }}
@.edg path {{ stroke: #161616; stroke-width: 4.5; }} @.edg .e2 {{ stroke: #e2402f; filter: none; }} @.port0 {{ background: #161616; box-shadow: none; }}
@.chip {{ background: #fbfaf6; color: #161616; border-radius: 0; box-shadow: 4px 6px 0 rgba(0,0,0,.2); filter: {TORN}; font-family: 'Oswald', sans-serif; text-transform: uppercase; }} @.chip i {{ border-radius: 0; }} @.r0, @.r3 {{ opacity: .5; filter: none; }}
@.s3 .ctr {{ background: radial-gradient(ellipse 56% 50% at center, rgba(205,182,142,.96) 40%, rgba(205,182,142,.7) 60%, transparent 80%); }}
@.fr {{ border-radius: 0; box-shadow: 0 0 0 10px #fbfaf6, 8px 16px 0 10px rgba(0,0,0,.22); rotate: -2deg; }} @.fr:nth-child(even) {{ rotate: 2.5deg; }} @.fl2 {{ background: #161616; color: #fff; border-radius: 0; }}
@.pill {{ background: #ffd23f; color: #161616; border-radius: 0; font-family: 'Oswald', sans-serif; text-transform: uppercase; letter-spacing: .05em; filter: {TORN}; }}
@.s5 .sh {{ background: linear-gradient(90deg, rgba(205,182,142,.97) 26%, rgba(205,182,142,.55) 52%, transparent 72%); }} @.s5 .k {{ display: inline-block; padding: 4px 12px; background: #161616; color: #fff; }}
@.s5 p {{ display: inline-block; padding: 12px 18px; background: #fbfaf6; color: #161616; rotate: -1deg; filter: {TORN}; }}
@.wc {{ position: relative; border-radius: 0; box-shadow: 0 0 0 10px #fbfaf6, 8px 16px 0 10px rgba(0,0,0,.24); }} @.wc::after {{ content: ''; position: absolute; left: 50%; top: -24px; width: 120px; height: 36px; margin-left: -60px; background: rgba(244,235,200,.8); rotate: -4deg; }}
@.tr small {{ color: #5a4a34; }} @.tr em {{ color: #e2402f; font-family: 'Oswald', sans-serif; }} @.tr > i, @.cp2 i {{ border-radius: 0; }} @.bub {{ background: #ffd23f; color: #161616; border-radius: 0; }} @.ty {{ color: #161616; }}
@.win {{ background: #e2402f; color: #fff; border-radius: 0; }} @.sr .t {{ border-radius: 0; background: rgba(0,0,0,.1); }} @.sr .t i {{ border-radius: 0; background: #161616; }} @.sr.best .t i {{ background: #e2402f; }} @.sr.best b, @.sr.best span {{ color: #e2402f; }}
@.ring .bgc {{ stroke: rgba(0,0,0,.12); }} @.ring .fg {{ stroke: #e2402f; stroke-linecap: butt; }} @.ring .c b {{ background: #fbfaf6; padding: 0 .12em; filter: {TORN}; }} @.ring .c small {{ color: #5a4a34; }} @.s7 .rt2 p {{ color: #161616; }}
@.s8 .btn {{ background: #161616; color: #fff; border-radius: 0; font-family: 'Oswald', sans-serif; text-transform: uppercase; letter-spacing: .05em; filter: {TORN}; }} @.s8 .url {{ border-radius: 0; background: #fbfaf6; box-shadow: none; filter: {TORN}; }}
@.s8 .fn {{ color: rgba(0,0,0,.55); }} @.end {{ background: {K}; }}
@.hud {{ color: #5a4a34; }} @.hud .l {{ color: #161616; }} @.hud .p {{ background: rgba(0,0,0,.15); }} @.hud .p i {{ background: #e2402f; }}
@.fl {{ background: #fbfaf6 !important; }} @.bar {{ height: 16px; border-radius: 0; background: #e2402f; filter: {TORN}; }}
""") + heads('collage', 'letter-spacing: .005em; text-transform: uppercase; font-weight: 700;') + '\n' + sizes('collage', SZ(wm=180, w=270, all=160, num=360, lbl=64, ttl=84, h2=160, ttl2=78, big=380, sub=58, h3=112, end=94, ring=110))

CSS = "@font-face { font-family: 'OSDigits'; src: url(fonts/PressStart2P-latin-3d97f0.woff2) format('woff2'); unicode-range: U+0030-0039, U+0025, U+002B, U+2212; font-display: block; size-adjust: 78%; }\n" + HAND + OS + RISO + CRT + COL + '\n@keyframes flick { 50% { opacity: 0; } }\n'

DEFS = """<filter id="rough" x="-8%" y="-8%" width="116%" height="116%"><feTurbulence class="boil" type="fractalNoise" baseFrequency=".032" numOctaves="2" seed="1" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="6" xChannelSelector="R" yChannelSelector="G"/></filter>
<filter id="torn" x="-6%" y="-10%" width="112%" height="120%"><feTurbulence type="fractalNoise" baseFrequency=".05" numOctaves="3" seed="4" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="11" xChannelSelector="R" yChannelSelector="G"/></filter>"""

# ---------------------------------------------------------------- hand-drawn doodles: (shape, x, y, w, h, start, end, colour, extra css)
SHAPES = {
    'circle': ('0 0 100 100', 'M52 6 C20 4 4 30 6 54 C8 82 34 96 60 94 C86 92 98 64 94 40 C90 18 70 6 44 10 C36 12 30 16 26 20'),
    'line': ('0 0 100 20', 'M2 13 C18 5 30 18 48 10 S78 3 98 12'),
    'arrow': ('0 0 100 60', 'M4 52 C28 10 62 8 92 30 M76 16 L92 30 L72 40'),
    'arrowd': ('0 0 60 100', 'M30 4 C10 30 50 60 30 94 M14 78 L30 94 L44 76'),
    'star': ('0 0 100 100', 'M50 6 L60 38 L94 38 L66 58 L78 92 L50 72 L22 92 L34 58 L6 38 L40 38 Z'),
    'burst': ('0 0 100 100', 'M50 4 V26 M50 74 V96 M4 50 H26 M74 50 H96 M18 18 L33 33 M82 82 L67 67 M82 18 L67 33 M18 82 L33 67'),
    'check': ('0 0 100 100', 'M8 56 L38 86 L94 12'),
    'loop': ('0 0 120 60', 'M4 40 C20 10 40 10 40 30 C40 50 20 50 26 32 C34 10 60 8 70 30 C78 50 56 52 62 32 C70 8 100 10 116 30'),
}
DOODLES = [
    ('circle', 640, 230, 640, 560, .35, 1.7, '#e2553e'), ('star', 560, 250, 90, 90, .7, 1.7, '#ffcf3a'), ('burst', 1290, 640, 120, 120, .9, 1.7, '#1d1d1f'),
    ('burst', 1420, 270, 150, 150, 2.1, 4.8, '#e2553e'), ('star', 380, 700, 110, 110, 4.15, 4.8, '#ffcf3a'), ('loop', 700, 820, 520, 90, 4.35, 4.8, '#e2553e'),
    ('circle', 620, 250, 680, 420, 5.35, 7.8, '#e2553e'), ('arrow', 1180, 740, 200, 110, 6.05, 7.8, '#1d1d1f'),
    ('arrow', 430, 720, 190, 100, 9.8, 12.7, '#e2553e'), ('star', 1750, 170, 100, 100, 11.4, 12.7, '#ffcf3a'), ('line', 1180, 150, 660, 50, 8.5, 12.7, '#e2553e'),
    ('line', 140, 660, 720, 50, 13.8, 15.8, '#e2553e'), ('star', 860, 250, 120, 120, 14.0, 15.8, '#ffcf3a'), ('arrowd', 620, 170, 80, 130, 14.2, 15.8, '#1d1d1f'),
    ('check', 620, 250, 60, 60, 17.1, 19.5, '#16a36a'), ('check', 1150, 250, 60, 60, 17.35, 19.5, '#16a36a'), ('check', 1680, 250, 60, 60, 17.6, 19.5, '#16a36a'),
    ('circle', 500, 220, 920, 560, 20.35, 21.8, '#e2553e'), ('burst', 360, 560, 140, 140, 20.9, 21.8, '#ffcf3a'),
    ('burst', 330, 190, 150, 150, 22.6, 23.75, '#ffcf3a'), ('line', 1060, 560, 460, 40, 22.9, 23.75, '#e2553e'),
    ('star', 520, 210, 110, 110, 24.5, 30, '#ffcf3a'), ('star', 1330, 210, 90, 90, 24.7, 30, '#e2553e'), ('arrow', 1370, 800, 200, 110, 25.6, 30, '#e2553e'),
]
NOTES = [('ого!', 1240, 590, -8, 1.0, 1.7), ('и ещё больше', 1300, 820, -4, 6.2, 7.8), ('клик!', 330, 800, -10, 10.0, 12.7),
         ('одним кликом', 1440, 90, 4, 11.5, 12.7), ('твои деньги', 1500, 700, -5, 23.0, 23.75), ('жми!', 1590, 880, -8, 25.8, 30)]


def scene_of(t):
    """Which scene a doodle belongs to (by its start time on the base timeline) — used to re-time it with ?o=hook."""
    return 's' + str(1 + sum(t >= c for c in (2, 5, 8, 13, 16, 20, 24)))


def doodles():
    out = ''
    for sh, x, y, w, h, d, o, c in DOODLES:
        vb, path = SHAPES[sh]
        vw, vh = map(float, vb.split()[2:])
        sw = 6 / ((w / vw * h / vh) ** .5)  # ≈6 px on screen whatever the doodle's size
        out += (f'<svg class="dd" data-sc="{scene_of(d)}" viewBox="{vb}" preserveAspectRatio="none" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;--d:{d}s;--o:{o}s;--c:{c};--sw:{sw:.2f}">'
                f'<path pathLength="1" d="{path}"/></svg>')
    for t, x, y, r, d, o in NOTES:
        out += f'<span class="ddt" data-sc="{scene_of(d)}" style="left:{x}px;top:{y}px;rotate:{r}deg;--d:{d}s;--o:{o}s">{t}</span>'
    return f'<div class="dds" aria-hidden="true">{out}</div>'


DDCSS = """
.dds { display: none; position: absolute; inset: 0; z-index: 30; pointer-events: none; } .port .dds { display: none !important; }
.dd { position: absolute; overflow: visible; filter: url(#rough); animation: fout .25s linear var(--o) forwards; }
.dd path { fill: none; stroke: var(--c); stroke-width: var(--sw); stroke-linecap: round; stroke-linejoin: round; stroke-dasharray: 1; stroke-dashoffset: 1; animation: ddraw .55s cubic-bezier(.4,0,.2,1) var(--d) forwards; }
@keyframes ddraw { to { stroke-dashoffset: 0; } }
.ddt { position: absolute; font: 700 64px 'Caveat', cursive; color: #e2553e; white-space: nowrap; animation: pop .45s var(--po) var(--d) both, fout .25s linear var(--o) forwards; }
"""
