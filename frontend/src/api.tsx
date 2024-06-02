import baseUrls from './client/urls'
import { PatientsApi } from './generated-client/patient'
import { ExamsApi } from './generated-client/exam'
import { WorkflowsApi } from './generated-client/exam'
import { TasksApi } from './generated-client/exam'
import { LoginApi } from './generated-client/userlogin'

export const patientApi = new PatientsApi(undefined, baseUrls.patientService)
export const examApi = new ExamsApi(undefined, baseUrls.examService)
export const workflowsApi = new WorkflowsApi(undefined, baseUrls.examService)
export const taskApi = new TasksApi(undefined, baseUrls.examService)
export const loginApi = new LoginApi(undefined, baseUrls.loginService)
