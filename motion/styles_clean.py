"""Ten complete looks for oneflow-clean.html, switched with ?s=<name> (class s-<name> on #st).

Each look replaces background, type, panel shape, accent gradient, text/button colours, ambient light and redraws the
wireframe product pictures in its own palette. css() returns every look's CSS; LOOKS lists name → caption.
"""
import wire

PANELS = '.aw, .dash, .tp, .aiw, .cww, .adc, .kr, .kbw, .zc, .cc, .mc, .pc, .tl, .nd, .xn, .trk, .ck'
FILLS = '.fm span, .dh .sr, .tabs, .th span, .xn .r, .ans, .pctl span, .cwh span:not(.ava), .adc .ln2, .trw:nth-child(2), .st, .ch, .fch, .tabs .on, .pc .bar, .xn .ln'
LINES = '.atb, .ch, .chh, .dash aside, .dt, .cwh, .nd .h, .xn .h'
MUTED = '.tabs span, .th span, .dash aside span, .pctl span, .cwh span:not(.ava), .fm em, .pn small, .pc .sc2 b small, .pc .sc2 > span, .cvh, .bud, .trw small, .dh .sr, .dt, .ac small, .sub, .fn, .url'
ACCENT = '.gob, .pill, .auto, .fch i, .ava, .tile .back, .tile .front, .rib'
BUTTONS = '.kb, .adb, .pctl .go, .dh .nw, .ub'
HEADS = '.row, .row *, .hl, .hl *, .done, .done *, .pn, .pn *, .lg b, .kb, .pl'


def look(name, *, bg, ink, mut, panel, line, fill, b1, b2, head, body, radius, shadow, btn, btxt, glow='none', amb=None, flash='#fff',
         grad=None, gradt=None, dot=None, base=None, atxt='#fff', headcss='', extra='', wire_pal=None):
    P = f'#st.s-{name}'  # noqa: N806
    sel = lambda group: ', '.join(f'{P} {s.strip()}' for s in group.split(','))  # noqa: E731
    grad = grad or f'linear-gradient(90deg, {b1}, {b2})'
    gradt = gradt or grad
    dot = dot or line
    amb1, amb2 = amb or ('transparent', 'transparent')
    css = f"""
{P} {{ background: {bg}; color: {ink}; --ink: {ink}; --mut: {mut}; --b1: {b1}; --b2: {b2}; --grad: {grad}; --gradt: {gradt}; --glow: {glow if glow != 'none' else 'transparent'}; }}
{P} * {{ font-family: {body} !important; }} {sel(HEADS)} {{ font-family: {head} !important; }}
{sel(HEADS.replace(', .row *', '').replace(', .hl *', '').replace(', .done *', '').replace(', .pn *', ''))} {{ {headcss} }}
{sel(PANELS)} {{ background: {panel}; box-shadow: {shadow}; border-radius: {radius}px; }}
{sel(FILLS)} {{ background: {fill}; box-shadow: none; }}
{sel(LINES)} {{ border-color: {line} !important; }}
{sel(MUTED)} {{ color: {mut}; }}
{sel(ACCENT)} {{ background: var(--grad); color: {atxt}; box-shadow: none; }}
{sel(BUTTONS)} {{ background: {'var(--grad)' if btn == 'grad' else btn}; color: {btxt}; box-shadow: none; }}
{P} .acv, {P} .cvs {{ background: radial-gradient({dot} 1.5px, transparent 2px) 0 0 / 28px 28px, {fill}; }}
{P} .aed path, {P} .aed2 path {{ stroke: {b1}; }} {P} .ck path {{ stroke: {b1}; }} {P} .rip {{ border-color: {b1}; }}
{P} .ck {{ background: {panel}; }} {P} .trw em {{ color: {b1}; }} {P} .tabs .on, {P} .dash aside .on, {P} .dt .on {{ color: {b1}; }} {P} .dash aside .on i {{ background: {b1}; }}
{P} .cglow {{ background: radial-gradient(ellipse at center, color-mix(in srgb, {base or flash} 94%, transparent) 35%, color-mix(in srgb, {base or flash} 65%, transparent) 55%, transparent 72%); }}
{P} .amb .g1 {{ background: radial-gradient(circle, {amb1}, transparent 62%); }} {P} .amb .g2 {{ background: radial-gradient(circle, {amb2}, transparent 62%); }}
{P} .flash {{ background: {flash}; }}
{P} #bg1 stop:nth-child(1) {{ stop-color: {b2}; }} {P} #bg1 stop:nth-child(2), {P} #bg1 stop:nth-child(3) {{ stop-color: {b1}; }}
{P} .bl {{ background: var(--gradt); -webkit-background-clip: text; background-clip: text; color: transparent; }}
{P} .tl.ui u {{ background: {ink}; }} {P} .tl.ui b {{ background: {fill}; }}
"""
    return css + extra.replace('P::', P + '::').replace('P ', P + ' ') + '\n' + wire.css_vars(P, wire_pal)


