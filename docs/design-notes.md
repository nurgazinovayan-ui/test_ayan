# nurgazinov.com — Art Director portfolio (static build)

> **RU, коротко:** это готовый статический сайт (HTML + CSS + JS + ассеты), собранный из дизайна в Claude. Его можно сразу открыть через любой локальный сервер или задеплоить. Ниже — описание структуры и задач для Claude Code.

A one-page, dark, cinematic portfolio for an art director with 10+ years of experience. The hero is a real-time 3D cinema hall (three.js): red velvet curtains open on click to reveal the showreel, a projector beam shines from the dot in the logo, and audience silhouettes walk in and take their seats.

No framework and no build step. Plain HTML/CSS/JS, so it can be dropped into any stack or migrated later.

---

## Run locally

Videos and the WebGL scene must be served over HTTP. Opening `index.html` via `file://` will not work.

```bash
cd nurgazinov-portfolio
python3 -m http.server 8080      # or: npx serve .
# open http://localhost:8080
```

## Structure

```
index.html                 all markup (sections in page order)
css/styles.css             all styles (tokens on .site / .site.dark)
js/main.js                 all behaviour (class Site, see below)
assets/js/three.min.js     three.js r159 UMD build (exposes window.THREE)
assets/fonts/              Dx Playhigh Expanded (hero title), Dx Burst (hero tagline), Dx Burst Smooth (unused, spare)
assets/video/              hero-showreel.mp4, film-01-lara.mp4, film-02-night-road.mp4
assets/img/                posters for the videos
assets/logos/              client logos as single-colour SVGs (already inlined in index.html; the files are kept as sources)
```

Google Fonts (loaded in `<head>`): **Archivo** (variable width/weight, used for almost everything) and **Caveat** (loader caption).

## Page sections (in order)

1. **Loader** (`.loader`, fixed overlay). Shows *real* progress, weighted across:
   - fonts (`document.fonts.load`)
   - three.js loaded
   - first 3D frame rendered
   - showreel buffered (`readyState >= 3`, or an error counts as done)
   - posters loaded

   It finishes with a curtain-split exit. A 15 s safety timeout means it can never trap the visitor.
2. **Hero / 3D cinema** (`header.hero`, `.stage3d`).
   - The `<canvas data-ref="canvas">` holds the hall, curtains, seats and silhouettes.
   - The `<canvas data-ref="beam">` holds the projector beam. It is a separate WebGL renderer, CSS-blurred and blended with `mix-blend-mode: screen`.
   - A transparent full-size `<button data-ref="curtains">` toggles the curtains and showreel. Its label is updated for screen readers.
   - Custom cursor badge `.hcur` ("CLICK" / "CLOSE"), shown on fine pointers only.
   - Title letters warp away from the cursor (`warpTitle`).
   - Tagline "love, action & humor" is set in Dx Burst.
3. **Client logo marquee.** CSS animation, pauses on hover. Logos are inline SVG using `fill: currentColor`.
4. **About** (`#about`). Scroll-linked blur fly-in. JS sets `--p` (0–1) on every `[data-r]` element and CSS does the rest. The "10" counts up.
5. **AI films** (`#films`). Accordion rows; each opens an inline player (play/pause, progress, timecode).
6. **Selected work** (`#work`). Asymmetric 12-column tile grid.
7. **Footer / contact** (`#contact`).

## JS overview (`js/main.js`)

Everything runs through `class Site` (`window.site` in the console).

| Method | What it does |
|---|---|
| `init()` | binds nav, hero, films and scroll, starts the loader, boots 3D |
| `boot3d()` / `init3d()` | waits for `window.THREE`, builds the scene, runs the render loop (paused when off-screen or the tab is hidden) |
| `toggleCurtain()` | opens/closes the curtains and plays/pauses the showreel |
| `startLoader()` / `tickLoader()` | real loading progress |
| `scribble()` / `unscribble()` | random hand-drawn SVG underline on nav hover |
| `warpTitle()` / `resetTitle()` | cursor-driven letter distortion on the hero title |
| `updateReveal()` | scroll progress for the About section |
| `bindFilms()` / `renderFilms()` | film accordion and players |

