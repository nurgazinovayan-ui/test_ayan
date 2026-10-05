/*
 * Stand-in "product photos" for the demo: a serum dropper bottle drawn in SVG, staged on soft
 * studio backgrounds. Used for the uploaded photos, the storyboard frames and the rendered clip.
 */

export type Shot = {
  bg: [string, string];
  /** bottle centre x and base y, as fractions of the frame */
  x: number;
  y: number;
  /** bottle height as a fraction of the frame height */
  size: number;
  sun?: { x: number; y: number; r: number; color: string };
  /** big word behind the bottle */
  word?: string;
  wordColor?: string;
  /** placeholder copy lines (storyboard frames) */
  bars?: 'left' | 'right' | 'bottom';
  /** a second, smaller bottle behind */
  pair?: boolean;
  /** tilt of the bottle in degrees (a fixed pose, not an animation) */
  tilt?: number;
  glass?: string;
  /** draw the table edge (off for cut-outs) */
  table?: boolean;
};

const Bottle: React.FC<{ glass: string; id: string }> = ({ glass, id }) => (
  <g>
    <defs>
      <linearGradient id={`g-${id}`} x1="0" x2="1">
        <stop offset="0" stopColor={glass} stopOpacity="0.95" />
        <stop offset="0.45" stopColor={glass} stopOpacity="0.75" />
        <stop offset="1" stopColor="#5f7a12" stopOpacity="0.95" />
      </linearGradient>
    </defs>
    {/* bulb + collar */}
    <rect x="-17" y="-262" width="34" height="58" rx="17" fill="#1d1d1f" />
    <rect x="-30" y="-214" width="60" height="44" rx="8" fill="#2b2b2b" />
    <rect x="-30" y="-214" width="60" height="8" rx="4" fill="#3c3c3e" />
    {/* glass body */}
    <rect x="-56" y="-176" width="112" height="176" rx="22" fill={`url(#g-${id})`} />
    <rect x="-40" y="-164" width="12" height="150" rx="6" fill="#fff" opacity="0.38" />
    {/* label */}
    <rect x="-42" y="-112" width="84" height="66" rx="6" fill="#fbfbf7" />
    <text x="0" y="-80" textAnchor="middle" fontFamily="Geist" fontWeight="700" fontSize="22" letterSpacing="1" fill="#2b2b2b">
      GLOW
    </text>
    <text x="0" y="-60" textAnchor="middle" fontFamily="Geist" fontWeight="400" fontSize="11" letterSpacing="2" fill="#7a7a7a">
      SERUM
    </text>
  </g>
);

export const ProductShot: React.FC<{ shot: Shot; w: number; h: number; id: string }> = ({ shot, w, h, id }) => {
  const s = (shot.size * h) / 262;
  const bx = shot.x * w;
  const by = shot.y * h;
  const glass = shot.glass ?? '#c9e955';
  return (
    <svg width={w} height={h} viewBox={`0 0 ${w} ${h}`} style={{ display: 'block' }}>
      <defs>
        <linearGradient id={`bg-${id}`} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor={shot.bg[0]} />
          <stop offset="1" stopColor={shot.bg[1]} />
        </linearGradient>
        <radialGradient id={`sh-${id}`}>
          <stop offset="0" stopColor="#000" stopOpacity="0.28" />
          <stop offset="1" stopColor="#000" stopOpacity="0" />
        </radialGradient>
      </defs>
      <rect width={w} height={h} fill={`url(#bg-${id})`} />
      {/* table edge */}
      {shot.table !== false && <rect x="0" y={by - 2} width={w} height={h - by + 2} fill="#000" opacity="0.035" />}
      {shot.sun && <circle cx={shot.sun.x * w} cy={shot.sun.y * h} r={shot.sun.r * h} fill={shot.sun.color} />}
      {shot.word && (
        <text
          x={w / 2}
          y={h * 0.62}
          textAnchor="middle"
          fontFamily="Geist"
          fontWeight="800"
          fontSize={h * 0.42}
          letterSpacing={-h * 0.02}
          fill={shot.wordColor ?? '#2b2b2b'}
        >
          {shot.word}
        </text>
      )}
      {shot.bars && (
        <g fill="#2b2b2b">
          {shot.bars === 'bottom' ? (
            <>
              <rect x={w * 0.3} y={h * 0.84} width={w * 0.4} height={h * 0.05} rx={h * 0.025} />
              <rect x={w * 0.38} y={h * 0.91} width={w * 0.24} height={h * 0.03} rx={h * 0.015} opacity="0.4" />
            </>
          ) : (
            <>
              <rect x={shot.bars === 'left' ? w * 0.08 : w * 0.56} y={h * 0.3} width={w * 0.34} height={h * 0.09} rx={h * 0.03} />
              <rect x={shot.bars === 'left' ? w * 0.08 : w * 0.56} y={h * 0.44} width={w * 0.24} height={h * 0.05} rx={h * 0.025} opacity="0.4" />
              <rect x={shot.bars === 'left' ? w * 0.08 : w * 0.56} y={h * 0.6} width={w * 0.16} height={h * 0.08} rx={h * 0.04} fill="#cdf158" />
            </>
          )}
        </g>
      )}
      <ellipse cx={bx} cy={by} rx={70 * s} ry={14 * s} fill={`url(#sh-${id})`} />
      {shot.pair && (
        <g transform={`translate(${bx + 78 * s} ${by - 4 * s}) scale(${s * 0.78})`} opacity="0.9">
          <Bottle glass="#e5f3a8" id={`${id}b`} />
        </g>
      )}
      <g transform={`translate(${bx} ${by}) rotate(${shot.tilt ?? 0}) scale(${s})`}>
        <Bottle glass={glass} id={id} />
      </g>
    </svg>
  );
};

