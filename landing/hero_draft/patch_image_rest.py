"""generate-image, 2026-11-20: the rest of the pictures through Atlas Cloud.
  * GPT Image 2.5 (Sunburst, Flare): Atlas first, at the sizes Atlas has
  * the service pictures (an edited area, a UGC frame, a One Launch card): Atlas first, waited for in place
  * a vector picture (SVG): GPT Image 2.6 Sunburst at Atlas, text only — Recraft is gone
  * Recraft and Krea are no longer models of the function
Run from the root of the main repo."""
p = 'supabase/functions/generate-image/index.ts'
s = open(p, encoding='utf-8').read()


def once(a, b):
    global s
    assert s.count(a) == 1, (a[:90], s.count(a))
    s = s.replace(a, b)


# ---- Recraft and Krea are gone
once("  'recraft-ai/recraft-v4-svg': 0.08,\n", "")
once("  'recraft/recraft-v4-styles-pro': 0.105,\n", "")
once("  'krea/krea-2-large': 0.06,\n", "")
once("    'krea/krea-2-large': ['1:1', '16:9', '9:16', '4:3', '3:4'],\n", "")

# ---- GPT Image 2.5 through Atlas
once("""  'x-ai/grok-imagine-image-2.0': {
    field: 'image_urls',""", """  'openai/gpt-image-2.5-sunburst': gpt25Route('openai/gpt-image-2.5-sunburst'),
  'openai/gpt-image-2.5-flare': gpt25Route('openai/gpt-image-2.5-flare'),
  'x-ai/grok-imagine-image-2.0': {
    field: 'image_urls',""")
once("const ATLAS_STILL_ROUTES: Record<string, AtlasStillRoute> = {", """// GPT Image 2.5 (2026-11-20): the tiers and proportions the app offers for it, at the sizes Atlas's schema names.
// A 4K picture in these proportions and a picture of an exact size (a node of the canvas) are sizes Atlas does
// not have for it: they go the old way.
const GPT25_SIZES: Record<string, Record<string, string>> = {
  '1K': { '1:1': '1024x1024', '3:2': '1536x1024', '2:3': '1024x1536' },
  '2K': { '1:1': '2048x2048' },
};
const GPT25_MODELS = new Set(['openai/gpt-image-2.5-sunburst', 'openai/gpt-image-2.5-flare']);
function gpt25Route(id: string): AtlasStillRoute {
  return {
    field: 'images',
    maxRefs: 10,
    byLink: true,
    plan: (a) => {
      const size = GPT25_SIZES[a.resolution ?? '1K']?.[a.aspectRatio];
      return size ? { model: `${id}/${a.refs ? 'edit' : 'text-to-image'}`, size, quality: 'medium', output_format: 'png' } : null;
    },
  };
}
const ATLAS_STILL_ROUTES: Record<string, AtlasStillRoute> = {""")
once("  'x-ai/grok-imagine-image-2.0': { '1K': 0.06, '2K': 0.08 },\n  'bytedance-seed/seedream-5-0-pro': { '1K': 0.036, '2K': 0.072 },",
     "  'x-ai/grok-imagine-image-2.0': { '1K': 0.06, '2K': 0.08 },\n  // Atlas's own count on 2026-11-20 (medium quality): $0.0145 for 1024x1024, $0.0122 for 1536x1024, $0.0254 for 2048x2048\n  'openai/gpt-image-2.5-sunburst': { '1K': 0.0146, '2K': 0.0255 },\n  'openai/gpt-image-2.5-flare': { '1K': 0.0146, '2K': 0.0255 },\n  'bytedance-seed/seedream-5-0-pro': { '1K': 0.036, '2K': 0.072 },")
