import type { CSSProperties, ReactNode } from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame } from 'remotion';
import '../fonts';
import { FONT } from '../fonts';
import { ease, mix, prog } from '../theme';
import { LOGO } from '../explainer/shared';
import { B, COPY, Comp, K, W } from '../kinetic/KineticAd';

/*
 * «Необрутализм»: flat colour, 5 px black outlines, hard offset shadows, sticker-like cards set at
 * small fixed tilts, chunky type. Things slam in with overshoot; buttons press down into their shadow.
 */

const PAPER = '#f3f2ea';
const LINE = 5;
const SH = 12;

const pop = (f: number, at: number) => spring({ frame: f - at, fps: 30, config: { damping: 9, stiffness: 160, mass: 0.8 } });

const Card: React.FC<{ x: number; y: number; w: number; h: number; bg?: string; tilt?: number; p: number; press?: number; children?: ReactNode; style?: CSSProperties; r?: number }> = ({
  x,
  y,
  w,
  h,
  bg = '#fff',
  tilt = 0,
  p,
  press = 0,
  children,
  style,
  r = 22,
}) => (
  <div
    style={{
      position: 'absolute',
      left: x + press * SH * 0.8,
      top: y + press * SH * 0.8,
      width: w,
      height: h,
      background: bg,
      border: `${LINE}px solid ${K.ink}`,
      borderRadius: r,
      boxShadow: `${SH * (1 - press * 0.8)}px ${SH * (1 - press * 0.8)}px 0 ${K.ink}`,
      transform: `rotate(${tilt}deg) scale(${p})`,
      overflow: 'hidden',
      ...style,
    }}
  >
    {children}
  </div>
);

const Sticker: React.FC<{ x: number; y: number; p: number; text: string; bg?: string; tilt?: number; size?: number }> = ({ x, y, p, text, bg = K.lime, tilt = -8, size = 40 }) => (
  <div style={{ position: 'absolute', left: x, top: y, padding: '14px 28px', background: bg, border: `${LINE}px solid ${K.ink}`, borderRadius: 999, boxShadow: `6px 6px 0 ${K.ink}`, transform: `rotate(${tilt}deg) scale(${p})`, fontSize: size, letterSpacing: '-0.02em', whiteSpace: 'nowrap', ...W(800) }}>{text}</div>
);

const Star: React.FC<{ x: number; y: number; s: number; rot: number; color?: string }> = ({ x, y, s, rot, color = K.lime }) => {
  const pts = Array.from({ length: 16 })
    .map((_, i) => {
      const a = (i / 16) * Math.PI * 2;
      const r = i % 2 ? 0.62 : 1;
      return `${50 + Math.cos(a) * 50 * r},${50 + Math.sin(a) * 50 * r}`;
    })
    .join(' ');
  return (
    <svg width={160 * s} height={160 * s} viewBox="-6 -6 112 112" style={{ position: 'absolute', left: x, top: y, transform: `rotate(${rot}deg)` }}>
      <polygon points={pts} fill={color} stroke={K.ink} strokeWidth={5} strokeLinejoin="round" />
    </svg>
  );
};

const Head: React.FC<{ f: number; at: number; children: ReactNode; size?: number; x?: number; y?: number; color?: string }> = ({ f, at, children, size = 150, x = 110, y = 90, color = K.ink }) => (
  <div style={{ position: 'absolute', left: x, top: y, fontSize: size, lineHeight: 0.92, letterSpacing: '-0.05em', color, ...W(900), transform: `translateY(${mix(-200, 0, pop(f, at))}px)`, opacity: prog(f, at, at + 3) }}>{children}</div>
);

