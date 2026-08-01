import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  // Base path the app is served under. '/' in dev and for a root deployment;
  // set APP_BASE (e.g. '/pmo/') at build time to serve behind the shared
  // apps.p3mai.com front door. Injected into asset URLs, the router basename,
  // and the API base so the whole app relocates from one env var.
  base: process.env.APP_BASE || '/',
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },
  test: {
    environment: 'jsdom',
    setupFiles: './src/test/setup.js',
    globals: true,
  },
})
