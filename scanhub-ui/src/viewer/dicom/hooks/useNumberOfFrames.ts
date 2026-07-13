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

      // 2) Prime metadata by loading the image as-is (no-op if cached), then
      //    try again. Deliberately no `?frame=` suffix here: we don't yet
      //    know whether this is multiframe, and a plain imageId always
      //    resolves to the first frame for both single- and multi-frame
      //    files, whereas guessing a frame number can be out of range for
      //    single-frame files (pixel data has exactly one frame, at index 0).
      try {
        await imageLoader.loadAndCacheImage(id);
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
