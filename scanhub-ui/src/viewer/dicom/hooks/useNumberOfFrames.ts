import { useEffect, useState } from 'react';
import { metaData, imageLoader } from '@cornerstonejs/core';

export function useNumberOfFrames(imageIds: string[] | undefined, ready: boolean): number {
  const [frames, setFrames] = useState(0);

  useEffect(() => {
    let alive = true;

    const run = async () => {
      if (!ready || !imageIds?.length) {
        if (alive) setFrames(0);
        return;
      }

      // If you already have multiple instances, treat that as the stack length
      if (imageIds.length > 1) {
        if (alive) setFrames(imageIds.length);
        return;
      }

      const id = imageIds[0];

      const readFramesFromMeta = () => {
        const ip = metaData.get('imagePixelModule', id) as { numberOfFrames?: number } | undefined;
        const mf = metaData.get('multiframeModule', id) as { NumberOfFrames?: number } | undefined;
        return (ip?.numberOfFrames ?? mf?.NumberOfFrames ?? 1) | 0;
      };

      // 1) Try metadata first
      let n = readFramesFromMeta();
      if (n > 1) {
        if (alive) setFrames(n);
        return;
      }

      // 2) Prime metadata by loading the first frame (no-op if cached),
      //    then try again
      try {
        const first = id.includes('?') ? id : `${id}?frame=1`;
        await imageLoader.loadAndCacheImage(first);
      } catch {
        /* ignore — we'll still fall back to 1 */
      }

      n = readFramesFromMeta() || 1;
      if (alive) setFrames(n);
    };

    run();
    return () => { alive = false; };
  }, [ready, imageIds?.[0]]);

  return frames;
}
