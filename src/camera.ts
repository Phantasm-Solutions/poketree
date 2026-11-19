// Camera zoom levels for the map viewer. Powers of two keep pixel art even when zoomed out
// (every 2nd, 4th or 8th pixel) and whole-pixel when zoomed in.
export const ZOOMS = [0.125, 0.25, 0.5, 1, 2] as const;

/** Largest zoom level that shows the whole map in the view (level 0 if none does). */
export function fitLevel(viewW: number, viewH: number, mapW: number, mapH: number): number {
  let best = 0;
  ZOOMS.forEach((z, i) => {
    if (mapW * z <= viewW && mapH * z <= viewH) best = i;
  });
  return best;
}

export const stepLevel = (level: number, dir: number): number =>
  Math.min(ZOOMS.length - 1, Math.max(0, level + Math.sign(dir)));

/**
 * Clamp one axis of a Phaser camera scroll so the view stays on the map; when the map is
 * smaller than the view on that axis, centre it.
 */
export function clampScroll(scroll: number, zoom: number, view: number, map: number): number {
  const half = view / 2;
  const seen = view / zoom;
  if (seen >= map) return map / 2 - half;
  return Math.min(Math.max(scroll, seen / 2 - half), map - half - seen / 2);
}

/**
 * New camera scroll that keeps the world point under screen point (px, py) in place when
 * zoom changes from z0 to z1. Phaser cameras zoom around the view's centre.
 */
export function scrollForZoom(
  scroll: { x: number; y: number },
  z0: number,
  z1: number,
  px: number,
  py: number,
  viewW: number,
  viewH: number,
): { x: number; y: number } {
  const wx = scroll.x + viewW / 2 + (px - viewW / 2) / z0;
  const wy = scroll.y + viewH / 2 + (py - viewH / 2) / z0;
  return { x: wx - viewW / 2 - (px - viewW / 2) / z1, y: wy - viewH / 2 - (py - viewH / 2) / z1 };
}
