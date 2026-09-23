// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  // Configure site URL and base path (supports custom domain or repository subpath)
  site: process.env.SITE_URL || 'https://kairosvector.com',
  base: process.env.BASE_PATH || '/',
  integrations: [sitemap()],
  build: {
    format: 'directory'
  }
});
