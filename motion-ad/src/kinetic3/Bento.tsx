import type { ReactNode } from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';
import '../fonts';
import { FONT } from '../fonts';
import { ease, mix, prog } from '../theme';
import { LOGO } from '../explainer/shared';
import { B, COPY, Comp, K, Mask, W } from '../kinetic/KineticAd';
import type { Copy } from '../kinetic/KineticAd';

/*
 * «Bento»: the whole frame is a grid of rounded tiles. On every beat the tiles re-flow into a new
 * arrangement (each one on its own easing, slightly staggered) and their content swaps.
 */

const PAD = 60;
const GAP = 20;
const CW = (1920 - 2 * PAD - 11 * GAP) / 12;
const RH = (1080 - 2 * PAD - 5 * GAP) / 6;
type Cell = [number, number, number, number]; // col, row, cols, rows
const rectOf = ([c, r, w, h]: Cell) => ({ x: PAD + c * (CW + GAP), y: PAD + r * (RH + GAP), w: w * CW + (w - 1) * GAP, h: h * RH + (h - 1) * GAP });

const STARTS = [0, B.motion, B.s1, B.s2, B.s3, B.res, B.end];
const LAYOUTS: Cell[][] = [
  [[0, 0, 8, 4], [8, 0, 4, 2], [8, 2, 2, 2], [10, 2, 2, 2], [0, 4, 4, 2], [4, 4, 8, 2]],
  [[2, 0, 8, 4], [0, 0, 2, 3], [10, 0, 2, 3], [0, 3, 2, 3], [10, 3, 2, 3], [2, 4, 8, 2]],
  [[0, 0, 5, 4], [5, 0, 3, 3], [8, 0, 2, 3], [10, 0, 2, 3], [5, 3, 7, 3], [0, 4, 5, 2]],
  [[0, 0, 4, 3], [4, 0, 4, 3], [8, 0, 4, 3], [0, 3, 4, 3], [4, 3, 4, 3], [8, 3, 4, 3]],
  [[0, 0, 7, 6], [7, 0, 5, 2], [7, 2, 5, 2], [7, 4, 2, 2], [9, 4, 2, 2], [11, 4, 1, 2]],
  [[4, 0, 8, 4], [0, 0, 4, 3], [0, 3, 2, 3], [2, 3, 2, 3], [4, 4, 4, 2], [8, 4, 4, 2]],
  [[0, 0, 8, 6], [8, 0, 4, 3], [8, 3, 2, 2], [10, 3, 2, 2], [8, 5, 4, 1], [8, 5, 4, 1]],
];

const Big: React.FC<{ t: number; a: string; b?: string; size?: number; color?: string; sub?: string }> = ({ t, a, b, size = 120, color = K.ink, sub }) => (
  <div style={{ position: 'absolute', left: 48, bottom: 44, right: 48, color }}>
    {sub && <div style={{ fontSize: 24, letterSpacing: '0.06em', opacity: 0.6, marginBottom: 14, ...W(500) }}>{sub}</div>}
    <div style={{ fontSize: size, lineHeight: 0.98, letterSpacing: '-0.05em' }}>
      <Mask y={mix(110, 0, prog(t, 4, 14, ease.out))}>
        <span style={W(mix(200, 750, prog(t, 4, 24)))}>{a}</span>
      </Mask>
      {b && (
        <Mask y={mix(110, 0, prog(t, 8, 18, ease.out))}>
          <span style={{ ...W(200), opacity: 0.55 }}>{b}</span>
        </Mask>
      )}
    </div>
  </div>
);

type TileDef = { bg: string; node: ReactNode };

