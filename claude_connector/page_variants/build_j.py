import re, sys
S, D = sys.argv[1], sys.argv[2]
def paths(f):
    t = open(f, encoding='utf-8').read()
    assert not re.search(r'<script|onload|href|<image|foreignObject', t, re.I)
    return ''.join('<path d="%s"/>' % d for d in re.findall(r'<path[^>]*\sd="([^"]+)"', t))
SPARK = '<svg class="spark" viewBox="0 0 24 24" aria-hidden="true">%s</svg>' % paths(D + '/package/icons/claude.svg')
WORD = '<svg class="word" viewBox="0 0 97 24" role="img" aria-label="Claude">%s</svg>' % paths(D + '/package/icons/claude-text.svg')
LOGO = '<svg viewBox="0 0 76 52" aria-hidden="true"><path fill="currentColor" d="M17 0C18.66 0 20 1.34 20 3V14C20 15.1 20.9 16 22 16H32C33.66 16 35 17.34 35 19V30C35 31.1 35.9 32 37 32H38C39.1 32 40 31.1 40 30V19C40 17.34 41.34 16 43 16H57C58.66 16 60 17.34 60 19V30C60 31.1 60.9 32 62 32H73C74.66 32 76 33.34 76 35V49C76 50.66 74.66 52 73 52H59C57.34 52 56 50.66 56 49V38C56 36.9 55.1 36 54 36H51C49.9 36 49 36.9 49 38V49C49 50.66 47.66 52 46 52H32C30.34 52 29 50.66 29 49V38C29 36.9 28.1 36 27 36H24C22.9 36 22 36.9 22 38V49C22 50.66 20.66 52 19 52H5C3.34 52 2 50.66 2 49V35C2 33.34 3.34 32 5 32H13C14.1 32 15 31.1 15 30V22C15 20.9 14.1 20 13 20H3C1.34 20 0 18.66 0 17V3C0 1.34 1.34 0 3 0H17Z"/></svg>'
URL = 'https://api.oneflow.art/functions/v1/mcp'
H1 = f'<h1>ONEFLOW <b>MCP</b><br>в<span class="cl">{SPARK}{WORD}</span></h1>'
def head(btn):
    return f'<header class="nav"><div class="wrap in"><a class="logo" href="#">{LOGO} ONEFLOW</a><nav><a>Почему ONEFLOW</a><a>Цены</a><a><b style="font-weight:600;color:var(--ink)">MCP</b></a><a>Вопросы</a></nav><span class="sp"></span><a class="lg">Войти</a><a class="btn sm {btn}">Регистрация</a></div></header>'
FOOT = '<footer><div class="wrap"><span>© 2026 ONEFLOW</span><span>Политика конфиденциальности · Пользовательское соглашение · Поддержка</span></div></footer>'
BASE = '''
h1 .cl{display:inline-flex;align-items:baseline;gap:.12em;margin-left:.2em;white-space:nowrap}
h1 .spark{height:.64em;width:.64em;fill:#D97757;transform:translateY(-.03em)}
h1 .word{height:.8em;width:auto;fill:currentColor;transform:translateY(.062em)}
.addr{display:flex;align-items:center;gap:18px;background:var(--bar);border-radius:8px;padding:14px 14px 14px 30px;text-align:left}
.addr code{flex:1;min-width:0;font:400 clamp(17px,1.8vw,22px)/1.3 var(--m);overflow-wrap:anywhere}
.n{font:200 72px/1 var(--d);letter-spacing:-.06em;color:var(--num)}
.st h3{font-size:27px;font-weight:500;letter-spacing:-.025em;line-height:1.15}
.st p{color:var(--ink2);font-size:19px;line-height:1.45}
.st p a,.ul{color:var(--ink);font-weight:600;text-decoration:underline;text-decoration-thickness:1.5px;text-underline-offset:5px}
@media (max-width:760px){.addr{flex-direction:column;align-items:stretch;padding:22px 16px 16px;gap:16px}.n{font-size:60px}}
'''
STEPS = [('Зарегистрируйтесь', 'Нужен аккаунт ONEFLOW. <a>Создать аккаунт</a>'), ('Скопируйте адрес', 'Он один для всех — в строке ниже.'), ('Вставьте в Claude', 'Настройки → Коннекторы → Добавить свой коннектор → «Разрешить».')]
DOES = [('Картинки', 'Баннеры, карточки товара, сторис — по описанию. От 2 кредитов.'), ('Видео', 'Из текста или из вашей картинки. От 23 кредитов.'), ('Галерея', 'Все ваши работы из ONEFLOW — прямо в чате.'), ('Баланс', 'Сколько кредитов осталось. Кредиты те же, что на сайте.')]
def chat(img, text='Сделай картинку: кулон в жидком серебре', tool='картинка'):
    return f'<div class="chat"><div class="me">{text}</div><div class="tool"><i></i>ONEFLOW · {tool}</div><img class="w" src="img/{img}" alt="" style="max-width:none"></div>'
