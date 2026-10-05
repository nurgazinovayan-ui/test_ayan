/** Pointer cursor; (x, y) is the tip of the arrow. */
export const Cursor: React.FC<{ x: number; y: number; scale: number; opacity: number }> = ({ x, y, scale, opacity }) => (
  <svg
    width={26}
    height={30}
    viewBox="0 0 26 30"
    style={{
      position: 'absolute',
      left: x - 3,
      top: y - 2,
      opacity,
      transform: `scale(${scale})`,
      transformOrigin: '3px 2px',
      filter: 'drop-shadow(0 6px 10px rgba(0,0,0,0.55))',
    }}
  >
    <path
      d="M3 2 L3 23 L8.6 17.6 L12.4 26.4 L16.2 24.8 L12.5 16.2 L20.4 16.2 Z"
      fill="#FAFAFA"
      stroke="#09090B"
      strokeWidth="1.4"
      strokeLinejoin="round"
    />
  </svg>
);
