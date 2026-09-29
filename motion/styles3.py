"""Ten more looks for the ONEFLOW motion video (made for the offer-first cut, ?o=hook).

theme() writes the shared overrides (palette, type, cards, fields, buttons, chips, photos, HUD) from a few parameters;
each look then adds its own signature: masthead rules, clay bevels, frosted glass, Bauhaus shapes, newsprint, chalk,
a thermal receipt with a barcode, a vaporwave sun and grid, gold hairlines, comic outlines and a starburst.
"""

NAMES = {
    'editorial': 'Editorial — журнальная вёрстка: антиква Playfair, красный курсив, тонкие линейки',
    'clay': 'Clay — «пластилиновый» 3D: пухлые карточки, мягкие объёмные тени, пастель',
    'glass': 'Glass — матовое стекло поверх размытых фото товаров',
    'bauhaus': 'Bauhaus — геометрия: красный, синий, жёлтый, круги и квадраты',
    'news': 'Newspaper — газета: серая бумага, антиква, полутоновые фото',
    'chalk': 'Chalk — школьная доска: мел, рисованные дудлы, «дрожащие» линии',
    'receipt': 'Receipt — кассовый чек: термобумага, моноширинный шрифт, штрихкод',
    'vapor': 'Vaporwave — закатное солнце, неоновая сетка, хромированный текст',
    'lux': 'Luxury — чёрный и золото, тонкий шрифт, много воздуха',
    'comic': 'Comic — поп-арт: жёлтый фон с растром, обводки, взрыв-звезда',
}

HEAD = ['.s1 .wm', '.s2 .w', '.s2 .all', '.s3 .num', '.s3 .lbl', '.s4 .ttl', '.s5 h2', '.s6 .ttl', '.s7 .big', '.s7 .sub', '.s7 h3', '.s8 .wm', '.s8 h2', '.ring .c b']
UI = ['.nd', '.pn', '.chip', '.pill', '.fm', '.go', '.bub', '.tr', '.sr', '.fl2', '.hud', '.s5 p', '.s5 .k', '.s7 .rt2 p', '.s8 .btn', '.s8 .url', '.ring .c small', '.s1 .tg', '.ty', '.s8 .fn', '.fn7']
SIZE_KEYS = {'wm': ['.s1 .wm', '.s8 .wm'], 'w': ['.s2 .w'], 'all': ['.s2 .all'], 'num': ['.s3 .num'], 'lbl': ['.s3 .lbl'], 'ttl': ['.s4 .ttl'], 'h2': ['.s5 h2'],
             'ttl2': ['.s6 .ttl'], 'big': ['.s7 .big'], 'sub': ['.s7 .sub'], 'h3': ['.s7 .rt2 h3'], 'end': ['.s8 h2'], 'ring': ['.ring .c b']}


