// made in ONEFLOW: the curved row (TiltedGridHero ported to plain JS — see made.py; this file is the
// script itself, put into the built pages by patch_made.mjs).
// The pictures are the built-in ones (--mi0…, squares) until the admin panel publishes its own list
// ('landing.made' in site_content: [{ media, w, h }]). Pictures of any proportions stand in one row:
// every tile has the same height and a width from its own proportions, so nothing is cropped.
(() => {
  const root = document.getElementById('madeBand'); if (!root) return;
  const host = root.parentElement;
  const SB = '__SB__', KEY = '__KEY__', MEDIA = SB + '/storage/v1/object/public/site-media/';
  const BUILT_IN = Array.from({ length: +root.dataset.count || 1 }, (_, i) => ({ bg: `var(--mi${i})`, ar: 1 }));
  let items = BUILT_IN;
  const SLICES = 16, CAMERA = 1.6, MAX_WIDTH = 55, MAX_TILES = 96;
  const speed = 4, gap = 6, axis = 63, curve = 80, fade = 12;
  let tileHeight = 38;  // % of the section height; smaller on phones (set per resize)
  const bend = (Math.min(85, Math.max(5, curve)) * Math.PI) / 180;
  const arc = (b) => (CAMERA - 1 + Math.cos(b)) / (2 * CAMERA * Math.sin(b));
  const deg = (rad) => (rad * 180) / Math.PI, round = (n) => +n.toFixed(4);
  const widest = () => Math.max(1, ...items.map((i) => i.ar));
  // with a wide picture in the row the tiles get lower on a narrow screen, so the widest still fits
  const fit = () => Math.max(1, widest() / 1.5);
  const measure = (width, height) => {
    const h = Math.min((tileHeight / 100) * height, ((MAX_WIDTH / 100) * width) / fit());
    const radius = width * arc(bend);
    if (!(h > 0) || !(radius > 0)) return null;
    const unit = deg(h / radius), limit = deg(bend) + (widest() * unit) / 2;
    // one loop: the pictures, repeated until they go round the whole visible arc and a little further
    const one = items.reduce((a, i) => a + (i.ar + gap / 100) * unit, 0);
    const reps = Math.max(1, Math.min(Math.ceil((2 * limit + unit) / one), Math.floor(MAX_TILES / items.length) || 1));
    const total = reps * one;
    return { reps, unit: round(unit), total: round(total), limit: round(Math.min(total / 2, limit)) };
  };
  const u = (n) => `calc(${round(n)} * min(${tileHeight}cqh, ${round(MAX_WIDTH / fit())}cqw))`;
  const r = 100 * arc(bend), radius = `${+r.toFixed(3)}cqw`;
  const turn = (d) => `translateZ(${radius}) rotateY(${round(d)}deg) translateZ(-${radius})`;
  const mask = `linear-gradient(90deg,transparent,#000 ${fade}%,#000 ${100 - fade}%,transparent)`;
  Object.assign(root.style, { perspective: `${+(r * CAMERA).toFixed(3)}cqw`, perspectiveOrigin: `50% ${axis}%`, maskImage: mask, webkitMaskImage: mask });
  const style = document.createElement('style'); document.head.appendChild(style);
  let cur = null, size = null;
  const render = (L) => {
    const { reps, unit, total, limit } = L, half = total / 2;
    // a square tile with its gap passes a point in `speed` seconds, whatever the mix of proportions
    const duration = round((total / ((1 + gap / 100) * unit)) * speed);
    const hide = round(((half - limit) / (total || 1)) * 100);
    style.textContent = `@keyframes mbOrbit{from{transform:${turn(-half)}}to{transform:${turn(half)}}` +
      (hide > 0.01 ? `0%,${hide}%,${100 - hide}%,100%{visibility:hidden}${hide + 0.001}%,${100 - hide - 0.001}%{visibility:visible}}` : '}') +
      `@media(prefers-reduced-motion:reduce){.mb-tile{animation-play-state:paused}}`;
    root.textContent = '';
    let at = 0;  // degrees from the start of the loop to the left edge of the next tile
    for (let rep = 0; rep < reps; rep++) {
      for (const item of items) {
        const w = item.ar, centre = at + (w * unit) / 2;
        at += (w + gap / 100) * unit;
        const tile = document.createElement('div'); tile.className = 'mb-tile';
        Object.assign(tile.style, { left: `calc(50% - ${u(w / 2)})`, top: `calc(${axis}% - ${u(0.5)})`, width: u(w), height: u(1),
          animation: `mbOrbit ${duration}s linear ${round(-(centre / total) * duration)}s infinite` });
        // the picture is cut into upright strips, each turned a little, so it bends with the row
        const n = Math.min(36, Math.max(6, Math.round(SLICES * w))), share = w / n;
        for (let k = 0; k < n; k++) {
          const s = document.createElement('div'); s.className = 'mb-strip' + (k === 0 ? ' l' : k === n - 1 ? ' r' : '');
          Object.assign(s.style, { left: u((w - share) / 2), width: k === n - 1 ? u(share) : `calc(${u(share)} + 1px)`, height: u(1),
            transform: turn((w / 2 - (k + 0.5) * share) * unit), backgroundImage: item.bg, backgroundSize: `${u(w)} ${u(1)}`, backgroundPosition: `${u(-k * share)} 0` });
          tile.appendChild(s);
        }
        root.appendChild(tile);
      }
    }
    root.classList.add('on');
  };
  const layout = (force) => {
    if (!size) return;
    tileHeight = size.width < 760 ? 30 : 38;
    const next = measure(size.width, size.height);
    if (!next || (!force && cur && cur.reps === next.reps && cur.total === next.total && cur.unit === next.unit)) return;
    cur = next; render(next);
  };
  new ResizeObserver(([entry]) => { size = entry.contentRect; layout(false); }).observe(host);

  // the admin's own pictures: only files of our public bucket, each with its size; anything else is dropped
  const FILE = /^home-banners\/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\.(jpg|png|webp|gif)$/;
  const use = (raw) => {
    let list = [];
    try {
      const data = raw ? JSON.parse(raw) : null;
      list = (Array.isArray(data && data.items) ? data.items : []).slice(0, 24).filter((x) => x && typeof x.media === 'string' && x.media.startsWith(MEDIA) &&
        FILE.test(x.media.slice(MEDIA.length)) && x.w > 0 && x.h > 0 && isFinite(x.w / x.h))
        .map((x) => ({ bg: `url("${x.media}")`, ar: Math.min(2.4, Math.max(0.45, x.w / x.h)) }));
    } catch (e) { list = []; }
    items = list.length ? list : BUILT_IN;
    layout(true);
  };
  try { const c = localStorage.getItem('of-made'); if (c) use(c); } catch (e) {}
  fetch(SB + '/rest/v1/site_content?select=value&key=eq.landing.made', { headers: { apikey: KEY } }).then((res) => (res.ok ? res.json() : null)).then((rows) => {
    if (!Array.isArray(rows)) return;
    const raw = rows[0] && typeof rows[0].value === 'string' ? rows[0].value : '';
    try { raw ? localStorage.setItem('of-made', raw) : localStorage.removeItem('of-made'); } catch (e) {}
    use(raw);
  }).catch(() => {});
})();
