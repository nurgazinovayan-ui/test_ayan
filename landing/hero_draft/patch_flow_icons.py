"""The node headers of the flow section: a small outline icon of the node's subject instead of a coloured dot
(the owner, 2026-11-20). No plate behind the icon; it keeps the node's accent colour.
python3 -I patch_flow_icons.py <ru.html> <index.html>"""
import re, sys

ICONS = {
    'n-idea': '<path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 0 0-3.6 10.800c.7.500 1.100 1.300 1.100 2.200h5c0-.900.400-1.700 1.100-2.200A6 6 0 0 0 12 3z"/>',
    'n-photo': '<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="8.500" cy="9.500" r="1.500"/><path d="M21 15.500l-4.500-4.500L7 20"/>',
    'n-text': '<path d="M5 7V4h14v3"/><path d="M12 4v16"/><path d="M9 20h6"/>',
    'n-video': '<rect x="3" y="5" width="13" height="14" rx="2"/><path d="M16 10.500l5-3v9l-5-3"/>',
    'n-adapt': '<rect x="3" y="3" width="8" height="13" rx="1.500"/><rect x="14" y="9" width="7" height="7" rx="1.500"/><path d="M4 20.500h16"/>',
    'n-done': '<circle cx="12" cy="12" r="9"/><path d="M8 12.400l2.800 2.800L16 9.600"/>',
}
CSS_SWAPS = [
    ('.flow .fl-stage svg { position: absolute;', '.flow .fl-stage > svg { position: absolute;'),
    ('.flow .fl-stage path { fill: none;', '.flow .fl-stage > svg path { fill: none;'),
    ('.flow .fl-stage path.run { stroke: #0a6cff;', '.flow .fl-stage > svg path.run { stroke: #0a6cff;'),
    ('html[data-theme="dark"] .flow .fl-stage path.run {', 'html[data-theme="dark"] .flow .fl-stage > svg path.run {'),
    ('.flow .fl-stage circle { fill: var(--bg);', '.flow .fl-stage > svg circle { fill: var(--bg);'),
    ('html[data-theme="dark"] .flow .fl-stage circle {', 'html[data-theme="dark"] .flow .fl-stage > svg circle {'),
    ('  .flow .fl-stage svg { display: none; }', '  .flow .fl-stage > svg { display: none; }'),
    ('@media (prefers-reduced-motion: reduce) { .flow .fl-stage path.run {', '@media (prefers-reduced-motion: reduce) { .flow .fl-stage > svg path.run {'),
    ('.flow .fl-nh i { width: 8px; height: 8px; border-radius: 50%; }',
     '.flow .fl-nh svg { flex: none; width: 17px; height: 17px; fill: none; stroke: currentColor; stroke-width: 1.800; stroke-linecap: round; stroke-linejoin: round; }\n'
     '/* light theme: the pale accents are too faint as thin lines on a light card */\n'
     'html:not([data-theme="dark"]) .flow .fl-nh svg { filter: brightness(.72) saturate(1.250); }'),
]
for path in sys.argv[1:3]:
    s = open(path, encoding='utf-8').read()
    for cls, body in ICONS.items():
        pat = re.compile(r'(<div class="fl-n ' + cls + r'"><div class="fl-nh">)<i style="background:([^"]+)"></i>')
        assert len(pat.findall(s)) == 1, (path, cls)
        s = pat.sub(lambda m: f'{m.group(1)}<svg viewBox="0 0 24 24" aria-hidden="true" style="color:{m.group(2)}">{body}</svg>', s)
    for a, b in CSS_SWAPS:
        assert s.count(a) == 1, (path, a)
        s = s.replace(a, b)
    open(path, 'w', encoding='utf-8').write(s)
    print(path.split('/')[-1], 'ok')
