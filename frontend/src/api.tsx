import baseUrls from './client/urls'
import { PatientsApi } from "./generated-client/patient"
import { ExamsApi } from './generated-client/exam'

export const patientApi = new PatientsApi(undefined, baseUrls.patientService)
export const examApi = new ExamsApi(undefined, baseUrls.examService)