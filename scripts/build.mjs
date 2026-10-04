/*
 * nurgazinov.com — static build
 *
 * Reads the content edited in the admin panel (content/*.json, content/projects/*.json),
 * renders it into src/index.template.html + one page per project, and writes the
 * finished site to dist/. No framework, one dependency (marked, for project texts).
 *
 *   npm run build      → dist/
 *   npm run dev        → build + serve dist/ on http://localhost:8080
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { marked } from 'marked';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SRC = path.join(ROOT, 'src');
const CONTENT = path.join(ROOT, 'content');
const DIST = path.join(ROOT, 'dist');
const SITE_URL = 'https://nurgazinov.com';

// ------------------------------------------------------------------ helpers
const readJSON = (p, fallback = {}) => {
  try { return JSON.parse(fs.readFileSync(p, 'utf8')); } catch (e) {
    if (e.code !== 'ENOENT') throw new Error('Cannot parse ' + p + ': ' + e.message);
    return fallback;
  }
};
const esc = (s) => String(s == null ? '' : s)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const pad2 = (n) => String(n).padStart(2, '0');
const isUrl = (p) => /^https?:\/\//i.test(p || '');
const media = (p) => (!p ? '' : isUrl(p) || p.startsWith('/') ? p : '/' + p);
const abs = (p) => (!p ? '' : isUrl(p) ? p : SITE_URL + media(p));
const isVideo = (p) => /\.(mp4|webm|mov|m4v)$/i.test(p || '');
const localFile = (p) => (p && !isUrl(p) ? path.join(SRC, media(p)) : null);
const parseDur = (s) => {
  const m = String(s || '').trim().match(/^(?:(\d+):)?(\d{1,2}):(\d{2})$/);
  return m ? (Number(m[1] || 0) * 3600 + Number(m[2]) * 60 + Number(m[3])) : 0;
};
const fmtDur = (secs) => pad2(Math.floor(secs / 60)) + ':' + pad2(Math.floor(secs % 60));
const paragraphs = (text) => esc(text).trim().split(/\n\s*\n/).map((x) => x.replace(/\n/g, '<br>')).join('<br><br>');
const warn = (msg) => console.warn('  ! ' + msg);
const checkMedia = (p, where) => {
  const f = localFile(p);
  if (f && !fs.existsSync(f)) warn(where + ': file not found ' + p);
};

// Logo aspect ratio from the file itself (SVG viewBox/width/height, PNG header).
function logoRatio(p) {
  const f = localFile(p);
  try {
    if (f && /\.svg$/i.test(f)) {
      const s = fs.readFileSync(f, 'utf8').slice(0, 4000);
      const vb = s.match(/viewBox\s*=\s*["']\s*[-\d.]+[\s,]+[-\d.]+[\s,]+([\d.]+)[\s,]+([\d.]+)/i);
      if (vb && +vb[2]) return +vb[1] / +vb[2];
      const w = s.match(/\swidth\s*=\s*["']([\d.]+)/i), h = s.match(/\sheight\s*=\s*["']([\d.]+)/i);
      if (w && h && +h[1]) return +w[1] / +h[1];
    }
    if (f && /\.png$/i.test(f)) {
      const b = fs.readFileSync(f);
      const w = b.readUInt32BE(16), h = b.readUInt32BE(20);
      if (h) return w / h;
    }
  } catch (e) { /* fall through */ }
  warn('logo ' + p + ': could not read proportions, using 3:1');
  return 3;
}

function embedUrl(url) {
  const yt = url.match(/(?:youtube\.com\/(?:watch\?v=|shorts\/|embed\/)|youtu\.be\/)([\w-]{6,})/i);
  if (yt) return 'https://www.youtube-nocookie.com/embed/' + yt[1] + '?rel=0';
  const vm = url.match(/vimeo\.com\/(?:video\/)?(\d+)(?:\/(\w+))?/i);
  if (vm) return 'https://player.vimeo.com/video/' + vm[1] + (vm[2] ? '?h=' + vm[2] : '');
  return url;
}

