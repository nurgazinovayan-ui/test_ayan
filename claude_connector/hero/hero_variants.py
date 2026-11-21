import re, sys
S = sys.argv[1]
src = open('/home/user/oneflow/landing/ru.html', encoding='utf-8').read()
spark_paths = ''.join('<path d="%s"/>' % d for d in re.findall(r'<path[^>]*\sd="([^"]+)"', open('/home/user/test_ayan/landing/assets/mcp/claude-spark.svg', encoding='utf-8').read()))
TG = '<svg class="i" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 2 11 13"/><path d="M22 2 15 22l-4-9-9-4 20-7z"/></svg>'
SP = f'<svg class="i sp" viewBox="0 0 24 24" aria-hidden="true">{spark_paths}</svg>'
WEB = '<svg class="i" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 2.8 2.6 15.200 0 18M12 3c-2.600 2.800-2.600 15.200 0 18"/></svg>'
BOT = 'https://t.me/oneflow_bot'
CSS = '''
.also{display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:8px 22px;font:400 16px/1.4 var(--d);color:var(--ink2);position:relative;z-index:3}
.also a{display:inline-flex;align-items:center;gap:8px;color:var(--ink);font-weight:500;text-decoration:underline;text-underline-offset:5px;text-decoration-thickness:1px;text-decoration-color:color-mix(in srgb,var(--ink) 35%,transparent)}
.also a:hover{text-decoration-color:var(--ink)}
.also .i{width:18px;height:18px;flex:none}.also .sp{fill:#D97757}
.also.a{margin-top:26px}
.also.b{margin-bottom:26px}.also.b b{font-weight:600;color:#fff;background:#0a6cff;padding:3px 9px;border-radius:5px;font-size:16px;line-height:1.3}
.also.c{margin-top:30px;gap:8px 34px}.also.c span{display:inline-flex;align-items:center;gap:8px}.also.c .lab{color:var(--ink2)}
'''
A = f'<p class="also a">Ещё в <a href="{BOT}">{TG}Telegram</a> и в <a href="/ru/mcp">{SP}Claude — MCP</a></p>'
B = f'<p class="also b"><b>Новое</b> ONEFLOW теперь в <a href="{BOT}">{TG}Telegram</a> и в <a href="/ru/mcp">{SP}Claude</a></p>'
C = f'<p class="also c"><span class="lab">Работает в</span><span>{WEB}браузере</span><a href="{BOT}">{TG}Telegram</a><a href="/ru/mcp">{SP}Claude — MCP</a></p>'
acts_end = '<a class="btn g" href="#engines">Как это работает</a></div>'
h1 = '<h1 aria-label="Рекламная студия в вашем браузере">'
assert src.count(acts_end) == 1 and src.count(h1) == 1
def put(s, css=CSS):
    i = s.rindex('</style>'); return s[:i] + css + s[i:]
open(S + '/hero/a.html', 'w', encoding='utf-8').write(put(src.replace(acts_end, acts_end + A)))
open(S + '/hero/b.html', 'w', encoding='utf-8').write(put(src.replace(h1, B + h1)))
open(S + '/hero/c.html', 'w', encoding='utf-8').write(put(src.replace(acts_end, acts_end + C)))
print('ok')
