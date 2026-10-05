import type { ReactNode } from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';
import '../fonts';
import { FONT, SERIF } from '../fonts';
import { ease, mix, prog } from '../theme';
import { LOGO } from '../explainer/shared';
import { B, COPY, Comp, K, W } from '../kinetic/KineticAd';

/*
 * «Serif / люкс»: Cormorant Garamond with italics for emphasis, Geist in spaced small caps for labels,
 * warm paper, hairlines and arches. Everything arrives slowly out of blur and wide tracking.
 */

const PAPER = '#ecebe6';
const INK = '#151514';
const SOFT = '#8d8b84';

const Soft: React.FC<{ p: number; children: ReactNode; track?: number }> = ({ p, children, track = 0.3 }) => (
  <span style={{ display: 'inline-block', opacity: p, filter: `blur(${(1 - p) * 14}px)`, letterSpacing: `${mix(track, -0.01, p)}em`, transform: `translateY(${mix(24, 0, p)}px)` }}>{children}</span>
);

const Label: React.FC<{ p: number; children: ReactNode }> = ({ p, children }) => (
  <div style={{ fontFamily: FONT, fontSize: 20, letterSpacing: '0.34em', textTransform: 'uppercase', color: SOFT, opacity: p, ...W(400) }}>{children}</div>
);

/** Arch-topped frame (a window), drawn as a hairline, with a composition inside. */
const Arch: React.FC<{ w: number; h: number; p: number; kind: number; t: number; dark?: boolean }> = ({ w, h, p, kind, t, dark }) => (
  <div style={{ position: 'relative', width: w, height: h }}>
    <div style={{ position: 'absolute', inset: 0, borderRadius: `${w / 2}px ${w / 2}px 0 0`, overflow: 'hidden', clipPath: `inset(${(1 - p) * 100}% 0 0 0)` }}>
      <Comp kind={kind} t={t} w={w} h={h} bg={dark ? INK : '#f6f5f1'} fg={dark ? '#f6f5f1' : INK} ac={K.lime} r={0} />
    </div>
    <svg width={w} height={h} style={{ position: 'absolute', inset: 0, overflow: 'visible' }}>
      <path d={`M0 ${h} V${w / 2} A${w / 2} ${w / 2} 0 0 1 ${w} ${w / 2} V${h} Z`} fill="none" stroke={INK} strokeWidth={1.2} pathLength={1} strokeDasharray="1 2" strokeDashoffset={1 - p} transform="translate(0 0)" />
    </svg>
  </div>
);