def theme(n, *, bg, t, m, head, ui, hw=800, ls='-.04em', tt='none', gt='none', gtc=None, mark=None, glow='none',
          card='#fff', cfg=None, crad='20px', csh='none', hdr='rgba(0,0,0,.1)', hb=None, field='#f2f2f2', fsh='none', frad='10px',
          btn=None, btnfg='#fff', brad='12px', bsh='none', acc='#ff3b3b', acc2=None, chip=None, chipfg=None, chsh='none', chrad='99px',
          photo_rad='14px', photo_sh='none', fl=None, ctr=None, sh=None, dots='rgba(0,0,0,.12)', blobs=None, grain=.06, vig='none', hud=None, sizes=None, end=None):
    S = f'.s-{n}'
    cfg, hb, btn, acc2, chip, chipfg = cfg or t, hb or acc, btn or acc, acc2 or acc, chip or card, chipfg or cfg or t
    ctr, sh, hud, end = ctr or bg, sh or bg, hud or m, end or bg
    rgb = lambda c: ','.join(str(int(c[i:i + 2], 16)) for i in (1, 3, 5))  # noqa: E731
    gt_rule = (f'background: {gt}; -webkit-background-clip: text; background-clip: text; color: transparent;' if gt != 'none' else f'background: none; color: {gtc or acc};')
    css = [
        f"{S} {{ --bg: {bg}; --t: {t}; --m: {m}; --gr: {gt}; --d-: {head}; }}",
        f"{S} .gt {{ {gt_rule} }}",
        ', '.join(f'{S} {h}' for h in HEAD) + f" {{ font-weight: {hw}; letter-spacing: {ls}; text-transform: {tt}; }}",
        ', '.join(f'{S} {u}' for u in UI) + f" {{ font-family: {ui}; }}",
        f"{S} .mk path {{ fill: {mark or t}; }} {S} .s1 .glow {{ background: {glow}; }}",
        f"{S} .grain {{ opacity: {grain}; }} {S} .vig {{ background: {vig}; }}",
        f"{S} .nd, {S} .pn {{ background: {card}; color: {cfg}; border-radius: {crad}; box-shadow: {csh}; }}",
        f"{S} .nd .h {{ border-bottom-color: {hdr}; }} {S} .nd .h b {{ background: {hb} !important; color: #fff !important; }} {S} .pn .k i {{ background: {acc} !important; }}",
        f"{S} .fm span {{ background: {field}; box-shadow: {fsh}; border-radius: {frad}; }} {S} .fm em {{ color: {m}; }}",
        f"{S} .go {{ background: {btn}; color: {btnfg}; border-radius: {brad}; box-shadow: {bsh}; }}",
        f"{S} .edg path {{ stroke: {cfg if card != 'transparent' else t}; }} {S} .edg .e2 {{ stroke: {acc}; filter: none; }} {S} .port0 {{ background: {t}; box-shadow: none; }}",
        f"{S} .chip {{ background: {chip}; color: {chipfg}; border-radius: {chrad}; box-shadow: {chsh}; font-family: {ui}; }} {S} .chip i {{ background: {acc} !important; }} {S} .r0, {S} .r3 {{ opacity: .4; filter: none; }}",
        f"{S} .s3 .ctr {{ background: radial-gradient(ellipse 60% 55% at center, rgba({rgb(ctr)},.97) 40%, rgba({rgb(ctr)},.75) 60%, transparent 80%); }} {S} .s4 .grid {{ background: radial-gradient({dots} 1.7px, transparent 2.1px) 0 0 / 34px 34px; }}",
        f"{S} .fr {{ border-radius: {photo_rad}; box-shadow: {photo_sh}; }} {S} .fl2 {{ background: {cfg if card != 'transparent' else '#000'}; color: {card if card not in ('transparent',) and not card.startswith('rgba') else '#fff'}; }}",
        f"{S} .pill {{ background: {chip}; color: {chipfg}; border-radius: {chrad}; box-shadow: {chsh}; }}",
        f"{S} .s5 .sh {{ background: linear-gradient(90deg, rgba({rgb(sh)},.97) 26%, rgba({rgb(sh)},.6) 52%, transparent 72%); }} {S} .s5 .k {{ color: {acc2}; }} {S} .s5 p {{ color: {t}; }} {S} .wc {{ border-radius: {photo_rad}; box-shadow: {photo_sh}; }}",
        f"{S} .tr small {{ color: {m}; }} {S} .tr em {{ color: {acc}; }} {S} .bub {{ background: {btn}; color: {btnfg}; border-radius: {brad}; }} {S} .ty {{ color: {cfg}; }} {S} .ty.tyc::after {{ color: {acc}; }}",
        f"{S} .win {{ background: {acc}; color: #fff; }} {S} .sr span, {S} .sr b {{ color: {cfg}; }} {S} .sr .t {{ background: rgba(128,128,128,.18); }} {S} .sr .t i {{ background: {acc2}; }} {S} .sr.best b, {S} .sr.best span {{ color: {acc}; }}",
        f"{S} .ring .bgc {{ stroke: rgba(128,128,128,.2); }} {S} .ring .fg {{ stroke: {acc}; }} {S} .ring .c small {{ color: {m}; }} {S} .s7 .rt2 p {{ color: {t}; }}",
        f"{S} .s8 .btn {{ background: {btn}; color: {btnfg}; border-radius: {brad}; box-shadow: {bsh}; }} {S} .s8 .url {{ color: {t}; border-radius: {brad}; box-shadow: inset 0 0 0 2px {t}; }} {S} .s8 .fn, {S} .fn7 {{ color: {m}; }} {S} .end {{ background: {end}; }}",
        f"{S} .hud {{ color: {hud}; }} {S} .hud .l {{ color: {t}; }} {S} .hud .p {{ background: rgba(128,128,128,.25); }} {S} .hud .p i {{ background: {acc}; }}",
        f"{S} .fl {{ background: {fl or acc} !important; }} {S} .bar {{ background: {acc}; }}",
    ]
    if blobs:
        css.append(f"{S} .bg .a {{ background: {blobs[0]} !important; }} {S} .bg .b {{ background: {blobs[1]} !important; }} {S} .bg .c {{ background: {blobs[2]} !important; }} {S} .bg i {{ mix-blend-mode: normal; }}")
    else:
        css.append(f"{S} .bg {{ display: none; }}")
    for k, v in (sizes or {}).items():
        css.append(', '.join(f'{S} {sel}' for sel in SIZE_KEYS[k]) + f' {{ font-size: {v}px; }}')
    return '\n'.join(css) + '\n'