once("'openai/gpt-image-2': 0.0141, 'x-ai/grok-imagine-image-2.0': 0.01 };", "'openai/gpt-image-2': 0.0141, 'x-ai/grok-imagine-image-2.0': 0.01, 'openai/gpt-image-2.5-sunburst': 0.0256, 'openai/gpt-image-2.5-flare': 0.0256 };")
once("    const route = Object.hasOwn(ATLAS_STILL_ROUTES, model) ? ATLAS_STILL_ROUTES[model] : null;",
     "    // GPT Image 2.5 at an exact size is a size Atlas does not have: it goes the old way\n    const route = Object.hasOwn(ATLAS_STILL_ROUTES, model) && !(width && height && GPT25_MODELS.has(model)) ? ATLAS_STILL_ROUTES[model] : null;")

# ---- the service pictures and the vector picture
once("// A poll: { jobId } of a picture job this account started — a UGC frame, a One Launch card or a casting", '''// ---- The service pictures through Atlas (2026-11-20): an edited area, a UGC frame, a One Launch card. They are
// waited for in place, so Atlas's job is followed here and its picture handed on inline, exactly as OpenRouter
// hands its own. null: Atlas did not take the request (no key, a size it does not have, no money, overload) —
// the caller draws it the old way. A refusal for the content is a refusal.
const ATLAS_NOW_MS = 110_000;
const ATLAS_NOW_MAX_BYTES = 20 * 1024 * 1024;
const bytesToBase64 = (bytes: Uint8Array): string => {
  let bin = '';
  for (let i = 0; i < bytes.length; i += 0x8000) bin += String.fromCharCode(...bytes.subarray(i, i + 0x8000));
  return btoa(bin);
};
async function atlasDrawNow(model: string, prompt: string, aspectRatio: string, resolution: string | undefined, refs: string[]): Promise<{ urls: string[]; costUsd: number | null } | null> {
  if (!ATLAS_API_KEY) return null;
  let input: Record<string, unknown>;
  if (ATLAS_IMAGE_MODELS.has(model)) {
    input = atlasImageInput(model, prompt, aspectRatio, resolution, undefined, undefined, refs, null, false);
  } else {
    const route = Object.hasOwn(ATLAS_STILL_ROUTES, model) ? ATLAS_STILL_ROUTES[model] : null;
    const plan = route && refs.length <= route.maxRefs ? route.plan({ aspectRatio, resolution, refs: refs.length }) : null;
    if (!route || !plan) return null;
    input = { ...plan, prompt };
    if (refs.length) {
      const links = await atlasRefs(refs, route);
      if (!links) return null;
      input[route.field] = links;
    }
  }
  const quoteUsd = await atlasImageQuote(input);
  const sent = await submitAtlasImage(input);
  if ('refused' in sent) throw new GuardError(400, 'provider_refused', sent.refused);
  if ('soft' in sent) {
    if (/status (402|429|5\\d\\d)|no connection/.test(sent.soft)) notifyAlert(sent.soft.includes('402') ? 'atlas_balance_low' : 'atlas_unavailable', 'image');
    console.error('atlas did not take the service picture, drawn through OpenRouter instead:', sent.soft);
    return null;
  }
  const until = Date.now() + ATLAS_NOW_MS;
  while (Date.now() < until) {
    await new Promise((r) => setTimeout(r, 2500));
    const state = await pollAtlasImage(sent.id);
    if (state.status === 'waiting') continue;
    if (state.status === 'failed') {
      if (ATLAS_REFUSED.test(state.error)) throw new GuardError(400, 'provider_refused', 'Модель не приняла запрос по правилам провайдера. Измените описание или фото.');
      throw new Error(`atlas service picture failed: ${state.error}`);
    }
    const urls: string[] = [];
    for (const url of state.outputs) {
      const got = await assetBytes(url);
      if (got && ASSET_IMAGE_TYPES[got.mime] && got.bytes.length <= ATLAS_NOW_MAX_BYTES) urls.push(`data:${got.mime};base64,${bytesToBase64(got.bytes)}`);
    }
    if (!urls.length) throw new Error('atlas service picture: nothing to hand on');
    console.log('service picture', JSON.stringify({ model: input.model, provider: 'atlas', references: refs.length }));
    return { urls, costUsd: state.billedUsd ?? quoteUsd };
  }
  // Atlas has the job and may still finish (and bill) it: it is not drawn a second time elsewhere
  throw new Error('atlas service picture timed out');
}

// ---- A vector picture (SVG) — the canvas's vector node (2026-11-20). Drawn by GPT Image 2.6 Sunburst at Atlas
// with output_format svg, from words only (Atlas's edit model does not write SVG). It is a job like any picture
// of Atlas: the app follows it by its id; the finished file is handed over inline and is not kept in storage
// (an SVG is a document, not a bitmap — storage serves only the bitmap types).
const VECTOR_MODEL = 'openai/gpt-image-2.6-sunburst';
// Atlas's own count on 2026-11-20: $0.4725 … $0.5099 for one SVG, whatever its size (the dearest is held)
const VECTOR_HOLD_USD = 0.51;
const VECTOR_MAX_BYTES = 4 * 1024 * 1024;
async function vectorPicture(req: Request, caller: { id: string; email: string }, params: Record<string, any>): Promise<Response> {
  let reservation: string | null = null;
  try {
    if (!ATLAS_API_KEY) throw new GuardError(503, 'provider_unavailable', 'Генерация вектора сейчас недоступна. Попробуйте позже.');
    const prompt = clipText(params.prompt, 4000);
    if (!prompt.trim()) throw badRequest('Опишите, что нарисовать.');
    const aspectRatio = typeof params.aspectRatio === 'string' && /^\\d{1,2}:\\d{1,2}$/.test(params.aspectRatio) ? params.aspectRatio : '1:1';
    const size = ATLAS_STILL_SIZE['1K'][aspectRatio] ?? atlasSize(aspectRatio, ATLAS_TIER_AREA['1K'], ATLAS_TIER_EDGE['1K']);
    const input = { model: `${VECTOR_MODEL}/text-to-image`, prompt, n: 1, size, quality: 'medium', output_format: 'svg' };
    const quoteUsd = await atlasImageQuote(input);
    reservation = await reserveSpend(req, caller.id, VECTOR_MODEL, 'vector', quoteUsd ?? VECTOR_HOLD_USD);
    const sent = await submitAtlasImage(input);
    console.log('vector submit', JSON.stringify({ provider: 'atlas', size, taken: 'id' in sent, quoteUsd }));
    if ('refused' in sent) throw new GuardError(400, 'provider_refused', sent.refused);
    if ('soft' in sent) {
      if (/status (402|429|5\\d\\d)|no connection/.test(sent.soft)) notifyAlert(sent.soft.includes('402') ? 'atlas_balance_low' : 'atlas_unavailable', 'image');
      throw new GuardError(503, 'provider_unavailable', 'Генерация вектора сейчас недоступна. Кредиты не списаны — попробуйте позже.');
    }
    const job: AtlasImageJob = { asset: { model: VECTOR_MODEL, prompt, meta: { aspectRatio, vector: true } }, quoteUsd };
    const { error: jobError } = await supabaseAdmin.from('generation_reservations').update({ result: { atlasImage: job } }).eq('id', reservation);
    if (jobError) console.error('vector job not kept', String(jobError).slice(0, 200));
    await markSubmitted(reservation, ATLAS_IMAGE_PREFIX + sent.id);
    const jobId = reservation;
    reservation = null; // the job owns the hold from here: settled or released by its polls
    return jsonResponse({ pending: true, jobId }, 202);
  } catch (err) {
    return failResponse(err, reservation, 'Не удалось сгенерировать вектор. Попробуйте ещё раз.');
  }
}
// the SVG Atlas made, inline: only a document that is an SVG, without anything that runs
async function vectorInline(url: string): Promise<string | null> {
  const got = await assetBytes(url);
  if (!got || got.bytes.length > VECTOR_MAX_BYTES) return null;
  let text = new TextDecoder().decode(got.bytes);
  if (!/<svg[\\s>]/i.test(text.slice(0, 2000))) return null;
  text = text
    .replace(/<script[\\s\\S]*?<\\/script\\s*>/gi, '')
    .replace(/<foreignObject[\\s\\S]*?<\\/foreignObject\\s*>/gi, '')
    .replace(/\\son[a-z]+\\s*=\\s*("[^"]*"|'[^']*'|[^\\s>]+)/gi, '')
    .replace(/(href\\s*=\\s*["']?)\\s*javascript:[^"'\\s>]*/gi, '$1#');
  return `data:image/svg+xml;base64,${bytesToBase64(new TextEncoder().encode(text))}`;
}

// A poll: { jobId } of a picture job this account started — a UGC frame, a One Launch card or a casting''')

