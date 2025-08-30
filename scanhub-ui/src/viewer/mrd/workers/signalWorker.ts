// / <reference lib="webworker" />
import type { ComplexMode } from '../types';
import { fftRadix2, fftshift, nextPow2 } from '../utils/fft';

type WorkIn = {
  items: {
    acqId: number;
    nCoils: number;
    nSamples: number;
    data: Float32Array;  // interleaved [re,im] per coil contiguous by coil
    coil: number;
    label: string;
    sampleRateHz: number;
  }[];
  wantTime: boolean;
  wantFreq: boolean;
  mode: ComplexMode;
};

function extractCoil(data: Float32Array, nCoils: number, nSamples: number, coil: number) {
  const offset = coil * (nSamples * 2);
  return data.subarray(offset, offset + nSamples * 2);
}

function toScalar(reim: Float32Array, mode: ComplexMode) {
  const n = reim.length >> 1;
  const out = new Float32Array(n);
  for (let i = 0; i < n; i++) {
    const r = reim[i << 1];
    const im = reim[(i << 1) + 1];
    switch (mode) {
      case 'real': out[i] = r; break;
      case 'imag': out[i] = im; break;
      case 'phase': out[i] = Math.atan2(im, r); break;
      default: out[i] = Math.hypot(r, im);
    }
  }
  return out;
}

self.onmessage = (ev: MessageEvent<WorkIn>) => {
  const { items, wantTime, wantFreq, mode } = ev.data;
  const result: any = { time: [], freq: [] };

  for (const it of items) {
    const reim = extractCoil(it.data, it.nCoils, it.nSamples, it.coil);

    // --- time domain ---
    if (wantTime) {
      const y = toScalar(reim, mode);
      const dt = 1 / it.sampleRateHz;
      const x = new Float32Array(y.length);
      for (let i = 0; i < y.length; i++) x[i] = i * dt * 1000;
      result.time.push({ label: it.label, x, y });
    }

    // --- frequency domain ---
    if (wantFreq) {
      const n0 = reim.length >> 1;
      let buf = new Float32Array(reim);

      // pad to next pow2
      const nfft = nextPow2(n0);
      if (nfft !== n0) {
        const padded = new Float32Array(nfft * 2);
        padded.set(buf);
        buf = padded;
      }

      fftRadix2(buf);
      const yRaw = toScalar(buf, mode);
      const y = fftshift(yRaw);  // <-- shifted spectrum

      const x = new Float32Array(y.length);
      const df = it.sampleRateHz / nfft;
      for (let i = 0; i < y.length; i++) {
        x[i] = (i - nfft / 2) * df; // centered at 0 Hz
      }

      result.freq.push({ label: it.label, x, y });
    }
  }

  // build transferables safely
  const transferables: ArrayBuffer[] = [];
  for (const t of result.time) if (t?.x && t?.y) transferables.push(t.x.buffer, t.y.buffer);
  for (const t of result.freq) if (t?.x && t?.y) transferables.push(t.x.buffer, t.y.buffer);

  (self as any).postMessage(result, transferables);
};
