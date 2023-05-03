// Component interfaces: Pass data and functions between components

import { Job } from './data.interface';
import { Device } from './data.interface';
import { Workflow } from './data.interface';

export interface CreateModalProps {
    dialogOpen: boolean,
    setDialogOpen: (open: boolean) => void;
    onCreated: () => void;
}

export interface ComponentProps<T> {
    data: T;
    refetchParentData: () => void;
    isSelected: boolean;
}

export interface JobComponentProps {
    job: Job;
    devices: Device[];
    workflows: Workflow[];
    refetchParentData: () => void;
}