"""The app's top-up window gets the control of the landing: a row of squares over an invisible range input,
numbers that roll like a drum, and the three examples counted from the app's own (Atlas Cloud) price tables.
Run from the root of the main repo:  python3 -I patch_topup_app.py"""

# ---- credits.ts
p = 'src/credits.ts'
s = open(p, encoding='utf-8').read()
tail = s[s.index('// What a credit buys, for the'):]
new = '''// What a credit buys, for the "≈ N images" hints: the same three examples as the landing (the strip under the
// hero and the pricing section), counted from the app's own price tables — the prices of Atlas Cloud — the way
// the server counts credits (1 credit = 1 cent of cost, rounded up, with the model's price factor).
export const EXAMPLE_VIDEO_MODEL = 'bytedance/seedance-2.5';
export function creditExamples(modelCredits: (usd: number, model: string) => number): { image: number; video5s: number; music: number } {
  return {
    image: Math.max(1, modelCredits(estimateImageCost('google/nano-banana-2.1', '1K', 1), 'google/nano-banana-2.1')), // 4
    video5s: Math.max(1, modelCredits(estimateVideoCost(EXAMPLE_VIDEO_MODEL, '480p', 5), EXAMPLE_VIDEO_MODEL)), // 48 at factor 0.7
    music: Math.max(1, usdToCredits(SONG_USD)), // Suno V6, one request with two takes: 14
  };
}
'''
s = s.replace(tail, new)
a = "import { usdToCredits, type CreditBalance } from './types';"
assert s.count(a) == 1
s = s.replace(a, "import { SONG_USD, estimateImageCost, estimateVideoCost, usdToCredits, type CreditBalance } from './types';")
open(p, 'w', encoding='utf-8').write(s)

# ---- i18n
p = 'src/i18n.ts'
s = open(p, encoding='utf-8').read()
for a, b in [("videos: 'видео 5 с · Kling 3.0, 720p',", "videos: 'видео 5 с · Seedance 2.5, 480p',"),
             ("music: 'треков · Lyria 3 Pro',", "music: 'треков · Suno V6',"),
             ("videos: '5-second videos · Kling 3.0, 720p',", "videos: '5-second videos · Seedance 2.5, 480p',"),
             ("music: 'music tracks · Lyria 3 Pro',", "music: 'music tracks · Suno V6',")]:
    assert s.count(a) == 1, a
    s = s.replace(a, b)
open(p, 'w', encoding='utf-8').write(s)

# ---- TopUpModal
p = 'src/components/TopUpModal.tsx'
s = open(p, encoding='utf-8').read()


def once(a, b):
    global s
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)


once("import { CREDIT_EXAMPLES, creditsForTopUp, topUpStops, useCredits } from '../credits';",
     "import { creditExamples, creditsForTopUp, topUpStops, useCredits, useModelCredits } from '../credits';")
once("// Top-up window: a slider over sensible amounts,", '''// The squares of the amount control, as on the landing: they light up to the chosen sum and the last lit ones
// pulse, the stronger the larger the sum. The real range input lies over them, invisible, so the keyboard, the
// mouse and touch work as with any slider.
const HUES = [326, 300, 262, 236, 212, 190, 158, 110, 70, 36];
const PULSE = 7;

function useNarrow(): boolean {
  const [narrow, setNarrow] = useState(() => window.matchMedia('(max-width: 560px)').matches);
  useEffect(() => {
    const mq = window.matchMedia('(max-width: 560px)');
    const on = () => setNarrow(mq.matches);
    mq.addEventListener('change', on);
    return () => mq.removeEventListener('change', on);
  }, []);
  return narrow;
}

function Squares({ part, amp }: { part: number; amp: number }) {
  const n = useNarrow() ? 24 : 40;
  const lit = Math.max(1, Math.round(part * (n - 1)) + 1);
  const box = { ['--amp' as string]: amp.toFixed(3), ['--beat' as string]: `${(1.5 - amp * 0.85).toFixed(2)}s` };
  return (
    <div className="sq-cells" aria-hidden="true" style={box}>
      {Array.from({ length: n }, (_, i) => {
        const back = lit - 1 - i; // 0 is the square under the thumb
        const beat = back > 0 && back <= PULSE;
        const hue = HUES[Math.min(HUES.length - 1, Math.floor((i * HUES.length) / n))];
        return (
          <i
            key={i}
            className={`${i < lit ? 'on' : ''}${i === lit - 1 ? ' at' : ''}${beat ? ' beat' : ''}`}
            style={{
              ['--c' as string]: `hsl(${hue} 100% 62%)`,
              ...(beat ? { ['--near' as string]: (1 - (back - 1) / PULSE).toFixed(2), animationDelay: `${(-back * 0.09).toFixed(2)}s` } : {}),
            }}
          />
        );
      })}
    </div>
  );
}

/** A number whose digits roll to their new value like a drum; columns are counted from the right, so a longer
 *  number grows on the left. */
function Roll({ text }: { text: string }) {
  const chars = text.split('');
  return (
    <span className="sq-roll" role="text" aria-label={text}>
      {chars.map((ch, k) => {
        const fromRight = chars.length - k;
        return ch >= '0' && ch <= '9' ? (
          <span key={`d${fromRight}`} className="sq-col" aria-hidden="true">
            <u style={{ transform: `translateY(${-Number(ch) * 10}%)` }}>
              0<br />1<br />2<br />3<br />4<br />5<br />6<br />7<br />8<br />9
            </u>
          </span>
        ) : (
          <span key={`c${fromRight}`} className="sq-ch" aria-hidden="true">
            {ch}
          </span>
        );
      })}
    </span>
  );
}

// Top-up window: a slider over sensible amounts,''')
once("  const [consented, setConsented] = useState(false);\n",
     "  const [consented, setConsented] = useState(false);\n  const modelCredits = useModelCredits();\n")
