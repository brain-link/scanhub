import type { ColormapName } from '../types';

type RGB = [number, number, number];
const VIRIDIS: RGB[] = [
  [68,1,84],[71,44,122],[59,81,139],[44,113,142],[33,144,141],
  [39,173,129],[92,200,99],[170,220,50],[253,231,37]
];
const PLASMA: RGB[] = [
  [13,8,135],[75,3,161],[125,3,168],[168,34,150],[203,70,121],
  [229,107,93],[248,148,65],[253,195,40],[240,249,33]
];

const maps: Record<ColormapName, RGB[]> = { viridis: VIRIDIS, plasma: PLASMA };
const css = ([r,g,b]: RGB) => `rgb(${r},${g},${b})`;

export function colorCycle(name: ColormapName, n: number): string[] {
  const stops = maps[name];
  if (n <= stops.length) return stops.slice(0, n).map(css);
  const out: string[] = [];
  for (let i = 0; i < n; i++) {
    const t = i / (n - 1), p = t * (stops.length - 1);
    const i0 = Math.floor(p), i1 = Math.min(stops.length - 1, i0 + 1);
    const a = stops[i0], b = stops[i1];
    const rgb: RGB = [
      Math.round(a[0] + (b[0]-a[0])*(p - i0)),
      Math.round(a[1] + (b[1]-a[1])*(p - i0)),
      Math.round(a[2] + (b[2]-a[2])*(p - i0)),
    ];
    out.push(css(rgb));
  }
  return out;
}
