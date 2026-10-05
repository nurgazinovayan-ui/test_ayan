import { AbsoluteFill, useCurrentFrame } from 'remotion';
import '../fonts';
import { FONT } from '../fonts';
import { ease, mix, mixRect, prog } from '../theme';
import type { Rect } from '../theme';
import { ProductShot } from '../light/Product';
import { ActivePanel, COPY, EndCopy, IntroTitle, PANEL_H, PANEL_W, ResultClip, StepCaption, THEMES, TL } from './shared';

/*
 * Variant «Стекло и свет»: frosted-glass panels over a soft studio gradient with drifting light and a
 * huge out-of-focus product behind. Steps change with a rack focus: the old panel falls back out of
 * focus, the next one comes forward into it.
 */

const T = THEMES.glass;
const PANEL: Rect = { x: 880, y: 220, w: PANEL_W, h: PANEL_H, r: 34 };
const PLAYER: Rect = { x: 300, y: 150, w: 1320, h: 742.5, r: 36 };
const FINAL: Rect = { x: 1010, y: 300, w: 780, h: 438.75, r: 30 };

export const GlassExplainer: React.FC<{ lang?: 'ru' | 'en' }> = ({ lang = 'ru' }) => {
  const f = useCurrentFrame();
  const c = COPY[lang];

  // rack focus between steps
  const bounds = [TL.s1, TL.s2, TL.s3, TL.res];
  const panels = [0, 1, 2].map((i) => {
    const a = bounds[i];
    const b = bounds[i + 1];
    const inP = prog(f, a - 4, a + 14, ease.out);
    const outP = i === 2 ? 0 : prog(f, b - 10, b + 8, ease.inOut);
    if (f < a - 4 || (i < 2 && f > b + 8) || (i === 2 && f >= TL.res + 2)) return null;
    const s = mix(1.12, 1, inP) * mix(1, 0.84, outP);
    const blur = 16 * (1 - inP) + 14 * outP;
    const o = inP * (1 - outP);
    return { i, s, blur, o, y: -30 * outP };
  });

  // render panel → player → end card
  let player = mixRect(PANEL, PLAYER, prog(f, TL.res, TL.res + 26, ease.inOut));
  if (f >= TL.end) player = mixRect(PLAYER, FINAL, prog(f, TL.end, TL.end + 26, ease.inOut));
  const clipOn = prog(f, TL.res, TL.res + 10);

  const drift = (k: number) => Math.sin(f / (60 + k * 13)) * 40;

  return (
    <AbsoluteFill style={{ fontFamily: FONT, color: T.ink, overflow: 'hidden', background: 'linear-gradient(160deg, #f2f2f0 0%, #e4e4e1 55%, #d9dad4 100%)' }}>
      {/* light + big defocused product */}
      <div style={{ position: 'absolute', left: 1100 + drift(1), top: -260, width: 1000, height: 900, borderRadius: '50%', background: 'radial-gradient(closest-side, rgba(205,241,88,0.55), transparent)', filter: 'blur(20px)' }} />
      <div style={{ position: 'absolute', left: -300 + drift(2), top: 500, width: 1100, height: 900, borderRadius: '50%', background: 'radial-gradient(closest-side, rgba(255,255,255,0.95), transparent)' }} />
      <div style={{ position: 'absolute', left: 1180 - f * 0.4, top: 40, width: 760, height: 1080, filter: 'blur(26px)', opacity: 0.55 }}>
        <ProductShot shot={{ bg: ['rgba(0,0,0,0)', 'rgba(0,0,0,0)'], x: 0.5, y: 0.96, size: 0.95, table: false }} w={760} h={1080} id="gbig" />
      </div>
      <div style={{ position: 'absolute', left: 980 + drift(3), top: 640, width: 520, height: 520, borderRadius: '50%', background: 'radial-gradient(closest-side, rgba(205,241,88,0.45), transparent)', filter: 'blur(10px)' }} />

      <IntroTitle f={f} c={c} color={T.ink} y={330} />
      <StepCaption f={f} c={c} color={T.ink} muted={T.muted} x={140} y={390} />

      {panels.map(
        (p) =>
          p && (
            <div
              key={p.i}
              style={{
                position: 'absolute',
                left: PANEL.x,
                top: PANEL.y + p.y,
                width: PANEL_W,
                height: PANEL_H,
                opacity: p.o,
                transform: `scale(${p.s})`,
                filter: p.blur > 0.3 ? `blur(${p.blur}px)` : undefined,
                borderRadius: 34,
                backdropFilter: 'blur(30px) saturate(1.5)',
                WebkitBackdropFilter: 'blur(30px) saturate(1.5)',
                boxShadow: '0 50px 100px -40px rgba(40,50,10,0.35), 0 1px 0 rgba(255,255,255,0.9) inset',
              }}
            >
              <ActivePanel f={f} step={p.i} T={T} c={c} />
            </div>
          ),
      )}

      {f >= TL.res && (
        <div
          style={{
            position: 'absolute',
            left: player.x,
            top: player.y,
            width: player.w,
            height: player.h,
            borderRadius: player.r,
            padding: 12,
            boxSizing: 'border-box',
            background: 'rgba(255,255,255,0.45)',
            backdropFilter: 'blur(30px) saturate(1.5)',
            boxShadow: '0 60px 120px -50px rgba(40,50,10,0.45), inset 0 0 0 1px rgba(255,255,255,0.85)',
          }}
        >
          <div style={{ position: 'relative', width: '100%', height: '100%', borderRadius: player.r - 10, overflow: 'hidden', opacity: clipOn }}>
            <ResultClip t={f - TL.res - 6} w={player.w - 24} h={player.h - 24} c={c} />
          </div>
        </div>
      )}
      {f >= TL.res + 8 && f < TL.end + 6 && (
        <div style={{ position: 'absolute', left: PLAYER.x, top: PLAYER.y - 58, fontSize: 24, color: T.muted, opacity: prog(f, TL.res + 14, TL.res + 24) * (1 - prog(f, TL.end - 6, TL.end + 4)) }}>
          ▶ {c.resultTitle}
        </div>
      )}
      <EndCopy f={f} c={c} T={T} x={140} y={300} size={86} />
    </AbsoluteFill>
  );
};
