/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * api.tsx contains instances of the different apis.
 */
import { ExamsApi } from './generated-client/exam'
import { WorkflowsApi } from './generated-client/exam'
import { TasksApi } from './generated-client/exam'
import { PatientsApi } from './generated-client/patient'
import { LoginApi } from './generated-client/userlogin'
import { UserApi } from './generated-client/userlogin'
import baseUrls from './utils/Urls'


export const patientApi = new PatientsApi(undefined, baseUrls.patientService)
export const examApi = new ExamsApi(undefined, baseUrls.examService)
export const workflowsApi = new WorkflowsApi(undefined, baseUrls.examService)
export const taskApi = new TasksApi(undefined, baseUrls.examService)
export const loginApi = new LoginApi(undefined, baseUrls.userloginService)
export const userApi = new UserApi(undefined, baseUrls.userloginService)
