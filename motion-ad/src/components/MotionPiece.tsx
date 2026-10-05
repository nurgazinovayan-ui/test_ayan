import { spring } from 'remotion';
import { C, FPS, ease, mix, prog } from '../theme';
import { FONT } from '../fonts';

/**
 * The "result" of the generation: an authored motion composition built from letters, a circle that
 * stretches into a capsule, lines that fold into a grid, typography moving through masks and a final
 * ad layout. Drawn at a native 830×324 and scaled by the parent (preview window, thumbnails, finale).
 * Everything is a pure function of `t` (frames since this piece started).
 */
export const PIECE_W = 830;
export const PIECE_H = 324;

type Box = { x: number; y: number; w: number; h: number };

type Layout = {
  mirror: boolean;
  flow: { x: number; y: number; size: number; align: 'left' | 'center' };
  capsule: Box;
  /** where the circle sits inside the capsule before it stretches: 0 = left end, 0.5 = centre */
  anchor: number;
  ticker: Box;
  dot: Box;
  rule: { x1: number; x2: number; y: number };
};

const LEFT: Layout = {
  mirror: false,
  flow: { x: 44, y: 70, size: 140, align: 'left' },
  capsule: { x: 486, y: 62, w: 300, h: 92 },
  anchor: 0,
  ticker: { x: 486, y: 178, w: 240, h: 52 },
  dot: { x: 742, y: 182, w: 44, h: 44 },
  rule: { x1: 44, x2: 786, y: 262 },
};

const CENTER: Layout = {
  mirror: false,
  flow: { x: 0, y: 26, size: 148, align: 'center' },
  capsule: { x: 285, y: 196, w: 260, h: 64 },
  anchor: 0.5,
  ticker: { x: 561, y: 202, w: 200, h: 52 },
  dot: { x: 225, y: 206, w: 44, h: 44 },
  rule: { x1: 44, x2: 786, y: 284 },
};

export type Variant = {
  bg: string;
  ink: string;
  muted: string;
  a1: string;
  a2: string;
  capInk: string;
  grid: number;
  layout: 'left' | 'center' | 'right';
  /** rhythm: playback speed of the whole piece and the delay between letters */
  speed: number;
  stagger: number;
};

export const VARIANTS = {
  // the original: night palette, text left, even rhythm
  a: {
    bg: '#0E0F14',
    ink: C.ink,
    muted: 'rgba(250,250,250,0.42)',
    a1: C.blue,
    a2: C.violet,
    capInk: '#FFFFFF',
    grid: 0.1,
    layout: 'left',
    speed: 1,
    stagger: 5,
  },
  // light palette, centred layout, quick tight rhythm
  b: {
    bg: '#ECECF2',
    ink: '#0B0B10',
    muted: 'rgba(11,11,16,0.48)',
    a1: '#6D5BF5',
    a2: C.blue,
    capInk: '#FFFFFF',
    grid: 0.13,
    layout: 'center',
    speed: 1.3,
    stagger: 3,
  },
  // deep blue palette, mirrored layout, slow wide rhythm
  c: {
    bg: '#0B1741',
    ink: '#F4F6FF',
    muted: 'rgba(244,246,255,0.5)',
    a1: C.violet,
    a2: '#63A4FF',
    capInk: '#0B1741',
    grid: 0.14,
    layout: 'right',
    speed: 0.8,
    stagger: 8,
  },
} satisfies Record<string, Variant>;

const ROWS = [54, 108, 162, 216, 270];
const COLS = [138, 277, 415, 553, 692];
const WORDS = ['ИДЕЯ', 'СТИЛЬ', 'МОУШН'];

