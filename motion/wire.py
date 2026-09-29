"""Wireframe vector stand-ins for the product photos in oneflow-clean: a card layout sketched in lines (title bars,
feature chips, price tag) with the product drawn as outline art inside a dashed selection box with corner handles.

css_vars() → ':root { --w-bunny: url(data:image/svg+xml;base64,…); … }' — pages use background-image: var(--w-<name>).
"""
import base64

INK, BLUE, BAR = '#5a6690', '#3b5cff', '#d5dcf4'
TINT = {'bunny': '#f7f0f6', 'coffee': '#f6f2ec', 'airbuds': '#eef2ff', 'watch': '#edf3fb', 'speaker': '#fbefef', 'blender': '#eef8f3',
        'pajama': '#f7f0fb', 'robot': '#eef5fb', 'hoodie': '#f2f2f8', 'pyramid': '#f8f4ea', 'airfryer': '#f1f4f0', 'powerbank': '#eef1fb',
        'toothbrush': '#edf7f8', 'body': '#faf1ec'}

# product outline art in a 200×220 box (drawn at x 175–375, y 110–330 of the 400×400 card)
ART = {
    'bunny': '<ellipse cx="78" cy="48" rx="15" ry="46" transform="rotate(-12 78 48)"/><ellipse cx="122" cy="48" rx="15" ry="46" transform="rotate(12 122 48)"/>'
             '<ellipse cx="78" cy="48" rx="6" ry="30" transform="rotate(-12 78 48)" class="a"/><ellipse cx="122" cy="48" rx="6" ry="30" transform="rotate(12 122 48)" class="a"/>'
             '<ellipse cx="100" cy="165" rx="58" ry="52"/><circle cx="100" cy="105" r="44"/><circle cx="85" cy="100" r="4" class="d"/><circle cx="115" cy="100" r="4" class="d"/>'
             '<path d="M94 116 L100 121 L106 116"/><path d="M100 145 L76 132 L78 158 Z M100 145 L124 132 L122 158 Z" class="a"/><ellipse cx="70" cy="205" rx="20" ry="11"/><ellipse cx="130" cy="205" rx="20" ry="11"/>',
    'coffee': '<rect x="40" y="10" width="120" height="190" rx="14"/><rect x="52" y="24" width="96" height="30" rx="6" class="a"/><circle cx="70" cy="80" r="9"/><circle cx="100" cy="80" r="9"/>'
              '<circle cx="130" cy="80" r="9" class="a"/><rect x="60" y="104" width="80" height="12" rx="4"/><path d="M92 116 V132 M108 116 V132"/>'
              '<path d="M78 150 H122 L118 184 H82 Z"/><path d="M122 158 C136 158 136 176 120 176"/><rect x="50" y="188" width="100" height="8" rx="4" class="a"/>',
    'airbuds': '<rect x="45" y="100" width="110" height="96" rx="36"/><path d="M45 136 H155" class="a"/><circle cx="100" cy="152" r="4" class="d"/>'
               '<circle cx="70" cy="46" r="22"/><rect x="80" y="54" width="14" height="46" rx="7"/><circle cx="130" cy="46" r="22"/><rect x="106" y="54" width="14" height="46" rx="7"/>'
               '<circle cx="70" cy="46" r="9" class="a"/><circle cx="130" cy="46" r="9" class="a"/>',
    'watch': '<rect x="66" y="0" width="68" height="52" rx="10"/><rect x="66" y="168" width="68" height="52" rx="10"/><rect x="46" y="44" width="108" height="132" rx="30"/>'
             '<rect x="58" y="56" width="84" height="108" rx="20" class="a"/><path d="M100 110 V82 M100 110 L118 118"/><circle cx="100" cy="110" r="4" class="d"/><rect x="154" y="92" width="8" height="26" rx="3"/>',
    'speaker': '<rect x="50" y="20" width="100" height="180" rx="48"/><circle cx="100" cy="82" r="30"/><circle cx="100" cy="82" r="14" class="a"/>'
               '<circle cx="100" cy="150" r="20"/><circle cx="100" cy="150" r="8" class="a"/><path d="M76 36 H124"/>',
    'blender': '<path d="M60 20 H140 L128 140 H72 Z"/><rect x="54" y="8" width="92" height="16" rx="6" class="a"/><path d="M140 40 C168 40 168 104 134 104"/>'
               '<path d="M84 120 L116 108 M84 108 L116 120" class="a"/><path d="M64 140 H136 L146 200 H54 Z"/><circle cx="100" cy="172" r="12" class="a"/>',
    'pajama': '<path d="M60 20 L100 34 L140 20 L178 52 L160 78 L144 68 V130 H56 V68 L40 78 L22 52 Z"/><path d="M100 34 V130" class="a"/>'
              '<circle cx="100" cy="60" r="3" class="d"/><circle cx="100" cy="86" r="3" class="d"/><circle cx="100" cy="112" r="3" class="d"/>'
              '<path d="M62 140 H138 L142 212 H108 L100 166 L92 212 H58 Z"/>',
    'robot': '<ellipse cx="100" cy="126" rx="88" ry="30"/><path d="M12 126 V140 C12 158 188 158 188 140 V126"/><ellipse cx="100" cy="118" rx="36" ry="12" class="a"/>'
             '<circle cx="100" cy="116" r="5" class="d"/><path d="M36 106 C60 96 140 96 164 106" class="a"/>',
    'hoodie': '<path d="M70 30 C70 6 130 6 130 30 L170 50 L188 150 L160 154 L150 90 V210 H50 V90 L40 154 L12 150 L30 50 Z"/>'
              '<path d="M70 30 C76 58 124 58 130 30" class="a"/><path d="M92 52 V82 M108 52 V82"/><rect x="68" y="140" width="64" height="36" rx="8" class="a"/>',
    'pyramid': '<path d="M100 10 L190 190 H10 Z"/><path d="M100 10 L120 190" class="a"/><path d="M40 130 H160" stroke-dasharray="6 8"/>'
               '<rect x="84" y="150" width="32" height="40" rx="6"/><circle cx="100" cy="162" r="5" class="d"/>',
    'airfryer': '<path d="M44 40 C44 20 156 20 156 40 V196 H44 Z"/><rect x="70" y="36" width="60" height="24" rx="6" class="a"/>'
                '<rect x="56" y="96" width="88" height="90" rx="12"/><rect x="84" y="128" width="32" height="12" rx="6" class="a"/><circle cx="100" cy="76" r="6"/>',
    'powerbank': '<rect x="56" y="20" width="88" height="170" rx="18"/><circle cx="84" cy="160" r="5" class="d"/><circle cx="100" cy="160" r="5" class="d"/>'
                 '<circle cx="116" cy="160" r="5"/><path d="M104 60 L90 92 H106 L96 124" class="a"/><path d="M100 190 V206 C100 222 150 222 150 204 V180"/>',
    'toothbrush': '<rect x="88" y="70" width="24" height="146" rx="12"/><rect x="92" y="8" width="16" height="66" rx="8"/>'
                  '<path d="M84 14 V56 M78 18 V52 M72 22 V48" class="a"/><circle cx="100" cy="120" r="5" class="d"/>',
    'body': '<path d="M70 70 H130 V204 C130 214 70 214 70 204 Z"/><rect x="86" y="44" width="28" height="26" rx="4"/><path d="M100 44 V22 H138 V32"/>'
            '<rect x="80" y="110" width="40" height="52" rx="6" class="a"/>',
}


