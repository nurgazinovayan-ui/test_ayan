"""The ONEFLOW MCP page of oneflow.art (the connector for Claude): /mcp in English, /ru/mcp in Russian.

python3 mcp_page.py            →  site/mcp/mcp.html (EN) and site/mcp/mcp-ru.html (RU), self-contained (fonts, pictures and
                                  the icon are inside); both are copied into the app repo as landing/mcp.html and
                                  landing/mcp-ru.html, from where scripts/build-vercel.mjs puts them at /mcp and /ru/mcp
python3 mcp_page.py --preview  →  the same two files only (nothing is copied into the app repo)

The header, the language and theme switches and the footer repeat the landing's (same sizes, same storage key for the
theme). The menu item on the landing itself is added by patch_mcp_nav.mjs.
The pictures of the chat window are screenshots of the connector's real window (assets/mcp/window-<lang>-<theme>.webp).
The Claude mark and wordmark (assets/mcp/claude-*.svg) are Anthropic's trademark, shown to say where ONEFLOW works.
"""
import html as html_, os, re, shutil, sys

from build_vercel import APPREPO, HERE, inline_fonts, uri

ADDRESS = 'https://api.oneflow.art/functions/v1/mcp'   # what a person pastes into Claude
SITE = 'https://oneflow.art'
PATHS = {'en': '/mcp', 'ru': '/ru/mcp'}
HOME = {'en': '/', 'ru': '/ru'}
FONTS = {'Geist|200', 'Geist|400', 'Geist|500', 'Geist|600', 'Geist|700', 'JetBrains Mono|400'}

T = {
    'ru': dict(
        title='ONEFLOW MCP — картинки и видео для рекламы прямо в Claude',
        desc='Подключите ONEFLOW к Claude за три шага: зарегистрируйтесь, скопируйте адрес коннектора и вставьте его в настройках Claude. Картинки и видео для рекламы — по одной фразе в чате.',
        locale='ru_RU', skip='К содержанию', logo='ONEFLOW — на главную', sections='Разделы', menu='Меню',
        nav=('Почему ONEFLOW', 'Цены', 'Вопросы'), theme='Тёмная тема', to_dark='Тёмная тема', to_light='Светлая тема',
        login='Войти', register='Регистрация', open_menu='Открыть меню', close_menu='Закрыть меню',
        prep='в', sub='Картинки и видео для рекламы — по одной фразе в чате.',
        steps_label='Как подключить',
        steps=(('Зарегистрируйтесь', 'Нужен аккаунт ONEFLOW. <a href="/app?auth=register">Создать аккаунт</a>'),
               ('Скопируйте адрес', 'Он один для всех — в строке ниже.'),
               ('Вставьте в Claude', 'Настройки → Коннекторы → Добавить свой коннектор → «Разрешить».')),
        addr_label='Адрес коннектора', copy='Копировать адрес', copied='Скопировано', copy_fail='Выделите и скопируйте',
        does_a='Что', does_b='умеет',
        does=(('Картинки', 'Баннеры, карточки товара, сторис — по описанию. От 2 кредитов.'),
              ('Видео', 'Из текста или из вашей картинки. От 23 кредитов.'),
              ('Галерея', 'Все ваши работы из ONEFLOW — прямо в чате.'),
              ('Баланс', 'Сколько кредитов осталось. Кредиты те же, что на сайте.')),
        chat_me='Сделай картинку: кулон в жидком серебре', chat_tool='ONEFLOW · картинка',
        chat_alt='Окно ONEFLOW в чате Claude: готовая картинка кулона и кнопки «Открыть», «Скачать», «Сделать видео»',
        fin_a='Подключите', fin_b='за минуту', create='Создать аккаунт',
        note='Claude не видит ваш пароль. Доступ отключается одной кнопкой — на <a href="/connect">странице подключений</a>.',
        docs='Документы', foot=(('privacy', 'Конфиденциальность'), ('terms', 'Условия'), ('refunds', 'Возврат'), ('support', 'Поддержка')),
    ),
    'en': dict(
        title='ONEFLOW MCP — ad pictures and videos right in Claude',
        desc='Connect ONEFLOW to Claude in three steps: sign up, copy the connector address and paste it into Claude’s settings. Pictures and videos for your ads — from one line in the chat.',
        locale='en_US', skip='Skip to content', logo='ONEFLOW — home', sections='Sections', menu='Menu',
        nav=('Why ONEFLOW', 'Pricing', 'FAQ'), theme='Dark theme', to_dark='Dark theme', to_light='Light theme',
        login='Log in', register='Sign up', open_menu='Open menu', close_menu='Close menu',
        prep='in', sub='Pictures and videos for your ads — from one line in the chat.',
        steps_label='How to connect',
        steps=(('Sign up', 'You need a ONEFLOW account. <a href="/app?auth=register">Create an account</a>'),
               ('Copy the address', 'It is the same for everyone — in the line below.'),
               ('Paste it into Claude', 'Settings → Connectors → Add custom connector → “Allow”.')),
        addr_label='Connector address', copy='Copy the address', copied='Copied', copy_fail='Select and copy',
        does_a='What it', does_b='does',
        does=(('Pictures', 'Banners, product cards, stories — from a description. From 2 credits.'),
              ('Videos', 'From text or from your own picture. From 23 credits.'),
              ('Gallery', 'Everything you made in ONEFLOW — right in the chat.'),
              ('Balance', 'How many credits are left. The same credits as on the site.')),
        chat_me='Make a picture: a pendant in liquid silver', chat_tool='ONEFLOW · picture',
        chat_alt='The ONEFLOW window in a Claude chat: a finished picture of a pendant with the buttons Open, Download and Make a video',
        fin_a='Connect it', fin_b='in a minute', create='Create an account',
        note='Claude never sees your password. Access is switched off with one button — on the <a href="/connect">connections page</a>.',
        docs='Documents', foot=(('privacy', 'Privacy'), ('terms', 'Terms'), ('refunds', 'Refunds'), ('support', 'Support')),
    ),
}

