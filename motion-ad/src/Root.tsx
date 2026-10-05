import { Composition, Folder } from 'remotion';
import { OneflowMotionAd } from './OneflowMotionAd';
import { HandAd } from './hand/HandAd';
import { DURATION, FPS, HEIGHT, WIDTH } from './theme';

export const RemotionRoot: React.FC = () => (
  <Folder name="ONEFLOW-Motion">
    <Composition id="OneflowMotionAdHand" component={HandAd} width={WIDTH} height={HEIGHT} fps={FPS} durationInFrames={DURATION} />
    <Composition id="OneflowMotionAd" component={OneflowMotionAd} width={WIDTH} height={HEIGHT} fps={FPS} durationInFrames={DURATION} />
  </Folder>
);
