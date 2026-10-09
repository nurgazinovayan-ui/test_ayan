"""«New AI models» — a row of rectangular video/image cards right under the hero (above the models ticker), each
with a small «NEW» badge, a title and a short line of text.

The cards come from the admin page (oneflow.art/admin → «Новинки на сайте»): one JSON row 'landing.news' in
site_content ({v: 1, items: [{type, media, poster, isNew, link, ru: {title, text}, en: {title, text}}]}), media in the
public 'site-media' bucket. admin-api validates on save; the page checks again before showing anything (media only from
our bucket or the site itself, links only https:// or a path on this site) and builds the cards with DOM calls, never
innerHTML. Until something is published, the built-in cards below are shown (they are in the HTML, so the row is never
empty, even without JavaScript). Text follows the page language; a card without English falls back to Russian.
"""

SB = 'https://ayxmfihtrsacfdhszsri.supabase.co'
KEY = 'sb_publishable_xfd5nkUu18qvdzoo-dzhHQ_f5RKq4tS'  # publishable key (already public in the page's CMS script)

# built-in cards: (CSS image variable from made.py, title, text)
DEFAULT_NEWS = [
    ('--mi2', 'Nano Banana 2.1', 'Новая модель Google: 4K, в 2 раза дешевле'),
    ('--mi0', 'Kling 3.0', 'Видео из фото или текста'),
    ('--mi3', 'Seedance 2.5', 'Новое поколение видео от ByteDance'),
    ('--mi1', 'GPT Image 2.5 Sunburst', 'Новая модель изображений OpenAI'),
    ('--mi4', 'Lyria 3 Pro', 'Музыка по описанию от Google'),
]  # the admin can publish up to 6


def news_html():
    cards = ''.join(
        f'<article class="nw-card"><div class="nw-media" style="background-image:var({var})"></div>'
        f'<span class="nw-new">NEW</span><div class="nw-txt"><b>{title}</b><span>{text}</span></div></article>'
        for var, title, text in DEFAULT_NEWS)
    return f'<div class="news" id="news" role="region" aria-label="Новинки ИИ-моделей"><div class="wrap"><div class="nw-row">{cards}</div></div></div>'


NEWS_CSS = """
/* news: rectangular video/image cards under the hero; they share the row while they fit, then the row scrolls */
.news { position: relative; z-index: 1; margin: 8px 0 0; }
.nw-row { display: flex; gap: 12px; overflow-x: auto; scroll-snap-type: x mandatory; scroll-padding: 0 20px; scrollbar-width: none;
  padding: 8px 20px 36px; margin: -8px -20px -36px; }
.nw-row::-webkit-scrollbar { display: none; }
/* centred while they fit; once the row scrolls, the auto margins collapse and it starts at the left edge */
.nw-row > :first-child { margin-left: auto; } .nw-row > :last-child { margin-right: auto; }
.nw-card { position: relative; flex: 1 1 0; min-width: 190px; max-width: 260px; aspect-ratio: 21 / 9; border-radius: 16px; overflow: hidden; scroll-snap-align: start; isolation: isolate;
  background: #cfcfcf; box-shadow: none; color: #fff; text-decoration: none;
  transition: transform .3s var(--e); }
a.nw-card:hover { transform: translateY(-3px); }
.nw-media, .nw-card video, .nw-card img { position: absolute; inset: 0; z-index: -2; width: 100%; height: 100%; object-fit: cover; background: center / cover no-repeat; }
.nw-card { --nw-grain: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='80' height='80'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0.1 0'/%3E%3C/filter%3E%3Crect width='80' height='80' filter='url(%23n)'/%3E%3C/svg%3E"); }
/* ring of matte blue glass (the app's light-theme glass): frosted grain, a soft sheen running round it */
.nw-card::before { content: ''; position: absolute; inset: 0; z-index: 2; border-radius: inherit; padding: 3px; pointer-events: none;
  background: var(--nw-grain),
    conic-gradient(from var(--nwa), rgba(255,255,255,0) 0deg, rgba(225,240,255,.9) 34deg, rgba(255,255,255,0) 80deg, rgba(255,255,255,0) 180deg, rgba(160,210,255,.55) 214deg, rgba(255,255,255,0) 260deg),
    linear-gradient(165deg, rgba(42,111,230,.82), rgba(15,67,168,.88));
  -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0); -webkit-mask-composite: xor; mask-composite: exclude;
  animation: nwBorder 4.5s linear infinite; }
/* the sheen runs round the card (stays still where @property isn't supported) */
@property --nwa { syntax: '<angle>'; inherits: false; initial-value: 0deg; }
@keyframes nwBorder { to { --nwa: 360deg; } }
.nw-card::after { content: ''; position: absolute; inset: 0; z-index: -1; background: linear-gradient(180deg, rgba(0,0,0,0) 38%, rgba(0,0,0,.72)); }
.nw-new { position: absolute; left: 6px; top: 6px; width: 40px; height: 40px; display: grid; place-items: center; isolation: isolate;
  color: #fff; font: 800 8.5px/1 var(--d); letter-spacing: .05em; transform: rotate(-14deg); text-shadow: 0 1px 1px rgba(0,15,50,.4);
  filter: drop-shadow(0 3px 8px rgba(10,40,120,.4)); }
/* a scalloped «flower» sticker of matte blue glass: frosted, a glow from below; the shape turns slowly, the word stays put */
.nw-new::before { content: ''; position: absolute; inset: 0; z-index: -1;
  background: var(--nw-grain), linear-gradient(120deg, rgba(255,255,255,0) 30%, rgba(225,240,255,.55) 50%, rgba(255,255,255,0) 70%),
    radial-gradient(110% 90% at 50% 110%, rgba(150,205,255,.8), rgba(60,140,255,.35) 45%, rgba(60,140,255,0) 75%),
    linear-gradient(165deg, rgba(42,111,230,.88), rgba(15,67,168,.92));
  -webkit-backdrop-filter: blur(8px) saturate(150%); backdrop-filter: blur(8px) saturate(150%);
  clip-path: path('M20.00 4.80 A5.07 5.07 0 0 1 28.93 7.70 A5.07 5.07 0 0 1 34.46 15.30 A5.07 5.07 0 0 1 34.46 24.70 A5.07 5.07 0 0 1 28.93 32.30 A5.07 5.07 0 0 1 20.00 35.20 A5.07 5.07 0 0 1 11.07 32.30 A5.07 5.07 0 0 1 5.54 24.70 A5.07 5.07 0 0 1 5.54 15.30 A5.07 5.07 0 0 1 11.07 7.70 A5.07 5.07 0 0 1 20.00 4.80 Z'); animation: nwSpin 14s linear infinite; }
@keyframes nwSpin { to { transform: rotate(360deg); } }
.nw-txt { position: absolute; left: 12px; right: 12px; bottom: 9px; display: grid; gap: 2px; text-shadow: 0 1px 8px rgba(0,0,0,.35); }
.nw-txt b { font: 600 13px/1.25 var(--d); letter-spacing: -.01em; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.nw-txt span { font-size: 11px; line-height: 1.35; color: rgba(255,255,255,.82); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
@media (prefers-reduced-motion: reduce) { .nw-new::before, .nw-card::before { animation: none; } }
@media (max-width: 760px) { .news { margin-top: 4px; } .nw-card { flex: none; width: 62vw; min-width: 0; max-width: 228px; } }
"""