// ------------------------------------------------------------------ content
const hero = readJSON(path.join(CONTENT, 'settings/hero.json'));
const about = readJSON(path.join(CONTENT, 'settings/about.json'));
const contact = readJSON(path.join(CONTENT, 'settings/contact.json'));
const seo = readJSON(path.join(CONTENT, 'settings/seo.json'));
const films = (readJSON(path.join(CONTENT, 'films.json')).films || []).filter((f) => f && f.video);
const logos = (readJSON(path.join(CONTENT, 'logos.json')).logos || []).filter((l) => l && l.file);

const projDir = path.join(CONTENT, 'projects');
const projects = (fs.existsSync(projDir) ? fs.readdirSync(projDir) : [])
  .filter((f) => f.endsWith('.json'))
  .map((f) => {
    const p = readJSON(path.join(projDir, f));
    const slug = String(p.url || f.replace(/\.json$/, '')).toLowerCase().trim()
      .replace(/[^a-z0-9-]+/g, '-').replace(/^-+|-+$/g, '') || f.replace(/\.json$/, '');
    return Object.assign({}, p, { slug });
  })
  .filter((p) => p.published !== false && p.title)
  .sort((a, b) => (Number(a.order) || 0) - (Number(b.order) || 0) || String(b.year).localeCompare(String(a.year)));

{ // duplicate URLs would overwrite each other
  const seen = new Set();
  projects.forEach((p) => {
    if (seen.has(p.slug)) { warn('duplicate project url "' + p.slug + '", adding suffix'); p.slug += '-' + seen.size; }
    seen.add(p.slug);
  });
}

const name = about.name || 'Name Surname';
const email = (contact.email || '').trim();
const phone = (contact.phone || '').trim();
const socials = (contact.socials || []).filter((s) => s && s.label && s.url);

// ------------------------------------------------------------------ shared parts
function head({ title, description, url, image, type = 'website' }) {
  return [
    '<title>' + esc(title) + '</title>',
    '<meta name="description" content="' + esc(description) + '">',
    '<link rel="canonical" href="' + esc(url) + '">',
    '<meta property="og:type" content="' + type + '">',
    '<meta property="og:site_name" content="nurgazinov.com">',
    '<meta property="og:title" content="' + esc(title) + '">',
    '<meta property="og:description" content="' + esc(description) + '">',
    '<meta property="og:url" content="' + esc(url) + '">',
    image ? '<meta property="og:image" content="' + esc(abs(image)) + '">' : '',
    '<meta name="twitter:card" content="summary_large_image">',
    '<meta name="theme-color" content="#0F0F0E">',
    '<link rel="icon" href="/favicon.svg" type="image/svg+xml">'
  ].filter(Boolean).join('\n');
}

