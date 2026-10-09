// Deploy in Supabase Studio → Edge Functions → Create a new function → name it "admin-api" → paste this file → Deploy.
// Keep "Verify JWT" ON (default). No secrets to configure: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are injected
// into every Edge Function automatically.
//
// Backend of the oneflow.art/admin page. Only an admin (isAdminUser: ADMIN_EMAILS, optional MFA) may call it — checked here against the caller's own verified
// JWT (the page hiding itself from others is just UX). Requires admin.sql (site_content, support_tickets) and the
// app's existing generation_log / presence tables.
//
// Body { action, ... }:
//   overview                         → users + generation stats + online + tickets + content overrides
//   ticket-update { id, status?, reply? } → change status; a reply is also delivered in-app (admin_messages) when the
//                                      ticket's contact is the email of a registered account
//   content-save  { key, value }     → upsert a landing text override; value null/'' deletes it (back to default)
//   banners-save  { slides }         → validate + store the app home-screen banners (site_content 'app.home.banners');
//                                      an empty list deletes the row, so the app shows its built-in banners again
//   media-upload-url { name, type, size } → one-time signed upload URL for a banner image/video in the public
//                                      'site-media' bucket (admin.sql); the page uploads the file straight to Storage
//   media-delete  { path }           → remove a banner file from that bucket (only home-banners/<uuid>.<ext>)
//   news-save     { items }          → validate + store the landing's «new AI models» cards under the top menu
//                                      (site_content 'landing.news'); an empty list deletes the row → built-in cards
//   generation-pause { paused }      → kill switch for all new paid generations (app_settings)
//   credits-grant { userId, credits, note? } → add a pack of credits to an account by hand (credit_packs, source
//                                      'admin', valid 12 months); requires the app's 202610060001_credits.sql

import { createClient } from 'npm:@supabase/supabase-js@2';

const SUPABASE_URL = Deno.env.get('SUPABASE_URL') ?? '';
const SERVICE_ROLE_KEY = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? '';
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
const ONLINE_WINDOW_MINUTES = 3;
const STATS_DAYS = 30;
const MAX_LOG_ROWS = 50000;

// ---- app home-screen banners -------------------------------------------------------------------
const BANNERS_KEY = 'app.home.banners';
const MEDIA_BUCKET = 'site-media';
const MEDIA_DIR = 'home-banners';
const MAX_SLIDES = 12;
const APP_MODES = ['canvas', 'generate', 'text', 'trends', 'evaluate', 'onelaunch', 'musicaudio', 'motion', 'strategy'];
const MEDIA_TYPES: Record<string, { ext: string; max: number }> = {
  'image/jpeg': { ext: 'jpg', max: 10 * 1024 * 1024 },
  'image/png': { ext: 'png', max: 10 * 1024 * 1024 },
  'image/webp': { ext: 'webp', max: 10 * 1024 * 1024 },
  'image/gif': { ext: 'gif', max: 10 * 1024 * 1024 },
  'video/mp4': { ext: 'mp4', max: 50 * 1024 * 1024 },
  'video/webm': { ext: 'webm', max: 50 * 1024 * 1024 },
};
const MEDIA_PATH_RE = new RegExp(`^${MEDIA_DIR}/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\\.(jpg|png|webp|gif|mp4|webm)$`);

// Strips control characters and caps the length; non-strings become ''.
const cleanText = (v: unknown, max: number) =>
  typeof v === 'string' ? v.replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/g, '').trim().slice(0, max) : '';

class BadInput extends Error {}

// Banner media: a file in our own public bucket, or a same-origin path shipped with the app.
function cleanMedia(v: unknown, publicPrefix: string, required: boolean): string {
  const s = cleanText(v, 1000);
  if (!s) {
    if (required) throw new BadInput('У каждого баннера должна быть картинка или видео.');
    return '';
  }
  if (s.startsWith(publicPrefix) && MEDIA_PATH_RE.test(s.slice(publicPrefix.length))) return s;
  if (/^\/[A-Za-z0-9._\-/]+$/.test(s) && !s.startsWith('//') && !s.includes('..')) return s;
  throw new BadInput('Недопустимый адрес файла баннера.');
}

// Banner link: one of the app's modes ('mode:<id>') or an https:// URL.
function cleanLink(v: unknown): string {
  const s = cleanText(v, 1000);
  if (!s) return '';
  if (s.startsWith('mode:') && APP_MODES.includes(s.slice(5))) return s;
  try {
    const u = new URL(s);
    if (u.protocol === 'https:' && !u.username && !u.password) return u.toString();
  } catch {
    // fall through
  }
  throw new BadInput('Ссылка должна быть режимом приложения или адресом https://');
}

