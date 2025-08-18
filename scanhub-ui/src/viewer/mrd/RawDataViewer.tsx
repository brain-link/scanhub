import React, { useEffect, useMemo, useRef, useState } from 'react';
import ReactECharts from 'echarts-for-react';

import { useData } from './hooks/useData';
import { useMeta } from './hooks/useMeta';
import { useFileIds } from './hooks/useFileIds';
import { ColormapName, ComplexMode } from './types';
import Controls from './Controls';
import { colorCycle } from './utils/colormaps';
import Container from '@mui/joy/Container';
import AlertItem from '../../components/AlertItem';
import { Alerts } from '../../interfaces/components.interface';
import Card from '@mui/joy/Card';
import Stack from '@mui/joy/Stack';

// ---- ECharts (no barrel import) ----
import { init, use as echartsUse } from 'echarts/core';
import { LineChart } from 'echarts/charts';
import {
  GridComponent,
  LegendComponent,
  TooltipComponent,
  DataZoomComponent,
} from 'echarts/components';
import { CanvasRenderer } from 'echarts/renderers';
echartsUse([LineChart, GridComponent, LegendComponent, TooltipComponent, DataZoomComponent, CanvasRenderer]);
const echarts = { init, use: echartsUse };

export default function RawDataViewer({ taskId }: { taskId: string | undefined }) {
  // ---------------- UI state (always same order) ----------------
  const [overlay, setOverlay] = useState(true);
  const [wantTime, setWantTime] = useState(true);
  const [wantFreq, setWantFreq] = useState(false);
  const [mode, setMode] = useState<ComplexMode>('abs');
  const [zeroPadPow2, setZeroPadPow2] = useState(true);
  const [colormap, setColormap] = useState<ColormapName>('viridis');
  const [serverStride, setServerStride] = useState(1);
  const [clientDownsample, setClientDownsample] = useState(4000);
  const [coil, setCoil] = useState(0);
  const [acqRange, setAcqRange] = useState<[number, number]>([0, 0]);
  const [currentAcq, setCurrentAcq] = useState(0);

  const containerRef = useRef<HTMLDivElement | null>(null);

  // ---------------- Data-layer hooks (never early-return) ----------------
  const {
    fileIds,
    isLoading: idsLoading,
    isError: idsError,
    error: idsErrorObj,
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
    setAcqRange([0, Math.max(0, n - 1)]);
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
    serverStride
  );

  // ---------------- Worker lifecycle (always mounted) ----------------
  const workerRef = useRef<Worker | null>(null);
  useEffect(() => {
    workerRef.current = new Worker(new URL('./workers/signalWorker.ts', import.meta.url), { type: 'module' });
    return () => workerRef.current?.terminate();
  }, []);

  // ---------------- Chart option state ----------------
  const [option, setOption] = useState<any>({});

  useEffect(() => {
    const meta = metaQuery.data;
    const batch = acqQuery.data;
    console.log("META", meta)
    console.log("BATCH", batch)
    const worker = workerRef.current;
    if (!meta || !batch || !worker) return;

    // dwell_time (sec) -> sampleRateHz per acquisition
    const dwellById = new Map<number, number>();
    meta.acquisitions?.forEach((a: any) => dwellById.set(a.acquisition_id, a.dwell_time));

    const items = batch.map((acq: any) => {
      const dwell = dwellById.get(acq.acqId)!;
      const fs = 1 / dwell;
      return {
        acqId: acq.acqId,
        nCoils: acq.nCoils,
        nSamples: acq.nSamples,
        data: acq.data,
        coil,
        label: `Acq ${acq.acqId} • Coil ${coil}`,
        sampleRateHz: fs,
      };
    });

    const onMsg = (ev: MessageEvent<any>) => {
      const { time, freq } = ev.data as {
        time: { label: string; x: Float32Array; y: Float32Array }[];
        freq: { label: string; x: Float32Array; y: Float32Array }[];
      };

      const colors = colorCycle(colormap, Math.max(time.length, freq.length));
      const series: any[] = [];
      const xAxis: any[] = [];
      const yAxis: any[] = [];
      const grid: any[] = [];
      const dataZoom: any[] = [];

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
        grid.push({ top: `${topPct}%`, height: `${heightPct}%`, left: 60, right: 20 });
        xAxis.push({
          type: 'value',
          gridIndex: gridIdx,
          name: title === 'Time' ? 'Time (s)' : 'Frequency (Hz)',
        });
        yAxis.push({ type: 'value', gridIndex: gridIdx, name: yLabel(title === 'Time' ? 'time' : 'freq') });

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
          { type: 'inside', xAxisIndex: gridIdx },
          { type: 'slider', xAxisIndex: gridIdx, height: 18, bottom: 0 }
        );
      };

      if (wantTime && wantFreq) {
        addPanel(time, 'Time', 6, 40, 0);
        addPanel(freq, 'Freq', 56, 40, 1);
      } else if (wantTime) {
        addPanel(time, 'Time', 6, 86, 0);
      } else if (wantFreq) {
        addPanel(freq, 'Freq', 6, 86, 0);
      }

      const legendShow = (wantTime && time.length > 1) || (wantFreq && freq.length > 1);

      setOption({
        animation: false,
        tooltip: { trigger: 'axis', axisPointer: { type: 'cross' } },
        legend: { show: legendShow },
        grid,
        xAxis,
        yAxis,
        dataZoom,
        series,
      });

      worker!.removeEventListener('message', onMsg);
    };

    worker.addEventListener('message', onMsg);
    worker.postMessage({
      items,
      wantTime,
      wantFreq,
      mode,
      zeroPadPow2,
      downsampleTarget: clientDownsample,
    });
  }, [
    metaQuery.data,
    acqQuery.data,
    coil,
    wantTime,
    wantFreq,
    mode,
    zeroPadPow2,
    clientDownsample,
    colormap,
  ]);

  // ---------------- Render (no early returns) ----------------
  const showEmpty =
    (idsError || !fileIds) &&
    !(idsLoading); // avoid flashing the empty while still loading

  return (

    <Stack sx={{ display: 'flex', flexDirection: 'column', flexGrow: 1, width: '100%', height: 'calc(100vh - var(--Navigation-height))', p: 1, gap: 1}}>
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
        zeroPadPow2={zeroPadPow2}
        setZeroPadPow2={setZeroPadPow2}
        colormap={colormap}
        setColormap={setColormap}
        serverStride={serverStride}
        setServerStride={setServerStride}
        clientDownsample={clientDownsample}
        setClientDownsample={setClientDownsample}
        coil={coil}
        setCoil={setCoil}
        acqRange={acqRange}
        setAcqRange={setAcqRange}
        currentAcq={currentAcq}
        setCurrentAcq={setCurrentAcq}
      />
      <Card variant="plain" color="neutral" sx={{ p: 0.5, height: '100%', border: '5px solid' }}>
        <div style={{ position: 'relative' }}>
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
        </div>
      </Card>
    </Stack>
  );
}