export const BrutalKinetic: React.FC<{ lang?: 'ru' | 'en' }> = ({ lang = 'ru' }) => {
  const f = useCurrentFrame();
  const c = COPY[lang];
  let body: ReactNode;
  let bg = PAPER;

  if (f < B.motion) {
    body = (
      <>
        {c.open.map((l, i) => (
          <Card key={l} x={130 + i * 90} y={150 + i * 250} w={i === 2 ? 1180 : 1000} h={210} bg={i === 2 ? K.lime : '#fff'} tilt={[-2, 1.5, -1][i]} p={pop(f, i * 8)}>
            <div style={{ position: 'absolute', left: 50, top: 22, fontSize: 140, lineHeight: 1, letterSpacing: '-0.05em', ...W(i === 2 ? 900 : 600) }}>{l}</div>
          </Card>
        ))}
        <Star x={1460} y={140} s={1.6} rot={f * 3} />
      </>
    );
  } else if (f < B.s1) {
    const t = f - B.motion;
    bg = K.lime;
    body = (
      <>
        <Card x={150} y={180} w={1620} h={330} bg={K.ink} tilt={-1.5} p={pop(t, 0)}>
          <div style={{ position: 'absolute', left: 60, top: 10, fontSize: 300, lineHeight: 1, letterSpacing: '-0.06em', color: K.lime, ...W(900) }}>MOTION</div>
        </Card>
        <Card x={520} y={560} w={1100} h={300} bg="#fff" tilt={2} p={pop(t, 6)}>
          <div style={{ position: 'absolute', left: 60, top: 14, fontSize: 250, lineHeight: 1, letterSpacing: '-0.06em', ...W(900) }}>ENGINE</div>
        </Card>
        <Sticker x={140} y={620} p={pop(t, 14)} text="ONEFLOW" bg="#fff" tilt={-10} size={48} />
        <Star x={1600} y={40} s={1.2} rot={f * 4} color="#fff" />
      </>
    );
  } else if (f < B.s2) {
    const t = f - B.s1;
    const typed = Math.floor(interpolate(t, [36, 62], [0, c.tags.length], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }));
    const press = t < 72 ? 0 : t < 76 ? prog(t, 72, 76) : 1 - prog(t, 78, 86);
    body = (
      <>
        <Head f={t} at={0} size={110}>
          01 {c.s1a}
          <br />
          <span style={W(500)}>{c.s1b}</span>
        </Head>
        {[0, 3, 1].map((k, i) => (
          <Card key={i} x={1000 + i * 300} y={110 + (i % 2) * 60} w={260} h={300} bg={i === 1 ? K.ink : '#fff'} tilt={[-4, 3, -2][i]} p={pop(t, 6 + i * 5)}>
            <Comp kind={k} t={t - 10 - i * 5} w={250} h={290} bg={i === 1 ? K.ink : '#fff'} fg={i === 1 ? '#fff' : K.ink} ac={K.lime} r={0} />
          </Card>
        ))}
        <Card x={110} y={520} w={1180} h={230} bg="#fff" tilt={0} p={pop(t, 30)}>
          <div style={{ position: 'absolute', left: 36, top: 26, fontSize: 28, color: K.mid, ...W(700) }}>{c.s1c.toUpperCase()}</div>
          <div style={{ position: 'absolute', left: 36, top: 84, display: 'flex', gap: 16, flexWrap: 'wrap', width: 1100 }}>
            {c.tags.slice(0, typed).map((tg, k) => (
              <div key={tg} style={{ padding: '10px 24px', borderRadius: 99, border: `4px solid ${K.ink}`, background: k % 2 ? '#fff' : K.lime, fontSize: 38, ...W(700), transform: `rotate(${[-3, 2, -1, 3][k]}deg)` }}>
                {tg}
              </div>
            ))}
          </div>
        </Card>
        <Card x={1320} y={570} w={520} h={140} bg={K.ink} p={pop(t, 62)} press={press} r={999}>
          <div style={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', color: K.lime, fontSize: 30, ...W(800), textAlign: 'center', lineHeight: 1.1, padding: '0 24px', whiteSpace: 'nowrap' }}>{c.make} →</div>
        </Card>
        {t > 76 && <Star x={1700} y={480} s={0.8 * pop(t, 76)} rot={t * 6} />}
      </>
    );
  } else if (f < B.s3) {
    const t = f - B.s2;
    const pick = prog(t, 52, 60, ease.out);
    bg = '#d9d6f5';
    body = (
      <>
        <Head f={t} at={0} size={130}>
          02 {c.s2}
        </Head>
        {[0, 1, 2].map((r) =>
          [0, 1, 2, 3].map((i) => {
            const chosen = r === 1 && i === 2;
            return (
              <Card key={`${r}${i}`} x={110 + i * 330} y={300 + r * 230} w={290} h={190} bg={chosen && pick > 0.5 ? K.lime : '#fff'} tilt={chosen ? mix(0, -4, pick) : 0} p={pop(t, 10 + r * 5 + i * 3) * (chosen ? mix(1, 1.12, pick) : 1)} style={{ opacity: chosen ? 1 : mix(1, 0.45, pick), zIndex: chosen ? 2 : 1 }}>
                <Comp kind={(r + i * 2) % 5} t={t - 12 - r * 5 - i * 3} w={280} h={180} bg={chosen && pick > 0.5 ? K.lime : '#fff'} fg={K.ink} ac={chosen && pick > 0.5 ? '#fff' : K.lime} r={0} />
              </Card>
            );
          }),
        )}
        <Sticker x={1480} y={420} p={pop(t, 54)} text={`✓ ${c.picked}`} tilt={8} size={44} />
        <div style={{ position: 'absolute', left: 1460, top: 580, width: 380, fontSize: 64, lineHeight: 1, letterSpacing: '-0.04em', ...W(800), opacity: prog(t, 56, 60) }}>{c.s2b}</div>
      </>
    );
  } else if (f < B.res) {
    const t = f - B.s3;
    const p = prog(t, 6, 50, ease.soft);
    bg = K.ink;
    body = (
      <>
        <Head f={t} at={0} size={130} color="#fff">
          03 {c.s3}
        </Head>
        <Card x={110} y={320} w={1700} h={200} bg="#fff" p={pop(t, 4)} r={999}>
          <div style={{ position: 'absolute', left: 0, top: 0, bottom: 0, width: `${p * 100}%`, background: `repeating-linear-gradient(-45deg, ${K.lime} 0 40px, #b7dc3c 40px 80px)`, borderRight: p > 0 && p < 1 ? `${LINE}px solid ${K.ink}` : 'none' }} />
        </Card>
        <div style={{ position: 'absolute', left: 110, top: 560, fontSize: 340, lineHeight: 1, letterSpacing: '-0.06em', color: '#fff', fontVariantNumeric: 'tabular-nums', ...W(900) }}>{Math.round(p * 100)}%</div>
        <Sticker x={1250} y={640} p={pop(t, 52)} text="MP4" bg={K.lime} tilt={-10} size={96} />
        <Sticker x={1440} y={820} p={pop(t, 56)} text={`✓ ${c.done}`} bg="#fff" tilt={6} size={52} />
      </>
    );
  } else if (f < B.end) {
    const t = f - B.res;
    bg = K.lime;
    body = (
      <>
        <Card x={820} y={150} w={980} h={560} bg={K.ink} tilt={2} p={pop(t, 0)}>
          <Comp kind={1} t={t - 4} w={970} h={550} bg={K.ink} fg="#fff" ac={K.lime} r={0} />
        </Card>
        <Head f={t} at={4} size={200} y={240}>
          {c.res1}
          <br />
          <span style={W(500)}>{c.res2}</span>
        </Head>
        <Star x={700} y={700} s={1.3} rot={t * 5} color="#fff" />
      </>
    );
  } else {
    const t = f - B.end;
    body = (
      <>
        <Card x={110} y={160} w={1100} h={700} bg="#fff" p={pop(t, 0)} tilt={-1}>
          <div style={{ position: 'absolute', left: 60, top: 60, display: 'flex', alignItems: 'center', gap: 18 }}>
            <svg width="76" height="76" viewBox="0 0 96 96">
              <rect width="96" height="96" rx="22" fill={K.ink} />
              <g transform="translate(10 13.2)">
                <path d={LOGO} fill="#fff" />
              </g>
            </svg>
            <span style={{ fontSize: 40, ...W(800) }}>ONEFLOW</span>
            <span style={{ fontSize: 40, ...W(400) }}>Motion Engine</span>
          </div>
          <div style={{ position: 'absolute', left: 60, top: 230, fontSize: 84, lineHeight: 1.3, letterSpacing: '-0.05em', ...W(900), whiteSpace: 'nowrap' }}>
            {c.end1}
            <br />
            <span style={{ background: K.lime, padding: '0 14px', border: `${LINE}px solid ${K.ink}` }}>{c.end2}</span>
          </div>
        </Card>
        <Card x={1250} y={620} w={620} h={130} bg={K.ink} p={pop(t, 10)} r={999} tilt={-3}>
          <div style={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', color: K.lime, fontSize: 30, ...W(800), textAlign: 'center', padding: '0 24px', whiteSpace: 'nowrap' }}>{c.cta} →</div>
        </Card>
        <Star x={1420} y={170} s={1.8} rot={t * 2} />
      </>
    );
  }

  return (
    <AbsoluteFill style={{ background: bg, fontFamily: FONT, color: K.ink, overflow: 'hidden' }}>
      <div style={{ position: 'absolute', inset: 0, backgroundImage: `radial-gradient(${bg === K.ink ? 'rgba(255,255,255,0.12)' : 'rgba(17,17,17,0.12)'} 2px, transparent 2.5px)`, backgroundSize: '36px 36px' }} />
      {body}
    </AbsoluteFill>
  );
};
