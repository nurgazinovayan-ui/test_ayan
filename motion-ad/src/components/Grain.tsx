import { AbsoluteFill } from 'remotion';
import { HEIGHT, WIDTH } from '../theme';

/** Barely visible film grain; the noise seed is derived from the frame, so renders are repeatable. */
export const Grain: React.FC<{ frame: number }> = ({ frame }) => {
  const seed = Math.floor(frame / 2) % 24;
  return (
    <AbsoluteFill style={{ pointerEvents: 'none', mixBlendMode: 'overlay', opacity: 0.5 }}>
      <svg width={WIDTH} height={HEIGHT}>
        <filter id={`grain-${seed}`} x="0" y="0" width="100%" height="100%">
          <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed={seed} stitchTiles="stitch" />
          <feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.16 0" />
        </filter>
        <rect width={WIDTH} height={HEIGHT} filter={`url(#grain-${seed})`} />
      </svg>
    </AbsoluteFill>
  );
};