def x(n, css):  # style-specific extras: @ → .s-<n>
    return css.replace('@', f'.s-{n} ') + '\n'


PF, SERIF, NUN, MAN, MONO, INTER = "'Playfair Display', serif", "'PT Serif', serif", "'Nunito', sans-serif", "'Manrope', sans-serif", "'IBM Plex Mono', monospace", "'Inter', sans-serif"

CSS = ''
# 1 · Editorial
CSS += theme('editorial', bg='#f4f1ea', t='#111111', m='#6b6b6b', head=PF, ui=INTER, hw=900, ls='-.02em', gtc='#c8102e', card='#fbfaf6', crad='0',
             csh='0 0 0 1.5px #111', hdr='#111', hb='#111', field='#fff', fsh='inset 0 0 0 1px #111', frad='0', btn='#111', brad='0', acc='#c8102e', acc2='#111',
             chip='transparent', chipfg='#111', chsh='inset 0 -2px 0 #111', chrad='0', photo_rad='0', photo_sh='0 0 0 1.5px #111', fl='#111',
             sizes=dict(wm=150, w=250, all=150, num=360, lbl=58, ttl=84, h2=160, ttl2=76, big=400, sub=56, h3=110, end=90, ring=110))
CSS += x('editorial', """
@.gt { font-style: italic; } @.s4 .ttl, @.s6 .ttl { top: 134px; } .s-editorial #st::before { content: ''; position: absolute; inset: 0; background: linear-gradient(#111, #111) 64px 104px / calc(100% - 128px) 3px no-repeat, linear-gradient(#111, #111) 64px 110px / calc(100% - 128px) 1px no-repeat, linear-gradient(#111, #111) 64px calc(100% - 104px) / calc(100% - 128px) 1px no-repeat; }
@.chip { font-family: 'Playfair Display', serif; font-style: italic; font-weight: 700; } @.chip i { border-radius: 0; } @.hud .l { font-family: 'Playfair Display', serif; font-weight: 900; }
@.s5 .k { letter-spacing: .3em; } @.s3 .lbl, @.s7 .sub { font-style: italic; font-weight: 400; }""")
# 2 · Clay
CLAY = 'inset -10px -10px 20px rgba(60,40,140,.12), inset 10px 10px 20px rgba(255,255,255,.95), 20px 26px 44px rgba(80,60,160,.28)'
CSS += theme('clay', bg='#e9e4ff', t='#2b2451', m='#7a74a8', head=NUN, ui=NUN, hw=900, ls='-.02em', gtc='#ff6f9f', card='#f6f3ff', crad='42px', csh=CLAY,
             hdr='rgba(43,36,81,.08)', hb='#8f7bff', field='#ece8ff', fsh='inset 3px 3px 6px rgba(60,40,140,.12), inset -3px -3px 6px #fff', frad='16px',
             btn='#ff7aa8', brad='26px', bsh='inset -5px -5px 10px rgba(150,30,80,.25), inset 5px 5px 10px rgba(255,255,255,.5), 10px 14px 24px rgba(255,90,150,.35)', acc='#ff6f9f', acc2='#8f7bff',
             chip='#fff', chipfg='#2b2451', chsh=CLAY, photo_rad='34px', photo_sh=CLAY, fl='#fff', blobs=('#cfc6ff', '#bff0dc', '#ffd6c2'), grain=.03,
             sizes=dict(wm=150, w=270, all=160, num=370, lbl=62, ttl=86, h2=170, ttl2=78, big=410, sub=58, h3=110, end=92, ring=110))
