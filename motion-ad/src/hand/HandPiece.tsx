import { spring } from 'remotion';
import { FPS, ease, mix, prog } from '../theme';
import { FONT, HAND } from '../fonts';
import { Sketch, rr } from './rough';

/**
 * Hand-drawn cut of the generated piece (native 830×324, scaled by the parent):
 * FLOW letters arrive one by one, a sketched circle stretches into a capsule, pencil lines fold into
 * a grid, words move through masks and everything settles into a small poster layout.
 * Pure function of `t` (frames since the piece started) and `frame` (for the line boil).
 */
export const HP_W = 830;
export const HP_H = 324;

type Box = { x: number; y: number; w: number; h: number };

type Layout = {
  mirror: boolean;
  flow: { x: number; y: number; size: number; align: 'left' | 'center' };
  capsule: Box;
  anchor: number;
  ticker: Box;
  dot: Box;
  rule: { x1: number; x2: number; y: number };
};

const LEFT: Layout = {
  mirror: false,
  flow: { x: 44, y: 48, size: 172, align: 'left' },
  capsule: { x: 486, y: 62, w: 300, h: 92 },
  anchor: 0,
  ticker: { x: 490, y: 172, w: 236, h: 62 },
  dot: { x: 740, y: 184, w: 44, h: 44 },
  rule: { x1: 44, x2: 786, y: 262 },
};

const CENTER: Layout = {
  mirror: false,
  flow: { x: 0, y: 12, size: 176, align: 'center' },
  capsule: { x: 285, y: 196, w: 260, h: 64 },
  anchor: 0.5,
  ticker: { x: 563, y: 196, w: 200, h: 64 },
  dot: { x: 225, y: 206, w: 44, h: 44 },
  rule: { x1: 44, x2: 786, y: 284 },
};

export type HandVariant = {
  bg: string;
  ink: string;
  muted: string;
  a1: string;
  a2: string;
  capInk: string;
  grid: number;
  layout: 'left' | 'center' | 'right';
  speed: number;
  stagger: number;
};

export const HAND_VARIANTS = {
  // chalk on night: the original
  a: {
    bg: '#0E0F14',
    ink: '#F4F4F6',
    muted: 'rgba(244,244,246,0.5)',
    a1: '#3B7BFF',
    a2: '#A78BFA',
    capInk: '#FFFFFF',
    grid: 0.16,
    layout: 'left',
    speed: 1,
    stagger: 5,
  },
  // pencil on paper, centred, quick rhythm
  b: {
    bg: '#EFECE4',
    ink: '#16161C',
    muted: 'rgba(22,22,28,0.55)',
    a1: '#6D5BF5',
    a2: '#3B7BFF',
    capInk: '#FFFFFF',
    grid: 0.18,
    layout: 'center',
    speed: 1.3,
    stagger: 3,
  },
  // blueprint, mirrored, slow rhythm
  c: {
    bg: '#0D1C4F',
    ink: '#EEF2FF',
    muted: 'rgba(238,242,255,0.55)',
    a1: '#A78BFA',
    a2: '#7FB0FF',
    capInk: '#0D1C4F',
    grid: 0.22,
    layout: 'right',
    speed: 0.8,
    stagger: 8,
  },
} satisfies Record<string, HandVariant>;

const ROWS = [54, 108, 162, 216, 270];
const COLS = [138, 277, 415, 553, 692];
const WORDS = ['идея', 'стиль', 'моушн'];

