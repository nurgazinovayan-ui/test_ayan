import type { CSSProperties, ReactNode } from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame } from 'remotion';
import '../fonts';
import { FONT } from '../fonts';
import { ease, mix, prog } from '../theme';
import { LOGO } from '../explainer/shared';

/*
 * ONEFLOW Motion Engine — kinetic typography, 1920×1080, 30 fps, 15 s, silent.
 * Only type and geometry: no product shots. The variable weight of Geist is animated, backgrounds
 * cut between grey, black and lime on the beat, and the "photos", storyboards and the finished video
 * are abstract compositions of circles, capsules and lines.
 *
 *   0– 32  «Ваши фото. Ваша идея. Ваш ролик.»
 *  32– 74  MOTION / ENGINE (black)
 *  74–162  01 · upload + describe (grey)
 * 162–246  02 · storyboards, pick one (black)
 * 246–318  03 · render 0→100 %, MP4 (lime)
 * 318–390  the finished piece (grey)
 * 390–450  end card
 */

export const KIN_W = 1920;
export const KIN_H = 1080;
export const KIN_DURATION = 450;

export const K = { grey: '#e5e5e5', ink: '#111111', lime: '#cdf158', white: '#f7f7f7', mid: '#8a8a8a' };
export const B = { motion: 32, s1: 74, s2: 162, s3: 246, res: 318, end: 390 };

export const COPY = {
  ru: {
    open: ['Ваши фото.', 'Ваша идея.', 'Ваш ролик.'],
    s1a: 'Загрузите',
    s1b: 'фото',
    s1c: 'Опишите задачу',
    tags: ['лето', 'свежо', 'ярко', 'продукт в фокусе'],
    make: 'Сделать раскадровку',
    s2: 'Раскадровки',
    s2b: 'Выберите лучшую',
    picked: 'Выбрано',
    s3: 'Рендер',
    done: 'Готово',
    res1: 'Ролик',
    res2: 'готов.',
    end1: 'Ролик из ваших фото',
    end2: 'за пару минут',
    cta: 'Попробовать Motion Engine',
  },
  en: {
    open: ['Your photos.', 'Your idea.', 'Your video.'],
    s1a: 'Upload',
    s1b: 'photos',
    s1c: 'Describe the task',
    tags: ['summer', 'fresh', 'bright', 'product in focus'],
    make: 'Make storyboard',
    s2: 'Storyboards',
    s2b: 'Pick the best',
    picked: 'Selected',
    s3: 'Render',
    done: 'Done',
    res1: 'Video',
    res2: 'ready.',
    end1: 'A video from your photos',
    end2: 'in minutes',
    cta: 'Try Motion Engine',
  },
};
export type Copy = (typeof COPY)['ru'];

// ---- helpers --------------------------------------------------------------------------------------

/** Variable-weight text. */
export const W = (w: number): CSSProperties => ({ fontWeight: Math.round(w), fontVariationSettings: `'wght' ${w.toFixed(0)}` });

export const Mask: React.FC<{ y: number; children: ReactNode; style?: CSSProperties }> = ({ y, children, style }) => (
  <div style={{ overflow: 'hidden', padding: '0.06em 0 0.12em', margin: '-0.06em 0 -0.12em', ...style }}>
    <div style={{ transform: `translateY(${y}%)` }}>{children}</div>
  </div>
);

const Scene: React.FC<{ bg: string; s?: number; ox?: number; oy?: number; children: ReactNode }> = ({ bg, s = 1, ox = 960, oy = 540, children }) => (
  <AbsoluteFill style={{ background: bg, overflow: 'hidden' }}>
    <AbsoluteFill style={{ transform: `scale(${s})`, transformOrigin: `${ox}px ${oy}px` }}>{children}</AbsoluteFill>
  </AbsoluteFill>
);

export const punch = (f: number, at: number, k = 0.08) => 1 + k * (1 - spring({ frame: f - at, fps: 30, config: { damping: 11, stiffness: 170 } }));

/**
 * Abstract composition — the stand-in for a photo / storyboard frame / the finished video.
 * kind 0: circle pops and drifts · 1: capsule stretches · 2: lines draw and fold into a grid ·
 * 3: two blocks slide past each other · 4: big letter through a mask.
 */
