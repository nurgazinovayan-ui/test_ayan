import type { CSSProperties, ReactNode } from 'react';
import { interpolate, spring } from 'remotion';
import { ease, mix, prog } from '../theme';
import { BOARDS, PHOTOS, ProductShot } from '../light/Product';
import { ResultClip } from '../light/LightAd';

/*
 * Shared pieces of the "premium explainer" variants: one script and timing, the real UI of the
 * Motion Engine mode (brief → storyboards → render) as theme-able panels, captions and the end card.
 * Every variant only decides where the camera is and what the world around the panels looks like.
 */

export const EX_W = 1920;
export const EX_H = 1080;
export const EX_DURATION = 450;

/** Scene boundaries (frames). */
export const TL = { intro: 0, s1: 60, s2: 150, s3: 240, res: 320, end: 390 };

export const PANEL_W = 900;
export const PANEL_H = 640;

export type Theme = {
  dark: boolean;
  panel: string;
  panelBorder: string;
  card: string;
  ink: string;
  muted: string;
  shimmer: string;
  accent: string;
  btn: string;
  btnInk: string;
  pickGlow: string;
};

export const THEMES: Record<'light' | 'glass' | 'night' | 'paper', Theme> = {
  light: {
    dark: false,
    panel: '#f7f7f7',
    panelBorder: 'rgba(255,255,255,0.9)',
    card: '#ffffff',
    ink: '#2b2b2b',
    muted: '#8a8a8a',
    shimmer: '#e9e9e9',
    accent: '#cdf158',
    btn: '#111111',
    btnInk: '#ffffff',
    pickGlow: '#cdf158',
  },
  glass: {
    dark: false,
    panel: 'rgba(255,255,255,0.46)',
    panelBorder: 'rgba(255,255,255,0.85)',
    card: 'rgba(255,255,255,0.62)',
    ink: '#232323',
    muted: '#7d7d7d',
    shimmer: 'rgba(255,255,255,0.5)',
    accent: '#cdf158',
    btn: '#111111',
    btnInk: '#ffffff',
    pickGlow: '#cdf158',
  },
  night: {
    dark: true,
    panel: 'rgba(24,24,27,0.78)',
    panelBorder: 'rgba(255,255,255,0.10)',
    card: 'rgba(255,255,255,0.05)',
    ink: '#f4f4f5',
    muted: '#8b8b93',
    shimmer: 'rgba(255,255,255,0.06)',
    accent: '#cdf158',
    btn: '#cdf158',
    btnInk: '#111111',
    pickGlow: '#cdf158',
  },
  paper: {
    dark: false,
    panel: '#fbfbf9',
    panelBorder: '#d9d9d4',
    card: '#f1f1ee',
    ink: '#1f1f1f',
    muted: '#86867f',
    shimmer: '#e8e8e4',
    accent: '#cdf158',
    btn: '#111111',
    btnInk: '#ffffff',
    pickGlow: '#cdf158',
  },
};

export const COPY = {
  ru: {
    tag: 'Motion Engine',
    h1: 'Ролик из ваших фото',
    h2: 'за пару минут',
    steps: [
      ['Загрузите фото', 'и опишите задачу'],
      ['Получите раскадровки', 'и выберите лучшую'],
      ['Отправьте в рендер', 'и скачайте MP4'],
    ],
    resultTitle: 'Готовый ролик',
    panel: 'Motion Engine',
    tabs: ['Бриф', 'Раскадровки', 'Рендер'],
    photos: 'Фото товара',
    brief: 'Задача',
    briefText: 'Летний запуск сыворотки GLOW — свежо, ярко, с акцентом на продукт',
    make: 'Сделать раскадровку',
    variants: ['Вариант A', 'Вариант B', 'Вариант C'],
    picked: 'Выбрано',
    toRender: 'В рендер',
    rendering: 'Рендер',
    done: 'Готово',
    download: 'Скачать MP4',
    clip1: 'Сияние',
    clip2: 'лета',
    clipTag: 'новинка',
    cta: 'Попробовать Motion Engine',
    notes: [
      ['фото товара', 'задача своими словами'],
      ['несколько вариантов', 'выбор в один клик'],
      ['прогресс рендера', 'готовый MP4'],
    ],
  },
  en: {
    tag: 'Motion Engine',
    h1: 'A video from your photos',
    h2: 'in minutes',
    steps: [
      ['Upload photos', 'and describe the task'],
      ['Get storyboards', 'and pick the best'],
      ['Send it to render', 'and download the MP4'],
    ],
    resultTitle: 'The finished video',
    panel: 'Motion Engine',
    tabs: ['Brief', 'Storyboards', 'Render'],
    photos: 'Product photos',
    brief: 'Task',
    briefText: 'Summer launch of GLOW serum — fresh, bright, product in focus',
    make: 'Make storyboard',
    variants: ['Variant A', 'Variant B', 'Variant C'],
    picked: 'Selected',
    toRender: 'To render',
    rendering: 'Rendering',
    done: 'Done',
    download: 'Download MP4',
    clip1: 'Summer',
    clip2: 'glow',
    clipTag: 'new',
    cta: 'Try Motion Engine',
    notes: [
      ['product photos', 'the task in your words'],
      ['several variants', 'pick in one click'],
      ['render progress', 'the finished MP4'],
    ],
  },
};
export type Copy = (typeof COPY)['ru'];

