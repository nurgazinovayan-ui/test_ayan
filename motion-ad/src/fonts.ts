import { loadFont } from '@remotion/fonts';
import { continueRender, delayRender, staticFile } from 'remotion';

// Geist (SIL OFL 1.1, see public/fonts/OFL-Geist.txt) — variable weight, latin + cyrillic subsets.
export const FONT = "'Geist', system-ui, sans-serif";
// Caveat (SIL OFL 1.1, see public/fonts/OFL-Caveat.txt) — handwriting for the hand-drawn cut.
export const HAND = "'Caveat', 'Geist', cursive";
// Geist Mono and Cormorant Garamond (SIL OFL 1.1) — for the mono and serif kinetic cuts.
export const MONO = "'Geist Mono', ui-monospace, monospace";
export const SERIF = "'Cormorant Garamond', Georgia, serif";
// Press Start 2P (SIL OFL 1.1) — pixel face for the pixel cut.
export const PIXEL = "'Press Start 2P', monospace";

const CYRILLIC = 'U+0301,U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116';
const LATIN =
  'U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD';

const handle = delayRender('Loading Geist');
Promise.all([
  loadFont({ family: 'Geist', url: staticFile('fonts/geist-latin-wght-normal.woff2'), weight: '100 900', unicodeRange: LATIN }),
  loadFont({ family: 'Geist', url: staticFile('fonts/geist-cyrillic-wght-normal.woff2'), weight: '100 900', unicodeRange: CYRILLIC }),
  loadFont({ family: 'Geist Mono', url: staticFile('fonts/geist-mono-latin-wght-normal.woff2'), weight: '100 900', unicodeRange: LATIN }),
  loadFont({ family: 'Geist Mono', url: staticFile('fonts/geist-mono-cyrillic-wght-normal.woff2'), weight: '100 900', unicodeRange: CYRILLIC }),
  ...(['300', '500'] as const).flatMap((w) =>
    (['normal', 'italic'] as const).flatMap((st) => [
      loadFont({ family: 'Cormorant Garamond', url: staticFile(`fonts/cormorant-garamond-latin-${w}-${st}.woff2`), weight: w, style: st, unicodeRange: LATIN }),
      loadFont({ family: 'Cormorant Garamond', url: staticFile(`fonts/cormorant-garamond-cyrillic-${w}-${st}.woff2`), weight: w, style: st, unicodeRange: CYRILLIC }),
    ]),
  ),
  // hand-lettered faces for the hand-drawn looks (all SIL OFL, licences next to the files)
  ...(
    [
      ['Caveat', 'caveat', '400'],
      ['Caveat', 'caveat', '700'],
      ['Neucha', 'neucha', '400'],
      ['Pangolin', 'pangolin', '400'],
      ['Amatic SC', 'amatic-sc', '400'],
      ['Amatic SC', 'amatic-sc', '700'],
      ['Rubik Doodle Shadow', 'rubik-doodle-shadow', '400'],
      ['Press Start 2P', 'press-start-2p', '400'],
    ] as const
  ).flatMap(([family, file, w]) => [
    loadFont({ family, url: staticFile(`fonts/${file}-latin-${w}-normal.woff2`), weight: w, unicodeRange: LATIN }),
    loadFont({ family, url: staticFile(`fonts/${file}-cyrillic-${w}-normal.woff2`), weight: w, unicodeRange: CYRILLIC }),
  ]),
])
  .then(() => continueRender(handle))
  .catch((err) => {
    console.error(err);
    continueRender(handle);
  });
