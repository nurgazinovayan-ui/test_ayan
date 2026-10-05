import type { CSSProperties, ReactNode } from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame } from 'remotion';
import '../fonts';
import { FONT } from '../fonts';
import { ease, mix, prog } from '../theme';
import { rr } from '../hand/rough';

/*
 * ONEFLOW Motion Engine — "cuts" edit: 1920×1080, 30 fps, 15 s, silent.
 * Fast changes of shot (wide → close-up → detail) between the steps of the mode, every mock-up drawn
 * as a vector outline that traces itself on; lime is the only fill. Each shot has its own camera move,
 * shots are joined by hard cuts, lime wipes, whip-pans, zoom-throughs and an iris.
 */

export const CUTS_W = 1920;
export const CUTS_H = 1080;
export const CUTS_DURATION = 450;

const K = {
  page: '#e5e5e5',
  ink: '#2b2b2b',
  muted: '#8a8a8a',
  lime: '#cdf158',
  black: '#111111',
  paper: '#f1f1f1',
};
const STROKE = 3;

const COPY = {
  ru: {
    l1: 'Ролик',
    l2: 'из ваших фото',
    l3: 'за пару минут',
    steps: ['Фото и бриф', 'Раскадровки', 'Рендер', 'Готовый ролик'],
    s1: 'Загрузите фото',
    brief: 'Задача',
    briefText: 'Летний запуск сыворотки GLOW — свежо и ярко',
    make: 'Сделать раскадровку',
    s2: 'Получите раскадровки',
    variants: ['A', 'B', 'C'],
    picked: 'Выбрано',
    s3: 'Отправьте в рендер',
    done: 'Готово',
    clip1: 'Сияние',
    clip2: 'лета',
    tag: 'новинка',
    end1: 'Ролик из ваших фото',
    end2: 'за пару минут',
    cta: 'Попробовать Motion Engine',
  },
  en: {
    l1: 'Video',
    l2: 'from your photos',
    l3: 'in minutes',
    steps: ['Photos & brief', 'Storyboards', 'Render', 'Finished video'],
    s1: 'Upload photos',
    brief: 'Task',
    briefText: 'Summer launch of GLOW serum — fresh and bright',
    make: 'Make storyboard',
    s2: 'Get storyboards',
    variants: ['A', 'B', 'C'],
    picked: 'Selected',
    s3: 'Send it to render',
    done: 'Done',
    clip1: 'Summer',
    clip2: 'glow',
    tag: 'new',
    end1: 'A video from your photos',
    end2: 'in minutes',
    cta: 'Try Motion Engine',
  },
};
type Copy = (typeof COPY)['ru'];

const LOGO =
  'M17 4.4C18.66 4.4 20 5.74 20 7.4V18.4C20 19.5 20.9 20.4 22 20.4H32C33.66 20.4 35 21.74 35 23.4V34.4C35 35.5 35.9 36.4 37 36.4H38C39.1 36.4 40 35.5 40 34.4V23.4C40 21.74 41.34 20.4 43 20.4H57C58.66 20.4 60 21.74 60 23.4V34.4C60 35.5 60.9 36.4 62 36.4H73C74.66 36.4 76 37.74 76 39.4V53.4C76 55.06 74.66 56.4 73 56.4H59C57.34 56.4 56 55.06 56 53.4V42.4C56 41.3 55.1 40.4 54 40.4H51C49.9 40.4 49 41.3 49 42.4V53.4C49 55.06 47.66 56.4 46 56.4H32C30.34 56.4 29 55.06 29 53.4V42.4C29 41.3 28.1 40.4 27 40.4H24C22.9 40.4 22 41.3 22 42.4V53.4C22 55.06 20.66 56.4 19 56.4H5C3.34 56.4 2 55.06 2 53.4V39.4C2 37.74 3.34 36.4 5 36.4H13C14.1 36.4 15 35.5 15 34.4V26.4C15 25.3 14.1 24.4 13 24.4H3C1.34 24.4 0 23.06 0 21.4V7.4C0 5.74 1.34 4.4 3 4.4H17Z';

// ---- vector helpers ----------------------------------------------------------------------------------

/** A path that traces itself on (p: 0→1). */
const Line: React.FC<{ d: string; p?: number; w?: number; color?: string; fill?: string; style?: CSSProperties }> = ({
  d,
  p = 1,
  w = STROKE,
  color = K.ink,
  fill = 'none',
  style,
}) =>
  p <= 0 ? null : (
    <path
      d={d}
      fill={fill}
      stroke={color}
      strokeWidth={w}
      strokeLinecap="round"
      strokeLinejoin="round"
      vectorEffect="non-scaling-stroke"
      pathLength={1}
      strokeDasharray={p >= 1 ? undefined : '1 2'}
      strokeDashoffset={p >= 1 ? undefined : 1 - p}
      style={style}
    />
  );