LOGO = ('<svg viewBox="0 0 76 52" aria-hidden="true"><path fill="currentColor" d="M17 0C18.66 0 20 1.34 20 3V14C20 15.1 20.9 16 22 16H32C33.66 16 35 17.34 35 19V30C35 31.1 35.9 32 37 32H38C39.1 32 40 31.1 40 30V19C40 17.34 41.34 16 43 16H57C58.66 16 60 17.34 60 19V30C60 31.1 60.9 32 62 32H73C74.66 32 76 33.34 76 35V49C76 50.66 74.66 52 73 52H59C57.34 52 56 50.66 56 49V38C56 36.9 55.1 36 54 36H51C49.9 36 49 36.9 49 38V49C49 50.66 47.66 52 46 52H32C30.34 52 29 50.66 29 49V38C29 36.9 28.1 36 27 36H24C22.9 36 22 36.9 22 38V49C22 50.66 20.66 52 19 52H5C3.34 52 2 50.66 2 49V35C2 33.34 3.34 32 5 32H13C14.1 32 15 31.1 15 30V22C15 20.9 14.1 20 13 20H3C1.34 20 0 18.66 0 17V3C0 1.34 1.34 0 3 0H17Z"/></svg>')
MOON = '<svg class="moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/></svg>'
SUN = '<svg class="sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
COPY = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V6a2 2 0 0 1 2-2h9"/></svg>'


def svg_paths(name):
    """The drawing of a logo file: only its <path d="…"> data is taken (the file must hold nothing that runs or loads)."""
    t = open(os.path.join(HERE, 'assets', 'mcp', name), encoding='utf-8').read()
    assert not re.search(r'<script|\son\w+=|href|<image|foreignObject|<style', t, re.I), name
    ds = re.findall(r'<path[^>]*\sd="([^"]+)"', t)
    assert ds and all(re.fullmatch(r'[MmLlHhVvCcSsQqTtAaZz0-9eE+\-.,\s]+', d) for d in ds), name
    return ''.join(f'<path d="{d}"/>' for d in ds)


