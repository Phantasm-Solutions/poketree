# Poketree — Development Plan

Exported from the Claude Doc "Poketree — Development Plan" (rev 34, Nov 17, 2026). The doc is the source of truth; re-export when it changes. Two diagrams (system architecture, build roadmap) live only in the doc.

## Overview

Poketree starts with one client, New Giza Sporting Club (NGSC): Phantasm builds a 2D pixel-art version of the club first and shows it working, instead of quoting a custom build up front.

The concept was pitched as Poketree and Ashgar World to Ashgar, Giza Party to NGSC, and Blue Ribbon World and Club Fantasy to Blue Ribbon. Clubs liked it but stalled on budget, and New Giza turned the quote down as too expensive. With Claude writing the code and PixelLab making the art, the same cycle as *2-3 Years in Dagestan*, Phantasm can walk in with a working product instead.

The MVP is deliberately small: the New Giza map, characters roaming it, a multiplayer tennis game at the tennis court, a marker for members who are physically at the club, phone sign-in controlled by an admin, and GR points that level up each character. Shops, PokeTrees and other clubs come after.

The MVP takes about 13 weeks, with a demo ready for New Giza after about 8. Both estimates assume one developer working with Claude plus part-time art direction.

## Product scope

The MVP is seven small parts built in order, each usable on its own before the next starts.

| Part | What a member sees | Phase |
| --- | --- | --- |
| The New Giza map | NGSC's courts, club house, pool and paths, generated with PixelLab | 1 |
| Pick a character and roam | Open the website, choose a character, walk around the club | 2 |
| Play together | Other players walking around; step onto the tennis court to start a 1v1 match | 3 |
| On-site marker | A marker over characters whose owner is physically at the club | 4 |
| Phone sign-in | Log in with a phone number and a one-time SMS code | 5 |
| Admin allowlist | Admins decide which phone numbers can log in, and who is a coach | 5 |
| Points and levels | GR from games and from coaches; a level on every character | 6 |

**Points rule.** GR is the only currency. Members earn it two ways: digital activities (tennis for now) and awards from coaches, who sign in to their own panel with their phone. Total GR sets the character's level. Digital earnings have a daily cap, so once a shop exists, rewards still lean on real training.

**After the MVP.** A shop to redeem GR for items comes first. Then more court games (football, basketball, padel), PokeTree hunts with the Lotus line (Little Lotus لوتوسة, Junior Lotus لوتوسونة, Big Lotus لوتس كبير) and the Sycamore Fig line (Baby Sycamore Fig جميزوش, Junior Sycamore Fig جميزونة, Big Sycamore Fig جميز كبير), the Giza Party mascots Reeshon (ريشون) and Driblo (دريبلو) as guides, seasonal themes, native apps, and other clubs on subscription.

## Tech requirements and architecture

Claude Code picks the stack in Phase 0, choosing whatever it builds fastest and most reliably, as long as the result meets the requirements below.

*[Diagram in the doc: System architecture · 2 apps, 1 backend, art pipeline]*

Both apps talk to one backend; the game server arrives in Phase 3, and art reaches the game only through the approved atlases.

| Requirement | Why |
| --- | --- |
| Runs in a phone browser, no app install | Members join from a link |
| 2D tilemap and sprites with pixel-perfect scaling | PixelLab art must stay crisp |
| Real-time multiplayer: a shared map and 1v1 tennis, with the server deciding ball and score | Fair matches; Phase 3 |
| Phone sign-in with one-time SMS codes, limited to a list admins manage | Phase 5 |
| Browser location check against a club boundary | On-site marker; Phase 4 |
| A separate web console for admins and coaches | Phases 4–6 |
| Every record tied to a club, with access limited per club | Other clubs can join later without a rebuild |
| English and Arabic, right-to-left layout | NGSC members use both |
| Low running cost and little upkeep at New Giza's scale | One client pays for it at first |