**Film data lives in two places.** `FILMS` at the top of `main.js` drives timing and progress; the rows are written out in `index.html`. Keep them in sync, or move the markup to be generated from `FILMS`.

### 3D notes

- Units are roughly metres. The screen is a 15.4 × 6.3 plane at z = −0.4. Curtains are displaced planes rebuilt every frame (`updateCurtain`). Seats are `InstancedMesh` with a rounded-box helper.
- The audience intro starts when the loader finishes (`site.introAt`).
- The video goes onto the screen as a `VideoTexture`. If the browser blocks texture upload (tainted canvas), the code falls back to positioning the HTML `<video>` over the projected screen rectangle.
- `prefers-reduced-motion` is respected: no curtain sway, no letter warp, near-instant transitions.

## Placeholders to replace (content)

- `Name Surname` in the About text and the footer (©, big wordmark).
- `[City, Country]` in About → Based in, and in the footer.
- Email `hello@[yourname].com` / `mailto:hello@yourname.com`, phone `[+7 000 000 00 00]`.
- Social links (Instagram, Behance, Vimeo, LinkedIn, Telegram) all point to `#contact`.
- **Portrait** in About is a grey plate. Replace it with an `<img>`.
- **Selected work**: all 7 tiles are placeholders (fictional vendors Volta, Nordhaus, Kairo, Orbis, Meridian, Halden, Takumi; grey plates). Replace them with real projects: vendor, title, category, year, image or video.
- **AI films**: titles, years, loglines and tool lists for "Lara" and "Night Road" are placeholders written from the footage. Confirm them with the owner.
- "Watch the full film →" links point to `#films`. Add real links (Vimeo/YouTube) if needed.

## Suggested next steps for Claude Code

1. Fill in the real content above (ask the owner for the data and images).
2. Add SEO and social meta: Open Graph / Twitter image, favicon, canonical `https://nurgazinov.com`.
3. Make the media production-ready:
   - generate WebM/AV1 alongside MP4;
   - add `width`/`height` to media;
   - consider lazy-loading film videos (`preload="none"` until the row opens);
   - compress posters to AVIF/WebP.
4. Upgrade three.js. The UMD build (r159) is deprecated. Migrate to the ES-module build (`import * as THREE from 'three'`) when adding a bundler (Vite works well).
5. Optionally move to a framework (Astro or Next.js) if a CMS is planned for works/films. Keep the 3D hero as a client-only island.
6. Deploy (Vercel / Netlify / Cloudflare Pages) and point the `nurgazinov.com` DNS there.
7. QA:
   - Safari: no `animation-timeline`, so the `.rise` headings in Films/Work simply appear; the About section uses JS and works everywhere.
   - Mobile: the custom cursor is hidden on touch; check 3D performance on low-end phones and consider a static poster fallback below a GPU threshold.
   - Keyboard focus on the hero button and the film rows.

## Fonts / licensing

- **Dx Playhigh Expanded** and **Dx Burst** (`assets/fonts/*.otf`) were supplied by the owner. Make sure the licence covers web embedding, and convert to WOFF2 for production (`fonttools`, with Brotli installed: `pyftsubset … --flavor=woff2`).
- Client logos belong to their owners and are used as a client list.

## Design tokens (quick reference)

- Dark background `#0F0F0E`, ink `#ECEBE7`, muted `#9C9B95`, rules `rgba(236,235,231,.16)`.
- A light theme still exists in CSS (`.site` without `.dark`); the toggle button was removed on request.
- Accents: hero tagline `#FFD60A` with a hard black shadow; cursor badge and loader `#C8FF2E`; small marker dots `#E04E24`. Curtain velvet is about `#8a0f16`.
- Type: hero title = Dx Playhigh (uppercase). Headings = Archivo `font-stretch: 125%`, weights 800 and 200. Small labels = Archivo 500, uppercase, `letter-spacing: .05em`.
