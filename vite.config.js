import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// Yahoo Finance has no CORS headers, so the browser talks to it through this proxy.
const proxy = {
  '/yahoo': {
    target: 'https://query1.finance.yahoo.com',
    changeOrigin: true,
    rewrite: (path) => path.replace(/^\/yahoo/, ''),
    headers: { 'User-Agent': 'Mozilla/5.0' },
  },
};

export default defineConfig({
  plugins: [react()],
  server: { proxy },
  preview: { proxy },
});
