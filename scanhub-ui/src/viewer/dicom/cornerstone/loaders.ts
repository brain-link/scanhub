/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * DicomViewer.tsx is responsible for rendering the DICOM viewport.
 */
import { volumeLoader, Types, cache } from '@cornerstonejs/core';
import { init as dicomImageLoaderInit } from '@cornerstonejs/dicom-image-loader';
import { cornerstoneStreamingImageVolumeLoader } from '@cornerstonejs/streaming-image-volume-loader';

// const { registerVolumeLoader } = volumeLoader;

export async function initLoaders(opts: { getAccessToken?: () => string | undefined } = {}) {
  // Register streaming volume loader
  volumeLoader.registerVolumeLoader(
    'cornerstoneStreamingImageVolume',
    cornerstoneStreamingImageVolumeLoader as unknown as Types.VolumeLoaderFn
  );

  await dicomImageLoaderInit({
    strict: false,
    maxWebWorkers: navigator.hardwareConcurrency || 1,
    beforeSend: (_xhr, _imageId, defaultHeaders) => {
      const token = opts.getAccessToken?.();
      return token ? { ...defaultHeaders, Authorization: `Bearer ${token}` } : defaultHeaders;
    },
  });

  // Optional: enlarge cache for big series
  // cache.setMaxCacheSize(1024 * 1024 * 1024);
}