// Landing news cards: an https:// URL or a path on this site; never a mode (the landing has none).
const NEWS_KEY = 'landing.news';
const MAX_NEWS = 6;
function cleanSiteLink(v: unknown): string {
  const s = cleanText(v, 1000);
  if (!s) return '';
  if (/^\/[A-Za-z0-9._\-/?=&#]*$/.test(s) && !s.startsWith('//')) return s;
  try {
    const u = new URL(s);
    if (u.protocol === 'https:' && !u.username && !u.password) return u.toString();
  } catch {
    // fall through
  }
  throw new BadInput('Ссылка должна начинаться с https:// или быть адресом на сайте (/app…).');
}

function cleanNews(input: unknown, publicPrefix: string) {
  if (!Array.isArray(input)) throw new BadInput('Неверный формат новинок.');
  if (input.length > MAX_NEWS) throw new BadInput(`Не больше ${MAX_NEWS} карточек.`);
  return input.map((raw, i) => {
    const x = (raw && typeof raw === 'object' ? raw : {}) as Record<string, unknown>;
    const type = x.type === 'video' ? 'video' : 'image';
    const lang = (l: unknown) => {
      const o = (l && typeof l === 'object' ? l : {}) as Record<string, unknown>;
      return { title: cleanText(o.title, 80), text: cleanText(o.text, 160) };
    };
    const ru = lang(x.ru), en = lang(x.en);
    if (!ru.title && !en.title) throw new BadInput(`Карточка ${i + 1}: добавьте заголовок.`);
    const id = cleanText(x.id, 64).replace(/[^A-Za-z0-9_-]/g, '') || crypto.randomUUID();
    return { id, type, media: cleanMedia(x.media, publicPrefix, true), poster: type === 'video' ? cleanMedia(x.poster, publicPrefix, false) : '',
      isNew: x.isNew !== false, link: cleanSiteLink(x.link), ru, en };
  });
}

function cleanSlides(input: unknown, publicPrefix: string) {
  if (!Array.isArray(input)) throw new BadInput('Неверный формат баннеров.');
  if (input.length > MAX_SLIDES) throw new BadInput(`Не больше ${MAX_SLIDES} баннеров.`);
  return input.map((raw, i) => {
    const x = (raw && typeof raw === 'object' ? raw : {}) as Record<string, unknown>;
    const type = x.type === 'video' ? 'video' : 'image';
    const lang = (l: unknown) => {
      const o = (l && typeof l === 'object' ? l : {}) as Record<string, unknown>;
      return { tag: cleanText(o.tag, 60), title: cleanText(o.title, 140), text: cleanText(o.text, 400), button: cleanText(o.button, 40) };
    };
    const ru = lang(x.ru), en = lang(x.en);
    if (!ru.title && !en.title) throw new BadInput(`Баннер ${i + 1}: добавьте заголовок.`);
    const id = cleanText(x.id, 64).replace(/[^A-Za-z0-9_-]/g, '') || crypto.randomUUID();
    return { id, type, media: cleanMedia(x.media, publicPrefix, true), poster: type === 'video' ? cleanMedia(x.poster, publicPrefix, false) : '', link: cleanLink(x.link), ru, en };
  });
}

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
    if (!caller || !isAdminUser(caller, token)) return json({ error: 'Доступ запрещён.' }, 403);

    const body = await req.json().catch(() => ({}));
    const action = String(body.action ?? 'overview');
    // every change made from the admin page is journaled (security_events); reads are not
    if (action !== 'overview') {
      const pick = (k: string) => (typeof body[k] === 'string' || typeof body[k] === 'number' ? String(body[k]).slice(0, 120) : undefined);
      await auditAdmin(admin, action.replace(/[^a-z-]/g, '').slice(0, 40), caller.id, {
        id: pick('id'), key: pick('key'), userId: pick('userId'), credits: pick('credits'), status: pick('status'), path: pick('path'), paused: body.paused === true,
      });
    }

    // Kill switch for every new paid generation (app_settings.paid_generation_enabled, read by
    // reserve_generation_v2): { paused: true } stops new jobs at once, { paused: false } resumes.
    if (action === 'generation-pause') {
      const paused = body.paused === true;
      const { error } = await admin.from('app_settings').upsert({ key: 'paid_generation_enabled', value: paused ? 0 : 1 });
      if (error) throw error;
      return json({ ok: true, paused });
    }

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

      // unexpired credits per account (credit_packs; absent until the credits migration is run)
      const credits = new Map<string, number>();
      const { data: packs, error: pErr } = await admin.from('credit_packs').select('user_id, credits_left')
        .gt('credits_left', 0).gt('expires_at', new Date().toISOString()).limit(MAX_LOG_ROWS);
      if (!pErr) for (const p of packs ?? []) credits.set(p.user_id, (credits.get(p.user_id) ?? 0) + Number(p.credits_left));

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
            generations30: g?.last30 ?? 0, spendUsd: Math.round((g?.spend ?? 0) * 100) / 100, lastGenerationAt: g?.lastAt ?? null,
            credits: credits.get(u.id) ?? 0 };
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

    const publicPrefix = `${SUPABASE_URL}/storage/v1/object/public/${MEDIA_BUCKET}/`;

    if (action === 'banners-save') {
      let slides;
      try {
        slides = cleanSlides(body.slides, publicPrefix);
      } catch (e) {
        if (e instanceof BadInput) return json({ error: e.message }, 400);
        throw e;
      }
      if (!slides.length) {
        const { error } = await admin.from('site_content').delete().eq('key', BANNERS_KEY);
        if (error) throw error;
        return json({ ok: true, reset: true });
      }
      const value = JSON.stringify({ v: 1, slides });
      const { error } = await admin.from('site_content')
        .upsert({ key: BANNERS_KEY, value, updated_at: new Date().toISOString(), updated_by: caller.email });
      if (error) throw error;
      return json({ ok: true, value });
    }

    if (action === 'news-save') {
      let items;
      try {
        items = cleanNews(body.items, publicPrefix);
      } catch (e) {
        if (e instanceof BadInput) return json({ error: e.message }, 400);
        throw e;
      }
      if (!items.length) {
        const { error } = await admin.from('site_content').delete().eq('key', NEWS_KEY);
        if (error) throw error;
        return json({ ok: true, reset: true });
      }
      const value = JSON.stringify({ v: 1, items });
      const { error } = await admin.from('site_content')
        .upsert({ key: NEWS_KEY, value, updated_at: new Date().toISOString(), updated_by: caller.email });
      if (error) throw error;
      return json({ ok: true, value });
    }

    if (action === 'media-upload-url') {
      const type = String(body.type ?? '');
      const size = Number(body.size ?? 0);
      const spec = MEDIA_TYPES[type];
      if (!spec) return json({ error: 'Поддерживаются JPG, PNG, WebP, GIF, MP4 и WebM.' }, 400);
      if (!Number.isFinite(size) || size <= 0 || size > spec.max) {
        return json({ error: `Файл слишком большой: максимум ${Math.round(spec.max / 1024 / 1024)} МБ.` }, 400);
      }
      const path = `${MEDIA_DIR}/${crypto.randomUUID()}.${spec.ext}`;
      const { data, error } = await admin.storage.from(MEDIA_BUCKET).createSignedUploadUrl(path);
      if (error || !data) throw error ?? new Error('signed upload url');
      return json({ path, signedUrl: data.signedUrl, publicUrl: publicPrefix + path });
    }

    if (action === 'media-delete') {
      const path = String(body.path ?? '');
      if (!MEDIA_PATH_RE.test(path)) return json({ error: 'Неверный путь файла.' }, 400);
      const { error } = await admin.storage.from(MEDIA_BUCKET).remove([path]);
      if (error) throw error;
      return json({ ok: true });
    }

    if (action === 'credits-grant') {
      const userId = String(body.userId ?? '');
      const amount = Number(body.credits);
      const note = typeof body.note === 'string' ? body.note.trim().slice(0, 200) : '';
      if (!/^[0-9a-f-]{36}$/i.test(userId)) return json({ error: 'Неверный пользователь.' }, 400);
      if (!Number.isInteger(amount) || amount < 1 || amount > 1_000_000) return json({ error: 'Укажите от 1 до 1 000 000 кредитов.' }, 400);
      const { data: target, error: uErr } = await admin.auth.admin.getUserById(userId);
      if (uErr || !target.user) return json({ error: 'Пользователь не найден.' }, 404);
      const { error } = await admin.rpc('grant_credits', {
        p_user: userId, p_source: 'admin', p_credits: amount, p_amount_usd: null,
        p_note: note || `Начислено администратором (${caller.email})`, p_external_id: null,
      });
      if (error) throw error;
      const { data: bal, error: bErr } = await admin.rpc('credit_balance', { p_user: userId });
      if (bErr) throw bErr;
      const row = Array.isArray(bal) ? bal[0] : bal;
      return json({ ok: true, credits: Number(row?.available ?? 0) });
    }

    if (action === 'content-save') {
      const key = String(body.key ?? '').trim();
      if (!/^[a-z0-9._-]{1,120}$/.test(key)) return json({ error: 'Неверный ключ.' }, 400);
      if (key === BANNERS_KEY || key === NEWS_KEY) return json({ error: 'Баннеры и новинки сохраняются отдельно.' }, 400);
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
