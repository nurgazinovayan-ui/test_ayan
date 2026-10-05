import { Composition, Folder } from 'remotion';
import { OneflowMotionAd } from './OneflowMotionAd';
import { HandAd } from './hand/HandAd';
import { LOOKS } from './hand/look';
import { DURATION, FPS, HEIGHT, WIDTH } from './theme';

const size = { width: WIDTH, height: HEIGHT, fps: FPS, durationInFrames: DURATION };

export const RemotionRoot: React.FC = () => (
  <>
    <Folder name="Hand-drawn">
      <Composition id="OneflowMotionAdHand" component={HandAd} defaultProps={{ look: 'chalk' }} {...size} />
      {Object.values(LOOKS)
        .filter((l) => l.id !== 'chalk')
        .map((l) => (
          <Composition key={l.id} id={`Hand-${l.id}`} component={HandAd} defaultProps={{ look: l.id }} {...size} />
        ))}
    </Folder>
    <Folder name="Premium-SaaS">
      <Composition id="OneflowMotionAd" component={OneflowMotionAd} {...size} />
    </Folder>
  </>
);
