import { AbsoluteFill, useCurrentFrame } from 'remotion';
import '../fonts';
import { FONT } from '../fonts';
import { ease, mix, prog } from '../theme';
import { ActivePanel, COPY, EndCopy, IntroTitle, PANEL_H, PANEL_W, ResultClip, StepCaption, THEMES, TL } from './shared';

/*
 * Variant «Ночной кинематограф»: letterboxed 2.39:1, near-black set lit by lime. The panels hang in a
 * row like screens in a gallery; the camera trucks sideways from one to the next with parallax light
 * in the foreground, inactive screens turn away into the dark.
 */

const T = THEMES.night;
const GAP = 1500;
const BAR = 118;

export const NightExplainer: React.FC<{ lang?: 'ru' | 'en' }> = ({ lang = 'ru' }) => {
  const f = useCurrentFrame();
  const c = COPY[lang];

  // camera position along the row of screens (0 = brief, 1 = boards, 2 = render, 3 = player)
  const pos =
    prog(f, TL.s2 - 10, TL.s2 + 14, ease.inOut) +
    prog(f, TL.s3 - 10, TL.s3 + 14, ease.inOut) +
    prog(f, TL.res - 6, TL.res + 20, ease.inOut);
  const camX = -pos * GAP;
  const intro = 1 - prog(f, TL.s1 - 14, TL.s1 + 10, ease.inOut);
  const push = mix(1, 1.04, (f % 90) / 90) * (1 - intro * 0.25);
  const endP = prog(f, TL.end, TL.end + 28, ease.inOut);

  const screen = (i: number) => {
    const d = i - pos;
    const focus = Math.max(0, 1 - Math.abs(d));
    return { d, focus, x: 880 + i * GAP + camX, rotY: -d * 22, o: mix(0.25, 1, focus) };
  };

  // player (4th screen) becomes the right half of the end card
  const pl = screen(3);
  const PW = mix(1320, 800, endP);
  const PH = PW * 0.5625;
  const plX = mix(pl.x - 580, 1010, endP);
  const plY = mix(1080 / 2 - PH / 2, 320, endP);

  return (
    <AbsoluteFill style={{ fontFamily: FONT, color: T.ink, overflow: 'hidden', background: '#09090a' }}>
      {/* rim light + slow beam */}
      <div style={{ position: 'absolute', left: 900, top: 120, width: 1100, height: 900, borderRadius: '50%', background: 'radial-gradient(closest-side, rgba(205,241,88,0.22), transparent)' }} />
      <div
        style={{
          position: 'absolute',
          left: -600 + ((f * 6) % 3200),
          top: -200,
          width: 380,
          height: 1500,
          transform: 'rotate(18deg)',
          background: 'linear-gradient(90deg, transparent, rgba(205,241,88,0.07), transparent)',
        }}
      />

      <div style={{ position: 'absolute', inset: 0, transform: `scale(${push})`, transformOrigin: '1300px 540px', perspective: 2200 }}>
        {[0, 1, 2].map((i) => {
          const s = screen(i);
          if (Math.abs(s.d) > 1.6) return null;
          return (
            <div
              key={i}
              style={{
                position: 'absolute',
                left: s.x,
                top: 1080 / 2 - PANEL_H / 2 + 20,
                width: PANEL_W,
                height: PANEL_H,
                opacity: s.o * (1 - intro * 0.6),
                transform: `rotateY(${s.rotY}deg) scale(${mix(0.88, 1, s.focus)})`,
                filter: `blur(${(1 - s.focus) * 6}px)`,
                borderRadius: 34,
                boxShadow: `0 0 ${120 * s.focus}px -30px rgba(205,241,88,${0.55 * s.focus}), 0 40px 90px -30px rgba(0,0,0,0.9)`,
                backdropFilter: 'blur(20px)',
              }}
            >
              <ActivePanel f={f} step={i} T={T} c={c} cursor={s.focus > 0.6} />
            </div>
          );
        })}
      </div>

      {f >= TL.res - 12 && (
        <div
          style={{
            position: 'absolute',
            left: plX,
            top: plY,
            width: PW,
            height: PH,
            borderRadius: 30,
            overflow: 'hidden',
            boxShadow: '0 0 160px -30px rgba(205,241,88,0.6), 0 0 0 1px rgba(255,255,255,0.12)',
          }}
        >
          <ResultClip t={f - TL.res - 4} w={PW} h={PH} c={c} />
        </div>
      )}

      {/* foreground parallax orbs */}
      {[0, 1, 2, 3].map((k) => (
        <div
          key={k}
          style={{
            position: 'absolute',
            left: 300 + k * 900 + camX * 1.35,
            top: [760, 120, 820, 200][k],
            width: 220,
            height: 220,
            borderRadius: '50%',
            background: 'radial-gradient(closest-side, rgba(205,241,88,0.35), transparent)',
            filter: 'blur(14px)',
          }}
        />
      ))}

      <IntroTitle f={f} c={c} color={T.ink} y={360} size={120} marker="rgba(205,241,88,0.45)" />
      <StepCaption f={f} c={c} color={T.ink} muted={T.muted} x={140} y={400} size={64} />
      {f >= TL.res + 8 && f < TL.end + 6 && (
        <div style={{ position: 'absolute', left: 300, top: BAR + 22, fontSize: 24, color: T.muted, opacity: prog(f, TL.res + 18, TL.res + 28) * (1 - prog(f, TL.end - 6, TL.end + 4)) }}>
          ▶ {c.resultTitle}
        </div>
      )}
      <EndCopy f={f} c={c} T={T} x={140} y={320} size={80} />

      {/* letterbox */}
      <div style={{ position: 'absolute', left: 0, right: 0, top: 0, height: BAR, background: '#000' }} />
      <div style={{ position: 'absolute', left: 0, right: 0, bottom: 0, height: BAR, background: '#000' }} />
    </AbsoluteFill>
  );
};