# the finished vector job: handed over inline, not kept
once("""    const assetIds: (string | null)[] = [];
    for (const url of state.outputs) assetIds.push(await keepImageAsset(caller.id, url, info));
    const quote = typeof r.atlasImage?.quoteUsd === 'number' && r.atlasImage.quoteUsd > 0 ? r.atlasImage.quoteUsd : null;
    const providerUsd = state.billedUsd ?? quote ?? job.amount_usd;""", """    const quote = typeof r.atlasImage?.quoteUsd === 'number' && r.atlasImage.quoteUsd > 0 ? r.atlasImage.quoteUsd : null;
    const providerUsd = state.billedUsd ?? quote ?? job.amount_usd;
    if ((info.meta as { vector?: unknown }).vector === true) {
      const inline: string[] = [];
      for (const url of state.outputs) {
        const svg = await vectorInline(url);
        if (svg) inline.push(svg);
      }
      if (!inline.length) throw new Error('vector: no svg in the answer');
      // a later poll of the same job gets the links Atlas holds the files under
      await settleSpend(job.id, caller.email, providerUsd, { assetIds: state.outputs.map(() => null), urls: state.outputs, providerUsd });
      return jsonResponse({ urls: inline, assetIds: inline.map(() => null) });
    }
    const assetIds: (string | null)[] = [];
    for (const url of state.outputs) assetIds.push(await keepImageAsset(caller.id, url, info));""")

