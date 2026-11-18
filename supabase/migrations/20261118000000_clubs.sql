-- Phase 0: one club record. Later tables carry club_id and per-club RLS.
create table public.clubs (
  id uuid primary key default gen_random_uuid(),
  slug text not null unique,
  name_en text not null,
  name_ar text not null,
  map text,          -- tilemap path, set in Phase 1
  boundary jsonb,    -- on-site check polygon, set in Phase 4
  created_at timestamptz not null default now()
);

-- RLS on with no policies: nothing is readable from the client until a phase adds a policy.
alter table public.clubs enable row level security;
