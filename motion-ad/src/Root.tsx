import { Composition, Folder } from 'remotion';
import { OneflowMotionAd } from './OneflowMotionAd';
import { HandAd } from './hand/HandAd';
import { LOOKS } from './hand/look';
import { LIGHT_DURATION, LIGHT_H, LIGHT_W, LightAd } from './light/LightAd';
import { DURATION, FPS, HEIGHT, WIDTH } from './theme';

const size = { width: WIDTH, height: HEIGHT, fps: FPS, durationInFrames: DURATION };

export const RemotionRoot: React.FC = () => (
  <>
    <Folder name="Light-explainer">
      <Composition id="MotionLight" component={LightAd} defaultProps={{ lang: 'ru' as const }} width={LIGHT_W} height={LIGHT_H} fps={FPS} durationInFrames={LIGHT_DURATION} />
      <Composition id="MotionLight-en" component={LightAd} defaultProps={{ lang: 'en' as const }} width={LIGHT_W} height={LIGHT_H} fps={FPS} durationInFrames={LIGHT_DURATION} />
    </Folder>
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
