// hooks/useViewportResize.ts
import React from 'react';
import type { RenderingEngine } from '@cornerstonejs/core';
import type { ViewLayout } from '../cornerstone/viewLayouts';

export function useViewportResize(
  engineRef: React.RefObject<RenderingEngine | null>,
  layout: ViewLayout,
  containerRef: React.RefObject<HTMLDivElement | null>,
  viewportReady: boolean
) {
  React.useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    // Observe every tile; a single grid resize can miss some tiles otherwise
    const tiles = Array.from(container.querySelectorAll<HTMLDivElement>('[id^="viewport-"]'));

    const observer = new ResizeObserver(() => {
      // Skip if everything is 0x0 (hidden during panel transitions)
      const allZero = tiles.every(t => t.clientWidth === 0 || t.clientHeight === 0);
      if (allZero) return;

      // Defer one frame so CSS grid has finalized sizes
      requestAnimationFrame(() => {
        try {
          const eng = engineRef.current;
          if (!eng) return;
          eng.resize(false, true);
          // Reset each viewport’s camera so the projection matrix reflects the new aspect ratio
          eng.getViewports().forEach(vp => vp?.resetCamera?.());
          eng.render();
        } catch (e) {
          // ignore transient races during enable/disable
        }
      });
    });

    tiles.forEach(t => observer.observe(t));
    return () => observer.disconnect();
    // viewportReady is the key dependency here: on first mount, imageIds is
    // still empty and the parent renders its "select a result" placeholder
    // instead of `containerRef`'s markup, so this effect finds no container
    // and sets up no observer. `engineRef`/`containerRef` are refs with stable
    // identity, so they never trigger a re-run on their own — without
    // `viewportReady` flipping true (which only happens once the container
    // and its tiles genuinely exist), the observer would never get created.
  }, [engineRef, layout, containerRef, viewportReady]);
}
