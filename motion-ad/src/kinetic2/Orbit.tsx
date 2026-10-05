import type { ReactNode } from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame } from 'remotion';
import '../fonts';
import { FONT } from '../fonts';
import { ease, mix, prog } from '../theme';
import { LOGO } from '../explainer/shared';
import { B, COPY, Comp, K, Mask, W } from '../kinetic/KineticAd';

/*
 * «Орбиты»: concentric rings of type turn around a centre where each step happens. Photos and
 * storyboard frames travel on orbits and land in the middle; the render becomes a ring filling up.
 */

const CX = 1240;
const CY = 540;

const Ring: React.FC<{ r: number; text: string; rot: number; size: number; color: string; id: string; opacity?: number; weight?: number }> = ({ r, text, rot, size, color, id, opacity = 1, weight = 500 }) => {
  const circ = 2 * Math.PI * r;
  const unit = `${text}  ·  `;
  const reps = Math.max(1, Math.floor(circ / (unit.length * size * 0.56)));
  return (
    <svg width={1920} height={1080} style={{ position: 'absolute', inset: 0, overflow: 'visible', opacity }}>
      <defs>
        <path id={id} d={`M ${CX - r} ${CY} a ${r} ${r} 0 1 1 ${2 * r} 0 a ${r} ${r} 0 1 1 ${-2 * r} 0`} />
      </defs>
      <g transform={`rotate(${rot} ${CX} ${CY})`}>
        <text fontFamily="Geist" fontSize={size} fontWeight={weight} letterSpacing={size * 0.12} fill={color}>
          <textPath href={`#${id}`} textLength={circ - 2} lengthAdjust="spacing">
            {unit.repeat(reps).toUpperCase()}
          </textPath>
        </text>
      </g>
    </svg>
  );
};

const Orbit: React.FC<{ r: number; p?: number }> = ({ r, p = 1 }) => (
  <svg width={1920} height={1080} style={{ position: 'absolute', inset: 0 }}>
    <circle cx={CX} cy={CY} r={r} fill="none" stroke="rgba(17,17,17,0.18)" strokeWidth={1.5} pathLength={1} strokeDasharray="1 2" strokeDashoffset={1 - p} />
  </svg>
);

const Left: React.FC<{ children: ReactNode }> = ({ children }) => <div style={{ position: 'absolute', left: 130, top: 330, width: 620, color: K.ink }}>{children}</div>;

