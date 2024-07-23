// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
// Component interfaces: Pass data and functions between components
import {  ReactNode } from 'react'
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
}

export interface PatientTableInterface {
  patients: PatientOut[]
}

export interface ItemInterface<T> {
  data: T
  refetchParentData: () => void
}

export interface CreateItemModalInterface {
  parentId: string
  onSubmit: () => void
  isOpen: boolean
  setOpen: (open: boolean) => void
  createTemplate: boolean
}

export interface AccordionWithMenuInterface {
  accordionSummary?: ReactNode    // the summary that is always shown
  children?: ReactNode            // the details to expand
  accordionMenu?: ReactNode       // the element/menu that is displayed next to the summary
}
