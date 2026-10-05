import type { ReactNode } from 'react';
import { C, GRADIENT, mix } from '../theme';
import type { Rect } from '../theme';

/** Positioned box with the shared panel look (hairline border, rounded corners, near-black fill). */
export const Panel: React.FC<{
  rect: Rect;
  glow?: number;
  border?: number;
  fill?: string;
  opacity?: number;
  dx?: number;
  children?: ReactNode;
}> = ({ rect, glow = 0, border = 1, fill = '#111115', opacity = 1, dx = 0, children }) => (
  <div
    style={{
      position: 'absolute',
      left: rect.x + dx,
      top: rect.y,
      width: rect.w,
      height: rect.h,
      borderRadius: rect.r,
      background: fill,
      opacity,
      overflow: 'hidden',
      boxShadow: [
        `inset 0 0 0 1px rgba(255,255,255,${0.1 * border + 0.35 * glow})`,
        `inset 0 1px 0 rgba(255,255,255,${0.06 * border})`,
        `0 0 ${36 * glow}px ${-4 + 6 * glow}px rgba(59,123,255,${0.55 * glow})`,
        `0 24px 60px -30px rgba(0,0,0,${0.8 * border})`,
      ].join(', '),
    }}
  >
    {children}
  </div>
);

// ---- prompt field ------------------------------------------------------------------------------

export const PROMPT = 'Создай динамичную анимацию для моего бренда';

export const PromptContent: React.FC<{
  chars: number;
  caretOn: boolean;
  press: number;
  ripple: number;
  opacity: number;
}> = ({ chars, caretOn, press, ripple, opacity }) => (
  <div style={{ position: 'absolute', inset: 0, padding: '18px 20px', opacity }}>
    <div style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: 13, color: C.ink3, letterSpacing: '0.02em' }}>
      <div style={{ width: 6, height: 6, borderRadius: 9, background: C.blue, boxShadow: `0 0 8px ${C.blue}` }} />
      Опишите идею
    </div>
    <div style={{ marginTop: 12, fontSize: 20, lineHeight: '27px', color: C.ink, letterSpacing: '-0.01em', width: 480 }}>
      {PROMPT.slice(0, chars)}
      <span
        style={{
          display: 'inline-block',
          width: 2,
          height: 22,
          marginLeft: 2,
          verticalAlign: '-4px',
          background: C.blueSoft,
          opacity: caretOn ? 1 : 0,
        }}
      />
    </div>
    {/* «Создать» */}
    <div style={{ position: 'absolute', right: 16, bottom: 16, width: 116, height: 40 }}>
      <div
        style={{
          position: 'absolute',
          inset: 0,
          borderRadius: 99,
          border: `1px solid ${C.blueSoft}`,
          opacity: (1 - ripple) * (ripple > 0 ? 0.8 : 0),
          transform: `scale(${1 + ripple * 0.5}, ${1 + ripple * 1.1})`,
        }}
      />
      <div
        style={{
          position: 'absolute',
          inset: 0,
          borderRadius: 99,
          background: `linear-gradient(90deg, ${C.blue}, #6F6BFF)`,
          boxShadow: `0 8px 24px -8px rgba(59,123,255,0.8), inset 0 1px 0 rgba(255,255,255,0.3)`,
          transform: `scale(${1 - press * 0.07})`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: 8,
          color: '#fff',
          fontSize: 15,
          fontWeight: 500,
        }}
      >
        Создать
        <svg width="14" height="14" viewBox="0 0 14 14">
          <path d="M2 7h9M7.5 3.5 11 7l-3.5 3.5" stroke="#fff" strokeWidth="1.6" fill="none" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </div>
    </div>
  </div>
);

// ---- process cards -----------------------------------------------------------------------------

const Icon: React.FC<{ kind: 0 | 1 | 2 }> = ({ kind }) => (
  <svg width="30" height="30" viewBox="0 0 30 30">
    {kind === 0 && (
      <>
        <circle cx="13" cy="16" r="9" fill="none" stroke={C.ink2} strokeWidth="1.3" />
        <circle cx="23" cy="7" r="3" fill={C.blue} />
      </>
    )}
    {kind === 1 && (
      <>
        <circle cx="11" cy="15" r="8" fill={C.blue} fillOpacity="0.9" />
        <circle cx="19" cy="15" r="8" fill={C.violet} fillOpacity="0.75" />
      </>
    )}
    {kind === 2 && (
      <>
        <rect x="2" y="9" width="26" height="12" rx="6" fill="none" stroke={C.ink2} strokeWidth="1.3" />
        <circle cx="9" cy="15" r="3.4" fill={C.violet} />
      </>
    )}
  </svg>
);

export const CardFace: React.FC<{ index: number; title: string; opacity: number; lit: number }> = ({
  index,
  title,
  opacity,
  lit,
}) => (
  <div style={{ position: 'absolute', inset: 0, padding: '14px 16px', opacity }}>
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
      <span style={{ fontSize: 12, color: C.ink3, letterSpacing: '0.12em', fontVariantNumeric: 'tabular-nums', marginTop: 4 }}>
        0{index + 1}
      </span>
      <Icon kind={index as 0 | 1 | 2} />
    </div>
    <div
      style={{
        position: 'absolute',
        left: 16,
        bottom: 16,
        fontSize: 22,
        fontWeight: 500,
        letterSpacing: '-0.02em',
        color: C.ink,
      }}
    >
      {title}
    </div>
    <div
      style={{
        position: 'absolute',
        left: 16,
        right: 16,
        bottom: 0,
        height: 2,
        background: GRADIENT,
        opacity: lit,
        transform: `scaleX(${mix(0.2, 1, lit)})`,
      }}
    />
  </div>
);
