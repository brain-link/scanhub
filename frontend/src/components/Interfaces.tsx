
export interface Patient {
    id: number;
    sex: number;
    birthday: string;
    concern: string;
    // admission_date: string;
    status: string;
  }

export interface Device {
    id: number;
    modality: string;
    address: string;
    // site: string;    This is a foreign key
}