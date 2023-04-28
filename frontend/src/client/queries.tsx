import { Patient } from './interfaces';
import { Device } from './interfaces';
import { Workflow } from './interfaces';
import { Exam } from './interfaces';
import { Procedure } from './interfaces';
import { Job } from './interfaces';
import { Record } from './interfaces';

import baseUrls from './urls';

import { ApiService } from './abstract-query-client';


export class PatientApiService extends ApiService<Patient> {
    constructor() {
      super(baseUrls.patientService);
    }
}

export class DeviceApiService extends ApiService<Device> {
    constructor() {
      super(baseUrls.deviceService);
    }
}

export class WorkflowApiService extends ApiService<Workflow> {
    constructor() {
      super(baseUrls.workflowService);
    }
}

export class ExamApiService extends ApiService<Exam> {
    constructor() {
      super(baseUrls.examService);
    }
}

export class ProcedureApiService extends ApiService<Procedure> {
    constructor() {
      super(baseUrls.procedureService);
    }
}
  
export class JobApiService extends ApiService<Job> {
    constructor() {
      super(baseUrls.jobService);
    }
}


const patientService = new PatientApiService();
const workflowService = new WorkflowApiService();
const deviceService = new DeviceApiService();
const examService = new ExamApiService();
const procedureService = new ProcedureApiService();
const jobService = new JobApiService();


// Export all services in one client
export default {
    patientService,
    workflowService,
    deviceService,
    examService,
    procedureService,
    jobService,
}