NOTE = 'Claude не видит ваш пароль. Доступ отключается одной кнопкой в ONEFLOW.'

# ---------- J: centred, dark, glow
J = f'''<!doctype html><html lang="ru" data-theme="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>J</title><link rel="stylesheet" href="fonts.css"><link rel="stylesheet" href="common.css"><style>
html[data-theme]{{--bg:#08080a;--bar:#17171a;--num:#6aa8ff;--s2:#1d1d21}}{BASE}
.top{{position:relative;overflow:hidden}}
.top:before{{content:"";position:absolute;inset:0;background:radial-gradient(56% 44% at 50% -4%,rgba(10,108,255,.5),rgba(10,108,255,.12) 55%,transparent 78%),radial-gradient(26% 22% at 80% 6%,rgba(217,119,87,.2),transparent 72%)}}
.top>*{{position:relative}}
.hero{{text-align:center;padding:120px 0 170px}}
.hero h1{{font-size:clamp(44px,9.4vw,138px);letter-spacing:-.065em;line-height:.95}}
.hero .sub{{color:var(--ink);font-size:23px;margin:44px auto 0;max-width:680px}}
.steps{{display:grid;grid-template-columns:repeat(3,1fr);gap:64px;margin-top:130px}}
.steps h3{{margin-top:24px}}.steps p{{margin:12px auto 0;max-width:300px}}
.hero .addr{{width:min(860px,100%);margin:72px auto 0}}
.does{{padding:60px 0 0;text-align:center}}
.does h2{{font-size:clamp(40px,5.6vw,84px);letter-spacing:-.055em}}
.does .g{{display:grid;grid-template-columns:repeat(4,1fr);gap:48px;margin-top:100px;text-align:left}}
.does .g b{{display:block;font:200 44px/1 var(--d);letter-spacing:-.045em}}
.does .g span{{display:block;margin-top:20px;color:var(--ink2);font-size:19px;line-height:1.5}}
.show{{padding:190px 0 0}}
.show .box{{width:min(720px,100% - 32px);margin:0 auto;position:relative}}
.show .box:before{{content:"";position:absolute;inset:8% -24% -14% -24%;background:radial-gradient(50% 50% at 50% 55%,rgba(10,108,255,.38),transparent 72%)}}
.show .chat{{position:relative}}
.fin{{padding:230px 0 200px;text-align:center}}
.fin h2{{font-size:clamp(44px,7.2vw,112px);letter-spacing:-.06em;line-height:.96}}
.fin .cta{{display:flex;gap:30px;justify-content:center;align-items:center;flex-wrap:wrap;margin-top:56px}}
.fin p{{margin:64px auto 0;color:var(--muted);max-width:520px;font-size:18px}}
@media (max-width:760px){{.hero{{padding:52px 0 96px}}.hero .sub{{font-size:19px;margin-top:28px}}.steps{{grid-template-columns:1fr;gap:52px;margin-top:76px}}.steps h3{{margin-top:14px}}.hero .addr{{margin-top:56px}}
.does{{padding-top:20px}}.does .g{{grid-template-columns:1fr;gap:44px;margin-top:56px;text-align:center}}.does .g b{{font-size:38px}}.does .g span{{margin-top:10px}}.show{{padding-top:100px}}.fin{{padding:130px 0 110px}}.fin .cta{{margin-top:40px}}.fin p{{margin-top:44px}}}}
</style></head><body><main>
<div class="top">{head('ink')}
<section class="hero"><div class="wrap">{H1}
<p class="sub">Картинки и видео для рекламы — по одной фразе в чате.</p>
<div class="steps st">{''.join(f'<div><div class="n">{i+1}</div><h3>{t}</h3><p>{p}</p></div>' for i,(t,p) in enumerate(STEPS))}</div>
<div class="addr"><code>{URL}</code><a class="btn blue">Копировать адрес</a></div>
</div></section></div>
<section class="does"><div class="wrap"><h2>Что <b>умеет</b></h2><div class="g">{''.join(f'<div><b>{t}</b><span>{p}</span></div>' for t,p in DOES)}</div></div></section>
<section class="show"><div class="box">{chat('w-image-dark.png')}</div></section>
<section class="fin"><div class="wrap"><h2>Подключите<br><b>за минуту</b></h2><div class="cta"><a class="btn blue">Копировать адрес</a><a class="link">Создать аккаунт</a></div><p>{NOTE}</p></div></section>
</main>{FOOT}</body></html>'''

