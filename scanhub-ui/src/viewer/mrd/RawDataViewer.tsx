import React, { useEffect, useMemo, useRef, useState } from 'react';
import ReactECharts from 'echarts-for-react';

import { useData } from './hooks/useData';
import { useMeta } from './hooks/useMeta';
import { useFileIds } from './hooks/useFileIds';
import { ColormapName, ComplexMode } from './types';
import type { CallbackDataParams } from 'echarts/types/dist/shared';
import Controls from './Controls';
import { colorCycle } from './utils/colormaps';
import { WorkerMessage } from './utils/interfaces';
import Container from '@mui/joy/Container';
import AlertItem from '../../components/AlertItem';
import { Alerts } from '../../interfaces/components.interface';
import Card from '@mui/joy/Card';
import Stack from '@mui/joy/Stack';

import type { EChartsOption } from 'echarts';

// ---- ECharts (no barrel import) ----
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
import { MRDAcquisitionInfo } from '../../openapi/generated-client/exam';
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
const echarts = { init, use: echartsUse };

export default function RawDataViewer({ taskId }: { taskId: string | undefined }) {
  // ---------------- UI state (always same order) ----------------
  const [overlay, setOverlay] = useState(true);
  const [wantTime, setWantTime] = useState(true);
  const [wantFreq, setWantFreq] = useState(false);
  const [mode, setMode] = useState<ComplexMode>('abs');
  const [colormap, setColormap] = useState<ColormapName>('viridis');
  const [coil, setCoil] = useState(0);
  const [acqRange, setAcqRange] = useState<[number, number]>([0, 0]);
  const [currentAcq, setCurrentAcq] = useState(0);

  const containerRef = useRef<HTMLDivElement | null>(null);

  // ---------------- Data-layer hooks (never early-return) ----------------
  const {
    fileIds,
    isLoading: idsLoading,
    isError: idsError,
  } = useFileIds(taskId);

  // Derive IDs (safe defaults) and readiness
  const workflowId = fileIds?.workflowId ?? '';
  const resolvedTaskId = fileIds?.taskId ?? '';
  const resultId = fileIds?.resultId ?? '';
  const idsReady = !!fileIds && !idsError;

  // Meta query — MUST be called every render; gate with `enabled`
  const metaQuery = useMeta(idsReady, workflowId, resolvedTaskId, resultId);

  // Initialize range when meta changes (effect is fine; it's not a Hook order concern)
  useEffect(() => {
    const meta = metaQuery.data;
    if (!meta) return;
    const n = meta.acquisitions?.length ? meta.acquisitions.length : 1;
    setAcqRange([0, Math.min(10, n - 1)]);
    setCurrentAcq(0);
    setCoil(0);
  }, [metaQuery.data]);

  // ids expression (safe when meta not ready)
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

  // Binary acquisitions query — ALWAYS call, but disabled until ready
  const acqQuery = useData(
    idsReady && !!idsExpr,
    workflowId,
    resolvedTaskId,
    resultId,
    idsExpr,
    0,
    1
  );

  // ---------------- Worker lifecycle (always mounted) ----------------
  const workerRef = useRef<Worker | null>(null);
  useEffect(() => {
    workerRef.current = new Worker(new URL('./workers/signalWorker.ts', import.meta.url), { type: 'module' });
    return () => workerRef.current?.terminate();
  }, []);

  // ---------------- Chart option state ----------------
  const [option, setOption] = useState<EChartsOption>({});

  useEffect(() => {
    const meta = metaQuery.data;
    const batch = acqQuery.data;
    const worker = workerRef.current;
    if (!meta || !batch || !worker) return;

    // dwell_time (sec) -> sampleRateHz per acquisition
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

      const colors = colorCycle(colormap, Math.max(time.length, freq.length));
      const series: SeriesOption[] = [];
      const xAxis: XAXisComponentOption[] = [];
      const yAxis: YAXisComponentOption[] = [];
      const grid: GridComponentOption[] = [];
      const dataZoom: DataZoomComponentOption[] = [];

      const yLabel = (domain: 'time' | 'freq') =>
        mode === 'abs'
          ? domain === 'time'
            ? '|s(t)|'
            : '|S(f)|'
          : mode === 'phase'
          ? 'Phase (rad)'
          : mode === 'real'
          ? domain === 'time'
            ? 'Re{s(t)}'
            : 'Re{S(f)}'
          : domain === 'time'
          ? 'Im{s(t)}'
          : 'Im{S(f)}';

      const addPanel = (
        traces: { label: string; x: Float32Array; y: Float32Array }[],
        title: 'Time' | 'Freq',
        topPct: number,
        heightPct: number,
        gridIdx: number
      ) => {

        grid.push({
          top: `${topPct}%`,
          height: `${heightPct}%`,
          left: 60,
          right: 20
        });

        xAxis.push({
          type: 'value',
          gridIndex: gridIdx,
          name: title === 'Time' ? 'Time (s)' : 'Frequency (Hz)',
          nameLocation: 'middle',
        });

        yAxis.push({
          type: 'value',
          gridIndex: gridIdx,
          name: yLabel(title === 'Time' ? 'time' : 'freq'),
          nameLocation: 'middle',
        });

        traces.forEach((t, idx) => {
          const len = t.x.length;
          const pts = new Array(len);
          for (let i = 0; i < len; i++) pts[i] = [t.x[i], t.y[i]];
          series.push({
            type: 'line',
            name: t.label,
            xAxisIndex: gridIdx,
            yAxisIndex: gridIdx,
            showSymbol: false,
            large: true,
            sampling: 'lttb',
            lineStyle: { width: 1.5, color: colors[idx % colors.length] },
            data: pts,
          });
        });

        dataZoom.push(
          {
            type: 'inside',
            xAxisIndex: gridIdx,
            filterMode: 'none',   // independent zoom
          },
        );
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
        tooltip: {
          trigger: 'axis',
          axisPointer: { type: 'cross', snap: true },
          formatter: (params: CallbackDataParams | CallbackDataParams[]) => {
            const list = Array.isArray(params) ? params : [params];
            if (list.length === 0) return '';
            // First line: x value
            let res = '';
            // Cut off at 10 series, each line is marker + series name + value (like default)
            res += list.slice(0, 10).map((p) => {
              // p.data can be unknown, so cast to [number, number] if that’s your shape
              const point = p.data as [number, number];
              return `${p.marker}${p.seriesName}: ${point[1].toFixed(5)}`;
            }).join('<br/>');
            // Optional: indicate more values
            if (list.length > 10) { res += '<br/>...'; }
            return res;
          },
        },
        // legend: { show: legendShow },
        grid,
        xAxis,
        yAxis,
        dataZoom,
        series,
        toolbox: {
          show: true,
          feature: {
            dataZoom: {
              yAxisIndex: 'none',   // zoom only in x by default
              title: {
                zoom: 'Zoom',
                back: 'Reset Zoom'
              }
            },
            restore: { title: 'Restore' },
            saveAsImage: { title: 'Download' },
          },
        },
      });

      worker!.removeEventListener('message', onMsg);
    };

    worker.addEventListener('message', onMsg);
    worker.postMessage({
      items,
      wantTime,
      wantFreq,
      mode,
    });
  }, [
    metaQuery.data,
    acqQuery.data,
    coil,
    wantTime,
    wantFreq,
    mode,
    colormap,
  ]);

  // ---------------- Render (no early returns) ----------------
  const showEmpty =
    (idsError || !fileIds) &&
    !(idsLoading); // avoid flashing the empty while still loading

  return (

    <Stack sx={{ display: 'flex', flexDirection: 'column', flexGrow: 1, width: '100%', height: 'calc(100vh - var(--Navigation-height)) - 4', p: 2, gap: 1}}>
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
        colormap={colormap}
        setColormap={setColormap}
        coil={coil}
        setCoil={setCoil}
        acqRange={acqRange}
        setAcqRange={setAcqRange}
        currentAcq={currentAcq}
        setCurrentAcq={setCurrentAcq}
      />
      <Card variant="outlined" color="neutral" sx={{ p: 0.5, height: '100%' }}>

          {
            showEmpty ? (
              <Container maxWidth={false} sx={{ width: '50%', mt: 5, justifyContent: 'center' }}>
                <AlertItem
                  title="Please select a reconstruction or processing task with a result to show a DICOM image."
                  type={Alerts.Info}
                />
              </Container>
            ) : (
              <div
                ref={containerRef}
                style={{
                  height: '100%',
                  minHeight: 320,   // avoid 0 height on first paint
                  minWidth: 400,
                }}
              >
                <ReactECharts
                  echarts={echarts}
                  option={option}
                  notMerge
                  lazyUpdate
                  style={{ width: '100%', height: '100%' }}
                  opts={{ renderer: 'canvas' }}
                />
              </div>
            )
          }
      </Card>
    </Stack>
  );
}