function footer() {
  const mail = email ? '<a class="mono" href="mailto:' + esc(email) + '">' + esc(email) + '</a>' : '';
  const tel = phone ? '<a class="mono" href="tel:' + esc(phone.replace(/[^\d+]/g, '')) + '">' + esc(phone) + '</a>' : '';
  return `<footer id="contact" style="padding: clamp(80px, 10vw, 140px) 32px 0; overflow: hidden">
<div class="g12" style="display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); column-gap: 20px; row-gap: 24px; align-items: start">
<div style="grid-column: 1 / span 3; display: flex; flex-direction: column; gap: 6px">
<span class="mono">(04) — Contact</span>
</div>
<div style="grid-column: 4 / span 9; display: flex; flex-direction: column; gap: 40px; align-items: flex-start">
<h2 class="rise" style="margin: 0; font-weight: 400; font-size: clamp(30px, 5.8vw, 92px); line-height: 1; display: flex; flex-wrap: wrap; column-gap: 0.3em">
<span class="disp">Let’s make</span>
<span class="serif" style="color: #E04E24">it felt.</span>
</h2>
${email ? '<a href="mailto:' + esc(email) + '" class="bigmail" style="font-size: clamp(26px, 4.4vw, 64px); line-height: 1; letter-spacing: -0.03em; font-weight: 500">' + esc(email) + '</a>' : ''}
</div>
</div>
<div class="g12" style="display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); column-gap: 20px; row-gap: 40px; margin-top: 96px; align-items: start">
<div style="grid-column: 4 / span 3; display: flex; flex-direction: column; gap: 10px">
<span class="mono" style="color: var(--muted)">Direct</span>
${mail}
${tel}
</div>
<div style="grid-column: 7 / span 3; display: flex; flex-direction: column; gap: 10px">
${socials.length ? '<span class="mono" style="color: var(--muted)">Social</span>' : ''}
${socials.map((s) => '<a class="mono" href="' + esc(s.url) + '" target="_blank" rel="noopener">' + esc(s.label) + ' ↗</a>').join('\n')}
</div>
<div style="grid-column: 10 / span 3; display: flex; flex-direction: column; gap: 10px">
<span class="mono" style="color: var(--muted)">Based in</span>
<span class="mono">${esc(about.city)}</span>
${contact.open_to ? '<span class="mono" style="color: var(--muted); margin-top: 14px">Open to</span>\n<span class="mono">' + esc(contact.open_to) + '</span>' : ''}
</div>
</div>
<div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 16px; margin-top: 112px">
<span class="mono">© ${new Date().getFullYear()} ${esc(name)}</span>
<a class="mono" href="#top">Back to top ↑</a>
</div>
<div class="disp" aria-hidden="true" style="font-size: clamp(28px, 9.4vw, 150px); line-height: 0.9; white-space: nowrap; margin-top: 24px; letter-spacing: -0.02em">${esc(name)}</div>
</footer>`;
}

// ------------------------------------------------------------------ home: sections
function logosSection() {
  if (!logos.length) return '';
  const items = logos.map((l) => {
    checkMedia(l.file, 'logo "' + l.name + '"');
    const h = Math.max(12, Math.min(90, Number(l.height) || 36));
    const w = (h * logoRatio(l.file)).toFixed(1);
    const url = esc(media(l.file));
    return `<li class="logo" aria-label="${esc(l.name)}" style="display: flex; align-items: center">
<span class="clogo" role="img" aria-label="${esc(l.name)}" style="width: ${w}px; height: ${h}px; -webkit-mask-image: url('${url}'); mask-image: url('${url}')"></span>
</li>`;
  }).join('\n');
  const ul = (hidden) => `<ul${hidden ? ' aria-hidden="true"' : ''} style="list-style: none; margin: 0; padding: 0 clamp(56px, 7vw, 104px) 0 0; display: flex; align-items: center; gap: clamp(56px, 7vw, 104px); color: var(--ink); white-space: nowrap">
${items}
</ul>`;
  return `<section aria-label="Selected clients" style="padding: 28px 0 44px; overflow: hidden">
<div style="display: flex; justify-content: space-between; gap: 16px; padding: 0 32px 28px">
<span class="mono">Selected clients</span></div>
<div class="marquee" style="overflow: hidden">
<div class="track" style="display: flex; width: max-content">
${ul(false)}
${ul(true)}
</div>
</div>
</section>`;
}

function portrait() {
  const box = 'grid-column: 1 / span 3; aspect-ratio: 3 / 4; background: var(--p1); display: flex; align-items: flex-end; box-sizing: border-box; overflow: hidden';
  if (about.portrait) {
    checkMedia(about.portrait, 'portrait');
    return `<div class="fly" data-r="" style="--dx: -160px; --dy: 40px; ${box}">
<img src="${esc(media(about.portrait))}" alt="${esc(name)}" loading="lazy" decoding="async" style="width: 100%; height: 100%; object-fit: cover; display: block">
</div>`;
  }
  return `<div class="fly" data-r="" style="--dx: -160px; --dy: 40px; ${box}; padding: 16px">
<span class="mono" style="color: var(--plate-ink)">[ Portrait ]</span>
</div>`;
}