export const MotionPiece: React.FC<{ t: number; v: Variant; bgOpacity?: number; frameOpacity?: number }> = ({
  t,
  v,
  bgOpacity = 1,
}) => {
  const T = t * v.speed;
  const L = v.layout === 'center' ? CENTER : v.layout === 'right' ? { ...LEFT, mirror: true } : LEFT;
  // mirrored layouts flip every box horizontally inside the piece
  const bx = (b: Box): Box => (L.mirror ? { ...b, x: PIECE_W - b.x - b.w } : b);
  const live = prog(T, 90, 120, ease.soft); // blends the idle "living" motion in after assembly

  // ---- lines → grid ---------------------------------------------------------------------------
  const fold = prog(T, 16, 46, ease.inOut);
  const hLines = ROWS.map((row, i) => {
    const draw = prog(T, i * 2, 22 + i * 2, ease.out);
    const y = mix(162 + (i - 2) * 7, row, fold);
    const op = mix(0.55, v.grid, fold);
    return (
      <div
        key={`h${i}`}
        style={{
          position: 'absolute',
          left: 0,
          top: y,
          width: PIECE_W,
          height: 1,
          background: v.ink,
          opacity: op,
          transform: `scaleX(${draw})`,
          transformOrigin: L.mirror ? 'right' : 'left',
        }}
      />
    );
  });
  const vLines = COLS.map((col, j) => {
    const draw = prog(T, 22 + j * 3, 46 + j * 3, ease.out);
    return (
      <div
        key={`v${j}`}
        style={{
          position: 'absolute',
          left: col,
          top: 0,
          width: 1,
          height: PIECE_H,
          background: v.ink,
          opacity: v.grid,
          transform: `scaleY(${draw})`,
        }}
      />
    );
  });
  // a light pulse that keeps running along one grid line once the layout is assembled
  const sweepX = ((Math.max(0, T - 84) * 7) % (PIECE_W + 400)) - 200;
  const sweep = (
    <div
      style={{
        position: 'absolute',
        left: L.mirror ? PIECE_W - sweepX - 200 : sweepX,
        top: ROWS[4] - 0.5,
        width: 200,
        height: 2,
        opacity: prog(T, 84, 96),
        background: `linear-gradient(90deg, transparent, ${v.a1}, transparent)`,
      }}
    />
  );

  // ---- circle → capsule -----------------------------------------------------------------------
  const cap = bx(L.capsule);
  const pop = spring({ frame: T - 4, fps: FPS, config: { damping: 13, stiffness: 150, mass: 0.7 } });
  const stretch = prog(T, 24, 50, ease.inOut);
  const capW = mix(cap.h, cap.w, stretch) * Math.min(1, pop + stretch);
  const capH = cap.h * Math.min(1, pop + stretch);
  const anchor = L.mirror ? 1 - L.anchor : L.anchor;
  const capX = cap.x + (cap.w - capW) * anchor + (cap.h - capH) / 2 * (1 - 2 * anchor) * (1 - stretch);
  const capY = cap.y + (cap.h - capH) / 2;
  const breathe = 1 + Math.sin(T / 22) * 0.012 * live;

  const fs = cap.h * 0.36;
  const wordBox = fs * 4.9;
  const dotBox = fs * 1.7;
  const period = wordBox + dotBox;
  const marqueeIn = prog(T, 44, 64, ease.out);
  const scroll = (T * 1.4) % period;
  const marquee = (
    <div
      style={{
        position: 'absolute',
        left: -scroll,
        top: 0,
        height: '100%',
        display: 'flex',
        alignItems: 'center',
        transform: `translateY(${mix(100, 0, marqueeIn)}%)`,
      }}
    >
      {Array.from({ length: 8 }).map((_, i) => (
        <div key={i} style={{ display: 'flex', alignItems: 'center' }}>
          <div
            style={{
              width: wordBox,
              paddingLeft: fs * 0.9,
              fontSize: fs,
              fontWeight: 600,
              letterSpacing: '0.06em',
              color: v.capInk,
              lineHeight: 1,
            }}
          >
            MOTION
          </div>
          <div style={{ width: dotBox, display: 'flex', justifyContent: 'center' }}>
            <div style={{ width: fs * 0.28, height: fs * 0.28, borderRadius: 99, background: v.capInk, opacity: 0.7 }} />
          </div>
        </div>
      ))}
    </div>
  );

  // ---- FLOW: letters arrive one by one, then a gradient copy travels through a moving mask --------
  const F = L.flow;
  const letters = 'FLOW'.split('');
  const renderFlow = (accent: boolean) =>
    letters.map((ch, i) => {
      const k = prog(T, 12 + i * v.stagger, 36 + i * v.stagger, ease.out);
      const idle = Math.sin((T - i * 9) / 17) * 2.5 * live;
      return (
        <span key={i} style={{ display: 'inline-block', overflow: 'hidden', padding: '0 0.01em', verticalAlign: 'top' }}>
          <span
            style={{
              display: 'inline-block',
              transform: `translate(${mix(-0.12, 0, k) * F.size}px, ${mix(108, 0, k)}%) translateY(${idle}px)`,
              ...(accent
                ? {
                    backgroundImage: `linear-gradient(90deg, ${v.a1}, ${v.a2})`,
                    WebkitBackgroundClip: 'text',
                    backgroundClip: 'text',
                    color: 'transparent',
                  }
                : { color: v.ink }),
            }}
          >
            {ch}
          </span>
        </span>
      );
    });
  const flowStyle: React.CSSProperties = {
    position: 'absolute',
    top: F.y,
    fontSize: F.size,
    lineHeight: 1,
    fontWeight: 600,
    letterSpacing: '-0.05em',
    whiteSpace: 'nowrap',
    ...(F.align === 'center'
      ? { left: 0, width: PIECE_W, textAlign: 'center' }
      : L.mirror
        ? { right: F.x, textAlign: 'right' }
        : { left: F.x }),
  };
  // the sweep repeats every 150 frames: reveal left→right, then hide left→right
  const ph = T < 64 ? -1 : (T - 64) % 150;
  const wipeIn = ph < 0 ? 0 : prog(ph, 0, 22, ease.inOut);
  const wipeOut = ph < 0 ? 0 : prog(ph, 26, 50, ease.inOut);
  const clip = L.mirror
    ? `inset(0 ${wipeOut * 100}% 0 ${(1 - wipeIn) * 100}%)`
    : `inset(0 ${(1 - wipeIn) * 100}% 0 ${wipeOut * 100}%)`;

  // ---- ticker: words move through a mask ---------------------------------------------------------
  const tk = bx(L.ticker);
  const tickIn = prog(T, 52, 72, ease.out);
  let words: { w: string; y: number }[];
  if (T < 74) {
    words = [{ w: WORDS[0], y: mix(110, 0, tickIn) }];
  } else {
    const c = (T - 74) % 34;
    const k = Math.floor((T - 74) / 34);
    const tr = prog(c, 24, 34, ease.inOut);
    words = [
      { w: WORDS[k % 3], y: -tr * 110 },
      { w: WORDS[(k + 1) % 3], y: (1 - tr) * 110 },
    ];
  }

  // ---- accent dot: splits off the capsule's end and docks next to the ticker ---------------------
  const dot = bx(L.dot);
  const fromEnd = dot.x + dot.w / 2 > cap.x + cap.w / 2;
  const dotStart = {
    x: fromEnd ? cap.x + cap.w - cap.h / 2 - dot.w / 2 : cap.x + cap.h / 2 - dot.w / 2,
    y: cap.y + cap.h / 2 - dot.h / 2,
  };
  const dm = prog(T, 62, 86, ease.inOut);
  const dotX = mix(dotStart.x, dot.x, dm) + Math.sin(T / 19) * 5 * live;
  const dotY = mix(dotStart.y, dot.y, dm);
  const dotOp = prog(T, 60, 66);

  // ---- rule + labels -----------------------------------------------------------------------------
  const R = L.rule;
  const ruleDraw = prog(T, 64, 90, ease.inOut);
  const labelsIn = prog(T, 72, 96, ease.inOut);

  return (
    <div
      style={{
        position: 'absolute',
        left: 0,
        top: 0,
        width: PIECE_W,
        height: PIECE_H,
        overflow: 'hidden',
        fontFamily: FONT,
      }}
    >
      <div style={{ position: 'absolute', inset: 0, background: v.bg, opacity: bgOpacity }} />
      <div
        style={{
          position: 'absolute',
          left: L.mirror ? -120 : PIECE_W - 520,
          top: -200,
          width: 640,
          height: 520,
          borderRadius: '50%',
          opacity: prog(T, 10, 50) * 0.9,
          background: `radial-gradient(closest-side, ${v.a1}33, transparent)`,
        }}
      />
      {hLines}
      {vLines}
      {sweep}

      {/* capsule */}
      <div
        style={{
          position: 'absolute',
          left: capX,
          top: capY,
          width: capW,
          height: capH,
          borderRadius: 999,
          overflow: 'hidden',
          background: `linear-gradient(90deg, ${v.a1}, ${v.a2})`,
          boxShadow: `0 0 ${40 * pop}px ${v.a1}55`,
          transform: `scale(${breathe})`,
        }}
      >
        {marquee}
      </div>

      {/* FLOW + gradient copy through a travelling mask */}
      <div style={flowStyle}>{renderFlow(false)}</div>
      <div style={{ ...flowStyle, clipPath: clip }}>{renderFlow(true)}</div>

      {/* ticker */}
      <div
        style={{
          position: 'absolute',
          left: tk.x,
          top: tk.y,
          width: tk.w,
          height: tk.h,
          overflow: 'hidden',
          textAlign: L.mirror ? 'right' : 'left',
        }}
      >
        {words.map(({ w, y }) => (
          <div
            key={w}
            style={{
              position: 'absolute',
              inset: 0,
              fontSize: tk.h * 0.66,
              lineHeight: `${tk.h}px`,
              fontWeight: 500,
              letterSpacing: '-0.01em',
              color: v.ink,
              transform: `translateY(${y}%)`,
              ...(v.layout === 'center' ? { textAlign: 'left' as const } : {}),
            }}
          >
            {w}
          </div>
        ))}
      </div>

      {/* accent dot */}
      <div
        style={{
          position: 'absolute',
          left: dotX,
          top: dotY,
          width: dot.w,
          height: dot.h,
          borderRadius: 999,
          background: v.a2,
          opacity: dotOp,
          boxShadow: `0 0 24px ${v.a2}88`,
        }}
      />

      {/* rule + labels */}
      <div
        style={{
          position: 'absolute',
          left: R.x1,
          top: R.y,
          width: R.x2 - R.x1,
          height: 1,
          background: v.ink,
          opacity: 0.3,
          transform: `scaleX(${ruleDraw})`,
          transformOrigin: L.mirror ? 'right' : 'left',
        }}
      />
      <div
        style={{
          position: 'absolute',
          left: R.x1,
          top: R.y + 13,
          width: R.x2 - R.x1,
          display: 'flex',
          justifyContent: 'space-between',
          fontSize: 12,
          fontWeight: 500,
          letterSpacing: '0.26em',
          color: v.muted,
          clipPath: L.mirror ? `inset(0 0 0 ${(1 - labelsIn) * 100}%)` : `inset(0 ${(1 - labelsIn) * 100}% 0 0)`,
        }}
      >
        <span>ONEFLOW</span>
        <span>MOTION</span>
      </div>
    </div>
  );
};
