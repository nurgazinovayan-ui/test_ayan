// Real screenshots of the mini app's screens from the development server, with sample data.
const { chromium } = require('playwright');
const path = require('path');
const out = process.argv[2];
const BASE = 'http://localhost:5175/tg.html';
const stub = (lang) => `window.__back=false;window.Telegram={WebApp:{initData:'',initDataUnsafe:{user:{first_name:'Аян',language_code:'${lang}'}},version:'8.0',platform:'ios',ready(){},expand(){},isVersionAtLeast(){return true},setHeaderColor(){},setBackgroundColor(){},disableVerticalSwipes(){},BackButton:{show(){window.__back=true},hide(){window.__back=false},onClick(cb){window.__backCb=cb},offClick(){}},HapticFeedback:{notificationOccurred(){},selectionChanged(){}},openInvoice(u,cb){},openTelegramLink(){},downloadFile(p,cb){cb(true)},requestWriteAccess(cb){cb(true)}}};`;

(async () => {
  const browser = await chromium.launch();
  const errors = [];
  const open = async (mode, lang = 'ru', telegram = true) => {
    const ctx = await browser.newContext({ viewport: { width: 390, height: 708 }, deviceScaleFactor: 2 });
    const page = await ctx.newPage();
    await page.route('https://telegram.org/**', (r) => r.fulfill({ contentType: 'application/javascript', body: telegram ? stub(lang) : '' }));
    page.on('pageerror', (e) => errors.push(`${mode}: ${e.message}`));
    page.on('console', (m) => m.type() === 'error' && errors.push(`${mode}: console ${m.text().slice(0, 200)}`));
    await page.goto(mode === null ? BASE : `${BASE}?preview=${mode}`);
    await page.waitForTimeout(900);
    return page;
  };
  const backs = {};
  const shot = async (page, name) => {
    await page.waitForTimeout(350);
    backs[name] = await page.evaluate(() => window.__back === true);
    await page.screenshot({ path: path.join(out, `${name}.png`) });
    // nothing may be wider than the screen
    const wide = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    if (wide > 0) errors.push(`${name}: ${wide}px wider than the screen`);
  };
  const PROMPT = 'Кулон с бриллиантом в жидком серебре, холодный голубой свет, макро';

  let p = await open('1');
  await shot(p, '01-home');
  await p.click('.tile >> nth=0');
  await p.fill('textarea', PROMPT);
  await p.setInputFiles('input[type=file]', '/home/user/oneflow/public/auth-gallery/coffee.webp');
  await shot(p, '02-gen-image');
  await p.click('.row');
  await shot(p, '03-quality');
  await p.click('.opt >> nth=1');
  await p.click('.mainbtn');
  await p.waitForSelector('.res');
  await shot(p, '06-result');
  await p.click('.acts button >> nth=1');
  await p.waitForSelector('.toast');
  await shot(p, '07-sent');
  await p.click('.tabs button >> nth=1');
  await shot(p, '08-gallery');
  await p.click('.thumb.v');
  await p.waitForSelector('.res video');
  await p.waitForTimeout(1200);
  await shot(p, '08b-gallery-video');
  await p.click('.tabs button >> nth=2');
  await p.waitForSelector('.pack');
  await shot(p, '09-balance');
  await p.click('.tabs button >> nth=0');
  await p.click('.row.invite');
  await p.waitForSelector('.hero');
  await shot(p, '11-invite');
  await p.evaluate(() => window.__backCb());
  await p.click('.tile.w');
  await shot(p, '12-casting');
  await p.evaluate(() => window.__backCb());
  await p.click('.tile >> nth=1');
  await p.fill('textarea', 'Крупный план ног бегущего в кроссовках, утренний город, камера летит рядом');
  await p.click('.chips >> nth=1 >> button >> nth=1');
  await shot(p, '04-gen-video');
  await p.context().close();

  p = await open('hold');
  await p.click('.tile >> nth=0');
  await p.fill('textarea', PROMPT);
  await p.click('.mainbtn');
  await shot(p, '05-making');
  await p.context().close();

  p = await open('short');
  await p.click('.tile >> nth=0');
  await p.fill('textarea', PROMPT);
  await p.click('.row');
  await p.click('.opt >> nth=1');
  await p.click('.mainbtn');
  await p.waitForSelector('.shortage');
  await shot(p, '10-short');
  await p.context().close();

  p = await open('refused');
  await p.click('.tile >> nth=0');
  await p.fill('textarea', PROMPT);
  await p.click('.mainbtn');
  await p.waitForSelector('.toast');
  await shot(p, '13-notice');
  await p.context().close();

  p = await open('empty');
  await shot(p, '14-home-new');
  await p.click('.tabs button >> nth=1');
  await shot(p, '15-gallery-empty');
  await p.context().close();

  p = await open(null, 'ru', false);
  await shot(p, '16-outside');
  await p.context().close();

  p = await open('1', 'en');
  await shot(p, '17-home-en');
  await p.click('.tile >> nth=0');
  await shot(p, '18-gen-en');
  await p.click('.row');
  await shot(p, '19-quality-en');
  await p.context().close();

  // a narrow phone: nothing may overflow
  {
    const ctx = await browser.newContext({ viewport: { width: 320, height: 568 }, deviceScaleFactor: 1 });
    const page = await ctx.newPage();
    await page.route('https://telegram.org/**', (r) => r.fulfill({ contentType: 'application/javascript', body: stub('ru') }));
    await page.goto(`${BASE}?preview=1`);
    await page.waitForTimeout(900);
    for (const step of [null, '.tile >> nth=0', '.tabs-none']) {
      if (step === '.tabs-none') break;
      if (step) await page.click(step);
      await page.waitForTimeout(300);
      const wide = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
      const clipped = await page.evaluate(() => [...document.querySelectorAll('.pad *')].filter((e) => e.getBoundingClientRect().right > window.innerWidth + 0.5).length);
      if (wide > 0 || clipped > 0) errors.push(`320px ${step ?? 'home'}: wide ${wide}, clipped ${clipped}`);
    }
    await page.screenshot({ path: path.join(out, '20-narrow.png') });
    await ctx.close();
  }
  await browser.close();
  require('fs').writeFileSync(path.join(out, 'backs.json'), JSON.stringify(backs));
  console.log(errors.length ? errors.join('\n') : 'no errors');
})();
