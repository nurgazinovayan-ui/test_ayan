import { Composition, Folder } from 'remotion';
import { OneflowMotionAd } from './OneflowMotionAd';
import { HandAd } from './hand/HandAd';
import { LOOKS } from './hand/look';
import { LIGHT_DURATION, LIGHT_H, LIGHT_W, LightAd } from './light/LightAd';
import { CUTS_DURATION, CUTS_H, CUTS_W, CutsAd } from './cuts/CutsAd';
import { EX_DURATION, EX_H, EX_W } from './explainer/shared';
import { LayersExplainer } from './explainer/Layers';
import { GlassExplainer } from './explainer/Glass';
import { NightExplainer } from './explainer/Night';
import { EditorialExplainer } from './explainer/Editorial';

import { KIN_DURATION, KIN_H, KIN_W, KineticAd } from './kinetic/KineticAd';

import { SwissKinetic } from './kinetic2/Swiss';
import { MonoKinetic } from './kinetic2/Mono';
import { SerifKinetic } from './kinetic2/Serif';
import { OrbitKinetic } from './kinetic2/Orbit';

import { BentoKinetic } from './kinetic3/Bento';
import { BrutalKinetic } from './kinetic3/Brutal';
import { AuroraKinetic } from './kinetic3/Aurora';
import { PixelKinetic } from './kinetic3/Pixel';

const ex = { width: EX_W, height: EX_H, fps: FPS, durationInFrames: EX_DURATION };
import { DURATION, FPS, HEIGHT, WIDTH } from './theme';

const size = { width: WIDTH, height: HEIGHT, fps: FPS, durationInFrames: DURATION };

export const RemotionRoot: React.FC = () => (
  <>
    <Folder name="Modern-styles">
      <Composition id="Modern-bento" component={BentoKinetic} defaultProps={{ lang: 'ru' as const }} {...ex} />
      <Composition id="Modern-brutal" component={BrutalKinetic} defaultProps={{ lang: 'ru' as const }} {...ex} />
      <Composition id="Modern-aurora" component={AuroraKinetic} defaultProps={{ lang: 'ru' as const }} {...ex} />
      <Composition id="Modern-pixel" component={PixelKinetic} defaultProps={{ lang: 'ru' as const }} {...ex} />
    </Folder>
    <Folder name="Kinetic-styles">
      <Composition id="Kinetic-swiss" component={SwissKinetic} defaultProps={{ lang: 'ru' as const }} {...ex} />
      <Composition id="Kinetic-mono" component={MonoKinetic} defaultProps={{ lang: 'ru' as const }} {...ex} />
      <Composition id="Kinetic-serif" component={SerifKinetic} defaultProps={{ lang: 'ru' as const }} {...ex} />
      <Composition id="Kinetic-orbit" component={OrbitKinetic} defaultProps={{ lang: 'ru' as const }} {...ex} />
    </Folder>
    <Folder name="Kinetic-type">
      <Composition id="MotionKinetic" component={KineticAd} defaultProps={{ lang: 'ru' as const }} width={KIN_W} height={KIN_H} fps={FPS} durationInFrames={KIN_DURATION} />
      <Composition id="MotionKinetic-en" component={KineticAd} defaultProps={{ lang: 'en' as const }} width={KIN_W} height={KIN_H} fps={FPS} durationInFrames={KIN_DURATION} />
    </Folder>
    <Folder name="Explainer">
      <Composition id="Explainer-layers" component={LayersExplainer} defaultProps={{ lang: 'ru' as const }} {...ex} />
      <Composition id="Explainer-glass" component={GlassExplainer} defaultProps={{ lang: 'ru' as const }} {...ex} />
      <Composition id="Explainer-night" component={NightExplainer} defaultProps={{ lang: 'ru' as const }} {...ex} />
      <Composition id="Explainer-editorial" component={EditorialExplainer} defaultProps={{ lang: 'ru' as const }} {...ex} />
    </Folder>
    <Folder name="Cuts-outline">
      <Composition id="MotionCuts" component={CutsAd} defaultProps={{ lang: 'ru' as const }} width={CUTS_W} height={CUTS_H} fps={FPS} durationInFrames={CUTS_DURATION} />
      <Composition id="MotionCuts-en" component={CutsAd} defaultProps={{ lang: 'en' as const }} width={CUTS_W} height={CUTS_H} fps={FPS} durationInFrames={CUTS_DURATION} />
    </Folder>
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
