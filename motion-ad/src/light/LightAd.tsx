import type { CSSProperties, ReactNode } from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame } from 'remotion';
import '../fonts';
import { FONT } from '../fonts';
import { ease, mix, mixRect, prog } from '../theme';
import type { Rect } from '../theme';
import { BOARDS, PHOTOS, ProductShot } from './Product';
import type { Shot } from './Product';

/*
 * ONEFLOW Motion Engine — light explainer, 1920×1080, 30 fps, 15 s, silent.
 * Colours and type follow the app's light theme: grey page, light cards, ink #2b2b2b,
 * lime accent, black pill buttons, thin Geist headings.
 *
 *   0– 70  «Ролик из ваших фото — за пару минут»
 *  70–160  step 1: photos drop in, the brief is typed, click «Сделать раскадровку»
 * 160–255  step 2: three storyboards are generated, the best one is picked
 * 255–330  step 3: «В рендер» → progress → MP4 ready
 * 330–390  the rendered clip opens full size
 * 390–450  end card; copy is still for the last 1.5 s
 */

export const LIGHT_W = 1920;
export const LIGHT_H = 1080;
export const LIGHT_DURATION = 450;

const K = {
  page: '#e5e5e5',
  card: '#f7f7f7',
  card2: '#efefef',
  ink: '#2b2b2b',
  muted: '#8a8a8a',
  faint: '#b9b9b9',
  lime: '#cdf158',
  limeDeep: '#9cc21c',
  black: '#111111',
};

const COPY = {
  ru: {
    tag: 'Новое · Motion Engine',
    h1: 'Ролик из ваших фото',
    h2: 'за пару минут',
    steps: ['Фото и бриф', 'Раскадровки', 'Рендер'],
    s1: ['Загрузите фото', 'и опишите задачу'],
    s2: ['ONEFLOW предложит', 'раскадровки'],
    s2b: 'Выберите лучшую',
    s3: ['Отправьте', 'в рендер'],
    s3b: 'и скачайте MP4',
    step: 'Шаг',
    panel: 'Motion Engine',
    photos: 'Фото товара',
    brief: 'Задача',
    briefText: 'Летний запуск сыворотки GLOW — свежо, ярко, с акцентом на продукт',
    make: 'Сделать раскадровку',
    boards: 'Раскадровки',
    variants: ['Вариант A', 'Вариант B', 'Вариант C'],
    picked: 'Выбрано',
    toRender: 'В рендер',
    rendering: 'Рендер',
    done: 'Готово',
    download: 'Скачать MP4',
    result: 'Готовый ролик',
    clip1: 'Сияние',
    clip2: 'лета',
    clipTag: 'новинка',
    cta: 'Попробовать Motion Engine',
  },
  en: {
    tag: 'New · Motion Engine',
    h1: 'A video from your photos',
    h2: 'in minutes',
    steps: ['Photos & brief', 'Storyboards', 'Render'],
    s1: ['Upload photos', 'and describe the task'],
    s2: ['ONEFLOW proposes', 'storyboards'],
    s2b: 'Pick the best one',
    s3: ['Send it', 'to render'],
    s3b: 'and download the MP4',
    step: 'Step',
    panel: 'Motion Engine',
    photos: 'Product photos',
    brief: 'Task',
    briefText: 'Summer launch of GLOW serum — fresh, bright, product in focus',
    make: 'Make storyboard',
    boards: 'Storyboards',
    variants: ['Variant A', 'Variant B', 'Variant C'],
    picked: 'Selected',
    toRender: 'To render',
    rendering: 'Rendering',
    done: 'Done',
    download: 'Download MP4',
    result: 'The finished video',
    clip1: 'Summer',
    clip2: 'glow',
    clipTag: 'new',
    cta: 'Try Motion Engine',
  },
};
type Copy = (typeof COPY)['ru'];

// ---- geometry --------------------------------------------------------------------------------------
const STAGE: Rect = { x: 820, y: 214, w: 960, h: 690, r: 36 };
const PLAYER: Rect = { x: 300, y: 150, w: 1320, h: 742.5, r: 32 };
const FINAL: Rect = { x: 960, y: 300, w: 820, h: 461.25, r: 28 };
const PAD = 40;

