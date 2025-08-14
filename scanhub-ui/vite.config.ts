// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],

  // Let Vite pre-bundle Cornerstone libs (fixes Safari star-export/default issues)
  optimizeDeps: {
    // don't exclude cornerstone/* or codecs
    include: [
      '@cornerstonejs/core',
      '@cornerstonejs/tools',
      '@cornerstonejs/dicom-image-loader',
      '@cornerstonejs/streaming-image-volume-loader',
      '@cornerstonejs/codec-openjpeg',
      '@cornerstonejs/codec-openjph',
      '@cornerstonejs/codec-charls',
      '@cornerstonejs/codec-libjpeg-turbo-8bit',
      '@kitware/vtk.js',
      'dicom-parser',
      'gl-matrix',
    ],
  },

  // WASM + workers
  assetsInclude: ['**/*.wasm'],
  worker: { format: 'es' },

  server: {
    host: '0.0.0.0',
    port: 3000,
    headers: {
      'Cross-Origin-Opener-Policy': 'same-origin',
      'Cross-Origin-Embedder-Policy': 'require-corp',
    },
    // If you proxy through HTTPS:8443 (nginx), HMR may need these:
    // hmr: { protocol: 'wss', host: 'localhost', port: 8443 }, // optional
  },

  preview: {
    host: '0.0.0.0',
    port: 3000,
    headers: {
      'Cross-Origin-Opener-Policy': 'same-origin',
      'Cross-Origin-Embedder-Policy': 'require-corp',
    },
  },

  build: { target: 'es2020' },
});