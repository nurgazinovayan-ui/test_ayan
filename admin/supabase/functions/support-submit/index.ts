// Deploy in Supabase Studio → Edge Functions → Create a new function → name it "support-submit" → paste this file →
// Deploy, then turn "Verify JWT" OFF for this one: landing visitors aren't signed in. No secrets to configure.
//
// «Написать в поддержку» form on oneflow.art → one row in support_tickets (admin.sql). Public on purpose, so it guards
// itself: a hidden honeypot field, length limits, at most 5 tickets per visitor IP per hour and 100 per hour overall
// (IP stored only as a SHA-256 hash). Tickets are read and answered in oneflow.art/admin through the admin-api function.

import { createClient } from 'npm:@supabase/supabase-js@2';

const SUPABASE_URL = Deno.env.get('SUPABASE_URL') ?? '';
const SERVICE_ROLE_KEY = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? '';
const PER_HOUR = 5;          // per visitor IP
const ALL_PER_HOUR = 100;    // for everyone together — a safety net if a bot rotates or spoofs IPs

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};
const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });

const sha256 = async (s: string) =>
  [...new Uint8Array(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s)))].map((b) => b.toString(16).padStart(2, '0')).join('');

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: corsHeaders });
  if (req.method !== 'POST') return new Response('Method not allowed', { status: 405, headers: corsHeaders });
  try {
    const body = await req.json().catch(() => ({}));
    if (body.website) return json({ ok: true }); // honeypot filled → a bot; pretend success
    const name = String(body.name ?? '').trim().slice(0, 100);
    const contact = String(body.contact ?? '').trim();
    const message = String(body.message ?? '').trim();
    const page = String(body.page ?? '').slice(0, 200);
    if (contact.length < 3 || contact.length > 200) return json({ error: 'Укажите email или телефон для ответа.' }, 400);
    if (message.length < 5 || message.length > 4000) return json({ error: 'Опишите вопрос (от 5 до 4000 символов).' }, 400);

    const ip = (req.headers.get('x-forwarded-for') ?? '').split(',')[0].trim() || 'unknown';
    const ipHash = await sha256(ip + SERVICE_ROLE_KEY);  // peppered with a server secret: the stored hash can't be reversed by trying all IPs
    const admin = createClient(SUPABASE_URL, SERVICE_ROLE_KEY);
    const since = new Date(Date.now() - 3_600_000).toISOString();
    const { count } = await admin.from('support_tickets').select('id', { count: 'exact', head: true }).eq('ip_hash', ipHash).gte('created_at', since);
    if ((count ?? 0) >= PER_HOUR) return json({ error: 'Слишком много обращений. Попробуйте через час.' }, 429);
    const { count: all } = await admin.from('support_tickets').select('id', { count: 'exact', head: true }).gte('created_at', since);
    if ((all ?? 0) >= ALL_PER_HOUR) return json({ error: 'Поддержка сейчас перегружена. Попробуйте позже.' }, 429);

    const { error } = await admin.from('support_tickets').insert({ name, contact, message, page, ip_hash: ipHash });
    if (error) throw error;
    return json({ ok: true });
  } catch (err) {
    console.error(err);
    return json({ error: 'Не удалось отправить. Попробуйте позже.' }, 500);
  }
});
