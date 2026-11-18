import Phaser from 'phaser';
import { getLang, isRtl, setLang, t } from './i18n';
import { integerFit } from './scale';

const TILE = 32;
// Placeholder colours until 1.3 locks the palette.
const GRASS = 0x5a9e4b;
const PATH = 0xd9c48f;

class ShellScene extends Phaser.Scene {
  constructor() {
    super('shell');
  }

  create() {
    this.layout();
    this.scale.on('resize', () => this.layout());
  }

  layout() {
    this.children.removeAll(true);
    const { width, height } = this.scale.gameSize;
    for (let y = 0; y < height; y += TILE)
      for (let x = 0; x < width; x += TILE)
        this.add.rectangle(x, y, TILE - 1, TILE - 1, (x / TILE + y / TILE) % 7 === 0 ? PATH : GRASS).setOrigin(0);

    const style = { fontFamily: 'system-ui, sans-serif', color: '#ffffff', rtl: isRtl() };
    const cx = Math.round(width / 2);
    const cy = Math.round(height / 2);
    this.add.text(cx, cy - 12, t('title'), { ...style, fontSize: '16px' }).setOrigin(0.5);
    this.add.text(cx, cy + 12, t('subtitle'), { ...style, fontSize: '10px' }).setOrigin(0.5);
  }
}

const fit = integerFit(window.innerWidth, window.innerHeight);
const game = new Phaser.Game({
  type: Phaser.AUTO,
  parent: 'game',
  pixelArt: true,
  roundPixels: true,
  backgroundColor: '#1b2b1f',
  width: fit.width,
  height: fit.height,
  scale: { mode: Phaser.Scale.NONE, zoom: fit.zoom },
  scene: ShellScene,
});

window.addEventListener('resize', () => {
  const f = integerFit(window.innerWidth, window.innerHeight);
  game.scale.setZoom(f.zoom);
  game.scale.resize(f.width, f.height);
});

const button = document.getElementById('lang') as HTMLButtonElement;
const refresh = () => {
  button.textContent = t('switchLanguage');
  (game.scene.getScene('shell') as ShellScene | null)?.layout();
};
button.addEventListener('click', () => {
  setLang(getLang() === 'en' ? 'ar' : 'en');
  refresh();
});
setLang('en');
button.textContent = t('switchLanguage');
