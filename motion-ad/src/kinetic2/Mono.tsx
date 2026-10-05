import type { CSSProperties, ReactNode } from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';
import '../fonts';
import { MONO } from '../fonts';
import { ease, mix, prog } from '../theme';
import { B, COPY, Comp, K, W, punch } from '../kinetic/KineticAd';

/*
 * «Mono / терминал»: Geist Mono on near-black, lime as the signal colour. Words decode out of
 * scrambled characters (deterministic per frame), progress is drawn with block characters, panels
 * are thin-ruled boxes. Precise, technical, calm.
 */

const BG = '#0b0b0c';
const FG = '#e9e9e6';
const DIM = '#6d6d70';
const CHARS = 'ABCDEFGHJKLMNOPQRSTUVWXYZ0123456789#%&*+=<>/\\';

/** Deterministic scramble: each character settles at its own frame. */
const decode = (text: string, t: number, speed = 1.6, start = 0) =>
  text
    .split('')
    .map((ch, i) => {
      if (ch === ' ') return ' ';
      const settle = start + i * speed + 6;
      if (t >= settle) return ch;
      if (t < start + i * speed * 0.4) return ' ';
      const h = Math.abs(Math.sin((i + 1) * 12.9898 + Math.floor(t) * 78.233) * 43758.5453);
      return CHARS[Math.floor((h - Math.floor(h)) * CHARS.length)];
    })
    .join('');

const blocks = (p: number, n = 32) => '█'.repeat(Math.round(p * n)) + '░'.repeat(n - Math.round(p * n));

const Box: React.FC<{ x: number; y: number; w: number; h: number; title: string; p: number; children?: ReactNode; style?: CSSProperties }> = ({ x, y, w, h, title, p, children, style }) => (
  <div style={{ position: 'absolute', left: x, top: y, width: w, height: h, ...style }}>
    <svg width={w} height={h} style={{ position: 'absolute', inset: 0, overflow: 'visible' }}>
      <rect x={1} y={1} width={w - 2} height={h - 2} fill="none" stroke={DIM} strokeWidth={1.5} pathLength={1} strokeDasharray="1 2" strokeDashoffset={1 - p} />
    </svg>
    <div style={{ position: 'absolute', left: 18, top: -14, padding: '0 10px', background: BG, fontSize: 20, color: DIM, opacity: p }}>{title}</div>
    {children}
  </div>
);

const Line: React.FC<{ t: number; at: number; children: string; color?: string; size?: number }> = ({ t, at, children, color = FG, size = 30 }) => {
  if (t < at) return null;
  const n = Math.floor((t - at) * 2.4);
  return <div style={{ fontSize: size, lineHeight: 1.5, color, whiteSpace: 'pre' }}>{children.slice(0, n)}</div>;
};

