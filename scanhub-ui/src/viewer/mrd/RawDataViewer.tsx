import React, { useEffect, useMemo, useRef, useState } from 'react';
import ReactECharts from 'echarts-for-react';

import { useData } from './hooks/useData';
import { useMeta } from './hooks/useMeta';
import { ColorPalette, ComplexMode } from './types';
import type { CallbackDataParams } from 'echarts/types/dist/shared';
import { plotColorPalettes, plotColorPaletteOptions } from './utils/colormaps';
import { WorkerMessage } from './utils/interfaces';
import Container from '@mui/joy/Container';
import AlertItem from '../../components/AlertItem';
import { Alerts } from '../../interfaces/components.interface';
import Box from '@mui/joy/Box';
import Card from '@mui/joy/Card';
import Checkbox from '@mui/joy/Checkbox';
import IconButton from '@mui/joy/IconButton';
import Input from '@mui/joy/Input';
import Option from '@mui/joy/Option';
import Select from '@mui/joy/Select';
import Sheet from '@mui/joy/Sheet';
import Stack from '@mui/joy/Stack';
import Switch from '@mui/joy/Switch';
import Typography from '@mui/joy/Typography';
import { Popper } from '@mui/base/Popper';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import TuneIcon from '@mui/icons-material/Tune';
import { type EChartsOption } from 'echarts';

import { init, use as echartsUse } from 'echarts/core';
import { LineChart } from 'echarts/charts';
import {
  GridComponent,
  LegendComponent,
  TooltipComponent,
  DataZoomComponent,
  ToolboxComponent,
} from 'echarts/components';
import type {
  SeriesOption,
  XAXisComponentOption,
  YAXisComponentOption,
  GridComponentOption,
  DataZoomComponentOption,
} from 'echarts';
import { CanvasRenderer } from 'echarts/renderers';
import { MRDAcquisitionInfo } from '../../openapi/generated-client/protocol';
import { ParsedAcq } from './utils/packet';
echartsUse([
  LineChart,
  GridComponent,
  LegendComponent,
  TooltipComponent,
  DataZoomComponent,
  ToolboxComponent,
  CanvasRenderer,
]);
const echartsCore = { init, use: echartsUse };


interface RawDataViewerProps {
  selectedResultId: string;
  protocolId: string;
  taskId: string;
  onDownload?: () => void;
  taskName?: string;
}