function filmsSection() {
  if (!films.length) return '';
  const total = pad2(films.length);
  const rows = films.map((f, i) => {
    checkMedia(f.video, 'film "' + f.title + '"');
    checkMedia(f.poster, 'film "' + f.title + '" poster');
    const no = pad2(i + 1);
    const open = i === 0;
    const secs = parseDur(f.duration);
    const dur = secs ? fmtDur(secs) : '--:--';
    const tools = (f.tools || []).filter(Boolean);
    return `<li class="film" data-film="${i}" data-secs="${secs || ''}" style="border-top: 1px solid var(--rule)">
<button class="film-row" aria-expanded="${open}" aria-controls="film-panel-${no}" style="width: 100%; display: grid; grid-template-columns: 80px minmax(0, 1.5fr) minmax(0, 1.4fr) 80px 64px 40px; align-items: center; gap: 20px; padding: 28px 0; background: none; border: 0; text-align: left; cursor: pointer; color: var(--ink); font: inherit">
<span class="mono" style="display: flex; align-items: center; gap: 12px"><span class="fdot" style="width: 8px; height: 8px; background: #E04E24; opacity: ${open ? 1 : 0}"></span>${no}</span>
<span class="ft disp" style="font-size: clamp(22px, 3vw, 44px); line-height: 1.05; color: var(${open ? '--ink' : '--dim'})">${esc(f.title)}</span>
<span class="mono col-tools" style="color: var(--muted)">${esc(tools.join(' / '))}</span>
<span class="mono">${esc(f.year)}</span>
<span class="mono col-dur fdur" style="text-align: right">${dur}</span>
<span class="pm" aria-hidden="true" style="justify-self: end; display: flex"><svg width="22" height="22" viewBox="0 0 22 22" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M11 2v18M2 11h18"></path></svg></span>
</button>
<div class="acc${open ? ' open' : ''}" id="film-panel-${no}">
<div class="acc-clip">
<div class="acc-in" style="display: flex; flex-wrap: wrap; gap: 40px 24px; padding: 8px 0 56px; align-items: stretch">
<div class="player " style="flex: 2 1 560px; min-width: 0; position: relative; isolation: isolate; overflow: hidden; aspect-ratio: 16 / 9; background: #121211; color: #FFFFFF; display: flex; flex-direction: column; justify-content: space-between; padding: 20px; box-sizing: border-box">
<video data-ref="filmVideo" src="${esc(media(f.video))}"${f.poster ? ' poster="' + esc(media(f.poster)) + '"' : ''} playsinline="" preload="metadata" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; display: block; cursor: pointer"></video>
<div style="position: relative; display: flex; justify-content: space-between; gap: 16px; pointer-events: none">
<span class="mono blend">Now showing — ${no} / ${total}</span>
<span class="mono blend">AI short film</span>
</div>
<div class="pbtn" style="position: relative; display: flex; justify-content: center; pointer-events: none">
<button class="fplay" aria-label="Play film" style="pointer-events: auto; width: 96px; height: 96px; border-radius: 50%; border: 0; background: #ECEBE7; color: #121211; display: flex; align-items: center; justify-content: center; cursor: pointer; padding: 0">
<span class="ic-pause">
<svg width="26" height="26" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></svg>
</span>
<span class="ic-play">
<svg width="26" height="26" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 4.5v15l12-7.5z"></path></svg>
</span>
</button>
</div>
<div class="blend" style="position: relative; display: flex; flex-direction: column; gap: 10px; pointer-events: none">
<div style="height: 2px; background: rgba(255, 255, 255, 0.3)">
<div class="fprog" style="height: 2px; width: 0.00%; background: #FFFFFF"></div>
</div>
<div style="display: flex; justify-content: space-between; gap: 16px">
<span class="mono ftc" style="font-variant-numeric: tabular-nums">00:00</span>
<span class="mono fdur">${dur}</span>
</div>
</div>
</div>
<div style="flex: 1 1 300px; min-width: 0; display: flex; flex-direction: column; gap: 28px">
<div style="display: flex; justify-content: space-between; align-items: baseline; gap: 16px">
<span class="disp" style="font-size: clamp(40px, 4.6vw, 68px); line-height: 0.9">${esc(f.year)}</span>
<span class="mono">Runtime <span class="fdur">${dur}</span></span>
</div>
<h3 class="serif" style="margin: 0; font-size: clamp(30px, 3.6vw, 52px); line-height: 1.05">${esc(f.title)}</h3>
${f.logline ? '<p style="margin: 0; font-size: 18px; line-height: 1.45; max-width: 34ch; text-wrap: pretty">' + esc(f.logline) + '</p>' : ''}
${tools.length ? `<div style="display: flex; flex-direction: column; gap: 12px">
<span class="mono" style="color: var(--muted)">Tools</span>
<ul style="list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 8px">
${tools.map((t, k) => '<li class="mono" style="font-size: 13px; display: flex; gap: 14px"><span style="color: var(--muted)">' + pad2(k + 1) + '</span><span>' + esc(t) + '</span></li>').join('\n')}
</ul>
</div>` : ''}
${f.link ? '<a href="' + esc(f.link) + '" class="mono" target="_blank" rel="noopener" style="margin-top: auto">Watch the full film →</a>' : ''}
</div>
</div>
</div>
</div>
</li>`;
  }).join('\n\n');
  return `<section id="films" style="padding: clamp(80px, 10vw, 140px) 32px">
<div class="g12" style="display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); column-gap: 20px; row-gap: 24px; align-items: end">
<div style="grid-column: 1 / span 3; display: flex; flex-direction: column; gap: 6px">
<span class="mono">(02) — AI Films</span>
<span class="mono" style="color: var(--muted)">${films.length} short film${films.length === 1 ? '' : 's'}</span>
</div>
<h2 class="rise" style="grid-column: 4 / span 9; margin: 0; font-weight: 400; font-size: clamp(30px, 5.8vw, 92px); line-height: 1; display: flex; flex-wrap: wrap; column-gap: 0.3em">
<span class="disp">Short films</span>
<span class="serif">made with AI</span>
</h2>
</div>
<ol style="list-style: none; margin: 72px 0 0; padding: 0; border-bottom: 1px solid var(--rule)">
${rows}
</ol>
</section>`;
}

