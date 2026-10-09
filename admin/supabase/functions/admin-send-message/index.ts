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
// ---- Admin check — generated from supabase/functions/_shared/admin_check.ts by
// scripts/sync-edge-guard.mjs (the admin-api / admin-send-message copies in the admin repo carry the
// same block). Edit the shared file, not this copy.
//
// Admin = a confirmed account whose e-mail is in ADMIN_EMAILS (comma separated secret; defaults to
// the owner). With ADMIN_REQUIRE_MFA=1 the session must also have passed MFA: the JWT, already
// verified by auth.getUser before this runs, carries aal2 (Supabase Auth → MFA → TOTP).
const ADMIN_EMAILS = (Deno.env.get('ADMIN_EMAILS') ?? 'nurgazinov.ayan@gmail.com')
  .split(',')
  .map((s) => s.trim().toLowerCase())
  .filter(Boolean);
function jwtClaim(token: string, claim: string): unknown {
  try {
    const part = token.split('.')[1] ?? '';
    const b64 = part.replace(/-/g, '+').replace(/_/g, '/').padEnd(Math.ceil(part.length / 4) * 4, '=');
    return JSON.parse(atob(b64))?.[claim];
  } catch {
    return undefined;
  }
}
function isAdminUser(user: { email?: string | null; email_confirmed_at?: string | null } | null | undefined, token: string): boolean {
  if (!user || !user.email_confirmed_at || !ADMIN_EMAILS.includes((user.email ?? '').toLowerCase())) return false;
  if (Deno.env.get('ADMIN_REQUIRE_MFA') === '1' && jwtClaim(token, 'aal') !== 'aal2') return false;
  return true;
}
// Every administrative action leaves a row in security_events (who, what, on whom; never secrets).
type AuditClient = { rpc: (fn: string, args: Record<string, unknown>) => PromiseLike<{ error: unknown }> };
async function auditAdmin(client: AuditClient, action: string, actorId: string, details: Record<string, unknown>): Promise<void> {
  const { error } = await client.rpc('log_security_event', {
    p_kind: `admin_${action}`.slice(0, 60),
    p_severity: 'info',
    p_user: actorId,
    p_details: details,
    p_dedupe: null,
  });
  if (error) console.error('audit log failed', error);
}
// ---- end of admin check
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
    if (!caller || !isAdminUser(caller, token)) {
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
    await auditAdmin(admin, 'send_message', caller.id, { mode, recipients: targetIds.length });

    return json({ ok: true, count: targetIds.length });
  } catch (err) {
    console.error(err);
    return json({ error: 'Ошибка сервера.' }, 500);
  }
});
