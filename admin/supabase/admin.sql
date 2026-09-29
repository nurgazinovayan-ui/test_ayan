-- ONEFLOW admin (oneflow.art/admin) — run once in Supabase Studio → SQL Editor.
--
-- site_content   — text overrides for the landing page. Anyone may READ (the public landing fetches them with the
--                  publishable key); nobody may write directly: only the admin-api Edge Function (service role, admin
--                  email checked against the caller's own JWT) inserts, updates or deletes rows.
-- support_tickets — «Написать в поддержку» form on the landing. No policies at all for anon/authenticated: the
--                  support-submit Edge Function inserts (service role), admin-api reads and updates.
--
-- Also required (already created earlier for the app): generation_log, presence, admin_messages.

create table if not exists public.site_content (
  key text primary key,
  value text not null,
  updated_at timestamptz not null default now(),
  updated_by text
);

alter table public.site_content enable row level security;

drop policy if exists "Anyone can read site content" on public.site_content;
create policy "Anyone can read site content"
  on public.site_content for select
  using (true);

create table if not exists public.support_tickets (
  id uuid primary key default gen_random_uuid(),
  name text not null default '',
  contact text not null,
  message text not null,
  page text,
  ip_hash text,
  status text not null default 'new' check (status in ('new', 'in_progress', 'closed')),
  reply text,
  replied_at timestamptz,
  created_at timestamptz not null default now()
);

alter table public.support_tickets enable row level security;
-- No policies on purpose: with RLS on and no policy, anon/authenticated can neither read nor write.

create index if not exists support_tickets_created_at_idx on public.support_tickets (created_at desc);
create index if not exists support_tickets_ip_idx on public.support_tickets (ip_hash, created_at desc);
