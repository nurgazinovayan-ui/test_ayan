// Deploy in Supabase Studio → Edge Functions → Create a new function → name it "admin-api" → paste this file → Deploy.
// Keep "Verify JWT" ON (default). No secrets to configure: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are injected
// into every Edge Function automatically.
//
// Backend of the oneflow.art/admin page. Only ADMIN_EMAIL may call it — checked here against the caller's own verified
// JWT (the page hiding itself from others is just UX). Requires admin.sql (site_content, support_tickets) and the
// app's existing generation_log / presence tables.
//
// Body { action, ... }:
//   overview                         → users + generation stats + online + tickets + content overrides
//   ticket-update { id, status?, reply? } → change status; a reply is also delivered in-app (admin_messages) when the
//                                      ticket's contact is the email of a registered account
//   content-save  { key, value }     → upsert a landing text override; value null/'' deletes it (back to default)

import { createClient } from 'npm:@supabase/supabase-js@2';

const SUPABASE_URL = Deno.env.get('SUPABASE_URL') ?? '';
const SERVICE_ROLE_KEY = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? '';
const ADMIN_EMAIL = 'nurgazinov.ayan@gmail.com';
const ONLINE_WINDOW_MINUTES = 3;
const STATS_DAYS = 30;
const MAX_LOG_ROWS = 50000;

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};
const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });

