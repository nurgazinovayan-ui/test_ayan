import re, sys
S = sys.argv[1]
src = open('/home/user/oneflow/landing/ru.html', encoding='utf-8').read()
spark_paths = ''.join('<path d="%s"/>' % d for d in re.findall(r'<path[^>]*\sd="([^"]+)"', open('/home/user/test_ayan/landing/assets/mcp/claude-spark.svg', encoding='utf-8').read()))
TG = '<svg class="hs-i" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 2 11 13"/><path d="M22 2 15 22l-4-9-9-4 20-7z"/></svg>'
SP = f'<svg class="hs-i hs-sp" viewBox="0 0 24 24" aria-hidden="true">{spark_paths}</svg>'
AR = '<svg class="hs-ar" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
BOT = 'https://t.me/oneflow_bot'
CSS = '''
.hsm{position:relative;z-index:3;display:flex;justify-content:center;gap:10px;margin:0 auto 34px;font-family:var(--d);text-align:left}
.hsm a{text-decoration:none}
.hsm .hs-i{width:22px;height:22px;flex:none}
.hsm .hs-ar{width:18px;height:18px;flex:none;margin-left:4px}
/* E, half size: two colour banners in one row */
.hsm.hs-e .hs-b{display:inline-flex;align-items:center;gap:11px;height:56px;padding:0 18px 0 18px;border-radius:8px;font-size:17px;font-weight:500;line-height:1.2;letter-spacing:-.01em;white-space:nowrap}
.hsm.hs-e .hs-tg{background:#0a6cff;color:#fff}
.hsm.hs-e .hs-cl{background:#D97757;color:#1b0f08}
.hsm.hs-e .hs-cl .hs-sp{fill:#1b0f08}
/* F, half size: one banner with two links */
.hsm.hs-f{width:min(700px,100%);height:84px;align-items:center;justify-content:space-between;gap:14px;border-radius:10px;overflow:hidden;background:linear-gradient(100deg,#0f2a52,#151517 34%,#151517 66%,#46281c);text-align:center}
.hsm.hs-f .hs-ph{flex:none;align-self:flex-end;width:74px;height:70px;margin-left:22px;border-radius:8px 8px 0 0;overflow:hidden;transform:rotate(-5deg) translateY(6px);box-shadow:0 0 30px rgba(0,0,0,.5)}
.hsm.hs-f .hs-wn{flex:none;align-self:flex-end;width:92px;height:70px;margin-right:20px;border-radius:7px 7px 0 0;overflow:hidden;transform:rotate(4deg) translateY(6px);box-shadow:0 0 30px rgba(0,0,0,.5)}
.hsm.hs-f img{display:block;width:100%}
.hsm.hs-f .hs-m{flex:1;min-width:0}
.hsm.hs-f b{display:block;font-weight:500;font-size:18px;line-height:1.2;letter-spacing:-.02em;color:#f2f2f4}
.hsm.hs-f .hs-ls{display:flex;justify-content:center;gap:6px 22px;flex-wrap:wrap;margin-top:8px;font-size:16px}
.hsm.hs-f .hs-ls a{display:inline-flex;align-items:center;gap:7px;font-weight:500;color:#f2f2f4;text-decoration:underline;text-underline-offset:4px;text-decoration-thickness:1px;text-decoration-color:rgba(242,242,244,.4)}
.hsm.hs-f .hs-i{width:18px;height:18px}.hsm.hs-f .hs-sp{fill:#D97757}
@media (max-width:760px){.hsm{margin-bottom:26px;gap:8px}
.hsm.hs-e .hs-b{flex:1;justify-content:center;height:52px;padding:0 10px;font-size:16px;gap:8px}.hsm.hs-e .hs-long,.hsm.hs-e .hs-ar{display:none}.hsm.hs-e .hs-i{width:20px;height:20px}
.hsm.hs-f{height:auto;padding:16px 12px}.hsm.hs-f .hs-ph,.hsm.hs-f .hs-wn{display:none}}
'''
E = f'''<div class="hsm hs-e"><a class="hs-b hs-tg" href="{BOT}">{TG}<span><span class="hs-long">ONEFLOW </span>в Telegram</span>{AR}</a><a class="hs-b hs-cl" href="/ru/mcp">{SP}<span><span class="hs-long">ONEFLOW </span>MCP в Claude</span>{AR}</a></div>'''
F = f'''<div class="hsm hs-f"><span class="hs-ph"><img src="/v/tg.png" alt=""></span><span class="hs-m"><b>Теперь в Telegram и в Claude</b><span class="hs-ls"><a href="{BOT}">{TG}Открыть в Telegram</a><a href="/ru/mcp">{SP}Подключить MCP</a></span></span><span class="hs-wn"><img src="/v/win.webp" alt=""></span></div>'''
h1 = '<h1 aria-label="Рекламная студия в вашем браузере">'
assert src.count(h1) == 1
def put(s):
    i = s.rindex('</style>'); return s[:i] + CSS + s[i:]
for k, v in (('g', E), ('h', F)):
    open(f'{S}/hero/{k}.html', 'w', encoding='utf-8').write(put(src.replace(h1, v + h1)))
print('ok')
