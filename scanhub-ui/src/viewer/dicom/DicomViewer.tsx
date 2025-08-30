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
import { useNumberOfFrames } from './hooks/useNumberOfFrames';
import LoginContext from '../../LoginContext';
import { getLinkedToolGroup, destroyLinkedToolGroup, attachViewportsToLinkedGroup } from './cornerstone/toolgroups';
import DiconViewerToolbar from './DicomViewerToolbar';

import Card from '@mui/joy/Card';
import Stack from '@mui/joy/Stack';
import Container from '@mui/joy/Container';
import AlertItem from '../../components/AlertItem';
import { Alerts } from '../../interfaces/components.interface'


const RENDERING_ENGINE_ID = 're-min';
const VIEWPORT_ID = 'vp-min';

/**
 * Minimal single-viewport DICOM viewer:
 * - Initializes Cornerstone3D once (uses your existing initCornerstone3D)
 * - Creates 1 viewport (STACK or ORTHOGRAPHIC for volume)
 * - Loads imageIds for the given task and displays them
 */
export default function DicomViewer3D({imageIds}: {imageIds: string[]}) {
  const [user] = React.useContext(LoginContext);
  const [ready, setReady] = React.useState(false);
  const [viewportReady, setViewportReady] = React.useState(false);
  const containerRef = React.useRef<HTMLDivElement | null>(null);
  const engineRef = React.useRef<RenderingEngine | null>(null);
  
  const numberOfFrames = useNumberOfFrames(imageIds, ready);


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
  
    const viewportType = numberOfFrames > 1 ? Enums.ViewportType.ORTHOGRAPHIC : Enums.ViewportType.STACK;

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
      try {
        engine.destroy();
      } catch (err) {
        // Intentionally ignore: engine may already be destroyed
        // console.debug('engine.destroy failed', err);
      } finally {
        engineRef.current = null;
      }
    };
  }, [ready, numberOfFrames]);


  // Attach tools only after the viewport exists
  React.useEffect(() => {
    if (!viewportReady) return;
    getLinkedToolGroup();
    attachViewportsToLinkedGroup(RENDERING_ENGINE_ID, [VIEWPORT_ID]);
    return () => destroyLinkedToolGroup();
  }, [viewportReady]);


  // Load data and render
  React.useEffect(() => {
    console.log('Trying to load the following imageIDs: ', imageIds)
    if (!viewportReady || !numberOfFrames) return;

    (async () => {
      const engine = engineRef.current;
      if (!engine) return;  

      // Get viewport
      const vp = engine.getViewport(VIEWPORT_ID) as Types.IStackViewport | Types.IVolumeViewport;

      try {
        if ('setVolumes' in vp && numberOfFrames > 1) {
          console.log('Using volume loader...')

          // Create volume image ids -> add ?frame=1...N
          const volumeId = `cornerstoneStreamingImageVolume:${Date.now()}`;
          const volumeImageIds = Array.from({ length: numberOfFrames }, (_, i) => `${imageIds[0]}?frame=${i + 1}`);
          // Create and cache volume image ids for volume id
          const volume = await volumeLoader.createAndCacheVolume(volumeId, { imageIds: volumeImageIds });
          // Load volume
          await volume.load();
          // Set volume in viewport
          await (vp as Types.IVolumeViewport).setVolumes([{ volumeId }]);

        } else {
          console.log('Using stack viewport...')
          // If 2D 
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


  if (imageIds.length == 0 || !numberOfFrames) {
    return (
      <Container maxWidth={false} sx={{ width: '50%', mt: 5, justifyContent: 'center' }}>
        <AlertItem title='Please select a reconstruction or processing task with a result to show a DICOM image.' type={Alerts.Info} />
      </Container>
    )
  }

  return (
    <Stack sx={{ display: 'flex', flexDirection: 'column', flexGrow: 1, width: '100%', height: 'calc(100vh - var(--Navigation-height))', p: 1, gap: 1}}>
      < DiconViewerToolbar />
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