CSS += x('clay', """
@.s1 .wm, @.s2 .w, @.s2 .all, @.s3 .num, @.s5 h2, @.s7 .big, @.s8 .wm, @.s8 h2, @.s4 .ttl, @.s6 .ttl, @.s7 h3 { text-shadow: 0 6px 0 #cbbff8, 0 12px 0 #b6a8f2, 0 22px 30px rgba(80,60,160,.3); }
@.mk { filter: drop-shadow(0 8px 0 #b6a8f2) drop-shadow(0 18px 20px rgba(80,60,160,.35)); } @.mk path { fill: #8f7bff; } @.bg i { opacity: .9 !important; filter: blur(110px); }
@.ring .fg { stroke-linecap: round; } @.s8 .url { box-shadow: inset 0 0 0 3px #2b2451; }""")
# 3 · Glass
GL = 'inset 0 0 0 1.5px rgba(255,255,255,.35), inset 0 1px 0 rgba(255,255,255,.6), 0 30px 60px -20px rgba(0,0,0,.5)'
CSS += theme('glass', bg='#0c0c14', t='#ffffff', m='rgba(255,255,255,.72)', head="'Onest', sans-serif", ui=INTER, gt='linear-gradient(95deg, #ffffff 30%, #ffd1f0 70%, #c9f5ff)',
             card='rgba(255,255,255,.13)', cfg='#fff', crad='30px', csh=GL, hdr='rgba(255,255,255,.18)', hb='rgba(255,255,255,.25)', field='rgba(255,255,255,.12)',
             fsh='inset 0 0 0 1px rgba(255,255,255,.25)', frad='12px', btn='rgba(255,255,255,.92)', btnfg='#111', brad='99px', acc='#ff9ad5', acc2='#9ae8ff',
             chip='rgba(255,255,255,.14)', chipfg='#fff', chsh=GL, photo_rad='22px', photo_sh=GL, fl='#fff', ctr='#1c1830', sh='#15131f', dots='rgba(255,255,255,.14)',
             vig='radial-gradient(ellipse at center, transparent 50%, rgba(0,0,0,.5))')
CSS += x('glass', """
.s-glass #st::before { content: ''; position: absolute; inset: -12%; background: url(../landing/assets/ol/bunny.webp) 8% 20% / 42% no-repeat, url(../landing/assets/ol/coffee.webp) 92% 25% / 40% no-repeat,
  url(../landing/assets/ol/airbuds.webp) 55% 105% / 45% no-repeat, linear-gradient(135deg, #3a2a7a, #0f4d5a); filter: blur(60px) saturate(1.5) brightness(.8); }
@.nd, @.pn, @.chip, @.pill, @.bub, @.s8 .url { -webkit-backdrop-filter: blur(26px) saturate(1.6); backdrop-filter: blur(26px) saturate(1.6); } @.s8 .url { box-shadow: inset 0 0 0 1.5px rgba(255,255,255,.5); background: rgba(255,255,255,.12); }
@.bub { color: #111; } @.ring .bgc { stroke: rgba(255,255,255,.18); } @.s3 .ctr { background: radial-gradient(ellipse 55% 50% at center, rgba(20,16,40,.5) 30%, transparent 75%); }""")
# 4 · Bauhaus
BR, BB, BY = '#e63b2e', '#1f4ea3', '#f5c21b'
CSS += theme('bauhaus', bg='#f0e9d8', t='#111111', m='#5b5448', head="'Rubik Mono One', sans-serif", ui="'Rubik', sans-serif", hw=400, ls='-.02em', tt='uppercase', gtc=BR,
             card='#fff', crad='0', csh='0 0 0 4px #111', hdr='#111', hb=BB, field='#f0e9d8', fsh='inset 0 0 0 2px #111', frad='0', btn=BR, brad='0',
             acc=BR, acc2=BB, chip='#fff', chipfg='#111', chsh='inset 0 0 0 3px #111', chrad='0', photo_rad='0', photo_sh='0 0 0 4px #111', fl=BY,
             sizes=dict(wm=110, w=170, all=104, num=280, lbl=40, ttl=56, h2=104, ttl2=52, big=300, sub=40, h3=72, end=60, ring=80))
