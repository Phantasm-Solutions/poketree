# Poketree — Stack

Status: **approved 2026-11-19**; the product owner delegated all stack decisions to Claude Code. Rule: pick the least-friction option for Claude Code, and decide each thing only when its phase starts.

## Decided now (Phase 0)

| Area | Choice | Why |
|---|---|---|
| Language | TypeScript everywhere | One language; Claude Code typechecks its own work |
| Game client | Phaser 3 + Vite | Most-documented 2D web engine; pixel-perfect scaling built in; runs in a phone browser |
| Backend | Supabase | Postgres with per-club access rules; phone sign-in and realtime are there when later phases need them |
| Repo & CI | GitHub (already connected), GitHub Actions | Typecheck, lint and tests on every push |
| Staging | GitHub Pages | No new account; deploys from the repo |
| Strings | `en.json` / `ar.json` with a right-to-left switch | English and Arabic from day one |
| Tests | Vitest | Runs from the terminal, no setup |

Monthly cost now: $0 (GitHub free, Supabase free tier).

## Decided later

| What | When |
|---|---|
| Map tooling (PixelLab map tools or Tiled) | Phase 1 |
| Multiplayer game server and its hosting | Phase 3 |
| Admin & coach console | Phase 4 |
| SMS sign-in: Akedly | Phase 5 |
| Production hosting and costs | Before launch |

## Repo layout

```
src/                game code
supabase/           migrations and seed
docs/plan.md
docs/stack.md
CLAUDE.md
assets/style-bible.md
assets/raw/
assets/manifest.json
```

More folders get added when a phase needs them.

## Approval

- [x] Approved by: product owner (delegated to Claude Code)  Date: 2026-11-19

## Live services

- Repo: github.com/Phantasm-Solutions/poketree
- Staging: https://phantasm-solutions.github.io/poketree/ (deployed by CI on every push to `main`)
- Supabase: org "Phantasm Solutions" (free), project `poketree`, region Europe. URL and anon key go in environment variables when a phase first uses them.
