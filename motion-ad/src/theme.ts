import { Easing, interpolate } from 'remotion';

export const WIDTH = 1230;
export const HEIGHT = 380;
export const FPS = 30;
export const DURATION = 18 * FPS;

// Safe area: ≥40 px horizontally, ≥28 px vertically. Text column starts at 56.
export const SAFE_X = 40;
export const SAFE_Y = 28;
export const TEXT_X = 56;

export const C = {
  bg: '#09090B',
  ink: '#FAFAFA',
  ink2: 'rgba(250, 250, 250, 0.62)',
  ink3: 'rgba(250, 250, 250, 0.38)',
  line: 'rgba(255, 255, 255, 0.09)',
  lineStrong: 'rgba(255, 255, 255, 0.16)',
  panel: 'rgba(255, 255, 255, 0.035)',
  blue: '#3B7BFF',
  blueSoft: '#7FA8FF',
  violet: '#A78BFA',
};

export const GRADIENT = `linear-gradient(90deg, ${C.blueSoft} 0%, ${C.violet} 100%)`;

export const ease = {
  /** energetic start, long soft landing */
  out: Easing.bezier(0.16, 1, 0.3, 1),
  /** fast through the middle, soft at both ends — for moves of the whole scene */
  inOut: Easing.bezier(0.76, 0, 0.24, 1),
  soft: Easing.bezier(0.45, 0, 0.55, 1),
  in: Easing.bezier(0.6, 0, 0.9, 0.4),
};

type EasingFn = (t: number) => number;

/** 0→1 progress between two frames (clamped). */
export const prog = (f: number, a: number, b: number, easing: EasingFn = ease.out) =>
  interpolate(f, [a, b], [0, 1], { easing, extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

export const mix = (a: number, b: number, t: number) => a + (b - a) * t;

export type Rect = { x: number; y: number; w: number; h: number; r: number };

export const mixRect = (a: Rect, b: Rect, t: number): Rect => ({
  x: mix(a.x, b.x, t),
  y: mix(a.y, b.y, t),
  w: mix(a.w, b.w, t),
  h: mix(a.h, b.h, t),
  r: mix(a.r, b.r, t),
});

/** Piecewise rect animation: [frame, rect] keys, each segment eased on its own. */
export const rectAt = (f: number, keys: [number, Rect][], easing: EasingFn = ease.inOut): Rect => {
  if (f <= keys[0][0]) return keys[0][1];
  for (let i = 1; i < keys.length; i++) {
    const [f1, r1] = keys[i];
    const [f0, r0] = keys[i - 1];
    if (f <= f1) return mixRect(r0, r1, prog(f, f0, f1, easing));
  }
  return keys[keys.length - 1][1];
};
