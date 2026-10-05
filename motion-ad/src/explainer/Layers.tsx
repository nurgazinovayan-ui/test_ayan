import { AbsoluteFill, useCurrentFrame } from 'remotion';
import '../fonts';
import { FONT } from '../fonts';
import { ease, mix, prog } from '../theme';
import { ActivePanel, COPY, EndCopy, IntroTitle, PANEL_H, PANEL_W, ResultClip, StepCaption, THEMES, TL } from './shared';

/*
 * Variant «Слои в 3D»: the pipeline lies on a tilted floor as isometric layers joined by a lime path.
 * For each step the camera glides along the floor and the active panel lifts off and turns to face
 * the viewer; the others stay down in the layout. Light theme of the app.
 */

const T = THEMES.light;
const RX = 56;
const RZ = -36;
const SPACING = 1150;
const PLAYER_W = 1240;
const PLAYER_H = 697.5;

export const LayersExplainer: React.FC<{ lang?: 'ru' | 'en' }> = ({ lang = 'ru' }) => {
  const f = useCurrentFrame();
  const c = COPY[lang];

  // focus along the floor: 0 brief, 1 boards, 2 render, 3 player
  const focus =
    prog(f, TL.s2 - 12, TL.s2 + 12, ease.inOut) +
    prog(f, TL.s3 - 12, TL.s3 + 12, ease.inOut) +
    prog(f, TL.res - 8, TL.res + 18, ease.inOut);
  const lift = (i: number) => {
    const starts = [TL.s1, TL.s2, TL.s3, TL.res];
    const ends = [TL.s2, TL.s3, TL.res, 9999];
    return prog(f, starts[i] - 2, starts[i] + 16, ease.inOut) * (1 - prog(f, ends[i] - 12, ends[i] + 4, ease.inOut));
  };
  const wide = 1 - prog(f, TL.s1 - 16, TL.s1 + 8, ease.inOut);
  const endP = prog(f, TL.end, TL.end + 28, ease.inOut);
  const camX = mix(mix(320, 0, prog(f, TL.res - 8, TL.res + 18, ease.inOut)), 360, endP);
  const camS = mix(1, 0.5, wide) * mix(1, 0.66, endP);
  const camY = mix(0, 170, wide);

  const objects = [0, 1, 2, 3].map((i) => ({ i, x: i * SPACING, k: lift(i) }));

  return (
    <AbsoluteFill style={{ fontFamily: FONT, color: T.ink, overflow: 'hidden', background: 'radial-gradient(120% 90% at 60% 30%, #f3f3f1 0%, #e5e5e5 60%, #dcdcda 100%)' }}>
      <div style={{ position: 'absolute', inset: 0, perspective: 2600, perspectiveOrigin: '50% 45%' }}>
        <div
          style={{
            position: 'absolute',
            left: 960 + camX,
            top: 560 + camY,
            width: 0,
            height: 0,
            transformStyle: 'preserve-3d',
            transform: `scale(${camS}) rotateX(${RX}deg) rotateZ(${RZ}deg) translate3d(${-focus * SPACING}px, 0, 0)`,
          }}
        >
          {/* floor: dotted grid + lime path that grows with the steps */}
          <div
            style={{
              position: 'absolute',
              left: -1400,
              top: -1400,
              width: 6400,
              height: 2800,
              backgroundImage: 'radial-gradient(circle, rgba(43,43,43,0.16) 1.6px, transparent 2px)',
              backgroundSize: '44px 44px',
              maskImage: 'radial-gradient(closest-side, #000 40%, transparent)',
              WebkitMaskImage: 'radial-gradient(closest-side, #000 40%, transparent)',
            }}
          />
          <div
            style={{
              position: 'absolute',
              left: 0,
              top: -6,
              height: 12,
              borderRadius: 6,
              width: Math.max(0, mix(0, 3 * SPACING, prog(f, TL.s1, TL.res + 18, (x) => x))),
              background: '#cdf158',
              boxShadow: '0 0 30px rgba(205,241,88,0.9)',
            }}
          />
          {objects.map(({ i, x, k }) => {
            const isPlayer = i === 3;
            const w = isPlayer ? PLAYER_W : PANEL_W;
            const h = isPlayer ? PLAYER_H : PANEL_H;
            if (isPlayer && f < TL.s3) return null;
            return (
              <div key={i} style={{ position: 'absolute', left: 0, top: 0, transformStyle: 'preserve-3d' }}>
                {/* contact shadow on the floor */}
                <div
                  style={{
                    position: 'absolute',
                    left: x - w / 2,
                    top: -h / 2,
                    width: w,
                    height: h,
                    borderRadius: 40,
                    background: 'rgba(30,35,10,0.28)',
                    filter: `blur(${20 + 50 * k}px)`,
                    opacity: mix(0.7, 0.35, k),
                    transform: `translate(${30 + 60 * k}px, ${30 + 60 * k}px)`,
                  }}
                />
                <div
                  style={{
                    position: 'absolute',
                    left: x - w / 2,
                    top: -h / 2,
                    width: w,
                    height: h,
                    transformStyle: 'preserve-3d',
                    transform: `rotateZ(${-RZ * k}deg) rotateX(${-RX * k}deg) translateZ(${mix(8, 230, k)}px)`,
                    borderRadius: 34,
                    boxShadow: `0 ${60 * k}px ${120 * k}px -40px rgba(30,35,10,${0.4 * k})`,
                  }}
                >
                  {isPlayer ? (
                    <div style={{ position: 'absolute', inset: 0, borderRadius: 34, overflow: 'hidden', background: '#f7f7f7', boxShadow: 'inset 0 0 0 1px #fff' }}>
                      <ResultClip t={f - TL.res - 6} w={w} h={h} c={c} />
                    </div>
                  ) : (
                    <ActivePanel f={f} step={i} T={T} c={c} cursor={k > 0.7} />
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      <IntroTitle f={f} c={c} color={T.ink} y={110} size={112} />
      <StepCaption f={f} c={c} color={T.ink} muted={T.muted} x={120} y={400} size={64} />
      <EndCopy f={f} c={c} T={T} x={120} y={300} size={80} />
    </AbsoluteFill>
  );
};
