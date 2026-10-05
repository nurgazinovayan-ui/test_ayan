import type { CSSProperties, ReactNode } from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';
import '../fonts';
import { PIXEL } from '../fonts';
import { mix, prog } from '../theme';
import { LOGO } from '../explainer/shared';
import { B, COPY, K } from '../kinetic/KineticAd';

/*
 * «Пиксель»: Press Start 2P, shapes rasterised onto a coarse grid, motion stepped like a sprite
 * (the clock advances every 3 frames), hard 4 px borders and block shadows. Retro-modern, playful.
 */

const STEP = 3;
const q = (f: number) => Math.floor(f / STEP) * STEP;
const PX = (s: number): CSSProperties => ({ fontFamily: PIXEL, fontSize: s, lineHeight: 1.35, letterSpacing: 0 });

/** Rasterised composition on an n×m grid. */
const PixelArt: React.FC<{ kind: number; t: number; w: number; h: number; cell?: number; bg?: string; fg?: string; ac?: string }> = ({ kind, t, w, h, cell = 16, bg = '#f7f7f7', fg = K.ink, ac = K.lime }) => {
  const n = Math.floor(w / cell);
  const m = Math.floor(h / cell);
  const cells: { x: number; y: number; c: string }[] = [];
  const cx = n / 2;
  const cy = m / 2;
  const g = Math.min(1, Math.max(0, t / 18));
  for (let y = 0; y < m; y++) {
    for (let x = 0; x < n; x++) {
      let c: string | null = null;
      const dx = x + 0.5 - cx;
      const dy = y + 0.5 - cy;
      if (kind === 0) {
        const r = Math.min(n, m) * 0.32 * g;
        if (dx * dx + dy * dy < r * r) c = ac;
      } else if (kind === 1) {
        const hh = m * 0.18;
        const half = mix(hh, n * 0.38, Math.min(1, Math.max(0, (t - 8) / 14)));
        const ex = Math.max(0, Math.abs(dx) - (half - hh));
        if (ex * ex + dy * dy < hh * hh * g) c = fg;
        const px = cx - half + hh + ((Math.floor(t / 6) % 8) / 7) * (2 * half - 2 * hh);
        if ((x + 0.5 - px) ** 2 + dy * dy < (hh * 0.6) ** 2 && g >= 1) c = ac;
      } else if (kind === 2) {
        const rows = [0.2, 0.4, 0.6, 0.8];
        rows.forEach((ry, i) => {
          if (y === Math.floor(m * ry) && x > n * 0.1 && x < n * 0.1 + n * 0.8 * Math.min(1, Math.max(0, (t - i * 3) / 12))) c = i === 1 ? ac : fg;
        });
        if ((x === Math.floor(n * 0.35) || x === Math.floor(n * 0.65)) && y > m * 0.2 && y < m * 0.2 + m * 0.6 * Math.min(1, Math.max(0, (t - 10) / 10))) c = fg;
      } else if (kind === 3) {
        const s = Math.floor(Math.min(n, m) * 0.4);
        const off = Math.round(mix(-s, 0, Math.min(1, t / 14)));
        const ax = Math.floor(n * 0.2) + off;
        const bx = Math.floor(n * 0.42) - off;
        const ty = Math.floor(m / 2 - s / 2);
        if (x >= ax && x < ax + s && y >= ty && y < ty + s) c = ac;
        if (x >= bx && x < bx + s && y >= ty + 2 && y < ty + 2 + s) c = c ? '#5d6b1f' : fg;
      } else {
        // a pixel "M"
        const L = Math.floor(n * 0.25);
        const R = Math.floor(n * 0.75);
        const T = Math.floor(m * 0.2);
        const Bt = Math.floor(m * 0.8);
        const mid = Math.floor(n / 2);
        const vis = y < T + (Bt - T) * Math.min(1, t / 14);
        if (vis && y >= T && y <= Bt && (x === L || x === L + 1 || x === R || x === R - 1)) c = fg;
        if (vis && y >= T && y <= T + (mid - L) && (x - L === y - T || R - x === y - T)) c = fg;
        if (y === Bt && x === R + 2 && t > 14) c = ac;
      }
      if (c) cells.push({ x, y, c });
    }
  }
  return (
    <svg width={w} height={h} style={{ display: 'block', background: bg }} shapeRendering="crispEdges">
      {cells.map((p, i) => (
        <rect key={i} x={p.x * cell} y={p.y * cell} width={cell} height={cell} fill={p.c} />
      ))}
    </svg>
  );
};