JS_NEWS = """<script>
// news cards under the menu: the admin's published list ('landing.news' in site_content) replaces the built-in cards
(() => {
  const row = document.querySelector('#news .nw-row'); if (!row) return;
  const builtIn = [...row.children];  // shown again if the admin's list is removed
  const SB = '__SB__', KEY = '__KEY__', MEDIA = SB + '/storage/v1/object/public/site-media/';
  const okMedia = (u) => typeof u === 'string' && ((u.startsWith(MEDIA) && /^[\\w\\-/]+\\.(jpg|png|webp|gif|mp4|webm)$/.test(u.slice(MEDIA.length))) || /^\\/[\\w.\\-/]+$/.test(u));
  const okLink = (u) => typeof u === 'string' && (/^https:\\/\\/[^\\s"'<>]+$/i.test(u) || /^\\/[\\w.\\-/?=&#]*$/.test(u));
  const en = document.documentElement.lang === 'en';
  const pick = (x, k) => { const a = (en ? x.en : x.ru) || {}, b = (en ? x.ru : x.en) || {}; return String(a[k] || b[k] || '').slice(0, 200); };
  const render = (items) => {
    const cards = items.filter((x) => x && okMedia(x.media) && (pick(x, 'title'))).slice(0, 6).map((x) => {
      const card = document.createElement(x.link && okLink(x.link) ? 'a' : 'article'); card.className = 'nw-card';
      if (card.tagName === 'A') { card.href = x.link; if (/^https:/i.test(x.link)) { card.target = '_blank'; card.rel = 'noopener'; } }
      let m;
      if (x.type === 'video') { m = document.createElement('video'); Object.assign(m, { muted: true, loop: true, playsInline: true, autoplay: true, preload: 'metadata' });
        m.setAttribute('muted', ''); m.setAttribute('playsinline', ''); m.setAttribute('aria-hidden', 'true'); if (okMedia(x.poster)) m.poster = x.poster;
        if (matchMedia('(prefers-reduced-motion: reduce)').matches) m.autoplay = false; }
      else { m = document.createElement('img'); m.alt = ''; m.loading = 'lazy'; m.decoding = 'async'; }
      m.src = x.media; card.appendChild(m);
      if (x.isNew !== false) { const n = document.createElement('span'); n.className = 'nw-new'; n.textContent = 'NEW'; card.appendChild(n); }
      const t = document.createElement('div'); t.className = 'nw-txt'; const b = document.createElement('b'); b.textContent = pick(x, 'title'); t.appendChild(b);
      const s = pick(x, 'text'); if (s) { const sp = document.createElement('span'); sp.textContent = s; t.appendChild(sp); }
      card.appendChild(t); return card; });
    if (cards.length) row.replaceChildren(...cards);
  };
  const use = (raw) => { try { const v = JSON.parse(raw); if (v && Array.isArray(v.items)) render(v.items); } catch (e) {} };
  try { const c = localStorage.getItem('of-news'); if (c) use(c); } catch (e) {}
  fetch(SB + '/rest/v1/site_content?select=value&key=eq.landing.news', { headers: { apikey: KEY } }).then((r) => r.ok ? r.json() : null).then((rows) => {
    if (!rows) return; const raw = rows[0] && rows[0].value;
    try { raw ? localStorage.setItem('of-news', raw) : localStorage.removeItem('of-news'); } catch (e) {}
    if (raw) use(raw); else row.replaceChildren(...builtIn); }).catch(() => {});
})();
</script>
""".replace('__SB__', SB).replace('__KEY__', KEY)
