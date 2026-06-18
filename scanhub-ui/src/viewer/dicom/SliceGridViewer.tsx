import React from 'react';
import { Enums, imageLoader, type Types } from '@cornerstonejs/core';
import type { RenderingEngine } from '@cornerstonejs/core';

const COLS = 4;

interface SliceGridViewerProps {
  imageIds: string[];
  numberOfFrames: number;
  engineRef: React.RefObject<RenderingEngine | null>;
}

export function SliceGridViewer({ imageIds, numberOfFrames, engineRef }: SliceGridViewerProps) {
  const scrollRef = React.useRef<HTMLDivElement>(null);
  const gridRef = React.useRef<HTMLDivElement>(null);

  const frameUrls = React.useMemo(() => {
    if (!imageIds.length || !numberOfFrames) return [];
    if (imageIds.length > 1) return imageIds;
    if (numberOfFrames === 1) return [imageIds[0]];
    return Array.from({ length: numberOfFrames }, (_, i) => `${imageIds[0]}?frame=${i + 1}`);
  }, [imageIds, numberOfFrames]);

  // Capture wheel events before Cornerstone's bubble-phase handlers can
  // consume them, and manually forward them to the scroll container.
  React.useEffect(() => {
    const container = scrollRef.current;
    if (!container) return;

    const handler = (e: WheelEvent) => {
      container.scrollBy({ top: e.deltaY });
      e.preventDefault();
    };

    container.addEventListener('wheel', handler, { capture: true, passive: false });
    return () => container.removeEventListener('wheel', handler, { capture: true });
  }, []);

  // Pass 1 – prime the image cache and collect the global pixel range so
  // every viewport can be initialised with the same VOI.
  // Pass 2 – enable viewports; images are already cached so setStack is fast.
  React.useEffect(() => {
    const engine = engineRef.current;
    if (!engine || !frameUrls.length || !gridRef.current) return;

    let cancelled = false;

    (async () => {
      let globalMin = Infinity;
      let globalMax = -Infinity;

      for (const url of frameUrls) {
        if (cancelled) return;
        try {
          const image = await imageLoader.loadAndCacheImage(url);
          if (isFinite(image.minPixelValue) && image.minPixelValue < globalMin) globalMin = image.minPixelValue;
          if (isFinite(image.maxPixelValue) && image.maxPixelValue > globalMax) globalMax = image.maxPixelValue;
        } catch { /* skip frames that fail to load */ }
      }

      const voiRange =
        isFinite(globalMin) && isFinite(globalMax)
          ? { lower: globalMin, upper: globalMax }
          : undefined;

      for (let i = 0; i < frameUrls.length; i++) {
        if (cancelled) return;

        const el = gridRef.current!.querySelector(`#slice-tile-${i}`) as HTMLDivElement | null;
        if (!el) continue;

        try {
          await engine.enableElement({
            viewportId: `slice-${i}`,
            element: el,
            type: Enums.ViewportType.STACK,
            defaultOptions: { background: [0, 0, 0] },
          });
        } catch { continue; }

        if (cancelled) return;

        const vp = engine.getViewport(`slice-${i}`) as Types.IStackViewport | null;
        if (!vp) continue;

        try {
          await vp.setStack([frameUrls[i]]);
          if (voiRange) vp.setProperties({ voiRange });
          vp.resetCamera();
          if (!cancelled) await vp.render();
        } catch { /* ignore transient render errors */ }
      }
    })();

    return () => {
      cancelled = true;
      const eng = engineRef.current;
      if (!eng) return;
      for (let i = 0; i < frameUrls.length; i++) {
        try { eng.disableElement(`slice-${i}`); } catch { /* already gone */ }
      }
    };
  }, [frameUrls, engineRef]);

  // Keep canvases in sync when the container is resized.
  React.useEffect(() => {
    const el = scrollRef.current;
    if (!el) return;

    const observer = new ResizeObserver(() => {
      requestAnimationFrame(() => {
        try {
          const eng = engineRef.current;
          if (!eng) return;
          eng.resize(false, true);
          eng.getViewports().forEach(vp => vp?.resetCamera?.());
          eng.render();
        } catch { /* ignore transient races */ }
      });
    });

    observer.observe(el);
    return () => observer.disconnect();
  }, [engineRef]);

  return (
    <>
      <style>{`
        .slice-scroll {
          overflow-y: auto;
          height: 100%;
          width: 100%;
          scrollbar-width: thin;
          scrollbar-color: rgba(255,255,255,0.22) rgba(255,255,255,0.05);
        }
        .slice-scroll::-webkit-scrollbar { width: 6px; }
        .slice-scroll::-webkit-scrollbar-track {
          background: rgba(255,255,255,0.05);
          border-radius: 3px;
        }
        .slice-scroll::-webkit-scrollbar-thumb {
          background: rgba(255,255,255,0.22);
          border-radius: 3px;
        }
        .slice-scroll::-webkit-scrollbar-thumb:hover {
          background: rgba(255,255,255,0.40);
        }
      `}</style>
      <div ref={scrollRef} className="slice-scroll">
        <div
          ref={gridRef}
          style={{
            display: 'grid',
            gridTemplateColumns: `repeat(${COLS}, 1fr)`,
            gap: 4,
            padding: 4,
          }}
        >
          {frameUrls.map((_, i) => (
            <div
              key={i}
              id={`slice-tile-${i}`}
              style={{ aspectRatio: '1', background: 'black', borderRadius: 4 }}
            />
          ))}
        </div>
      </div>
    </>
  );
}
