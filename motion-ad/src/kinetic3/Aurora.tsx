import type { ReactNode } from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';
import '../fonts';
import { FONT } from '../fonts';
import { ease, mix, prog } from '../theme';
import { LOGO } from '../explainer/shared';
import { B, COPY, Comp, K, W } from '../kinetic/KineticAd';

/*
 * «Аврора»: near-black stage lit by slow, blurred light fields (lime, mint, ice). Thin white type
 * that resolves out of blur, gradient-filled key words, frosted glass chips. Calm and luminous.
 */

const INK = '#f4f6f2';
const DIM = 'rgba(244,246,242,0.55)';
const GRAD = 'linear-gradient(100deg, #cdf158 0%, #7ef0c5 55%, #bfe3ff 100%)';

const Blur: React.FC<{ p: number; children: ReactNode }> = ({ p, children }) => (
  <span style={{ display: 'inline-block', opacity: p, filter: `blur(${(1 - p) * 22}px)`, transform: `translateY(${mix(30, 0, p)}px) scale(${mix(1.06, 1, p)})` }}>{children}</span>
);

const Grad: React.FC<{ children: ReactNode }> = ({ children }) => (
  <span style={{ backgroundImage: GRAD, WebkitBackgroundClip: 'text', backgroundClip: 'text', color: 'transparent' }}>{children}</span>
);

const Glass: React.FC<{ x: number; y: number; w: number; h: number; p: number; children?: ReactNode; r?: number; glow?: number }> = ({ x, y, w, h, p, children, r = 32, glow = 0 }) => (
  <div
    style={{
      position: 'absolute',
      left: x,
      top: y,
      width: w,
      height: h,
      borderRadius: r,
      background: 'rgba(255,255,255,0.06)',
      backdropFilter: 'blur(24px) saturate(1.4)',
      boxShadow: `inset 0 0 0 1px rgba(255,255,255,0.14), 0 0 ${80 * glow}px rgba(205,241,88,${0.5 * glow})`,
      opacity: p,
      transform: `translateY(${mix(40, 0, p)}px)`,
      overflow: 'hidden',
    }}
  >
    {children}
  </div>
);

