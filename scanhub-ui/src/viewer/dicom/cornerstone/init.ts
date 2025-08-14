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

// import { init as initTurboJPEG8 } from '@cornerstonejs/codec-libjpeg-turbo-8bit';
// import { init as initCharLS } from '@cornerstonejs/codec-charls';
// import { init as initOpenJPEG } from '@cornerstonejs/codec-openjpeg';
// import { init as initOpenJPH } from '@cornerstonejs/codec-openjph';

let initialized = false;

export async function initCornerstone3D(getAccessToken?: () => string | undefined) {

  if (initialized) return;

  // core
  await csInit();
  // tools
  toolsInit();

  // codecs
  // initTurboJPEG8();
  // initCharLS();
  // initOpenJPEG();
  // initOpenJPH();

  // loaders
  initLoaders({ getAccessToken });
  // tool registration
  registerDefaultTools();

  initialized = true;
}