CSS += x('bauhaus', f"""
.s-bauhaus #st::before {{ content: ''; position: absolute; inset: 0; background: radial-gradient(circle at 1720px 180px, {BY} 0 260px, transparent 261px), radial-gradient(circle at 0 1080px, {BB} 0 330px, transparent 331px),
  linear-gradient({BR}, {BR}) 1560px 820px / 210px 210px no-repeat, linear-gradient(#111, #111) 110px 120px / 8px 300px no-repeat; }}
@.nd .h {{ background: {BB}; color: #fff; }} @.pn .k {{ margin: -30px -30px 20px; padding: 14px 30px; background: {BB}; color: #fff; }} @.chip i {{ border-radius: 50%; }}
@.chip:nth-child(3n) i {{ background: {BB} !important; border-radius: 0; }} @.chip:nth-child(3n+1) i {{ background: {BY} !important; }} @.ring .fg {{ stroke-linecap: butt; }} @.s8 .url {{ box-shadow: inset 0 0 0 4px #111; }}""")
# 5 · Newspaper
HT = 'grayscale(1) contrast(1.35) brightness(1.05)'
CSS += theme('news', bg='#ece8de', t='#151515', m='#5d5a53', head=SERIF, ui=SERIF, hw=700, ls='-.02em', gtc='#151515', card='#f4f1e8', crad='0',
             csh='0 -6px 0 -3px #151515, 0 0 0 1px #151515', hdr='#151515', hb='#151515', field='#fff', fsh='inset 0 0 0 1px #151515', frad='0', btn='#151515', brad='0',
             acc='#151515', acc2='#b3261e', chip='#f4f1e8', chipfg='#151515', chsh='inset 0 0 0 1px #151515', chrad='0', photo_rad='0', photo_sh='0 0 0 1px #151515', fl='#fff', grain=.3,
             sizes=dict(wm=150, w=250, all=150, num=360, lbl=58, ttl=84, h2=160, ttl2=76, big=400, sub=56, h3=110, end=90, ring=110))
CSS += x('news', f"""
@.s4 .ttl, @.s6 .ttl {{ top: 134px; }} @.gt {{ font-style: italic; text-decoration: underline; text-decoration-thickness: 6px; text-underline-offset: 12px; }} @.grain {{ mix-blend-mode: multiply; }}
@.fr > i, @.wc, @.tr > i, @.cp2 i, @.n1 .im {{ filter: {HT}; }} @.fr::before {{ filter: blur(18px) {HT}; }}
.s-news #st::before {{ content: ''; position: absolute; inset: 0; background: linear-gradient(#151515, #151515) 64px 100px / calc(100% - 128px) 4px no-repeat, linear-gradient(#151515, #151515) 64px 108px / calc(100% - 128px) 1px no-repeat; }}
@.hud .l {{ font: 700 26px 'PT Serif', serif; letter-spacing: .02em; }} @.hud .l::after {{ content: ' · ВЕСТНИК КОНТЕНТА'; font-weight: 400; font-style: italic; }} @.sr .t i {{ background: #151515; }} @.s5 .k {{ color: #b3261e; }}""")
# 6 · Chalk
CH = '#f4f1e4'
CSS += theme('chalk', bg='#22392c', t=CH, m='#b9c7b9', head="'Caveat', cursive", ui="'Pangolin', cursive", hw=700, ls='0', gt='linear-gradient(transparent 58%, rgba(255,214,102,.55) 58%, rgba(255,214,102,.55) 88%, transparent 88%)', gtc=CH,
             card='transparent', cfg=CH, crad='20px', csh='none', hdr='rgba(244,241,228,.6)', hb='transparent', field='transparent', fsh='inset 0 0 0 2px rgba(244,241,228,.7)', frad='10px',
             btn='transparent', btnfg=CH, brad='16px', bsh='inset 0 0 0 3px #ffd666', acc='#ffd666', acc2='#ff9bb0', chip='transparent', chipfg=CH, chsh='inset 0 0 0 3px rgba(244,241,228,.8)',
             photo_rad='3px', photo_sh='0 0 0 9px #f4f1e4, 8px 14px 20px 9px rgba(0,0,0,.35)', fl=CH, grain=.22, vig='radial-gradient(ellipse at center, transparent 45%, rgba(0,0,0,.55))',
             sizes=dict(wm=210, w=330, all=210, num=440, lbl=90, ttl=112, h2=210, ttl2=104, big=470, sub=84, h3=150, end=128, ring=150))