export const AuroraKinetic: React.FC<{ lang?: 'ru' | 'en' }> = ({ lang = 'ru' }) => {
  const f = useCurrentFrame();
  const c = COPY[lang];
  let body: ReactNode;

  // light fields drift continuously; each beat nudges their centre
  const beatShift = interpolate(f, [0, B.motion, B.s1, B.s2, B.s3, B.res, B.end, 450], [0, 1, 0.3, 0.8, 0.5, 1, 0.2, 0.3], { easing: ease.inOut });
  const blobs = [
    { x: 1300 + Math.sin(f / 50) * 160 - beatShift * 300, y: 260 + Math.cos(f / 60) * 90, s: 900, c: 'rgba(205,241,88,0.55)' },
    { x: 500 + Math.cos(f / 55) * 200 + beatShift * 200, y: 800 + Math.sin(f / 45) * 80, s: 1000, c: 'rgba(126,240,197,0.42)' },
    { x: 1600 + Math.sin(f / 40) * 120, y: 900 - beatShift * 200, s: 700, c: 'rgba(191,227,255,0.35)' },
  ];

  if (f < B.motion) {
    body = (
      <div style={{ position: 'absolute', left: 0, right: 0, top: 250, textAlign: 'center', fontSize: 150, lineHeight: 1.08, letterSpacing: '-0.045em', color: INK }}>
        {c.open.map((l, i) => (
          <div key={l} style={W(i === 2 ? 600 : 200)}>
            <Blur p={prog(f, i * 8, i * 8 + 14, ease.out)}>{i === 2 ? <Grad>{l}</Grad> : l}</Blur>
          </div>
        ))}
      </div>
    );
  } else if (f < B.s1) {
    const t = f - B.motion;
    body = (
      <>
        <div style={{ position: 'absolute', left: 0, right: 0, top: 270, textAlign: 'center', fontSize: 300, lineHeight: 0.95, letterSpacing: '-0.06em', color: INK }}>
          <div style={W(700)}>
            <Blur p={prog(t, 0, 16, ease.out)}>
              <Grad>Motion</Grad>
            </Blur>
          </div>
          <div style={W(150)}>
            <Blur p={prog(t, 6, 22, ease.out)}>Engine</Blur>
          </div>
        </div>
        <div style={{ position: 'absolute', left: 0, right: 0, top: 200, textAlign: 'center', fontSize: 24, letterSpacing: '0.5em', color: DIM, opacity: prog(t, 14, 24) }}>ONEFLOW</div>
      </>
    );
  } else if (f < B.s2) {
    const t = f - B.s1;
    const typed = Math.floor(interpolate(t, [34, 62], [0, c.tags.length], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }));
    const press = t > 72 && t < 82 ? 1 : 0;
    body = (
      <>
        <div style={{ position: 'absolute', left: 140, top: 150, color: INK }}>
          <div style={{ fontSize: 24, letterSpacing: '0.3em', color: DIM, opacity: prog(t, 0, 10) }}>01</div>
          <div style={{ marginTop: 18, fontSize: 120, lineHeight: 1, letterSpacing: '-0.05em', ...W(200) }}>
            <Blur p={prog(t, 2, 18, ease.out)}>{c.s1a}</Blur> <Blur p={prog(t, 8, 24, ease.out)}><Grad><b style={W(600)}>{c.s1b}</b></Grad></Blur>
          </div>
        </div>
        {[0, 3, 1].map((k, i) => (
          <Glass key={i} x={140 + i * 330} y={420} w={300} h={300} p={prog(t, 8 + i * 5, 22 + i * 5, ease.out)}>
            <Comp kind={k} t={t - 12 - i * 5} w={300} h={300} bg="rgba(0,0,0,0)" fg={INK} ac={K.lime} r={0} />
          </Glass>
        ))}
        <Glass x={1180} y={420} w={600} h={300} p={prog(t, 30, 40, ease.out)}>
          <div style={{ position: 'absolute', left: 36, top: 30, fontSize: 24, color: DIM }}>{c.s1c}</div>
          <div style={{ position: 'absolute', left: 36, top: 84, right: 30, display: 'flex', flexWrap: 'wrap', gap: 12 }}>
            {c.tags.slice(0, typed).map((tg, k) => (
              <div key={tg} style={{ padding: '10px 22px', borderRadius: 99, background: k === 0 ? K.lime : 'rgba(255,255,255,0.1)', color: k === 0 ? K.ink : INK, fontSize: 30, ...W(500) }}>
                {tg}
              </div>
            ))}
          </div>
        </Glass>
        <div style={{ position: 'absolute', left: 140, top: 790, padding: '24px 44px', borderRadius: 99, background: GRAD, color: K.ink, fontSize: 34, ...W(600), opacity: prog(t, 62, 70), transform: `scale(${press ? 0.95 : 1})`, boxShadow: `0 0 ${press ? 80 : 30}px rgba(205,241,88,0.6)` }}>
          {c.make} →
        </div>
      </>
    );
  } else if (f < B.s3) {
    const t = f - B.s2;
    const pick = prog(t, 50, 60, ease.out);
    body = (
      <>
        <div style={{ position: 'absolute', left: 140, top: 130, color: INK }}>
          <div style={{ fontSize: 24, letterSpacing: '0.3em', color: DIM }}>02</div>
          <div style={{ marginTop: 18, fontSize: 110, lineHeight: 1, letterSpacing: '-0.05em', ...W(200) }}>
            <Blur p={prog(t, 2, 18, ease.out)}>{c.s2}</Blur>
          </div>
        </div>
        {[0, 1, 2].map((r) =>
          [0, 1, 2, 3].map((i) => {
            const chosen = r === 1;
            return (
              <Glass key={`${r}${i}`} x={140 + i * 300} y={340 + r * 190} w={276} h={160} p={prog(t, 8 + r * 5 + i * 3, 20 + r * 5 + i * 3, ease.out) * (chosen ? 1 : mix(1, 0.35, pick))} r={20} glow={chosen ? pick : 0}>
                <Comp kind={(r * 2 + i) % 5} t={t - 10 - r * 5 - i * 3} w={276} h={160} bg="rgba(0,0,0,0)" fg={INK} ac={K.lime} r={0} />
              </Glass>
            );
          }),
        )}
        <div style={{ position: 'absolute', left: 1400, top: 520, fontSize: 70, lineHeight: 1.05, letterSpacing: '-0.04em', color: INK, ...W(300) }}>
          <Blur p={pick}>
            <Grad>{c.s2b}</Grad>
          </Blur>
        </div>
      </>
    );
  } else if (f < B.res) {
    const t = f - B.s3;
    const p = prog(t, 6, 50, ease.soft);
    body = (
      <>
        <div style={{ position: 'absolute', left: 140, top: 130, fontSize: 24, letterSpacing: '0.3em', color: DIM }}>03 · {c.s3.toUpperCase()}</div>
        <div style={{ position: 'absolute', left: 0, right: 0, top: 200, textAlign: 'center', fontSize: 460, lineHeight: 1, letterSpacing: '-0.07em', fontVariantNumeric: 'tabular-nums', ...W(mix(100, 700, p)) }}>
          <Grad>{Math.round(p * 100)}</Grad>
          <span style={{ color: DIM, fontSize: 200, ...W(100) }}>%</span>
        </div>
        <div style={{ position: 'absolute', left: 360, right: 360, top: 780, height: 4, borderRadius: 4, background: 'rgba(255,255,255,0.12)' }}>
          <div style={{ width: `${p * 100}%`, height: 4, borderRadius: 4, background: GRAD, boxShadow: '0 0 30px rgba(205,241,88,0.8)' }} />
        </div>
        <div style={{ position: 'absolute', left: 0, right: 0, top: 830, textAlign: 'center', fontSize: 36, color: INK, opacity: prog(t, 50, 58), ...W(400) }}>MP4 · ✓ {c.done}</div>
      </>
    );
  } else if (f < B.end) {
    const t = f - B.res;
    body = (
      <>
        <Glass x={900} y={200} w={880} h={600} p={prog(t, 0, 14, ease.out)} glow={0.6}>
          <Comp kind={1} t={t - 4} w={880} h={600} bg="rgba(0,0,0,0)" fg={INK} ac={K.lime} r={0} />
        </Glass>
        <div style={{ position: 'absolute', left: 140, top: 330, fontSize: 190, lineHeight: 1, letterSpacing: '-0.055em', color: INK }}>
          <div style={W(200)}>
            <Blur p={prog(t, 4, 20, ease.out)}>{c.res1}</Blur>
          </div>
          <div style={W(700)}>
            <Blur p={prog(t, 10, 26, ease.out)}>
              <Grad>{c.res2}</Grad>
            </Blur>
          </div>
        </div>
      </>
    );
  } else {
    const t = f - B.end;
    body = (
      <div style={{ position: 'absolute', left: 0, right: 0, top: 260, textAlign: 'center', color: INK }}>
        <div style={{ display: 'inline-flex', alignItems: 'center', gap: 16, opacity: prog(t, 0, 12) }}>
          <svg width="64" height="64" viewBox="0 0 96 96">
            <rect width="96" height="96" rx="22" fill="rgba(255,255,255,0.12)" />
            <g transform="translate(10 13.2)">
              <path d={LOGO} fill={INK} />
            </g>
          </svg>
          <span style={{ fontSize: 34, ...W(600) }}>ONEFLOW</span>
          <span style={{ fontSize: 34, color: DIM, ...W(300) }}>Motion Engine</span>
        </div>
        <div style={{ marginTop: 40, fontSize: 120, lineHeight: 1.04, letterSpacing: '-0.05em' }}>
          <div style={W(200)}>
            <Blur p={prog(t, 4, 18, ease.out)}>{c.end1}</Blur>
          </div>
          <div style={W(650)}>
            <Blur p={prog(t, 8, 22, ease.out)}>
              <Grad>{c.end2}</Grad>
            </Blur>
          </div>
        </div>
        <div style={{ marginTop: 50, display: 'inline-block', padding: '24px 48px', borderRadius: 99, background: GRAD, color: K.ink, fontSize: 32, ...W(600), opacity: prog(t, 14, 24) }}>{c.cta} →</div>
      </div>
    );
  }

  return (
    <AbsoluteFill style={{ background: '#060708', fontFamily: FONT, overflow: 'hidden' }}>
      {blobs.map((b, i) => (
        <div key={i} style={{ position: 'absolute', left: b.x - b.s / 2, top: b.y - b.s / 2, width: b.s, height: b.s, borderRadius: '50%', background: `radial-gradient(closest-side, ${b.c}, transparent)`, filter: 'blur(40px)' }} />
      ))}
      {body}
      {/* grain */}
      <svg width={1920} height={1080} style={{ position: 'absolute', inset: 0, mixBlendMode: 'overlay', opacity: 0.4 }}>
        <filter id={`ag${Math.floor(f / 2) % 12}`}>
          <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed={Math.floor(f / 2) % 12} />
          <feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.18 0" />
        </filter>
        <rect width={1920} height={1080} filter={`url(#ag${Math.floor(f / 2) % 12})`} />
      </svg>
    </AbsoluteFill>
  );
};
