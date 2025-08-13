import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

// Helper to resolve from project root
const r = (p: string) => path.resolve(__dirname, p);

export default defineConfig({

  plugins: [react()],

  // Needed for multi-threaded WASM, web workers, and volume rendering in dev    
  server: {
    port: 3000,              // serve at :3000 instead of default 5173
    host: '0.0.0.0',         // optional: allow access from Docker/other hosts
    headers: {
      'Cross-Origin-Opener-Policy': 'same-origin',
      'Cross-Origin-Embedder-Policy': 'require-corp',
    },
  },
  preview: {
    port: 3000,              // also match in preview mode
    host: '0.0.0.0',
    headers: {
      'Cross-Origin-Opener-Policy': 'same-origin',
      'Cross-Origin-Embedder-Policy': 'require-corp',
    },
  },

  build: {
    target: 'es2020',
    // Use modern chunks; workers will be emitted as separate files
    rollupOptions: {
      output: {
        // Long-term cache if you like
        // manualChunks: { vtk: ['@kitware/vtk.js'] },
      },
    },
  },

    resolve: {
    alias: {
      // === Cornerstone codec aliases (mirror your Parcel alias block) ===
      '@cornerstonejs/codec-libjpeg-turbo-8bit/decodewasmjs':
        r('node_modules/@cornerstonejs/codec-libjpeg-turbo-8bit/dist/libjpegturbowasm_decode.js'),
      '@cornerstonejs/codec-libjpeg-turbo-8bit/decodewasm':
        r('node_modules/@cornerstonejs/codec-libjpeg-turbo-8bit/dist/libjpegturbowasm_decode.wasm'),

      '@cornerstonejs/codec-charls/decodewasmjs':
        r('node_modules/@cornerstonejs/codec-charls/dist/charlswasm_decode.js'),
      '@cornerstonejs/codec-charls/decodewasm':
        r('node_modules/@cornerstonejs/codec-charls/dist/charlswasm_decode.wasm'),

      '@cornerstonejs/codec-openjpeg/decodewasmjs':
        r('node_modules/@cornerstonejs/codec-openjpeg/dist/openjpegwasm_decode.js'),
      '@cornerstonejs/codec-openjpeg/decodewasm':
        r('node_modules/@cornerstonejs/codec-openjpeg/dist/openjpegwasm_decode.wasm'),

      '@cornerstonejs/codec-openjph/wasmjs':
        r('node_modules/@cornerstonejs/codec-openjph/dist/openjphjs.js'),
      '@cornerstonejs/codec-openjph/wasm':
        r('node_modules/@cornerstonejs/codec-openjph/dist/openjphjs.wasm'),
    },
  },

  // Let Vite treat wasm files as assets when referenced via new URL()
  assetsInclude: ['**/*.wasm'],

  // Cornerstone + vtk.js can be heavy to prebundle; excluding avoids esbuild worker/wasm quirks
  optimizeDeps: {
    exclude: [
      '@cornerstonejs/core',
      '@cornerstonejs/tools',
      '@cornerstonejs/dicom-image-loader',
      '@cornerstonejs/streaming-image-volume-loader',
      '@kitware/vtk.js'
    ],
  },

});