CSS += x('chalk', f"""
@.gt {{ -webkit-background-clip: border-box; background-clip: border-box; color: {CH}; }} @.grain {{ mix-blend-mode: screen; }} @.dds {{ display: block; }} @.dd {{ --c: #f4f1e4 !important; }} @.dd:nth-child(3n) {{ --c: #ffd666 !important; }} @.dd:nth-child(3n+1) {{ --c: #ff9bb0 !important; }} @.ddt {{ color: #ffd666; }}
@.mk {{ filter: url(#rough); }} @.mk path {{ fill: none; stroke: {CH}; stroke-width: 2.4; }} @.s1 .wm, @.s2 .w, @.s2 .all, @.s3 .num, @.s5 h2, @.s7 .big, @.s8 .wm, @.s8 h2 {{ filter: url(#rough); text-shadow: 0 0 2px rgba(244,241,228,.6); }}
@.nd, @.pn {{ isolation: isolate; }} @.nd::before, @.pn::before {{ content: ''; position: absolute; inset: 0; z-index: -1; border-radius: 22px 18px 26px 16px; box-shadow: 0 0 0 3.5px rgba(244,241,228,.9); filter: url(#rough); }}
@.chip, @.pill, @.go, @.s8 .btn, @.s8 .url, @.edg, @.ring svg, @.bar {{ filter: url(#rough); }} @.nd .h b {{ box-shadow: 0 0 0 2px {CH}; }} @.bub {{ box-shadow: inset 0 0 0 3px #ffd666; }} @.ty {{ font: 700 40px/1.15 'Caveat', cursive; }}
@.tr em {{ font: 700 44px 'Caveat', cursive; }} @.sr .t {{ background: transparent; box-shadow: inset 0 0 0 2px rgba(244,241,228,.7); }} @.sr .t i {{ background: repeating-linear-gradient(45deg, #ffd666 0 3px, transparent 3px 8px); }}
@.s8 .url {{ box-shadow: inset 0 0 0 3px {CH}; }} @.win {{ color: #22392c; }} @.hud .l {{ font: 700 38px 'Caveat', cursive; }}""")
# 7 · Receipt
CSS += theme('receipt', bg='#f7f5ef', t='#1b1b1b', m='#6d6a64', head=MONO, ui=MONO, hw=600, ls='-.03em', tt='uppercase', gtc='#f7f5ef', card='#fffefb', crad='0',
             csh='0 0 0 2px #1b1b1b', hdr='#1b1b1b', hb='#1b1b1b', field='transparent', fsh='inset 0 -2px 0 #1b1b1b', frad='0', btn='#1b1b1b', brad='0', acc='#1b1b1b', acc2='#1b1b1b',
             chip='#fffefb', chipfg='#1b1b1b', chsh='inset 0 0 0 2px #1b1b1b', chrad='0', photo_rad='0', photo_sh='0 0 0 2px #1b1b1b', fl='#1b1b1b', grain=.1,
             sizes=dict(wm=120, w=200, all=120, num=300, lbl=44, ttl=64, h2=120, ttl2=58, big=330, sub=44, h3=84, end=70, ring=90))
CSS += x('receipt', """
@.gt { background: #1b1b1b; color: #f7f5ef; padding: 0 .1em; } @.s4 .ttl, @.s6 .ttl { top: 134px; } .s-receipt #st::before { content: ''; position: absolute; inset: 0; background: repeating-linear-gradient(90deg, #1b1b1b 0 10px, transparent 10px 20px) 64px 110px / calc(100% - 128px) 2px no-repeat,
  repeating-linear-gradient(90deg, #1b1b1b 0 10px, transparent 10px 20px) 64px calc(100% - 110px) / calc(100% - 128px) 2px no-repeat; }
@.nd, @.pn { box-shadow: 0 0 0 2px #1b1b1b; -webkit-mask: linear-gradient(#000, #000) top / 100% calc(100% - 14px) no-repeat, conic-gradient(from -45deg at bottom, transparent 90deg, #000 0) bottom / 28px 14px repeat-x;
  mask: linear-gradient(#000, #000) top / 100% calc(100% - 14px) no-repeat, conic-gradient(from -45deg at bottom, transparent 90deg, #000 0) bottom / 28px 14px repeat-x; }
@.fr > i, @.wc, @.tr > i, @.cp2 i, @.n1 .im { filter: grayscale(1) contrast(1.4); } @.fr::before { filter: blur(18px) grayscale(1); }
@.sr .t { background: transparent; box-shadow: inset 0 0 0 2px #1b1b1b; } @.sr .t i { background: repeating-linear-gradient(90deg, #1b1b1b 0 6px, transparent 6px 9px); } @.ring .fg { stroke-linecap: butt; } @.ring .bgc { stroke: rgba(27,27,27,.12); stroke-dasharray: 6 10; }
@.s8 .fn::before { content: ''; display: block; width: 520px; height: 80px; margin: 0 auto 16px; background: repeating-linear-gradient(90deg, #1b1b1b 0 4px, transparent 4px 7px, #1b1b1b 7px 9px, transparent 9px 13px, #1b1b1b 13px 18px, transparent 18px 21px, #1b1b1b 21px 22px, transparent 22px 27px); }
@.s8 .fn { bottom: 40px; } @.hud .l::after { content: ' · ЧЕК №0001'; font-weight: 400; } @.s3 .lbl::before { content: '= '; } @.s7 .sub::before { content: 'ИТОГО: '; }""")
# 8 · Vaporwave
VP, VC = '#ff6ec7', '#00f0ff'
CSS += theme('vapor', bg='#1a0b3d', t='#ffffff', m='#d5b8ff', head="'Russo One', sans-serif", ui="'Russo One', sans-serif", hw=400, ls='.01em', tt='uppercase',
             gt=f'linear-gradient(180deg, #e8fbff 20%, #8a6bff 52%, {VP} 53%, #ffd1ec 90%)', card='rgba(40,12,80,.82)', cfg='#fff', crad='10px',
             csh=f'0 0 0 2px {VC}, 0 0 40px rgba(0,240,255,.35)', hdr='rgba(0,240,255,.4)', hb=VP, field='rgba(255,255,255,.08)', fsh=f'inset 0 0 0 1px rgba(0,240,255,.5)', frad='6px',
             btn=VP, brad='8px', bsh='0 0 30px rgba(255,110,199,.6)', acc=VP, acc2=VC, chip='rgba(40,12,80,.8)', chipfg='#fff', chsh=f'inset 0 0 0 2px {VC}', chrad='8px',
             photo_rad='8px', photo_sh=f'0 0 0 3px {VP}, 0 0 40px rgba(255,110,199,.5)', fl=VP, ctr='#1a0b3d', sh='#1a0b3d', dots='rgba(0,240,255,.2)',
             sizes=dict(wm=140, w=230, all=140, num=320, lbl=52, ttl=70, h2=130, ttl2=64, big=340, sub=50, h3=90, end=80, ring=96))
