export function nextPow2(n:number){
    return 1 << (32 - Math.clz32(Math.max(1, n-1)));
}

export function fftRadix2(reim: Float32Array){
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

export function fftshift<T extends Float32Array | Float64Array>(arr: T): T {
  const n = arr.length;
  const half = Math.floor(n / 2);
  const out = new (arr.constructor as any)(n);
  out.set(arr.subarray(half), 0);
  out.set(arr.subarray(0, half), n - half);
  return out;
}

export function ifftshift<T extends Float32Array | Float64Array>(arr: T): T {
  const n = arr.length;
  const half = Math.floor((n + 1) / 2); // note the offset
  const out = new (arr.constructor as any)(n);
  out.set(arr.subarray(half), 0);
  out.set(arr.subarray(0, half), n - half);
  return out;
}