type LogRow = { user_id: string; email: string; model: string; category: string; cost_usd: number | null; created_at: string };

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: corsHeaders });
  if (req.method !== 'POST') return new Response('Method not allowed', { status: 405, headers: corsHeaders });
  try {
    const admin = createClient(SUPABASE_URL, SERVICE_ROLE_KEY);
    const token = (req.headers.get('Authorization') ?? '').replace(/^Bearer\s+/i, '');
    const { data: callerData } = await admin.auth.getUser(token);
    const caller = callerData.user;
    // exactly one account: the admin email, and only once that address is confirmed (Google sign-ins are confirmed by Google)
    if (!caller || !caller.email_confirmed_at || caller.email?.toLowerCase() !== ADMIN_EMAIL.toLowerCase()) return json({ error: 'Доступ запрещён.' }, 403);

    const body = await req.json().catch(() => ({}));
    const action = String(body.action ?? 'overview');

    // every account (small user base: page through listUsers once)
    const listUsers = async () => {
      const users: { id: string; email: string; createdAt: string; lastSignIn: string | null; confirmed: boolean; provider: string }[] = [];
      for (let page = 1; page <= 50; page++) {
        const { data, error } = await admin.auth.admin.listUsers({ page, perPage: 200 });
        if (error) throw error;
        users.push(...data.users.map((u) => ({
          id: u.id,
          email: (u.email ?? '').toLowerCase(),
          createdAt: u.created_at,
          lastSignIn: u.last_sign_in_at ?? null,
          confirmed: Boolean(u.email_confirmed_at),
          provider: String(u.app_metadata?.provider ?? 'email'),
        })));
        if (data.users.length < 200) break;
      }
      return users;
    };

    if (action === 'overview') {
      const users = await listUsers();

      const { data: logData, error: logError } = await admin
        .from('generation_log')
        .select('user_id, email, model, category, cost_usd, created_at')
        .order('created_at', { ascending: false })
        .limit(MAX_LOG_ROWS);
      if (logError) throw logError;
      const log = (logData ?? []) as LogRow[];

      const since = Date.now() - STATS_DAYS * 86_400_000;
      const perUser = new Map<string, { total: number; spend: number; last30: number; lastAt: string | null }>();
      const byModel = new Map<string, { model: string; category: string; count: number; spend: number }>();
      const byDay = new Map<string, { count: number; spend: number }>();
      for (const r of log) {
        const cost = Number(r.cost_usd ?? 0);
        const u = perUser.get(r.user_id) ?? { total: 0, spend: 0, last30: 0, lastAt: null };
        u.total += 1; u.spend += cost; u.lastAt = u.lastAt ?? r.created_at;
        const t = Date.parse(r.created_at);
        if (t >= since) {
          u.last30 += 1;
          const m = byModel.get(r.model) ?? { model: r.model, category: r.category, count: 0, spend: 0 };
          m.count += 1; m.spend += cost; byModel.set(r.model, m);
          const day = r.created_at.slice(0, 10);
          const d = byDay.get(day) ?? { count: 0, spend: 0 };
          d.count += 1; d.spend += cost; byDay.set(day, d);
        }
        perUser.set(r.user_id, u);
      }

      const onlineSince = new Date(Date.now() - ONLINE_WINDOW_MINUTES * 60_000).toISOString();
      const { data: presence } = await admin.from('presence').select('user_id, last_seen');
      const lastSeen = new Map((presence ?? []).map((p: { user_id: string; last_seen: string }) => [p.user_id, p.last_seen]));

      const { data: tickets, error: tErr } = await admin
        .from('support_tickets')
        .select('id, name, contact, message, page, status, reply, replied_at, created_at')
        .order('created_at', { ascending: false })
        .limit(500);
      if (tErr) throw tErr;

      const { data: content, error: cErr } = await admin.from('site_content').select('key, value, updated_at');
      if (cErr) throw cErr;

      return json({
        generatedAt: new Date().toISOString(),
        users: users.map((u) => {
          const g = perUser.get(u.id);
          const seen = lastSeen.get(u.id) ?? null;
          return { ...u, lastSeen: seen, online: Boolean(seen && seen >= onlineSince), generations: g?.total ?? 0,
            generations30: g?.last30 ?? 0, spendUsd: Math.round((g?.spend ?? 0) * 100) / 100, lastGenerationAt: g?.lastAt ?? null };
        }),
        stats: {
          days: STATS_DAYS,
          totalGenerations: log.length,
          byDay: [...byDay.entries()].map(([day, v]) => ({ day, ...v })).sort((a, b) => a.day.localeCompare(b.day)),
          byModel: [...byModel.values()].sort((a, b) => b.count - a.count),
        },
        recent: log.slice(0, 300).map((r) => ({ email: r.email, model: r.model, category: r.category, costUsd: Number(r.cost_usd ?? 0), createdAt: r.created_at })),
        tickets: tickets ?? [],
        content: content ?? [],
      });
    }

    if (action === 'ticket-update') {
      const id = String(body.id ?? '');
      if (!id) return json({ error: 'Не указано обращение.' }, 400);
      const patch: Record<string, unknown> = {};
      if (body.status && ['new', 'in_progress', 'closed'].includes(body.status)) patch.status = body.status;
      const reply = typeof body.reply === 'string' ? body.reply.trim() : '';
      let delivered = false;
      if (reply) {
        patch.reply = reply; patch.replied_at = new Date().toISOString();
        if (!patch.status) patch.status = 'closed';
        const { data: t } = await admin.from('support_tickets').select('contact').eq('id', id).single();
        const contact = String(t?.contact ?? '').trim().toLowerCase();
        if (contact.includes('@')) {
          const match = (await listUsers()).find((u) => u.email === contact);
          if (match) {
            const { error } = await admin.from('admin_messages').insert({ target_user_id: match.id, body: `Поддержка ONEFLOW: ${reply}` });
            if (error) throw error;
            delivered = true;
          }
        }
      }
      if (!Object.keys(patch).length) return json({ error: 'Нечего сохранять.' }, 400);
      const { error } = await admin.from('support_tickets').update(patch).eq('id', id);
      if (error) throw error;
      return json({ ok: true, deliveredInApp: delivered });
    }

    if (action === 'content-save') {
      const key = String(body.key ?? '').trim();
      if (!/^[a-z0-9._-]{1,120}$/.test(key)) return json({ error: 'Неверный ключ.' }, 400);
      const value = typeof body.value === 'string' ? body.value : null;
      if (value === null || value.trim() === '') {
        const { error } = await admin.from('site_content').delete().eq('key', key);
        if (error) throw error;
        return json({ ok: true, reset: true });
      }
      if (value.length > 5000) return json({ error: 'Слишком длинный текст.' }, 400);
      const { error } = await admin.from('site_content')
        .upsert({ key, value, updated_at: new Date().toISOString(), updated_by: caller.email });
      if (error) throw error;
      return json({ ok: true });
    }

    return json({ error: 'Неизвестное действие.' }, 400);
  } catch (err) {
    console.error(err);
    return json({ error: 'Ошибка сервера.' }, 500);
  }
});
