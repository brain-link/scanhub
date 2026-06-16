/**
 * Global Cornerstone rendering engine singleton.
 *
 * A RenderingEngine allocates Cornerstone's WebGLContextPool upfront. Creating
 * more than one engine (e.g., from React StrictMode double-invoke or component
 * remounts) exhausts the browser's WebGL context limit (~8-16 contexts). Sharing
 * a single long-lived engine and managing only viewport lifecycles per component
 * is the correct Cornerstone3D usage pattern.
 */
import { RenderingEngine, getRenderingEngine } from '@cornerstonejs/core';
import { initCornerstone } from './init';

export const RENDERING_ENGINE_ID = 're-dicom-global';

let engineReadyPromise: Promise<RenderingEngine> | null = null;

/**
 * Returns the global rendering engine, initialising Cornerstone and creating
 * the engine exactly once per browser session. Safe to call concurrently.
 */
export function getOrCreateEngine(getAccessToken?: () => string | undefined): Promise<RenderingEngine> {
  if (!engineReadyPromise) {
    engineReadyPromise = (async () => {
      await initCornerstone(getAccessToken);
      const existing = getRenderingEngine(RENDERING_ENGINE_ID);
      if (existing) return existing;
      return new RenderingEngine(RENDERING_ENGINE_ID);
    })();
  } else if (getAccessToken) {
    // Update the token getter for subsequent WADO requests without re-creating engine.
    initCornerstone(getAccessToken);
  }
  return engineReadyPromise;
}
