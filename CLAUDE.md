# Poketree

2D pixel-art club world for New Giza Sporting Club (NGSC). Plan: `docs/plan.md`. Stack: `docs/stack.md`. Current phase task list: `docs/phase-<n>.md`.

## Commands

- `npm run dev` — local dev server
- `npm run typecheck` / `npm run lint` / `npm test` — what CI runs on every push
- `npm run build` — production build to `dist/`; `main` deploys to GitHub Pages

## How to work

1. At the start of a phase, read `docs/plan.md` and this file, write the phase's task list, and wait for approval.
2. Build in vertical slices, one feature at a time: schema, server logic, UI, tests.
3. Close a phase only when every done-criterion is shown working; report what shipped, what was deferred and known issues.
4. Never pull work forward from a later phase.

## Rules

- Stick to the approved stack in `docs/stack.md`; propose any change before making it.
- Every record carries a club id, with a test that club A cannot see club B.
- GR moves only through the server-side ledger; the client never writes a balance.
- GR comes only from games, under a daily cap, and from coach awards.
- All user-facing text goes through `src/i18n/en.json` and `src/i18n/ar.json`; every screen is checked right-to-left.
- Pixel-perfect rendering: integer scale, nearest-neighbor, whole-pixel positions.
- Art comes from the PixelLab MCP per `assets/style-bible.md`; raw exports go in `assets/raw/`, and the game loads only files listed in `assets/manifest.json`. Before generating art, write the batch's task list (assets, prompts, palette) and wait for approval.
- Code never waits on art: use labeled placeholder boxes until the real asset is approved.
- Children: no free-text chat, no public profiles, no real-money purchases. Location is used only for the on-site check and never stored as a history.
- Keys live in environment variables, never in the repo.
- Ask before adding a paid service, running a migration that deletes data, or touching real member data.

## Layout

- `src/` game code (Phaser 3 + Vite, TypeScript)
- `supabase/migrations/`, `supabase/seed.sql` — database schema and seed
- `assets/maps/` — map sources (`blockout.py` regenerates `ngsc-blockout.tmj`)
- Fixed paths: `docs/plan.md`, `CLAUDE.md`, `assets/style-bible.md`, `assets/raw/`, `assets/manifest.json`