LOOKS = {}


def add(name, base, caption, **kw):
    kw['base'] = base
    LOOKS[name] = (caption, look(name, **kw))


add('midnight', base='#060913', caption='Midnight — тёмный неон, стекло, голубое свечение',
    bg='radial-gradient(ellipse 80% 60% at 50% 115%, #1c2c78, transparent 70%), #060913', ink='#eef1ff', mut='#8a93c0',
    panel='rgba(22,28,58,.92)', line='rgba(140,160,255,.2)', fill='rgba(255,255,255,.06)', b1='#4d7cff', b2='#35e0ff', head="'Manrope'", body="'Manrope'",
    radius=24, shadow='0 0 0 1.5px rgba(140,160,255,.28), 0 40px 90px -30px rgba(0,0,0,.9)', btn='grad', btxt='#fff', glow='rgba(53,224,255,.6)',
    amb=('rgba(77,124,255,.35)', 'rgba(53,224,255,.25)'), flash='#0b1233', headcss='font-weight: 600;',
    wire_pal=dict(ink='#a9b8ff', acc='#35e0ff', bar='#2a3566', bg='#10163a', dot='#222c5c', fill='#10163a', head='#a9b8ff', sw=2.6))

add('brutal', base='#ffe45c', caption='Neo-brutal — жёлтый, чёрные рамки, жёсткие тени',
    bg='#ffe45c', ink='#111', mut='#4a4a4a', panel='#fff', line='#111', fill='#fff7d1', b1='#ff4f8b', b2='#ff4f8b', head="'Dela Gothic One'", body="'Onest'",
    radius=16, shadow='0 0 0 3px #111, 8px 8px 0 #111', btn='#111', btxt='#fff', flash='#fff', dot='#e6d27a',
    headcss='letter-spacing: -.01em;', grad='linear-gradient(90deg, #ff4f8b, #ff4f8b)', gradt='linear-gradient(90deg, #111, #111)',
    extra='P .bl { background: #ff4f8b !important; color: #111 !important; -webkit-background-clip: border-box !important; background-clip: border-box !important; padding: 0 .15em; box-shadow: 0 0 0 3px #111; }\n'
          'P .pill, P .auto, P .adb, P .pctl .go, P .gob, P .kb { box-shadow: 0 0 0 3px #111, 4px 4px 0 #111 !important; }',
    wire_pal=dict(ink='#111', acc='#ff4f8b', bar='#111', bg='#fff7d1', dot='#e6d27a', fill='#fff', head='#111', sw=3.4))

add('editorial', base='#f2ece1', caption='Editorial — журнальная вёрстка, антиква, красный акцент',
    bg='#f2ece1', ink='#1b1712', mut='#7a6f60', panel='#faf6ee', line='#1b1712', fill='#efe7d8', b1='#c8391f', b2='#c8391f', head="'Playfair Display'", body="'PT Serif'",
    radius=0, shadow='0 0 0 1px #1b1712', btn='#1b1712', btxt='#faf6ee', flash='#faf6ee', dot='#d8ccb6',
    headcss='font-weight: 500; letter-spacing: -.02em;',
    extra='P .bl { font-style: italic; }\nP .row { font-size: 104px !important; }',
    wire_pal=dict(ink='#3a3128', acc='#c8391f', bar='#d9cdb8', bg='#f4ede0', dot='#e0d4bf', fill='#faf6ee', head='#3a3128', sw=2.2))

