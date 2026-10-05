import type { CSSProperties, ReactNode } from 'react';
import { mix } from '../theme';

/**
 * One line of text that rises into view through its own mask and leaves upwards through it.
 * `enter` and `exit` are 0→1 progress values computed from the frame by the caller.
 */
export const MaskLine: React.FC<{
  enter: number;
  exit?: number;
  children: ReactNode;
  style?: CSSProperties;
}> = ({ enter, exit = 0, children, style }) => {
  const y = exit > 0 ? mix(0, -112, exit) : mix(112, 0, enter);
  return (
    // padding keeps descenders (у, д, р) inside the mask; the negative margin keeps the line box unchanged
    <div style={{ overflow: 'hidden', padding: '0.06em 0 0.16em', margin: '-0.06em 0 -0.16em', ...style }}>
      <div style={{ transform: `translateY(${y}%)`, willChange: 'transform' }}>{children}</div>
    </div>
  );
};
