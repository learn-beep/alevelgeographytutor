import { defineConfig } from 'astro/config';

// scripts/build.mjs builds each exam board separately (OUT_DIR, NO_PUBLIC) and writes the sitemap itself.
export default defineConfig({
  site: 'https://www.alevelgeographytutor.com',
  trailingSlash: 'always',
  outDir: process.env.OUT_DIR || './dist',
  publicDir: process.env.NO_PUBLIC ? './.no-public' : './public',
});
