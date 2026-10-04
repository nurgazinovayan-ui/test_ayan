# nurgazinov.com — Art Director portfolio (static build)

> **RU, коротко:** это готовый статический сайт (HTML + CSS + JS + ассеты), собранный из дизайна в Claude. Все шрифты лежат внутри проекта, интернет для них не нужен. Ниже описана структура и задачи для Claude Code.

A one-page, dark, cinematic portfolio for an art director with 10+ years of experience. The hero is a real-time 3D cinema hall built with three.js:

- red velvet curtains open on click to reveal the showreel;
- a projector beam shines from the dot in the logo;
- audience silhouettes walk in and take their seats.

There is no framework and no build step: plain HTML/CSS/JS, easy to drop into any stack or migrate later.

---

## Run locally

Videos and WebGL work best over HTTP. Fonts are embedded, so they also render from `file://`.

```bash
cd nurgazinov-portfolio
python3 -m http.server 8080      # or: npx serve .
# open http://localhost:8080
```

## Structure

```
index.html                 all markup (sections in page order)
css/fonts.css              ALL fonts as embedded @font-face (data URIs) — no network needed
css/styles.css             all styles (tokens on .site / .site.dark)
js/main.js                 all behaviour (class Site, see below)
assets/js/three.min.js     three.js r159 UMD build (exposes window.THREE)
assets/fonts/              the same fonts as files (.woff2 + original .otf)
assets/video/              hero-showreel.mp4, film-01-lara.mp4, film-02-night-road.mp4
assets/img/                posters for the videos
assets/logos/              client logos as single-colour SVGs (already inlined in index.html; files kept as sources)
```

## Fonts used

| Family | File | Where |
|---|---|---|
| **Dx Playhigh Expanded** (owner-supplied) | `DxPlayhigh-Expanded.woff2` | hero title "ART DIRECTOR / EMOTION FIRST", loader percentage |
| **Dx Burst Regular** (owner-supplied) | `DxBurst-Regular.woff2` | hero tagline "love, action & humor" (yellow, `#FFD60A`) |
| **Archivo** (variable: weight 100–900, width 62–125%) | `Archivo-Variable-latin.woff2` | everything else |
| **Caveat** (variable: weight 400–700) | `Caveat-Variable-latin.woff2` | loader caption ("finding your seat…") |

Archivo is used in three ways:

- logo, headings, film titles and footer name: `font-stretch: 125%`, weight 800, uppercase;
- the light half of headings ("made with AI", "work", "it felt."): `font-stretch: 125%`, weight 200;
- small labels: weight 500, uppercase, `letter-spacing: .05em`.

`DxBurst-Smooth` is included as a spare and is not used.

The fonts are embedded as base64 in `css/fonts.css` so they never "disappear", even in previews without network or opened via `file://`. For production you can switch each `src:` to `url(../assets/fonts/<file>.woff2)` to get smaller CSS and better caching.

## Page sections (in order)

1. **Loader** (`.loader`, fixed overlay). Shows *real* progress, weighted across:
   - fonts;
   - three.js loaded;
   - first 3D frame rendered;
   - showreel buffered;
   - posters loaded.

   It exits by splitting like curtains, and a 15 s safety timeout keeps it from hanging.
2. **Hero / 3D cinema** (`header.hero`, `.stage3d`).
   - `<canvas data-ref="canvas">` draws the hall, curtains, seats and silhouettes.
   - `<canvas data-ref="beam">` draws the projector beam: a second WebGL renderer, CSS-blurred, `mix-blend-mode: screen`.
   - A transparent full-size `<button data-ref="curtains">` toggles the curtains and the showreel.
   - Custom cursor badge `.hcur` ("CLICK" / "CLOSE"), shown on fine pointers only.
   - Title letters warp away from the cursor (`warpTitle`).
3. **Client logo marquee.** CSS animation that pauses on hover. Logos are inline SVG with `fill: currentColor`.
4. **About** (`#about`). Scroll-linked blur fly-in: JS sets `--p` (0–1) on each `[data-r]` element. The "10" counts up.
5. **AI films** (`#films`). Accordion rows, each opening an inline player.
6. **Selected work** (`#work`). Asymmetric 12-column tile grid.
7. **Footer / contact** (`#contact`).

## JS overview (`js/main.js`)

Everything lives in `class Site` (`window.site` in the console):

| Method | What it does |
|---|---|
| `init()` | binds nav, hero, films and scroll; starts the loader; boots 3D |
| `boot3d()` / `init3d()` | waits for `window.THREE`, builds the scene, runs the render loop (paused off-screen or when the tab is hidden) |
| `toggleCurtain()` | opens/closes the curtains and plays/pauses the showreel |
| `startLoader()` / `tickLoader()` | real loading progress |
| `scribble()` / `unscribble()` | random hand-drawn SVG underline on nav hover |
| `warpTitle()` / `resetTitle()` | cursor-driven letter distortion |
| `updateReveal()` | scroll progress for About |
| `bindFilms()` / `renderFilms()` | film accordion and players |

**Film data lives in two places:** `FILMS` at the top of `main.js` and the rows written out in `index.html`. Keep them in sync, or generate the markup from `FILMS`.

### 3D notes

- Units are roughly metres. The screen is a 15.4 × 6.3 plane at z = −0.4.
- Curtains are displaced planes rebuilt every frame. Seats use `InstancedMesh` with a rounded-box helper.
- The audience intro starts when the loader finishes (`site.introAt`).
- The video is shown on the screen as a `VideoTexture`. If texture upload is blocked (tainted canvas), the HTML `<video>` is positioned over the projected screen rectangle instead.
- `prefers-reduced-motion` is respected.

## Placeholders to replace (content)

- `Name Surname` in the About text and the footer.
- `[City, Country]` in About and the footer.
- Email `hello@[yourname].com`, phone `[+7 000 000 00 00]`.
- Social links: they all point to `#contact`.
- **Portrait** in About: currently a grey plate; replace it with an `<img>`.
- **Selected work**: all 7 tiles are placeholders (fictional vendors, grey plates). Replace them with real projects: vendor, title, category, year, image or video.
- **AI films**: titles, years, loglines and tools for "Lara" and "Night Road" are placeholders; confirm them with the owner.
- "Watch the full film →" links point to `#films`.

## Suggested next steps for Claude Code

1. Fill in the real content above.
2. Add OG/Twitter meta, a favicon, and a canonical `https://nurgazinov.com`.
3. Media:
   - provide WebM/AV1 versions of the videos;
   - lazy-load the film videos;
   - convert posters to AVIF/WebP.
4. Migrate three.js from the deprecated UMD build (r159) to the ES-module build when adding a bundler (Vite).
5. Optionally move to Astro or Next.js if works and films should come from a CMS. Keep the 3D hero as a client-only island.
6. Deploy to Vercel, Netlify or Cloudflare Pages and point the `nurgazinov.com` DNS there.
7. QA:
   - Safari: `.rise` headings use `animation-timeline` and simply appear there.
   - Mobile: check 3D performance.
   - Keyboard: check focus states.

## Licensing

- Make sure the licences for **Dx Playhigh** and **Dx Burst** allow web embedding.
- Archivo and Caveat are under the SIL Open Font License.
- Client logos belong to their owners.
