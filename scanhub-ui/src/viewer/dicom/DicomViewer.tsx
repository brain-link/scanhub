// src/viewer/dicom/DicomViewerMinimal.tsx
import React from 'react';
import {
  RenderingEngine,
  getRenderingEngine,
  Enums,
  volumeLoader,
  type Types,
} from '@cornerstonejs/core';
import { initCornerstone } from './cornerstone/init';
import { useImageIds } from './hooks/useImageIds';
import { usePreferVolume } from './hooks/useVolumeIntent';
import LoginContext from '../../LoginContext';
import { getLinkedToolGroup, destroyLinkedToolGroup, attachViewportsToLinkedGroup } from './cornerstone/toolgroups';

import Card from '@mui/joy/Card'
import Stack from '@mui/joy/Stack'

const RENDERING_ENGINE_ID = 're-min';
const VIEWPORT_ID = 'vp-min';



/**
 * Minimal single-viewport DICOM viewer:
 * - Initializes Cornerstone3D once (uses your existing initCornerstone3D)
 * - Creates 1 viewport (STACK or ORTHOGRAPHIC for volume)
 * - Loads imageIds for the given task and displays them
 */
export default function DicomViewer3D({taskId}: {taskId: string | undefined}) {
  const [user] = React.useContext(LoginContext);
  const [ready, setReady] = React.useState(false);
  const [viewportReady, setViewportReady] = React.useState(false);
  const containerRef = React.useRef<HTMLDivElement | null>(null);
  const engineRef = React.useRef<RenderingEngine | null>(null);
  const { imageIds } = useImageIds(taskId);
  const preferVolume = usePreferVolume(imageIds);


  // Init Cornerstone once
  React.useEffect(() => {
    let cancelled = false;
    (async () => {
      await initCornerstone(() => user?.access_token);
      if (!cancelled) setReady(true);
    })();
    return () => {
      cancelled = true;
    };
  }, [user?.access_token]);


  // Create engine + viewport (STACK for small/1 frame; ORTHOGRAPHIC for many)
  React.useEffect(() => {
    if (!ready || !containerRef.current) return;

    // clean previous
    getRenderingEngine(RENDERING_ENGINE_ID)?.destroy();

    const engine = new RenderingEngine(RENDERING_ENGINE_ID);
    engineRef.current = engine;
  
    const viewportType = preferVolume ? Enums.ViewportType.ORTHOGRAPHIC : Enums.ViewportType.STACK;

    (async () => {
      await engine.enableElement({
        viewportId: VIEWPORT_ID,
        element: containerRef.current!,
        type: viewportType,
        defaultOptions: { background: [0, 0, 0] },
      });
      setViewportReady(true);
    })();

    return () => {
      setViewportReady(false);
      try { engine.destroy(); } catch {}
      engineRef.current = null;
    };
  }, [ready, imageIds.length]);


  // Attach tools only after the viewport exists
  React.useEffect(() => {
    if (!viewportReady) return;
    getLinkedToolGroup();
    attachViewportsToLinkedGroup(RENDERING_ENGINE_ID, [VIEWPORT_ID]);
    return () => destroyLinkedToolGroup();
  }, [viewportReady]);


  // Load data and render
  React.useEffect(() => {
    console.log("Trying to load the following imageIDs: ", imageIds)
    if (!viewportReady || !imageIds?.length) return;

    (async () => {
      const engine = engineRef.current;
      if (!engine) return;

      const vp = engine.getViewport(VIEWPORT_ID) as Types.IStackViewport | Types.IVolumeViewport;
      try {
        if ('setVolumes' in vp && preferVolume) {
          console.log("Using volume loader...")
          const volumeId = `cornerstoneStreamingImageVolume:${Date.now()}`;
          await volumeLoader.createAndCacheVolume(volumeId, { imageIds });
          await (vp as Types.IVolumeViewport).setVolumes([{ volumeId }]);
        } else {
          console.log("Using stack viewport... preferVolume: ", preferVolume)
          await (vp as Types.IStackViewport).setStack(imageIds);
        }
        await vp.render();
      } catch (e) {
        console.error('Viewport load failed; forcing stack path', e);
        try {
          await (vp as Types.IStackViewport).setStack(imageIds);
          await vp.render();
        } catch (e2) {
          console.error('Stack fallback failed', e2);
        }
      }
    })();
  }, [viewportReady, imageIds]);

  if (!imageIds?.length) {
    return <div style={{ padding: 12 }}>No DICOM instances provided.</div>;
  }

  return (
    <Stack sx={{ display: 'flex', flexDirection: 'column', flexGrow: 1, width: '100%', height: 'calc(100vh - var(--Navigation-height))', p: 1 }}>
      <Card variant="plain" color="neutral" sx={{ p: 0.5, bgcolor: '#000', height: '100%', border: '5px solid' }}>
        <div 
          ref={containerRef}
          id="dicomViewport"
          onContextMenu={(e) => {
            e.preventDefault();
            e.stopPropagation(); // optional, keeps it from bubbling into the page
          }}
          style={{ 
            width: '100%',
            height: '100%',
            background: 'black',
            borderRadius: 8,
            overscrollBehavior: 'contain',
            userSelect: 'none',
            WebkitUserSelect: 'none',
            WebkitTouchCallout: 'none',
          }} />
      </Card>
    </Stack>
  );
}