CSS += x('vapor', f"""
.s-vapor #st {{ background: linear-gradient(180deg, #1a0b3d 0%, #4a1a7a 45%, #ff6ec7 62%, #2a0a4a 62.2%, #12052a 100%); }}
.s-vapor #st::before {{ content: ''; position: absolute; left: -50%; right: -50%; bottom: -8%; height: 46%; background: linear-gradient({VP} 2px, transparent 2px) 0 0 / 100% 70px, linear-gradient(90deg, {VP} 2px, transparent 2px) 0 0 / 110px 100%; transform: perspective(500px) rotateX(62deg); transform-origin: 50% 100%; opacity: .7; }}
@.bg .b, @.bg .c {{ display: none; }} @.bg {{ display: block; }} @.bg .a {{ left: 1400px !important; top: 40px !important; width: 460px; height: 460px; background: linear-gradient(#ffe36b, {VP} 75%) !important; filter: none; mix-blend-mode: normal; opacity: .95 !important;
  -webkit-mask: linear-gradient(#000 52%, transparent 52% 56%, #000 56% 64%, transparent 64% 69%, #000 69% 76%, transparent 76% 83%, #000 83% 89%, transparent 89%); mask: linear-gradient(#000 52%, transparent 52% 56%, #000 56% 64%, transparent 64% 69%, #000 69% 76%, transparent 76% 83%, #000 83% 89%, transparent 89%); }}
@.s2 .w, @.s2 .all, @.s3 .num, @.s5 h2, @.s7 .big, @.s8 .wm, @.s8 h2, @.s1 .wm {{ filter: drop-shadow(4px 4px 0 {VC}) drop-shadow(0 0 24px rgba(255,110,199,.6)); }}
@.mk path {{ fill: #e8fbff; }} @.mk {{ filter: drop-shadow(4px 4px 0 {VC}); }} @.vig {{ background: repeating-linear-gradient(0deg, rgba(0,0,0,.18) 0 2px, transparent 2px 4px); }} @.s8 .url {{ box-shadow: inset 0 0 0 2px {VC}; }} @.hud .l {{ color: {VC}; }}""")
# 9 · Luxury
GD = '#c9a45c'
CSS += theme('lux', bg='#0b0b0b', t='#f1e9da', m='#8c8475', head=MAN, ui=MAN, hw=200, ls='-.03em', gt='linear-gradient(100deg, #f3e2b8 10%, #c9a45c 50%, #8a6a2c 90%)', card='#111111', cfg='#f1e9da',
             crad='2px', csh=f'0 0 0 1px {GD}', hdr='rgba(201,164,92,.35)', hb='transparent', field='transparent', fsh='inset 0 -1px 0 rgba(201,164,92,.6)', frad='0', btn='transparent', btnfg=GD, brad='0',
             bsh=f'inset 0 0 0 1px {GD}', acc=GD, acc2=GD, chip='transparent', chipfg='#f1e9da', chsh='inset 0 0 0 1px rgba(201,164,92,.6)', chrad='0', photo_rad='2px', photo_sh=f'0 0 0 1px {GD}',
             fl=GD, grain=.05, vig='radial-gradient(ellipse at center, transparent 50%, rgba(0,0,0,.7))',
             sizes=dict(wm=140, w=270, all=150, num=380, lbl=56, ttl=80, h2=160, ttl2=74, big=420, sub=52, h3=110, end=86, ring=120))