export const SerifKinetic: React.FC<{ lang?: 'ru' | 'en' }> = ({ lang = 'ru' }) => {
  const f = useCurrentFrame();
  const c = COPY[lang];
  let body: ReactNode;
  const drift = 1 + 0.015 * Math.sin(f / 70);

  if (f < B.motion) {
    body = (
      <div style={{ position: 'absolute', left: 0, right: 0, top: 260, textAlign: 'center', fontFamily: SERIF, fontSize: 140, lineHeight: 1.1, color: INK, fontWeight: 300 }}>
        {c.open.map((l, i) => (
          <div key={l} style={{ fontStyle: i === 1 ? 'italic' : 'normal', fontWeight: i === 2 ? 500 : 300 }}>
            <Soft p={prog(f, i * 8, i * 8 + 14, ease.out)}>{l}</Soft>
          </div>
        ))}
      </div>
    );
  } else if (f < B.s1) {
    const t = f - B.motion;
    const r = 330;
    body = (
      <>
        <svg width={1920} height={1080} style={{ position: 'absolute', inset: 0 }}>
          <circle cx={960} cy={520} r={r} fill="none" stroke={INK} strokeWidth={1.2} pathLength={1} strokeDasharray="1 2" strokeDashoffset={1 - prog(t, 0, 30, ease.inOut)} transform="rotate(-90 960 520)" />
          <circle cx={960 + r * Math.cos(prog(t, 0, 30, ease.inOut) * Math.PI * 2 - Math.PI / 2)} cy={520 + r * Math.sin(prog(t, 0, 30, ease.inOut) * Math.PI * 2 - Math.PI / 2)} r={10} fill={K.lime} stroke={INK} strokeWidth={1.2} />
        </svg>
        <div style={{ position: 'absolute', left: 0, right: 0, top: 300, textAlign: 'center', fontFamily: SERIF, fontStyle: 'italic', fontSize: 330, lineHeight: 1, color: INK, fontWeight: 300 }}>
          <Soft p={prog(t, 2, 22, ease.out)} track={0.15}>
            Motion
          </Soft>
        </div>
        <div style={{ position: 'absolute', left: 0, right: 0, top: 690, textAlign: 'center' }}>
          <Label p={prog(t, 12, 24)}>Engine · ONEFLOW</Label>
        </div>
      </>
    );
  } else if (f < B.s2) {
    const t = f - B.s1;
    const typed = Math.floor(interpolate(t, [42, 64], [0, c.s1c.length], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }));
    const press = t < 74 ? 0 : t < 77 ? 1 : 1 - prog(t, 77, 84);
    body = (
      <>
        <div style={{ position: 'absolute', left: 150, top: 150 }}>
          <Label p={prog(t, 0, 10)}>I — {c.s1a}</Label>
          <div style={{ marginTop: 24, fontFamily: SERIF, fontSize: 132, lineHeight: 1, color: INK, fontWeight: 300 }}>
            <Soft p={prog(t, 2, 18, ease.out)}>{c.s1a}</Soft> <i>
              <Soft p={prog(t, 8, 24, ease.out)}>{c.s1b}</Soft>
            </i>
          </div>
          <div style={{ marginTop: 70, fontFamily: SERIF, fontStyle: 'italic', fontSize: 64, lineHeight: 1.2, color: INK, fontWeight: 300, opacity: prog(t, 40, 46) }}>
            «{c.s1c.slice(0, typed)}»
          </div>
          <div style={{ marginTop: 18, fontFamily: FONT, fontSize: 24, letterSpacing: '0.2em', textTransform: 'uppercase', color: SOFT, ...W(400), opacity: prog(t, 56, 62) }}>{c.tags.join(' · ')}</div>
          <div style={{ marginTop: 46, display: 'inline-flex', alignItems: 'center', gap: 18, height: 80, padding: '0 40px', borderRadius: 99, border: `1.2px solid ${INK}`, background: press > 0 ? K.lime : 'transparent', fontFamily: FONT, fontSize: 24, letterSpacing: '0.16em', textTransform: 'uppercase', color: INK, ...W(500), opacity: prog(t, 64, 70) }}>
            {c.make} →
          </div>
        </div>
        <div style={{ position: 'absolute', left: 1110, top: 180, display: 'flex', gap: 30 }}>
          {[0, 3, 1].map((k, i) => (
            <div key={i} style={{ transform: `translateY(${i % 2 ? 80 : 0}px)` }}>
              <Arch w={196} h={440} p={prog(t, 4 + i * 6, 30 + i * 6, ease.inOut)} kind={k} t={t - 10 - i * 6} dark={i === 1} />
            </div>
          ))}
        </div>
      </>
    );
  } else if (f < B.s3) {
    const t = f - B.s2;
    const pick = prog(t, 52, 64, ease.inOut);
    const scroll = mix(200, -420, prog(t, 0, 84, ease.soft));
    const kinds = [0, 2, 3, 1, 4, 0, 2, 3];
    body = (
      <>
        <div style={{ position: 'absolute', left: 150, top: 150 }}>
          <Label p={prog(t, 0, 10)}>II — {c.s2}</Label>
          <div style={{ marginTop: 24, fontFamily: SERIF, fontSize: 132, lineHeight: 1, color: INK, fontWeight: 300 }}>
            <Soft p={prog(t, 2, 18, ease.out)}>{c.s2}</Soft>
          </div>
          <div style={{ marginTop: 10, fontFamily: SERIF, fontStyle: 'italic', fontSize: 72, color: INK, fontWeight: 300 }}>
            <Soft p={prog(t, 46, 62, ease.out)}>{c.s2b.toLowerCase()}</Soft>
          </div>
        </div>
        <div style={{ position: 'absolute', left: scroll, top: 560, display: 'flex', gap: 28 }}>
          {kinds.map((k, i) => {
            const chosen = i === 4;
            return (
              <div key={i} style={{ position: 'relative', opacity: chosen ? 1 : mix(1, 0.35, pick) }}>
                <Comp kind={k} t={t - 6 - i * 3} w={340} h={240} bg={chosen ? INK : '#f6f5f1'} fg={chosen ? '#f6f5f1' : INK} ac={K.lime} r={4} />
                <div style={{ marginTop: 12, fontFamily: FONT, fontSize: 16, letterSpacing: '0.24em', color: SOFT, ...W(400) }}>{String(i + 1).padStart(2, '0')}</div>
                {chosen && (
                  <svg width={420} height={320} style={{ position: 'absolute', left: -40, top: -40, overflow: 'visible' }}>
                    <ellipse cx={210} cy={160} rx={205} ry={150} fill="none" stroke={INK} strokeWidth={1.4} pathLength={1} strokeDasharray="1 2" strokeDashoffset={1 - pick} />
                  </svg>
                )}
              </div>
            );
          })}
        </div>
      </>
    );
  } else if (f < B.res) {
    const t = f - B.s3;
    const p = prog(t, 6, 50, ease.soft);
    body = (
      <>
        <div style={{ position: 'absolute', left: 150, top: 150 }}>
          <Label p={prog(t, 0, 10)}>III — {c.s3}</Label>
        </div>
        <div style={{ position: 'absolute', left: 0, right: 0, top: 230, textAlign: 'center', fontFamily: SERIF, fontSize: 460, lineHeight: 1, color: INK, fontWeight: 300, fontVariantNumeric: 'lining-nums tabular-nums' }}>
          {Math.round(p * 100)}
          <i style={{ fontSize: 220 }}>%</i>
        </div>
        <div style={{ position: 'absolute', left: 360, right: 360, top: 790, height: 1.2, background: 'rgba(21,21,20,0.2)' }}>
          <div style={{ width: `${p * 100}%`, height: 1.2, background: INK }} />
          <div style={{ position: 'absolute', left: `${p * 100}%`, top: -8, width: 16, height: 16, marginLeft: -8, borderRadius: 99, background: K.lime, border: `1.2px solid ${INK}` }} />
        </div>
        <div style={{ position: 'absolute', left: 0, right: 0, top: 850, textAlign: 'center' }}>
          <Label p={prog(t, 50, 58)}>MP4 · {c.done}</Label>
        </div>
      </>
    );
  } else if (f < B.end) {
    const t = f - B.res;
    body = (
      <>
        <div style={{ position: 'absolute', left: 1060, top: 170 }}>
          <Arch w={560} h={740} p={prog(t, 0, 24, ease.inOut)} kind={1} t={t - 6} dark />
        </div>
        <div style={{ position: 'absolute', left: 150, top: 330, fontFamily: SERIF, fontSize: 200, lineHeight: 1, color: INK, fontWeight: 300 }}>
          <div>
            <Soft p={prog(t, 4, 20, ease.out)}>{c.res1}</Soft>
          </div>
          <div style={{ fontStyle: 'italic' }}>
            <Soft p={prog(t, 10, 26, ease.out)}>{c.res2}</Soft>
          </div>
        </div>
      </>
    );
  } else {
    const t = f - B.end;
    body = (
      <>
        <div style={{ position: 'absolute', left: 1180, top: 240 }}>
          <Arch w={440} h={600} p={prog(t, 0, 20, ease.inOut)} kind={0} t={t} />
        </div>
        <div style={{ position: 'absolute', left: 150, top: 250 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 18, opacity: prog(t, 0, 12) }}>
            <svg width="60" height="60" viewBox="0 0 96 96">
              <rect width="96" height="96" rx="48" fill={INK} />
              <g transform="translate(10 13.2)">
                <path d={LOGO} fill="#fff" />
              </g>
            </svg>
            <Label p={1}>ONEFLOW · Motion Engine</Label>
          </div>
          <div style={{ marginTop: 40, fontFamily: SERIF, fontSize: 118, lineHeight: 1.04, color: INK, fontWeight: 300, whiteSpace: 'nowrap' }}>
            <div>
              <Soft p={prog(t, 4, 18, ease.out)}>{c.end1}</Soft>
            </div>
            <div style={{ fontStyle: 'italic', position: 'relative', display: 'inline-block' }}>
              <span style={{ position: 'absolute', left: 0, right: 0, bottom: 18, height: 3, background: K.lime, transform: `scaleX(${prog(t, 16, 30, ease.inOut)})`, transformOrigin: 'left' }} />
              <Soft p={prog(t, 8, 22, ease.out)}>{c.end2}</Soft>
            </div>
          </div>
          <div style={{ marginTop: 56, display: 'inline-flex', alignItems: 'center', gap: 18, height: 80, padding: '0 40px', borderRadius: 99, background: INK, color: '#f6f5f1', fontFamily: FONT, fontSize: 22, letterSpacing: '0.16em', textTransform: 'uppercase', ...W(500), opacity: prog(t, 14, 24) }}>
            {c.cta} <span style={{ color: K.lime }}>→</span>
          </div>
        </div>
      </>
    );
  }

  return (
    <AbsoluteFill style={{ background: PAPER, overflow: 'hidden' }}>
      <AbsoluteFill style={{ transform: `scale(${drift})`, transformOrigin: '960px 540px' }}>{body}</AbsoluteFill>
      <div style={{ position: 'absolute', left: 150, right: 150, top: 80, height: 1, background: 'rgba(21,21,20,0.25)' }} />
      <div style={{ position: 'absolute', left: 150, right: 150, bottom: 80, height: 1, background: 'rgba(21,21,20,0.25)' }} />
    </AbsoluteFill>
  );
};