add('swiss', base='#ffffff', caption='Swiss — белый, чёрный, красный, сетка и капс',
    bg='repeating-linear-gradient(90deg, #ececec 0 1px, transparent 1px 160px), #fff', ink='#000', mut='#6b6b6b', panel='#fff', line='#000', fill='#f2f2f2',
    b1='#ff2a00', b2='#ff2a00', head="'Inter Tight'", body="'Inter Tight'", radius=0, shadow='0 0 0 2px #000', btn='#000', btxt='#fff', flash='#ff2a00', dot='#d6d6d6',
    headcss='font-weight: 800; text-transform: uppercase; letter-spacing: -.045em;',
    wire_pal=dict(ink='#000', acc='#ff2a00', bar='#cfcfcf', bg='#fff', dot='#e2e2e2', fill='#fff', head='#000', sw=2.8))

add('blueprint', base='#0d3a86', caption='Blueprint — чертёж: синяя калька, белые линии, моноширинный',
    bg='repeating-linear-gradient(0deg, rgba(255,255,255,.07) 0 1px, transparent 1px 40px), repeating-linear-gradient(90deg, rgba(255,255,255,.07) 0 1px, transparent 1px 40px), #0d3a86',
    ink='#fff', mut='#a9c3f0', panel='rgba(13,58,134,.92)', line='rgba(255,255,255,.7)', fill='rgba(255,255,255,.07)', b1='#fff', b2='#9fd3ff', head="'IBM Plex Mono'", body="'IBM Plex Mono'",
    radius=4, shadow='0 0 0 1.5px rgba(255,255,255,.85)', btn='#fff', btxt='#0d3a86', atxt='#0d3a86', flash='#fff', dot='rgba(255,255,255,.2)',
    headcss='font-weight: 500; letter-spacing: -.04em;',
    extra='P .aw, P .dash, P .tp, P .aiw, P .cww, P .pc, P .cc { outline: 1.5px dashed rgba(255,255,255,.5); outline-offset: 10px; }',
    wire_pal=dict(ink='#fff', acc='#9fd3ff', bar='rgba(255,255,255,.35)', bg='#0f4196', dot='#2a5aa8', fill='#0f4196', head='#fff', sw=2.4))

add('holo', base='#eee9f8', caption='Holo — перламутр, пастельные градиенты, мягкое стекло',
    bg='linear-gradient(135deg, #f3e3ff, #dcf6f1 45%, #fff0df)', ink='#261c40', mut='#7d7299', panel='rgba(255,255,255,.72)', line='rgba(255,255,255,.95)',
    fill='rgba(243,236,255,.8)', b1='#9b5cff', b2='#ff6fb1', head="'Unbounded'", body="'Nunito'", radius=38,
    shadow='0 0 0 1.5px rgba(255,255,255,.9), 0 40px 80px -40px rgba(155,92,255,.45)', btn='grad', btxt='#fff', glow='rgba(155,92,255,.45)',
    extra='P .hl { font-size: 54px !important; } P .row { font-size: 80px !important; }',
    amb=('rgba(255,111,177,.28)', 'rgba(111,220,255,.3)'), grad='linear-gradient(90deg, #9b5cff, #ff6fb1 60%, #ffb36b)', headcss='font-weight: 500; letter-spacing: -.04em;',
    wire_pal=dict(ink='#5b4a8a', acc='#9b5cff', bar='#e3d6ff', bg='#f7f0ff', dot='#e4d9fa', fill='#fff', head='#5b4a8a', sw=2.8))

add('terminal', base='#050c07', caption='Terminal — чёрный экран, зелёный фосфор, моноширинный',
    bg='radial-gradient(ellipse at center, #0b1a10, #030604 75%)', ink='#b8ffcf', mut='#4f9a68', panel='#06120a', line='#1f7a45', fill='#0b2014',
    b1='#39ff88', b2='#39ff88', head="'JetBrains Mono'", body="'JetBrains Mono'", radius=4, shadow='0 0 0 1.5px #1f7a45', btn='#39ff88', btxt='#031008',
    glow='rgba(57,255,136,.6)', flash='#0f3a1f', dot='#13391f', headcss='font-weight: 500; letter-spacing: -.05em;',
    extra='P::after { content: ""; position: absolute; inset: 0; z-index: 70; pointer-events: none; background: repeating-linear-gradient(0deg, rgba(0,0,0,.22) 0 2px, transparent 2px 4px); }\n'
          'P .ava, P .pill, P .auto, P .fch i, P .gob { color: #031008; }',
    wire_pal=dict(ink='#39ff88', acc='#b8ffcf', bar='#1f5a36', bg='#06120a', dot='#123a22', fill='#06120a', head='#39ff88', sw=2.4))