CSS = r'''
*{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#e5e5e5;--ink:#2d2d2d;--ink2:#5b5b5b;--muted:#6f6f6f;--raised:#f7f7f7;--field:#ededed;--ac:#2b2b2b;--acink:#fff;--bar:#f7f7f7;--me:#f7f7f7;--num:#0a6cff;--blue:#0a6cff;--spark:#D97757;--line:rgba(0,0,0,.08);
--glow:rgba(10,108,255,.2);--glow2:rgba(217,119,87,.16);--halo:rgba(10,108,255,.2);--sh-sm:0 1px 0 rgba(255,255,255,.9) inset,0 8px 18px -12px rgba(0,0,0,.22);--sh2:0 34px 70px -40px rgba(0,0,0,.35);
--d:'Geist',system-ui,-apple-system,'Segoe UI',sans-serif;--m:'JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;--e:cubic-bezier(.2,.7,.2,1);color-scheme:light}
html[data-theme="dark"]{--bg:#0b0b0d;--ink:#f2f2f4;--ink2:#b4b4bb;--muted:#8f8f97;--raised:#1d1d20;--field:#26262a;--ac:#f2f2f4;--acink:#111113;--bar:#17171a;--me:#1d1d20;--num:#6aa8ff;--line:rgba(255,255,255,.08);
--glow:rgba(10,108,255,.5);--glow2:rgba(217,119,87,.2);--halo:rgba(10,108,255,.38);--sh-sm:0 1px 0 rgba(255,255,255,.05) inset,0 8px 18px -12px rgba(0,0,0,.8);--sh2:0 1px 0 rgba(255,255,255,.04) inset,0 34px 70px -40px rgba(0,0,0,.9);color-scheme:dark}
html{background:var(--bg);-webkit-text-size-adjust:100%}
body{background:var(--bg);color:var(--ink);font:400 18px/1.5 var(--d);-webkit-font-smoothing:antialiased;overflow-x:hidden}
a{color:inherit;text-decoration:none}
img,svg{display:block}
button{font:inherit;color:inherit}
:focus-visible{outline:2px solid var(--ink);outline-offset:3px}
.skip{position:absolute;left:12px;top:-60px;z-index:100;padding:10px 14px;border-radius:8px;background:var(--ac);color:var(--acink);font-size:16px}
.skip:focus{top:12px}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}
.wrap{width:min(1120px,100% - 48px);margin:0 auto}
/* the header, the switches and the menu — as on the landing */
.nav{position:sticky;top:12px;z-index:50;transition:opacity .35s var(--e),translate .35s var(--e),visibility .35s}
.nav.gone{opacity:0;translate:0 -14px;visibility:hidden;pointer-events:none}
.nav .in{display:flex;align-items:center;gap:26px;height:60px;padding:0 10px 0 22px}
.logo{display:flex;align-items:center;gap:9px;font:700 16px var(--d);letter-spacing:-.01em;color:var(--ink)}
.logo svg{width:22px;height:16px}
.nav nav{display:flex;gap:24px;font-size:14px}
.nav nav a{color:var(--ink2)}
.nav nav a:hover,.nav nav a[aria-current]{color:var(--ink)}
.nav nav a[aria-current]{font-weight:600}
.nav .sp{flex:1}
.lang{display:inline-flex;gap:2px;padding:3px;border-radius:8px;background:var(--raised);box-shadow:var(--sh-sm)}
.lang a{padding:4px 9px;border-radius:6px;font:600 12px/1.2 var(--d);color:var(--muted)}
.lang a:hover{color:var(--ink)}
.lang a[aria-current]{background:var(--ac);color:var(--acink)}
.thm{flex:none;display:inline-grid;place-items:center;width:36px;height:36px;margin-left:8px;border:0;border-radius:8px;background:var(--raised);box-shadow:var(--sh-sm);color:var(--ink);cursor:pointer}
.thm:hover{background:var(--field)}
.thm svg{width:17px;height:17px}
.thm .sun,.mthm .sun,.mthm .to-light,html[data-theme="dark"] .thm .moon,html[data-theme="dark"] .mthm .moon,html[data-theme="dark"] .mthm .to-dark{display:none}
html[data-theme="dark"] .thm .sun,html[data-theme="dark"] .mthm .sun,html[data-theme="dark"] .mthm .to-light{display:block}
.nav .lg{font-size:14px;font-weight:500}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:9px;height:52px;padding:0 26px;border:0;border-radius:8px;font:500 16px/1 var(--d);white-space:nowrap;cursor:pointer;transition:background .15s}
.btn.p{background:var(--ac);color:var(--acink)}
.btn.blue{background:var(--blue);color:#fff}
.btn.blue:hover{background:#2a80ff}
.nav .btn{height:40px;padding:0 18px;font:600 14px/1 var(--d);box-shadow:0 14px 28px -16px rgba(0,0,0,.6)}
.burger{display:none;width:44px;height:44px;border:0;background:none;cursor:pointer;place-items:center;align-content:center;gap:6px}
.burger i{display:block;width:20px;height:2px;background:currentColor;transition:transform .2s}
.burger[aria-expanded="true"] i:first-child{transform:translateY(4px) rotate(45deg)}
.burger[aria-expanded="true"] i:last-child{transform:translateY(-4px) rotate(-45deg)}
.mnav{position:fixed;left:12px;right:12px;top:84px;z-index:60;display:grid;gap:2px;padding:10px;border-radius:16px;background:rgba(241,241,241,.97);box-shadow:var(--sh2)}
html[data-theme="dark"] .mnav{background:rgba(21,21,23,.97)}
.mnav[hidden]{display:none}
.mnav a{padding:13px 14px;border-radius:10px;font-weight:500;font-size:16px}
.mnav a:hover,.mthm:hover{background:var(--field)}
.mnav a[aria-current]{font-weight:700}
.mthm{display:flex;align-items:center;gap:10px;width:100%;padding:12px 14px;border:0;border-radius:10px;background:none;font-size:16px;text-align:left;cursor:pointer}
.mthm svg{width:18px;height:18px;flex:none}
.mnav .row{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:8px;margin-top:8px}
.mnav .row a{display:flex;align-items:center;justify-content:center;min-width:0;height:48px;border-radius:8px}
.mnav .row .in2{background:var(--field)}
.mnav .row .btn{font:600 16px/1 var(--d);padding:0}
/* first screen */
.top{position:relative;padding-top:12px}
.top::before{content:"";position:absolute;left:0;right:0;top:0;height:900px;pointer-events:none;background:radial-gradient(56% 44% at 50% -4%,var(--glow),transparent 76%),radial-gradient(26% 22% at 80% 6%,var(--glow2),transparent 72%)}
.top>main{position:relative}
h1,h2{font-weight:200;letter-spacing:-.055em;line-height:.96}
h1 b,h2 b{font-weight:500}
.hero{text-align:center;padding:108px 0 170px}
.hero h1{font-size:clamp(44px,9.4vw,138px);letter-spacing:-.065em;line-height:.95}
.hero h1 .cl{display:inline-flex;align-items:baseline;gap:.12em;margin-left:.2em;white-space:nowrap}
.hero h1 .spark{height:.64em;width:.64em;fill:var(--spark);transform:translateY(-.03em)}
.hero h1 .word{height:.8em;width:auto;fill:currentColor;transform:translateY(.062em)}
.hero .sub{font-size:23px;line-height:1.4;margin:44px auto 0;max-width:680px}
.steps{list-style:none;display:grid;grid-template-columns:repeat(3,1fr);gap:64px;margin-top:130px}
.steps .n{display:block;font:200 72px/1 var(--d);letter-spacing:-.06em;color:var(--num)}
.steps h3{margin-top:24px;font-size:27px;font-weight:500;letter-spacing:-.025em;line-height:1.15}
.steps p{margin:12px auto 0;max-width:300px;color:var(--ink2);font-size:19px;line-height:1.45}
.steps p a,.fin .note a{color:var(--ink);font-weight:600;text-decoration:underline;text-decoration-thickness:1.5px;text-underline-offset:5px}
.addr{display:flex;align-items:center;gap:18px;width:min(860px,100%);margin:72px auto 0;background:var(--bar);border-radius:8px;padding:14px 14px 14px 30px;text-align:left}
.addr code{flex:1;min-width:0;font:400 clamp(17px,1.8vw,22px)/1.3 var(--m);overflow-wrap:anywhere;user-select:all;-webkit-user-select:all}
.btn[data-copy]{min-width:232px}
.btn[data-copy].ok{background:#12996b}
/* what it does */
.does{padding:60px 0 0;text-align:center}
.does h2{font-size:clamp(40px,5.6vw,84px)}
.does ul{list-style:none;display:grid;grid-template-columns:repeat(4,1fr);gap:48px;margin-top:100px;text-align:left}
.does li b{display:block;font:200 44px/1 var(--d);letter-spacing:-.045em}
.does li span{display:block;margin-top:20px;color:var(--ink2);font-size:19px;line-height:1.5}
.show{padding:190px 0 0;overflow-x:clip}
.show figure{width:min(720px,100% - 32px);margin:0 auto;position:relative}
.show figure::before{content:"";position:absolute;inset:8% -24% -14% -24%;pointer-events:none;background:radial-gradient(50% 50% at 50% 55%,var(--halo),transparent 72%)}
.chat{position:relative;display:flex;flex-direction:column;gap:14px}
.chat .me{align-self:flex-end;max-width:78%;background:var(--me);padding:13px 18px;border-radius:14px;font-size:17px;line-height:1.4}
.chat .tool{display:flex;align-items:center;gap:9px;color:var(--ink2);font-size:16px}
.chat .tool i{width:9px;height:9px;border-radius:50%;background:var(--blue)}
.chat img{width:100%;height:auto}
.chat .lt,html[data-theme="dark"] .chat .dk{display:block}
.chat .dk,html[data-theme="dark"] .chat .lt{display:none}
/* the last block */
.fin{padding:230px 0 200px;text-align:center}
.fin h2{font-size:clamp(44px,7.2vw,112px);letter-spacing:-.06em}
.fin .cta{display:flex;gap:30px;justify-content:center;align-items:center;flex-wrap:wrap;margin-top:56px}
.link{font-weight:600;font-size:18px;text-decoration:underline;text-decoration-thickness:1.5px;text-underline-offset:6px}
.fin .note{margin:64px auto 0;color:var(--ink2);max-width:540px;font-size:18px}
footer{padding:26px 0 36px;border-top:1px solid var(--line);font-size:13.5px;color:var(--muted)}
footer .wrap{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:14px 24px}
footer .l{display:flex;align-items:center;gap:14px}
footer nav{display:flex;flex-wrap:wrap;gap:10px 20px}
footer nav a:hover{color:var(--ink)}
@media (max-width:960px){.nav nav{display:none}.burger{display:grid}}
@media (max-width:760px){
.wrap{width:calc(100% - 32px)}
.nav .thm{display:none}.nav .lang{margin-left:auto}
.hero{padding:52px 0 96px}.hero .sub{font-size:19px;margin-top:28px}
.steps{grid-template-columns:1fr;gap:52px;margin-top:76px}.steps .n{font-size:60px}.steps h3{margin-top:14px}
.addr{flex-direction:column;align-items:stretch;padding:22px 16px 16px;gap:16px;margin-top:56px}.btn[data-copy]{min-width:0}
.does{padding-top:20px}.does ul{grid-template-columns:1fr;gap:44px;margin-top:56px;text-align:center}.does li b{font-size:38px}.does li span{margin-top:10px}
.show{padding-top:100px}.chat .me{max-width:92%}
.fin{padding:130px 0 110px}.fin .cta{margin-top:40px}.fin .note{margin-top:44px}
}
@media (max-width:560px){.nav .lg,.nav .sp,.nav .logo svg{display:none}.nav .in{gap:8px;padding:0 0 0 16px}.nav .btn{padding:0 12px}.burger{width:40px;margin-right:-8px}}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
'''

