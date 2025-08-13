import { useMemo } from 'react';
import * as cs3d from '@cornerstonejs/core';

/**
 * Decide if we should prefer volume (MPR) rendering.
 * True if:
 *  - there are multiple imageIds, or
 *  - a single imageId is multi-frame (NumberOfFrames > 1)
 */
export function usePreferVolume(imageIds: string[]): boolean {
  return useMemo(() => {
    if (!imageIds || imageIds.length === 0) return false;

    // Classic case: multiple files = likely a volume
    if (imageIds.length > 1) return true;

    // Single file: check if it's multi-frame
    const imageId = imageIds[0];
    const mf = cs3d.metaData.get('multiFrameModule', imageId) as
      | { numberOfFrames?: number }
      | undefined;

    const nFrames = mf?.numberOfFrames ?? 0;
    return nFrames > 1;
  }, [imageIds]);
}