const Svg: React.FC<{ w: number; h: number; children: ReactNode; style?: CSSProperties }> = ({ w, h, children, style }) => (
  <svg width={w} height={h} viewBox={`0 0 ${w} ${h}`} style={{ position: 'absolute', left: 0, top: 0, overflow: 'visible', ...style }}>
    {children}
  </svg>
);

const outline = (w = 3, color = K.ink): CSSProperties => ({ WebkitTextStroke: `${w}px ${color}`, color: 'transparent' });

/** Serum bottle as a line drawing; (x, y) is the base centre, h its height in px. */
const BottleLines: React.FC<{ x: number; y: number; h: number; p: number; w?: number; label?: boolean }> = ({ x, y, h, p, w = STROKE, label = true }) => {
  const s = h / 262;
  const parts = [rr(-56, -176, 112, 176, 22), rr(-30, -214, 60, 44, 8), rr(-17, -262, 34, 58, 17), 'M-34 -158 V -30'];
  return (
    <g transform={`translate(${x} ${y}) scale(${s})`}>
      {/* light fill so the bottle sits in front of words and shapes */}
      {parts.slice(0, 3).map((d, i) => (
        <path key={`f${i}`} d={d} fill="#f4f4f2" opacity={prog(p, 0.25, 0.6)} />
      ))}
      {parts.map((d, i) => (
        <Line key={i} d={d} p={prog(p, i * 0.12, 0.5 + i * 0.12, ease.soft)} w={w} />
      ))}
      {label && (
        <>
          <Line d={rr(-42, -112, 84, 66, 6)} p={prog(p, 0.45, 0.9)} w={w} />
          <text x="0" y="-74" textAnchor="middle" fontFamily="Geist" fontWeight="700" fontSize="22" fill={K.ink} opacity={prog(p, 0.8, 1)}>
            GLOW
          </text>
        </>
      )}
    </g>
  );
};

type Mini = { sun?: [number, number, number]; bars?: 'l' | 'r' | 'b'; word?: string; bx: number; size: number; pair?: boolean };

/** One storyboard frame / photo as an outline drawing. */
const MiniFrame: React.FC<{ w: number; h: number; m: Mini; p: number; lime?: number; r?: number }> = ({ w, h, m, p, lime = 0, r = 14 }) => (
  <Svg w={w} h={h}>
    <path d={rr(0, 0, w, h, r)} fill={K.lime} opacity={lime} />
    <Line d={rr(0, 0, w, h, r)} p={prog(p, 0, 0.45)} />
    <Line d={`M0 ${h * 0.84} H${w}`} p={prog(p, 0.2, 0.55)} w={2} color={K.muted} />
    {m.sun && <circle cx={m.sun[0] * w} cy={m.sun[1] * h} r={m.sun[2] * h * prog(p, 0.3, 0.7, ease.out)} fill={K.lime} stroke={K.ink} strokeWidth={2} />}
    {m.word && (
      <text x={w / 2} y={h * 0.62} textAnchor="middle" fontFamily="Geist" fontWeight="800" fontSize={h * 0.36} fill="none" stroke={K.ink} strokeWidth={2} opacity={prog(p, 0.4, 0.8)}>
        {m.word}
      </text>
    )}
    {m.bars &&
      (m.bars === 'b' ? (
        <>
          <Line d={`M${w * 0.3} ${h * 0.92} H${w * 0.7}`} p={prog(p, 0.5, 0.9)} w={5} />
        </>
      ) : (
        <>
          <Line d={`M${m.bars === 'l' ? w * 0.1 : w * 0.58} ${h * 0.3} h${w * 0.3}`} p={prog(p, 0.5, 0.8)} w={6} />
          <Line d={`M${m.bars === 'l' ? w * 0.1 : w * 0.58} ${h * 0.45} h${w * 0.2}`} p={prog(p, 0.6, 0.9)} w={3} />
          <path d={rr(m.bars === 'l' ? w * 0.1 : w * 0.58, h * 0.56, w * 0.14, h * 0.1, h * 0.05)} fill={K.lime} stroke={K.ink} strokeWidth={2} opacity={prog(p, 0.8, 1)} />
        </>
      ))}
    {m.pair && <BottleLines x={(m.bx + 0.13) * w} y={h * 0.84} h={h * m.size * 0.75} p={p} w={2} label={false} />}
    <BottleLines x={m.bx * w} y={h * 0.84} h={h * m.size} p={p} w={2} />
  </Svg>
);

