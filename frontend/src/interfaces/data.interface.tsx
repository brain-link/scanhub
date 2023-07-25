// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

// Definition of interfaces for data objects

// TODO: Could add constructors for interfaces, requires the definition of a class and a constructor() within

export interface Patient {
    id: number;
    sex: string;
    name: string;
    birth_date: string; // TODO: change this to date...
    issuer: string;
    status: string;
    comment: string;
    datetime_created: Date;
    datetime_updated?: Date | null;
}

export interface Workflow {
    id: number;
    host: string;
    name: string;
    author?: string | null;
    modality: string;
    type: string;
    status: string;
    kafka_topic: string;
    datetime_created: Date;
    datetime_updated?: Date | null;
}

export interface Device {
    id: number;
    name: string;
    manufacturer: string;
    modality: string;
    status: string;
    site: string | null;
    ip_address: string;
    datetime_created: Date;
    datetime_updated?: Date | null;
}

export interface Record {
    id: number;
    data_path?: string | null;
    comment?: string | null;
    datetime_created: Date;
}

export interface Job {
    id: number;
    procedure_id: number;
    type: string;
    comment?: string | null;
    is_acquired?: boolean;
    sequence_id: string;
    device_id: Number;
    workflow_id?: Number | null;
    records?: [Record] | [];
    datetime_created: Date;
    datetime_updated?: Date | null;
}

export interface Procedure {
    id: number;
    exam_id: number;
    name: string;
    status: string;
    jobs?: [Job] | [];
    datetime_created: Date;
    datetime_updated?: Date | null;
}

export interface Exam {
    id: number;
    patient_id: number;
    name: string;
    procedures?: [Procedure] | [];
    country: string | null;
    site: string | null;
    address: string | null;
    creator: string;
    status: string;
    datetime_created: Date;
    datetime_updated?: Date | null;
}