# ---------- K: warm paper, split first screen, index list
K = f'''<!doctype html><html lang="ru" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>K</title><link rel="stylesheet" href="fonts.css"><link rel="stylesheet" href="common.css"><style>
html[data-theme]{{--bg:#f3efe7;--ink:#141413;--ink2:#45433d;--muted:#6f6c64;--s1:#fbf9f4;--s2:#e6e1d6;--bar:#e6e1d6;--num:#141413}}{BASE}
.hero{{padding:110px 0 190px}}
.hero .g{{display:grid;grid-template-columns:1.08fr .92fr;gap:80px;align-items:start}}
.hero h1{{font-size:clamp(44px,7.9vw,116px);letter-spacing:-.065em;line-height:.95}}
.hero .sub{{color:var(--ink);font-size:23px;margin-top:44px;max-width:480px}}
.list{{display:grid;gap:44px;padding-top:12px}}
.list>div{{display:grid;grid-template-columns:66px 1fr;align-items:start}}
.list .n{{font-size:60px;margin-top:-8px}}
.list p{{margin-top:8px}}
.hero .addr{{flex-direction:column;align-items:stretch;padding:22px 16px 16px 16px;margin-top:52px}}
.hero .addr code{{padding:0 8px;font-size:17px}}
.does{{padding:0}}
.does .lab{{font-size:19px;font-weight:600;margin-bottom:56px}}
.does ul{{list-style:none;display:grid;gap:34px}}
.does li{{display:grid;grid-template-columns:1fr 400px;gap:40px;align-items:baseline}}
.does li b{{font:200 clamp(56px,8.4vw,124px)/.98 var(--d);letter-spacing:-.065em}}
.does li span{{color:var(--ink2);font-size:20px;line-height:1.5}}
.show{{margin-top:210px;background:#e9e4d9;padding:150px 0}}
.show .box{{width:min(680px,100% - 32px);margin:0 auto;--s2:#dcd6c9}}
.fin{{padding:210px 0 190px}}
.fin .g{{display:flex;justify-content:space-between;align-items:flex-end;gap:40px;flex-wrap:wrap}}
.fin h2{{font-size:clamp(44px,7.2vw,112px);letter-spacing:-.06em;line-height:.96}}
.fin .cta{{display:flex;gap:30px;align-items:center;flex-wrap:wrap}}
.fin p{{margin-top:72px;color:var(--muted);font-size:18px}}
@media (max-width:760px){{.hero{{padding:48px 0 110px}}.hero .g{{grid-template-columns:1fr;gap:72px}}.hero .sub{{font-size:19px;margin-top:28px}}.list{{gap:40px}}.hero .addr{{margin-top:44px}}
.does .lab{{margin-bottom:36px}}.does ul{{gap:40px}}.does li{{grid-template-columns:1fr;gap:10px}}.show{{margin-top:110px;padding:72px 0}}.fin{{padding:120px 0 100px}}.fin p{{margin-top:44px}}}}
</style></head><body><main>
{head('ink')}
<section class="hero"><div class="wrap g">
<div>{H1}<p class="sub">Картинки и видео для рекламы — по одной фразе в чате.</p></div>
<div><div class="list st">{''.join(f'<div><div class="n">{i+1}</div><div><h3>{t}</h3><p>{p}</p></div></div>' for i,(t,p) in enumerate(STEPS))}</div>
<div class="addr"><code>{URL}</code><a class="btn ink">Копировать адрес</a></div></div>
</div></section>
<section class="does"><div class="wrap"><p class="lab">Что умеет</p><ul>{''.join(f'<li><b>{t}</b><span>{p}</span></li>' for t,p in DOES)}</ul></div></section>
<section class="show"><div class="box">{chat('w-image-light.png')}</div></section>
<section class="fin"><div class="wrap"><div class="g"><h2>Подключите<br><b>за минуту</b></h2><div class="cta"><a class="btn ink">Копировать адрес</a><a class="link">Создать аккаунт</a></div></div><p>{NOTE}</p></div></section>
</main>{FOOT}</body></html>'''