export const HandPiece: React.FC<{ t: number; frame: number; v: HandVariant; bgOpacity?: number; seed?: number }> = ({
  t,
  frame,
  v,
  bgOpacity = 1,
  seed = 100,
}) => {
  const T = t * v.speed;
  const L = v.layout === 'center' ? CENTER : v.layout === 'right' ? { ...LEFT, mirror: true } : LEFT;
  const bx = (b: Box): Box => (L.mirror ? { ...b, x: HP_W - b.x - b.w } : b);
  const live = prog(T, 90, 120, ease.soft);
  const pencil = { stroke: v.ink, strokeWidth: 1.2, roughness: 1.6 };

  // ---- pencil lines → grid ------------------------------------------------------------------------
  const fold = prog(T, 16, 46, ease.inOut);
  const hLines = ROWS.map((row, i) => {
    const y = mix(162 + (i - 2) * 8, row, fold);
    return (
      <div key={`h${i}`} style={{ position: 'absolute', inset: 0, opacity: mix(0.7, v.grid, fold) }}>
        <Sketch
          id={seed + i}
          frame={frame}
          shape={L.mirror ? { kind: 'line', x1: HP_W - 4, y1: y, x2: 4, y2: y } : { kind: 'line', x1: 4, y1: y, x2: HP_W - 4, y2: y }}
          draw={prog(T, i * 2, 22 + i * 2, ease.out)}
          opts={pencil}
        />
      </div>
    );
  });
  const vLines = COLS.map((col, j) => (
    <div key={`v${j}`} style={{ position: 'absolute', inset: 0, opacity: v.grid }}>
      <Sketch
        id={seed + 10 + j}
        frame={frame}
        shape={{ kind: 'line', x1: col, y1: 4, x2: col, y2: HP_H - 4 }}
        draw={prog(T, 22 + j * 3, 46 + j * 3, ease.out)}
        opts={pencil}
      />
    </div>
  ));

  // ---- circle → capsule (shape is re-sketched every frame of the stretch) -------------------------
  const cap = bx(L.capsule);
  const pop = spring({ frame: T - 4, fps: FPS, config: { damping: 13, stiffness: 150, mass: 0.7 } });
  const stretch = prog(T, 24, 50, ease.inOut);
  const grow = Math.min(1, pop + stretch);
  const capW = mix(cap.h, cap.w, stretch) * grow;
  const capH = cap.h * grow;
  const anchor = L.mirror ? 1 - L.anchor : L.anchor;
  const capX = cap.x + (cap.w - capW) * anchor + ((cap.h - capH) / 2) * (1 - 2 * anchor) * (1 - stretch);
  const capY = cap.y + (cap.h - capH) / 2;
  const capShape = { kind: 'path' as const, d: rr(capX, capY, Math.max(capW, 1), Math.max(capH, 1), capH / 2) };

  const fs = cap.h * 0.5;
  const wordBox = fs * 3.5;
  const dotBox = fs * 1.2;
  const period = wordBox + dotBox;
  const marqueeIn = prog(T, 44, 64, ease.out);
  const scroll = (T * 1.4) % period;

  // ---- FLOW ---------------------------------------------------------------------------------------
  const F = L.flow;
  const flowStyle: React.CSSProperties = {
    position: 'absolute',
    top: F.y,
    fontFamily: HAND,
    fontSize: F.size,
    lineHeight: 1,
    fontWeight: 700,
    letterSpacing: '0.01em',
    whiteSpace: 'nowrap',
    ...(F.align === 'center'
      ? { left: 0, width: HP_W, textAlign: 'center' }
      : L.mirror
        ? { right: F.x, textAlign: 'right' }
        : { left: F.x }),
  };
  const renderFlow = (color: string, dx: number, dy: number) =>
    'FLOW'.split('').map((ch, i) => {
      const k = prog(T, 12 + i * v.stagger, 36 + i * v.stagger, ease.out);
      const idle = Math.sin((T - i * 9) / 17) * 3 * live;
      // a small hand-animated wobble that steps on threes, like the lines
      const step = Math.floor(frame / 3) % 4;
      const wob = [0, 0.8, -0.6, 0.4][(step + i) % 4] * live;
      return (
        <span key={i} style={{ display: 'inline-block', overflow: 'hidden', padding: '0 0.04em 0.1em', verticalAlign: 'top' }}>
          <span
            style={{
              display: 'inline-block',
              color,
              transform: `translate(${mix(-0.12, 0, k) * F.size + dx}px, ${mix(110, 0, k)}%) translateY(${idle + dy}px) rotate(${wob}deg)`,
            }}
          >
            {ch}
          </span>
        </span>
      );
    });
  // misregistered colour pass slides in through a moving mask, repeats every 150 frames
  const ph = T < 64 ? -1 : (T - 64) % 150;
  const wipeIn = ph < 0 ? 0 : prog(ph, 0, 22, ease.inOut);
  const wipeOut = ph < 0 ? 0 : prog(ph, 40, 64, ease.inOut);
  const clip = L.mirror
    ? `inset(0 ${wipeOut * 100}% 0 ${(1 - wipeIn) * 100}%)`
    : `inset(0 ${(1 - wipeIn) * 100}% 0 ${wipeOut * 100}%)`;

  // ---- ticker ---------------------------------------------------------------------------------------
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

  // ---- accent dot -----------------------------------------------------------------------------------
  const dot = bx(L.dot);
  const fromEnd = dot.x + dot.w / 2 > cap.x + cap.w / 2;
  const dsx = fromEnd ? cap.x + cap.w - cap.h / 2 - dot.w / 2 : cap.x + cap.h / 2 - dot.w / 2;
  const dsy = cap.y + cap.h / 2 - dot.h / 2;
  const dm = prog(T, 62, 86, ease.inOut);
  const dotX = mix(dsx, dot.x, dm) + Math.sin(T / 19) * 5 * live;
  const dotY = mix(dsy, dot.y, dm);
  const dotOp = prog(T, 60, 66);

  const R = L.rule;
  const ruleDraw = prog(T, 64, 90, ease.inOut);
  const labelsIn = prog(T, 72, 96, ease.inOut);
  // a pencil tick that travels along the rule once assembled
  const sweepX = ((Math.max(0, T - 90) * 5) % (R.x2 - R.x1 + 200)) - 100;

  return (
    <div style={{ position: 'absolute', left: 0, top: 0, width: HP_W, height: HP_H, overflow: 'hidden', fontFamily: FONT }}>
      <div style={{ position: 'absolute', inset: 0, background: v.bg, opacity: bgOpacity }} />
      {hLines}
      {vLines}

      {/* capsule: soft colour underlay + hachure + chalk outline */}
      <div
        style={{
          position: 'absolute',
          left: capX + 4,
          top: capY + 4,
          width: Math.max(0, capW - 8),
          height: Math.max(0, capH - 8),
          borderRadius: 999,
          background: `linear-gradient(90deg, ${v.a1}, ${v.a2})`,
          opacity: 0.55 * grow,
        }}
      />
      <Sketch
        id={seed + 20}
        frame={frame}
        shape={capShape}
        draw={Math.min(1, pop * 1.4)}
        fillDraw={prog(T, 8, 40, ease.soft)}
        opts={{ stroke: v.ink, strokeWidth: 2, fill: v.a1, fillStyle: 'hachure', hachureAngle: -40, hachureGap: 5, fillWeight: 2 }}
      />
      <div
        style={{
          position: 'absolute',
          left: capX + 6,
          top: capY,
          width: Math.max(0, capW - 12),
          height: capH,
          borderRadius: 999,
          overflow: 'hidden',
        }}
      >
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
                  paddingLeft: fs * 0.5,
                  fontFamily: HAND,
                  fontSize: fs,
                  fontWeight: 700,
                  color: v.capInk,
                  lineHeight: 1,
                }}
              >
                motion
              </div>
              <div style={{ width: dotBox, fontFamily: HAND, fontSize: fs, color: v.capInk, textAlign: 'center' }}>•</div>
            </div>
          ))}
        </div>
      </div>

      {/* FLOW: colour pass behind, ink on top */}
      <div style={{ ...flowStyle, clipPath: clip }}>{renderFlow(v.a1, 7, 6)}</div>
      <div style={flowStyle}>{renderFlow(v.ink, 0, 0)}</div>

      {/* ticker */}
      <div style={{ position: 'absolute', left: tk.x, top: tk.y, width: tk.w, height: tk.h, overflow: 'hidden' }}>
        {words.map(({ w, y }) => (
          <div
            key={w}
            style={{
              position: 'absolute',
              inset: 0,
              fontFamily: HAND,
              fontSize: tk.h * 0.8,
              lineHeight: `${tk.h}px`,
              fontWeight: 700,
              color: v.ink,
              textAlign: L.mirror ? 'right' : 'left',
              transform: `translateY(${y}%)`,
            }}
          >
            {w}
          </div>
        ))}
      </div>

      {/* accent dot */}
      <div style={{ position: 'absolute', left: dotX, top: dotY, width: dot.w, height: dot.h, opacity: dotOp }}>
        <Sketch
          id={seed + 30}
          frame={frame}
          shape={{ kind: 'ellipse', cx: dot.w / 2, cy: dot.h / 2, w: dot.w, h: dot.h }}
          opts={{ stroke: v.ink, strokeWidth: 1.6, fill: v.a2, fillStyle: 'solid' }}
        />
      </div>

      {/* rule + labels */}
      <Sketch
        id={seed + 40}
        frame={frame}
        shape={L.mirror ? { kind: 'line', x1: R.x2, y1: R.y, x2: R.x1, y2: R.y } : { kind: 'line', x1: R.x1, y1: R.y, x2: R.x2, y2: R.y }}
        draw={ruleDraw}
        opts={{ stroke: v.ink, strokeWidth: 1.4, roughness: 1.4 }}
      />
      <div
        style={{
          position: 'absolute',
          left: R.x1 + sweepX,
          top: R.y - 4,
          width: 100,
          height: 8,
          opacity: prog(T, 90, 100) * 0.9,
        }}
      >
        <Sketch
          id={seed + 41}
          frame={frame}
          shape={{ kind: 'line', x1: 0, y1: 4, x2: 100, y2: 4 }}
          opts={{ stroke: v.a2, strokeWidth: 3, roughness: 1.2 }}
        />
      </div>
      <div
        style={{
          position: 'absolute',
          left: R.x1,
          top: R.y + 8,
          width: R.x2 - R.x1,
          display: 'flex',
          justifyContent: 'space-between',
          fontFamily: HAND,
          fontSize: 22,
          fontWeight: 700,
          letterSpacing: '0.08em',
          color: v.muted,
          clipPath: L.mirror ? `inset(0 0 0 ${(1 - labelsIn) * 100}%)` : `inset(0 ${(1 - labelsIn) * 100}% 0 0)`,
        }}
      >
        <span>ONEFLOW</span>
        <span>motion</span>
      </div>
    </div>
  );
};
