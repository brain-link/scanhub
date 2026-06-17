import React, { useEffect, useMemo, useRef, useState } from 'react';
import ReactECharts from 'echarts-for-react';

import { useData } from './hooks/useData';
import { useMeta } from './hooks/useMeta';
import { ColorPalette, ComplexMode } from './types';
import type { CallbackDataParams } from 'echarts/types/dist/shared';
import Controls from './Controls';
import { plotColorPalettes } from './utils/colormaps';
import { WorkerMessage } from './utils/interfaces';
import Container from '@mui/joy/Container';
import AlertItem from '../../components/AlertItem';
import { Alerts } from '../../interfaces/components.interface';
import Card from '@mui/joy/Card';
import Stack from '@mui/joy/Stack';
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
}

export default function RawDataViewer({ selectedResultId, protocolId, taskId }: RawDataViewerProps) {
  const [overlay, setOverlay] = useState(true);
  const [wantTime, setWantTime] = useState(true);
  const [wantFreq, setWantFreq] = useState(false);
  const [mode, setMode] = useState<ComplexMode>('abs');
  const [colorPalette, setColorPalette] = useState<ColorPalette>(plotColorPalettes.default);
  const [coil, setCoil] = useState(0);
  const [acqRange, setAcqRange] = useState<[number, number]>([0, 0]);
  const [currentAcq, setCurrentAcq] = useState(0);

  const containerRef = useRef<HTMLDivElement | null>(null);

  const idsReady = !!protocolId && !!taskId && !!selectedResultId;

  // Meta query
  const metaQuery = useMeta(idsReady, protocolId, taskId, selectedResultId);

  // Initialize range when meta changes
  useEffect(() => {
    if (!metaQuery.data) return;
    const n = metaQuery.data.acquisitions?.length ?? 1;
    setAcqRange([0, Math.min(10, n - 1)]);
    setCurrentAcq(0);
    setCoil(0);
  }, [metaQuery.data]);

  // ids expression
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

  // Binary acquisitions query
  const acqQuery = useData(
    idsReady && !!idsExpr,
    protocolId,
    taskId,
    selectedResultId,
    idsExpr,
    0,
    1
  );

  // Worker lifecycle
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
      <Controls
        metaCount={metaQuery.data?.acquisitions?.length ?? 0}
        overlay={overlay}
        setOverlay={setOverlay}
        wantTime={wantTime}
        setWantTime={setWantTime}
        wantFreq={wantFreq}
        setWantFreq={setWantFreq}
        mode={mode}
        setMode={setMode}
        colorPalette={colorPalette}
        setColorPalette={setColorPalette}
        coil={coil}
        setCoil={setCoil}
        acqRange={acqRange}
        setAcqRange={setAcqRange}
        currentAcq={currentAcq}
        setCurrentAcq={setCurrentAcq}
      />
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
