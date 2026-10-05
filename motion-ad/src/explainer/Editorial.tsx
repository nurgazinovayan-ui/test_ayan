import { AbsoluteFill, useCurrentFrame } from 'remotion';
import '../fonts';
import { FONT } from '../fonts';
import { ease, mix, mixRect, prog } from '../theme';
import type { Rect } from '../theme';
import { ActivePanel, COPY, EndCopy, IntroTitle, PANEL_H, PANEL_W, ResultClip, THEMES, TL, Rise } from './shared';

/*
 * Variant «Редакционный»: a printed-page layout on a visible 12-column grid. Huge step numerals,
 * thin headlines, a flat panel that slides in register with the columns and hairline callouts that
 * point at the parts of the interface being explained.
 */

const T = THEMES.paper;
const M = 120; // outer margin
const COL = (1920 - 2 * M - 11 * 24) / 12;
const colX = (i: number) => M + i * (COL + 24);
const PANEL: Rect = { x: colX(5), y: 236, w: PANEL_W, h: PANEL_H, r: 34 };
const PLAYER: Rect = { x: colX(1), y: 150, w: colX(11) - colX(1), h: (colX(11) - colX(1)) * 0.5625, r: 28 };
const FINAL: Rect = { x: colX(5) + 60, y: 330, w: 840, h: 840 * 0.5625, r: 24 };

// callouts: label position (absolute) → target point (panel-local)
const NOTES: { lx: number; ly: number; tx: number; ty: number }[][] = [
  [
    { lx: colX(3), ly: 470, tx: 70, ty: 210 },
    { lx: colX(3), ly: 690, tx: 60, ty: 470 },
  ],
  [
    { lx: colX(3), ly: 470, tx: 40, ty: 160 },
    { lx: colX(3), ly: 640, tx: 40, ty: 340 },
  ],
  [
    { lx: colX(3), ly: 560, tx: 60, ty: 380 },
    { lx: colX(3), ly: 760, tx: 60, ty: 610 },
  ],
];

