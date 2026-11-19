# Phase 1 · The New Giza map — task list

Status: **1.1–1.5 done, 1.6 (map viewer) next**. Goal: NGSC as a pixel-art map members recognize.

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

- The kids water play's water touches grass and sand directly (22 tiles); these sets have no grass ↔ water or sand ↔ water edge. Either give it a paved deck in `blockout.py` or add a grass ↔ water set in 1.4/1.5.
- Greenheart's west sand pit touches the path ring (5 tiles); there is no sand ↔ path edge. Pull the sand ellipse 1 tile into the lawn.
- One-tile diagonal paths render as stair-steps; widen them to two tiles or straighten them.

## Buildings and landmarks (1.4) — task list

Status: **done 2026-11-19** (results below). Budget before the batch: 265.5 generations left until the 2026-11-22 reset.

Most of the club's buildings are 7–16 tiles across (224–512 px), larger than any PixelLab object (256 px max). So buildings are painted like terrain, from a roof tileset, over the blockout's building shapes. Courts, the pitch and the track are flat surfaces with exact white lines, so a script draws them on the palette (free, crisp lines). PixelLab makes what needs character: trees, the fountain, the gate, the playground and the other props.

### Tasks

1. **Set D · path ↔ roof** (tileset, 15 gen). Every building gets a 1-tile paved apron in 1.5, so roofs only ever meet path.
2. **Set E · sand ↔ path** (tileset, 15 gen). Chains A's path and C's sand; this fixes the Greenheart sand pit and the kids areas without reshaping them.
3. **Court surfaces by script** (free): clay, hard, padel/green, football pitch with mowing stripes, red running track with lanes. Lines in `#ffffff`, nets in `#1e2430`. Kids garden becomes sand with playground props, since its brown isn't on the palette.
4. **Props** (12 objects, about 61 gen): listed below.
5. **Check** each asset (on palette, size, transparent background), then paint a test patch: club house, Greenheart with its fountain, the tennis courts and the small pool.
6. **Review and save** to `assets/raw/buildings/` and `assets/raw/props/`. One regeneration per rejected asset.

### Tileset settings (D, E)

Same as 1.3: pro, 32 px, low top-down, medium detail, basic shading, Poketree palette.

| Set | Lower | Upper | Shape | Walkable |
|---|---|---|---|---|
| D | path from A (`lower_base_tile_id`) | flat white club building roof, light grey gravel, low parapet edge; `transition_size` 0.25 for a short wall | roundness 0, raggedness 0 | path yes, roof no |
| E | path from A (`lower_base_tile_id`) | sand from C (`upper_base_tile_id`) | roundness 1, raggedness 0.3 | both |

### Props

`create_object_pro_flash`: 1 direction, low top-down, Poketree palette, selective outline. Style anchor: A's grass tile, the same on every call.

| # | Asset | Size (px) | Prompt | Gen |
|---|---|---|---|---|
| 1 | date palm | 64 × 96 | tall date palm tree, green fronds, textured trunk | 5 |
| 2 | shade tree | 64 × 64 | round leafy shade tree, dense green canopy | 5 |
| 3 | shrub | 32 × 32 | small trimmed green hedge bush | 5 |
| 4 | fountain | 64 × 64 | round stone garden fountain, turquoise water, central spout | 5 |
| 5 | bench | 32 × 32 | wooden park bench, light wood, dark metal legs | 5 |
| 6 | pool umbrella | 64 × 64 | white pool umbrella over two blue sun loungers | 5 |
| 7 | football goal | 64 × 32 | white football goal with net, seen from above | 5 |
| 8 | playground | 96 × 96 | kids playground: colorful slide and climbing frame | 5 |
| 9 | splash pad | 64 × 64 | kids water play fountain: colorful mushroom sprayers | 5 |
| 10 | main gate | 128 × 64 | modern sporting club entrance gate, pillars, sign board | 6 |
| 11 | lamp post | 32 × 64 | slim garden lamp post, dark metal | 5 |
| 12 | club house entrance | 96 × 64 | club house entrance canopy, glass doors, sign | 5 |

### Cost

Tilesets 30 plus props 61 comes to 91 generations; 182 at most with one regeneration each.

### Style decision (outlines)

Ground tiles and roofs have no outline. Props and characters use a selective outline in `#1e2430`, so they stand out from the ground. Recorded in `assets/style-bible.md`.

### Results

Approved 2026-11-19 and generated the same day. Cost: 91 generations, no regenerations.

