# Poketree — Style bible

Status: **draft, awaiting art director approval**.

| Rule | Value |
|---|---|
| Grid | 32 × 32 px tiles, top-down view for the club world; side view allowed inside minigames |
| Characters | One fixed canvas size, 4 directions for the MVP, 8 later. Size: **64 px proposed** (room for readable faces and a level badge at 32 px tiles); 48 px is the alternative. Art director decides. |
| Palette | Poketree's own bright, family-friendly palette, not Dagestan's dark parchment. Locked 2026-11-18 in batch 1.3: `assets/palette.hex` (32 colours, swatch `assets/palette-proposal.svg`). Every asset is drawn on it or colour-reduced onto it. |
| Outlines | Decided with the palette in 1.3. |
| Rendering | Integer scaling, nearest-neighbor filtering, positions snapped to whole pixels |
| Names | `<category>/<name>_<variant>_<animation>`, e.g. `poketree/lotus_stage1_idle` |

## Per asset batch

1. Brief: one prompt per asset from this bible and the phase's asset list, approved before generating.
2. Generate through the PixelLab MCP; raw exports go in `assets/raw/`.
3. Review: the art director approves or rejects; rejected prompts get rewritten.
4. Clean in Aseprite: palette, outlines, grid alignment.
5. Pack into atlases and list each in `assets/manifest.json`. The game loads only what the manifest lists.

## Approval

- [ ] Approved by: ________  Date: ________
