import React from 'react';
import type { ColormapName, ComplexMode } from './types';

export interface ControlsProps {
  metaCount: number;

  overlay: boolean;            setOverlay: (v: boolean) => void;
  wantTime: boolean;           setWantTime: (v: boolean) => void;
  wantFreq: boolean;           setWantFreq: (v: boolean) => void;

  mode: ComplexMode;           setMode: (v: ComplexMode) => void;
  zeroPadPow2: boolean;        setZeroPadPow2: (v: boolean) => void;

  colormap: ColormapName;      setColormap: (v: ColormapName) => void;
  serverStride: number;        setServerStride: (v: number) => void;
  clientDownsample: number;    setClientDownsample: (v: number) => void;

  coil: number;                setCoil: (v: number) => void;

  acqRange: [number, number];  setAcqRange: (v: [number, number]) => void;
  currentAcq: number;          setCurrentAcq: (v: number) => void;
}

export default function Controls(p: ControlsProps) {
  const maxIdx = Math.max(0, p.metaCount - 1);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
      <h3>Raw Data Viewer</h3>

      <label><input type="checkbox" checked={p.overlay} onChange={e=>p.setOverlay(e.target.checked)} /> Overlay</label>

      <div>
        <label><input type="checkbox" checked={p.wantTime} onChange={e=>p.setWantTime(e.target.checked)} /> Time</label>
        <label style={{ marginLeft: 12 }}>
          <input type="checkbox" checked={p.wantFreq} onChange={e=>p.setWantFreq(e.target.checked)} /> Frequency
        </label>
      </div>

      <div>
        <label>Complex</label>
        <select value={p.mode} onChange={e=>p.setMode(e.target.value as ComplexMode)}>
          <option value="abs">Abs (default)</option>
          <option value="phase">Phase</option>
          <option value="real">Real</option>
          <option value="imag">Imag</option>
        </select>
      </div>

      <div>
        <label>Colormap</label>
        <select value={p.colormap} onChange={e=>p.setColormap(e.target.value as ColormapName)}>
          <option value="viridis">viridis</option>
          <option value="plasma">plasma</option>
        </select>
      </div>

      <div>
        <label>Server stride</label>
        <input type="number" min={1} step={1} value={p.serverStride}
               onChange={e=>p.setServerStride(Math.max(1, Number(e.target.value)))} />
      </div>

      <div>
        <label>Client downsample (pts)</label>
        <input type="number" min={0} step={500} value={p.clientDownsample}
               onChange={e=>p.setClientDownsample(Math.max(0, Number(e.target.value)))} />
        <div style={{ fontSize: 12, opacity: 0.7 }}>(0 = off)</div>
      </div>

      <div>
        <label>Coil</label>
        <input type="number" min={0} value={p.coil} onChange={e=>p.setCoil(Math.max(0, Number(e.target.value)))} />
      </div>

      <div>
        <label>Acq range</label>
        <div style={{ display: 'flex', gap: 6 }}>
          <input type="number" min={0} max={maxIdx} value={p.acqRange[0]}
                 onChange={e=>p.setAcqRange([Math.max(0, Number(e.target.value)), p.acqRange[1]])}/>
          <input type="number" min={0} max={maxIdx} value={p.acqRange[1]}
                 onChange={e=>p.setAcqRange([p.acqRange[0], Math.min(maxIdx, Number(e.target.value))])}/>
        </div>
      </div>

      {!p.overlay && (
        <div>
          <label>Current acq</label>
          <input type="number" min={0} max={maxIdx} value={p.currentAcq}
                 onChange={e=>p.setCurrentAcq(Math.max(0, Math.min(maxIdx, Number(e.target.value))))}/>
        </div>
      )}
    </div>
  );
}
