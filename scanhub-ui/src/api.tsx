/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * api.tsx contains instances of the different apis.
 */
import { PatientsApi, HealthApi as PatientManagerHealthApi } from './openapi/generated-client/patient'
import { ProtocolsApi, TasksApi, ResultsApi, MriSequencesApi, DataApi, HealthApi as ProtocolManagerHealthApi } from './openapi/generated-client/protocol'
import { UserApi, LoginApi, HealthApi as UserLoginManagerHealthApi } from './openapi/generated-client/userlogin'
import { DevicesApi, HealthApi as DeviceManagerHealthApi } from './openapi/generated-client/device'
import baseUrls from './utils/Urls'


export const patientApi = new PatientsApi(undefined, baseUrls.patientService)
export const patientManagerHealthApi = new PatientManagerHealthApi(undefined, baseUrls.patientService)

export const protocolApi = new ProtocolsApi(undefined, baseUrls.protocolService)
export const taskApi = new TasksApi(undefined, baseUrls.protocolService)
export const resultApi = new ResultsApi(undefined, baseUrls.protocolService)
export const sequenceApi = new MriSequencesApi(undefined, baseUrls.protocolService)
export const dataApi = new DataApi(undefined, baseUrls.protocolService)
export const protocolManagerHealthApi = new ProtocolManagerHealthApi(undefined, baseUrls.protocolService)

export const loginApi = new LoginApi(undefined, baseUrls.userloginService)
export const userApi = new UserApi(undefined, baseUrls.userloginService)
export const userLoginManagerHealthApi = new UserLoginManagerHealthApi(undefined, baseUrls.userloginService)

export const deviceApi = new DevicesApi(undefined, baseUrls.deviceService)
export const deviceManagerHealthApi = new DeviceManagerHealthApi(undefined, baseUrls.deviceService)