export const LOGO =
  'M17 4.4C18.66 4.4 20 5.74 20 7.4V18.4C20 19.5 20.9 20.4 22 20.4H32C33.66 20.4 35 21.74 35 23.4V34.4C35 35.5 35.9 36.4 37 36.4H38C39.1 36.4 40 35.5 40 34.4V23.4C40 21.74 41.34 20.4 43 20.4H57C58.66 20.4 60 21.74 60 23.4V34.4C60 35.5 60.9 36.4 62 36.4H73C74.66 36.4 76 37.74 76 39.4V53.4C76 55.06 74.66 56.4 73 56.4H59C57.34 56.4 56 55.06 56 53.4V42.4C56 41.3 55.1 40.4 54 40.4H51C49.9 40.4 49 41.3 49 42.4V53.4C49 55.06 47.66 56.4 46 56.4H32C30.34 56.4 29 55.06 29 53.4V42.4C29 41.3 28.1 40.4 27 40.4H24C22.9 40.4 22 41.3 22 42.4V53.4C22 55.06 20.66 56.4 19 56.4H5C3.34 56.4 2 55.06 2 53.4V39.4C2 37.74 3.34 36.4 5 36.4H13C14.1 36.4 15 35.5 15 34.4V26.4C15 25.3 14.1 24.4 13 24.4H3C1.34 24.4 0 23.06 0 21.4V7.4C0 5.74 1.34 4.4 3 4.4H17Z';

export const Logo: React.FC<{ size: number; bg?: string; fg?: string }> = ({ size, bg = '#111', fg = '#fff' }) => (
  <svg width={size} height={size} viewBox="0 0 96 96">
    <rect width="96" height="96" rx="22" fill={bg} />
    <g transform="translate(10 13.2)">
      <path d={LOGO} fill={fg} />
    </g>
  </svg>
);

// ---- small pieces ----------------------------------------------------------------------------------

export const Rise: React.FC<{ p: number; out?: number; children: ReactNode; style?: CSSProperties }> = ({ p, out = 0, children, style }) => (
  <div style={{ overflow: 'hidden', padding: '0.08em 0 0.14em', margin: '-0.08em 0 -0.14em', ...style }}>
    <div style={{ transform: `translateY(${out > 0 ? -115 * out : mix(115, 0, p)}%)` }}>{children}</div>
  </div>
);

export const Marker: React.FC<{ p: number; color?: string; children: ReactNode }> = ({ p, color = '#cdf158', children }) => (
  <span style={{ position: 'relative', display: 'inline-block' }}>
    <span
      style={{
        position: 'absolute',
        left: '-0.04em',
        right: '-0.04em',
        bottom: '0.06em',
        height: '0.3em',
        background: color,
        transform: `scaleX(${p})`,
        transformOrigin: 'left',
        borderRadius: 2,
      }}
    />
    <span style={{ position: 'relative' }}>{children}</span>
  </span>
);