// The asymmetric grid from the design, repeated every 7 projects.
const SLOTS = [
  { col: '1 / span 8', mt: 0, ar: '16 / 10', label: 'Key visual — 16:10' },
  { col: '9 / span 4', mt: 140, ar: '4 / 5', label: 'Packshot — 4:5' },
  { col: '1 / span 4', mt: 0, ar: '1 / 1', label: 'Social / motion — 1:1' },
  { col: '6 / span 7', mt: 96, ar: '3 / 2', label: 'Launch film still — 3:2' },
  { col: '1 / -1', mt: 0, ar: '12 / 5', label: 'Campaign / OOH — 12:5' },
  { col: '1 / span 7', mt: 0, ar: '4 / 3', label: 'Key visual — 4:3' },
  { col: '9 / span 4', mt: 160, ar: '1 / 1', label: 'Identity — 1:1' }
];

function coverMedia(p, { lazy = true } = {}) {
  const img = p.cover ? esc(media(p.cover)) : '';
  if (p.cover_video) {
    checkMedia(p.cover_video, 'project "' + p.title + '" cover video');
    return `<video class="cover" data-autoplay="" src="${esc(media(p.cover_video))}"${img ? ' poster="' + img + '"' : ''} muted="" loop="" playsinline="" preload="${lazy ? 'none' : 'auto'}" aria-hidden="true"></video>`;
  }
  if (img) {
    checkMedia(p.cover, 'project "' + p.title + '" cover');
    return `<img class="cover" src="${img}" alt="${esc(p.title)}"${lazy ? ' loading="lazy"' : ''} decoding="async">`;
  }
  return '';
}