export const OrbitKinetic: React.FC<{ lang?: 'ru' | 'en' }> = ({ lang = 'ru' }) => {
  const f = useCurrentFrame();
  const c = COPY[lang];
  const rot = f * 0.6;
  let center: ReactNode = null;
  let left: ReactNode = null;
  let ringText = 'Motion Engine · ONEFLOW';
  let ringOn = prog(f, B.motion, B.motion + 16);

  const heading = (n: string, a: string, b: string, t: number) => (
    <Left>
      <div style={{ fontSize: 24, letterSpacing: '0.2em', color: K.mid, opacity: prog(t, 0, 8), ...W(500) }}>{n}</div>
      <div style={{ marginTop: 16, fontSize: 96, lineHeight: 1.02, letterSpacing: '-0.045em' }}>
        <Mask y={mix(110, 0, prog(t, 2, 12, ease.out))}>
          <span style={W(mix(200, 700, prog(t, 2, 22)))}>{a}</span>
        </Mask>
        <Mask y={mix(110, 0, prog(t, 6, 16, ease.out))}>
          <span style={{ ...W(200), color: K.mid }}>{b}</span>
        </Mask>
      </div>
    </Left>
  );

  if (f < B.motion) {
    // the word in the middle changes: photos → idea → video
    const i = Math.min(2, Math.floor(f / 10));
    const t = f - i * 10;
    const words = c.open.map((w) => w.split(' ')[1].replace('.', ''));
    ringText = c.open.join(' ');
    ringOn = prog(f, 0, 10);
    center = (
      <div style={{ position: 'absolute', left: CX - 400, top: CY - 110, width: 800, textAlign: 'center', fontSize: 190, lineHeight: 1, letterSpacing: '-0.05em', color: K.ink, ...W(i === 2 ? 800 : 300) }}>
        <Mask y={mix(110, 0, prog(t, 0, 7, ease.out))}>{words[i]}</Mask>
      </div>
    );
    left = (
      <Left>
        <div style={{ fontSize: 110, lineHeight: 1, letterSpacing: '-0.05em', ...W(200) }}>
          <Mask y={mix(110, 0, prog(t, 0, 7, ease.out))}>{c.open[i].split(' ')[0]}</Mask>
        </div>
      </Left>
    );
  } else if (f < B.s1) {
    const t = f - B.motion;
    const d = spring({ frame: t, fps: 30, config: { damping: 14, stiffness: 120 } });
    center = (
      <>
        <div style={{ position: 'absolute', left: CX - 230 * d, top: CY - 230 * d, width: 460 * d, height: 460 * d, borderRadius: '50%', background: K.lime }} />
        <div style={{ position: 'absolute', left: CX - 400, top: CY - 100, width: 800, textAlign: 'center', fontSize: 130, lineHeight: 0.86, letterSpacing: '-0.05em', color: K.ink }}>
          <Mask y={mix(110, 0, prog(t, 4, 14, ease.out))}>
            <span style={W(800)}>MOTION</span>
          </Mask>
          <Mask y={mix(110, 0, prog(t, 8, 18, ease.out))}>
            <span style={W(200)}>ENGINE</span>
          </Mask>
        </div>
      </>
    );
    left = (
      <Left>
        <Mask y={mix(110, 0, prog(t, 10, 20, ease.out))}>
          <div style={{ fontSize: 30, letterSpacing: '0.2em', ...W(600) }}>ONEFLOW</div>
        </Mask>
      </Left>
    );
  } else if (f < B.s2) {
    const t = f - B.s1;
    left = heading('01 / 03', c.s1a, c.s1c.toLowerCase(), t);
    ringText = c.tags.join(' · ');
    const typedTags = Math.floor(interpolate(t, [40, 64], [0, c.tags.length], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }));
    center = (
      <>
        {[0, 3, 1].map((k, i) => {
          // each "photo" travels along the orbit and lands in a row in the centre
          const land = prog(t, 14 + i * 6, 36 + i * 6, ease.inOut);
          const a = (-90 + i * 120 + t * 2.2) * (Math.PI / 180);
          const ox = CX + Math.cos(a) * 380;
          const oy = CY + Math.sin(a) * 380;
          const tx = CX - 300 + i * 210;
          const ty = CY - 90;
          const x = mix(ox - 90, tx - 90, land);
          const y = mix(oy - 90, ty, land);
          const s = mix(0.7, 1, land);
          return (
            <div key={i} style={{ position: 'absolute', left: x, top: y, transform: `scale(${s})`, opacity: prog(t, 4 + i * 4, 10 + i * 4), boxShadow: '0 20px 40px -20px rgba(0,0,0,0.3)', borderRadius: 24 }}>
              <Comp kind={k} t={t - 10 - i * 5} w={180} h={180} bg={i === 1 ? K.ink : '#f7f7f7'} fg={i === 1 ? '#f7f7f7' : K.ink} ac={K.lime} r={24} />
            </div>
          );
        })}
        <div style={{ position: 'absolute', left: CX - 300, top: CY + 130, width: 600, display: 'flex', flexWrap: 'wrap', gap: 10, justifyContent: 'center' }}>
          {c.tags.slice(0, typedTags).map((tag, i) => (
            <div key={tag} style={{ padding: '8px 20px', borderRadius: 99, background: i === 0 ? K.lime : '#f7f7f7', fontSize: 26, ...W(500) }}>
              {tag}
            </div>
          ))}
        </div>
        <div style={{ position: 'absolute', left: 130, top: 640, display: 'inline-flex', alignItems: 'center', gap: 14, height: 76, padding: '0 34px', borderRadius: 99, background: K.ink, color: '#fff', fontSize: 28, ...W(500), opacity: prog(t, 66, 72) }}>
          {c.make} <span style={{ color: K.lime }}>→</span>
        </div>
      </>
    );
  } else if (f < B.s3) {
    const t = f - B.s2;
    left = heading('02 / 03', c.s2, c.s2b.toLowerCase(), t);
    ringText = c.s2;
    const pick = prog(t, 48, 64, ease.inOut);
    const n = 10;
    center = (
      <>
        {Array.from({ length: n }).map((_, i) => {
          const a = ((i / n) * 360 + t * 1.4 - 90) * (Math.PI / 180);
          const chosen = i === 3;
          const r = mix(320, 320, 1);
          let x = CX + Math.cos(a) * r - 80;
          let y = CY + Math.sin(a) * r - 45;
          let s = prog(t, 4 + i * 2, 12 + i * 2, ease.out);
          if (chosen) {
            x = mix(x, CX - 220, pick);
            y = mix(y, CY - 124, pick);
            s *= mix(1, 2.75, pick);
          }
          return (
            <div key={i} style={{ position: 'absolute', left: x, top: y, width: 160, height: 90, transform: `scale(${s})`, transformOrigin: '0 0', opacity: chosen ? 1 : mix(1, 0.3, pick), zIndex: chosen ? 2 : 1, boxShadow: chosen ? `0 0 0 ${3 * pick}px ${K.lime}` : 'none', borderRadius: 12 }}>
              <Comp kind={i % 5} t={t - 6 - i * 2} w={160} h={90} bg={chosen ? K.ink : '#f7f7f7'} fg={chosen ? '#f7f7f7' : K.ink} ac={K.lime} r={12} />
            </div>
          );
        })}
      </>
    );
  } else if (f < B.res) {
    const t = f - B.s3;
    left = heading('03 / 03', c.s3, 'MP4', t);
    ringText = c.s3;
    const p = prog(t, 6, 50, ease.soft);
    const R = 300;
    center = (
      <>
        <svg width={1920} height={1080} style={{ position: 'absolute', inset: 0 }}>
          <circle cx={CX} cy={CY} r={R} fill="none" stroke="rgba(17,17,17,0.12)" strokeWidth={34} />
          <circle cx={CX} cy={CY} r={R} fill="none" stroke={K.lime} strokeWidth={34} strokeLinecap="round" pathLength={1} strokeDasharray={`${p} 2`} transform={`rotate(-90 ${CX} ${CY})`} />
        </svg>
        <div style={{ position: 'absolute', left: CX - 300, top: CY - 110, width: 600, textAlign: 'center', fontSize: 200, lineHeight: 1, letterSpacing: '-0.06em', color: K.ink, fontVariantNumeric: 'tabular-nums', ...W(mix(150, 850, p)) }}>
          {Math.round(p * 100)}
          <span style={{ ...W(150), fontSize: 110 }}>%</span>
        </div>
        <div style={{ position: 'absolute', left: CX - 120, top: CY + 120, width: 240, textAlign: 'center', fontSize: 30, letterSpacing: '0.16em', ...W(600), opacity: prog(t, 50, 56) }}>✓ {c.done.toUpperCase()}</div>
      </>
    );
  } else if (f < B.end) {
    const t = f - B.res;
    ringText = `${c.res1} ${c.res2}`;
    left = (
      <Left>
        <div style={{ fontSize: 170, lineHeight: 0.95, letterSpacing: '-0.055em' }}>
          <Mask y={mix(110, 0, prog(t, 2, 12, ease.out))}>
            <span style={W(800)}>{c.res1}</span>
          </Mask>
          <Mask y={mix(110, 0, prog(t, 6, 16, ease.out))}>
            <span style={W(200)}>{c.res2}</span>
          </Mask>
        </div>
      </Left>
    );
    center = (
      <div style={{ position: 'absolute', left: CX - 330, top: CY - 186, borderRadius: 36, overflow: 'hidden', transform: `scale(${spring({ frame: t, fps: 30, config: { damping: 14, stiffness: 110 } })})` }}>
        <Comp kind={1} t={t - 4} w={660} h={372} bg={K.ink} fg="#f7f7f7" ac={K.lime} r={36} />
      </div>
    );
  } else {
    const t = f - B.end;
    ringText = 'ONEFLOW · Motion Engine';
    const e = [prog(t, 0, 12), prog(t, 4, 16), prog(t, 8, 20), prog(t, 12, 24)];
    center = (
      <div style={{ position: 'absolute', left: CX - 150, top: CY - 150, width: 300, height: 300, borderRadius: '50%', background: K.lime, display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `scale(${spring({ frame: t, fps: 30, config: { damping: 14, stiffness: 120 } })})` }}>
        <svg width="120" height="120" viewBox="0 0 96 96">
          <g transform="translate(10 13.2)">
            <path d={LOGO} fill={K.ink} />
          </g>
        </svg>
      </div>
    );
    left = (
      <div style={{ position: 'absolute', left: 130, top: 300, color: K.ink }}>
        <Mask y={mix(110, 0, e[0])}>
          <div style={{ fontSize: 32, letterSpacing: '0.04em', ...W(600) }}>
            ONEFLOW <span style={{ ...W(300), color: K.mid }}>Motion Engine</span>
          </div>
        </Mask>
        <div style={{ marginTop: 30, fontSize: 80, lineHeight: 1.04, letterSpacing: '-0.05em', whiteSpace: 'nowrap' }}>
          <Mask y={mix(110, 0, e[1])}>
            <span style={W(250)}>{c.end1}</span>
          </Mask>
          <Mask y={mix(110, 0, e[2])}>
            <span style={W(750)}>{c.end2}</span>
          </Mask>
        </div>
        <div style={{ marginTop: 46, display: 'inline-flex', alignItems: 'center', gap: 14, height: 80, padding: '0 36px', borderRadius: 99, background: K.ink, color: '#fff', fontSize: 28, ...W(500), opacity: e[3] }}>
          {c.cta} <span style={{ color: K.lime }}>→</span>
        </div>
      </div>
    );
  }

  return (
    <AbsoluteFill style={{ background: K.grey, fontFamily: FONT, overflow: 'hidden' }}>
      <AbsoluteFill style={{ transform: `scale(${mix(0.9, 0.66, prog(f, B.end, B.end + 20, ease.inOut))})`, transformOrigin: `${CX}px ${CY}px` }}>
      <Orbit r={260} p={prog(f, 0, 20, ease.inOut)} />
      <Orbit r={380} p={prog(f, 4, 26, ease.inOut)} />
      <Ring r={470} text={ringText} rot={rot} size={30} color={K.ink} id="r1" opacity={ringOn} weight={500} />
      <Ring r={530} text={ringText} rot={-rot * 0.7} size={22} color={K.mid} id="r2" opacity={ringOn * 0.8} weight={400} />
      {/* a lime satellite */}
      <div style={{ position: 'absolute', left: CX + Math.cos((f * 2.4 * Math.PI) / 180) * 380 - 14, top: CY + Math.sin((f * 2.4 * Math.PI) / 180) * 380 - 14, width: 28, height: 28, borderRadius: '50%', background: K.lime, border: `2px solid ${K.ink}` }} />
      {center}
      </AbsoluteFill>
      {left}
    </AbsoluteFill>
  );
};