Before building, Claude Code writes `docs/stack.md`: each choice, why it fits these requirements, and its monthly cost at New Giza's scale. The stack is approved once and changes only with sign-off.

**Data model.** Balances are computed from the ledger and never edited directly.

| Table | Holds | Phase |
| --- | --- | --- |
| clubs | Name, map, boundary for the on-site check | 0 |
| places | Named zones on the map, including the tennis court | 1 |
| characters | Character options and each player's pick (per device until sign-in) | 2 |
| matches | Tennis matches: players, score, winner | 3 |
| presence | Who is in the world now and whether they were on site at the last check | 4 |
| allowed_phones | Numbers admins approved, each with a role (member, coach, admin) | 5 |
| profiles | Signed-in person, role, chosen character | 5 |
| ledger | Every GR movement: member, amount, source (game or coach), awarded by, reason, idempotency key | 6 |
| levels | GR threshold for each level | 6 |

## Art pipeline

Art runs the Dagestan way: PixelLab generates, a human art-directs and cleans up in Aseprite, and only approved assets enter the game.

**Style bible (Phase 0, before any mass generation).**

- Grid: 32 × 32 px tiles, top-down view for the club world; side view allowed inside minigames.
- Characters: one fixed canvas size (48 or 64 px, decided in Phase 0), 4 directions for the MVP, 8 later.
- Palette: Poketree's own bright, family-friendly palette, not Dagestan's dark parchment. Run PixelLab's color reduction so every asset sits on it.
- Rendering: integer scaling, nearest-neighbor filtering, positions snapped to whole pixels.

**Per asset batch.**

1. Brief: Claude writes one prompt per asset from the style bible and the phase's asset list.
2. Generate through the PixelLab MCP: characters and animations for avatars and NPCs, top-down tilesets and maps for club grounds, map objects and building kits for courts and buildings, one-direction objects for props, UI assets, sound effects and music.
3. Review: the art director approves or rejects the batch; rejected prompts get rewritten.
4. Clean in Aseprite: palette, outlines, grid alignment.
5. Pack: export sprite sheets, pack into atlases, list each one in `assets/manifest.json`.
6. Ship: the game loads only what the manifest lists.

Asset names follow `<category>/<name>_<variant>_<animation>`, for example `poketree/lotus_stage1_idle`. Code never waits on art: Claude builds with labeled placeholder boxes until the real asset is approved.

**The New Giza map comes first.** It is built from the club's real layout (a site plan if NGSC shares one, otherwise satellite views and photos), so members recognize the tennis courts, club house and gates at a glance. Later clubs reuse the characters and UI and get a new map.

## Phased build plan

Seven phases (0–6) take New Giza from an empty repo to a live MVP in about 13 weeks, and each ends on done-criteria Claude must meet before the next starts.

*[Diagram in the doc: Build roadmap · 7 phases, 2 gates]*

Phases run top to bottom; New Giza sees a demo after Phase 3 and goes live after Phase 6.

### Phase 0 · Foundations (about 1 week)

Goal: a deployed, empty shell and a locked art style.

- Claude Code picks the stack against the tech requirements and writes `docs/stack.md` for approval.
- Repo, CI (typecheck, lint and tests on every push) and a staging deploy.
- Backend with a club record seeded with New Giza.
- A 2D scene rendering at integer scale; English and Arabic strings with a right-to-left switch.
- Style bible written; `CLAUDE.md` seeded from the working rules below.

Done when:

- [ ] The stack in `docs/stack.md` is approved.
- [ ] The staging URL opens on a phone and shows a 2D scene.
- [ ] The art director approves the style bible.

### Phase 1 · The New Giza map (about 2 weeks)

Goal: NGSC as a pixel-art map members recognize.

