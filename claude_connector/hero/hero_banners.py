import re, sys
S = sys.argv[1]
src = open('/home/user/oneflow/landing/ru.html', encoding='utf-8').read()
spark_paths = ''.join('<path d="%s"/>' % d for d in re.findall(r'<path[^>]*\sd="([^"]+)"', open('/home/user/test_ayan/landing/assets/mcp/claude-spark.svg', encoding='utf-8').read()))
TG = '<svg class="hb-i" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 2 11 13"/><path d="M22 2 15 22l-4-9-9-4 20-7z"/></svg>'
SP = f'<svg class="hb-i hb-sp" viewBox="0 0 24 24" aria-hidden="true">{spark_paths}</svg>'
AR = '<svg class="hb-ar" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
BOT = 'https://t.me/oneflow_bot'
CSS = '''
.hb{position:relative;z-index:3;display:grid;grid-template-columns:1fr 1fr;gap:16px;width:min(940px,100%);margin:36px auto 0;text-align:left;font-family:var(--d)}
.hb a{color:inherit;text-decoration:none}
.hb .hb-i{width:20px;height:20px;flex:none}.hb .hb-sp{fill:#D97757}
.hb .hb-ar{width:22px;height:22px;flex:none}
.hb b{display:block;font-weight:500;font-size:23px;line-height:1.15;letter-spacing:-.025em;color:var(--ink)}
.hb .hb-s{display:block;margin-top:8px;font-size:16px;line-height:1.35;color:var(--ink2)}
.hb .hb-k{display:flex;align-items:center;gap:8px;font-size:16px;color:var(--ink2);margin-bottom:12px}
/* D: two banners, each with a real screenshot */
.hb.hb-d .hb-b{display:flex;justify-content:space-between;gap:14px;height:164px;border-radius:12px;overflow:hidden;padding:22px 0 0 26px}
.hb.hb-d .hb-tg{background:linear-gradient(115deg,#151517 38%,#0f2a52)}
.hb.hb-d .hb-cl{background:linear-gradient(115deg,#151517 38%,#46281c)}
.hb.hb-d .hb-p{flex:none;width:176px;height:142px;margin-right:24px;border-radius:14px 14px 0 0;overflow:hidden;box-shadow:0 0 50px rgba(0,0,0,.5)}
.hb.hb-d .hb-p img{display:block;width:100%}
.hb.hb-d .hb-cl .hb-p{width:200px}
/* E: two colour banners */
.hb.hb-e .hb-b{display:flex;align-items:center;gap:18px;height:112px;border-radius:12px;padding:0 24px 0 26px}
.hb.hb-e .hb-tg{background:#0a6cff}.hb.hb-e .hb-tg b,.hb.hb-e .hb-tg .hb-s,.hb.hb-e .hb-tg{color:#fff}
.hb.hb-e .hb-cl{background:#D97757}.hb.hb-e .hb-cl b,.hb.hb-e .hb-cl .hb-s,.hb.hb-e .hb-cl{color:#1b0f08}
.hb.hb-e .hb-big{width:40px;height:40px;flex:none}.hb.hb-e .hb-cl .hb-big{fill:#1b0f08}
.hb.hb-e .hb-t{flex:1}.hb.hb-e .hb-s{margin-top:5px}
/* F: one wide banner */
.hb.hb-f{display:flex;align-items:center;justify-content:space-between;gap:20px;height:168px;border-radius:12px;overflow:hidden;background:linear-gradient(100deg,#0f2a52,#151517 34%,#151517 66%,#46281c);text-align:center}
.hb.hb-f .hb-ph{flex:none;align-self:flex-end;width:150px;height:140px;margin-left:44px;border-radius:14px 14px 0 0;overflow:hidden;transform:rotate(-5deg) translateY(10px);box-shadow:0 0 50px rgba(0,0,0,.5)}
.hb.hb-f .hb-wn{flex:none;align-self:flex-end;width:190px;height:140px;margin-right:40px;border-radius:12px 12px 0 0;overflow:hidden;transform:rotate(4deg) translateY(10px);box-shadow:0 0 50px rgba(0,0,0,.5)}
.hb.hb-f img{display:block;width:100%}
.hb.hb-f .hb-m{flex:1}
.hb.hb-f b{font-size:26px}
.hb.hb-f .hb-ls{display:flex;justify-content:center;gap:10px 30px;flex-wrap:wrap;margin-top:16px;font-size:17px}
.hb.hb-f .hb-ls a{display:inline-flex;align-items:center;gap:8px;font-weight:500;color:var(--ink);text-decoration:underline;text-underline-offset:5px;text-decoration-thickness:1px;text-decoration-color:color-mix(in srgb,var(--ink) 35%,transparent)}
@media (max-width:760px){.hb{grid-template-columns:1fr;gap:10px;margin-top:26px}
.hb.hb-d .hb-b{height:132px;padding:18px 0 0 18px}.hb.hb-d .hb-p,.hb.hb-d .hb-cl .hb-p{width:120px;height:114px;margin-right:16px}.hb b{font-size:20px}.hb .hb-k{margin-bottom:8px}
.hb.hb-e .hb-b{height:96px;padding:0 16px 0 18px;gap:14px}.hb.hb-e .hb-big{width:32px;height:32px}
.hb.hb-f{height:auto;flex-direction:column;padding:26px 16px 0;gap:22px}.hb.hb-f .hb-ph{display:none}.hb.hb-f .hb-wn{align-self:center;margin:0;transform:none;width:220px;height:110px}.hb.hb-f b{font-size:22px}}
'''
D = f'''<div class="hb hb-d"><a class="hb-b hb-tg" href="{BOT}"><span><span class="hb-k">{TG}Telegram</span><b>ONEFLOW<br>в Telegram</b><span class="hb-s">Прямо в мессенджере</span></span><span class="hb-p"><img src="/v/tg.png" alt=""></span></a><a class="hb-b hb-cl" href="/ru/mcp"><span><span class="hb-k">{SP}Claude · MCP</span><b>ONEFLOW<br>в Claude</b><span class="hb-s">По одной фразе в чате</span></span><span class="hb-p"><img src="/v/win.webp" alt=""></span></a></div>'''
E = f'''<div class="hb hb-e"><a class="hb-b hb-tg" href="{BOT}">{TG.replace('class="hb-i"', 'class="hb-big"')}<span class="hb-t"><b>ONEFLOW в Telegram</b><span class="hb-s">Картинки и видео прямо в мессенджере</span></span>{AR}</a><a class="hb-b hb-cl" href="/ru/mcp">{SP.replace('class="hb-i hb-sp"', 'class="hb-big"')}<span class="hb-t"><b>ONEFLOW MCP в Claude</b><span class="hb-s">Реклама по одной фразе в чате</span></span>{AR}</a></div>'''
F = f'''<div class="hb hb-f"><span class="hb-ph"><img src="/v/tg.png" alt=""></span><span class="hb-m"><b>Теперь в Telegram и в Claude</b><span class="hb-ls"><a href="{BOT}">{TG}Открыть в Telegram</a><a href="/ru/mcp">{SP}Подключить MCP</a></span></span><span class="hb-wn"><img src="/v/win.webp" alt=""></span></div>'''
acts_end = '<a class="btn g" href="#engines">Как это работает</a></div>'
assert src.count(acts_end) == 1
def put(s):
    i = s.rindex('</style>'); return s[:i] + CSS + s[i:]
for k, v in (('d', D), ('e', E), ('f', F)):
    open(f'{S}/hero/{k}.html', 'w', encoding='utf-8').write(put(src.replace(acts_end, acts_end + v)))
print('ok')
