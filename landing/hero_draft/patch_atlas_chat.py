"""Text models through Atlas Cloud first: the shared block _shared/atlas_chat.ts gets its markers in the five
functions that ask a chat model, their calls go through chatFetch, and the sync script learns the block.
Run from the root of the main repo, then: node scripts/sync-edge-guard.mjs"""
import re

END = '// ---- end of atlas chat'
p = 'supabase/functions/_shared/atlas_chat.ts'
s = open(p, encoding='utf-8').read()
s = s.replace('// ---- end of the Atlas Cloud chat block\n', '')
s = s.replace('scripts/sync-atlas-chat.mjs', 'scripts/sync-edge-guard.mjs')
open(p, 'w', encoding='utf-8').write(s)

STUB = '// ---- Atlas Cloud chat\n' + END + '\n\n'


def edit(path, pairs, stub_before):
    s = open(path, encoding='utf-8').read()
    for a, b in pairs:
        assert s.count(a) == 1, (path, a[:80], s.count(a))
        s = s.replace(a, b)
    assert s.count(stub_before) == 1, (path, stub_before)
    s = s.replace(stub_before, STUB + stub_before)
    open(path, 'w', encoding='utf-8').write(s)
    print(path.split('/')[-2], 'ok')


F = 'supabase/functions/%s/index.ts'
edit(F % 'generate-chat', [
    ("  const res = await fetch(OPENROUTER_CHAT_URL, {\n    method: 'POST',\n    headers: {\n      Authorization: `Bearer ${OPENROUTER_API_KEY}`,\n      'Content-Type': 'application/json',\n    },\n    body: JSON.stringify({ model, messages, max_tokens: MAX_REPLY_TOKENS, usage: { include: true } }),\n  });",
     "  const res = await chatFetch({\n    method: 'POST',\n    headers: {\n      Authorization: `Bearer ${OPENROUTER_API_KEY}`,\n      'Content-Type': 'application/json',\n    },\n    body: JSON.stringify({ model, messages, max_tokens: MAX_REPLY_TOKENS, usage: { include: true } }),\n  });"),
], 'async function callOpenRouterChat(')
edit(F % 'marketing-ai', [
    ("  const res = await fetchWithTimeout(OPENROUTER_CHAT_URL, {\n    method: 'POST',\n    headers: { Authorization: `Bearer ${OPENROUTER_API_KEY}`, 'Content-Type': 'application/json' },\n    body: JSON.stringify({\n      model,\n      messages: [\n        { role: 'system', content: systemPrompt },",
     "  const res = await chatFetch({\n    method: 'POST',\n    headers: { Authorization: `Bearer ${OPENROUTER_API_KEY}`, 'Content-Type': 'application/json' },\n    body: JSON.stringify({\n      model,\n      messages: [\n        { role: 'system', content: systemPrompt },"),
], 'async function fetchWithTimeout(')
edit(F % 'evaluate-creative', [
    ("    const res = await fetch(OPENROUTER_CHAT_URL, {\n      method: 'POST',", "    const res = await chatFetch({\n      method: 'POST',"),
], 'async function fetchWithTimeout(')
edit(F % 'motion-storyboard', [
    ("  const res = await fetchWithTimeout(OPENROUTER_CHAT_URL, {\n    method: 'POST',\n    headers: { Authorization: `Bearer ${OPENROUTER_API_KEY}`, 'Content-Type': 'application/json' },\n    body: JSON.stringify({\n      model: MODEL,\n      messages: [{ role: 'system', content: system }, { role: 'user', content }],",
     "  const res = await chatFetch({\n    method: 'POST',\n    headers: { Authorization: `Bearer ${OPENROUTER_API_KEY}`, 'Content-Type': 'application/json' },\n    body: JSON.stringify({\n      model: MODEL,\n      messages: [{ role: 'system', content: system }, { role: 'user', content }],"),
    ("    const res = await fetch(OPENROUTER_CHAT_URL, {\n      method: 'POST',\n      headers: { Authorization: `Bearer ${OPENROUTER_API_KEY}`, 'Content-Type': 'application/json' },\n      body: JSON.stringify({\n        model: MODEL,\n        messages: [{ role: 'system', content: mode === 'styles'",
     "    const res = await chatFetch({\n      method: 'POST',\n      headers: { Authorization: `Bearer ${OPENROUTER_API_KEY}`, 'Content-Type': 'application/json' },\n      body: JSON.stringify({\n        model: MODEL,\n        messages: [{ role: 'system', content: mode === 'styles'"),
], 'async function fetchWithTimeout(')
edit(F % 'generate-video', [
    ("    const res = await fetchWithTimeout('https://openrouter.ai/api/v1/chat/completions', {\n      method: 'POST',\n      headers: { Authorization: `Bearer ${OPENROUTER_API_KEY}`, 'Content-Type': 'application/json' },\n      body: JSON.stringify({\n        model: OPERATOR_MODEL,",
     "    const res = await chatFetch({\n      method: 'POST',\n      headers: { Authorization: `Bearer ${OPENROUTER_API_KEY}`, 'Content-Type': 'application/json' },\n      body: JSON.stringify({\n        model: OPERATOR_MODEL,"),
], 'async function cinemaOperator(')

# the sync script: one more block
p = 'scripts/sync-edge-guard.mjs'
s = open(p, encoding='utf-8').read()
a = "const blocks = [\n"
assert s.count(a) == 1
s = s.replace(a, a + "  { shared: 'atlas_chat.ts', start: /^\\/\\/ ---- Atlas Cloud chat/, end: '// ---- end of atlas chat', files: CHAT_FUNCTIONS.map((n) => [n, join(fnDir, n, 'index.ts')]) },\n")
a = "export const ADMIN_FUNCTIONS ="
assert s.count(a) == 1
s = s.replace(a, "// every function that asks a text model: Atlas Cloud first, OpenRouter for what Atlas does not take\nexport const CHAT_FUNCTIONS = ['generate-chat', 'marketing-ai', 'evaluate-creative', 'motion-storyboard', 'generate-video'];\n" + a)
a = "//   supabase/functions/_shared/onelaunch_cards.ts"
assert s.count(a) == 1
s = s.replace(a, "//   supabase/functions/_shared/atlas_chat.ts → every function that asks a text model («// ---- Atlas Cloud chat» …\n//                                                «// ---- end of atlas chat»)\n" + a)
open(p, 'w', encoding='utf-8').write(s)
print('sync script ok')
