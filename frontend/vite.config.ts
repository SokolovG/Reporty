import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import tailwindcss from '@tailwindcss/vite';
import { BACKEND_API_URL } from '$env/static/private';

export default defineConfig({
  plugins: [
    tailwindcss(),
    sveltekit(),
  ],
  server: {
    proxy: {
      '/api': {
        target: BACKEND_API_URL,
        changeOrigin: true,
      }
    }
  }
});
