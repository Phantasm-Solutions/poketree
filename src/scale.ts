// Shortest screen side shows at least this many game pixels.
export const MIN_VIEW = 240;

/** Largest integer zoom that keeps MIN_VIEW game pixels on the short side, and the game size at that zoom. */
export function integerFit(screenW: number, screenH: number) {
  const zoom = Math.max(1, Math.floor(Math.min(screenW, screenH) / MIN_VIEW));
  // Never 0: a zero-size canvas (hidden tab at load) breaks Phaser's WebGL boot.
  return { zoom, width: Math.max(1, Math.ceil(screenW / zoom)), height: Math.max(1, Math.ceil(screenH / zoom)) };
}
