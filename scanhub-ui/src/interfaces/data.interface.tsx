// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

// Definition of interfaces for data objects

// TODO: Could add constructors for interfaces, requires the definition of a class and a constructor() within

export interface Device {
  id: string
  name: string
  manufacturer: string
  modality: string
  status: string
  site: string | null
  ip_address: string
  datetime_created: Date
  datetime_updated?: Date | null
}

interface Record {
  id: string
  data_path?: string | null
  comment?: string | null
  datetime_created: Date
}

interface XYZ {
  X: number
  Y: number
  Z: number
}

interface AcquisitonLimits {
  patient_height: number
  patient_weight: number
  patient_gender: string
  patient_age: number
}

export interface SequenceParameters {
  fov: XYZ
  fov_offset: XYZ
}

export interface Job {
  id: string
  exam_id: string
  type: string
  comment?: string | null
  is_acquired?: boolean
  sequence_id: string
  device_id: string
  workflow_id?: number | null
  records?: [Record] | []
  datetime_created: Date
  datetime_updated?: Date | null
  acquisition_limits: AcquisitonLimits
  sequence_parameters: SequenceParameters
}

export interface Exam {
  id: string
  patient_id: number
  name: string
  jobs?: [Job] | []
  country: string | null
  site: string | null
  address: string | null
  creator: string
  status: string
  datetime_created: Date
  datetime_updated?: Date | null
}