CSS += x('lux', f"""
.s-lux #st::before {{ content: ''; position: absolute; inset: 44px; box-shadow: inset 0 0 0 1px rgba(201,164,92,.35); }} @.mk path {{ fill: {GD}; }}
@.s3 .lbl, @.s7 .sub, @.s5 .k, @.pn .k, @.nd .h {{ letter-spacing: .28em; font-weight: 300; text-transform: uppercase; }} @.s3 .lbl, @.s7 .sub {{ font-size: 34px; }} @.nd .h b {{ box-shadow: 0 0 0 1px {GD}; color: {GD} !important; }}
@.chip {{ font-weight: 300; letter-spacing: .06em; }} @.go, @.s8 .btn {{ letter-spacing: .2em; text-transform: uppercase; font-weight: 500; }} @.s8 .url {{ box-shadow: inset 0 0 0 1px rgba(241,233,218,.4); font-weight: 300; }}
@.sr .t {{ height: 4px; }} @.ring circle {{ stroke-width: 6; }} @.hud .l {{ letter-spacing: .3em; font-weight: 300; }}""")
# 10 · Comic
CSS += theme('comic', bg='#ffe14a', t='#111111', m='#3a3210', head="'Rubik', sans-serif", ui="'Rubik', sans-serif", hw=900, ls='-.02em', tt='uppercase', gtc='#ff3b3b', card='#fff', crad='22px',
             csh='0 0 0 5px #111, 12px 12px 0 #111', hdr='#111', hb='#ff3b3b', field='#fff', fsh='inset 0 0 0 3px #111', frad='12px', btn='#ff3b3b', brad='16px', bsh='0 0 0 4px #111, 6px 6px 0 #111',
             acc='#ff3b3b', acc2='#2a6bff', chip='#fff', chipfg='#111', chsh='0 0 0 4px #111, 5px 5px 0 #111', chrad='99px', photo_rad='16px', photo_sh='0 0 0 5px #111, 10px 10px 0 #111', fl='#fff',
             sizes=dict(wm=150, w=250, all=150, num=360, lbl=58, ttl=82, h2=150, ttl2=76, big=400, sub=54, h3=104, end=86, ring=106))
CSS += x('comic', """
.s-comic #st::before { content: ''; position: absolute; inset: 0; background: radial-gradient(circle, rgba(255,59,59,.5) 4px, transparent 4.5px) 0 0 / 22px 22px; -webkit-mask: linear-gradient(120deg, #000, transparent 55%); mask: linear-gradient(120deg, #000, transparent 55%); }
@.s1 .wm, @.s2 .w, @.s2 .all, @.s3 .num, @.s5 h2, @.s7 .big, @.s8 .wm, @.s8 h2, @.s4 .ttl, @.s6 .ttl, @.s7 h3, @.s3 .lbl, @.s7 .sub { color: #fff; -webkit-text-stroke: 5px #111; paint-order: stroke fill; text-shadow: 8px 8px 0 #111; }
@.gt { -webkit-text-stroke: 5px #111; } @.s3 .lbl, @.s7 .sub { -webkit-text-stroke: 3px #111; text-shadow: 5px 5px 0 #111; }
@.s7 .a1::before { content: ''; position: absolute; left: 50%; top: 50%; width: 1100px; height: 1100px; margin: -560px 0 0 -550px; background: #2a6bff; clip-path: polygon(50% 0, 58% 32%, 85% 12%, 70% 40%, 100% 45%, 71% 58%, 90% 88%, 60% 70%, 50% 100%, 40% 70%, 10% 88%, 29% 58%, 0 45%, 30% 40%, 15% 12%, 42% 32%); }
@.s7 .a1 > :not(.fn7) { position: relative; } @.mk path { fill: #111; } @.bub { position: relative; box-shadow: 0 0 0 4px #111; } @.bub::after { content: ''; position: absolute; right: 30px; bottom: -22px; border: 12px solid transparent; border-top: 16px solid #111; }
@.s8 .url { box-shadow: 0 0 0 4px #111, 6px 6px 0 #111; background: #fff; } @.sr .t { box-shadow: inset 0 0 0 3px #111; } @.fn7 { color: #111 !important; }""")
