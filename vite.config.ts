import { defineConfig } from 'vite';

// GitHub Pages serves the repo at /poketree/
export default defineConfig({
  base: process.env.GITHUB_ACTIONS ? '/poketree/' : '/',
});
