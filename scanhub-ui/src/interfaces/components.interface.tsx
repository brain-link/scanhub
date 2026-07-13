// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
// Component interfaces: Pass data and functions between components
import type { ReactElement } from 'react'
import { ItemStatus } from '../openapi/generated-client/protocol'


// export interface SequenceViewerProps {
//   sequence_id: string
// }

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

export interface RefetchableItemInterface<T> {
  item: T
  refetchParentData: () => void
}

export interface ItemSelection {
  type: 'protocol' | 'ACQUISITION' | undefined,
  name: string | undefined,
  itemId: string | undefined,
  status: ItemStatus,
  progress?: number,
  deviceId?: string
}

export const ITEM_UNSELECTED = { type: undefined, name: undefined, itemId: undefined, status: ItemStatus.New, progress: 0 }

export interface SelectableItemInterface<T> {
  item: T
  selection: ItemSelection
  onClick: () => void
  icon?: ReactElement
  hoverIcon?: ReactElement
}

export interface ModalProps {
  onSubmit: () => void
  isOpen: boolean
  setOpen: (open: boolean) => void
}

export interface ModalPropsItem<T> extends ModalProps {
  item: T
}

export interface ModalPropsCreate extends ModalProps {
  createTemplate: boolean
  parentId: string | undefined
  modalType: 'create'
}

export interface ModalPropsModify<T> extends ModalPropsItem<T> {
  modalType: 'modify'
}

export interface ModalPropsCreateModifyFromTemplate<T> extends ModalPropsItem<T> {
  modalType: 'createModifyFromTemplate'
}

export interface ModalPropsCreateFirstUser extends ModalProps {
  modalType: 'createFirstUser'
}