const content = (beat: number, t: number, i: number, w: number, h: number, c: Copy): TileDef => {
  const comp = (kind: number, bg = '#f7f7f7', fg: string = K.ink, ac: string = K.lime, delay = 0) => <Comp kind={kind} t={t - 4 - delay} w={w} h={h} bg={bg} fg={fg} ac={ac} r={0} />;
  switch (beat) {
    case 0:
      return [
        { bg: '#f7f7f7', node: <div style={{ position: 'absolute', left: 48, bottom: 44, fontSize: 118, lineHeight: 1.0, letterSpacing: '-0.05em', color: K.ink }}>{c.open.map((l, k) => <Mask key={l} y={mix(110, 0, prog(t, k * 8, k * 8 + 10, ease.out))}><span style={W(k === 2 ? 800 : 250)}>{l}</span></Mask>)}</div> },
        { bg: K.lime, node: comp(0, K.lime, K.ink, '#f7f7f7') },
        { bg: K.ink, node: <div style={{ position: 'absolute', left: 28, bottom: 24, color: '#f7f7f7', fontSize: 30, ...W(700) }}>ONEFLOW</div> },
        { bg: '#f7f7f7', node: comp(2) },
        { bg: '#f7f7f7', node: comp(3) },
        { bg: K.ink, node: <div style={{ position: 'absolute', left: 48, top: '50%', transform: 'translateY(-50%)', color: K.lime, fontSize: 64, letterSpacing: '-0.03em', ...W(300) }}>Motion Engine</div> },
      ][i];
    case 1:
      return [
        { bg: K.ink, node: <Big t={t} a="Motion" b="Engine" size={200} color="#f7f7f7" sub="ONEFLOW" /> },
        { bg: K.lime, node: comp(0, K.lime, K.ink, K.ink) },
        { bg: '#f7f7f7', node: comp(1) },
        { bg: '#f7f7f7', node: comp(3) },
        { bg: K.lime, node: comp(2, K.lime, K.ink, '#f7f7f7') },
        { bg: '#f7f7f7', node: <div style={{ position: 'absolute', left: 48, top: '50%', transform: 'translateY(-50%)', fontSize: 52, letterSpacing: '-0.03em', color: K.ink, ...W(300) }}>{c.end1} <b style={W(700)}>{c.end2}</b></div> },
      ][i];
    case 2: {
      const typed = Math.floor(interpolate(t, [30, 60], [0, c.tags.length], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }));
      const press = t < 74 ? 0 : t < 77 ? 1 : 1 - prog(t, 77, 84);
      return [
        { bg: '#f7f7f7', node: <Big t={t} a={`${c.s1a} ${c.s1b}`} b={c.s1c.toLowerCase()} size={96} sub="01 / 03" /> },
        { bg: '#f7f7f7', node: comp(0, '#f7f7f7', K.ink, K.lime, 4) },
        { bg: K.ink, node: comp(3, K.ink, '#f7f7f7', K.lime, 8) },
        { bg: '#f7f7f7', node: comp(1, '#f7f7f7', K.ink, K.lime, 12) },
        { bg: '#f7f7f7', node: <div style={{ position: 'absolute', left: 40, top: 40, right: 40 }}><div style={{ fontSize: 22, color: K.mid, ...W(500) }}>{c.s1c}</div><div style={{ marginTop: 22, display: 'flex', flexWrap: 'wrap', gap: 14 }}>{c.tags.slice(0, typed).map((tg, k) => <div key={tg} style={{ padding: '14px 28px', borderRadius: 99, background: k === 0 ? K.lime : '#ececec', fontSize: 38, ...W(500) }}>{tg}</div>)}</div></div> },
        { bg: K.ink, node: <div style={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 20, color: '#fff', fontSize: 46, ...W(500), transform: `scale(${1 - press * 0.06})`, background: press > 0 ? '#000' : undefined }}>{c.make} <span style={{ color: K.lime }}>→</span></div> },
      ][i];
    }
    case 3: {
      const pick = prog(t, 50, 58, ease.out);
      const frame = (kind: number, chosen: boolean, d: number) => (
        <>
          {comp(kind, chosen && pick > 0.5 ? K.lime : '#f7f7f7', K.ink, chosen && pick > 0.5 ? '#f7f7f7' : K.lime, d)}
          {chosen && <div style={{ position: 'absolute', right: 20, top: 20, padding: '8px 18px', borderRadius: 99, background: K.ink, color: K.lime, fontSize: 24, ...W(600), opacity: pick }}>✓ {c.picked}</div>}
        </>
      );
      return [
        { bg: K.ink, node: <Big t={t} a={c.s2} size={70} color="#f7f7f7" sub="02 / 03" /> },
        { bg: '#f7f7f7', node: frame(3, false, 6) },
        { bg: '#f7f7f7', node: frame(0, true, 10) },
        { bg: '#f7f7f7', node: frame(2, false, 14) },
        { bg: '#f7f7f7', node: frame(1, false, 18) },
        { bg: K.lime, node: <Big t={t - 40} a={c.s2b} size={76} /> },
      ][i];
    }
    case 4: {
      const p = prog(t, 6, 50, ease.soft);
      return [
        { bg: K.lime, node: <div style={{ position: 'absolute', left: 40, bottom: 0, fontSize: 400, lineHeight: 1, letterSpacing: '-0.07em', color: K.ink, fontVariantNumeric: 'tabular-nums', ...W(mix(150, 900, p)) }}>{Math.round(p * 100)}<span style={W(150)}>%</span></div> },
        { bg: '#f7f7f7', node: <Big t={t} a={c.s3} size={96} sub="03 / 03" /> },
        { bg: '#f7f7f7', node: <div style={{ position: 'absolute', left: 40, right: 40, top: '50%', height: 22, marginTop: -11, borderRadius: 99, background: '#e2e2e2', overflow: 'hidden' }}><div style={{ width: `${p * 100}%`, height: '100%', background: K.ink, borderRadius: 99 }} /></div> },
        { bg: K.ink, node: <div style={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', color: K.lime, fontSize: 60, ...W(800) }}>MP4</div> },
        { bg: p >= 1 ? K.lime : '#f7f7f7', node: <div style={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 80, ...W(300), opacity: prog(t, 50, 56) }}>✓</div> },
        { bg: '#f7f7f7', node: comp(2) },
      ][i];
    }
    case 5:
      return [
        { bg: K.ink, node: comp(1, K.ink, '#f7f7f7', K.lime) },
        { bg: '#f7f7f7', node: <Big t={t} a={c.res1} b={c.res2} size={110} /> },
        { bg: K.lime, node: comp(0, K.lime, K.ink, K.ink, 4) },
        { bg: '#f7f7f7', node: comp(3, '#f7f7f7', K.ink, K.lime, 8) },
        { bg: '#f7f7f7', node: comp(2, '#f7f7f7', K.ink, K.lime, 12) },
        { bg: K.lime, node: comp(4, K.lime, K.ink, '#f7f7f7', 6) },
      ][i];
    default:
      return [
        {
          bg: '#f7f7f7',
          node: (
            <div style={{ position: 'absolute', left: 56, bottom: 56, color: K.ink }}>
              <div style={{ fontSize: 28, ...W(600), opacity: prog(t, 2, 10) }}>
                ONEFLOW <span style={{ ...W(300), color: K.mid }}>Motion Engine</span>
              </div>
              <div style={{ marginTop: 22, fontSize: 118, lineHeight: 1, letterSpacing: '-0.05em', whiteSpace: 'nowrap' }}>
                <Mask y={mix(110, 0, prog(t, 4, 14, ease.out))}><span style={W(250)}>{c.end1}</span></Mask>
                <Mask y={mix(110, 0, prog(t, 8, 18, ease.out))}><span style={W(800)}>{c.end2}</span></Mask>
              </div>
            </div>
          ),
        },
        { bg: K.lime, node: <div style={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center' }}><svg width="190" height="190" viewBox="0 0 96 96"><g transform="translate(10 13.2)"><path d={LOGO} fill={K.ink} /></g></svg></div> },
        { bg: K.ink, node: comp(0, K.ink, '#f7f7f7', K.lime) },
        { bg: '#f7f7f7', node: comp(1) },
        { bg: K.ink, node: <div style={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 16, color: '#fff', fontSize: 34, ...W(500) }}>{c.cta} <span style={{ color: K.lime }}>→</span></div> },
        { bg: K.ink, node: null },
      ][i];
  }
};

