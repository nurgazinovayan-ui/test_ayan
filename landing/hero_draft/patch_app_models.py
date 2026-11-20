"""The app, 2026-11-20: Recraft and Krea are gone, a vector is drawn by generate-image ({ vector: true }) and
names no model, GPT Image 2.5 shows Atlas's prices, a team account sees the shared balance and is told when it
has run out. Run from the root of the main repo."""
import re


def edit(path, pairs):
    s = open(path, encoding='utf-8').read()
    for a, b in pairs:
        assert s.count(a) == 1, (path, a[:80], s.count(a))
        s = s.replace(a, b)
    open(path, 'w', encoding='utf-8').write(s)
    print(path, 'ok')


# ---- types.ts
p = 'src/types.ts'
s = open(p, encoding='utf-8').read()


def once(a, b):
    global s
    assert s.count(a) == 1, (a[:80], s.count(a))
    s = s.replace(a, b)


once("// \"Вектор\" node — SVG-only output, single fixed model.\nexport const VECTOR_MODEL = 'recraft-ai/recraft-v4-svg';",
     "// \"Вектор\" node — SVG-only output. The node names no model: it is one tool of the canvas. What one SVG costs\n// at Atlas Cloud (its own count on 2026-11-20, $0.4725–$0.5099 whatever the size): the server holds and settles\n// Atlas's count; this number is only what the app notes in its own log.\nexport const VECTOR_LABEL = 'vector';\nexport const VECTOR_USD = 0.4784;")
once("  'recraft-ai/recraft-v4-svg': 0.08,\n", "")
once("  'recraft/recraft-v4-styles-pro': 0.105,\n", "")
once("  'krea/krea-2-large': 0.06,\n", "")
once("  { label: 'Recraft V4 Styles Pro (по референсу стиля)', value: 'recraft/recraft-v4-styles-pro' },\n", "")
once("  { label: 'Krea 2 Large (Krea)', value: 'krea/krea-2-large' },\n", "")
once("""  // Requires at least one style reference image attached (see the Референс-фото slots) — the
  // model has no separate resolution knob, so there's only one option here.
  'recraft/recraft-v4-styles-pro': {
    resolutions: [{ label: '2K', value: '2K' }],
  },
""", "")
once("""  'krea/krea-2-large': {
    resolutions: [{ label: '1K', value: '1K' }],
  },
""", "")
once("// bytedance-seed/seedream-5-0-lite's 4K rate, recraft/recraft-v4-styles-pro's flat rate (base\n// single-style-reference price; extra references and moodboards cost slightly more) and\n// krea/krea-2-large's flat rate are the base/lowest published tier — not broken out further.\n",
     "// bytedance-seed/seedream-5-0-lite's 4K rate is the base/lowest published tier — not broken out further.\n")
# the shared balance flag
once("  unlimited: boolean;\n", "  unlimited: boolean;\n  /** a team account: the number is what is left on the company's provider account, one for the whole team */\n  shared?: boolean;\n")
# GPT Image 2.5 at Atlas's prices where Atlas draws it (1K, 2K); 4K stays the old way's
m = re.findall(r"  'openai/gpt-image-2\.5-(?:sunburst|flare)': \{ '1K': 0\.06, '2K': 0\.1, '4K': 0\.16 \},\n", s)
assert len(m) == 2, len(m)
s = re.sub(r"(  'openai/gpt-image-2\.5-(?:sunburst|flare)': )\{ '1K': 0\.06, '2K': 0\.1, '4K': 0\.16 \},\n", r"\1{ '1K': 0.0146, '2K': 0.0255, '4K': 0.16 }, // 1K and 2K: Atlas's own count (2026-11-20); 4K is drawn the old way\n", s)
open(p, 'w', encoding='utf-8').write(s)
print(p, 'ok')

# ---- the web API: a vector is a job of generate-image
edit('src/webApi.ts', [
    ("""      const outputs = await callFunction<string[]>('generate-vector', params);
      const costUsd = estimateImageCost('recraft-ai/recraft-v4-svg', undefined, outputs.length);
      logWebGeneration({
        timestamp: Date.now(),
        model: 'recraft-ai/recraft-v4-svg',
        category: 'vector',
        costUsd,
      });
      return outputs;""", """      const d = await callFunction<{ urls?: string[] }>('generate-image', { vector: true, prompt: params.prompt, aspectRatio: params.aspectRatio });
      const outputs = Array.isArray(d?.urls) ? d.urls.filter((u): u is string => typeof u === 'string' && u !== '') : [];
      if (!outputs.length) throw new Error(t().errors.generationError);
      logWebGeneration({ timestamp: Date.now(), model: VECTOR_LABEL, category: 'vector', costUsd: VECTOR_USD * outputs.length });
      return outputs;"""),
    ("import { estimateImageCost, estimateVideoCost, DSP_URL, AREA_EDIT_PRICE_MODEL, JPG_PNG_REFERENCE_MODELS } from './types';",
     "import { estimateImageCost, estimateVideoCost, DSP_URL, AREA_EDIT_PRICE_MODEL, JPG_PNG_REFERENCE_MODELS, VECTOR_LABEL, VECTOR_USD } from './types';"),
])
edit('src/mockApi.ts', [
    ("      const vectorCost = estimateImageCost('recraft-ai/recraft-v4-svg', undefined, 1);", "      const vectorCost = VECTOR_USD;"),
    ("import { estimateImageCost, estimateVideoCost, DSP_URL, ADMIN_EMAIL } from './types';", "import { estimateImageCost, estimateVideoCost, DSP_URL, ADMIN_EMAIL, VECTOR_LABEL, VECTOR_USD } from './types';"),
    ("        model: 'recraft-ai/recraft-v4-svg',\n        category: 'vector',", "        model: VECTOR_LABEL,\n        category: 'vector',"),
])

# ---- the notice of an empty shared balance
edit('src/notices.ts', [
    ("  spend_limit: { kind: 'limit', title: 'Достигнут лимит расходов',",
     "  shared_balance_empty: { kind: 'limit', title: 'Общий баланс исчерпан', text: 'На общем балансе команды не хватает кредитов для этой генерации. Обратитесь к администратору — после пополнения всё заработает.' },\n  spend_limit: { kind: 'limit', title: 'Достигнут лимит расходов',"),
    ("  spend_limit: { kind: 'limit', title: 'Spending limit reached',",
     "  shared_balance_empty: { kind: 'limit', title: 'The shared balance has run out', text: 'The team\\'s shared balance does not cover this generation. Ask your administrator — it will work again after a top-up.' },\n  spend_limit: { kind: 'limit', title: 'Spending limit reached',"),
])

# ---- a team account: the balance is shown, the top-up is not offered
edit('src/components/HomePanel.tsx', [
    ("                <button className=\"home-topup-btn\" onClick={() => openTopUp()}>\n                  {t.credits.topUp}\n                </button>",
     "                {!credits.shared && (\n                  <button className=\"home-topup-btn\" onClick={() => openTopUp()}>\n                    {t.credits.topUp}\n                  </button>\n                )}"),
])
edit('src/components/BudgetBar.tsx', [
    ("    <button className=\"budget-ring budget-ring-btn\" title={label} aria-label={label} onClick={() => openTopUp()}>",
     "    <button className=\"budget-ring budget-ring-btn\" title={label} aria-label={label} onClick={() => { if (!balance.shared) openTopUp(); }}>"),
])
print('done')
