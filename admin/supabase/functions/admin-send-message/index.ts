// Deploy in Supabase Studio → Edge Functions → admin-send-message → replace the code with this file → Deploy.
// Keep "Verify JWT" ON (default). No secrets to configure: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are injected
// into every Edge Function automatically.
//
// Used by the ONEFLOW app and by oneflow.art/admin. Body: { mode: 'all', message } broadcasts to every account except
// the caller; { mode: 'selected', emails: string[], message } targets just those addresses (ones that don't resolve
// to a real account are skipped, as long as at least one does).

import { createClient } from 'npm:@supabase/supabase-js@2';

const SUPABASE_URL = Deno.env.get('SUPABASE_URL') ?? '';
const SERVICE_ROLE_KEY = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? '';

// Only this account may send admin messages — checked against the caller's own verified JWT, not anything the client claims.
const ADMIN_EMAIL = 'nurgazinov.ayan@gmail.com';
const MAX_MESSAGE = 5000;
const MAX_EMAILS = 1000;

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};
const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: corsHeaders });
  if (req.method !== 'POST') return new Response('Method not allowed', { status: 405, headers: corsHeaders });
  try {
    const admin = createClient(SUPABASE_URL, SERVICE_ROLE_KEY);
    const token = (req.headers.get('Authorization') ?? '').replace(/^Bearer\s+/i, '');
    const { data: callerData } = await admin.auth.getUser(token);
    const caller = callerData.user;
    // exactly one account: the admin email, and only once that address is confirmed (Google sign-ins are confirmed by Google)
    if (!caller || !caller.email_confirmed_at || caller.email?.toLowerCase() !== ADMIN_EMAIL.toLowerCase()) {
      return json({ error: 'Доступ запрещён.' }, 403);
    }

    const body = await req.json().catch(() => ({}));
    const mode = body.mode === 'all' ? 'all' : 'selected';
    const message = typeof body.message === 'string' ? body.message.trim() : '';
    if (!message) return json({ error: 'Укажите текст сообщения.' }, 400);
    if (message.length > MAX_MESSAGE) return json({ error: 'Слишком длинное сообщение.' }, 400);
    const emails: string[] = Array.isArray(body.emails)
      ? body.emails.filter((e: unknown) => typeof e === 'string').map((e: string) => e.trim().toLowerCase()).filter(Boolean)
      : [];
    if (mode === 'selected' && emails.length === 0) return json({ error: 'Укажите хотя бы одного получателя.' }, 400);
    if (emails.length > MAX_EMAILS) return json({ error: 'Слишком много получателей.' }, 400);

    // no "get users by email" in the admin API: page through listUsers once (small user base)
    const allUsers: { id: string; email: string }[] = [];
    for (let page = 1; page <= 50; page++) {
      const { data, error } = await admin.auth.admin.listUsers({ page, perPage: 200 });
      if (error) throw error;
      allUsers.push(...data.users.map((u) => ({ id: u.id, email: (u.email ?? '').toLowerCase() })));
      if (data.users.length < 200) break;
    }

    const wanted = new Set(emails);
    const targetIds = mode === 'all'
      ? allUsers.filter((u) => u.id !== caller.id).map((u) => u.id)
      : allUsers.filter((u) => wanted.has(u.email)).map((u) => u.id);
    if (targetIds.length === 0) return json({ error: 'Получатели не найдены.' }, 404);

    const { error: insertError } = await admin
      .from('admin_messages')
      .insert(targetIds.map((id) => ({ target_user_id: id, body: message })));
    if (insertError) throw insertError;

    return json({ ok: true, count: targetIds.length });
  } catch (err) {
    console.error(err);
    return json({ error: 'Ошибка сервера.' }, 500);
  }
});