| Asset | PixelLab id | File |
|---|---|---|
| Set D · path ↔ roof | `091433a3-d54f-4801-bf67-2ffcf1692695` (roof base tile `3a470880-d6de-4478-8c21-9169c242268d`) | `assets/raw/tilesets/roof-path.png` / `.json` |
| Set E · sand ↔ path | `efa8bb1b-5394-431f-a5eb-538cbcfad56d` | `assets/raw/tilesets/sand-path.png` / `.json` |
| palm | `cd512b56-01e6-4cc3-9de3-741aed7425b2` | `assets/raw/props/palm.png` |
| shade tree | `20ead522-e662-48c9-a851-ba8cd4e6b6a6` | `assets/raw/props/shade_tree.png` |
| shrub | `387b9673-73c0-4576-88d6-69e344a85366` | `assets/raw/props/shrub.png` |
| fountain | `650efe99-c975-4051-b244-23ba99accc02` | `assets/raw/props/fountain.png` |
| bench | `5b9eb8fc-28cc-4557-baa4-67cab859d2d8` | `assets/raw/props/bench.png` |
| pool umbrella | `bd08a116-c45c-4426-9edc-6b62bf3e1094` | `assets/raw/props/pool_umbrella.png` |
| football goal | `667015b0-9f66-4ef1-b1b8-c3dc1283368e` | `assets/raw/props/football_goal.png` |
| playground | `15990c95-c682-4446-95b7-473868694f51` | `assets/raw/props/playground.png` |
| splash pad | `00202579-ae35-4951-a52b-65ca51043c1d` | `assets/raw/props/splash_pad.png` |
| main gate | `6c5dce97-8a65-4d16-b1c7-805c4a110653` | `assets/raw/props/main_gate.png` |
| lamp post | `16e18e5f-40c8-4a2d-bc4f-96ca708d5da1` | `assets/raw/props/lamp_post.png` |
| club house entrance | `59320396-1d0d-490a-8404-f5cb98fb15e4` | `assets/raw/props/clubhouse_entrance.png` |

Courts, drawn by `python assets/maps/courts.py .`: `assets/raw/courts/` `tennis_clay`, `tennis_hard`, `padel`, `multi_court` and `stadium` (football pitch inside a 4-lane track, 44 × 26 tiles).

Checks: every sheet, prop and court is fully on the palette, and every prop has a transparent background. (PixelLab's object `/download` returns RGB; take the `rotations/unknown.png` URL instead.) `python assets/maps/patch14.py .` paints `assets/maps/art-test-patch.png` (club house, Greenheart, small pool, kids water play, tennis).

For 1.5, from the patch:

- **Roofs read as plain white areas.** Members recognise buildings by shape and detail, so add rooftop props (AC units, skylights, solar panels) or a second roof colour for the club house.
- **Building edges.** Roofs meet grass in 72 tiles and water in 14; the planned 1-tile paved apron around every building fixes this.
- **Water edges.** Water still meets grass or sand in 11 tiles (kids water play); give it a paved deck.
- **Courts.** The blockout's courts are skewed quads traced from an oblique photo. Straighten them into rectangles sized to the court sprites (tennis 5 × 9 tiles, padel 3 × 5).
- **Prop density.** At 32 px tiles, Greenheart is 24 tiles across, so it needs dozens of props, not a handful, to feel like a garden.

## Assemble (1.5)

Status: **done 2026-11-19**. No paid art.

Rebuild the map from scratch:

```
python assets/maps/blockout.py
python assets/maps/courts.py .
python assets/maps/assemble.py .
```

What changed in the blockout (`blockout.py`):

- **Courts are straight rectangles** placed in tile coords: one row of tennis (3 clay, 1 hard, 5 × 9 tiles each), 4 padel (3 × 5), the stadium (pitch inside a 4-lane track, 38 × 22) and the multi court (6 × 10, turned upright). They are drawn last, so walks and parking don't cut into them, and are listed in the new `courts` object layer.
- **Kids water play is a paved splash pad** with two splash fountains, not open water.

What the assembler does (`assemble.py`):

- **Edge repair.** Wherever terrains meet that no tileset joins (roof–grass, water–grass, grass–path–sand), it paves the lower terrain, so every building and pool gets a paved apron. 487 tiles were repaired; every corner now has a tile.
- **Ground.** Painted on a dual grid (one more row and column, shifted half a tile). The 51 Wang tiles in use are packed into `public/maps/terrain.png`.
- **Collision.** Roofs, water and everything outside the club are blocked, 2950 of 6528 tiles. Props carry a `solid` flag for Phase 2 movement.
- **Props (492), placed by deterministic rules:**
  - Landmarks: fountain at Greenheart's centre, club house entrance on its south face, main gate, playground, splash pads, goals on the pitch and umbrellas along the pool decks.
  - Greenheart: palms around the lawn edge, benches and lamps on the ring path, and shade trees that leave the middle open.
  - Elsewhere: lamps along the walks, shrubs by building aprons, trees through the gardens (denser along the club edge), and AC units and skylights on roofs.
- **Output** (the game loads only this): `public/maps/ngsc.tmj`, with layers `ground`, `collision`, `courts`, `props` and `zones`. Also `public/maps/terrain.png`, `public/maps/collision.png`, `public/sprites/*.png` and `assets/manifest.json`. `src/manifest.test.ts` checks that every listed file exists, every placed sprite is listed and the layer sizes match.
- **Preview** of the whole map: `assets/maps/ngsc-map-preview.png` (3072 × 2176).

Known issues, for whoever knows NGSC to check in 1.6:

- Roofs are still mostly white. Details help, but the club house is not yet a distinct landmark from above.
- The main pool under the covered hall came out narrow after edge repair.
- Layout positions are from the oblique aerial; see "To confirm" above.
