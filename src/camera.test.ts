import { describe, expect, it } from 'vitest';
import { ZOOMS, clampScroll, fitLevel, scrollForZoom, stepLevel } from './camera';

describe('map camera', () => {
  it('fits the whole 3072 x 2176 map', () => {
    expect(ZOOMS[fitLevel(390, 844, 3072, 2176)]).toBe(0.125); // phone portrait
    expect(ZOOMS[fitLevel(480, 270, 3072, 2176)]).toBe(0.125); // nothing fits: smallest level
    expect(ZOOMS[fitLevel(1600, 1200, 3072, 2176)]).toBe(0.5);
  });

  it('steps within the levels', () => {
    expect(stepLevel(0, -1)).toBe(0);
    expect(stepLevel(0, 3)).toBe(1);
    expect(stepLevel(ZOOMS.length - 1, 1)).toBe(ZOOMS.length - 1);
  });

  it('centres a small map and clamps a large one', () => {
    // map 272 px tall at zoom 0.125 is 34 px on an 812 px view: centred
    expect(clampScroll(0, 0.125, 812, 2176)).toBe(2176 / 2 - 406);
    // zoom 1 on a 400 px view: visible x range is [scroll, scroll + 400]
    expect(clampScroll(-50, 1, 400, 3072)).toBe(0);
    expect(clampScroll(5000, 1, 400, 3072)).toBe(3072 - 400);
    expect(clampScroll(100, 1, 400, 3072)).toBe(100);
  });

  it('keeps the point under the finger fixed when zooming', () => {
    const view = { w: 400, h: 300 };
    const s0 = { x: 100, y: 50 };
    const world = (s: { x: number; y: number }, z: number, px: number, py: number) => ({
      x: s.x + view.w / 2 + (px - view.w / 2) / z,
      y: s.y + view.h / 2 + (py - view.h / 2) / z,
    });
    const s1 = scrollForZoom(s0, 0.5, 1, 300, 100, view.w, view.h);
    expect(world(s1, 1, 300, 100)).toEqual(world(s0, 0.5, 300, 100));
  });
});