const LOGO =
  'M17 4.4C18.66 4.4 20 5.74 20 7.4V18.4C20 19.5 20.9 20.4 22 20.4H32C33.66 20.4 35 21.74 35 23.4V34.4C35 35.5 35.9 36.4 37 36.4H38C39.1 36.4 40 35.5 40 34.4V23.4C40 21.74 41.34 20.4 43 20.4H57C58.66 20.4 60 21.74 60 23.4V34.4C60 35.5 60.9 36.4 62 36.4H73C74.66 36.4 76 37.74 76 39.4V53.4C76 55.06 74.66 56.4 73 56.4H59C57.34 56.4 56 55.06 56 53.4V42.4C56 41.3 55.1 40.4 54 40.4H51C49.9 40.4 49 41.3 49 42.4V53.4C49 55.06 47.66 56.4 46 56.4H32C30.34 56.4 29 55.06 29 53.4V42.4C29 41.3 28.1 40.4 27 40.4H24C22.9 40.4 22 41.3 22 42.4V53.4C22 55.06 20.66 56.4 19 56.4H5C3.34 56.4 2 55.06 2 53.4V39.4C2 37.74 3.34 36.4 5 36.4H13C14.1 36.4 15 35.5 15 34.4V26.4C15 25.3 14.1 24.4 13 24.4H3C1.34 24.4 0 23.06 0 21.4V7.4C0 5.74 1.34 4.4 3 4.4H17Z';

// ---- small building blocks ---------------------------------------------------------------------------

/** Text line rising through its own mask. */
const Rise: React.FC<{ p: number; out?: number; children: ReactNode; style?: CSSProperties }> = ({ p, out = 0, children, style }) => (
  <div style={{ overflow: 'hidden', padding: '0.08em 0 0.14em', margin: '-0.08em 0 -0.14em', ...style }}>
    <div style={{ transform: `translateY(${out > 0 ? -115 * out : mix(115, 0, p)}%)` }}>{children}</div>
  </div>
);

/** Lime marker behind a phrase, swept in from the left — same treatment as the app's greeting. */
const Highlight: React.FC<{ p: number; children: ReactNode }> = ({ p, children }) => (
  <span style={{ position: 'relative', display: 'inline-block' }}>
    <span
      style={{
        position: 'absolute',
        left: '-0.04em',
        right: '-0.04em',
        bottom: '0.06em',
        height: '0.3em',
        background: K.lime,
        transform: `scaleX(${p})`,
        transformOrigin: 'left',
        borderRadius: 2,
      }}
    />
    <span style={{ position: 'relative' }}>{children}</span>
  </span>
);

const Pill: React.FC<{ dark?: boolean; children: ReactNode; style?: CSSProperties }> = ({ dark = true, children, style }) => (
  <div
    style={{
      display: 'inline-flex',
      alignItems: 'center',
      gap: 12,
      height: 60,
      padding: '0 30px',
      borderRadius: 999,
      background: dark ? K.black : '#fff',
      color: dark ? '#fff' : K.ink,
      fontSize: 22,
      fontWeight: 500,
      whiteSpace: 'nowrap',
      ...style,
    }}
  >
    {children}
  </div>
);

const Cursor: React.FC<{ x: number; y: number; press: number; o: number }> = ({ x, y, press, o }) => (
  <svg
    width={36}
    height={42}
    viewBox="0 0 26 30"
    style={{
      position: 'absolute',
      left: x - 4,
      top: y - 3,
      opacity: o,
      transform: `scale(${1 - press * 0.15})`,
      transformOrigin: '4px 3px',
      filter: 'drop-shadow(0 6px 10px rgba(0,0,0,0.25))',
    }}
  >
    <path d="M3 2 L3 23 L8.6 17.6 L12.4 26.4 L16.2 24.8 L12.5 16.2 L20.4 16.2 Z" fill={K.black} stroke="#fff" strokeWidth="1.5" strokeLinejoin="round" />
  </svg>
);

const Ripple: React.FC<{ x: number; y: number; p: number }> = ({ x, y, p }) =>
  p <= 0 || p >= 1 ? null : (
    <div
      style={{
        position: 'absolute',
        left: x - 60,
        top: y - 60,
        width: 120,
        height: 120,
        borderRadius: 999,
        border: `3px solid ${K.lime}`,
        opacity: 1 - p,
        transform: `scale(${mix(0.3, 1.4, p)})`,
      }}
    />
  );