once("  const pct = (idx / Math.max(1, stops.length - 1)) * 100;\n",
     "  const part = idx / Math.max(1, stops.length - 1);\n  const examples = creditExamples(modelCredits);\n")
once('<div className="topup-usd">${num(usd)}</div>',
     '<div className="topup-usd">\n              <Roll text={`$${num(usd)}`} />\n            </div>')
once("<b>{t.credits.count(credits)}</b>",
     "<b>\n                <Roll text={num(credits)} /> {t.credits.count(credits).replace(/^[\\d\\s.,]+/, '')}\n              </b>")
once('''<div className="topup-slider" style={{ ['--p' as string]: `${pct}%` }}>''',
     '''<div className="topup-slider">\n            <Squares part={part} amp={Math.min(1, usd / Math.max(1, topup.maxUsd))} />''')
for k in ['image', 'video5s', 'music']:
    once("<b>≈ {num(Math.floor(credits / CREDIT_EXAMPLES.%s))}</b>" % k,
         "<b>\n                  <Roll text={`≈ ${num(Math.floor(credits / examples.%s))}`} />\n                </b>" % k)
open(p, 'w', encoding='utf-8').write(s)

# ---- CSS
p = 'src/Credits.css'
s = open(p, encoding='utf-8').read()
i = s.index('/* slider */')
j = s.index('.topup-marks {')
new = '''/* the amount control: a row of squares with the real range input over them, invisible (as on the landing) */
.topup-slider {
  position: relative;
  margin: 26px 0 0;
  padding-bottom: 40px;
}
.sq-cells {
  display: flex;
  gap: 4px;
}
.sq-cells i {
  flex: 1;
  aspect-ratio: 1;
  border-radius: 2px;
  background: color-mix(in srgb, var(--c-text) 10%, transparent);
  transition: background 0.2s;
}
.sq-cells i.on {
  background: var(--c);
}
.sq-cells i.at {
  background: var(--c-text);
  transform: scale(1.35);
}
.sq-cells i.beat {
  animation: sq-beat var(--beat, 1.4s) ease-in-out infinite;
}
@keyframes sq-beat {
  0%,
  100% {
    transform: scale(1);
    filter: brightness(1);
    box-shadow: 0 0 0 0 transparent;
  }
  50% {
    transform: scale(calc(1 + 0.5 * var(--amp, 0) * var(--near, 0)));
    filter: brightness(calc(1 + 0.7 * var(--amp, 0) * var(--near, 0)));
    box-shadow: 0 0 calc(22px * var(--amp, 0) * var(--near, 0)) var(--c);
  }
}
/* html:root lifts it above the app's global input styles (border, panel background) */
html:root .topup-slider input[type='range'] {
  -webkit-appearance: none;
  appearance: none;
  position: absolute;
  left: 0;
  top: -10px;
  width: 100%;
  height: calc(100% - 20px);
  min-height: 34px;
  margin: 0;
  padding: 0;
  border: 0;
  box-shadow: none;
  background: transparent;
  opacity: 0;
  cursor: pointer;
}
.topup-slider:has(input:focus-visible) .sq-cells i.at {
  box-shadow: 0 0 0 3px var(--v2-accent);
}
/* a number that rolls: each digit is a column of ten */
.sq-roll {
  display: inline-flex;
  vertical-align: bottom;
  font-variant-numeric: tabular-nums;
}
.sq-col {
  display: inline-block;
  height: 1em;
  line-height: 1;
  overflow: hidden;
}
.sq-col u {
  display: block;
  text-align: center;
  text-decoration: none;
  line-height: 1;
  transition: transform 0.55s cubic-bezier(0.2, 0.9, 0.25, 1);
  will-change: transform;
}
.sq-ch {
  display: inline-block;
  line-height: 1;
  white-space: pre;
}
@media (prefers-reduced-motion: reduce) {
  .sq-cells i.beat {
    animation: none;
  }
  .sq-col u {
    transition: none;
  }
}

'''
s = s[:i] + new + s[j:]
a = ".topup-marks {\n  position: absolute;\n  left: 14px;\n  right: 14px;"
assert s.count(a) == 1
s = s.replace(a, ".topup-marks {\n  position: absolute;\n  left: 6px;\n  right: 6px;")
open(p, 'w', encoding='utf-8').write(s)
print('ok')
