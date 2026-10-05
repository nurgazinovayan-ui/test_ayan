import type { ReactNode } from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame } from 'remotion';
import '../fonts';
import { FONT } from '../fonts';
import { ease, mix, prog } from '../theme';
import { LOGO } from '../explainer/shared';
import { B, COPY, Comp, K, Mask, W, punch } from '../kinetic/KineticAd';

/*
 * «Swiss»: International-style poster. Strict 12-column grid, giant uppercase words that bleed off
 * the frame, cropped numerals, split colour fields and hairline rules. Hard pushes between beats.
 */

const M = 96;
const COL = (1920 - 2 * M - 11 * 20) / 12;
const cx = (i: number) => M + i * (COL + 20);

const Rules: React.FC<{ f: number; dark?: boolean; label: string; idx: string }> = ({ f, dark, label, idx }) => (
  <>
    <div style={{ position: 'absolute', left: M, right: M, top: 64, height: 2, background: dark ? '#f7f7f7' : K.ink, transform: `scaleX(${prog(f, 0, 14, ease.inOut)})`, transformOrigin: 'left' }} />
    <div style={{ position: 'absolute', left: M, top: 28, fontSize: 20, letterSpacing: '0.12em', color: dark ? '#f7f7f7' : K.ink, ...W(600) }}>ONEFLOW / MOTION ENGINE</div>
    <div style={{ position: 'absolute', left: cx(6), top: 28, fontSize: 20, letterSpacing: '0.12em', color: dark ? '#f7f7f7' : K.ink, ...W(400) }}>{label}</div>
    <div style={{ position: 'absolute', right: M, top: 28, fontSize: 20, letterSpacing: '0.12em', color: dark ? '#f7f7f7' : K.ink, ...W(400), fontVariantNumeric: 'tabular-nums' }}>{idx}</div>
  </>
);

const Bg: React.FC<{ c: string; children: ReactNode }> = ({ c, children }) => <AbsoluteFill style={{ background: c, overflow: 'hidden', fontFamily: FONT }}>{children}</AbsoluteFill>;

