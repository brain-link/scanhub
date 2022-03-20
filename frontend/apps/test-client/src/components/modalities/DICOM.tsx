import type { ModalityProps } from './types'


export function DICOM({
  recordingId,
}: ModalityProps) {
  return (
    <img src='https://upload.wikimedia.org/wikipedia/commons/e/ef/MRI_Head_Brain_Normal.jpg' alt={recordingId} />
  )
}
