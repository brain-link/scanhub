// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

// Query clients for all services

import axios from 'axios';

import { Patient } from './interfaces';
import { Device } from './interfaces';
import { Workflow } from './interfaces';
import { Exam } from './interfaces';
import { Procedure } from './interfaces';
import { Job } from './interfaces';
import { Record } from './interfaces';

import baseUrls from './urls';

// const patientApi = axios.create({baseURL: baseUrls.patientService})
// const deviceApi = axios.create({baseURL: baseUrls.deviceService})
// const workflowApi = axios.create({baseURL: baseUrls.workflowService})
// const examApi = axios.create({baseURL: baseUrls.examService, headers: {
//     "Content-type": "application/json"
// }})

// Idea: Create Template class
// Inherit all query clients (patients, exam, device, workflow, etc. ) from same template and gather them in one object

// Patient query client
const patients = {

    create: async (data: Patient): Promise<Patient> => {
        const response = await axios.post<Patient>(`${baseUrls.patientService}/`, data);
        // const response = await patientApi.post('/', data);
        return response.data;
    },
    getAll: async(): Promise<Patient[]> => {
        const response = await axios.get<Patient[]>(`${baseUrls.patientService}/patients`);
        // const response = await axios.get(`/patients`);
        return response.data;
    },
    get: async (id: number): Promise<Patient> => {
        const response = await axios.get<Patient>(`${baseUrls.patientService}/${id}/`);
        // const response = await patientApi.get(`/${id}`);
        return response.data;
    }, 
    update: async (id: number, data: Partial<Patient>): Promise<Patient> => {
        const response = await axios.patch<Patient>(`${baseUrls.patientService}/${id}/`, data);
        // const response = await patientApi.patch(`/${id}`, data);
        return response.data;
    },
    delete: async (id: number): Promise<void> => {
        await axios.delete(`${baseUrls.patientService}/${id}/`);
        // await patientApi.delete(`/${id}`);
    },
}

// Device queries
const devices = {
    create: async (data: Device): Promise<Device> => {
        const response = await axios.post<Device>(`${baseUrls.deviceService}/`, data);
        return response.data;
    },
    getAll: async(): Promise<Device[]> => {
        const response = await axios.get<Device[]>(`${baseUrls.deviceService}/devices/`);
        return response.data;
    },
    get: async(id: number): Promise<Device> => {
        const response = await axios.get<Device>(`${baseUrls.deviceService}/${id}/`);
        return response.data;
    },
    update: async(id: number, data: Partial<Device>): Promise<Device> => {
        const response = await axios.patch<Device>(`${baseUrls.deviceService}/${id}/`, data);
        return response.data;
    },
    delete: async(id: number): Promise<void> => {
        await axios.delete(`${baseUrls.deviceService}/${id}/`);
    },
}

// Workflow queries
const workflows = {
    create: async (data: Workflow): Promise<Workflow> => {
        const response = await axios.post<Workflow>(`${baseUrls.workflowService}/`, data);
        return response.data;
    },
    getAll: async(): Promise<Workflow[]> => {
        const response = await axios.get<Workflow[]>(`${baseUrls.workflowService}/workflows/`);
        return response.data;
    },
    get: async(id: number): Promise<Workflow> => {
        const response = await axios.get<Workflow>(`${baseUrls.workflowService}/${id}/`);
        return response.data;
    },
    update: async(id: number, data: Partial<Workflow>): Promise<Workflow> => {
        const response = await axios.patch<Workflow>(`${baseUrls.workflowService}/${id}/`, data);
        return response.data;
    },
    delete: async(id: number): Promise<void> => {
        await axios.delete(`${baseUrls.workflowService}/${id}/`);
    },
}

// Record queries
const records = {
    create: async (data: Record): Promise<Record> => {
        const response = await axios.post<Record>(`${baseUrls.examService}/record/`, data);
        return response.data;
    },
    getAll: async(job_id: number): Promise<Record[]> => {
        const response = await axios.get<Record[]>(`${baseUrls.examService}/records/${job_id}`);
        return response.data;
    },
    get: async(id: number): Promise<Record> => {
        const response = await axios.get<Record>(`${baseUrls.examService}/record/${id}/`);
        return response.data;
    },
    delete: async(id: number): Promise<void> => {
        await axios.delete(`${baseUrls.examService}/record/${id}/`);
    },
}

// Job queries
const jobs = {
    create: async (data: Job): Promise<Job> => {
        const response = await axios.post<Job>(`${baseUrls.examService}/job/`, data);
        return response.data;
    },
    getAll: async(procedure_id: number): Promise<Job[]> => {
        const response = await axios.get<Job[]>(`${baseUrls.examService}/jobs/${procedure_id}`);
        return response.data;
    },
    get: async(id: number): Promise<Job> => {
        const response = await axios.get<Job>(`${baseUrls.examService}/job/${id}`);
        return response.data;
    },
    update: async(id: number, data: Partial<Job>): Promise<Job> => {
        const response = await axios.patch<Job>(`${baseUrls.examService}/job/${id}`, data);
        return response.data;
    },
    delete: async(id: number): Promise<void> => {
        await axios.delete(`${baseUrls.examService}/job/${id}/`);
    },
}

// Procedure queries
const procedures = {
    create: async (data: Procedure): Promise<Procedure> => {
        const response = await axios.post<Procedure>(`${baseUrls.examService}/procedure/`, data);
        return response.data;
    },
    getAll: async(exam_id: number): Promise<Procedure[] | []> => {
        try {
            const response = await axios.get<Procedure[]>(`${baseUrls.examService}/procedures/${exam_id}/`);
            return response.data;
        } catch (err) {
            if (axios.isAxiosError(err) && err.response?.status) {
                console.log('Error response status: ', err.response?.status);
            } else {
                console.log(err);
            }
        }
        return [];
    },
    get: async(id: number): Promise<Procedure> => {
        const response = await axios.get<Procedure>(`${baseUrls.examService}/procedure/${id}/`);
        return response.data;
    },
    update: async(id: number, data: Partial<Procedure>): Promise<Procedure> => {
        const response = await axios.patch<Procedure>(`${baseUrls.examService}/procedure/${id}/`, data);
        return response.data;
    },
    delete: async(id: number): Promise<void> => {
        await axios.delete(`${baseUrls.examService}/procedure/${id}/`);
    },
}

// Exam queries
const exams = {
    create: async (data: Exam): Promise<Exam> => {
        const response = await axios.post<Exam>(`${baseUrls.examService}/exam/`, data);
        return response.data;
    },
    getAll: async(patientId: number): Promise<Exam[] | []> => {
        try {
            const response = await axios.get<Exam[]>(`${baseUrls.examService}/exams/${patientId}/`);
            return response.data;
        } catch (err) {
            // TODO: Implementation of error handling
            if (axios.isAxiosError(err) && err.response?.status) {
                console.log('Error response status: ', err.response?.status);
            } else {
                console.log(err);
            }
        }
        return [];
    },
    get: async(id: number): Promise<Exam> => {
        const response = await axios.get<Exam>(`${baseUrls.examService}/procedure/${id}/`);
        return response.data;
    },
    update: async(id: number, data: Partial<Exam>): Promise<Exam> => {
        const response = await axios.patch<Exam>(`${baseUrls.examService}/procedure/${id}/`, data);
        return response.data;
    },
    delete: async(id: number): Promise<void> => {
        await axios.delete(`${baseUrls.examService}/procedure/${id}/`);
    },
}


export default {
    patients,
    devices,
    workflows,
    records,
    jobs,
    procedures,
    exams,
}
