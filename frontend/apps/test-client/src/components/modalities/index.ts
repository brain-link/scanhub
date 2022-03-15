import { ConfigureMRIModality } from './ConfigureMRI'

export type Modalities = 'configure-mri' | 'dicom'

export function getModalityComponent(modality: string) {
  switch(modality) {
    case 'configure-mri': return ConfigureMRIModality
    default:
      throw new Error(`Modality not found, this could happen due to version mismatch.`)
  }
}
