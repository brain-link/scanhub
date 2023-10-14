// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
// Component interfaces: Pass data and functions between components
import { Job } from './data.interface'
import { Device } from './data.interface'
// import { Workflow } from './data.interface';
import { MRISequence } from './mri-data.interface'

export interface ModalProps<T> {
  handleModalSubmit: (data: T) => void
  data: T | null
  dialogOpen: boolean
  setDialogOpen: (open: boolean) => void
}

export interface ComponentProps<T> {
  data: T
  refetchParentData: () => void
  isSelected: boolean
}

export interface JobComponentProps {
  data: Job
  devices: Device[]
  sequences: MRISequence[]
  // workflows: Workflow[];
  refetchParentData: () => void
}

// Reuse JobComponentProps but omit data which can be null in case of the modal props
export interface JobModalProps extends Omit<JobComponentProps, 'data'> {
  data: Job | null
  handleModalSubmit: (data: Job) => void
  dialogOpen: boolean
  setDialogOpen: (open: boolean) => void
}

export interface SequenceViewerProps {
  sequence_id: string
}

export enum Alerts {
  Success = 'success',
  Warning = 'warning',
  Danger = 'danger',
  Neutral = 'neutral',
}

export interface AlertProps {
  title: string
  info?: string
  type: Alerts
}

export interface ExamTreeProps {
  setDataPath: (dataPath: string) => void
}

export interface SequenceUploadModal {
  fetchSequences: () => void
  dialogOpen: boolean
  setDialogOpen: (open: boolean) => void
}