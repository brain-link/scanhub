import React from 'react';
import {
  RenderingEngine,
  getRenderingEngine,
  Enums,
  volumeLoader
} from '@cornerstonejs/core';
import { initCornerstone3D } from './cornerstone/init';
import { useImageIds } from './hooks/useImageIds';
import { useViewportGrid, Layout } from './hooks/useViewportGrid';
import { usePreferVolume } from './hooks/useVolumeIntent';
import { getLinkedToolGroup, destroyLinkedToolGroup, attachViewportsToLinkedGroup } from './cornerstone/toolgroups';
import LoginContext from '../../LoginContext';



const renderingEngineId = 're-1';

export default function DicomViewer3D({taskId}: {taskId: string | undefined}) {
  const [user] = React.useContext(LoginContext);
  const [ready, setReady] = React.useState(false);
  const [layout, setLayout] = React.useState<Layout>('1x1');
  const [viewportIds, setViewportIds] = React.useState<string[]>([]);
  const containerRef = React.useRef<HTMLDivElement>(null);
  const { imageIds } = useImageIds(taskId);
  const grid = useViewportGrid(layout);
  const preferVolume = usePreferVolume(imageIds);

  React.useEffect(() => { 
    initCornerstone3D(() => user?.access_token).then(() => setReady(true));
  }, []);

  // create viewports on layout/mode change
  React.useEffect(() => {
    if (!ready || !containerRef.current) return;

    const previous = getRenderingEngine(renderingEngineId);
    if (previous) previous.destroy();

    const re = new RenderingEngine(renderingEngineId);
    const cells = Array.from(containerRef.current.querySelectorAll('[data-cell]')) as HTMLDivElement[];
    const ids: string[] = [];

    cells.forEach((el, i) => {
      const viewportId = `vp-${i + 1}`;
      ids.push(viewportId);
      re.enableElement({
        viewportId,
        element: el,
        type: preferVolume ? Enums.ViewportType.ORTHOGRAPHIC : Enums.ViewportType.STACK,
      });
    });

    setViewportIds(ids);
    return () => { re.destroy(); };
  }, [ready, layout, preferVolume]);


  // create/bind tool group when viewports exist
  React.useEffect(() => {
    if (!ready || viewportIds.length === 0) return;

    // ensure group exists and attach current viewports
    getLinkedToolGroup();
    attachViewportsToLinkedGroup(renderingEngineId, viewportIds);

    // clean up on unmount (or when we fully tear down viewports)
    return () => {
      destroyLinkedToolGroup();
    };
  }, [ready, viewportIds]);


  // optional: orient orthographic cameras (A/S/C) if we have ≥3 ortho viewports
  function setOrthoOrientation(vp: any, kind: 'axial'|'sagittal'|'coronal') {
    const preset = {
      axial:    { viewPlaneNormal: [0, 0, 1], viewUp: [0, -1, 0] },
      sagittal: { viewPlaneNormal: [1, 0, 0], viewUp: [0, 0, 1] },
      coronal:  { viewPlaneNormal: [0, 1, 0], viewUp: [0, 0, 1] },
    }[kind];
    vp.setCamera(preset);
  }

  // load & render (try volume; fallback to stack)
  React.useEffect(() => {
    if (!ready || viewportIds.length === 0 || imageIds.length === 0) return;

    (async () => {
      const re = getRenderingEngine(renderingEngineId);
      if (!re) return;

      const tryVolume = async () => {
        const volumeId = `cornerstoneStreamingImageVolume:${Date.now()}`;
        await volumeLoader.createAndCacheVolume(volumeId, { imageIds });

        viewportIds.forEach((vpId) => {
          const vp: any = re.getViewport(vpId);
          if (vp.type === Enums.ViewportType.ORTHOGRAPHIC) vp.setVolumes([{ volumeId }]);
          else vp.setStack(imageIds);
        });

        const orthoIds = viewportIds.filter(vpId => (re.getViewport(vpId) as any).type === Enums.ViewportType.ORTHOGRAPHIC);
        if (orthoIds.length >= 3) {
          setOrthoOrientation(re.getViewport(orthoIds[0]) as any, 'axial');
          setOrthoOrientation(re.getViewport(orthoIds[1]) as any, 'sagittal');
          setOrthoOrientation(re.getViewport(orthoIds[2]) as any, 'coronal');
        }

        re.render();
      };

      const tryStack = async () => {
        viewportIds.forEach((vpId) => {
          const vp: any = re.getViewport(vpId);
          vp.setStack(imageIds);
        });
        re.render();
      };

      try {
        if (preferVolume) await tryVolume();
        else await tryStack();
      } catch (e) {
        console.warn('Volume load failed; falling back to stack.', e);
        await tryStack();
      }
    })();
  }, [ready, viewportIds, imageIds, preferVolume]);

  if (!imageIds || imageIds.length === 0) {
    return <div style={{ padding: 12 }}>No DICOM instances provided.</div>;
  }

  // Build CSS grid template without String.replaceAll (TS lib friendly)
  const gridTemplateAreas = grid.areas.map((row) => `"${row}"`).join(' ');

  return (
    <div className="dv-root">
      <div className="dv-toolbar">
        <select value={layout} onChange={(e) => setLayout(e.target.value as Layout)}>
          <option value="1x1">1 view</option>
          <option value="1x3">3 in a row</option>
          <option value="2x2">2 × 2</option>
          <option value="2x1">2 stacked</option>
          <option value="L-2v">2 left + 1 right</option>
          <option value="R-2v">1 left + 2 right</option>
        </select>
      </div>

      <div
        className="dv-grid"
        style={{
          gridTemplateRows: `repeat(${grid.rows}, 1fr)`,
          gridTemplateColumns: `repeat(${grid.cols}, 1fr)`,
          gridTemplateAreas: gridTemplateAreas,
        }}
        ref={containerRef}
      >
        {Array.from(new Set(grid.areas.join(' ').split(' '))).map((name) => (
          <div key={name} className="dv-cell" style={{ gridArea: name }}>
            <div data-cell style={{ width: '100%', height: '100%', background: 'black' }} />
          </div>
        ))}
      </div>
    </div>
  );
}
