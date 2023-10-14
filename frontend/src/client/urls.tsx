// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

// Definition of global variables

const baseUrls = {
  patientService: 'http://localhost:8100',
  deviceService: 'http://localhost:8080/api/v1/device',
  workflowService: 'http://localhost:8080/api/v1/workflow',
  examService: 'http://localhost:8080/api/v1/exam',
  procedureService: 'http://localhost:8080/api/v1/exam/procedure',
  jobService: 'http://localhost:8080/api/v1/exam/job',
  recordService: 'http://localhost:8080/api/v1/exam/record',
  mriSequenceService: 'http://localhost:8080/api/v1/mri/sequences',
  acquisitionControlService: 'http://localhost:8080/api/v1/mri/acquisitioncontrol',
}

export default baseUrls