function workSection() {
  if (!projects.length) return '';
  const years = projects.map((p) => parseInt(p.year, 10)).filter(Boolean);
  const range = years.length ? (Math.min(...years) === Math.max(...years) ? String(years[0]) : Math.min(...years) + '—' + Math.max(...years)) : '';
  const tiles = projects.map((p, i) => {
    const s = SLOTS[i % SLOTS.length];
    const cover = coverMedia(p);
    return `<a href="/projects/${p.slug}/" class="tile" style="grid-column: ${s.col}${s.mt ? '; margin-top: ' + s.mt + 'px' : ''}">
<div style="overflow: hidden">
<div class="plate${cover ? ' has-media' : ''}" style="aspect-ratio: ${s.ar}; background: var(--p${(i % 7) + 1}); display: flex; flex-direction: column; justify-content: space-between; padding: 16px; box-sizing: border-box">
${cover}
<div class="plate-top" style="display: flex; justify-content: space-between; gap: 16px"><span class="mono" style="color: var(--plate-ink)">${pad2(i + 1)}</span><span class="mono go">View case →</span></div>
${cover ? '' : '<span class="mono" style="color: var(--plate-ink)">[ ' + s.label + ' ]</span>'}
</div>
</div>
<div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 16px; padding-top: 16px">
<div style="display: flex; flex-direction: column; gap: 6px; min-width: 0">
<span class="mono" style="font-weight: 500">${esc(p.client)}</span>
<span style="font-size: clamp(22px, 2.2vw, 32px); line-height: 1.05; font-weight: 500; letter-spacing: -0.015em">${esc(p.title)}</span>
</div>
<div style="display: flex; flex-direction: column; gap: 6px; align-items: flex-end; text-align: right">
<span class="mono" style="color: var(--muted)">${esc(p.category)}</span>
<span class="mono">${esc(p.year)}</span>
</div>
</div>
</a>`;
  }).join('\n\n');
  return `<section id="work" style="padding: clamp(80px, 10vw, 140px) 32px">
<div class="g12" style="display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); column-gap: 20px; row-gap: 24px; align-items: end">
<div style="grid-column: 1 / span 3; display: flex; flex-direction: column; gap: 6px">
<span class="mono">(03) — Work</span>
<span class="mono" style="color: var(--muted)">${range}</span>
</div>
<h2 class="rise" style="grid-column: 4 / span 9; margin: 0; font-weight: 400; font-size: clamp(30px, 5.8vw, 92px); line-height: 1; display: flex; flex-wrap: wrap; column-gap: 0.3em">
<span class="disp">Selected</span>
<span class="serif">work</span>
</h2>
</div>

<div class="g12" style="display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); column-gap: 20px; row-gap: 88px; margin-top: 80px; align-items: start">
${tiles}
</div>
</section>`;
}

// ------------------------------------------------------------------ project page
function blockHtml(b) {
  const cap = (c) => (c ? '<figcaption class="mono">' + esc(c) + '</figcaption>' : '');
  switch (b.type) {
    case 'text':
      return `<section class="pb pb-text g12">
<div class="pb-h">${b.heading ? '<h2 class="mono">' + esc(b.heading) + '</h2>' : ''}</div>
<div class="pb-body mtxt">${marked.parse(b.body || '')}</div>
</section>`;
    case 'image':
      if (!b.image) return '';
      checkMedia(b.image, 'image block');
      return `<figure class="pb pb-image ${b.size === 'inset' ? 'inset' : 'full'}">
<img src="${esc(media(b.image))}" alt="${esc(b.alt || b.caption || '')}" loading="lazy" decoding="async">
${cap(b.caption)}
</figure>`;
    case 'gallery': {
      const imgs = (b.images || []).map((x) => (typeof x === 'string' ? x : x && x.image)).filter(Boolean);
      if (!imgs.length) return '';
      imgs.forEach((x) => checkMedia(x, 'gallery block'));
      const cols = Math.max(2, Math.min(4, Number(b.columns) || 2));
      return `<figure class="pb pb-gallery">
<div class="pb-grid" style="--cols: ${cols}">
${imgs.map((x) => '<img src="' + esc(media(x)) + '" alt="" loading="lazy" decoding="async">').join('\n')}
</div>
${cap(b.caption)}
</figure>`;
    }
    case 'video': {
      let inner = '';
      if (b.embed) {
        inner = `<div class="pb-embed"><iframe src="${esc(embedUrl(b.embed))}" title="${esc(b.caption || 'Video')}" loading="lazy" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe></div>`;
      } else if (b.video) {
        checkMedia(b.video, 'video block');
        const poster = b.poster ? ' poster="' + esc(media(b.poster)) + '"' : '';
        inner = b.loop
          ? `<video data-autoplay="" src="${esc(media(b.video))}"${poster} muted="" loop="" playsinline="" preload="none"></video>`
          : `<video src="${esc(media(b.video))}"${poster} controls="" playsinline="" preload="metadata"></video>`;
      } else return '';
      return `<figure class="pb pb-video">
${inner}
${cap(b.caption)}
</figure>`;
    }
    case 'quote':
      if (!b.text) return '';
      return `<blockquote class="pb pb-quote">
<p class="serif">${esc(b.text)}</p>
${b.author ? '<cite class="mono">' + esc(b.author) + '</cite>' : ''}
</blockquote>`;
    default:
      return '';
  }
}

