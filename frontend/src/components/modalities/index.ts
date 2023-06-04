// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

// ConerstoneInit.ts initializes cornerstone and cornerstoneTools and sets some default values for the tools and the viewer

import { ConfigureMRI } from './ConfigureMRI'
import { DICOM } from './DICOM'

export type Modalities = 'configure-mri' | 'dicom'

export function getModalityComponent(modality: string) {
  switch(modality) {
    case 'configure-mri': return ConfigureMRI
    case 'dicom': return DICOM
    default:
      throw new Error(`Modality not found, this could happen due to version mismatch.`)
  }
}