JS = r'''
(() => {
  const root = document.documentElement, meta = document.querySelector('meta[name="theme-color"]');
  // ☀/☾: dark by default; the choice is shared with the landing (the same storage key)
  const sync = () => { const dark = root.dataset.theme === 'dark';
    document.querySelectorAll('.thm').forEach((b) => b.setAttribute('aria-pressed', String(dark)));
    if (meta) meta.content = dark ? '#0b0b0d' : '#e5e5e5'; };
  document.querySelectorAll('.thm, .mthm').forEach((b) => b.addEventListener('click', () => {
    const dark = root.dataset.theme !== 'dark';
    if (dark) root.dataset.theme = 'dark'; else delete root.dataset.theme;
    try { localStorage.setItem('of-site-theme', dark ? 'dark' : 'light'); } catch (e) {}
    sync(); }));
  sync();
  // the phone menu and the header that hides on the way down
  const b = document.querySelector('.burger'), m = document.getElementById('mnav'), nav = document.querySelector('.nav');
  const open = (o) => { m.hidden = !o; b.setAttribute('aria-expanded', String(o)); b.setAttribute('aria-label', o ? b.dataset.close : b.dataset.open); };
  b.addEventListener('click', () => open(m.hidden));
  m.addEventListener('click', (e) => { if (e.target.closest('a')) open(false); });
  addEventListener('keydown', (e) => { if (e.key === 'Escape' && !m.hidden) { open(false); b.focus(); } });
  addEventListener('resize', () => { if (getComputedStyle(b).display === 'none') open(false); });
  let ticking = false;
  const onScroll = () => { ticking = false; const gone = scrollY > 80; nav.classList.toggle('gone', gone); if (gone && !m.hidden) open(false); };
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();
  // «copy the address»: the clipboard when the browser allows it, otherwise the address is selected for a manual copy
  const code = document.getElementById('addr'), live = document.getElementById('copied'), text = code.textContent.trim();
  const select = () => { const r = document.createRange(); r.selectNodeContents(code); const s = getSelection(); s.removeAllRanges(); s.addRange(r); };
  document.querySelectorAll('[data-copy]').forEach((btn) => {
    const label = btn.querySelector('span'), idle = label.textContent; let timer = 0;
    btn.addEventListener('click', async () => {
      let ok = false;
      try { await navigator.clipboard.writeText(text); ok = true; }
      catch (e) { try { select(); ok = document.execCommand('copy'); } catch (e2) { ok = false; } }
      if (!ok) { select(); code.scrollIntoView({ block: 'center' }); }
      const said = ok ? btn.dataset.done : btn.dataset.fail;
      label.textContent = said; btn.classList.toggle('ok', ok); live.textContent = said;
      clearTimeout(timer); timer = setTimeout(() => { label.textContent = idle; btn.classList.remove('ok'); live.textContent = ''; }, 2400);
    });
  });
})();
'''


