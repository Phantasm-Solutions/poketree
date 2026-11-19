import { existsSync, readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import manifest from '../assets/manifest.json';

const pub = (p: string) => new URL(`../public/${p}`, import.meta.url);

interface Layer { name: string; type: string; width?: number; height?: number; data?: number[]; objects?: { name: string }[] }
const map = JSON.parse(readFileSync(pub(manifest.maps.ngsc), 'utf8')) as { width: number; height: number; layers: Layer[] };
const layer = (name: string) => map.layers.find((l) => l.name === name)!;

describe('asset manifest', () => {
  it('lists only files that exist', () => {
    const paths = [...Object.values(manifest.maps), ...Object.values(manifest.tilesets), ...Object.values(manifest.images)];
    for (const p of paths) expect(existsSync(pub(p)), p).toBe(true);
  });

  it('has every sprite the map places', () => {
    for (const name of ['courts', 'props']) {
      for (const o of layer(name).objects!) expect(manifest.images, o.name).toHaveProperty(o.name);
    }
  });

  it('has full ground and collision layers', () => {
    expect(layer('ground').data).toHaveLength((map.width + 1) * (map.height + 1));
    expect(layer('collision').data).toHaveLength(map.width * map.height);
  });
});
