# Phase 1 · The New Giza map — task list

Status: **1.1 and 1.2 done (first pass), 1.3 next**. Goal: NGSC as a pixel-art map members recognize.

## Batches

| # | Batch | Output | Paid art? |
|---|---|---|---|
| 1.1 | Layout reference | Zone list below + full-club reference image | No |
| 1.2 | Blockout | Map in flat placeholder colours (grass, path, water, building, court) with collision and named zones | No |
| 1.3 | Terrain art | PixelLab top-down tilesets: grass↔path, grass↔water, grass↔sand. Locks the map palette | Yes |
| 1.4 | Buildings and landmarks | Club house, pool, tennis courts, other courts, F&B, kids areas, fountains, trees | Yes |
| 1.5 | Assemble | Real art painted over the blockout; tilemap, collision and zones exported and listed in `assets/manifest.json` | No |
| 1.6 | Map viewer | Drag and pinch to explore in the browser; phone test against the done-criteria | No |

The blockout comes before any art so we can check "do people recognize the club?" for free, and only pay for art once the layout is right.

## Map scale

- 32 × 32 px tiles, top-down (per the plan's style bible).
- Compressed scale, about 100 × 100 tiles: open lawn and parking shrink, buildings and courts keep their proportions and relative positions.
- The court on the map only needs to be recognizable; tennis itself plays on its own screen in Phase 3.

## Layout reference

Primary source: the aerial photo of the whole club in the Giza Party deck (slide 13). The NGSC event map in the project files fills in detail around Greenheart.

Traced zones, all in `assets/maps/ngsc-blockout.tmj`: tennis courts (clay and hard), club house, Greenheart, small pool, main pool, covered hall, kids water play, kids garden, small courts, football pitch, running track, multi-purpose court, main gate.

## Blockout (1.2)

- `assets/maps/ngsc-blockout.tmj`: Tiled JSON, 96 × 68 tiles at 32 px, layers `ground`, `collision`, `zones`.
- `assets/maps/blockout-tiles.png`: flat placeholder colours, one tile per terrain.
- `assets/maps/blockout.py`: regenerates the map; edit the shapes there to fix the layout.
- Blocked: buildings, water, outside the club. Courts, pitch and track are walkable.

## To confirm by someone who knows NGSC

- The aerial is an oblique photo and may predate recent changes; shapes are approximate.
- Main gate position.
- Which pool is the Olympic one (likely under the covered hall).
- What the east block next to the tennis courts is.

## Terrain art (1.3) — task list

Status: **generated 2026-11-18, awaiting art director review.** Approved: palette, path ↔ water for set B, one grass terrain.

Output: three connected PixelLab top-down tilesets on one locked palette, so the blockout's grass, path, water and sand can be painted in 1.5. Court surfaces (clay, hard, pitch, track, kids garden) are not terrain sets: they come with the courts in 1.4.

### Tasks

1. **Lock the palette.** Approve `assets/palette.hex` (32 colours, swatch in `assets/palette-proposal.svg`). On approval it is added to `assets/style-bible.md` and every later asset is drawn on it or colour-reduced onto it.
2. **Set A · path ↔ grass.** Generated first; its grass tile becomes the shared grass for B and C.
3. **Set B · water ↔ path**, chained on A's path (pools sit in paved decks).
4. **Set C · sand ↔ grass**, chained on A's grass.
5. **Check each sheet** before showing it: terrains not swapped, every pixel on the palette, seams tile in a 3 × 3 repeat. Then paint a test patch (Greenheart and the small pool from the blockout) with the three sets.
6. **Review.** Art director approves or rejects each set; a rejected set gets a rewritten prompt and one regeneration.
7. **Save.** Sheets and Wang metadata to `assets/raw/tilesets/`; not added to `assets/manifest.json` until 1.5 packs them.

### Settings, all three sets

| Setting | Value | Why |
|---|---|---|
| Tool | `create_topdown_tileset`, `mode: "pro"` | Only pro takes a palette and pastes the shared grass exactly |
| Tile size | 32 px | Style bible grid |
| Transition | 0 (flat), 16 tiles per set | Ground only; no banks or walls |
| View | low top-down | PixelLab's character default, so Phase 2 characters match. Barely visible on flat ground |
| Palette | `assets/palette.hex`, name "Poketree" | Locks the map palette |
| Detail / shading | medium detail, basic shading | Reads at phone size; family-friendly, not gritty |

### Prompts

| Set | Lower terrain | Upper terrain | Shape | Walkable |
|---|---|---|---|---|
| A | light beige stone paving slabs, clean club walkway, subtle joints | bright green mowed lawn grass, short even blades, cheerful | roundness 0.5, raggedness 0 (paved edges are crisp) | both |
| B | clear turquoise swimming pool water, gentle ripples, light caustics | path from A (`upper_base_tile_id`) | roundness 0, raggedness 0 (pools are rectangular) | water no, path yes |
| C | soft pale yellow playground sand, fine grain | grass from A (`upper_base_tile_id`) | roundness 1, raggedness 0.3 (soft natural edge) | both |

Grass is always the upper terrain: PixelLab's docs say sets with grass as lower swap terrains more often.

### Cost

Pro tilesets at 32 px cost 15 generations each: 45 for the three sets, 90 at most with one regeneration each. The account has 585.5 generations left in the cycle that resets 2026-11-22.

### Decided

- Set B is **path ↔ water**, not grass ↔ water: every pool sits in a paved deck.
- One grass terrain for `garden` and `lawn`; garden areas get trees and shrubs as props in 1.4.

### Results (awaiting review)

| Set | PixelLab tileset id | Sheet + Wang metadata |
|---|---|---|
| A · path ↔ grass | `be7ae4cb-dd48-4371-942f-2287eaddd46f` | `assets/raw/tilesets/path-grass.png` / `.json` |
| B · water ↔ path | `dc87fe7f-2f7b-4d57-bc19-3e5cdb045be0` | `assets/raw/tilesets/water-path.png` / `.json` |
| C · sand ↔ grass | `69875ba1-204a-4523-9f04-da6cece476f9` | `assets/raw/tilesets/sand-grass.png` / `.json` |

Shared base tiles: grass `d1345a5b-b8ae-489d-a662-643e1cae241e`, path `39d909ea-13df-4da1-a30d-29f380e81c3f` (pasted exactly into B and C). Cost: 45 generations, no regenerations.

Checks (`python assets/maps/tilecheck.py .` re-runs them): 16 tiles per set, 0 pixels off the palette, terrains not swapped. Test patch of Greenheart, both small pools and the kids water play: `assets/maps/terrain-test-patch.png`.

Found by the test patch, for 1.5 to fix in the blockout:

- The kids water play's water touches grass and sand directly (24 tiles); these sets have no grass ↔ water or sand ↔ water edge. Either give it a paved deck in `blockout.py` or add a grass ↔ water set in 1.4/1.5.
- One-tile diagonal paths render as stair-steps; widen them to two tiles or straighten them.
