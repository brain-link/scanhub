/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * Initialize cornerstone 3D.
 */
import {init as csInit} from '@cornerstonejs/core';
import { init as toolsInit } from '@cornerstonejs/tools';
import { initLoaders } from './loaders';
import { registerDefaultTools } from './toolgroups';


let initialized: Promise<void> | null = null;

export function initCornerstone(getAccessToken?: () => string | undefined) {
  if (!initialized) {
    initialized = (
      async () => {
        // core
        await csInit();
        // tools
        toolsInit();
        // loaders
        await initLoaders({ getAccessToken });
        // tool registration
        registerDefaultTools();
      }
    )();
  }
  return initialized;
}