function projectPage(p, i) {
  const next = projects[(i + 1) % projects.length];
  const url = SITE_URL + '/projects/' + p.slug + '/';
  const credits = (p.credits || []).filter((c) => c && (c.role || c.name));
  const facts = [['Client', p.client], ['Category', p.category], ['Year', p.year], ['Role', p.role]].filter((x) => x[1]);
  const cover = coverMedia(p, { lazy: false });
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
${head({
    title: p.title + (p.client ? ' — ' + p.client : '') + ' · ' + name,
    description: p.summary || seo.description || '',
    url, image: p.cover || seo.og_image, type: 'article'
  })}
<link rel="preload" href="/assets/fonts/Archivo-Variable-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/css/fonts.css">
<link rel="stylesheet" href="/css/styles.css">
<script defer src="/js/main.js"></script>
</head>
<body>
<div id="top" class="site dark project" style="background: var(--bg); color: var(--ink); font-family: 'Archivo', 'Helvetica Neue', Helvetica, sans-serif; font-stretch: 100%">

<nav class="pnav">
<a href="/" class="disp" style="font-size: 20px; letter-spacing: -0.02em; text-transform: none">nurgazinov.com</a>
<div style="display: flex; flex-wrap: wrap; gap: 8px 32px">
<a class="mono nl" href="/#work">← All work<svg class="scrib" viewBox="0 0 100 14" preserveAspectRatio="none" aria-hidden="true"><path d="M0 7 L100 7" pathLength="1"></path></svg></a>
<a class="mono nl" href="#contact">Contact<svg class="scrib" viewBox="0 0 100 14" preserveAspectRatio="none" aria-hidden="true"><path d="M0 7 L100 7" pathLength="1"></path></svg></a>
</div>
</nav>

<header class="phead g12">
<div class="phead-no"><span class="mono">(Case) — ${pad2(i + 1)} / ${pad2(projects.length)}</span></div>
<h1 class="disp phead-title">${esc(p.title)}</h1>
<dl class="phead-facts">
${facts.map((f) => '<div><dt class="mono" style="color: var(--muted)">' + f[0] + '</dt><dd class="mono">' + esc(f[1]) + '</dd></div>').join('\n')}
</dl>
</header>

${cover ? '<figure class="pb pb-cover">' + cover + '</figure>' : ''}

${p.summary || credits.length ? `<section class="pb pb-intro g12">
<p class="pb-lead">${paragraphs(p.summary || '')}</p>
${credits.length ? '<dl class="pb-credits">' + credits.map((c) => '<div><dt class="mono" style="color: var(--muted)">' + esc(c.role) + '</dt><dd class="mono">' + esc(c.name) + '</dd></div>').join('\n') + '</dl>' : ''}
</section>` : ''}

${(p.blocks || []).map(blockHtml).filter(Boolean).join('\n\n')}

${next && next !== p ? `<a class="pnext" href="/projects/${next.slug}/">
<span class="mono" style="color: var(--muted)">Next case →</span>
<span class="disp pnext-title">${esc(next.title)}</span>
<span class="mono">${esc(next.client)}</span>
</a>` : ''}

${footer()}

</div>
</body>
</html>
`;
}

// ------------------------------------------------------------------ write
function copyDir(from, to, skip) {
  fs.mkdirSync(to, { recursive: true });
  for (const e of fs.readdirSync(from, { withFileTypes: true })) {
    if (skip && skip(e.name)) continue;
    const a = path.join(from, e.name), b = path.join(to, e.name);
    if (e.isDirectory()) copyDir(a, b, skip); else fs.copyFileSync(a, b);
  }
}

function build() {
  console.log('Building nurgazinov.com …');
  fs.rmSync(DIST, { recursive: true, force: true });
  copyDir(SRC, DIST, (n) => n === 'index.template.html' || n === '.gitkeep' || n === '.DS_Store');

  // Admin panel: Decap CMS bundle from node_modules (self-hosted, no CDN needed)
  const cms = path.join(ROOT, 'node_modules/decap-cms/dist/decap-cms.js');
  if (fs.existsSync(cms)) fs.copyFileSync(cms, path.join(DIST, 'admin/decap-cms.js'));
  else warn('decap-cms is not installed — run "npm install" (the admin panel needs it)');

  checkMedia(hero.video, 'hero video');
  checkMedia(hero.poster, 'hero poster');

  const vars = {
    'hero.video': esc(media(hero.video)),
    'hero.poster': esc(media(hero.poster)),
    'about.text': paragraphs(about.text || ''),
    'about.years': esc(about.years || 10),
    'about.views': esc(about.views),
    'about.focus': esc(about.focus),
    'about.city': esc(about.city)
  };
  let html = fs.readFileSync(path.join(SRC, 'index.template.html'), 'utf8');
  html = html
    .replace('<!--@head-->', () => head({
      title: seo.title || 'nurgazinov.com — Art Director',
      description: seo.description || '',
      url: SITE_URL + '/',
      image: seo.og_image || hero.poster
    }))
    .replace('<!--@logos-->', () => logosSection())
    .replace('<!--@portrait-->', () => portrait())
    .replace('<!--@films-->', () => filmsSection())
    .replace('<!--@work-->', () => workSection())
    .replace('<!--@footer-->', () => footer())
    .replace(/\{\{([\w.]+)\}\}/g, (m, k) => (k in vars ? vars[k] : m));
  if (!films.length) html = html.replace(/<a class="mono nl" href="#films">.*?<\/a>\n/, '');
  if (!projects.length) html = html.replace(/<a class="mono nl" href="#work">.*?<\/a>\n/, '');
  if (!hero.poster) html = html.replace(' poster=""', '');
  fs.writeFileSync(path.join(DIST, 'index.html'), html);

  projects.forEach((p, i) => {
    const dir = path.join(DIST, 'projects', p.slug);
    fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(path.join(dir, 'index.html'), projectPage(p, i));
  });

  const today = new Date().toISOString().slice(0, 10);
  const urls = ['/'].concat(projects.map((p) => '/projects/' + p.slug + '/'));
  fs.writeFileSync(path.join(DIST, 'sitemap.xml'),
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    urls.map((u) => '  <url><loc>' + SITE_URL + u + '</loc><lastmod>' + today + '</lastmod></url>').join('\n') +
    '\n</urlset>\n');
  fs.writeFileSync(path.join(DIST, 'robots.txt'), 'User-agent: *\nDisallow: /admin/\nSitemap: ' + SITE_URL + '/sitemap.xml\n');

  console.log('  ✓ index.html, ' + projects.length + ' project page(s), ' + films.length + ' film(s), ' + logos.length + ' logo(s) → dist/');
}

build();