const Shimmer: React.FC<{ f: number }> = ({ f }) => (
  <div style={{ position: 'absolute', inset: 0, background: '#e8e8e8', overflow: 'hidden' }}>
    <div
      style={{
        position: 'absolute',
        top: 0,
        bottom: 0,
        width: '60%',
        left: `${((f * 4) % 220) - 60}%`,
        background: 'linear-gradient(90deg, transparent, rgba(255,255,255,0.75), transparent)',
      }}
    />
  </div>
);

/** A storyboard / photo frame: shimmer while "generating", then the shot fades in. */
const Frame: React.FC<{ shot: Shot; w: number; h: number; id: string; f: number; at: number; r?: number }> = ({ shot, w, h, id, f, at, r = 12 }) => {
  const show = prog(f, at, at + 8);
  const appear = prog(f, at - 10, at - 2);
  return (
    <div style={{ position: 'relative', width: w, height: h, borderRadius: r, overflow: 'hidden', opacity: appear, transform: `scale(${mix(0.94, 1, appear)})` }}>
      <Shimmer f={f} />
      <div style={{ position: 'absolute', inset: 0, opacity: show }}>
        <ProductShot shot={shot} w={w} h={h} id={id} />
      </div>
    </div>
  );
};

/** The rendered ad itself: product, sun, kinetic type. Pure function of local time t. */
export const ResultClip: React.FC<{ t: number; w: number; h: number; c: Pick<Copy, "clip1" | "clip2" | "clipTag"> }> = ({ t, w, h, c }) => {
  const u = h / 742.5;
  const sun = spring({ frame: t - 2, fps: 30, config: { damping: 18, stiffness: 90 } });
  const up = spring({ frame: t - 6, fps: 30, config: { damping: 15, stiffness: 110 } });
  const w1 = prog(t, 14, 30);
  const w2 = prog(t, 20, 36);
  const tag = prog(t, 34, 46);
  const drift = Math.sin(t / 24) * 6 * u;
  return (
    <div style={{ position: 'absolute', inset: 0, overflow: 'hidden', background: 'linear-gradient(180deg, #f4f8e6, #e3edc2)' }}>
      <div
        style={{
          position: 'absolute',
          left: w * 0.62 - 230 * u,
          top: h * 0.46 - 230 * u,
          width: 460 * u,
          height: 460 * u,
          borderRadius: 999,
          background: K.lime,
          transform: `scale(${sun})`,
        }}
      />
      <div style={{ position: 'absolute', left: w * 0.62 - 300 * u, top: h * 0.08 + drift, transform: `translateY(${mix(h * 0.7, 0, up)}px)` }}>
        <ProductShot shot={{ bg: ['rgba(0,0,0,0)', 'rgba(0,0,0,0)'], x: 0.5, y: 0.92, size: 0.84, table: false }} w={600 * u} h={640 * u} id="clip" />
      </div>
      <div style={{ position: 'absolute', left: 90 * u, top: h * 0.28, color: K.ink, fontWeight: 700, fontSize: 150 * u, lineHeight: 0.95, letterSpacing: '-0.05em' }}>
        <Rise p={w1}>{c.clip1}</Rise>
        <Rise p={w2}>{c.clip2}</Rise>
      </div>
      <div
        style={{
          position: 'absolute',
          left: 94 * u,
          top: h * 0.28 + 320 * u,
          opacity: tag,
          transform: `translateY(${mix(20, 0, tag)}px)`,
          padding: `${10 * u}px ${24 * u}px`,
          borderRadius: 999,
          background: K.black,
          color: '#fff',
          fontSize: 28 * u,
          fontWeight: 500,
        }}
      >
        GLOW · {c.clipTag}
      </div>
    </div>
  );
};

// ---- the film ----------------------------------------------------------------------------------------