const BOARDS: Mini[][] = [
  [
    { word: 'GLOW', bx: 0.5, size: 0.62 },
    { bars: 'l', bx: 0.74, size: 0.7 },
    { sun: [0.5, 0.42, 0.28], bx: 0.5, size: 0.72 },
    { bars: 'b', bx: 0.5, size: 0.5 },
  ],
  [
    { sun: [0.5, 0.4, 0.26], bx: 0.5, size: 0.66 },
    { bars: 'r', bx: 0.3, size: 0.74 },
    { word: 'SUN', bx: 0.5, size: 0.7 },
    { pair: true, bars: 'b', bx: 0.44, size: 0.5 },
  ],
  [
    { sun: [0.74, 0.3, 0.16], bx: 0.5, size: 0.64 },
    { bars: 'l', bx: 0.7, size: 0.74 },
    { pair: true, bx: 0.42, size: 0.66 },
    { bars: 'b', bx: 0.5, size: 0.5 },
  ],
];

const Cursor: React.FC<{ x: number; y: number; s?: number; press?: number }> = ({ x, y, s = 1, press = 0 }) => (
  <svg
    width={36 * s}
    height={42 * s}
    viewBox="0 0 26 30"
    style={{ position: 'absolute', left: x - 4 * s, top: y - 3 * s, transform: `scale(${1 - press * 0.14})`, transformOrigin: `${4 * s}px ${3 * s}px` }}
  >
    <path d="M3 2 L3 23 L8.6 17.6 L12.4 26.4 L16.2 24.8 L12.5 16.2 L20.4 16.2 Z" fill="#fff" stroke={K.ink} strokeWidth={1.4} strokeLinejoin="round" />
  </svg>
);

/** Lime burst of short strokes around a point (no flash, just lines). */
const Burst: React.FC<{ x: number; y: number; p: number; r0: number; r1: number; n?: number }> = ({ x, y, p, r0, r1, n = 12 }) => {
  if (p <= 0 || p >= 1) return null;
  const a = mix(r0, r1, ease.out(p));
  const b = mix(r0, r1 * 1.25, ease.out(Math.min(1, p * 1.4)));
  return (
    <Svg w={CUTS_W} h={CUTS_H}>
      {Array.from({ length: n }).map((_, i) => {
        const t = (i / n) * Math.PI * 2;
        return (
          <line
            key={i}
            x1={x + Math.cos(t) * a}
            y1={y + Math.sin(t) * a}
            x2={x + Math.cos(t) * b}
            y2={y + Math.sin(t) * b}
            stroke={i % 2 ? K.ink : K.lime}
            strokeWidth={i % 2 ? 4 : 8}
            strokeLinecap="round"
            opacity={1 - p}
          />
        );
      })}
    </Svg>
  );
};

/** A shot: everything inside sits on its own camera (scale/translate around the frame centre). */
const Shot: React.FC<{ cam: { s?: number; x?: number; y?: number; blur?: number; o?: number }; children: ReactNode; bg?: string }> = ({ cam, children, bg }) => (
  <AbsoluteFill style={{ opacity: cam.o ?? 1, background: bg, overflow: 'hidden' }}>
    <AbsoluteFill
      style={{
        transform: `translate(${cam.x ?? 0}px, ${cam.y ?? 0}px) scale(${cam.s ?? 1})`,
        transformOrigin: '960px 540px',
        filter: cam.blur ? `url(#whip${Math.round(cam.blur)})` : undefined,
      }}
    >
      {children}
    </AbsoluteFill>
  </AbsoluteFill>
);

// ---- the film ----------------------------------------------------------------------------------------

