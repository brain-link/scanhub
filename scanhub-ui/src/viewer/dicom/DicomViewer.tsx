// src/viewer/dicom/DicomViewer.tsx
import React from 'react';
import {
  getRenderingEngine,
  Enums,
  volumeLoader,
  cache as csCache,
  type Types,
} from '@cornerstonejs/core';
import { useNumberOfFrames } from './hooks/useNumberOfFrames';
import LoginContext from '../../LoginContext';
import { attachToolGroupsForLayout, destroyToolGroups } from './cornerstone/toolgroups';
import DiconViewerToolbar from './DicomViewerToolbar';
import { VIEW_LAYOUTS, VIEW_LAYOUT_META, ViewportId, ViewLayout } from './cornerstone/viewLayouts';
import { SliceGridViewer } from './SliceGridViewer';
import { useViewportResize } from './hooks/useViewportResize';
import { getOrCreateEngine, RENDERING_ENGINE_ID } from './cornerstone/engine';

import Card from '@mui/joy/Card';
import Stack from '@mui/joy/Stack';
import Container from '@mui/joy/Container';
import AlertItem from '../../components/AlertItem';
import { ItemSelection } from '../../interfaces/components.interface';
import { Alerts } from '../../interfaces/components.interface';
import { useImageIds } from '../../hooks/useImageIds';


function makeVolumeId(imageIds: string[]) {
  return `cornerstoneStreamingImageVolume:${btoa(imageIds[0]).slice(0, 16)}`;
}

function safeEvictVolume(volumeId: string | null) {
  if (!volumeId) return;
  try { csCache.removeVolumeLoadObject(volumeId); } catch { /* not cached or already evicted */ }
}


interface DicomViewer3DProps {
  item: ItemSelection;
  selectedResultId?: string;
  onDownloadDicom?: () => void;
  onExportToXnat?: () => void;
}


