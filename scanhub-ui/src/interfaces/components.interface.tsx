// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
// Component interfaces: Pass data and functions between components
import {  ReactNode } from 'react'
import { PatientOut } from '../generated-client/patient'

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

export interface PatientTableInterface {
  patients: PatientOut[]
}

export interface RefetchableItemInterface<T> {
  item: T
  refetchParentData: () => void
}

export interface ItemSelection {
  type: 'exam' | 'workflow' | 'task' | undefined, 
  name: string | undefined,
  itemId: string | undefined
}

export const ITEM_UNSELECTED = { type: undefined, name: undefined, itemId: undefined }

export interface SelectableItemInterface<T> {
  item: T
  selection: ItemSelection
  onClick: () => void
}

export interface ModalProps {
  onSubmit: () => void
  isOpen: boolean
  setOpen: (open: boolean) => void
}

export interface ModalPropsCreate extends ModalProps {
  createTemplate: boolean
  parentId: string | undefined
  modalType: 'create'
}

export interface ModalPropsModify<T> extends ModalProps {
  item: T
  modalType: 'modify'
}

export interface ModalPropsCreateModifyFromTemplate<T> extends ModalProps {
  item: T
  modalType: 'createModifyFromTemplate'
}

export interface AccordionWithMenuInterface {
  accordionSummary?: ReactNode    // the summary that is always shown
  children?: ReactNode            // the details to expand
  accordionMenu?: ReactNode       // the element/menu that is displayed next to the summary
}