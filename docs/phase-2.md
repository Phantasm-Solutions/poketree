# Phase 2 · Pick a character and roam — task list

Status: **awaiting approval** (2026-11-21).

Goal: anyone who opens the website picks a character and walks around the club.

Done when:

- [ ] From opening the URL to walking takes under a minute, with no account.
- [ ] Characters cannot walk through buildings, fences or water.
- [ ] Movement looks smooth on a mid-range Android phone.

## Slices, in build order

Code never waits on art: slices 2.1–2.4 use labelled placeholder characters until the art in 2.5 is approved.

| # | Slice | What ships |
|---|---|---|
| 2.1 | Walk | One placeholder character at the spawn inside the main gate. Arrow keys and WASD on desktop. Collision against the map's collision layer plus the bottom row of solid props (trees, palms, fountain, lamps, shrubs, playground, gate). The camera follows the character once the intro lands. |
| 2.2 | Tap to move | Tap a spot: the character walks there along the shortest path around obstacles (A* on the tile grid). Drag still pans the camera; the camera eases back to the character when it moves. Pinch and +/− keep working. |
| 2.3 | Place labels | Walking into a named zone shows its name for 2 s: tennis courts, club house, Greenheart, both pools, covered hall, kids water play, kids garden, small courts, football pitch, running track, multi court, main gate. English and Arabic names go in the string files. |
| 2.4 | Character picker | Shown on first visit over the zoomed-out map: a row of characters, tap one, then the intro glides in and you can walk. The pick is saved on the device (`localStorage`); later visits skip the picker. A small button changes the character. |
| 2.5 | Character art | Six PixelLab characters with 4-direction walk and idle (below). Replaces the placeholders. |
| 2.6 | Phone check | Test the three done-criteria on a real mid-range Android phone; fix what's slow. |

### Decided (stack and data, delegated)

- **The pick lives on the device only** (`localStorage`). The plan's `characters` table is created in Phase 3, when the shared world first needs other players' picks; a table nobody reads yet would only add a migration to maintain.
- **Free movement, not tile-stepping.** The character moves smoothly at about 3 tiles a second and slides along walls. Collision checks the tiles it overlaps, and positions are drawn on whole pixels.
- **No fences exist on the map yet.** The club's outer edge is blocked; courts stay walkable. Court fences, if wanted, are art for a later batch.

## Character art (2.5) — needs approval before generating

### Characters

Six club members, family-friendly, in sportswear, different ages and looks. Names are for us; players see only the picture.

| # | Name | Prompt |
|---|---|---|
| 1 | Tennis boy | boy about 10 in white tennis shirt and shorts, white cap, holding nothing, friendly |
| 2 | Ponytail girl | girl about 9 in pink sports top and navy shorts, brown ponytail, white sneakers |
| 3 | Football teen | teenage boy in green football jersey and white shorts, short black hair, football boots |
| 4 | Runner | young woman in teal running top and black leggings, hair in a bun, running shoes |
| 5 | Club dad | man in light blue polo shirt and beige shorts, short beard, sunglasses on head |
| 6 | Sporty hijabi girl | girl about 12 in purple sports hijab, long-sleeve purple top and black track pants, sneakers |

### Settings

| Setting | Value | Why |
|---|---|---|
| Tool | `create_character`, mode `v3`, from text | Most detailed sprites; 2 generations each up to 88 px |
| Size | **48 px (recommended) or 64 px — your call** | 48 px stands about 1.5 tiles tall, in scale with benches and the gate. 64 px reads better on small phones but towers over the props. Same cost either way. |
| View | low top-down | Matches the tilesets and props |
| Directions | 4 used (south, east, north, west); v3 draws 8, the other 4 are kept for later | Plan: 4 for the MVP |
| Animations | template `walking` (6 frames) and `breathing-idle` (4 frames), 4 directions each | 1 generation per direction |
| Palette | v3 takes no palette, so each frame is colour-reduced onto `assets/palette.hex` locally (free) | Style bible: every asset on the palette |
| Outline | selective outline | Style bible: props and characters |

### Cost

Per character: 2 (sprite) + 4 (walk) + 4 (idle) = 10 generations. Six characters: **60 generations**; at most 120 with one redo each. PixelLab has 0.5 generations left today and resets on 2026-11-22, so generation starts after the reset.

### Checks before showing

Each character faces the right way in every direction, walk loops without a jump, every pixel is on the palette after reduction, and all six look like one set next to the props.