export const CutsAd: React.FC<{ lang?: 'ru' | 'en' }> = ({ lang = 'ru' }) => {
  const f = useCurrentFrame();
  const c: Copy = COPY[lang];

  // transition helpers (frame-local)
  const whipOut = (a: number) => ({ x: -2200 * prog(f, a - 5, a, ease.in), blur: 40 * prog(f, a - 5, a - 1) });
  const whipIn = (a: number) => ({ x: 2200 * (1 - prog(f, a, a + 6, ease.out)), blur: 40 * (1 - prog(f, a + 1, a + 6)) });
  const zoomOut = (a: number) => ({ s: mix(1, 5, prog(f, a - 6, a, ease.in)), o: 1 - prog(f, a - 3, a) });
  const zoomIn = (a: number) => mix(0.55, 1, prog(f, a, a + 10, ease.out));
  const punch = (a: number, k = 0.12) => 1 + k * (1 - spring({ frame: f - a, fps: 30, config: { damping: 12, stiffness: 180 } }));
  const wipe = (a: number) => {
    // lime band crosses the screen; the cut happens under it
    // the band fully covers the frame at the cut (p = 0.5)
    const p = prog(f, a - 5, a + 5, ease.inOut);
    return p <= 0 || p >= 1 ? null : (
      <div style={{ position: 'absolute', top: -20, bottom: -20, width: 2500, left: mix(-2750, 2170, p), background: K.lime, transform: 'skewX(-12deg)' }} />
    );
  };

  // shot boundaries
  const B = { s2: 45, s3: 75, s4: 104, s5: 130, s6: 176, s7: 204, s8: 236, s9: 274, s10: 298, s11: 386 };
  const stepOf = f < B.s5 ? 0 : f < B.s7 ? 1 : f < B.s10 ? 2 : 3;
  // shots never overlap: every transition is played out inside the shots on either side of the cut
  const between = (a: number, b: number) => f >= a && f < b;

  // ---------------------------------------------------------------- S1 · title (wide, type)
  const s1 = between(0, B.s2) && (
    <Shot cam={{ s: mix(1, 1.08, prog(f, 0, B.s2, ease.soft)) * (f >= B.s2 - 6 ? zoomOut(B.s2).s : 1), o: f >= B.s2 - 6 ? zoomOut(B.s2).o : 1 }}>
      <div style={{ position: 'absolute', left: 0, right: 0, top: 170, textAlign: 'center', lineHeight: 0.98, letterSpacing: '-0.05em' }}>
        <div style={{ fontSize: 300, fontWeight: 800, ...outline(4), transform: `translateX(${mix(-700, 0, prog(f, 0, 14))}px)` }}>{c.l1}</div>
        <div style={{ fontSize: 150, fontWeight: 300, color: K.ink, transform: `translateX(${mix(700, 0, prog(f, 5, 19))}px)` }}>{c.l2}</div>
        <div style={{ display: 'inline-block', marginTop: 20, fontSize: 150, fontWeight: 300, color: K.ink, position: 'relative', transform: `translateY(${mix(200, 0, prog(f, 10, 24))}px)`, opacity: prog(f, 10, 16) }}>
          <span style={{ position: 'absolute', left: -10, right: -10, bottom: 18, height: 54, background: K.lime, transform: `scaleX(${prog(f, 20, 32, ease.inOut)})`, transformOrigin: 'left' }} />
          <span style={{ position: 'relative' }}>{c.l3}</span>
        </div>
      </div>
    </Shot>
  );

  // ---------------------------------------------------------------- S2 · photos drop in (medium)
  const s2t = f - B.s2;
  const s2 = between(B.s2, B.s3) && (
    <Shot cam={{ s: zoomIn(B.s2) * mix(1, 1.06, prog(f, B.s2, B.s3, ease.soft)) }}>
      <div style={{ position: 'absolute', left: 150, top: 120, fontSize: 84, fontWeight: 300, letterSpacing: '-0.035em', transform: `translateX(${mix(-120, 0, prog(s2t, 0, 12))}px)`, opacity: prog(s2t, 0, 8) }}>
        {c.s1}
      </div>
      {[0, 1, 2].map((i) => {
        const d = spring({ frame: s2t - 3 - i * 5, fps: 30, config: { damping: 13, stiffness: 160 } });
        const m: Mini = i === 0 ? { bx: 0.5, size: 0.62 } : i === 1 ? { bx: 0.44, size: 0.56, pair: true } : { bx: 0.5, size: 0.6, sun: [0.7, 0.28, 0.15] };
        return (
          <div key={i} style={{ position: 'absolute', left: 150 + i * 560, top: 290, width: 500, height: 560, transform: `translateY(${mix(-900, 0, d)}px)` }}>
            <MiniFrame w={500} h={560} m={m} p={prog(s2t, 6 + i * 5, 26 + i * 5)} r={28} lime={i === 2 ? 0 : 0} />
          </div>
        );
      })}
      {wipe(B.s3)}
    </Shot>
  );

  // ---------------------------------------------------------------- S3 · brief typing (macro, panning)
  const s3t = f - B.s3;
  const typed = Math.floor(interpolate(s3t, [3, 24], [0, c.briefText.length], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }));
  const s3 = between(B.s3, B.s4) && (
    <Shot cam={{ s: 1.06, x: mix(70, -70, prog(f, B.s3, B.s4, ease.soft)) }}>
      <Svg w={CUTS_W} h={CUTS_H}>
        <Line d={rr(160, 330, 1600, 400, 48)} p={prog(s3t, 0, 10, ease.out)} w={4} />
        <Line d="M240 650 H900" p={prog(s3t, 18, 28)} w={3} color={K.muted} />
      </Svg>
      <div style={{ position: 'absolute', left: 240, top: 380, fontSize: 40, color: K.muted }}>{c.brief}</div>
      <div style={{ position: 'absolute', left: 240, top: 450, width: 1460, fontSize: 72, fontWeight: 400, lineHeight: 1.2, letterSpacing: '-0.025em' }}>
        {c.briefText.slice(0, typed)}
        <span style={{ display: 'inline-block', width: 6, height: 76, marginLeft: 6, verticalAlign: '-10px', background: K.lime, outline: `2px solid ${K.ink}` }} />
      </div>
      {wipe(B.s3)}
    </Shot>
  );

  // ---------------------------------------------------------------- S4 · button ECU + click
  const s4t = f - B.s4;
  const press = s4t < 12 ? 0 : s4t < 15 ? prog(s4t, 12, 15) : 1 - prog(s4t, 15, 22);
  const s4 = between(B.s4, B.s5) && (
    <Shot cam={{ s: punch(B.s4, 0.18) * (s4t > 14 ? punch(B.s4 + 14, -0.04) : 1), ...(f >= B.s5 - 5 ? whipOut(B.s5) : {}) }}>
      <div
        style={{
          position: 'absolute',
          left: 160,
          top: 380,
          width: 1600,
          height: 300,
          borderRadius: 999,
          background: K.black,
          color: '#fff',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: 40,
          fontSize: 104,
          fontWeight: 500,
          letterSpacing: '-0.03em',
          transform: `scale(${1 - press * 0.05})`,
        }}
      >
        {c.make}
        <svg width="90" height="90" viewBox="0 0 24 24">
          <path d="M3 12h16M13 6l6 6-6 6" stroke={K.lime} strokeWidth="2.4" fill="none" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </div>
      <Cursor x={mix(1900, 1360, prog(s4t, 0, 11, ease.out))} y={mix(1080, 560, prog(s4t, 0, 11, ease.out))} s={4} press={press} />
      <Burst x={1380} y={580} p={prog(s4t, 14, 30)} r0={180} r1={420} n={14} />
    </Shot>
  );

  // ---------------------------------------------------------------- S5 · storyboards (wide, pull-out)
  const s5t = f - B.s5;
  const FW = 380;
  const FH = 213.75;
  const gridX = (1920 - (4 * FW + 3 * 28)) / 2;
  const gridY = 210;
  const rowY = (r: number) => gridY + r * (FH + 64);
  const s5 = between(B.s5, B.s6) && (
    <Shot cam={{ s: mix(1.45, 1, prog(f, B.s5, B.s5 + 30, ease.inOut)), y: mix(260, 0, prog(f, B.s5, B.s5 + 30, ease.inOut)), ...(f < B.s5 + 6 ? whipIn(B.s5) : {}) }}>
      <div style={{ position: 'absolute', left: gridX, top: 96, fontSize: 64, fontWeight: 300, letterSpacing: '-0.03em', opacity: prog(s5t, 8, 16) }}>{c.s2}</div>
      {BOARDS.map((row, r) => (
        <div key={r}>
          <div style={{ position: 'absolute', left: gridX - 70, top: rowY(r) + FH / 2 - 26, fontSize: 44, fontWeight: 600, opacity: prog(s5t, 4 + r * 5, 10 + r * 5) }}>{c.variants[r]}</div>
          {row.map((m, i) => (
            <div key={i} style={{ position: 'absolute', left: gridX + i * (FW + 28), top: rowY(r), width: FW, height: FH }}>
              <MiniFrame w={FW} h={FH} m={m} p={prog(s5t, 2 + r * 6 + i * 3, 20 + r * 6 + i * 3)} />
            </div>
          ))}
        </div>
      ))}
    </Shot>
  );

  // ---------------------------------------------------------------- S6 · pick B (close-up)
  const s6t = f - B.s6;
  const pick = prog(s6t, 8, 16, ease.out);
  const s6 = between(B.s6, B.s7) && (
    <Shot cam={{ s: punch(B.s6, 0.1) * mix(1.75, 1.85, prog(f, B.s6, B.s7, ease.soft)), y: -(rowY(1) + FH / 2 - 540) * 1.8 }}>
      {BOARDS[1].map((m, i) => (
        <div key={i} style={{ position: 'absolute', left: gridX + i * (FW + 28), top: rowY(1), width: FW, height: FH, transform: `translateY(${-10 * pick}px)` }}>
          <MiniFrame w={FW} h={FH} m={m} p={1} lime={0.95 * prog(s6t, 10 + i * 2, 16 + i * 2)} />
        </div>
      ))}
      {[0, 2].map((r) =>
        BOARDS[r].map((m, i) => (
          <div key={`${r}${i}`} style={{ position: 'absolute', left: gridX + i * (FW + 28), top: rowY(r), width: FW, height: FH, opacity: 1 - 0.75 * pick }}>
            <MiniFrame w={FW} h={FH} m={m} p={1} />
          </div>
        )),
      )}
      <div
        style={{
          position: 'absolute',
          left: gridX + 4 * FW + 3 * 28 - 210,
          top: rowY(1) - 46,
          height: 40,
          padding: '0 16px',
          borderRadius: 99,
          background: K.black,
          color: K.lime,
          fontSize: 22,
          fontWeight: 600,
          display: 'flex',
          alignItems: 'center',
          gap: 8,
          opacity: pick,
          transform: `scale(${mix(0.6, 1, pick)})`,
        }}
      >
        ✓ {c.picked}
      </div>
      <Cursor x={mix(1500, gridX + 2 * (FW + 28) + 190, prog(s6t, 0, 8, ease.out))} y={mix(900, rowY(1) + 120, prog(s6t, 0, 8, ease.out))} press={s6t > 8 && s6t < 14 ? 1 : 0} />
      {wipe(B.s7)}
    </Shot>
  );

  // ---------------------------------------------------------------- S7 · frames fly into the timeline
  const s7t = f - B.s7;
  const TLY = 520;
  const s7 = between(B.s7, B.s8) && (
    <Shot cam={{ s: mix(1, 1.1, prog(f, B.s7, B.s8, ease.soft)), ...(f >= B.s8 - 6 ? zoomOut(B.s8) : {}) }}>
      <div style={{ position: 'absolute', left: 150, top: 150, fontSize: 84, fontWeight: 300, letterSpacing: '-0.035em', opacity: prog(s7t, 2, 10) }}>{c.s3}</div>
      <Svg w={CUTS_W} h={CUTS_H}>
        <Line d={rr(150, TLY - 20, 1620, 300, 28)} p={prog(s7t, 0, 12, ease.out)} />
        {Array.from({ length: 41 }).map((_, i) => (
          <Line key={i} d={`M${150 + i * 40.5} ${TLY + 300} v${i % 5 ? 14 : 28}`} p={prog(s7t, 4 + i * 0.2, 8 + i * 0.2)} w={2} color={K.muted} />
        ))}
      </Svg>
      {BOARDS[1].map((m, i) => {
        const k = prog(s7t, 4 + i * 3, 16 + i * 3, ease.out);
        const x = mix(2000 + i * 300, 190 + i * 390, k);
        return (
          <div key={i} style={{ position: 'absolute', left: x, top: TLY, width: 370, height: 208 }}>
            {/* speed lines */}
            <Svg w={370} h={208}>
              {[0.25, 0.5, 0.75].map((yy) => (
                <line key={yy} x1={380} y1={208 * yy} x2={380 + 500 * (1 - k)} y2={208 * yy} stroke={K.ink} strokeWidth={3} strokeLinecap="round" opacity={(1 - k) * 0.8} />
              ))}
            </Svg>
            <MiniFrame w={370} h={208} m={m} p={1} lime={0.95} />
          </div>
        );
      })}
      <div style={{ position: 'absolute', left: mix(190, 1740, prog(s7t, 20, 32, ease.inOut)), top: TLY - 40, width: 4, height: 290, background: K.ink, opacity: prog(s7t, 18, 20) }} />
    </Shot>
  );

  // ---------------------------------------------------------------- S8 · progress ECU
  const s8t = f - B.s8;
  const pct = prog(s8t, 4, 32, ease.soft);
  const s8 = between(B.s8, B.s9) && (
    <Shot cam={{ s: zoomIn(B.s8) * mix(1, 1.08, prog(f, B.s8, B.s9, ease.soft)) }}>
      <div style={{ position: 'absolute', left: 0, right: 0, top: 230, textAlign: 'center', fontSize: 380, fontWeight: 800, letterSpacing: '-0.06em', lineHeight: 1, fontVariantNumeric: 'tabular-nums', ...outline(4) }}>
        {Math.round(pct * 100)}%
      </div>
      <Svg w={CUTS_W} h={CUTS_H}>
        <path d={rr(210, 700, 1500 * pct, 70, 35)} fill={K.lime} />
        <Line d={rr(210, 700, 1500, 70, 35)} p={prog(s8t, 0, 8, ease.out)} />
      </Svg>
    </Shot>
  );

  // ---------------------------------------------------------------- S9 · MP4 ready (punch)
  const s9t = f - B.s9;
  const iris = prog(f, B.s10 - 8, B.s10, ease.inOut);
  const s9 = between(B.s9, B.s10) && (
    <Shot cam={{ s: punch(B.s9, 0.2) }}>
      <div style={{ position: 'absolute', left: 0, right: 0, top: 250, textAlign: 'center', fontSize: 420, fontWeight: 800, letterSpacing: '-0.05em', lineHeight: 1, ...outline(4) }}>MP4</div>
      <Svg w={CUTS_W} h={CUTS_H}>
        <Line d="M960 690 v120 M910 760 l50 50 50 -50 M880 860 h160" p={prog(s9t, 2, 12)} w={6} />
      </Svg>
      <div style={{ position: 'absolute', left: 0, right: 0, top: 160, textAlign: 'center', fontSize: 44, fontWeight: 500, opacity: prog(s9t, 4, 10) }}>
        <span style={{ background: K.lime, padding: '6px 20px', borderRadius: 99 }}>✓ {c.done}</span>
      </div>
      {iris > 0 && <div style={{ position: 'absolute', left: 960 - 1200 * iris, top: 540 - 1200 * iris, width: 2400 * iris, height: 2400 * iris, borderRadius: '50%', background: K.lime }} />}
    </Shot>
  );

  // ---------------------------------------------------------------- S10 · the finished clip, with its own cuts
  const s10t = f - B.s10;
  const sub = s10t < 30 ? 0 : s10t < 58 ? 1 : 2; // wide → bottle close-up → label detail
  const clipCam =
    sub === 0
      ? { s: mix(0.92, 1, prog(s10t, 0, 30, ease.out)), x: 0, y: 0 }
      : sub === 1
        ? { s: punch(B.s10 + 30, 0.1) * mix(2.1, 2.3, prog(s10t, 30, 58, ease.soft)), x: -900, y: -60 }
        : { s: punch(B.s10 + 58, 0.08) * mix(1.25, 1.3, prog(s10t, 58, 90, ease.soft)), x: 120, y: 0 };
  const sunP = spring({ frame: s10t - 2, fps: 30, config: { damping: 16, stiffness: 120 } });
  const s10 = between(B.s10, B.s11) && (
    <Shot cam={{ ...clipCam, ...(f >= B.s11 - 5 ? { x: clipCam.x + whipOut(B.s11).x, blur: whipOut(B.s11).blur } : {}) }} bg={K.page}>
      {/* the lime iris of the previous shot dissolves into the player */}
      <div style={{ position: 'absolute', inset: -400, background: K.lime, opacity: 1 - prog(s10t, 0, 10, ease.soft) }} />
      <Svg w={CUTS_W} h={CUTS_H}>
        {/* player frame + controls */}
        <Line d={rr(150, 110, 1620, 860, 36)} p={prog(s10t, 0, 10, ease.out)} />
        <circle cx={1280} cy={520} r={260 * sunP} fill={K.lime} stroke={K.ink} strokeWidth={3} />
        <Line d="M150 880 H1770" p={prog(s10t, 4, 14)} w={2} color={K.muted} />
        <Line d={`M230 925 h${1460 * prog(s10t, 0, 88, (x) => x)}`} p={1} w={6} />
        <Line d="M198 908 v34 l26 -17 z" p={prog(s10t, 2, 10)} w={3} />
        <BottleLines x={1280} y={830} h={560} p={prog(s10t, 4, 24)} w={4} />
      </Svg>
      <div style={{ position: 'absolute', left: 250, top: 250, fontSize: 210, opacity: sub === 1 ? 0 : 1, fontWeight: 800, lineHeight: 0.92, letterSpacing: '-0.055em' }}>
        <div style={{ overflow: 'hidden' }}>
          <div style={{ transform: `translateY(${mix(110, 0, prog(s10t, 6, 18))}%)` }}>{c.clip1}</div>
        </div>
        <div style={{ overflow: 'hidden' }}>
          <div style={{ transform: `translateY(${mix(110, 0, prog(s10t, 10, 22))}%)`, ...outline(4) }}>{c.clip2}</div>
        </div>
      </div>
      <div
        style={{
          position: 'absolute',
          left: 262,
          top: 680,
          visibility: sub === 1 ? 'hidden' : 'visible',
          padding: '10px 28px',
          borderRadius: 99,
          background: K.black,
          color: K.lime,
          fontSize: 40,
          fontWeight: 600,
          opacity: prog(s10t, 20, 28),
          transform: `translateX(${mix(-60, 0, prog(s10t, 20, 30))}px)`,
        }}
      >
        GLOW · {c.tag}
      </div>
    </Shot>
  );

  // ---------------------------------------------------------------- S11 · end card
  const s11t = f - B.s11;
  const e = [prog(s11t, 0, 12), prog(s11t, 4, 16), prog(s11t, 8, 20), prog(s11t, 12, 24)];
  const s11 = f >= B.s11 && (
    <Shot cam={{ ...(f < B.s11 + 6 ? whipIn(B.s11) : {}), s: mix(1.04, 1, prog(f, B.s11, 450, ease.soft)) }}>
      <Svg w={CUTS_W} h={CUTS_H}>
        <Line d={rr(1180, 250, 580, 580, 290)} p={prog(s11t, 2, 20, ease.out)} w={3} />
        <circle cx={1470} cy={540} r={200 * prog(s11t, 6, 22, ease.out)} fill={K.lime} />
        <BottleLines x={1470} y={720} h={380 + Math.sin(f / 14) * 4} p={prog(s11t, 6, 26)} w={4} />
      </Svg>
      <div style={{ position: 'absolute', left: 150, top: 290 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 20, opacity: e[0], transform: `translateY(${mix(30, 0, e[0])}px)` }}>
          <svg width="76" height="76" viewBox="0 0 96 96">
            <rect width="96" height="96" rx="22" fill={K.black} />
            <g transform="translate(10 13.2)">
              <path d={LOGO} fill="#fff" />
            </g>
          </svg>
          <span style={{ fontSize: 42, fontWeight: 600, letterSpacing: '-0.02em' }}>ONEFLOW</span>
          <span style={{ fontSize: 42, fontWeight: 300, color: K.muted }}>Motion Engine</span>
        </div>
        <div style={{ marginTop: 40, fontSize: 104, fontWeight: 200, lineHeight: 1.08, letterSpacing: '-0.045em', whiteSpace: 'nowrap' }}>
          <div style={{ overflow: 'hidden' }}>
            <div style={{ transform: `translateY(${mix(110, 0, e[1])}%)` }}>{c.end1}</div>
          </div>
          <div style={{ overflow: 'hidden', paddingBottom: 6 }}>
            <div style={{ transform: `translateY(${mix(110, 0, e[2])}%)`, display: 'inline-block', position: 'relative' }}>
              <span style={{ position: 'absolute', left: -6, right: -6, bottom: 12, height: 34, background: K.lime, transform: `scaleX(${prog(s11t, 18, 30, ease.inOut)})`, transformOrigin: 'left' }} />
              <span style={{ position: 'relative' }}>{c.end2}</span>
            </div>
          </div>
        </div>
        <div style={{ marginTop: 50, opacity: e[3], transform: `translateY(${mix(30, 0, e[3])}px)` }}>
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: 16, height: 84, padding: '0 40px', borderRadius: 99, background: K.black, color: '#fff', fontSize: 32, fontWeight: 500 }}>
            {c.cta} <span style={{ color: K.lime }}>→</span>
          </div>
        </div>
      </div>
    </Shot>
  );

  // ---------------------------------------------------------------- HUD: step + editorial timeline
  const hudOn = prog(f, B.s2, B.s2 + 8) * (1 - prog(f, B.s11 - 6, B.s11));
  const stepIn = prog(f, [B.s2, B.s5, B.s7, B.s10][stepOf], [B.s2, B.s5, B.s7, B.s10][stepOf] + 8, ease.out);

  return (
    <AbsoluteFill style={{ background: K.page, fontFamily: FONT, color: K.ink, overflow: 'hidden' }}>
      <svg width="0" height="0" style={{ position: 'absolute' }}>
        {Array.from({ length: 41 }).map((_, i) => (
          <filter key={i} id={`whip${i}`} x="-10%" y="0" width="120%" height="100%">
            <feGaussianBlur stdDeviation={`${i} 0`} />
          </filter>
        ))}
      </svg>
      {s1}
      {s2}
      {s3}
      {s4}
      {s5}
      {s6}
      {s7}
      {s8}
      {s9}
      {s10}
      {s11}

      <div style={{ position: 'absolute', left: 60, top: 44, display: 'flex', alignItems: 'center', gap: 16, opacity: hudOn, fontSize: 24, fontWeight: 500 }}>
        <div style={{ width: 44, height: 44, borderRadius: 99, background: K.lime, border: `2px solid ${K.ink}`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 20, fontWeight: 600 }}>
          {stepOf < 3 ? stepOf + 1 : '▶'}
        </div>
        <div style={{ overflow: 'hidden' }}>
          <div style={{ transform: `translateY(${mix(100, 0, stepIn)}%)` }}>{c.steps[stepOf]}</div>
        </div>
      </div>
      <div style={{ position: 'absolute', right: 60, top: 52, fontSize: 22, color: K.muted, opacity: hudOn, fontVariantNumeric: 'tabular-nums' }}>
        ONEFLOW · Motion Engine
      </div>
      <div style={{ position: 'absolute', left: 60, right: 60, bottom: 40, height: 2, background: 'rgba(43,43,43,0.15)', opacity: hudOn }}>
        <div style={{ width: `${(f / CUTS_DURATION) * 100}%`, height: 2, background: K.ink }} />
      </div>
    </AbsoluteFill>
  );
};