export const SwissKinetic: React.FC<{ lang?: 'ru' | 'en' }> = ({ lang = 'ru' }) => {
  const f = useCurrentFrame();
  const c = COPY[lang];
  const up = (s: string) => s.replace(/\.$/, '').toUpperCase();

  // ---- opening: one giant word at a time, pushed up out of frame
  if (f < B.motion) {
    const words = c.open.map((w) => up(w.split(' ')[1]));
    const i = Math.min(2, Math.floor(f / 10));
    const t = f - i * 10;
    return (
      <Bg c={i === 2 ? K.lime : K.grey}>
        <Rules f={f} label={c.open.join(' ')} idx="00" />
        <div style={{ position: 'absolute', left: cx(0) - 20, top: 140, fontSize: 150, lineHeight: 1, letterSpacing: '-0.04em', color: K.ink, ...W(300) }}>
          <Mask y={mix(110, 0, prog(t, 0, 6, ease.out))}>{up(c.open[i].split(' ')[0])}</Mask>
        </div>
        <div style={{ position: 'absolute', left: -30, top: 290, fontSize: 560, lineHeight: 0.86, letterSpacing: '-0.075em', color: K.ink, whiteSpace: 'nowrap', ...W(900) }}>
          <Mask y={mix(100, 0, prog(t, 0, 7, ease.out))}>{words[i]}</Mask>
        </div>
      </Bg>
    );
  }

  // ---- MOTION / ENGINE split field
  if (f < B.s1) {
    const t = f - B.motion;
    const split = prog(t, 0, 10, ease.out);
    return (
      <Bg c={K.grey}>
        <div style={{ position: 'absolute', left: 0, top: 0, bottom: 0, width: `${mix(0, 64, split)}%`, background: K.ink }} />
        <div style={{ position: 'absolute', right: 0, top: 0, bottom: 0, width: `${mix(0, 36, split)}%`, background: K.lime }} />
        <Rules f={t} dark label="MOTION ENGINE" idx="—" />
        <div style={{ position: 'absolute', left: M - 20, top: 210, fontSize: 380, lineHeight: 0.84, letterSpacing: '-0.07em', color: '#f7f7f7', ...W(900), transform: `translateX(${mix(-300, 0, prog(t, 2, 14, ease.out))}px)` }}>
          <Mask y={mix(100, 0, prog(t, 2, 12, ease.out))}>MOTION</Mask>
        </div>
        <div style={{ position: 'absolute', left: cx(8), top: 640, fontSize: 150, lineHeight: 0.9, letterSpacing: '-0.05em', color: K.ink, ...W(mix(100, 700, prog(t, 8, 28))) }}>
          <Mask y={mix(100, 0, prog(t, 8, 18, ease.out))}>ENGINE</Mask>
        </div>
        <div style={{ position: 'absolute', left: M, bottom: 60, fontSize: 30, color: '#f7f7f7', opacity: prog(t, 14, 22), ...W(400) }}>
          {c.end1} {c.end2}
        </div>
        <div style={{ position: 'absolute', left: 0, right: 0, top: 0, height: `${prog(t, 34, 42, ease.in) * 100}%`, background: K.grey }} />
      </Bg>
    );
  }

  const NumCrop: React.FC<{ n: string; t: number; color: string }> = ({ n, t, color }) => (
    <div style={{ position: 'absolute', left: -40, bottom: -230, fontSize: 760, lineHeight: 1, letterSpacing: '-0.08em', color, ...W(900), transform: `translateY(${mix(500, 0, prog(t, 0, 12, ease.out))}px)` }}>{n}</div>
  );

  // ---- 01
  if (f < B.s2) {
    const t = f - B.s1;
    const typed = Math.floor(interpolate(t, [40, 62], [0, c.s1c.length], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }));
    const press = t < 74 ? 0 : t < 77 ? 1 : 1 - prog(t, 77, 84);
    return (
      <Bg c={K.grey}>
        <Rules f={t + 20} label={`${c.s1a} ${c.s1b} / ${c.s1c}`} idx="01 / 03" />
        <NumCrop n="01" t={t} color={K.ink} />
        <div style={{ position: 'absolute', left: cx(0), top: 120, fontSize: 112, lineHeight: 0.98, letterSpacing: '-0.05em', color: K.ink }}>
          <Mask y={mix(110, 0, prog(t, 2, 12, ease.out))}>
            <span style={W(800)}>{c.s1a.toUpperCase()}</span>
          </Mask>
          <Mask y={mix(110, 0, prog(t, 6, 16, ease.out))}>
            <span style={W(200)}>{c.s1b.toUpperCase()}</span>
          </Mask>
        </div>
        {[0, 3, 1].map((kind, i) => {
          const d = spring({ frame: t - 6 - i * 4, fps: 30, config: { damping: 14, stiffness: 180 } });
          const x = cx(6 + i * 2);
          return (
            <div key={i} style={{ position: 'absolute', left: x, top: 120, transform: `translateY(${mix(-900, 0, d)}px)` }}>
              <Comp kind={kind} t={t - 8 - i * 4} w={COL * 2 + 20} h={COL * 2 + 20} bg={i === 1 ? K.ink : '#f7f7f7'} fg={i === 1 ? '#f7f7f7' : K.ink} ac={K.lime} r={0} />
              <div style={{ marginTop: 10, fontSize: 18, letterSpacing: '0.1em', ...W(500) }}>IMG_0{i + 1}</div>
            </div>
          );
        })}
        <div style={{ position: 'absolute', left: cx(6), top: 520, width: cx(12) - cx(6) - 20, borderTop: `2px solid ${K.ink}`, paddingTop: 18, opacity: prog(t, 36, 42) }}>
          <div style={{ fontSize: 20, letterSpacing: '0.1em', ...W(600) }}>{c.s1c.toUpperCase()}</div>
          <div style={{ marginTop: 14, fontSize: 64, lineHeight: 1.05, letterSpacing: '-0.035em', ...W(300), minHeight: 140 }}>
            {c.tags.slice(0, Math.max(0, Math.floor((typed / c.s1c.length) * c.tags.length + 0.01))).join(', ')}
            <span style={{ display: 'inline-block', width: 8, height: 60, marginLeft: 6, verticalAlign: '-8px', background: K.lime }} />
          </div>
          <div style={{ marginTop: 24, display: 'inline-flex', alignItems: 'center', gap: 16, height: 84, padding: '0 34px', background: K.ink, color: '#fff', fontSize: 32, ...W(500), opacity: prog(t, 62, 68), transform: `scale(${1 - press * 0.06})` }}>
            {c.make.toUpperCase()} <span style={{ color: K.lime }}>→</span>
          </div>
        </div>
      </Bg>
    );
  }

  // ---- 02
  if (f < B.s3) {
    const t = f - B.s2;
    const pick = prog(t, 50, 58, ease.out);
    const kinds = [
      [0, 2, 3, 1],
      [3, 0, 4, 2],
      [1, 3, 2, 0],
    ];
    const fw = COL * 2 + 20;
    const fh = fw * 0.5625;
    return (
      <Bg c={K.ink}>
        <Rules f={t + 20} dark label={`${c.s2} / ${c.s2b}`} idx="02 / 03" />
        <NumCrop n="02" t={t} color="#1d1d20" />
        <div style={{ position: 'absolute', left: cx(0), top: 120, fontSize: 112, lineHeight: 0.98, letterSpacing: '-0.05em', color: '#f7f7f7' }}>
          <Mask y={mix(110, 0, prog(t, 2, 12, ease.out))}>
            <span style={W(800)}>{c.s2.toUpperCase()}</span>
          </Mask>
          <Mask y={mix(110, 0, prog(t, 46, 56, ease.out))}>
            <span style={{ ...W(200), color: K.lime }}>{c.s2b.toUpperCase()}</span>
          </Mask>
        </div>
        {kinds.map((row, r) =>
          row.map((kind, i) => {
            const at = 10 + r * 6 + i * 3;
            const k = prog(t, at, at + 8, ease.out);
            const isB = r === 1;
            return (
              <div key={`${r}${i}`} style={{ position: 'absolute', left: cx(4 + i * 2), top: 380 + r * (fh + 24), clipPath: `inset(0 ${(1 - k) * 100}% 0 0)`, opacity: isB ? 1 : mix(1, 0.3, pick) }}>
                <Comp kind={kind} t={t - at} w={fw} h={fh} bg={isB && pick > 0.5 ? K.lime : '#1c1c1e'} fg={isB && pick > 0.5 ? K.ink : '#f7f7f7'} ac={isB && pick > 0.5 ? '#f7f7f7' : K.lime} r={0} />
              </div>
            );
          }),
        )}
        <div style={{ position: 'absolute', left: cx(4) - 70, top: 380 + fh + 24 + fh / 2 - 40, fontSize: 80, color: K.lime, ...W(300), opacity: pick, transform: `translateX(${mix(-40, 0, pick)}px)` }}>→</div>
      </Bg>
    );
  }

  // ---- 03
  if (f < B.res) {
    const t = f - B.s3;
    const p = prog(t, 6, 50, ease.soft);
    const done = prog(t, 50, 58, ease.out);
    return (
      <Bg c={K.lime}>
        <Rules f={t + 20} label={c.s3} idx="03 / 03" />
        <div style={{ position: 'absolute', left: cx(0), top: 120, fontSize: 112, letterSpacing: '-0.05em', color: K.ink, ...W(800) }}>
          <Mask y={mix(110, 0, prog(t, 2, 12, ease.out))}>{c.s3.toUpperCase()}</Mask>
        </div>
        <div style={{ position: 'absolute', right: M - 30, bottom: -120, fontSize: 820, lineHeight: 1, letterSpacing: '-0.08em', color: K.ink, fontVariantNumeric: 'tabular-nums', ...W(900) }}>{Math.round(p * 100)}</div>
        <div style={{ position: 'absolute', left: cx(0), top: 300, fontSize: 200, color: K.ink, ...W(100) }}>%</div>
        <div style={{ position: 'absolute', left: M, right: M, top: 260, height: 2, background: 'rgba(17,17,17,0.2)' }}>
          <div style={{ width: `${p * 100}%`, height: 2, background: K.ink }} />
        </div>
        <div style={{ position: 'absolute', left: cx(0), top: 560, display: 'flex', gap: 0, opacity: done, transform: `translateX(${mix(-80, 0, done)}px)` }}>
          <div style={{ padding: '18px 34px', background: K.ink, color: K.lime, fontSize: 56, ...W(800) }}>MP4</div>
          <div style={{ padding: '18px 34px', background: '#f7f7f7', color: K.ink, fontSize: 56, ...W(300) }}>{c.done.toUpperCase()}</div>
        </div>
      </Bg>
    );
  }

  // ---- the piece
  if (f < B.end) {
    const t = f - B.res;
    const side = COL * 2 + 20;
    return (
      <Bg c={K.grey}>
        <Rules f={t + 20} label={`${c.res1} ${c.res2}`} idx="→" />
        <div style={{ position: 'absolute', left: -20, top: 100, fontSize: 250, lineHeight: 0.86, letterSpacing: '-0.07em', color: K.ink }}>
          <Mask y={mix(100, 0, prog(t, 2, 12, ease.out))}>
            <span style={W(900)}>{up(c.res1)}</span>
          </Mask>
          <Mask y={mix(100, 0, prog(t, 6, 16, ease.out))}>
            <span style={W(100)}>{up(c.res2)}</span>
          </Mask>
        </div>
        <div style={{ position: 'absolute', left: cx(4), top: 600, display: 'flex', gap: 20, transform: `scale(${punch(f, B.res + 4, 0.05)})`, transformOrigin: 'left top' }}>
          {[1, 0, 2, 3].map((k, i) => (
            <Comp key={k} kind={k} t={t - 4 - i * 4} w={side} h={side} bg={i === 0 ? K.ink : i === 2 ? K.lime : '#f7f7f7'} fg={i === 0 ? '#f7f7f7' : K.ink} ac={i === 2 ? K.ink : K.lime} r={0} />
          ))}
        </div>
      </Bg>
    );
  }

  // ---- end
  const t = f - B.end;
  const e = [prog(t, 0, 12), prog(t, 4, 16), prog(t, 8, 20), prog(t, 12, 24)];
  return (
    <Bg c={K.grey}>
      <Rules f={t + 20} label={c.cta} idx="ONEFLOW" />
      <div style={{ position: 'absolute', left: cx(8), top: 0, bottom: 0, right: 0, background: K.lime, transform: `scaleY(${prog(t, 0, 14, ease.out)})`, transformOrigin: 'top' }} />
      <div style={{ position: 'absolute', left: cx(8) + 40, bottom: 80, fontSize: 200, lineHeight: 0.86, letterSpacing: '-0.06em', color: K.ink, ...W(900), opacity: prog(t, 8, 16) }}>
        M<span style={W(100)}>E</span>
      </div>
      <div style={{ position: 'absolute', left: cx(0), top: 170, color: K.ink }}>
        <Mask y={mix(110, 0, e[0])}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 18 }}>
            <svg width="72" height="72" viewBox="0 0 96 96">
              <rect width="96" height="96" rx="22" fill={K.ink} />
              <g transform="translate(10 13.2)">
                <path d={LOGO} fill="#fff" />
              </g>
            </svg>
            <span style={{ fontSize: 40, ...W(700), letterSpacing: '-0.02em' }}>ONEFLOW</span>
            <span style={{ fontSize: 40, ...W(300) }}>MOTION ENGINE</span>
          </div>
        </Mask>
        <div style={{ marginTop: 40, fontSize: 96, lineHeight: 0.98, letterSpacing: '-0.05em', whiteSpace: 'nowrap' }}>
          <Mask y={mix(110, 0, e[1])}>
            <span style={W(800)}>{c.end1.toUpperCase()}</span>
          </Mask>
          <Mask y={mix(110, 0, e[2])}>
            <span style={W(200)}>{c.end2.toUpperCase()}</span>
          </Mask>
        </div>
        <div style={{ marginTop: 56, display: 'inline-flex', alignItems: 'center', gap: 16, height: 88, padding: '0 38px', background: K.ink, color: '#fff', fontSize: 32, ...W(500), opacity: e[3], transform: `translateX(${mix(-60, 0, e[3])}px)` }}>
          {c.cta.toUpperCase()} <span style={{ color: K.lime }}>→</span>
        </div>
      </div>
    </Bg>
  );
};
