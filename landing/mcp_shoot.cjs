// Screenshots and checks of the ONEFLOW MCP page (site/mcp/mcp.html, mcp-ru.html):  node mcp_shoot.cjs <out dir>
// Both languages, both themes, a computer and a phone. Checks: nothing sticks out sideways, no text under 16px in the page
// body, nothing is loaded from outside, no script errors, «copy the address» really puts the address in the clipboard,
// the phone menu opens, the theme switch works.
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
const out = process.argv[2]; const dir = path.join(__dirname, 'site', 'mcp');
const ADDRESS = 'https://api.oneflow.art/functions/v1/mcp';
(async () => {
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch(); const notes = []; let checks = 0;
  const ok = (cond, what) => { checks++; if (!cond) notes.push(what); };
  for (const [lang, file] of [['ru', 'mcp-ru.html'], ['en', 'mcp.html']]) for (const theme of ['dark', 'light']) for (const [name, w, h, scale] of [['desk', 1440, 900, 1], ['phone', 390, 844, 2]]) {
    const id = `${lang}-${theme}-${name}`;
    const ctx = await b.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: scale, permissions: ['clipboard-read', 'clipboard-write'] });
    const outside = []; const errors = [];
    await ctx.route('**/*', (r) => { const u = r.request().url(); if (u.startsWith('file:') || u.startsWith('data:')) return r.continue(); outside.push(u); return r.abort(); });
    const p = await ctx.newPage(); p.on('pageerror', (e) => errors.push(String(e))); p.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
    await p.addInitScript((t) => { try { localStorage.setItem('of-site-theme', t); } catch (e) {} }, theme);
    await p.goto('file://' + path.join(dir, file)); await p.waitForTimeout(600);
    ok((await p.evaluate(() => document.documentElement.dataset.theme || 'light')) === theme, `${id}: theme is not ${theme}`);
    ok((await p.evaluate(() => document.documentElement.lang)) === lang, `${id}: lang`);
    ok((await p.evaluate(() => [getComputedStyle(document.querySelector('.nav')).position, getComputedStyle(document.getElementById('mnav')).position].join())) === 'sticky,fixed', `${id}: the header is not sticky or the menu is not fixed`);
    const wide = await p.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    ok(wide <= 0, `${id}: page is ${wide}px wider than the screen`);
    const small = await p.evaluate(() => [...document.querySelectorAll('.hero *, .does *, .show *, .fin *')].filter((e) => !e.closest('.sr') && e.children.length === 0 && e.textContent.trim() && parseFloat(getComputedStyle(e).fontSize) < 16).map((e) => e.textContent.trim().slice(0, 20)).slice(0, 4));
    ok(!small.length, `${id}: text under 16px ${JSON.stringify(small)}`);
    const clipped = await p.evaluate(() => [...document.querySelectorAll('h1, h2, h3, p, code, .btn, .steps li, .does li, header .in > *')].filter((e) => { const r = e.getBoundingClientRect(); return r.width > 0 && !e.closest('.sr, [hidden]') && (r.right > window.innerWidth + 1 || r.left < -1); }).map((e) => e.textContent.trim().slice(0, 24)).slice(0, 4));
    ok(!clipped.length, `${id}: sticks out ${JSON.stringify(clipped)}`);
    // the window picture for this theme is the one on screen
    const shown = await p.evaluate(() => [...document.querySelectorAll('.chat img')].filter((i) => getComputedStyle(i).display !== 'none').map((i) => i.className));
    ok(shown.length === 1 && shown[0] === (theme === 'dark' ? 'dk' : 'lt'), `${id}: window picture ${JSON.stringify(shown)}`);
    ok(await p.evaluate(() => [...document.querySelectorAll('.chat img')].every((i) => i.complete && i.naturalWidth === 1120)), `${id}: the window picture is not loaded`);
    // the whole-page picture is taken after the window picture is decoded and has been on screen once
    await p.evaluate(async () => { for (const i of document.querySelectorAll('.chat img')) { try { await i.decode(); } catch (e) {} } });
    await p.locator('.chat').scrollIntoViewIfNeeded(); await p.waitForTimeout(250); await p.evaluate(() => scrollTo(0, 0)); await p.waitForTimeout(450);
    await p.screenshot({ path: path.join(out, `${id}.png`), fullPage: true });
    if (name === 'desk') await p.screenshot({ path: path.join(out, `${id}-top.png`) });
    // copy the address
    const btn = p.locator('.addr [data-copy]'); const idle = (await btn.locator('span').textContent()).trim();
    await btn.click(); await p.waitForTimeout(150);
    ok((await p.evaluate(() => navigator.clipboard.readText())) === ADDRESS, `${id}: the clipboard does not hold the address`);
    const said = (await btn.locator('span').textContent()).trim();
    ok(said !== idle && said === (await btn.getAttribute('data-done')), `${id}: the button did not say it copied (${said})`);
    ok((await p.locator('#copied').textContent()).trim() === said, `${id}: no spoken confirmation`);
    if (lang === 'ru' && theme === 'dark' && name === 'desk') await p.screenshot({ path: path.join(out, 'copied.png'), clip: { x: 200, y: (await p.locator('.addr').boundingBox()).y - 40, width: 1040, height: 170 } });
    await p.waitForTimeout(2600);
    ok((await btn.locator('span').textContent()).trim() === idle, `${id}: the button label did not come back`);
    // phone: the menu; computer: the theme switch
    if (name === 'phone') {
      await p.evaluate(() => scrollTo(0, 0)); await p.waitForTimeout(450);
      await p.locator('.burger').click(); await p.waitForTimeout(250);
      ok(await p.locator('#mnav').isVisible(), `${id}: the menu did not open`);
      ok((await p.locator('#mnav a[aria-current="page"]').textContent()) === 'MCP', `${id}: MCP is not marked in the menu`);
      ok(await p.evaluate(() => [...document.querySelectorAll('#mnav, #mnav *')].every((e) => { const r = e.getBoundingClientRect(); return r.width === 0 || (r.left >= 0 && r.right <= window.innerWidth); })), `${id}: the menu sticks out`);
      if (lang === 'ru') await p.screenshot({ path: path.join(out, `${id}-menu.png`) });
      await p.keyboard.press('Escape'); ok(!(await p.locator('#mnav').isVisible()), `${id}: Esc did not close the menu`);
    } else {
      await p.evaluate(() => scrollTo(0, 0)); await p.waitForTimeout(450);
      await p.locator('.nav .thm').click();
      const now = await p.evaluate(() => [document.documentElement.dataset.theme || 'light', localStorage.getItem('of-site-theme')]);
      ok(now[0] !== theme && now[1] === now[0], `${id}: the theme switch ${JSON.stringify(now)}`);
      ok((await p.locator('.lang a[aria-current="page"]').textContent()) === lang.toUpperCase(), `${id}: language mark`);
      await p.evaluate(() => scrollTo(0, 400)); await p.waitForTimeout(500);
      ok(await p.evaluate(() => document.querySelector('.nav').classList.contains('gone')), `${id}: the header did not hide on scroll`);
    }
    ok(!outside.length, `${id}: asked the network for ${JSON.stringify(outside.slice(0, 3))}`);
    ok(!errors.length, `${id}: script errors ${JSON.stringify(errors.slice(0, 3))}`);
    await ctx.close();
  }
  await b.close();
  console.log(notes.length ? notes.join('\n') : `ok: ${checks} checks, no problems`);
  process.exit(notes.length ? 1 : 0);
})();
