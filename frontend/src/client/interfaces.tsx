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
    site?: string | null;
    ip_address: string;
    datetime_created: Date;
    datetime_updated?: Date | null;
}

export interface Record {
    id: number;
    device?: Device | null;
    workflow?: Workflow | null;
    status: string;
    comment?: string | null;
    datetime_created: Date;
    datetime_updated?: Date | null;
}

export interface Procedure {
    id: number;
    name: string;
    modality: string;
    status: string;
    // records: [Record];
    datetime_created: Date;
    datetime_updated?: Date | null;
}

export interface Exam {
    id: number;
    patient_id: string;
    name: string;
    procedures: [Procedure];
    country?: string | null;
    site?: string | null;
    address?: string | null;
    creator: string;
    status: string;
    datetime_created: Date;
    datetime_updated?: Date | null;
}