def page(lang):
    t = T[lang]
    e = lambda s: html_.escape(s, quote=True)
    home, other = HOME[lang], 'en' if lang == 'ru' else 'ru'
    links = ''.join(f'<a href="{home}#{a}">{e(n)}</a>' for a, n in zip(('why', 'pricing'), t['nav'][:2]))
    links += f'<a href="{PATHS[lang]}" aria-current="page">MCP</a><a href="{home}#faq">{e(t["nav"][2])}</a>'
    cur = ' aria-current="page"'
    langs = ''.join(f'<a href="{PATHS[l]}" hreflang="{l}" lang="{l}"{cur if l == lang else ""}>{l.upper()}</a>' for l in ('en', 'ru'))
    spark = f'<svg class="spark" viewBox="0 0 24 24" aria-hidden="true">{svg_paths("claude-spark.svg")}</svg>'
    word = f'<svg class="word" viewBox="0 0 97 24" role="img" aria-label="Claude">{svg_paths("claude-word.svg")}</svg>'
    copy = lambda cls: (f'<button type="button" class="btn {cls}" data-copy data-done="{e(t["copied"])}" data-fail="{e(t["copy_fail"])}">'
                        f'{COPY}<span>{e(t["copy"])}</span></button>')
    steps = ''.join(f'<li><span class="n" aria-hidden="true">{i}</span><h3>{e(h)}</h3><p>{p}</p></li>' for i, (h, p) in enumerate(t['steps'], 1))
    does = ''.join(f'<li><b>{e(h)}</b><span>{e(p)}</span></li>' for h, p in t['does'])
    # two pictures of the same window, one per theme; the hidden one is not read out (display: none)
    win = lambda theme: (f'<img class="{"dk" if theme == "dark" else "lt"}" src="assets/mcp/window-{lang}-{theme}.webp" width="1120" height="1140" '
                         f'alt="{e(t["chat_alt"])}">')
    foot = ''.join(f'<a href="{home}#doc-{k}">{e(n)}</a>' for k, n in t['foot'])
    url = SITE + PATHS[lang]
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(t["title"])}</title>
<meta name="description" content="{e(t["desc"])}">
<meta name="theme-color" content="#e5e5e5">
<meta property="og:type" content="website">
<meta property="og:site_name" content="ONEFLOW">
<meta property="og:locale" content="{t["locale"]}">
<meta property="og:title" content="{e(t["title"])}">
<meta property="og:description" content="{e(t["desc"])}">
<meta property="og:url" content="{url}">
<link rel="alternate" hreflang="en" href="{SITE}{PATHS["en"]}">
<link rel="alternate" hreflang="ru" href="{SITE}{PATHS["ru"]}">
<link rel="alternate" hreflang="x-default" href="{SITE}{PATHS["en"]}">
<link rel="canonical" href="{url}">
<script>document.documentElement.classList.add('js');try{{if(localStorage.getItem('of-site-theme')!=='light')document.documentElement.dataset.theme='dark'}}catch(e){{document.documentElement.dataset.theme='dark'}}</script>
<link rel="stylesheet" href="fonts.css">
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#main">{e(t["skip"])}</a>
<div class="top">
<header class="nav"><div class="wrap in"><a class="logo" href="{home}" aria-label="{e(t["logo"])}">{LOGO}ONEFLOW</a><nav aria-label="{e(t["sections"])}">{links}</nav><span class="sp"></span><div class="lang" role="group" aria-label="Язык / Language">{langs}</div><button type="button" class="thm" aria-pressed="false" aria-label="{e(t["theme"])}">{MOON}{SUN}</button><a class="lg" href="/app">{e(t["login"])}</a><a class="btn p" href="/app?auth=register">{e(t["register"])}</a><button class="burger" type="button" aria-label="{e(t["open_menu"])}" data-open="{e(t["open_menu"])}" data-close="{e(t["close_menu"])}" aria-expanded="false" aria-controls="mnav"><i></i><i></i></button></div></header>
<nav class="mnav" id="mnav" aria-label="{e(t["menu"])}" hidden>{links}<button type="button" class="mthm">{MOON}{SUN}<span class="to-dark">{e(t["to_dark"])}</span><span class="to-light">{e(t["to_light"])}</span></button><div class="row"><a class="in2" href="/app">{e(t["login"])}</a><a class="btn p" href="/app?auth=register">{e(t["register"])}</a></div></nav>
<main id="main">
<section class="hero"><div class="wrap">
<h1>ONEFLOW <b>MCP</b><br>{e(t["prep"])}<span class="cl">{spark}{word}</span></h1>
<p class="sub">{e(t["sub"])}</p>
<h2 class="sr">{e(t["steps_label"])}</h2>
<ol class="steps">{steps}</ol>
<div class="addr"><span class="sr">{e(t["addr_label"])}: </span><code id="addr">{ADDRESS}</code>{copy("blue")}</div>
<p class="sr" id="copied" role="status" aria-live="polite"></p>
</div></section>
</main>
</div>
<section class="does"><div class="wrap"><h2>{e(t["does_a"])} <b>{e(t["does_b"])}</b></h2><ul>{does}</ul></div></section>
<section class="show"><figure><div class="chat"><div class="me">{e(t["chat_me"])}</div><div class="tool"><i></i>{e(t["chat_tool"])}</div>{win("dark")}{win("light")}</div></figure></section>
<section class="fin"><div class="wrap"><h2>{e(t["fin_a"])}<br><b>{e(t["fin_b"])}</b></h2>
<div class="cta">{copy("blue")}<a class="link" href="/app?auth=register">{e(t["create"])}</a></div>
<p class="note">{t["note"]}</p></div></section>
<footer><div class="wrap"><div class="l"><span class="logo">{LOGO}ONEFLOW</span><span>© 2026</span></div><nav aria-label="{e(t["docs"])}">{foot}</nav></div></footer>
<script>{JS}</script>
</body>
</html>
'''


def build(lang):
    h = page(lang)
    h, nf = inline_fonts(h, FONTS)
    for name in sorted(set(re.findall(r'assets/mcp/([\w-]+\.webp)', h))):
        h = h.replace(f'assets/mcp/{name}', uri(os.path.join(HERE, 'assets', 'mcp', name), 'image/webp'))
    h = h.replace('<meta name="theme-color"', f'<link rel="icon" href="{uri(os.path.join(APPREPO, "public", "favicon.svg"), "image/svg+xml")}" type="image/svg+xml">\n<meta name="theme-color"', 1)
    # nothing may point outside the site: every address is a data: URI, an anchor, or one of the site's own pages
    assert 'assets/' not in h and 'fonts/' not in h and 'fonts.css' not in h
    own = r'(?:/|/ru|/mcp|/ru/mcp|/connect|/app|/app\?auth=register)(?:#[\w-]+)?'
    bad = [u for u in re.findall(r'(?:src|href)="([^"]*)"', h) if not (u.startswith('data:') or u.startswith('#') or re.fullmatch(own, u) or re.fullmatch(re.escape(SITE) + r'(?:/mcp|/ru/mcp)', u))]
    assert not bad, bad[:5]
    assert not re.search(r'url\((?!data:)', h), 'a stylesheet address that is not embedded'
    assert h.count(ADDRESS) == 1, 'the connector address must be written once'
    return h, nf


if __name__ == '__main__':
    out = os.path.join(HERE, 'site', 'mcp'); os.makedirs(out, exist_ok=True)
    for lang, name in (('en', 'mcp.html'), ('ru', 'mcp-ru.html')):
        h, nf = build(lang)
        open(os.path.join(out, name), 'w', encoding='utf-8').write(h)
        print(f'site/mcp/{name} {len(h.encode()) // 1024} KB, {nf} font faces')
        if '--preview' not in sys.argv:
            shutil.copyfile(os.path.join(out, name), os.path.join(APPREPO, 'landing', name))
            print(f'  → {APPREPO}/landing/{name}')