const Box: React.FC<{ x: number; y: number; w: number; h: number; bg?: string; children?: ReactNode; drop?: number; press?: number }> = ({ x, y, w, h, bg = '#f7f7f7', children, drop = 0, press = 0 }) => (
  <div style={{ position: 'absolute', left: x + press * 8, top: y - drop + press * 8, width: w, height: h, background: bg, border: `4px solid ${K.ink}`, boxShadow: `${8 - press * 8}px ${8 - press * 8}px 0 ${K.ink}`, overflow: 'hidden' }}>{children}</div>
);

/** Typewriter in steps. */
const type = (s: string, t: number, cps = 1.2) => s.slice(0, Math.max(0, Math.floor(t * cps)));

export const PixelKinetic: React.FC<{ lang?: 'ru' | 'en' }> = ({ lang = 'ru' }) => {
  const fr = useCurrentFrame();
  const f = q(fr);
  const c = COPY[lang];
  const blink = Math.floor(fr / 8) % 2 === 0;
  let body: ReactNode;
  let bg: string = K.grey;

  if (f < B.motion) {
    body = (
      <div style={{ position: 'absolute', left: 150, top: 300, color: K.ink }}>
        {c.open.map((l, i) => (
          <div key={l} style={{ ...PX(80), marginBottom: 30, display: 'table', whiteSpace: 'nowrap', padding: i === 2 ? '8px 20px' : 0, background: i === 2 && f > 20 ? K.lime : 'transparent' }}>
            {type(l.toUpperCase(), f - i * 9, 1.6)}
            {f >= i * 9 && f < (i + 1) * 9 && blink && '█'}
          </div>
        ))}
      </div>
    );
  } else if (f < B.s1) {
    const t = f - B.motion;
    bg = K.ink;
    body = (
      <>
        <div style={{ position: 'absolute', left: 0, right: 0, top: 300, textAlign: 'center', ...PX(170), color: K.lime, textShadow: `10px 10px 0 #4a5a12` }}>{type('MOTION', t, 0.6)}</div>
        <div style={{ position: 'absolute', left: 0, right: 0, top: 560, textAlign: 'center', ...PX(110), color: '#f7f7f7' }}>{type('ENGINE', t - 9, 0.6)}</div>
        <div style={{ position: 'absolute', left: 0, right: 0, top: 220, textAlign: 'center', ...PX(28), color: '#8a8a8a' }}>ONEFLOW</div>
        <div style={{ position: 'absolute', left: 0, right: 0, top: 780, textAlign: 'center', ...PX(30), color: '#f7f7f7', opacity: t > 18 && blink ? 1 : 0 }}>▶ PRESS START</div>
      </>
    );
  } else if (f < B.s2) {
    const t = f - B.s1;
    const typed = Math.floor(interpolate(t, [36, 62], [0, c.tags.length], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }));
    const press = t >= 72 && t < 81 ? 1 : 0;
    body = (
      <>
        <div style={{ position: 'absolute', left: 120, top: 110, ...PX(30), color: K.mid }}>STAGE 01</div>
        <div style={{ position: 'absolute', left: 120, top: 160, ...PX(64), color: K.ink }}>{type(`${c.s1a} ${c.s1b}`.toUpperCase(), t, 1.4)}</div>
        {[0, 3, 1].map((k, i) => {
          const land = Math.min(1, Math.max(0, (t - 6 - i * 6) / 9));
          return (
            <Box key={i} x={120 + i * 340} y={300} w={304} h={304} bg={i === 1 ? K.ink : '#f7f7f7'} drop={Math.round((1 - land) * 6) * 100}>
              <PixelArt kind={k} t={t - 12 - i * 6} w={296} h={296} bg={i === 1 ? K.ink : '#f7f7f7'} fg={i === 1 ? '#f7f7f7' : K.ink} />
            </Box>
          );
        })}
        <Box x={1180} y={300} w={620} h={304}>
          <div style={{ position: 'absolute', left: 26, top: 26, ...PX(20), color: K.mid }}>{c.s1c.toUpperCase()}</div>
          <div style={{ position: 'absolute', left: 26, top: 80, right: 20, display: 'flex', flexWrap: 'wrap', gap: 14 }}>
            {c.tags.slice(0, typed).map((tg, k) => (
              <div key={tg} style={{ ...PX(24), padding: '10px 14px', border: `4px solid ${K.ink}`, background: k === 0 ? K.lime : '#fff' }}>
                {tg.toUpperCase()}
              </div>
            ))}
          </div>
        </Box>
        {t >= 62 && (
          <Box x={120} y={700} w={940} h={130} bg={press ? K.lime : K.ink} press={press}>
            <div style={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', ...PX(36), color: press ? K.ink : K.lime }}>▶ {c.make.toUpperCase()}</div>
          </Box>
        )}
      </>
    );
  } else if (f < B.s3) {
    const t = f - B.s2;
    const picked = t >= 54;
    bg = '#1a1a1c';
    body = (
      <>
        <div style={{ position: 'absolute', left: 120, top: 110, ...PX(30), color: '#8a8a8a' }}>STAGE 02</div>
        <div style={{ position: 'absolute', left: 120, top: 160, ...PX(64), color: '#f7f7f7' }}>{type(c.s2.toUpperCase(), t, 1.4)}</div>
        {[0, 1, 2].map((r) =>
          [0, 1, 2, 3].map((i) => {
            const on = t >= 8 + r * 6 + i * 3;
            const chosen = r === 1 && i === 1;
            if (!on) return null;
            return (
              <div key={`${r}${i}`} style={{ position: 'absolute', left: 120 + i * 300, top: 300 + r * 200, border: `4px solid ${chosen && picked ? K.lime : '#3a3a3e'}`, opacity: picked && !chosen ? 0.35 : 1 }}>
                <PixelArt kind={(r + i) % 5} t={t - 8 - r * 6 - i * 3} w={272} h={160} cell={8} bg={chosen && picked ? K.lime : '#26262a'} fg={chosen && picked ? K.ink : '#f7f7f7'} ac={chosen && picked ? '#f7f7f7' : K.lime} />
              </div>
            );
          }),
        )}
        {picked && (
          <>
            <div style={{ position: 'absolute', left: 120 + 300 - 60, top: 300 + 200 + 50, ...PX(48), color: K.lime, opacity: blink ? 1 : 0 }}>▶</div>
            <div style={{ position: 'absolute', left: 1360, top: 500, ...PX(36), color: K.lime, lineHeight: 1.6 }}>
              ✓ {c.picked.toUpperCase()}
              <br />
              <span style={{ color: '#f7f7f7', fontSize: 28 }}>{c.s2b.toUpperCase()}</span>
            </div>
          </>
        )}
      </>
    );
  } else if (f < B.res) {
    const t = f - B.s3;
    const p = Math.min(1, Math.max(0, (t - 6) / 44));
    const n = 20;
    const filled = Math.floor(p * n);
    bg = K.lime;
    body = (
      <>
        <div style={{ position: 'absolute', left: 120, top: 110, ...PX(30), color: K.ink, opacity: 0.6 }}>STAGE 03</div>
        <div style={{ position: 'absolute', left: 120, top: 160, ...PX(64), color: K.ink }}>{type(c.s3.toUpperCase(), t, 1.4)}</div>
        <div style={{ position: 'absolute', left: 120, top: 330, ...PX(260), color: K.ink }}>{String(Math.round((filled / n) * 100)).padStart(3, ' ')}%</div>
        <div style={{ position: 'absolute', left: 120, top: 760, display: 'flex', gap: 10 }}>
          {Array.from({ length: n }).map((_, i) => (
            <div key={i} style={{ width: 74, height: 74, border: `4px solid ${K.ink}`, background: i < filled ? K.ink : 'transparent' }} />
          ))}
        </div>
        {filled >= n && <div style={{ position: 'absolute', right: 120, top: 150, ...PX(44), color: K.lime, background: K.ink, padding: '18px 24px' }}>MP4 ✓</div>}
      </>
    );
  } else if (f < B.end) {
    const t = f - B.res;
    body = (
      <>
        <Box x={860} y={180} w={940} h={620} bg={K.ink}>
          <PixelArt kind={1} t={t} w={932} h={612} cell={20} bg={K.ink} fg="#f7f7f7" />
        </Box>
        <div style={{ position: 'absolute', left: 120, top: 360, ...PX(96), color: K.ink, lineHeight: 1.5 }}>
          {type(c.res1.toUpperCase(), t, 1)}
          <br />
          <span style={{ background: K.lime }}>{type(c.res2.toUpperCase(), t - 8, 1)}</span>
        </div>
      </>
    );
  } else {
    const t = f - B.end;
    body = (
      <>
        <div style={{ position: 'absolute', left: 120, top: 220, display: 'flex', alignItems: 'center', gap: 24 }}>
          <svg width="96" height="96" viewBox="0 0 96 96" shapeRendering="crispEdges">
            <rect width="96" height="96" fill={K.ink} />
            <g transform="translate(10 13.2)">
              <path d={LOGO} fill={K.lime} />
            </g>
          </svg>
          <div style={{ ...PX(36), color: K.ink }}>ONEFLOW</div>
        </div>
        <div style={{ position: 'absolute', left: 120, top: 380, ...PX(60), color: K.ink, lineHeight: 1.5 }}>
          {type(c.end1.toUpperCase(), t, 2)}
          <br />
          <span style={{ background: K.lime, padding: '0 10px' }}>{type(c.end2.toUpperCase(), t - 8, 2)}</span>
        </div>
        {t >= 16 && (
          <Box x={120} y={680} w={1100} h={120} bg={K.ink}>
            <div style={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', ...PX(30), color: K.lime }}>
              {blink ? '▶' : ' '} {c.cta.toUpperCase()}
            </div>
          </Box>
        )}
        <div style={{ position: 'absolute', right: 120, top: 240 }}>
          <Box x={-460} y={0} w={460} h={460} bg={K.lime}>
            <PixelArt kind={4} t={t} w={452} h={452} cell={28} bg={K.lime} fg={K.ink} ac="#f7f7f7" />
          </Box>
        </div>
      </>
    );
  }

  return (
    <AbsoluteFill style={{ background: bg, overflow: 'hidden' }}>
      <div style={{ position: 'absolute', inset: 0, backgroundImage: `linear-gradient(${bg === K.ink || bg === '#1a1a1c' ? 'rgba(255,255,255,0.05)' : 'rgba(17,17,17,0.05)'} 2px, transparent 2px), linear-gradient(90deg, ${bg === K.ink || bg === '#1a1a1c' ? 'rgba(255,255,255,0.05)' : 'rgba(17,17,17,0.05)'} 2px, transparent 2px)`, backgroundSize: '32px 32px' }} />
      {body}
    </AbsoluteFill>
  );
};
