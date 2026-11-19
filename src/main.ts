import Phaser from 'phaser';
import manifest from '../assets/manifest.json';
import { ZOOMS, clampScroll, fitLevel, scrollForZoom, stepLevel } from './camera';
import { getLang, isRtl, setLang, t } from './i18n';
import { integerFit } from './scale';

const url = (p: string) => import.meta.env.BASE_URL + p;
const startedAt = performance.now();

class MapScene extends Phaser.Scene {
  private level = 0;
  private pinchFrom = 0;
  private wheel = 0;
  private mapW = 0;
  private mapH = 0;
  private loadingText?: Phaser.GameObjects.Text;

  constructor() {
    super('map');
  }

  preload() {
    const { width, height } = this.scale.gameSize;
    this.loadingText = this.add
      .text(Math.round(width / 2), Math.round(height / 2), t('loading'), {
        fontFamily: 'system-ui, sans-serif', fontSize: '12px', color: '#ffffff', rtl: isRtl(),
      })
      .setOrigin(0.5);
    this.load.tilemapTiledJSON('ngsc', url(manifest.maps.ngsc));
    for (const [key, path] of Object.entries(manifest.tilesets)) this.load.image(key, url(path));
    for (const [key, path] of Object.entries(manifest.images)) this.load.image(key, url(path));
  }

  create() {
    this.loadingText?.destroy();
    const map = this.make.tilemap({ key: 'ngsc' });
    const terrain = map.addTilesetImage('terrain', 'terrain')!;
    // dual-grid ground: one more row and column than the map, drawn half a tile up-left
    map.createLayer('ground', terrain)!.setPosition(-map.tileWidth / 2, -map.tileHeight / 2);

    for (const o of map.getObjectLayer('courts')!.objects) this.add.image(o.x!, o.y!, o.name).setOrigin(0).setDepth(0);
    for (const o of map.getObjectLayer('props')!.objects)
      this.add.image(o.x!, o.y!, o.name).setOrigin(0).setDepth(1 + (o.y! + o.height!) / map.heightInPixels);

    this.mapW = map.widthInPixels;
    this.mapH = map.heightInPixels;
    const { width, height } = this.scale.gameSize;
    this.level = fitLevel(width, height, this.mapW, this.mapH);
    this.cameras.main.setZoom(ZOOMS[this.level]);
    this.clamp();
    this.scale.on('resize', () => this.clamp());

    this.input.addPointer(1);
    this.input.on('pointermove', (p: Phaser.Input.Pointer) => this.onMove(p));
    this.input.on('pointerup', () => (this.pinchFrom = 0));
    this.input.on('wheel', (p: Phaser.Input.Pointer, _o: unknown, _dx: number, dy: number) => {
      this.wheel += dy;
      if (Math.abs(this.wheel) >= 100) {
        this.zoomBy(-Math.sign(this.wheel), p.x, p.y);
        this.wheel = 0;
      }
    });

    (window as unknown as { mapReadyMs: number }).mapReadyMs = Math.round(performance.now() - startedAt);
  }

  private onMove(p: Phaser.Input.Pointer) {
    const a = this.input.pointer1;
    const b = this.input.pointer2;
    if (a.isDown && b.isDown) {
      const d = Phaser.Math.Distance.Between(a.x, a.y, b.x, b.y);
      if (!this.pinchFrom) this.pinchFrom = d;
      const ratio = d / this.pinchFrom;
      if (ratio > 1.5 || ratio < 1 / 1.5) {
        this.zoomBy(ratio > 1 ? 1 : -1, (a.x + b.x) / 2, (a.y + b.y) / 2);
        this.pinchFrom = d;
      }
      return;
    }
    if (!p.isDown) return;
    const cam = this.cameras.main;
    cam.scrollX -= (p.x - p.prevPosition.x) / cam.zoom;
    cam.scrollY -= (p.y - p.prevPosition.y) / cam.zoom;
    this.clamp();
  }

  /** Keep the view on the map, centring it on any axis where it is smaller than the view. */
  private clamp() {
    const cam = this.cameras.main;
    const { width, height } = this.scale.gameSize;
    cam.setScroll(Math.round(clampScroll(cam.scrollX, cam.zoom, width, this.mapW)),
      Math.round(clampScroll(cam.scrollY, cam.zoom, height, this.mapH)));
  }

  zoomBy(dir: number, px?: number, py?: number) {
    const next = stepLevel(this.level, dir);
    if (next === this.level) return;
    const cam = this.cameras.main;
    const { width, height } = this.scale.gameSize;
    const s = scrollForZoom({ x: cam.scrollX, y: cam.scrollY }, ZOOMS[this.level], ZOOMS[next],
      px ?? width / 2, py ?? height / 2, width, height);
    this.level = next;
    cam.setZoom(ZOOMS[next]).setScroll(s.x, s.y);
    this.clamp();
  }
}

const fit = integerFit(window.innerWidth, window.innerHeight);
const game = new Phaser.Game({
  type: Phaser.AUTO,
  parent: 'game',
  pixelArt: true,
  roundPixels: true,
  backgroundColor: '#2f6b3a',
  width: fit.width,
  height: fit.height,
  scale: { mode: Phaser.Scale.NONE, zoom: fit.zoom },
  // Phaser drops to 6 parallel downloads on Android; the map's ~25 small files load faster all at once.
  loader: { maxParallelDownloads: 32 },
  scene: MapScene,
});

window.addEventListener('resize', () => {
  const f = integerFit(window.innerWidth, window.innerHeight);
  game.scale.setZoom(f.zoom);
  game.scale.resize(f.width, f.height);
});

const el = (id: string) => document.getElementById(id) as HTMLButtonElement;
const scene = () => game.scene.getScene('map') as MapScene | null;
const labels = () => {
  document.title = t('title');
  el('lang').textContent = t('switchLanguage');
  el('zoom-in').setAttribute('aria-label', t('zoomIn'));
  el('zoom-out').setAttribute('aria-label', t('zoomOut'));
};
el('lang').addEventListener('click', () => {
  setLang(getLang() === 'en' ? 'ar' : 'en');
  labels();
});
el('zoom-in').addEventListener('click', () => scene()?.zoomBy(1));
el('zoom-out').addEventListener('click', () => scene()?.zoomBy(-1));
setLang('en');
labels();