# ---------- L: cinematic frame
L = f'''<!doctype html><html lang="ru" data-theme="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>L</title><link rel="stylesheet" href="fonts.css"><link rel="stylesheet" href="common.css"><style>
html[data-theme]{{--bg:#060607;--bar:#151517;--num:#f2f2f4;--s2:#1d1d21}}{BASE}
.top{{position:relative;overflow:hidden;min-height:880px;display:flex;flex-direction:column}}
.top .pic{{position:absolute;inset:0;background:url(img/pendant.webp) right -110px top 40%/auto 106% no-repeat}}
.top:after{{content:"";position:absolute;inset:0;background:linear-gradient(90deg,#060607 0%,#060607 34%,rgba(6,6,7,.6) 56%,rgba(6,6,7,.05) 86%),linear-gradient(0deg,#060607 0%,rgba(6,6,7,0) 34%),linear-gradient(180deg,rgba(6,6,7,.6),rgba(6,6,7,0) 22%)}}
.top .nav,.hero{{position:relative;z-index:2}}
.hero{{flex:1;display:flex;align-items:flex-end;padding:0 0 96px}}
.hero h1{{font-size:clamp(44px,7.8vw,114px);letter-spacing:-.065em;line-height:.95}}
.hero .sub{{color:var(--ink);font-size:23px;margin-top:40px;max-width:520px}}
.how{{padding:90px 0 0}}
.steps{{display:grid;grid-template-columns:repeat(3,1fr);gap:72px}}
.steps h3{{margin-top:26px}}.steps p{{margin-top:12px;max-width:320px}}
.how .addr{{margin-top:72px}}
.does{{padding:220px 0 0}}
.does h2{{font-size:clamp(40px,5.6vw,84px);letter-spacing:-.055em}}
.does .g{{display:grid;grid-template-columns:repeat(4,1fr);gap:48px;margin-top:96px}}
.does .g b{{display:block;font:200 44px/1 var(--d);letter-spacing:-.045em}}
.does .g span{{display:block;margin-top:20px;color:var(--ink2);font-size:19px;line-height:1.5}}
.show{{padding:150px 0 0}}
.show .two{{display:grid;grid-template-columns:1fr 1fr;gap:72px;align-items:start}}
.fin{{position:relative;overflow:hidden;margin-top:220px;padding:210px 0 200px}}
.fin .pic{{position:absolute;inset:0;background:url(img/pendant.webp) center 42%/cover;opacity:.5}}
.fin:after{{content:"";position:absolute;inset:0;background:linear-gradient(180deg,#060607,rgba(6,6,7,.45) 40%,rgba(6,6,7,.75))}}
.fin .wrap{{position:relative;z-index:2;text-align:center}}
.fin h2{{font-size:clamp(44px,7.2vw,112px);letter-spacing:-.06em;line-height:.96}}
.fin .cta{{display:flex;gap:30px;justify-content:center;align-items:center;flex-wrap:wrap;margin-top:56px}}
.fin p{{margin:64px auto 0;color:#d4d4da;max-width:520px;font-size:18px}}
@media (max-width:760px){{.top{{min-height:640px}}.top .pic{{background:url(img/pendant.webp) 62% 0/auto 62% no-repeat}}.top:after{{background:linear-gradient(0deg,#060607 30%,rgba(6,6,7,.2) 66%,rgba(6,6,7,.55))}}.hero{{padding-bottom:48px}}.hero .sub{{font-size:19px;margin-top:26px}}
.how{{padding-top:56px}}.steps{{grid-template-columns:1fr;gap:52px}}.steps h3{{margin-top:14px}}.how .addr{{margin-top:52px}}.does{{padding-top:120px}}.does .g{{grid-template-columns:1fr;gap:44px;margin-top:52px}}.does .g b{{font-size:38px}}.does .g span{{margin-top:10px}}
.show{{padding-top:90px}}.show .two{{grid-template-columns:1fr;gap:56px}}.fin{{margin-top:120px;padding:130px 0 120px}}.fin .cta{{margin-top:40px}}.fin p{{margin-top:44px}}}}
</style></head><body><main>
<div class="top"><div class="pic"></div>{head('ink')}
<section class="hero"><div class="wrap">{H1}<p class="sub">Картинки и видео для рекламы — по одной фразе в чате.</p></div></section></div>
<section class="how"><div class="wrap">
<div class="steps st">{''.join(f'<div><div class="n">{i+1}</div><h3>{t}</h3><p>{p}</p></div>' for i,(t,p) in enumerate(STEPS))}</div>
<div class="addr"><code>{URL}</code><a class="btn blue">Копировать адрес</a></div>
</div></section>
<section class="does"><div class="wrap"><h2>Что <b>умеет</b></h2><div class="g">{''.join(f'<div><b>{t}</b><span>{p}</span></div>' for t,p in DOES)}</div></div></section>
<section class="show"><div class="wrap two">{chat('w-image-dark.png')}{chat('w-working-dark.png', 'Сними из неё видео на 5 секунд', 'видео')}</div></section>
<section class="fin"><div class="pic"></div><div class="wrap"><h2>Подключите<br><b>за минуту</b></h2><div class="cta"><a class="btn blue">Копировать адрес</a><a class="link">Создать аккаунт</a></div><p>{NOTE}</p></div></section>
</main>{FOOT}</body></html>'''
for k, v in (('j', J), ('k', K), ('l', L)):
    open(f'{S}/mcppage/{k}.html', 'w', encoding='utf-8').write(v)
print('ok')
