import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  // TODO(Milestone 6): add build/deployment configuration only when a target
  // host requires it; keep local development configuration minimal.
  test: {
    environment: 'jsdom',
    setupFiles: './src/test/setup.js',
  },
})