export default function DicomViewer3D({ item, selectedResultId, onDownloadDicom, onExportToXnat }: DicomViewer3DProps) {

  const { imageIds } = useImageIds(item, selectedResultId);

  const containerRef = React.useRef<HTMLDivElement | null>(null);
  const engineViewportIdsRef = React.useRef<ViewportId[]>([]);
  const volumeIdRef = React.useRef<string | null>(null);

  const [user] = React.useContext(LoginContext);
  const [ready, setReady] = React.useState(false);
  const [viewportReady, setViewportReady] = React.useState(false);
  const [layout, setLayout] = React.useState<ViewLayout>(ViewLayout.Single);

  // engineRef always points to the global singleton — never created or destroyed here.
  const engineRef = React.useRef(getRenderingEngine(RENDERING_ENGINE_ID) ?? null);

  const numberOfFrames = useNumberOfFrames(imageIds, ready);
  useViewportResize(engineRef, layout, containerRef);


  // Ensure Cornerstone is initialised and the global engine exists.
  // We do NOT destroy the engine on unmount — only viewport elements are released.
  React.useEffect(() => {
    setReady(false);
    setViewportReady(false);

    let cancelled = false;

    getOrCreateEngine(() => user?.access_token).then((engine) => {
      if (cancelled) return;
      engineRef.current = engine;
      setReady(true);
    });

    return () => {
      cancelled = true;
      // Disable viewports so their DOM elements can be safely unmounted.
      const engine = engineRef.current;
      if (engine) {
        for (const vpId of engineViewportIdsRef.current) {
          try { engine.disableElement(vpId); } catch { /* ignore */ }
        }
      }
      engineViewportIdsRef.current = [];
      safeEvictVolume(volumeIdRef.current);
      volumeIdRef.current = null;
      setReady(false);
      setViewportReady(false);
      destroyToolGroups();
    };
  }, [user?.access_token]); // eslint-disable-line react-hooks/exhaustive-deps


  // Enable / reconfigure viewports for the current layout.
  React.useEffect(() => {
    if (!ready || !containerRef.current || !engineRef.current) return;

    setViewportReady(false);

    let cancelled = false;
    const engine = engineRef.current;
    const layoutViewportIds = VIEW_LAYOUTS[layout].map(v => v.id);

    // Disable viewport elements that are no longer in this layout.
    for (const id of engineViewportIdsRef.current) {
      if (!layoutViewportIds.includes(id)) {
        try { engine.disableElement(id); } catch { /* already gone */ }
      }
    }

    (async () => {
      for (const view of VIEW_LAYOUTS[layout]) {
        if (cancelled || !engineRef.current) return;

        const element = containerRef.current!.querySelector(
          `#viewport-${view.id}`
        ) as HTMLDivElement | null;
        if (!element) return;

        const activeVpIds = engine.getViewports().map(vp => vp.id);
        const type =
          numberOfFrames <= 1
            ? Enums.ViewportType.STACK
            : view.is3D
              ? Enums.ViewportType.VOLUME_3D
              : Enums.ViewportType.ORTHOGRAPHIC;

        if (!activeVpIds.includes(view.id)) {
          await engine.enableElement({
            viewportId: view.id,
            element,
            type,
            defaultOptions: { background: [0, 0, 0] },
          });
        } else {
          const vp = engine.getViewport(view.id);
          if ((vp as any).element !== element || vp.type !== type) {
            engine.disableElement(view.id);
            if (cancelled) return;
            await engine.enableElement({
              viewportId: view.id,
              element,
              type,
              defaultOptions: { background: [0, 0, 0] },
            });
          }
        }
      }

      if (cancelled || !engineRef.current) return;

      requestAnimationFrame(() => {
        if (cancelled || !engineRef.current) return;
        engineRef.current.resize(false, true);
        engineRef.current.getViewports().forEach(vp => vp?.resetCamera?.());
        engineRef.current.render();
      });

      engineViewportIdsRef.current = layoutViewportIds;
      setViewportReady(true);
    })();

    return () => { cancelled = true; };

  }, [ready, layout, numberOfFrames]);


  // Load and display volume / stack.
  React.useEffect(() => {
    if (!viewportReady || imageIds.length === 0 || !engineRef.current) return;
    if (layout === ViewLayout.AllSlices) return; // handled entirely by SliceGridViewer

    let cancelled = false;

    (async () => {
      const engine = engineRef.current!;

      if (layout === ViewLayout.Single && numberOfFrames <= 1) {
        const vp = engine.getViewport('single');
        if (!vp || vp.type !== Enums.ViewportType.STACK) return;
        await (vp as Types.IStackViewport).setStack(imageIds);
        if (!cancelled) await vp.render();
        return;
      }

      const volumeId = makeVolumeId(imageIds);
      const volumeImageIds = Array.from(
        { length: numberOfFrames },
        (_, i) => `${imageIds[0]}?frame=${i + 1}`
      );

      if (volumeIdRef.current !== volumeId) {
        safeEvictVolume(volumeIdRef.current);
        const vol = await volumeLoader.createAndCacheVolume(volumeId, { imageIds: volumeImageIds });
        if (cancelled) return;
        await vol.load();
        volumeIdRef.current = volumeId;
      }

      if (cancelled || !engineRef.current) return;

      for (const view of VIEW_LAYOUTS[layout]) {
        if (cancelled) return;
        const vp = engine.getViewport(view.id) as Types.IVolumeViewport;
        if (!vp) continue;
        await vp.setVolumes([{ volumeId }]);
        if (view.orientation) vp.setOrientation(view.orientation);
        await vp.resetCamera();
        if (!cancelled) await vp.render();
      }

      if (!cancelled) await attachToolGroupsForLayout(VIEW_LAYOUTS[layout], RENDERING_ENGINE_ID);

    })();

    return () => { cancelled = true; };

  }, [viewportReady, layout, imageIds, numberOfFrames]);


  const { rows, cols } = VIEW_LAYOUT_META[layout];
  const gridTemplate = `repeat(${rows}, 1fr) / repeat(${cols}, 1fr)`;

  if (imageIds.length === 0 || !numberOfFrames) {
    return (
      <Container maxWidth={false} sx={{ width: '50%', mt: 5, justifyContent: 'center' }}>
        <AlertItem
          title="Please select a DICOM result to show an image."
          type={Alerts.Info}
        />
      </Container>
    );
  }

  return (
    <Stack
      sx={{
        display: 'flex',
        flexDirection: 'column',
        flexGrow: 1,
        width: '100%',
        height: '100%',
        p: 1,
        gap: 1,
        overflow: 'hidden',
      }}
    >
      <DiconViewerToolbar
        onLayoutChange={setLayout}
        currentLayout={layout}
        onDownloadDicom={onDownloadDicom}
        onExportToXnat={onExportToXnat}
      />

      <Card
        variant="plain"
        color="neutral"
        sx={{ p: 0.5, bgcolor: '#000', flex: 1, minHeight: 0, border: '5px solid', overflow: 'hidden' }}
      >
        {layout === ViewLayout.AllSlices ? (
          <SliceGridViewer
            imageIds={imageIds}
            numberOfFrames={numberOfFrames}
            engineRef={engineRef}
          />
        ) : (
          <div
            ref={containerRef}
            style={{ display: 'grid', gridTemplate, width: '100%', height: '100%' }}
          >
            {VIEW_LAYOUTS[layout].map((v) => (
              <div
                key={v.id}
                id={`viewport-${v.id}`}
                style={{
                  width: '100%',
                  height: '100%',
                  background: 'black',
                  borderRadius: 5,
                  overflow: 'hidden',
                }}
              />
            ))}
          </div>
        )}
      </Card>
    </Stack>
  );
}