export const Cursor: React.FC<{ x: number; y: number; press: number; o: number; dark?: boolean }> = ({ x, y, press, o, dark }) =>
  o <= 0 ? null : (
    <svg
      width={34}
      height={40}
      viewBox="0 0 26 30"
      style={{
        position: 'absolute',
        left: x - 4,
        top: y - 3,
        opacity: o,
        transform: `scale(${1 - press * 0.15})`,
        transformOrigin: '4px 3px',
        filter: 'drop-shadow(0 6px 10px rgba(0,0,0,0.3))',
        zIndex: 5,
      }}
    >
      <path d="M3 2 L3 23 L8.6 17.6 L12.4 26.4 L16.2 24.8 L12.5 16.2 L20.4 16.2 Z" fill={dark ? '#fff' : '#111'} stroke={dark ? '#111' : '#fff'} strokeWidth="1.5" strokeLinejoin="round" />
    </svg>
  );

const pressAt = (t: number, at: number) => (t < at ? 0 : t < at + 3 ? prog(t, at, at + 3) : 1 - prog(t, at + 3, at + 10));

const Ripple: React.FC<{ x: number; y: number; p: number; color: string }> = ({ x, y, p, color }) =>
  p <= 0 || p >= 1 ? null : (
    <div
      style={{
        position: 'absolute',
        left: x - 50,
        top: y - 50,
        width: 100,
        height: 100,
        borderRadius: 999,
        border: `3px solid ${color}`,
        opacity: 1 - p,
        transform: `scale(${mix(0.3, 1.5, p)})`,
        zIndex: 4,
      }}
    />
  );

const Pill: React.FC<{ T: Theme; children: ReactNode; style?: CSSProperties }> = ({ T, children, style }) => (
  <div
    style={{
      display: 'inline-flex',
      alignItems: 'center',
      gap: 10,
      height: 52,
      padding: '0 26px',
      borderRadius: 999,
      background: T.btn,
      color: T.btnInk,
      fontSize: 19,
      fontWeight: 500,
      whiteSpace: 'nowrap',
      ...style,
    }}
  >
    {children}
  </div>
);

const Shimmer: React.FC<{ t: number; T: Theme }> = ({ t, T }) => (
  <div style={{ position: 'absolute', inset: 0, background: T.shimmer, overflow: 'hidden' }}>
    <div
      style={{
        position: 'absolute',
        top: 0,
        bottom: 0,
        width: '60%',
        left: `${((t * 4) % 220) - 60}%`,
        background: `linear-gradient(90deg, transparent, ${T.dark ? 'rgba(255,255,255,0.12)' : 'rgba(255,255,255,0.8)'}, transparent)`,
      }}
    />
  </div>
);

/** Panel chrome: header with the mode name and the three tabs; the active one is highlighted. */
const Chrome: React.FC<{ T: Theme; c: Copy; tab: number; children: ReactNode }> = ({ T, c, tab, children }) => (
  <div
    style={{
      position: 'absolute',
      inset: 0,
      borderRadius: 34,
      background: T.panel,
      boxShadow: `inset 0 0 0 1px ${T.panelBorder}`,
      overflow: 'hidden',
      color: T.ink,
    }}
  >
    <div style={{ position: 'absolute', left: 34, right: 34, top: 26, display: 'flex', alignItems: 'center', gap: 12 }}>
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke={T.ink} strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
        <rect x="3" y="6" width="13" height="12" rx="2" />
        <path d="m16 10 5-3v10l-5-3" />
      </svg>
      <div style={{ fontSize: 22, fontWeight: 500 }}>{c.panel}</div>
      <div style={{ marginLeft: 'auto', display: 'flex', gap: 6 }}>
        {c.tabs.map((s, i) => (
          <div
            key={s}
            style={{
              padding: '6px 14px',
              borderRadius: 99,
              fontSize: 15,
              fontWeight: 500,
              background: i === tab ? T.accent : 'transparent',
              color: i === tab ? '#111' : T.muted,
            }}
          >
            {s}
          </div>
        ))}
      </div>
    </div>
    {children}
  </div>
);

// ---- the three panels (t = frames since the step started) -------------------------------------------