- Collect the club layout: a site plan if NGSC shares one, otherwise satellite views and photos.
- Generate with PixelLab: ground tileset (grass, paths, water), buildings, courts and landmark props.
- Assemble the map with PixelLab's map tools or Tiled and export a tilemap the game loads, with a collision layer and named zones (tennis courts, club house, pool, gates).
- Map viewer: drag and pinch to explore the whole club in the browser.

Done when:

- [ ] The full map loads on a mid-range Android phone in under 5 seconds.
- [ ] Someone who knows NGSC can point out the tennis courts, club house and main gate without labels.
- [ ] Every walkable and blocked area is marked in the collision layer.

### Phase 2 · Pick a character and roam (about 2 weeks)

Goal: anyone who opens the website picks a character and walks around the club.

- 4–6 PixelLab characters with 4-direction walk and idle animations.
- Character picker on first visit, remembered on that device; no sign-up yet.
- Tap-to-move on phones, arrow keys on desktop, camera follow, collisions.
- A place label appears when a character walks into a named zone.

Done when:

- [ ] From opening the URL to walking takes under a minute, with no account.
- [ ] Characters cannot walk through buildings, fences or water.
- [ ] Movement looks smooth on a mid-range Android phone.

### Phase 3 · Play together: tennis (about 3 weeks)

Goal: players see each other on the map and play tennis with whoever is at the court.

- Shared world: everyone online is on the same map, each with a name and character.
- Tennis court zone: stepping in shows "Play tennis" and pairs two players waiting at the court.
- Simple 1v1 top-down tennis: move, tap to swing, first to 5 points.
- The server runs the ball and the score; phones only send inputs.
- Results saved to `matches`; players return to the map after the match.

Done when:

- [ ] Two phones on mobile data play a full match with no visible desync.
- [ ] A player who drops mid-match rejoins within 15 seconds, or the match ends cleanly.
- [ ] 30 players roam the map at once without lag.

**Gate: demo to New Giza.** The map, roaming and tennis are shown to the club before the sign-in and points work starts.

### Phase 4 · On-site marker (about 1 week)

Goal: anyone can tell who is at the club in person and who is playing from elsewhere.

- At login, the browser asks for location; inside NGSC's boundary counts as on site.
- On-site players get a marker over their character, such as a green pin; online-only players have none.
- The check repeats every 15 minutes while the app is open; denied permission counts as online.
- Admins draw or edit the club boundary in the console.

Done when:

- [ ] A phone inside the club shows the marker; the same account at home does not.
- [ ] Leaving the club removes the marker within 15 minutes.
- [ ] Location is used only for the check and never stored as a history.

### Phase 5 · Phone sign-in and admin (about 2 weeks)

Goal: only people the club approves can play, and they log in with their phone.

- Admin console: add and remove phone numbers one by one or by CSV, and set each number's role (member, coach, admin).
- Phone sign-in with a one-time SMS code; numbers not on the list are told to contact the club.
- The character chosen on the device moves to the account; guest access closes.
- Admins sign in to the console with their own phone number.

Done when:

- [ ] An admin adds a number, and that person signs in within a minute.
- [ ] A number not on the list cannot sign in or join a match.
- [ ] Removing a number signs that person out on their next refresh.

### Phase 6 · Points and levels (about 2 weeks)

Goal: GR rewards play and training, and shows on every character as a level.

- Server-side ledger: append-only, each award with its source and reason.
- Digital points: GR for playing and winning tennis matches, under a daily cap.
- Coach panel: coaches sign in with their phone, find members and award GR with a reason, one at a time or to a whole training group.
- Levels: GR thresholds set in the console; the level shows above the character and on the profile.
- Profile screen: total GR, level, recent awards.

Done when:

- [ ] A coach awards 80 GR to a training group, and each member sees it within seconds.
- [ ] Tennis GR stops at the daily cap, and replayed requests pay once.
- [ ] A character levels up the moment its GR crosses a threshold, visible to other players.

**Gate: live at New Giza.** Members on the club's list use it day to day.

### Later · Shop and beyond

