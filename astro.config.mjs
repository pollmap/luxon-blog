import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  site: 'https://pollmap.github.io',
  base: '/luxon-blog',
  vite: {
    plugins: [tailwindcss()]
  }
});