# the request
once("    if (params.action === 'quote') return await quoteAtlasImage(caller, params);",
     "    if (params.action === 'quote') return await quoteAtlasImage(caller, params);\n    if (params.vector === true) return await vectorPicture(req, caller, params);")

# an edited area: Atlas first
once("""    const input = buildOpenRouterImageInput(AREA_EDIT_MODEL, areaEditPrompt(request), aspectRatio, undefined, [edit.image, edit.marked], resolution);
    const result = await callOpenRouterImage(input);""", """    const viaAtlas = await atlasDrawNow(AREA_EDIT_MODEL, areaEditPrompt(request), aspectRatio, resolution, [edit.image, edit.marked]);
    const result = viaAtlas
      ? { urls: viaAtlas.urls, realCostUsd: viaAtlas.costUsd }
      : await callOpenRouterImage(buildOpenRouterImageInput(AREA_EDIT_MODEL, areaEditPrompt(request), aspectRatio, undefined, [edit.image, edit.marked], resolution));""")

# a UGC frame, a One Launch card: Atlas first
once("""        const result = await callOpenRouterImage(input);
        spent += result.realCostUsd ?? (result.urls[0] ? estimate : 0);""", """        // Atlas first, from the same words, proportions and photos; the old way for what Atlas does not take
        const refs = (Array.isArray(input.input_references) ? input.input_references : []).map((x: { image_url?: { url?: unknown } }) => x?.image_url?.url).filter((u: unknown): u is string => typeof u === 'string');
        const viaAtlas = attempt === 1 ? await atlasDrawNow(model, String(input.prompt ?? ''), kind.aspectRatio, resolution, refs) : null;
        const result = viaAtlas ? { urls: viaAtlas.urls, realCostUsd: viaAtlas.costUsd } : await callOpenRouterImage(input);
        spent += result.realCostUsd ?? (result.urls[0] ? estimate : 0);""")

open(p, 'w', encoding='utf-8').write(s)
print('ok')