DEFAULT = dict(ink=INK, acc=BLUE, bar=BAR, bg=None, dot='#cdd4ea', fill='#fff', head=INK, sw=3)


def svg(name, pal=None):
    p = dict(DEFAULT, **(pal or {}))
    INK, BLUE, BAR = p['ink'], p['acc'], p['bar']  # noqa: N806
    FILL, DOT, HEAD, SW = p['fill'], p['dot'], p['head'], p['sw']  # noqa: N806
    bg = p['bg'] or TINT.get(name, '#f3f5fc')
    chips = ''.join(f'<circle cx="46" cy="{y}" r="13" fill="{FILL}" stroke="{INK}" stroke-width="2"/><rect x="66" y="{y - 9}" width="{w}" height="7" rx="3.5" fill="{BAR}"/>'
                    f'<rect x="66" y="{y + 3}" width="{w - 22}" height="6" rx="3" fill="{BAR}" opacity=".7"/>' for y, w in ((168, 74), (226, 64), (284, 80)))
    handles = ''.join(f'<rect x="{x - 5}" y="{y - 5}" width="10" height="10" fill="{FILL}" stroke="{BLUE}" stroke-width="2"/>' for x, y in ((165, 100), (385, 100), (165, 340), (385, 340)))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" viewBox="0 0 400 400">'
            f'<defs><pattern id="g" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1.2" fill="{DOT}"/></pattern>'
            f'<style>.art *{{fill:{FILL};stroke:{INK};stroke-width:{SW};stroke-linejoin:round;stroke-linecap:round}}.art .a{{fill:none;stroke:{BLUE}}}.art .d{{fill:{INK};stroke:none}}</style></defs>'
            f'<rect width="400" height="400" fill="{bg}"/><rect width="400" height="400" fill="url(#g)"/>'
            f'<rect x="30" y="32" width="230" height="22" rx="11" fill="{HEAD}" opacity=".85"/><rect x="30" y="66" width="160" height="10" rx="5" fill="{BAR}"/>'
            f'{chips}<rect x="30" y="336" width="104" height="36" rx="10" fill="{BLUE}"/><rect x="46" y="350" width="60" height="8" rx="4" fill="{FILL}" opacity=".9"/>'
            f'<rect x="165" y="100" width="220" height="240" fill="none" stroke="{BLUE}" stroke-width="1.6" stroke-dasharray="7 6" opacity=".7"/>{handles}'
            f'<g class="art" transform="translate(175 110)">{ART[name]}</g></svg>')


def css_vars(sel=':root', pal=None):
    return sel + ' { ' + ' '.join(f'--w-{n}: url(data:image/svg+xml;base64,{base64.b64encode(svg(n, pal).encode()).decode()});' for n in ART) + ' }'


if __name__ == '__main__':  # python3 wire.py → out/wire-sheet.html (all drawings side by side)
    import os
    os.makedirs('out', exist_ok=True)
    open('out/wire-sheet.html', 'w').write('<body style="margin:0;display:flex;flex-wrap:wrap;gap:8px;background:#fff">' + ''.join(svg(n) for n in ART) + '</body>')