export const BriefPanel: React.FC<{ t: number; T: Theme; c: Copy; cursor?: boolean }> = ({ t, T, c, cursor = true }) => {
  const typed = Math.floor(interpolate(t, [24, 56], [0, c.briefText.length], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }));
  const press = pressAt(t, 66);
  const btn = { x: PANEL_W - 34 - 120, y: PANEL_H - 34 - 26 };
  const cm = prog(t, 46, 64, ease.inOut);
  return (
    <Chrome T={T} c={c} tab={0}>
      <div style={{ position: 'absolute', left: 34, top: 92, right: 34 }}>
        <div style={{ fontSize: 16, color: T.muted, marginBottom: 12 }}>{c.photos}</div>
        <div style={{ display: 'flex', gap: 20 }}>
          {PHOTOS.map((p, i) => {
            const d = spring({ frame: t - 2 - i * 6, fps: 30, config: { damping: 14, stiffness: 130 } });
            return (
              <div key={i} style={{ width: 264, height: 214, borderRadius: 20, overflow: 'hidden', opacity: Math.min(1, d * 1.5), transform: `translateY(${mix(-90, 0, d)}px) scale(${mix(0.9, 1, d)})` }}>
                <ProductShot shot={p} w={264} h={214} id={`bp${i}`} />
              </div>
            );
          })}
        </div>
        <div style={{ fontSize: 16, color: T.muted, margin: '26px 0 12px' }}>{c.brief}</div>
        <div style={{ height: 104, borderRadius: 18, background: T.card, padding: '18px 22px', fontSize: 23, lineHeight: 1.4, opacity: prog(t, 16, 26) }}>
          {c.briefText.slice(0, typed)}
          <span style={{ display: 'inline-block', width: 2, height: 26, marginLeft: 2, verticalAlign: '-5px', background: T.ink, opacity: t < 58 || Math.floor(t / 8) % 2 ? 1 : 0 }} />
        </div>
      </div>
      <div style={{ position: 'absolute', right: 34, bottom: 34, opacity: prog(t, 22, 32), transform: `scale(${1 - press * 0.06})` }}>
        <Pill T={T}>
          {c.make} <span>→</span>
        </Pill>
      </div>
      <Ripple x={btn.x} y={btn.y} p={prog(t, 68, 86)} color={T.accent} />
      {cursor && <Cursor x={mix(PANEL_W + 40, btn.x + 10, cm)} y={mix(PANEL_H + 60, btn.y + 6, cm)} press={press} o={prog(t, 44, 50) * (1 - prog(t, 82, 88))} dark={T.dark} />}
    </Chrome>
  );
};