export const LightAd: React.FC<{ lang?: 'ru' | 'en' }> = ({ lang = 'ru' }) => {
  const f = useCurrentFrame();
  const c = COPY[lang];

  // intro
  const tagIn = prog(f, 0, 14);
  const h1 = prog(f, 2, 24);
  const h2 = prog(f, 8, 30);
  const hl = prog(f, 26, 46, ease.inOut);
  const introOut = prog(f, 60, 76, ease.inOut);

  // stage card: in, steady, → player, → end card
  const stageIn = prog(f, 62, 90, ease.out);
  let stage = { ...STAGE, x: mix(STAGE.x + 220, STAGE.x, stageIn) };
  if (f >= 330) stage = mixRect(STAGE, PLAYER, prog(f, 330, 362, ease.inOut));
  if (f >= 388) stage = mixRect(PLAYER, FINAL, prog(f, 388, 416, ease.inOut));
  const stageOpacity = prog(f, 62, 74);

  // which step is active (stepper + captions)
  const stepIdx = f < 160 ? 0 : f < 255 ? 1 : 2;
  const stepperIn = prog(f, 66, 86) * (1 - prog(f, 326, 340));

  // ---- step 1: photos + brief + click
  const s1Out = prog(f, 160, 172, ease.inOut);
  const typed = Math.floor(interpolate(f, [112, 146], [0, c.briefText.length], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }));
  const press1 = f < 150 ? 0 : f < 153 ? prog(f, 150, 153) : 1 - prog(f, 153, 160);

  // ---- step 2: boards
  const s2In = prog(f, 164, 180, ease.out);
  const s2Out = prog(f, 252, 264, ease.inOut);
  const pick = prog(f, 236, 246, ease.out);
  const press2 = f < 232 ? 0 : f < 235 ? prog(f, 232, 235) : 1 - prog(f, 235, 242);

  // ---- step 3: render
  const s3In = prog(f, 258, 272, ease.out);
  const press3 = f < 268 ? 0 : f < 271 ? prog(f, 268, 271) : 1 - prog(f, 271, 278);
  const renderP = prog(f, 276, 318, ease.soft);
  const doneP = prog(f, 318, 328, ease.out);
  const s3Out = prog(f, 330, 342);

  // ---- result + end
  const clipOn = prog(f, 328, 344);
  const clipT = f - 336;
  const endIn = [prog(f, 392, 410), prog(f, 398, 416), prog(f, 404, 420), prog(f, 410, 426)];
  const endHl = prog(f, 416, 434, ease.inOut);

  // cursor path: brief button → board B → render button
  const btn1 = { x: STAGE.x + STAGE.w - PAD - 150, y: STAGE.y + STAGE.h - PAD - 30 };
  const boardB = { x: STAGE.x + STAGE.w - PAD - 60, y: STAGE.y + 92 + 190 + 66 };
  const btn3 = { x: STAGE.x + STAGE.w - PAD - 90, y: STAGE.y + 92 + 34 };
  const cursorPts: [number, { x: number; y: number }][] = [
    [120, { x: 1700, y: 1010 }],
    [148, btn1],
    [208, btn1],
    [230, boardB],
    [250, boardB],
    [266, btn3],
    [290, { x: btn3.x + 40, y: btn3.y + 60 }],
  ];
  const cur = (() => {
    for (let i = 1; i < cursorPts.length; i++) {
      const [f1, p1] = cursorPts[i];
      const [f0, p0] = cursorPts[i - 1];
      if (f <= f1) {
        const t = prog(f, f0, f1, ease.inOut);
        return { x: mix(p0.x, p1.x, t), y: mix(p0.y, p1.y, t) };
      }
    }
    return cursorPts[cursorPts.length - 1][1];
  })();
  const curO = prog(f, 120, 130) * (1 - prog(f, 284, 296));

  const caption = (lines: string[], p: number, out: number, sub?: { text: string; p: number }) => (
    <div style={{ position: 'absolute', left: 140, top: 380, width: 670 }}>
      <Rise p={p} out={out}>
        <div style={{ fontSize: 24, color: K.muted, marginBottom: 18 }}>
          {c.step} {stepIdx + 1} / 3
        </div>
      </Rise>
      {lines.map((l, i) => (
        <Rise key={l} p={prog(p * 20, i * 3, 14 + i * 3)} out={out}>
          <div style={{ fontSize: 68, fontWeight: 200, lineHeight: 1.12, letterSpacing: '-0.035em', color: K.ink, whiteSpace: 'nowrap' }}>{l}</div>
        </Rise>
      ))}
      {sub && (
        <Rise p={sub.p} out={out} style={{ marginTop: 26 }}>
          <div style={{ fontSize: 34, fontWeight: 400, color: K.ink, whiteSpace: 'nowrap' }}>
            <Highlight p={sub.p}>{sub.text}</Highlight>
          </div>
        </Rise>
      )}
    </div>
  );

  return (
    <AbsoluteFill style={{ background: K.page, fontFamily: FONT, color: K.ink, overflow: 'hidden' }}>
      {/* soft light from the top */}
      <div style={{ position: 'absolute', left: 300, top: -500, width: 1400, height: 900, borderRadius: '50%', background: 'radial-gradient(closest-side, rgba(255,255,255,0.7), transparent)' }} />

      {/* ============ intro ============ */}
      {f < 80 && (
        <div style={{ position: 'absolute', left: 0, right: 0, top: 330, textAlign: 'center', opacity: 1 - introOut, transform: `translateY(${-60 * introOut}px)` }}>
          <div
            style={{
              display: 'inline-block',
              padding: '10px 22px',
              borderRadius: 999,
              background: 'linear-gradient(165deg, #62802a, #405618)',
              color: '#f4fbe0',
              fontSize: 22,
              fontWeight: 600,
              opacity: tagIn,
              transform: `translateY(${mix(14, 0, tagIn)}px)`,
              boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.25)',
            }}
          >
            {c.tag}
          </div>
          <div style={{ marginTop: 34, fontSize: 132, fontWeight: 200, lineHeight: 1.08, letterSpacing: '-0.045em' }}>
            <Rise p={h1}>{c.h1}</Rise>
            <Rise p={h2}>
              <Highlight p={hl}>{c.h2}</Highlight>
            </Rise>
          </div>
        </div>
      )}

      {/* ============ stepper ============ */}
      <div style={{ position: 'absolute', left: 0, right: 0, top: 70, display: 'flex', justifyContent: 'center', opacity: stepperIn, transform: `translateY(${mix(-20, 0, stepperIn)}px)` }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 18 }}>
          {c.steps.map((s, i) => {
            const active = i === stepIdx;
            const done = i < stepIdx;
            return (
              <div key={s} style={{ display: 'flex', alignItems: 'center', gap: 18 }}>
                {i > 0 && <div style={{ width: 70, height: 2, borderRadius: 2, background: done || active ? K.ink : K.faint }} />}
                <div
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: 12,
                    height: 56,
                    padding: '0 24px 0 10px',
                    borderRadius: 999,
                    background: active ? K.black : K.card,
                    color: active ? '#fff' : done ? K.ink : K.muted,
                    fontSize: 22,
                    fontWeight: 500,
                  }}
                >
                  <div
                    style={{
                      width: 36,
                      height: 36,
                      borderRadius: 999,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      background: done ? K.lime : active ? K.lime : K.card2,
                      color: K.ink,
                      fontSize: 18,
                      fontWeight: 600,
                    }}
                  >
                    {done ? '✓' : i + 1}
                  </div>
                  {s}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* ============ captions ============ */}
      {f >= 70 && f < 172 && caption(c.s1, prog(f, 76, 98), prog(f, 158, 170, ease.inOut))}
      {f >= 160 && f < 266 && caption(c.s2, prog(f, 166, 188), prog(f, 252, 264, ease.inOut), { text: c.s2b, p: prog(f, 226, 240) })}
      {f >= 255 && f < 344 && caption(c.s3, prog(f, 260, 282), prog(f, 328, 340, ease.inOut), { text: c.s3b, p: prog(f, 318, 330) })}

      {/* ============ stage card ============ */}
      <div
        style={{
          position: 'absolute',
          left: stage.x,
          top: stage.y,
          width: stage.w,
          height: stage.h,
          borderRadius: stage.r,
          background: K.card,
          opacity: stageOpacity,
          overflow: 'hidden',
          boxShadow: '0 40px 80px -40px rgba(0,0,0,0.25), 0 2px 0 rgba(255,255,255,0.8) inset',
        }}
      >
        {/* panel header */}
        <div style={{ position: 'absolute', left: PAD, top: 30, right: PAD, display: 'flex', alignItems: 'center', gap: 14, opacity: 1 - s3Out }}>
          <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke={K.ink} strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
            <rect x="3" y="6" width="13" height="12" rx="2" />
            <path d="m16 10 5-3v10l-5-3" />
          </svg>
          <div style={{ fontSize: 26, fontWeight: 500 }}>{c.panel}</div>
          <div style={{ marginLeft: 'auto', fontSize: 20, color: K.muted }}>{stepIdx === 0 ? c.brief : stepIdx === 1 ? c.boards : c.rendering}</div>
        </div>

        {/* step 1 */}
        {f < 176 && (
          <div style={{ position: 'absolute', left: PAD, top: 92, right: PAD, opacity: 1 - s1Out, transform: `translateX(${-60 * s1Out}px)` }}>
            <div style={{ fontSize: 20, color: K.muted, marginBottom: 14 }}>{c.photos}</div>
            <div style={{ display: 'flex', gap: 22 }}>
              {PHOTOS.map((p, i) => {
                const d = spring({ frame: f - (86 + i * 7), fps: 30, config: { damping: 14, stiffness: 130 } });
                return (
                  <div key={i} style={{ width: 280, height: 250, borderRadius: 22, overflow: 'hidden', opacity: Math.min(1, d * 1.5), transform: `translateY(${mix(-120, 0, d)}px)` }}>
                    <ProductShot shot={p} w={280} h={250} id={`ph${i}`} />
                  </div>
                );
              })}
            </div>
            <div style={{ fontSize: 20, color: K.muted, margin: '30px 0 14px' }}>{c.brief}</div>
            <div style={{ height: 116, borderRadius: 20, background: '#fff', padding: '22px 26px', fontSize: 27, lineHeight: 1.4, color: K.ink, opacity: prog(f, 100, 112) }}>
              {c.briefText.slice(0, typed)}
              <span style={{ display: 'inline-block', width: 3, height: 30, marginLeft: 2, verticalAlign: '-5px', background: K.ink, opacity: f < 148 || Math.floor(f / 8) % 2 ? 1 : 0 }} />
            </div>
          </div>
        )}
        {f < 176 && (
          <div style={{ position: 'absolute', right: PAD, bottom: PAD, opacity: prog(f, 108, 118) * (1 - s1Out), transform: `scale(${1 - press1 * 0.06})` }}>
            <Pill>
              {c.make}
              <span style={{ fontSize: 24 }}>→</span>
            </Pill>
          </div>
        )}

        {/* step 2 */}
        {f >= 160 && f < 266 && (
          <div style={{ position: 'absolute', left: PAD, top: 92, right: PAD, opacity: s2In * (1 - s2Out), transform: `translateX(${mix(60, 0, s2In) - 60 * s2Out}px)` }}>
            {BOARDS.map((b, r) => {
              const isB = r === 1;
              const dim = isB ? 1 : mix(1, 0.45, pick);
              return (
                <div
                  key={b.name}
                  style={{
                    position: 'relative',
                    marginBottom: 18,
                    padding: '14px 16px 16px',
                    borderRadius: 22,
                    background: '#fff',
                    opacity: dim,
                    boxShadow: isB ? `0 0 0 ${3 * pick}px ${K.lime}, 0 0 ${40 * pick}px ${K.lime}` : 'none',
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: 12, fontSize: 20, fontWeight: 500, marginBottom: 12 }}>
                    {c.variants[r]}
                    {isB && pick > 0 && (
                      <span style={{ marginLeft: 'auto', padding: '4px 14px', borderRadius: 999, background: K.lime, fontSize: 18, opacity: pick }}>✓ {c.picked}</span>
                    )}
                  </div>
                  <div style={{ display: 'flex', gap: 12 }}>
                    {b.shots.map((s, i) => (
                      <Frame key={i} shot={s} w={202} h={113.6} id={`b${r}${i}`} f={f} at={182 + r * 12 + i * 5} />
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {/* step 3 */}
        {f >= 255 && (
          <div style={{ position: 'absolute', left: PAD, top: 92, right: PAD, opacity: s3In * (1 - s3Out) }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 16, marginBottom: 20 }}>
              <div style={{ display: 'flex', gap: 8 }}>
                {BOARDS[1].shots.map((s, i) => {
                  const k = prog(f, 258 + i * 3, 270 + i * 3, ease.out);
                  return (
                    <div key={i} style={{ borderRadius: 8, overflow: 'hidden', transform: `translateY(${mix(140, 0, k)}px)`, opacity: k }}>
                      <ProductShot shot={s} w={120} h={67.5} id={`r${i}`} />
                    </div>
                  );
                })}
              </div>
              <div style={{ marginLeft: 'auto', transform: `scale(${1 - press3 * 0.06})` }}>
                <Pill style={{ height: 54, fontSize: 20, background: doneP > 0 ? K.lime : K.black, color: doneP > 0 ? K.ink : '#fff' }}>
                  {doneP > 0 ? `↓ ${c.download}` : c.toRender}
                </Pill>
              </div>
            </div>
            {/* preview being rendered */}
            <div style={{ position: 'relative', width: 880, height: 400, borderRadius: 22, overflow: 'hidden', background: '#e8e8e8' }}>
              <div style={{ position: 'absolute', inset: 0, clipPath: `inset(0 ${(1 - renderP) * 100}% 0 0)` }}>
                <ResultClip t={44} w={880} h={400} c={c} />
              </div>
              <div style={{ position: 'absolute', top: 0, bottom: 0, left: `${renderP * 100}%`, width: 4, background: K.lime, opacity: renderP > 0 && renderP < 1 ? 1 : 0, boxShadow: `0 0 24px ${K.lime}` }} />
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 18, marginTop: 22, fontSize: 22 }}>
              <span style={{ fontWeight: 500 }}>{doneP > 0 ? `✓ ${c.done}` : c.rendering}</span>
              <div style={{ flex: 1, height: 10, borderRadius: 99, background: '#e2e2e2', overflow: 'hidden' }}>
                <div style={{ width: `${renderP * 100}%`, height: '100%', background: K.ink }} />
              </div>
              <span style={{ fontVariantNumeric: 'tabular-nums', color: K.muted, width: 70, textAlign: 'right' }}>{Math.round(renderP * 100)}%</span>
            </div>
          </div>
        )}

        {/* the finished clip fills the card */}
        {f >= 328 && (
          <div style={{ position: 'absolute', inset: 0, opacity: clipOn }}>
            <ResultClip t={clipT} w={stage.w} h={stage.h} c={c} />
          </div>
        )}
      </div>

      {/* label over the player */}
      {f >= 340 && f < 400 && (
        <div style={{ position: 'absolute', left: PLAYER.x, top: PLAYER.y - 62, fontSize: 26, color: K.muted, opacity: prog(f, 346, 358) * (1 - prog(f, 386, 396)) }}>
          ▶ {c.result}
        </div>
      )}

      {/* ============ end card ============ */}
      {f >= 388 && (
        <div style={{ position: 'absolute', left: 140, top: 330 }}>
          <Rise p={endIn[0]}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 18 }}>
              <svg width="64" height="64" viewBox="0 0 96 96">
                <rect width="96" height="96" rx="22" fill={K.black} />
                <g transform="translate(10 13.2)">
                  <path d={LOGO} fill="#fff" />
                </g>
              </svg>
              <div style={{ fontSize: 34, fontWeight: 600, letterSpacing: '-0.02em' }}>ONEFLOW</div>
              <div style={{ fontSize: 34, fontWeight: 300, color: K.muted }}>Motion Engine</div>
            </div>
          </Rise>
          <div style={{ marginTop: 34, fontSize: 84, fontWeight: 200, lineHeight: 1.1, letterSpacing: '-0.04em', whiteSpace: 'nowrap' }}>
            <Rise p={endIn[1]}>{c.h1}</Rise>
            <Rise p={endIn[2]}>
              <Highlight p={endHl}>{c.h2}</Highlight>
            </Rise>
          </div>
          <Rise p={endIn[3]} style={{ marginTop: 40 }}>
            <Pill>
              {c.cta}
              <span style={{ fontSize: 24 }}>→</span>
            </Pill>
          </Rise>
        </div>
      )}

      {/* ripples + cursor on top */}
      <Ripple x={btn1.x} y={btn1.y} p={prog(f, 151, 168)} />
      <Ripple x={boardB.x} y={boardB.y} p={prog(f, 233, 250)} />
      <Ripple x={btn3.x} y={btn3.y} p={prog(f, 269, 286)} />
      {curO > 0 && <Cursor x={cur.x} y={cur.y} press={Math.max(press1, press2, press3)} o={curO} />}
    </AbsoluteFill>
  );
};
