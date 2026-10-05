import rough from 'roughjs';
import type { Options } from 'roughjs/bin/core';
import type { CSSProperties } from 'react';
import { useLook } from './look';

/*
 * Hand-drawn strokes. roughjs is deterministic for a given `seed`; the seed changes every BOIL
 * frames, so lines "boil" like hand-animated drawings on threes — still a pure function of the frame.
 */
const gen = rough.generator();
export const BOIL = 3;

export type Shape =
  | { kind: 'path'; d: string }
  | { kind: 'line'; x1: number; y1: number; x2: number; y2: number }
  | { kind: 'curve'; pts: [number, number][] }
  | { kind: 'ellipse'; cx: number; cy: number; w: number; h: number }
  | { kind: 'polygon'; pts: [number, number][] };

/** Rounded-rectangle path (a circle when w = h = 2r, a capsule when r = h/2). */
export const rr = (x: number, y: number, w: number, h: number, r: number) => {
  const k = Math.max(0, Math.min(r, w / 2, h / 2));
  return `M${x + k},${y} H${x + w - k} A${k},${k} 0 0 1 ${x + w},${y + k} V${y + h - k} A${k},${k} 0 0 1 ${x + w - k},${y + h} H${x + k} A${k},${k} 0 0 1 ${x},${y + h - k} V${y + k} A${k},${k} 0 0 1 ${x + k},${y} Z`;
};

const build = (s: Shape, o: Options) => {
  switch (s.kind) {
    case 'path':
      return gen.path(s.d, o);
    case 'line':
      return gen.line(s.x1, s.y1, s.x2, s.y2, o);
    case 'curve':
      return gen.curve(s.pts, o);
    case 'ellipse':
      return gen.ellipse(s.cx, s.cy, s.w, s.h, o);
    case 'polygon':
      return gen.polygon(s.pts, o);
  }
};

export const seedFor = (id: number, frame: number) => 1 + id * 13 + (Math.floor(frame / BOIL) % 4);

/**
 * One hand-drawn shape in an SVG that covers its parent. `draw` traces the outline on (0→1),
 * `fillDraw` colours the hachure in the same way, stroke by stroke.
 */
export const Sketch: React.FC<{
  shape: Shape;
  frame: number;
  id: number;
  draw?: number;
  fillDraw?: number;
  opts?: Options;
  style?: CSSProperties;
}> = ({ shape, frame, id, draw = 1, fillDraw, opts = {}, style }) => {
  const K = useLook();
  const o: Options = {
    roughness: 1.3,
    bowing: 1,
    stroke: '#FAFAFA',
    strokeWidth: 1.6,
    hachureGap: 6,
    fillWeight: 1.6,
    preserveVertices: false,
    ...opts,
    seed: seedFor(id, frame),
  };
  o.strokeWidth = (o.strokeWidth ?? 1.6) * K.stroke;
  o.roughness = (o.roughness ?? 1.3) * K.rough;
  o.fillWeight = (o.fillWeight ?? 1.6) * Math.max(1, K.stroke * 0.8);
  if (o.fill && o.fillStyle && o.fillStyle !== 'solid') o.fillStyle = K.fillStyle;
  const paths = gen.toPaths(build(shape, o));
  const fd = fillDraw ?? draw;
  return (
    <svg
      style={{
        position: 'absolute',
        left: 0,
        top: 0,
        width: '100%',
        height: '100%',
        overflow: 'visible',
        pointerEvents: 'none',
        filter: K.glow ? `drop-shadow(0 0 ${K.glow}px ${o.stroke})` : undefined,
        ...style,
      }}
    >
      {paths.map((p, i) => {
        // roughjs emits fill strokes with stroke === fill colour; the outline uses the stroke colour
        const isFill = !!o.fill && p.stroke === o.fill && p.fill === 'none';
        const t = isFill ? fd : draw;
        if (t <= 0) return null;
        return (
          <path
            key={i}
            d={p.d}
            stroke={p.stroke}
            strokeWidth={p.strokeWidth}
            fill={p.fill ?? 'none'}
            strokeLinecap="round"
            strokeLinejoin="round"
            pathLength={1}
            strokeDasharray={t >= 1 ? undefined : '1 2'}
            strokeDashoffset={t >= 1 ? undefined : 1 - t}
          />
        );
      })}
    </svg>
  );
};
