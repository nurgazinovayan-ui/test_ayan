import { Config } from '@remotion/cli/config';

// 1230×380 @ 30 fps, no audio track (the ad is silent by design).
Config.setVideoImageFormat('jpeg');
Config.setJpegQuality(95);
Config.setCodec('h264');
Config.setCrf(16);
Config.setPixelFormat('yuv420p');
Config.setMuted(true);
Config.setOverwriteOutput(true);