export const MonoKinetic: React.FC<{ lang?: 'ru' | 'en' }> = ({ lang = 'ru' }) => {
  const f = useCurrentFrame();
  const c = COPY[lang];
  const caret = Math.floor(f / 8) % 2 ? 1 : 0;
  let body: ReactNode;

  if (f < B.motion) {
    body = (
      <div style={{ position: 'absolute', left: 140, top: 250 }}>
        {c.open.map((l, i) => (
          <div key={l} style={{ fontSize: 120, lineHeight: 1.2, color: i === 2 ? K.lime : FG, ...W(i === 2 ? 700 : 300) }}>
            <span style={{ color: DIM }}>&gt; </span>
            {decode(l, f, 1.1, i * 8)}
            {i === Math.min(2, Math.floor(f / 8)) && <span style={{ opacity: caret, color: K.lime }}>█</span>}
          </div>
        ))}
      </div>
    );
  } else if (f < B.s1) {
    const t = f - B.motion;
    body = (
      <div style={{ position: 'absolute', inset: 0, transform: `scale(${punch(f, B.motion, 0.06)})` }}>
        <Box x={140} y={220} w={1640} h={640} title="motion_engine" p={prog(t, 0, 14, ease.out)}>
          <div style={{ position: 'absolute', left: 80, top: 90, fontSize: 250, lineHeight: 1, letterSpacing: '-0.04em', color: K.lime, ...W(700) }}>{decode('MOTION', t, 2.2, 2)}</div>
          <div style={{ position: 'absolute', left: 80, top: 340, fontSize: 250, lineHeight: 1, letterSpacing: '-0.04em', color: FG, ...W(200) }}>{decode('ENGINE', t, 2.2, 8)}</div>
          <div style={{ position: 'absolute', right: 60, bottom: 40, fontSize: 24, color: DIM }}>{decode('ONEFLOW // v.1', t, 1, 16)}</div>
        </Box>
      </div>
    );
  } else if (f < B.s2) {
    const t = f - B.s1;
    const files = ['photo_01.jpg', 'photo_02.jpg', 'photo_03.jpg'];
    const typed = Math.floor(interpolate(t, [40, 62], [0, c.tags.join(', ').length], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }));
    body = (
      <>
        <div style={{ position: 'absolute', left: 140, top: 110, fontSize: 30, color: DIM }}>[01/03]</div>
        <div style={{ position: 'absolute', left: 140, top: 150, fontSize: 110, letterSpacing: '-0.03em', color: FG, ...W(500) }}>
          {decode(`${c.s1a} ${c.s1b}`, t, 1.2)}
        </div>
        <div style={{ position: 'absolute', left: 140, top: 340, width: 760 }}>
          {files.map((fl, i) => {
            const p = prog(t, 8 + i * 5, 26 + i * 5);
            return (
              <div key={fl} style={{ fontSize: 30, lineHeight: 1.9, color: FG, opacity: prog(t, 6 + i * 5, 8 + i * 5), whiteSpace: 'pre' }}>
                {fl}  <span style={{ color: p >= 1 ? K.lime : DIM }}>{blocks(p, 14)}</span> {p >= 1 ? '✓' : `${Math.round(p * 100)}%`}
              </div>
            );
          })}
        </div>
        {[0, 3, 1].map((k, i) => (
          <div key={i} style={{ position: 'absolute', left: 980 + i * 280, top: 340, opacity: prog(t, 10 + i * 5, 16 + i * 5) }}>
            <Box x={0} y={0} w={250} h={250} title={`0${i + 1}`} p={prog(t, 8 + i * 5, 22 + i * 5)}>
              <div style={{ position: 'absolute', inset: 12 }}>
                <Comp kind={k} t={t - 14 - i * 5} w={226} h={226} bg="#141416" fg={FG} ac={K.lime} r={0} />
              </div>
            </Box>
          </div>
        ))}
        <div style={{ position: 'absolute', left: 140, top: 700, fontSize: 34, color: FG, whiteSpace: 'pre', opacity: prog(t, 36, 40) }}>
          <span style={{ color: DIM }}>brief: </span>«{c.tags.join(', ').slice(0, typed)}»{t < 66 && <span style={{ opacity: caret, color: K.lime }}>█</span>}
        </div>
        <div style={{ position: 'absolute', left: 140, top: 790, fontSize: 44, color: K.lime, ...W(600), opacity: prog(t, 66, 70) }}>
          $ {c.make.toLowerCase()} <span style={{ color: DIM }}>{t > 76 ? '↵' : ''}</span>
        </div>
      </>
    );
  } else if (f < B.s3) {
    const t = f - B.s2;
    const pick = prog(t, 50, 58, ease.out);
    const kinds = [
      [0, 2, 3, 1],
      [3, 0, 4, 2],
      [1, 3, 2, 0],
    ];
    body = (
      <div style={{ position: 'absolute', inset: 0, transform: `scale(${punch(f, B.s2, 0.05)})` }}>
        <div style={{ position: 'absolute', left: 140, top: 110, fontSize: 30, color: DIM }}>[02/03]</div>
        <div style={{ position: 'absolute', left: 140, top: 150, fontSize: 96, letterSpacing: '-0.03em', color: FG, ...W(500) }}>{decode(c.s2, t, 1.2)}</div>
        {kinds.map((row, r) => (
          <div key={r} style={{ position: 'absolute', left: 140, top: 340 + r * 200 }}>
            <div style={{ position: 'absolute', left: 0, top: 50, fontSize: 40, color: r === 1 && pick > 0.5 ? K.lime : DIM, ...W(600) }}>{['A', 'B', 'C'][r]}</div>
            {row.map((k, i) => {
              const at = 10 + r * 6 + i * 3;
              const isB = r === 1;
              return (
                <div key={i} style={{ position: 'absolute', left: 80 + i * 300, top: 0, opacity: prog(t, at, at + 2) * (isB ? 1 : mix(1, 0.3, pick)), outline: isB ? `${3 * pick}px solid ${K.lime}` : 'none', outlineOffset: 6 }}>
                  <Comp kind={k} t={t - at} w={280} h={157.5} bg="#141416" fg={FG} ac={K.lime} r={0} />
                </div>
              );
            })}
          </div>
        ))}
        <div style={{ position: 'absolute', left: 1440, top: 560, fontSize: 36, color: K.lime, opacity: pick, whiteSpace: 'pre' }}>
          {decode(`[ ${c.picked.toLowerCase()} ]`, t, 1, 50)}
          {'\n'}
          <span style={{ color: FG, fontSize: 30 }}>{decode(c.s2b.toLowerCase(), t, 0.8, 54)}</span>
        </div>
      </div>
    );
  } else if (f < B.res) {
    const t = f - B.s3;
    const p = prog(t, 6, 50, ease.soft);
    body = (
      <>
        <div style={{ position: 'absolute', left: 140, top: 110, fontSize: 30, color: DIM }}>[03/03]</div>
        <div style={{ position: 'absolute', left: 140, top: 150, fontSize: 96, letterSpacing: '-0.03em', color: FG, ...W(500) }}>{decode(c.s3, t, 1.2)}</div>
        <div style={{ position: 'absolute', left: 130, top: 300, fontSize: 380, lineHeight: 1, letterSpacing: '-0.05em', color: K.lime, fontVariantNumeric: 'tabular-nums', ...W(mix(200, 800, p)) }}>
          {String(Math.round(p * 100)).padStart(3, '0')}%
        </div>
        <div style={{ position: 'absolute', left: 140, top: 720, fontSize: 52, color: p >= 1 ? K.lime : FG, letterSpacing: '-0.02em' }}>{blocks(p, 40)}</div>
        <div style={{ position: 'absolute', left: 140, top: 820, fontSize: 36, color: K.lime, opacity: prog(t, 52, 56), whiteSpace: 'pre' }}>
          ✓ {c.done.toLowerCase()} → oneflow_glow.mp4
        </div>
      </>
    );
  } else if (f < B.end) {
    const t = f - B.res;
    body = (
      <>
        <Box x={980} y={200} w={800} h={680} title="preview" p={prog(t, 0, 14, ease.out)}>
          <div style={{ position: 'absolute', inset: 16 }}>
            <Comp kind={1} t={t - 4} w={768} h={420} bg="#141416" fg={FG} ac={K.lime} r={0} />
            <div style={{ display: 'flex', gap: 16, marginTop: 16 }}>
              {[0, 2, 3].map((k, i) => (
                <Comp key={k} kind={k} t={t - 8 - i * 3} w={245} h={196} bg="#141416" fg={FG} ac={K.lime} r={0} />
              ))}
            </div>
          </div>
        </Box>
        <div style={{ position: 'absolute', left: 140, top: 300, fontSize: 170, lineHeight: 1.05, letterSpacing: '-0.04em' }}>
          <div style={{ color: FG, ...W(300) }}>{decode(c.res1, t, 2)}</div>
          <div style={{ color: K.lime, ...W(700) }}>{decode(c.res2, t, 2, 6)}</div>
        </div>
      </>
    );
  } else {
    const t = f - B.end;
    body = (
      <>
        <div style={{ position: 'absolute', left: 140, top: 250, fontSize: 30, color: DIM }}>{decode('ONEFLOW // MOTION ENGINE', t, 0.6)}</div>
        <div style={{ position: 'absolute', left: 140, top: 320, fontSize: 104, lineHeight: 1.12, letterSpacing: '-0.04em', color: FG, ...W(300) }}>
          {decode(c.end1, t, 0.7, 2)}
          <br />
          <span style={{ color: K.lime, ...W(700) }}>{decode(c.end2, t, 0.9, 8)}</span>
          <span style={{ opacity: caret, color: K.lime }}>█</span>
        </div>
        <div style={{ position: 'absolute', left: 140, top: 640, fontSize: 40, color: BG, background: K.lime, padding: '18px 30px', ...W(600), opacity: prog(t, 16, 22) }}>[ {c.cta} → ]</div>
      </>
    );
  }

  return (
    <AbsoluteFill style={{ background: BG, fontFamily: MONO, overflow: 'hidden' }}>
      {/* faint scan grid */}
      <div style={{ position: 'absolute', inset: 0, backgroundImage: 'linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px)', backgroundSize: '100% 6px' }} />
      {body}
      <div style={{ position: 'absolute', left: 140, right: 140, bottom: 54, display: 'flex', justifyContent: 'space-between', fontSize: 20, color: DIM }}>
        <span>oneflow ~ motion-engine</span>
        <span style={{ fontVariantNumeric: 'tabular-nums' }}>{(f / 30).toFixed(2)}s</span>
      </div>
    </AbsoluteFill>
  );
};
