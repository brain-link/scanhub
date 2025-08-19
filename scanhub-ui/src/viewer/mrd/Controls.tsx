import React from 'react';
import type { ColormapName, ComplexMode } from './types';
import Checkbox from '@mui/joy/Checkbox';
import Switch from '@mui/joy/Switch';
import Select from '@mui/joy/Select';
import Option from '@mui/joy/Option';
import FormLabel from '@mui/joy/FormLabel'
// import Slider from '@mui/joy/Slider';
import Box from '@mui/joy/Box';
import Input from '@mui/joy/Input';
import Stack from '@mui/joy/Stack';


export interface ControlsProps {
  metaCount: number;
  overlay: boolean;
  setOverlay: (v: boolean) => void;
  wantTime: boolean;
  setWantTime: (v: boolean) => void;
  wantFreq: boolean;
  setWantFreq: (v: boolean) => void;
  mode: ComplexMode;
  setMode: (v: ComplexMode) => void;
  colormap: ColormapName;
  setColormap: (v: ColormapName) => void;
  coil: number;
  setCoil: (v: number) => void;
  acqRange: [number, number];
  setAcqRange: (v: [number, number]) => void;
  currentAcq: number;
  setCurrentAcq: (v: number) => void;
}

export default function Controls(p: ControlsProps) {
  const maxIdx = Math.max(0, p.metaCount - 1);

  return (
    
    <Stack direction={"row"} sx={{alignItems: 'center'}} gap={2}>
     
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3 }}>
        <Checkbox label="Time" size="sm" checked={p.wantTime} onChange={e=>p.setWantTime(e.target.checked)} />
        <Checkbox label="Frequency" size="sm" checked={p.wantFreq} onChange={e=>p.setWantFreq(e.target.checked)} />
      </Box>

      <FormLabel>Complex</FormLabel>
      <Select
        value={p.mode}
        defaultValue={"abs"}
        onChange={(_, value) => p.setMode(value as ComplexMode)}
        required
      >
          <Option value="abs">Magnitude</Option>
          <Option value="phase">Phase</Option>
          <Option value="real">Real</Option>
          <Option value="imag">Imag</Option>

      </Select>

      <FormLabel>Colormap</FormLabel>
      <Select
        value={p.colormap}
        defaultValue={"abs"}
        onChange={(_, value) => p.setColormap(value as ColormapName)}
        required
      >
          <Option value="viridis">Viridis</Option>
          <Option value="plasma">Plasma</Option>
      </Select>

      <FormLabel>Coil</FormLabel>
      <Input
        type="number"
        value={p.coil}
        slotProps={{ input: {min: 0, max: 999, step: 1} }}
        onChange={(e) => p.setCoil(Math.max(0, Number(e.target.value)))}
      />

      <FormLabel>Overlay</FormLabel>
      <Switch size="sm" checked={p.overlay} onChange={e=>p.setOverlay(e.target.checked)} />

      {/* <Slider
        getAriaLabel={() => 'Acquisition range'}
        min={0}
        max={maxIdx}
        step={1}
        value={p.acqRange}
        onChange={(_, value) => p.setAcqRange(value as [number, number])}
        valueLabelDisplay="auto"
      /> */}
      {
        p.overlay ?
          <Stack direction={"row"} gap={2}>
            <FormLabel>Acquisitions</FormLabel>
            <Input
              type="number"
              value={p.acqRange[0]}
              slotProps={{ input: {min: 0, max: maxIdx, step: 1} }}
              onChange={(e) => p.setAcqRange([Math.max(0, Number(e.target.value)), p.acqRange[1]])}
            />
            <Input
              type="number"
              value={p.acqRange[1]}
              slotProps={{ input: {min: 0, max: maxIdx, step: 1} }}
              onChange={(e) => p.setAcqRange([p.acqRange[0], Math.min(maxIdx, Number(e.target.value))])}
            />
          </Stack> :
          <Stack direction={"row"} gap={2}>
            <FormLabel>Current</FormLabel>
            <Input
              type="number"
              value={p.currentAcq}
              slotProps={{ input: {min: 0, max: maxIdx, step: 1} }}
              onChange={(e) => p.setCurrentAcq(Math.max(0, Math.min(maxIdx, Number(e.target.value))))}
            />
          </Stack>
      }
    </Stack>
  );
}
