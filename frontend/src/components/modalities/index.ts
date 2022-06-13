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