export default function RawDataViewer({ selectedResultId, protocolId, taskId, onDownload, taskName }: RawDataViewerProps) {
  const [overlay, setOverlay] = useState(true);
  const [wantTime, setWantTime] = useState(true);
  const [wantFreq, setWantFreq] = useState(false);
  const [mode, setMode] = useState<ComplexMode>('abs');
  const [colorPalette, setColorPalette] = useState<ColorPalette>(plotColorPalettes.default);
  const [coil, setCoil] = useState(0);
  const [acqRange, setAcqRange] = useState<[number, number]>([0, 0]);
  const [currentAcq, setCurrentAcq] = useState(0);

  const [settingsOpen, setSettingsOpen] = useState(false);
  const settingsAnchorRef = useRef<HTMLButtonElement>(null);
  const settingsPanelRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!settingsOpen) return;
    const handleMouseDown = (e: MouseEvent) => {
      if (
        !settingsAnchorRef.current?.contains(e.target as Node) &&
        !settingsPanelRef.current?.contains(e.target as Node)
      ) {
        setSettingsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleMouseDown);
    return () => document.removeEventListener('mousedown', handleMouseDown);
  }, [settingsOpen]);

  const containerRef = useRef<HTMLDivElement | null>(null);

  const idsReady = !!protocolId && !!taskId && !!selectedResultId;

  const metaQuery = useMeta(idsReady, protocolId, taskId, selectedResultId);

  const maxIdx = Math.max(0, (metaQuery.data?.acquisitions?.length ?? 0) - 1);

  useEffect(() => {
    if (!metaQuery.data) return;
    const n = metaQuery.data.acquisitions?.length ?? 1;
    setAcqRange([0, Math.min(10, n - 1)]);
    setCurrentAcq(0);
    setCoil(0);
  }, [metaQuery.data]);

  const idsExpr = useMemo(() => {
    const meta = metaQuery.data;
    if (!meta) return '';
    if (overlay) {
      const [s, e] = acqRange;
      const end = Math.min(e, s + 31);
      return `${s}-${end}`;
    }
    return String(currentAcq);
  }, [metaQuery.data, overlay, acqRange, currentAcq]);

  const acqQuery = useData(
    idsReady && !!idsExpr,
    protocolId,
    taskId,
    selectedResultId,
    idsExpr,
    0,
    1
  );

  const workerRef = useRef<Worker | null>(null);
  useEffect(() => {
    workerRef.current = new Worker(new URL('./workers/signalWorker.ts', import.meta.url), { type: 'module' });
    return () => workerRef.current?.terminate();
  }, []);

  const [option, setOption] = useState<EChartsOption>({});

  useEffect(() => {
    const meta = metaQuery.data;
    const batch = acqQuery.data;
    const worker = workerRef.current;
    if (!meta || !batch || !worker) return;

    const dwellById = new Map<number, number>();
    meta.acquisitions?.forEach((a: MRDAcquisitionInfo) => dwellById.set(a.acquisition_id, a.dwell_time));

    const items = batch.map((acq: ParsedAcq) => {
      const dwell = dwellById.get(acq.acqId)!;
      const fs = 1 / dwell;
      return {
        acqId: acq.acqId,
        nCoils: acq.nCoils,
        nSamples: acq.nSamples,
        data: acq.data,
        coil,
        label: `Acq k=${acq.acqId} (Coil ${coil})`,
        sampleRateHz: fs,
      };
    });

    const onMsg = (ev: MessageEvent<WorkerMessage>) => {
      const { time, freq } = ev.data as {
        time: { label: string; x: Float32Array; y: Float32Array }[];
        freq: { label: string; x: Float32Array; y: Float32Array }[];
      };

      const series: SeriesOption[] = [];
      const xAxis: XAXisComponentOption[] = [];
      const yAxis: YAXisComponentOption[] = [];
      const grid: GridComponentOption[] = [];
      const dataZoom: DataZoomComponentOption[] = [];

      const yLabel = (domain: 'time' | 'freq') => {
        switch (mode) {
          case 'abs': return domain === 'time' ? 'Magnitude s(t)' : 'Magnitude S(f)';
          case 'phase': return 'Phase / rad';
          case 'real': return domain === 'time' ? 'Real s(t)' : 'Real S(f)';
          case 'imag': return domain === 'time' ? 'Imaginary s(t)' : 'Imaginary S(f)';
          default: return '';
        }
      };

      const addPanel = (
        traces: { label: string; x: Float32Array; y: Float32Array }[],
        title: 'Time' | 'Freq',
        topPct: number,
        heightPct: number,
        gridIdx: number
      ) => {
        grid.push({ top: `${topPct}%`, height: `${heightPct}%`, left: 60, right: 20 });
        xAxis.push({
          type: 'value', gridIndex: gridIdx,
          name: title === 'Time' ? 'Time / ms' : 'Frequency / Hz',
          nameLocation: 'middle',
        });
        yAxis.push({
          type: 'value', gridIndex: gridIdx,
          name: yLabel(title === 'Time' ? 'time' : 'freq'),
          nameLocation: 'middle',
        });
        traces.forEach((t) => {
          const len = t.x.length;
          const pts = new Array(len);
          for (let i = 0; i < len; i++) pts[i] = [t.x[i], t.y[i]];
          series.push({
            type: 'line', name: t.label,
            xAxisIndex: gridIdx, yAxisIndex: gridIdx,
            showSymbol: false, sampling: 'lttb',
            lineStyle: { width: 1.5 }, data: pts,
          });
        });
        dataZoom.push({ type: 'inside', xAxisIndex: gridIdx, filterMode: 'none' });
      };

      if (wantTime && wantFreq) {
        addPanel(time, 'Time', 6, 40, 0);
        addPanel(freq, 'Freq', 54, 40, 1);
      } else if (wantTime) {
        addPanel(time, 'Time', 6, 86, 0);
      } else if (wantFreq) {
        addPanel(freq, 'Freq', 6, 86, 0);
      }

      setOption({
        animation: true,
        color: colorPalette.colors,
        tooltip: {
          trigger: 'axis',
          axisPointer: { type: 'cross', snap: true },
          formatter: (params: CallbackDataParams | CallbackDataParams[]) => {
            const list = Array.isArray(params) ? params : [params];
            if (list.length === 0) return '';
            let res = list.slice(0, 10).map((p) => {
              const point = p.data as [number, number];
              return `${p.marker}${p.seriesName}: ${point[1].toFixed(5)}`;
            }).join('<br/>');
            if (list.length > 10) { res += '<br/>...'; }
            return res;
          },
        },
        grid, xAxis, yAxis, dataZoom, series,
        toolbox: {
          show: true,
          feature: {
            dataZoom: { title: { zoom: 'Zoom', back: 'Reset Zoom' } },
            restore: { title: 'Restore' },
            saveAsImage: { title: 'Download' },
          },
        },
      });

      worker!.removeEventListener('message', onMsg);
    };

    worker.addEventListener('message', onMsg);
    worker.postMessage({ items, wantTime, wantFreq, mode });
  }, [metaQuery.data, acqQuery.data, coil, wantTime, wantFreq, mode, colorPalette]);

  const showEmpty = !idsReady || (metaQuery.isError && !metaQuery.isLoading);

  return (
    <Stack sx={{ display: 'flex', flexDirection: 'column', flexGrow: 1, height: '100%', p: 1, gap: 1, overflow: 'hidden' }}>

      {/* Toolbar */}
      <Stack direction='row' alignItems='center' gap={0.5}>
        <Typography level='title-sm' sx={{ flexGrow: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
          {taskName ? `${taskName} Raw Data` : 'Raw Data'}
        </Typography>

        {/* Settings */}
        <IconButton
          ref={settingsAnchorRef}
          size='sm'
          variant='plain'
          color='neutral'
          title='Plot settings'
          onClick={() => setSettingsOpen(v => !v)}
        >
          <TuneIcon fontSize='small' />
        </IconButton>

        <Popper open={settingsOpen} anchorEl={settingsAnchorRef.current} placement='bottom-end' style={{ zIndex: 1300 }}>
          <Sheet
            ref={settingsPanelRef}
            variant='outlined'
            sx={{ p: 2, mt: 0.5, borderRadius: 'sm', boxShadow: 'md', display: 'flex', flexDirection: 'column', gap: 1.5, minWidth: 220 }}
          >
            <Box>
              <Typography level='body-xs' fontWeight='lg' sx={{ mb: 0.5 }}>Domain</Typography>
              <Stack direction='row' gap={2}>
                <Checkbox label='Time' size='sm' checked={wantTime} onChange={e => setWantTime(e.target.checked)} />
                <Checkbox label='Frequency' size='sm' checked={wantFreq} onChange={e => setWantFreq(e.target.checked)} />
              </Stack>
            </Box>

            <Box>
              <Typography level='body-xs' fontWeight='lg' sx={{ mb: 0.5 }}>Mode</Typography>
              <Select size='sm' value={mode} defaultValue='abs' onChange={(_, v) => setMode(v as ComplexMode)} required
                slotProps={{ listbox: { disablePortal: true } }}
              >
                <Option value='abs'>Magnitude</Option>
                <Option value='phase'>Phase</Option>
                <Option value='real'>Real</Option>
                <Option value='imag'>Imag</Option>
              </Select>
            </Box>

            <Box>
              <Typography level='body-xs' fontWeight='lg' sx={{ mb: 0.5 }}>Color Palette</Typography>
              <Select
                size='sm'
                value={colorPalette.id}
                defaultValue={plotColorPalettes.default.id}
                onChange={(_, v) => setColorPalette(plotColorPalettes[v ?? plotColorPalettes.default.id])}
                required
                slotProps={{ listbox: { disablePortal: true } }}
              >
                {plotColorPaletteOptions.map(p => <Option key={p.id} value={p.id}>{p.name}</Option>)}
              </Select>
            </Box>

            <Box>
              <Typography level='body-xs' fontWeight='lg' sx={{ mb: 0.5 }}>Coil</Typography>
              <Input
                size='sm'
                type='number'
                value={coil}
                slotProps={{ input: { min: 0, max: 999, step: 1 } }}
                onChange={e => setCoil(Math.max(0, Number(e.target.value)))}
              />
            </Box>

            <Box>
              <Typography level='body-xs' fontWeight='lg' sx={{ mb: 0.5 }}>Plot Mode</Typography>
              <Stack direction='row' alignItems='center' gap={1}>
                <Typography level='body-xs'>Single</Typography>
                <Switch size='sm' checked={overlay} onChange={e => setOverlay(e.target.checked)} />
                <Typography level='body-xs'>Overlay</Typography>
              </Stack>
            </Box>

            {overlay ? (
              <Box>
                <Typography level='body-xs' fontWeight='lg' sx={{ mb: 0.5 }}>Range</Typography>
                <Stack direction='row' gap={1}>
                  <Input
                    size='sm'
                    type='number'
                    value={acqRange[0]}
                    slotProps={{ input: { min: 0, max: maxIdx, step: 1 } }}
                    onChange={e => setAcqRange([Math.max(0, Number(e.target.value)), acqRange[1]])}
                  />
                  <Input
                    size='sm'
                    type='number'
                    value={acqRange[1]}
                    slotProps={{ input: { min: 0, max: maxIdx, step: 1 } }}
                    onChange={e => setAcqRange([acqRange[0], Math.min(maxIdx, Number(e.target.value))])}
                  />
                </Stack>
              </Box>
            ) : (
              <Box>
                <Typography level='body-xs' fontWeight='lg' sx={{ mb: 0.5 }}>Readout</Typography>
                <Input
                  size='sm'
                  type='number'
                  value={currentAcq}
                  slotProps={{ input: { min: 0, max: maxIdx, step: 1 } }}
                  onChange={e => setCurrentAcq(Math.max(0, Math.min(maxIdx, Number(e.target.value))))}
                />
              </Box>
            )}
          </Sheet>
        </Popper>

        {/* Download */}
        {onDownload && (
          <IconButton size='sm' variant='outlined' color='neutral' title='Download MRD' onClick={onDownload}>
            <FileDownloadIcon sx={{ fontSize: 'var(--IconFontSize)' }} />
          </IconButton>
        )}
      </Stack>

      <Card variant="outlined" color="neutral" sx={{ p: 0.5, flex: 1, minHeight: 0 }}>
        {showEmpty ? (
          <Container maxWidth={false} sx={{ width: '50%', mt: 5, justifyContent: 'center' }}>
            <AlertItem
              title="No MRD data available for the selected result."
              type={Alerts.Info}
            />
          </Container>
        ) : (
          <div
            ref={containerRef}
            style={{ height: '100%', minHeight: 200, minWidth: 300 }}
          >
            <ReactECharts
              echarts={echartsCore}
              option={option}
              notMerge
              lazyUpdate
              style={{ width: '100%', height: '100%' }}
              opts={{ renderer: 'canvas' }}
            />
          </div>
        )}
      </Card>
    </Stack>
  );
}