Redeeming GR for items from club shops is the first build after launch; the rest of the list is under Product scope.

## New Giza first, subscription later

New Giza is the only client until the MVP is live there; selling to other clubs waits until then.

- Why New Giza: they already saw Giza Party and declined on price, so a working demo after Phase 3 changes the conversation. The Giza Party name and its mascots can carry over.
- Terms with New Giza are open: a free pilot, a discounted first year, or the first paying subscriber.
- After New Giza, other clubs pay a monthly fee per club, in tiers that mirror the old Visualise, Community and Play packages. A first price hypothesis is the old package price spread over three years: about $850, $1,700 and $3,000 a month.
- Next prospects: Ashgar and Blue Ribbon, which saw earlier proposals, then the Cairo list: Royal, Black Ball, Egypt Weapons Club, Palm Hills, ZED, O West, SODIC and RYZE.

## Working instructions for Claude

Claude builds one phase at a time, works back from the done-criteria, and stops at each phase end for review. Export this doc as Markdown into the repo as `docs/plan.md`, connect the PixelLab MCP in Claude Code, and start with Phase 0.

**How to work.**

1. At the start of a phase, read `docs/plan.md` and `CLAUDE.md`, write the phase's task list, and wait for approval.
2. Build in vertical slices, one feature at a time: schema, server logic, UI, tests.
3. Close the phase only when every done-criterion is shown working; report what shipped, what was deferred and known issues.
4. Never pull work forward from a later phase.

**Rules.**

- Stick to the approved stack in `docs/stack.md`; propose any change before making it.
- Every record carries a club id, with a test that club A cannot see club B.
- GR moves only through the server-side ledger; the client never writes a balance.
- GR comes only from games, under a daily cap, and from coach awards.
- All user-facing text goes through string files in English and Arabic, and every screen is checked right-to-left.
- Pixel-perfect rendering: integer scale, nearest-neighbor, whole-pixel positions.
- Art comes from the PixelLab MCP per the style bible; raw exports go in `assets/raw`, and the game loads only files listed in `assets/manifest.json`.
- Children: no free-text chat, no public profiles, no real-money purchases. Location is used only for the on-site check and never stored as a history.
- Keys live in environment variables, never in the repo.
- Ask before adding a paid service, running a migration that deletes data, or touching real member data.

**Repo layout.** Claude Code proposes it in `docs/stack.md`. These paths stay fixed: `docs/plan.md`, `CLAUDE.md`, `assets/style-bible.md`, `assets/raw/` and `assets/manifest.json`.

## Risks and open questions

The biggest risks are New Giza saying no again, the name, and children's safety; each has a cheap mitigation if handled early.

| Risk | Mitigation |
| --- | --- |
| New Giza declines again | Demo after Phase 3, before sign-in and points are built; everything stays reusable for other clubs |
| "Poketree" sits close to Pokémon's trademarks | Trademark check before any public launch; Giza Party as the NGSC-facing name |
| Phone location is spoofable and weak indoors | The marker means "checked in by location", not proof; coach awards stay the trusted source of GR |
| Points farmed through tennis | Daily cap, server-run matches, less GR for repeat matches against the same opponent |
| Children's data and safety | No chat, location never stored, legal review of Egyptian data protection rules before launch |
| SMS costs and delivery to Egyptian numbers | Test the provider in Phase 5; long sign-in sessions so codes are rare |
| Hundreds of AI assets drift in style | Style bible, one fixed palette, Aseprite pass, few character bases |

**Open questions.**

- [ ] Can New Giza share a site plan of the club for the map?
- [ ] On-site check: is a location check at login enough for now, or should staff confirm check-ins?
- [ ] After phone sign-in launches, can guests still look around without playing?
- [ ] Which game comes after tennis?
- [ ] Commercial terms with New Giza.
- [ ] Product name toward NGSC: Poketree or Giza Party.
- [ ] Who art-directs PixelLab batches, and how often they are reviewed.