add('clay', base='#f6e4d8', caption='Clay — тёплая глина, объёмные мягкие плашки',
    bg='radial-gradient(ellipse 70% 60% at 50% 110%, #ffd9c7, transparent 70%), #f6e4d8', ink='#3a2a2a', mut='#9b8078', panel='#fbede4', line='rgba(160,110,90,.18)',
    fill='#f3dccf', b1='#ff6f4f', b2='#b86bff', head="'Nunito'", body="'Nunito'", radius=40,
    shadow='inset 0 3px 0 rgba(255,255,255,.85), inset 0 -6px 12px rgba(190,120,95,.18), 16px 20px 40px -14px rgba(160,100,80,.4), -10px -10px 26px rgba(255,255,255,.75)',
    btn='grad', btxt='#fff', amb=('rgba(255,150,120,.3)', 'rgba(190,130,255,.22)'), flash='#fff5ef', headcss='font-weight: 800; letter-spacing: -.03em;',
    wire_pal=dict(ink='#7a5a52', acc='#ff6f4f', bar='#f0d2c4', bg='#fcefe7', dot='#f0dace', fill='#fff8f3', head='#7a5a52', sw=3.2))

add('sunset', base='#f0457a', caption='Sunset — яркий градиент, белый текст, матовое стекло',
    bg='linear-gradient(125deg, #ff8a3d, #ff3d7f 45%, #6c3dff)', ink='#fff', mut='rgba(255,255,255,.72)', panel='rgba(255,255,255,.16)', line='rgba(255,255,255,.35)',
    fill='rgba(255,255,255,.14)', b1='#fff', b2='#ffe07a', head="'Unbounded'", body="'Rubik'", radius=30,
    shadow='0 0 0 1.5px rgba(255,255,255,.45), 0 40px 80px -30px rgba(60,0,80,.5)', btn='#fff', btxt='#ff3d7f', flash='#fff',
    grad='linear-gradient(90deg, #ffe07a, #ffffff)', gradt='linear-gradient(90deg, #fff4c2, #ffe07a)', headcss='font-weight: 600; letter-spacing: -.04em;',
    extra='P .pill, P .auto, P .fch i, P .ava, P .gob { color: #ff3d7f; }\nP .hl { font-size: 54px !important; } P .row { font-size: 80px !important; }\nP .aw, P .dash, P .tp, P .aiw, P .cww, P .adc, P .kr, P .pc, P .cc { -webkit-backdrop-filter: blur(14px); backdrop-filter: blur(14px); }',
    wire_pal=dict(ink='#e8336f', acc='#6c3dff', bar='#ffd3c6', bg='#fff4ec', dot='#ffdcd0', fill='#fff', head='#e8336f', sw=2.8))

add('sketch', base='#fdfbf4', caption='Sketch — тетрадь в линейку, рукописные заголовки, маркер',
    bg='repeating-linear-gradient(180deg, #fdfbf4 0 46px, #d6e2f4 46px 48px), #fdfbf4', ink='#1f2a44', mut='#6b7593', panel='#fffef9', line='#1f2a44', fill='#f4f1e6',
    b1='#1f2a44', b2='#e8553a', head="'Caveat'", body="'Pangolin'", radius=12, shadow='0 0 0 2.2px #1f2a44, 5px 6px 0 rgba(31,42,68,.12)', btn='#1f2a44', btxt='#fffef9',
    flash='#fffef9', dot='#d9d3bf', headcss='font-weight: 700; letter-spacing: 0;',
    extra='P .bl { background: linear-gradient(transparent 58%, #ffe45c 58% 92%, transparent 92%) !important; color: #1f2a44 !important; -webkit-background-clip: border-box !important; background-clip: border-box !important; }\n'
          'P .row, P .hl { font-size: 118px !important; } P .hl { font-size: 92px !important; } P .aw, P .tp, P .cww, P .pc:nth-child(2) { rotate: -.6deg; } P .dash, P .aiw, P .pc:nth-child(1) { rotate: .5deg; }',
    wire_pal=dict(ink='#1f2a44', acc='#e8553a', bar='#cfd6e4', bg='#fffdf5', dot='#e7e1cc', fill='#fffef9', head='#1f2a44', sw=2.8))


def css():
    return '\n'.join(c for _, c in LOOKS.values())
