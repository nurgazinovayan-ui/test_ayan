import { AbsoluteFill } from 'remotion';
import { C, HEIGHT, WIDTH, mix } from '../theme';

/** Near-black field, a faint interface grid and two slow accent glows that follow the action. */
export const Background: React.FC<{ frame: number; focusX: number }> = ({ frame, focusX }) => {
  const drift = Math.sin(frame / 70) * 18;
  return (
    <AbsoluteFill style={{ backgroundColor: C.bg }}>
      <svg width={WIDTH} height={HEIGHT} style={{ position: 'absolute', inset: 0 }}>
        <defs>
          <radialGradient id="grid-fade" cx="62%" cy="50%" r="70%">
            <stop offset="0%" stopColor="#fff" stopOpacity="1" />
            <stop offset="100%" stopColor="#fff" stopOpacity="0" />
          </radialGradient>
          <mask id="grid-mask">
            <rect width={WIDTH} height={HEIGHT} fill="url(#grid-fade)" />
          </mask>
          <pattern id="grid" width="48" height="48" patternUnits="userSpaceOnUse" x={-frame * 0.12} y="22">
            <path d="M48 0H0V48" fill="none" stroke="#fff" strokeOpacity="0.045" strokeWidth="1" />
          </pattern>
        </defs>
        <rect width={WIDTH} height={HEIGHT} fill="url(#grid)" mask="url(#grid-mask)" />
      </svg>
      <div
        style={{
          position: 'absolute',
          left: focusX - 360 + drift,
          top: -260,
          width: 720,
          height: 520,
          borderRadius: '50%',
          background: `radial-gradient(closest-side, rgba(59, 123, 255, 0.20), rgba(59, 123, 255, 0) 100%)`,
        }}
      />
      <div
        style={{
          position: 'absolute',
          left: mix(-160, 120, (Math.sin(frame / 90) + 1) / 2),
          top: 170,
          width: 640,
          height: 460,
          borderRadius: '50%',
          background: `radial-gradient(closest-side, rgba(167, 139, 250, 0.13), rgba(167, 139, 250, 0) 100%)`,
        }}
      />
    </AbsoluteFill>
  );
};
