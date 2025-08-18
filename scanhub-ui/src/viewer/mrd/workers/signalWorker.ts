/// <reference lib="webworker" />
import type { ComplexMode } from '../types';

type WorkIn = {
  items: {
    acqId: number;
    nCoils: number;
    nSamples: number;
    data: Float32Array;  // interleaved [re,im] per coil contiguous by coil
    coil: number;
    label: string;
    sampleRateHz: number; // derived from dwellTimeSec per acquisition
  }[];
  wantTime: boolean;
  wantFreq: boolean;
  mode: ComplexMode;
  zeroPadPow2: boolean;
  downsampleTarget: number; // 0 = off
};

function extractCoil(data: Float32Array, nCoils: number, nSamples: number, coil: number) {
  const offset = coil * (nSamples * 2);
  return data.subarray(offset, offset + nSamples * 2);
}
function toScalar(reim: Float32Array, mode: ComplexMode) {
  const n = reim.length >> 1, out = new Float32Array(n);
  if (mode === 'real') { for (let i=0;i<n;i++) out[i]=reim[i<<1]; return out; }
  if (mode === 'imag') { for (let i=0;i<n;i++) out[i]=reim[(i<<1)+1]; return out; }
  if (mode === 'phase'){ for (let i=0;i<n;i++){ const r=reim[i<<1], im=reim[(i<<1)+1]; out[i]=Math.atan2(im,r);} return out; }
  for (let i=0;i<n;i++){ const r=reim[i<<1], im=reim[(i<<1)+1]; out[i]=Math.hypot(r,im); }
  return out;
}
function nextPow2(n:number){ return 1 << (32 - Math.clz32(Math.max(1, n-1))); }
function fftRadix2(reim: Float32Array){
  const n = reim.length>>1;
  if ((n & (n-1))!==0) throw new Error('FFT length must be power-of-two');
  let j=0;
  for (let i=0;i<n-1;i++){
    const ii=i<<1, jj=j<<1;
    if (i<j){ const tr=reim[ii], ti=reim[ii+1]; reim[ii]=reim[jj]; reim[ii+1]=reim[jj+1]; reim[jj]=tr; reim[jj+1]=ti; }
    let k=n>>1; while(k<=j){ j-=k; k>>=1;} j+=k;
  }
  for (let len=2; len<=n; len<<=1){
    const half=len>>1, ang=-2*Math.PI/len;
    const wpr=Math.cos(ang), wpi=Math.sin(ang);
    for (let s=0;s<n;s+=len){
      let wr=1, wi=0;
      for (let k=0;k<half;k++){
        const i0=(s+k)<<1, i1=(s+k+half)<<1;
        const xr=reim[i1], xi=reim[i1+1];
        const tr=wr*xr - wi*xi, ti=wr*xi + wi*xr;
        const ur=reim[i0], ui=reim[i0+1];
        reim[i0]=ur+tr; reim[i0+1]=ui+ti;
        reim[i1]=ur-tr; reim[i1+1]=ui-ti;
        const tmp=wr; wr=tmp*wpr - wi*wpi; wi=tmp*wpi + wi*wpr;
      }
    }
  }
}
function minmaxDownsample(y: Float32Array, target: number){
  const n=y.length; if (target<=0 || target>=n) return y;
  const bucket=n/target; const out=new Float32Array(target*2); let oi=0;
  for (let i=0;i<target;i++){
    const s=Math.floor(i*bucket), e=Math.min(n, Math.floor((i+1)*bucket));
    if (e<=s) continue;
    let mn=y[s], mx=y[s]; for (let k=s+1;k<e;k++){ const v=y[k]; if (v<mn) mn=v; if (v>mx) mx=v; }
    out[oi++]=mn; out[oi++]=mx;
  }
  return oi<out.length? out.slice(0,oi) : out;
}

self.onmessage = (ev: MessageEvent<WorkIn>) => {
  const { items, wantTime, wantFreq, mode, zeroPadPow2, downsampleTarget } = ev.data;
  const result: any = { time: [], freq: [] };

  for (const it of items){
    const reim = extractCoil(it.data, it.nCoils, it.nSamples, it.coil);

    if (wantTime){
      const y0 = toScalar(reim, mode);
      const y  = downsampleTarget ? minmaxDownsample(y0, downsampleTarget) : y0;
      const dt = 1 / it.sampleRateHz;
      const x  = new Float32Array(y.length);
      for (let i=0;i<y.length;i++) x[i] = i * dt;
      result.time.push({ label: it.label, x, y });
    }

    if (wantFreq){
      const n0 = reim.length>>1;
      let buf = new Float32Array(reim);
      let nfft = n0;
      if (zeroPadPow2){
        const N = nextPow2(n0);
        if (N>n0){ const z=new Float32Array(N*2); z.set(buf); buf=z; nfft=N; }
      }
      fftRadix2(buf);
      const ySpec = toScalar(buf, mode);
      const half  = (nfft>>1)+1;
      let y = ySpec.subarray(0, half);
      if (downsampleTarget) y = minmaxDownsample(y, downsampleTarget);
      const x = new Float32Array(y.length);
      const df = it.sampleRateHz / nfft;
      for (let i=0;i<y.length;i++) x[i] = i * df;
      result.freq.push({ label: it.label, x, y });
    }
  }

  (self as any).postMessage(result, [
    ...result.time.flatMap((t:any)=>[t.x.buffer, t.y.buffer]),
    ...result.freq.flatMap((t:any)=>[t.x.buffer, t.y.buffer]),
  ]);
};
