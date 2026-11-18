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
