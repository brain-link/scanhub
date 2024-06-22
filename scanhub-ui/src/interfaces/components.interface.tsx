// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
// Component interfaces: Pass data and functions between components
import { PatientOut } from '../generated-client/patient'
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
  Error = 'error',
  Info = 'info',
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

export interface ModalComponentProps<T> {
  onSubmit: (data: T) => void
  onClose: () => void
  setOpen: (open: boolean) => void
  isOpen: boolean
  setAlert?: (alert: string | null) => void
}

export interface PatientTableInterface {
  patients: PatientOut[]
}

export interface TemplateInterface<T> {
  data: T
  onClicked: () => void
  onDeleted: () => void
}

export interface InstanceInterface<T> {
  data: T
  refetchParentData: () => void
}

export interface CreateInstanceModalInterface {
  parentId: number | string
  onSubmit: () => void
  isOpen: boolean
  setOpen: (open: boolean) => void
}