export const EditorialExplainer: React.FC<{ lang?: 'ru' | 'en' }> = ({ lang = 'ru' }) => {
  const f = useCurrentFrame();
  const c = COPY[lang];
  const bounds = [TL.s1, TL.s2, TL.s3, TL.res];
  const step = f < TL.s2 ? 0 : f < TL.s3 ? 1 : 2;

  let player = mixRect(PANEL, PLAYER, prog(f, TL.res, TL.res + 24, ease.inOut));
  if (f >= TL.end) player = mixRect(PLAYER, FINAL, prog(f, TL.end, TL.end + 24, ease.inOut));

  const pageOn = prog(f, TL.s1 - 10, TL.s1 + 8);

  return (
    <AbsoluteFill style={{ fontFamily: FONT, color: T.ink, overflow: 'hidden', background: '#efefec' }}>
      {/* 12-column grid + baseline rules */}
      {Array.from({ length: 12 }).map((_, i) => (
        <div key={i} style={{ position: 'absolute', left: colX(i), top: 0, bottom: 0, width: COL, background: 'rgba(0,0,0,0.018)', borderLeft: '1px solid rgba(0,0,0,0.05)', borderRight: '1px solid rgba(0,0,0,0.05)', transform: `scaleY(${prog(f, i * 1.5, 18 + i * 1.5, ease.out)})`, transformOrigin: 'top' }} />
      ))}
      <div style={{ position: 'absolute', left: M, right: M, top: 96, height: 1, background: T.ink, transform: `scaleX(${prog(f, 4, 30, ease.inOut)})`, transformOrigin: 'left' }} />
      <div style={{ position: 'absolute', left: M, top: 60, fontSize: 18, letterSpacing: '0.14em', textTransform: 'uppercase', opacity: prog(f, 10, 20) }}>ONEFLOW — Motion Engine</div>
      <div style={{ position: 'absolute', right: M, top: 60, fontSize: 18, letterSpacing: '0.14em', textTransform: 'uppercase', color: T.muted, opacity: prog(f, 10, 20), fontVariantNumeric: 'tabular-nums' }}>
        {f < TL.s1 ? '00' : f < TL.res ? `0${step + 1}` : f < TL.end ? '04' : '05'} / 05
      </div>

      <IntroTitle f={f} c={c} color={T.ink} align="left" x={M} y={300} size={150} />

      {/* giant step numeral, rolling between steps */}
      {f >= TL.s1 - 6 && f < TL.res + 10 && (
        <div style={{ position: 'absolute', left: M - 12, top: 640, height: 330, overflow: 'hidden', opacity: pageOn * (1 - prog(f, TL.res - 4, TL.res + 8)) }}>
          <div style={{ transform: `translateY(${-(prog(f, TL.s2 - 6, TL.s2 + 8, ease.inOut) + prog(f, TL.s3 - 6, TL.s3 + 8, ease.inOut)) * 330}px)` }}>
            {['01', '02', '03'].map((n) => (
              <div key={n} style={{ height: 330, fontSize: 330, lineHeight: '330px', fontWeight: 100, letterSpacing: '-0.06em' }}>
                {n}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* headline per step */}
      {[0, 1, 2].map((i) => {
        const a = bounds[i];
        const b = bounds[i + 1];
        if (f < a || f >= b) return null;
        const out = prog(f, b - 12, b - 2, ease.inOut);
        return (
          <div key={i} style={{ position: 'absolute', left: M, top: 170 }}>
            {c.steps[i].map((l, k) => (
              <Rise key={l} p={prog(f, a + 4 + k * 4, a + 22 + k * 4)} out={out}>
                <div style={{ fontSize: 72, fontWeight: 200, lineHeight: 1.1, letterSpacing: '-0.04em', whiteSpace: 'nowrap' }}>{l}</div>
              </Rise>
            ))}
          </div>
        );
      })}

      {/* the panel, sliding in register; masked to its own column span */}
      {f >= TL.s1 - 10 && f < TL.res + 2 && (
        <div style={{ position: 'absolute', left: PANEL.x, top: PANEL.y, width: PANEL_W, height: PANEL_H, overflow: 'hidden', borderRadius: 34 }}>
          {[0, 1, 2].map((i) => {
            const a = bounds[i];
            const b = bounds[i + 1];
            const inP = i === 0 ? prog(f, a - 10, a + 10, ease.out) : prog(f, a - 8, a + 8, ease.inOut);
            const outP = i === 2 ? 0 : prog(f, b - 8, b + 8, ease.inOut);
            if (inP <= 0 || outP >= 1) return null;
            const x = i === 0 ? mix(0, 0, inP) : mix(PANEL_W, 0, inP);
            return (
              <div key={i} style={{ position: 'absolute', inset: 0, transform: `translate(${x - outP * PANEL_W}px, ${i === 0 ? mix(80, 0, inP) : 0}px)`, opacity: i === 0 ? inP : 1 }}>
                <ActivePanel f={f} step={i} T={T} c={c} />
              </div>
            );
          })}
        </div>
      )}

      {/* hairline callouts */}
      {f >= TL.s1 && f < TL.res && (
        <svg width={1920} height={1080} style={{ position: 'absolute', inset: 0, overflow: 'visible' }}>
          {NOTES[step].map((n, k) => {
            const a = bounds[step];
            const b = bounds[step + 1];
            const p = prog(f, a + 30 + k * 10, a + 46 + k * 10, ease.inOut) * (1 - prog(f, b - 10, b - 2));
            const tx = PANEL.x + n.tx;
            const ty = PANEL.y + n.ty;
            const sx = n.lx + 230;
            const len = Math.hypot(tx - sx, ty - n.ly);
            return (
              <g key={k} opacity={p > 0 ? 1 : 0}>
                <line x1={sx} y1={n.ly} x2={tx} y2={ty} stroke={T.ink} strokeWidth={1.5} strokeDasharray={len} strokeDashoffset={len * (1 - p)} />
                <circle cx={tx} cy={ty} r={9 * prog(p, 0.7, 1)} fill="#cdf158" stroke={T.ink} strokeWidth={1.5} />
                <circle cx={sx} cy={n.ly} r={3.5} fill={T.ink} />
                <text x={n.lx} y={n.ly - 14} fontFamily="Geist" fontSize={24} fill={T.ink} opacity={prog(p, 0.3, 0.8)}>
                  {c.notes[step][k]}
                </text>
              </g>
            );
          })}
        </svg>
      )}

      {f >= TL.res && (
        <div style={{ position: 'absolute', left: player.x, top: player.y, width: player.w, height: player.h, borderRadius: player.r, overflow: 'hidden', boxShadow: `0 0 0 1px ${T.panelBorder}` }}>
          <ResultClip t={f - TL.res - 6} w={player.w} h={player.h} c={c} />
        </div>
      )}
      {f >= TL.res + 8 && f < TL.end + 4 && (
        <div style={{ position: 'absolute', left: PLAYER.x, top: 118, fontSize: 22, letterSpacing: '0.1em', textTransform: 'uppercase', opacity: prog(f, TL.res + 16, TL.res + 26) * (1 - prog(f, TL.end - 6, TL.end + 2)) }}>
          ▶ {c.resultTitle}
        </div>
      )}
      <EndCopy f={f} c={c} T={T} x={M} y={300} size={84} />
    </AbsoluteFill>
  );
};