// uploaded photos (square)
export const PHOTOS: Shot[] = [
  { bg: ['#eef3df', '#dfe8c6'], x: 0.5, y: 0.82, size: 0.62 },
  { bg: ['#f1f1f1', '#dedede'], x: 0.44, y: 0.84, size: 0.56, pair: true },
  { bg: ['#f6ecdc', '#ead9bf'], x: 0.5, y: 0.8, size: 0.6, sun: { x: 0.7, y: 0.3, r: 0.16, color: '#f9d98a' } },
];

// three storyboard variants × four frames (16:9)
export const BOARDS: { name: string; shots: Shot[] }[] = [
  {
    name: 'A',
    shots: [
      { bg: ['#f1f1f1', '#e2e2e2'], x: 0.5, y: 0.86, size: 0.7, word: 'GLOW', wordColor: '#d9d9d9' },
      { bg: ['#eef3df', '#dfe8c6'], x: 0.7, y: 0.88, size: 0.78, bars: 'left' },
      { bg: ['#2b2b2b', '#1c1c1e'], x: 0.5, y: 0.9, size: 0.86, sun: { x: 0.5, y: 0.45, r: 0.3, color: '#cdf158' } },
      { bg: ['#f1f1f1', '#e2e2e2'], x: 0.5, y: 0.7, size: 0.5, bars: 'bottom' },
    ],
  },
  {
    name: 'B',
    shots: [
      { bg: ['#f3f7e6', '#e3edc2'], x: 0.5, y: 0.88, size: 0.74, sun: { x: 0.5, y: 0.42, r: 0.28, color: '#cdf158' } },
      { bg: ['#f3f7e6', '#e3edc2'], x: 0.32, y: 0.9, size: 0.84, bars: 'right' },
      { bg: ['#cdf158', '#b9de3c'], x: 0.5, y: 0.9, size: 0.8, word: 'SUMMER', wordColor: '#2b2b2b' },
      { bg: ['#f3f7e6', '#e3edc2'], x: 0.5, y: 0.72, size: 0.52, pair: true, bars: 'bottom' },
    ],
  },
  {
    name: 'C',
    shots: [
      { bg: ['#f6ecdc', '#ead9bf'], x: 0.5, y: 0.86, size: 0.7, sun: { x: 0.72, y: 0.3, r: 0.18, color: '#f9d98a' } },
      { bg: ['#f6ecdc', '#ead9bf'], x: 0.66, y: 0.9, size: 0.84, tilt: -8, bars: 'left' },
      { bg: ['#ffffff', '#f0f0f0'], x: 0.5, y: 0.88, size: 0.76, pair: true },
      { bg: ['#f6ecdc', '#ead9bf'], x: 0.5, y: 0.72, size: 0.5, bars: 'bottom' },
    ],
  },
];