export const BoardsPanel: React.FC<{ t: number; T: Theme; c: Copy; cursor?: boolean }> = ({ t, T, c, cursor = true }) => {
  const pick = prog(t, 64, 74, ease.out);
  const press = pressAt(t, 62);
  const target = { x: PANEL_W - 120, y: 92 + 172 + 90 };
  const cm = prog(t, 44, 62, ease.inOut);
  return (
    <Chrome T={T} c={c} tab={1}>
      <div style={{ position: 'absolute', left: 34, top: 88, right: 34 }}>
        {BOARDS.map((b, r) => {
          const isB = r === 1;
          return (
            <div
              key={b.name}
              style={{
                marginBottom: 14,
                padding: '12px 14px 14px',
                borderRadius: 20,
                background: T.card,
                opacity: isB ? 1 : mix(1, 0.4, pick),
                boxShadow: isB ? `0 0 0 ${3 * pick}px ${T.pickGlow}, 0 0 ${36 * pick}px ${T.pickGlow}` : 'none',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', fontSize: 17, fontWeight: 500, marginBottom: 10 }}>
                {c.variants[r]}
                {isB && pick > 0 && <span style={{ marginLeft: 'auto', padding: '3px 12px', borderRadius: 99, background: T.accent, color: '#111', fontSize: 15, opacity: pick }}>✓ {c.picked}</span>}
              </div>
              <div style={{ display: 'flex', gap: 12 }}>
                {b.shots.map((s, i) => {
                  const at = 8 + r * 10 + i * 4;
                  return (
                    <div key={i} style={{ position: 'relative', width: 195, height: 110, borderRadius: 12, overflow: 'hidden', opacity: prog(t, at - 8, at - 2), transform: `scale(${mix(0.94, 1, prog(t, at - 8, at))})` }}>
                      <Shimmer t={t} T={T} />
                      <div style={{ position: 'absolute', inset: 0, opacity: prog(t, at, at + 8) }}>
                        <ProductShot shot={s} w={195} h={110} id={`bb${r}${i}`} />
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>
      <Ripple x={target.x} y={target.y} p={prog(t, 63, 80)} color={T.accent} />
      {cursor && <Cursor x={mix(PANEL_W * 0.5, target.x, cm)} y={mix(PANEL_H + 60, target.y, cm)} press={press} o={prog(t, 40, 46) * (1 - prog(t, 80, 86))} dark={T.dark} />}
    </Chrome>
  );
};

export const RenderPanel: React.FC<{ t: number; T: Theme; c: Copy; cursor?: boolean }> = ({ t, T, c, cursor = true }) => {
  const press = pressAt(t, 10);
  const p = prog(t, 16, 60, ease.soft);
  const done = prog(t, 60, 68, ease.out);
  const btn = { x: PANEL_W - 34 - 80, y: 92 + 30 };
  const cm = prog(t, 0, 10, ease.inOut);
  return (
    <Chrome T={T} c={c} tab={2}>
      <div style={{ position: 'absolute', left: 34, top: 92, right: 34 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 18 }}>
          {BOARDS[1].shots.map((s, i) => {
            const k = prog(t, i * 2, 10 + i * 2, ease.out);
            return (
              <div key={i} style={{ borderRadius: 8, overflow: 'hidden', opacity: k, transform: `translateY(${mix(40, 0, k)}px)` }}>
                <ProductShot shot={s} w={108} h={60.75} id={`rp${i}`} />
              </div>
            );
          })}
          <div style={{ marginLeft: 'auto', transform: `scale(${1 - press * 0.06})` }}>
            <Pill T={T} style={done > 0 ? { background: T.accent, color: '#111' } : undefined}>
              {done > 0 ? `↓ ${c.download}` : c.toRender}
            </Pill>
          </div>
        </div>
        <div style={{ position: 'relative', width: 832, height: 380, borderRadius: 20, overflow: 'hidden', background: T.shimmer }}>
          <div style={{ position: 'absolute', inset: 0, clipPath: `inset(0 ${(1 - p) * 100}% 0 0)` }}>
            <ResultClip t={44} w={832} h={380} c={c} />
          </div>
          <div style={{ position: 'absolute', top: 0, bottom: 0, left: `${p * 100}%`, width: 4, background: T.accent, opacity: p > 0 && p < 1 ? 1 : 0, boxShadow: `0 0 26px ${T.accent}` }} />
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 16, marginTop: 20, fontSize: 19 }}>
          <span style={{ fontWeight: 500, width: 110 }}>{done > 0 ? `✓ ${c.done}` : c.rendering}</span>
          <div style={{ flex: 1, height: 8, borderRadius: 99, background: T.shimmer, overflow: 'hidden' }}>
            <div style={{ width: `${p * 100}%`, height: '100%', background: T.dark ? T.accent : T.ink }} />
          </div>
          <span style={{ color: T.muted, width: 60, textAlign: 'right', fontVariantNumeric: 'tabular-nums' }}>{Math.round(p * 100)}%</span>
        </div>
      </div>
      <Ripple x={btn.x} y={btn.y} p={prog(t, 11, 28)} color={T.accent} />
      {cursor && <Cursor x={mix(PANEL_W - 300, btn.x, cm)} y={mix(PANEL_H - 100, btn.y + 4, cm)} press={press} o={prog(t, 0, 4) * (1 - prog(t, 24, 30))} dark={T.dark} />}
    </Chrome>
  );
};

/** The panel for the current step, given the global frame. */
export const ActivePanel: React.FC<{ f: number; step: number; T: Theme; c: Copy; cursor?: boolean }> = ({ f, step, T, c, cursor }) =>
  step === 0 ? (
    <BriefPanel t={f - TL.s1} T={T} c={c} cursor={cursor} />
  ) : step === 1 ? (
    <BoardsPanel t={f - TL.s2} T={T} c={c} cursor={cursor} />
  ) : (
    <RenderPanel t={f - TL.s3} T={T} c={c} cursor={cursor} />
  );

export { ResultClip };

// ---- copy blocks --------------------------------------------------------------------------------------

/** Step caption: "01" + two lines; rises in after the step starts and leaves just before the next. */
export const StepCaption: React.FC<{ f: number; c: Copy; color: string; muted: string; x: number; y: number; size?: number; num?: boolean }> = ({
  f,
  c,
  color,
  muted,
  x,
  y,
  size = 68,
  num = true,
}) => {
  const starts = [TL.s1, TL.s2, TL.s3];
  const ends = [TL.s2, TL.s3, TL.res];
  return (
    <>
      {starts.map((a, i) => {
        if (f < a || f >= ends[i]) return null;
        const p = prog(f, a + 4, a + 24);
        const out = prog(f, ends[i] - 12, ends[i] - 2, ease.inOut);
        return (
          <div key={i} style={{ position: 'absolute', left: x, top: y, color }}>
            {num && (
              <Rise p={p} out={out}>
                <div style={{ fontSize: 22, color: muted, letterSpacing: '0.08em', marginBottom: 16 }}>0{i + 1} / 03</div>
              </Rise>
            )}
            {c.steps[i].map((l, k) => (
              <Rise key={l} p={prog(f, a + 6 + k * 4, a + 26 + k * 4)} out={out}>
                <div style={{ fontSize: size, fontWeight: 200, lineHeight: 1.12, letterSpacing: '-0.035em', whiteSpace: 'nowrap' }}>{l}</div>
              </Rise>
            ))}
          </div>
        );
      })}
    </>
  );
};

export const IntroTitle: React.FC<{ f: number; c: Copy; color: string; x?: number; y: number; align?: 'center' | 'left'; size?: number; marker?: string }> = ({
  f,
  c,
  color,
  x = 0,
  y,
  align = 'center',
  size = 128,
  marker = '#cdf158',
}) => {
  if (f >= TL.s1 + 8) return null;
  const out = prog(f, TL.s1 - 10, TL.s1 + 4, ease.inOut);
  return (
    <div style={{ position: 'absolute', left: align === 'center' ? 0 : x, right: align === 'center' ? 0 : undefined, top: y, textAlign: align, color }}>
      <Rise p={prog(f, 0, 14)} out={out}>
        <div style={{ fontSize: 24, letterSpacing: '0.12em', textTransform: 'uppercase', opacity: 0.6, marginBottom: 22 }}>{c.tag}</div>
      </Rise>
      <div style={{ fontSize: size, fontWeight: 200, lineHeight: 1.06, letterSpacing: '-0.045em' }}>
        <Rise p={prog(f, 2, 22)} out={out}>
          {c.h1}
        </Rise>
        <Rise p={prog(f, 8, 28)} out={out}>
          <Marker p={prog(f, 24, 42, ease.inOut)} color={marker}>
            {c.h2}
          </Marker>
        </Rise>
      </div>
    </div>
  );
};

export const EndCopy: React.FC<{ f: number; c: Copy; T: Theme; x: number; y: number; size?: number }> = ({ f, c, T, x, y, size = 92 }) => {
  if (f < TL.end) return null;
  const t = f - TL.end;
  const e = [prog(t, 2, 14), prog(t, 6, 18), prog(t, 10, 22), prog(t, 14, 26)];
  return (
    <div style={{ position: 'absolute', left: x, top: y, color: T.ink }}>
      <Rise p={e[0]}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
          <Logo size={60} bg={T.dark ? '#fff' : '#111'} fg={T.dark ? '#111' : '#fff'} />
          <span style={{ fontSize: 34, fontWeight: 600, letterSpacing: '-0.02em' }}>ONEFLOW</span>
          <span style={{ fontSize: 34, fontWeight: 300, color: T.muted }}>Motion Engine</span>
        </div>
      </Rise>
      <div style={{ marginTop: 34, fontSize: size, fontWeight: 200, lineHeight: 1.08, letterSpacing: '-0.045em', whiteSpace: 'nowrap' }}>
        <Rise p={e[1]}>{c.h1}</Rise>
        <Rise p={e[2]}>
          <Marker p={prog(t, 20, 34, ease.inOut)} color={T.dark ? 'rgba(205,241,88,0.45)' : T.accent}>
            {c.h2}
          </Marker>
        </Rise>
      </div>
      <Rise p={e[3]} style={{ marginTop: 40 }}>
        <Pill T={T} style={{ height: 70, fontSize: 26, padding: '0 34px' }}>
          {c.cta} <span>→</span>
        </Pill>
      </Rise>
    </div>
  );
};

/** Which step is on screen (0..2), or -1 before / 3 after. */
export const stepAt = (f: number) => (f < TL.s1 ? -1 : f < TL.s2 ? 0 : f < TL.s3 ? 1 : f < TL.res ? 2 : 3);
