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
CSS = '''
.top{background:var(--hb);color:var(--hi)}
.top .nav nav{color:var(--h2)}
.top .nav nav b{font-weight:600;color:var(--hi)}
.btn.hb{background:var(--hbtn);color:var(--hbtnc)}
.hero{padding:96px 0 0}
.hero h1{font-size:clamp(44px,10.2vw,148px);letter-spacing:-.065em;line-height:.94}
.hero h1 .cl{display:inline-flex;align-items:baseline;gap:.12em;margin-left:.2em;white-space:nowrap}
.hero h1 .spark{height:.64em;width:.64em;fill:var(--spark);transform:translateY(-.03em)}
.hero h1 .word{height:.8em;width:auto;fill:currentColor;transform:translateY(.062em)}
.hero .sub{color:var(--hi);font-size:23px;line-height:1.4;max-width:680px;margin-top:44px}
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:72px;margin-top:120px}
.steps .n{font:200 72px/1 var(--d);letter-spacing:-.06em;color:var(--num)}
.steps h3{font-size:27px;font-weight:500;letter-spacing:-.025em;line-height:1.15;margin-top:26px}
.steps p{margin-top:12px;color:var(--h2);font-size:19px;line-height:1.45;max-width:320px}
.steps p a{color:var(--hi);font-weight:600;text-decoration:underline;text-decoration-thickness:1.5px;text-underline-offset:5px}
.addr{display:flex;align-items:center;gap:18px;margin-top:64px;background:var(--hbar);border-radius:8px;padding:14px 14px 14px 30px}
.addr code{flex:1;min-width:0;font:400 clamp(17px,1.9vw,23px)/1.3 var(--m);overflow-wrap:anywhere}
.hero .end{height:140px}
.does{padding:200px 0 0}
.does .g{display:grid;grid-template-columns:.8fr 1.2fr;gap:72px;align-items:start}
.does h2{font-size:clamp(40px,5.4vw,80px);letter-spacing:-.055em}
.does ul{list-style:none;display:grid;gap:64px;padding-top:14px}
.does li{display:grid;grid-template-columns:230px 1fr;gap:32px;align-items:baseline}
.does li b{font:200 44px/1 var(--d);letter-spacing:-.045em}
.does li span{color:var(--ink2);font-size:20px;line-height:1.5;max-width:420px}
.show{margin-top:200px;background:var(--band);padding:150px 0}
.show .box{width:min(680px,100% - 32px);margin:0 auto}
.fin{padding:210px 0 200px;text-align:center}
.fin h2{font-size:clamp(44px,7.2vw,112px);letter-spacing:-.06em;line-height:.96}
.fin .cta{display:flex;gap:30px;justify-content:center;align-items:center;flex-wrap:wrap;margin-top:56px}
.fin p{margin:64px auto 0;color:var(--muted);max-width:520px;font-size:18px}
@media (max-width:760px){
.hero{padding-top:44px}.hero .sub{font-size:19px;margin-top:28px}
.steps{grid-template-columns:1fr;gap:52px;margin-top:72px}.steps .n{font-size:60px}.steps h3{margin-top:16px}
.addr{flex-direction:column;align-items:stretch;padding:22px 16px 16px;margin-top:52px;gap:16px}.hero .end{height:84px}
.does{padding-top:110px}.does .g{grid-template-columns:1fr;gap:52px}.does ul{gap:44px;padding-top:0}.does li{grid-template-columns:1fr;gap:10px}.does li b{font-size:38px}
.show{margin-top:110px;padding:72px 0}.fin{padding:120px 0 110px}.fin .cta{margin-top:40px}.fin p{margin-top:44px}
}'''
V = {
 'g': dict(theme='light', img='light', vars='--bg:#ffffff;--ink:#0b0b0d;--ink2:#3c3c46;--muted:#6d6d78;--s2:#eeeef2;--hb:#0a6cff;--hi:#ffffff;--h2:rgba(255,255,255,.86);--hbar:rgba(255,255,255,.14);--hbtn:#ffffff;--hbtnc:#0a3fb8;--spark:#ffffff;--num:#ffffff;--band:#f3f3f6', copy='hb'),
 'h': dict(theme='dark', img='dark', vars='--bg:#0b0b0d;--hb:#0b0b0d;--hi:#f2f2f4;--h2:#b4b4bb;--hbar:#19191c;--hbtn:#f2f2f4;--hbtnc:#0b0b0d;--spark:#D97757;--num:#6aa8ff;--band:#131315', copy='blue'),
 'i': dict(theme='light', img='light', vars='--bg:#ffffff;--ink:#0b0b0d;--ink2:#3c3c46;--muted:#6d6d78;--s2:#eeeef2;--hb:#ffffff;--hi:#0b0b0d;--h2:#3c3c46;--hbar:#f1f1f4;--hbtn:#0b0b0d;--hbtnc:#ffffff;--spark:#D97757;--num:#0a6cff;--band:#f3f3f6', copy='blue'),
}
for k, v in V.items():
    html = f'''<!doctype html><html lang="ru" data-theme="{v['theme']}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{k.upper()}</title><link rel="stylesheet" href="fonts.css"><link rel="stylesheet" href="common.css"><style>
html[data-theme]{{{v['vars']}}}{CSS}
</style></head><body><main>
<div class="top">
<header class="nav"><div class="wrap in"><a class="logo" href="#">{LOGO} ONEFLOW</a><nav><a>Почему ONEFLOW</a><a>Цены</a><a><b>MCP</b></a><a>Вопросы</a></nav><span class="sp"></span><a class="lg">Войти</a><a class="btn sm hb">Регистрация</a></div></header>
<section class="hero"><div class="wrap">
<h1>ONEFLOW <b>MCP</b><br>в<span class="cl">{SPARK}{WORD}</span></h1>
<p class="sub">Картинки и видео для рекламы — по одной фразе в чате.</p>
<div class="steps">
<div><div class="n">1</div><h3>Зарегистрируйтесь</h3><p>Нужен аккаунт ONEFLOW. <a>Создать аккаунт</a></p></div>
<div><div class="n">2</div><h3>Скопируйте адрес</h3><p>Он один для всех — в строке ниже.</p></div>
<div><div class="n">3</div><h3>Вставьте в Claude</h3><p>Настройки → Коннекторы → Добавить свой коннектор → «Разрешить».</p></div>
</div>
<div class="addr"><code>{URL}</code><a class="btn {v['copy']}">Копировать адрес</a></div>
<div class="end"></div>
</div></section></div>
<section class="does"><div class="wrap g">
<h2>Что <b>умеет</b></h2>
<ul>
<li><b>Картинки</b><span>Баннеры, карточки товара, сторис — по описанию. От 2 кредитов.</span></li>
<li><b>Видео</b><span>Из текста или из вашей картинки. От 23 кредитов.</span></li>
<li><b>Галерея</b><span>Все ваши работы из ONEFLOW — прямо в чате.</span></li>
<li><b>Баланс</b><span>Сколько кредитов осталось. Кредиты те же, что на сайте.</span></li>
</ul></div></section>
<section class="show"><div class="box"><div class="chat"><div class="me">Сделай картинку: кулон в жидком серебре</div><div class="tool"><i></i>ONEFLOW · картинка</div><img class="w" src="img/w-image-{v['img']}.png" alt="" style="max-width:none"></div></div></section>
<section class="fin"><div class="wrap"><h2>Подключите<br><b>за минуту</b></h2>
<div class="cta"><a class="btn blue">Копировать адрес</a><a class="link">Создать аккаунт</a></div>
<p>Claude не видит ваш пароль. Доступ отключается одной кнопкой в ONEFLOW.</p></div></section>
</main><footer><div class="wrap"><span>© 2026 ONEFLOW</span><span>Политика конфиденциальности · Пользовательское соглашение · Поддержка</span></div></footer></body></html>'''
    open(f'{S}/mcppage/{k}.html', 'w', encoding='utf-8').write(html)
print('ok')