export const BentoKinetic: React.FC<{ lang?: 'ru' | 'en' }> = ({ lang = 'ru' }) => {
  const f = useCurrentFrame();
  const c = COPY[lang];
  let beat = 0;
  for (let k = 0; k < STARTS.length; k++) if (f >= STARTS[k]) beat = k;
  const t = f - STARTS[beat];

  return (
    <AbsoluteFill style={{ background: K.grey, fontFamily: FONT, overflow: 'hidden' }}>
      {[0, 1, 2, 3, 4, 5].map((i) => {
        const prev = beat === 0 ? LAYOUTS[0][i] : LAYOUTS[beat - 1][i];
        const cur = LAYOUTS[beat][i];
        const k = beat === 0 ? prog(f, i * 2, 12 + i * 2, ease.out) : prog(t, i * 1.5, 14 + i * 1.5, ease.inOut);
        const a = rectOf(prev);
        const b = rectOf(cur);
        const r = { x: mix(a.x, b.x, k), y: mix(a.y, b.y, k), w: mix(a.w, b.w, k), h: mix(a.h, b.h, k) };
        const old = beat > 0 ? content(beat - 1, t + (STARTS[beat] - STARTS[beat - 1]), i, r.w, r.h, c) : null;
        const now = content(beat, t, i, r.w, r.h, c);
        const swap = prog(t, 2, 10);
        const hidden = beat === 6 && i === 5;
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: r.x,
              top: r.y,
              width: r.w,
              height: r.h,
              borderRadius: 36,
              overflow: 'hidden',
              background: swap < 0.5 && old ? old.bg : now.bg,
              opacity: hidden ? 1 - swap : beat === 0 ? prog(f, i * 2, 8 + i * 2) : 1,
              transform: beat === 0 ? `scale(${mix(0.9, 1, k)})` : undefined,
            }}
          >
            {old && swap < 1 && <div style={{ position: 'absolute', inset: 0, opacity: 1 - swap }}>{old.node}</div>}
            <div style={{ position: 'absolute', inset: 0, opacity: beat === 0 ? 1 : swap }}>{now.node}</div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};