export const Comp: React.FC<{ kind: number; t: number; w: number; h: number; bg: string; fg: string; ac: string; r?: number }> = ({ kind, t, w, h, bg, fg, ac, r = 18 }) => {
  const u = Math.min(w, h);
  const sp = spring({ frame: t, fps: 30, config: { damping: 13, stiffness: 120 } });
  const live = Math.sin(t / 14);
  let body: ReactNode = null;
  if (kind === 0) {
    const d = u * 0.56 * sp;
    body = <div style={{ position: 'absolute', left: w / 2 - d / 2 + live * u * 0.06, top: h / 2 - d / 2, width: d, height: d, borderRadius: '50%', background: ac }} />;
  } else if (kind === 1) {
    const st = prog(t, 6, 22, ease.inOut);
    const ch = u * 0.3 * sp;
    const cw = mix(ch, w * 0.72, st);
    body = (
      <>
        <div style={{ position: 'absolute', left: w / 2 - cw / 2, top: h / 2 - ch / 2, width: cw, height: ch, borderRadius: 999, background: fg }} />
        <div style={{ position: 'absolute', left: w / 2 - cw / 2 + ch * 0.18 + (cw - ch) * (0.5 + live * 0.5), top: h / 2 - ch * 0.32, width: ch * 0.64, height: ch * 0.64, borderRadius: 999, background: ac }} />
      </>
    );
  } else if (kind === 2) {
    body = (
      <>
        {[0, 1, 2, 3, 4].map((i) => {
          const fold = prog(t, 10, 26, ease.inOut);
          const y = mix(h / 2 + (i - 2) * 4, h * (0.18 + i * 0.16), fold);
          return <div key={i} style={{ position: 'absolute', left: w * 0.1, top: y, width: w * 0.8 * prog(t, i * 2, 10 + i * 2, ease.out), height: Math.max(2, u * 0.012), background: i === 2 ? ac : fg }} />;
        })}
        {[1, 2, 3].map((j) => (
          <div key={`v${j}`} style={{ position: 'absolute', left: w * (0.1 + j * 0.2), top: h * 0.18, width: Math.max(2, u * 0.012), height: h * 0.64 * prog(t, 18 + j * 2, 28 + j * 2, ease.out), background: fg, opacity: 0.5 }} />
        ))}
      </>
    );
  } else if (kind === 3) {
    const s = u * 0.42;
    const k = prog(t, 2, 18, ease.out);
    body = (
      <>
        <div style={{ position: 'absolute', left: mix(-s, w * 0.24, k) + live * 6, top: h / 2 - s / 2, width: s, height: s, borderRadius: s * 0.14, background: ac }} />
        <div style={{ position: 'absolute', left: mix(w, w * 0.42, k) - live * 6, top: h / 2 - s / 2 + s * 0.12, width: s, height: s, borderRadius: s * 0.14, background: fg, mixBlendMode: 'multiply', opacity: 0.92 }} />
      </>
    );
  } else {
    body = (
      <div style={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', overflow: 'hidden' }}>
        <div style={{ fontSize: h * 0.9, lineHeight: 1, color: fg, ...W(mix(200, 900, prog(t, 4, 24))), transform: `translateY(${mix(100, 0, prog(t, 0, 14, ease.out))}%)`, letterSpacing: '-0.06em' }}>
          M<span style={{ color: ac }}>.</span>
        </div>
      </div>
    );
  }
  return (
    <div style={{ position: 'relative', width: w, height: h, borderRadius: r, overflow: 'hidden', background: bg }}>
      {body}
    </div>
  );
};

const Pill: React.FC<{ children: ReactNode; bg?: string; fg?: string; style?: CSSProperties }> = ({ children, bg = K.ink, fg = '#fff', style }) => (
  <div style={{ display: 'inline-flex', alignItems: 'center', gap: 14, height: 76, padding: '0 36px', borderRadius: 999, background: bg, color: fg, fontSize: 32, ...W(500), whiteSpace: 'nowrap', ...style }}>
    {children}
  </div>
);

// ---- the film ---------------------------------------------------------------------------------------

export const KineticAd: React.FC<{ lang?: 'ru' | 'en' }> = ({ lang = 'ru' }) => {
  const f = useCurrentFrame();
  const c: Copy = COPY[lang];
  let scene: ReactNode = null;

  if (f < B.motion) {
    // ---------------------------------------------------------- opening triad
    scene = (
      <Scene bg={K.grey} s={mix(1, 1.06, prog(f, 0, B.motion, ease.soft))} ox={300}>
        <div style={{ position: 'absolute', left: 140, top: 170, fontSize: 200, lineHeight: 1.02, letterSpacing: '-0.055em', color: K.ink }}>
          {c.open.map((l, i) => {
            const a = i * 8;
            const k = prog(f, a, a + 10, ease.out);
            const last = i === 2;
            return (
              <Mask key={l} y={mix(110, 0, k)}>
                <div style={{ ...W(mix(100, last ? 800 : 300, prog(f, a + 2, a + 16, ease.out))), position: 'relative', display: 'inline-block' }}>
                  {last && <span style={{ position: 'absolute', left: -8, right: -8, bottom: 26, height: 70, background: K.lime, transform: `scaleX(${prog(f, 20, 30, ease.inOut)})`, transformOrigin: 'left' }} />}
                  <span style={{ position: 'relative' }}>{l}</span>
                </div>
              </Mask>
            );
          })}
        </div>
      </Scene>
    );
  } else if (f < B.s1) {
    // ---------------------------------------------------------- MOTION / ENGINE
    const t = f - B.motion;
    const letters = 'MOTION'.split('');
    scene = (
      <Scene bg={K.ink} s={punch(f, B.motion, 0.12) * mix(1, 1.08, prog(t, 0, 42, ease.soft))}>
        <div style={{ position: 'absolute', left: 0, right: 0, top: 190, textAlign: 'center', fontSize: 380, lineHeight: 0.9, letterSpacing: '-0.05em', color: K.lime }}>
          {letters.map((ch, i) => {
            const k = prog(t, i * 2, 10 + i * 2, ease.out);
            return (
              <span key={i} style={{ display: 'inline-block', overflow: 'hidden', verticalAlign: 'top', padding: '0 0.01em' }}>
                <span style={{ display: 'inline-block', transform: `translateY(${mix(105, 0, k)}%)`, ...W(mix(900, 300 + 200 * Math.sin((t - i * 3) / 6), prog(t, 10, 30))) }}>{ch}</span>
              </span>
            );
          })}
        </div>
        <div style={{ position: 'absolute', left: 0, right: 0, top: 560, textAlign: 'center', fontSize: 300, lineHeight: 0.9, letterSpacing: '0.04em', color: 'transparent', WebkitTextStroke: '3px #f7f7f7', ...W(700) }}>
          <Mask y={mix(110, 0, prog(t, 10, 22, ease.out))}>ENGINE</Mask>
        </div>
        <div style={{ position: 'absolute', left: 0, right: 0, top: 120, textAlign: 'center', fontSize: 26, letterSpacing: '0.4em', color: '#f7f7f7', opacity: prog(t, 16, 24) }}>ONEFLOW</div>
        {/* lime bar wipes into the next scene */}
        <div style={{ position: 'absolute', left: 0, right: 0, bottom: 0, height: `${prog(t, 34, 42, ease.in) * 100}%`, background: K.grey }} />
      </Scene>
    );
  } else if (f < B.s2) {
    // ---------------------------------------------------------- 01 · upload + describe
    const t = f - B.s1;
    const part2 = prog(t, 40, 52, ease.inOut);
    const typed = Math.floor(interpolate(t, [44, 62], [0, c.s1c.length], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }));
    const press = t < 74 ? 0 : t < 77 ? prog(t, 74, 77) : 1 - prog(t, 77, 84);
    scene = (
      <Scene bg={K.grey} s={mix(1, 1.05, prog(t, 0, 88, ease.soft))}>
        <div style={{ position: 'absolute', left: 120, top: 70, fontSize: 200, lineHeight: 1, letterSpacing: '-0.06em', color: K.ink }}>
          <Mask y={mix(110, 0, prog(t, 0, 10, ease.out))}>
            <span style={W(mix(100, 200, prog(t, 0, 30)))}>01</span>
          </Mask>
        </div>
        {/* «Загрузите фото» + abstract photos */}
        <div style={{ position: 'absolute', left: 420, top: 96, fontSize: 170, lineHeight: 1, letterSpacing: '-0.05em', color: K.ink, transform: `translateY(${-part2 * 340}px)`, opacity: 1 - part2 }}>
          <Mask y={mix(110, 0, prog(t, 2, 14, ease.out))}>
            <span style={W(mix(200, 700, prog(t, 4, 24, ease.out)))}>{c.s1a}</span> <span style={{ ...W(200), color: K.mid }}>{c.s1b}</span>
          </Mask>
        </div>
        {[0, 3, 1].map((kind, i) => {
          const d = spring({ frame: t - 10 - i * 5, fps: 30, config: { damping: 12, stiffness: 150 } });
          return (
            <div key={i} style={{ position: 'absolute', left: 420 + i * 470, top: 380 + mix(700, 0, d) + part2 * 700, opacity: 1 - part2, transform: `scale(${mix(1, 0.62, part2)})`, transformOrigin: `${-420 - i * 470 + 120}px 700px` }}>
              <Comp kind={kind} t={t - 12 - i * 5} w={430} h={520} bg={i === 1 ? K.ink : K.white} fg={i === 1 ? K.white : K.ink} ac={K.lime} r={32} />
            </div>
          );
        })}
        {/* «Опишите задачу» typed huge, tags fly in, click */}
        {t >= 40 && (
          <>
            <div style={{ position: 'absolute', left: 120, top: 330, fontSize: 150, lineHeight: 1.05, letterSpacing: '-0.05em', color: K.ink, ...W(300) }}>
              {c.s1c.slice(0, typed)}
              <span style={{ display: 'inline-block', width: 14, height: 140, marginLeft: 10, verticalAlign: '-18px', background: K.lime, opacity: t < 64 || Math.floor(t / 7) % 2 ? 1 : 0 }} />
            </div>
            <div style={{ position: 'absolute', left: 120, top: 560, display: 'flex', gap: 18 }}>
              {c.tags.map((tag, i) => {
                const k = spring({ frame: t - 56 - i * 3, fps: 30, config: { damping: 12, stiffness: 180 } });
                return (
                  <div key={tag} style={{ transform: `translateY(${mix(120, 0, k)}px) scale(${mix(0.6, 1, k)})`, opacity: Math.min(1, k * 2), padding: '14px 30px', borderRadius: 999, border: `3px solid ${K.ink}`, fontSize: 40, ...W(500), background: i === 0 ? K.lime : 'transparent' }}>
                    {tag}
                  </div>
                );
              })}
            </div>
            <div style={{ position: 'absolute', left: 120, top: 760, opacity: prog(t, 66, 72), transform: `translateX(${mix(-60, 0, prog(t, 66, 74, ease.out))}px) scale(${1 - press * 0.07})` }}>
              <Pill style={{ height: 110, fontSize: 48, padding: '0 54px' }}>
                {c.make} <span style={{ color: K.lime }}>→</span>
              </Pill>
            </div>
            {t >= 76 && (
              <div style={{ position: 'absolute', left: 120 + 330 - 400 * prog(t, 76, 88), top: 815 - 400 * prog(t, 76, 88), width: 800 * prog(t, 76, 88), height: 800 * prog(t, 76, 88), borderRadius: '50%', border: `6px solid ${K.lime}`, opacity: 1 - prog(t, 76, 88) }} />
            )}
          </>
        )}
      </Scene>
    );
  } else if (f < B.s3) {
    // ---------------------------------------------------------- 02 · storyboards (black)
    const t = f - B.s2;
    const up = prog(t, 14, 28, ease.inOut);
    const pick = prog(t, 52, 62, ease.out);
    const FW = 300;
    const FH = 168.75;
    const kinds = [
      [0, 2, 3, 1],
      [3, 0, 4, 2],
      [1, 3, 2, 0],
    ];
    scene = (
      <Scene bg={K.ink} s={punch(f, B.s2, 0.1) * mix(1, 1.05, prog(t, 0, 84, ease.soft))}>
        <div style={{ position: 'absolute', left: 120, top: mix(330, 60, up), fontSize: mix(260, 120, up), lineHeight: 1, letterSpacing: '-0.055em', color: K.white }}>
          <Mask y={mix(110, 0, prog(t, 0, 10, ease.out))}>
            <span style={{ ...W(mix(200, 800, prog(t, 0, 16))), color: K.lime }}>02</span> <span style={W(mix(800, 300, prog(t, 4, 24)))}>{c.s2}</span>
          </Mask>
        </div>
        {kinds.map((row, r) =>
          row.map((kind, i) => {
            const at = 22 + r * 5 + i * 3;
            const k = spring({ frame: t - at, fps: 30, config: { damping: 13, stiffness: 160 } });
            const isB = r === 1;
            return (
              <div
                key={`${r}${i}`}
                style={{
                  position: 'absolute',
                  left: 120 + i * (FW + 24),
                  top: 260 + r * (FH + 28),
                  opacity: Math.min(1, k * 2) * (isB ? 1 : mix(1, 0.28, pick)),
                  transform: `scale(${mix(0.5, 1, k) * (isB ? mix(1, 1.04, pick) : 1)})`,
                  borderRadius: 20,
                  boxShadow: isB ? `0 0 0 ${5 * pick}px ${K.lime}` : 'none',
                }}
              >
                <Comp kind={kind} t={t - at} w={FW} h={FH} bg={isB && pick > 0.5 ? K.lime : '#1d1d1f'} fg={isB && pick > 0.5 ? K.ink : K.white} ac={isB && pick > 0.5 ? K.white : K.lime} r={20} />
              </div>
            );
          }),
        )}
        <div style={{ position: 'absolute', left: 1460, top: 300, width: 360, color: K.white }}>
          <Mask y={mix(110, 0, prog(t, 56, 66, ease.out))}>
            <div style={{ fontSize: 76, lineHeight: 1.05, letterSpacing: '-0.04em', ...W(300) }}>{c.s2b}</div>
          </Mask>
          <div style={{ marginTop: 30, opacity: pick }}>
            <Pill bg={K.lime} fg={K.ink} style={{ height: 64, fontSize: 28 }}>
              ✓ {c.picked}
            </Pill>
          </div>
        </div>
      </Scene>
    );
  } else if (f < B.res) {
    // ---------------------------------------------------------- 03 · render (lime)
    const t = f - B.s3;
    const p = prog(t, 8, 52, ease.soft);
    const done = prog(t, 52, 60, ease.out);
    scene = (
      <Scene bg={K.lime} s={punch(f, B.s3, 0.1) * punch(f, B.s3 + 52, 0.06)}>
        <div style={{ position: 'absolute', left: 120, top: 70, fontSize: 110, lineHeight: 1, letterSpacing: '-0.05em', color: K.ink }}>
          <Mask y={mix(110, 0, prog(t, 0, 10, ease.out))}>
            <span style={W(800)}>03</span> <span style={W(300)}>{c.s3}</span>
          </Mask>
        </div>
        <div style={{ position: 'absolute', left: 100, top: 210, fontSize: 520, lineHeight: 1, letterSpacing: '-0.07em', color: K.ink, fontVariantNumeric: 'tabular-nums', ...W(mix(100, 900, p)) }}>
          {Math.round(p * 100)}
          <span style={W(100)}>%</span>
        </div>
        <div style={{ position: 'absolute', left: 120, right: 120, top: 830, height: 6, background: 'rgba(17,17,17,0.15)' }}>
          <div style={{ width: `${p * 100}%`, height: '100%', background: K.ink }} />
        </div>
        <div style={{ position: 'absolute', right: 120, top: 120, display: 'flex', gap: 18, opacity: done, transform: `translateY(${mix(40, 0, done)}px)` }}>
          <Pill style={{ height: 96, fontSize: 44 }}>MP4</Pill>
          <Pill bg={K.white} fg={K.ink} style={{ height: 96, fontSize: 44 }}>
            ✓ {c.done}
          </Pill>
        </div>
      </Scene>
    );
  } else if (f < B.end) {
    // ---------------------------------------------------------- the finished piece
    const t = f - B.res;
    const sp = spring({ frame: t, fps: 30, config: { damping: 12, stiffness: 120 } });
    const stretch = prog(t, 10, 26, ease.inOut);
    const ch = 300 * sp;
    const cw = mix(ch, 640, stretch);
    scene = (
      <Scene bg={K.grey} s={mix(1.04, 1, prog(t, 0, 72, ease.soft))}>
        {[0, 1, 2, 3, 4, 5].map((i) => {
          const fold = prog(t, 18, 34, ease.inOut);
          const y = mix(540 + (i - 2.5) * 8, 120 + i * 170, fold);
          return <div key={i} style={{ position: 'absolute', left: 0, top: y, width: 1920 * prog(t, 2 + i * 2, 16 + i * 2, ease.out), height: 2, background: K.ink, opacity: mix(0.6, 0.12, fold) }} />;
        })}
        <div style={{ position: 'absolute', left: 1560 - cw / 2, top: 600 - ch / 2, width: cw, height: ch, borderRadius: 999, background: K.ink }} />
        <div style={{ position: 'absolute', left: 1560 - cw / 2 + ch * 0.2 + (cw - ch) * (0.5 + 0.5 * Math.sin(t / 10)), top: 600 - ch * 0.3, width: ch * 0.6, height: ch * 0.6, borderRadius: 999, background: K.lime }} />
        <div style={{ position: 'absolute', left: 120, top: 150, fontSize: 280, lineHeight: 0.95, letterSpacing: '-0.06em', color: K.ink }}>
          <Mask y={mix(110, 0, prog(t, 4, 16, ease.out))}>
            <span style={W(mix(100, 800, prog(t, 4, 30)))}>{c.res1}</span>
          </Mask>
          <Mask y={mix(110, 0, prog(t, 8, 20, ease.out))}>
            <span style={W(mix(800, 200, prog(t, 8, 34)))}>{c.res2}</span>
          </Mask>
        </div>
      </Scene>
    );
  } else {
    // ---------------------------------------------------------- end card
    const t = f - B.end;
    const e = [prog(t, 0, 12), prog(t, 4, 16), prog(t, 8, 20), prog(t, 12, 24)];
    scene = (
      <Scene bg={K.grey} s={mix(1.03, 1, prog(t, 0, 60, ease.soft))}>
        <div style={{ position: 'absolute', right: -160, top: 160, width: 760, height: 760, borderRadius: '50%', background: K.lime, transform: `scale(${spring({ frame: t, fps: 30, config: { damping: 16, stiffness: 90 } })})` }} />
        <div style={{ position: 'absolute', right: 240, top: 470, width: 440 * prog(t, 6, 22, ease.out), height: 150, borderRadius: 999, background: K.ink }} />
        <div style={{ position: 'absolute', left: 140, top: 250, color: K.ink }}>
          <Mask y={mix(110, 0, e[0])}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 18 }}>
              <svg width="72" height="72" viewBox="0 0 96 96">
                <rect width="96" height="96" rx="22" fill={K.ink} />
                <g transform="translate(10 13.2)">
                  <path d={LOGO} fill="#fff" />
                </g>
              </svg>
              <span style={{ fontSize: 40, letterSpacing: '-0.02em', ...W(600) }}>ONEFLOW</span>
              <span style={{ fontSize: 40, color: K.mid, ...W(300) }}>Motion Engine</span>
            </div>
          </Mask>
          <div style={{ marginTop: 40, fontSize: 112, lineHeight: 1.04, letterSpacing: '-0.05em', whiteSpace: 'nowrap' }}>
            <Mask y={mix(110, 0, e[1])}>
              <span style={W(mix(100, 250, e[1]))}>{c.end1}</span>
            </Mask>
            <Mask y={mix(110, 0, e[2])}>
              <span style={{ position: 'relative', display: 'inline-block', ...W(mix(200, 700, prog(t, 10, 26))) }}>
                <span style={{ position: 'absolute', left: -6, right: -6, bottom: 14, height: 38, background: K.lime, transform: `scaleX(${prog(t, 18, 30, ease.inOut)})`, transformOrigin: 'left' }} />
                <span style={{ position: 'relative' }}>{c.end2}</span>
              </span>
            </Mask>
          </div>
          <div style={{ marginTop: 56, opacity: e[3], transform: `translateY(${mix(40, 0, e[3])}px)` }}>
            <Pill>
              {c.cta} <span style={{ color: K.lime }}>→</span>
            </Pill>
          </div>
        </div>
      </Scene>
    );
  }

  // small fixed HUD
  const step = f < B.s1 ? '' : f < B.s2 ? '01' : f < B.s3 ? '02' : f < B.res ? '03' : '';
  const dark = f >= B.motion && f < B.s1 ? true : f >= B.s2 && f < B.s3;
  return (
    <AbsoluteFill style={{ fontFamily: FONT }}>
      {scene}
      {f >= B.motion && f < B.end && (
        <>
          <div style={{ position: 'absolute', left: 120, bottom: 48, fontSize: 22, letterSpacing: '0.16em', color: dark ? K.white : K.ink, opacity: 0.7 }}>ONEFLOW · MOTION ENGINE</div>
          <div style={{ position: 'absolute', right: 120, bottom: 48, fontSize: 22, letterSpacing: '0.16em', color: dark ? K.white : K.ink, opacity: 0.7, fontVariantNumeric: 'tabular-nums' }}>{step ? `${step} / 03` : ''}</div>
        </>
      )}
    </AbsoluteFill>
  );
};
