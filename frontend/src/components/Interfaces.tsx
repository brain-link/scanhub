
export interface Patient {
    id: number;
    sex: number;
    birthday: string;
    concern: string;
    admission_date: string;
    status: number;
  }

export interface Site {
  id: number;
  name: string;
  city: string;
  country: string;
  address: string;
  patients: [number];
  users: [number];
}

export interface Device {
    id: number;
    modality: number;
    address: string;
    site_id: number;
    site: Site;
}

export interface Procedure {
  id: number;
  patient_id: number;
  reason: string;
  date: string;
}

export interface Record {
  id: number;
  procedure_id: number;
  device_id: number;
  date: string;
  thumbnail: string;
  data: string;
  comment: string;
}

