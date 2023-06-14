// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

// Component interfaces: Pass data and functions between components

import { Job } from './data.interface';
import { Device } from './data.interface';
import { Workflow } from './data.interface';
import { MRISequence } from './mri-data.interface';

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
    sequences: MRISequence[];
    // workflows: Workflow[];
    refetchParentData: () => void;
}

export interface SequenceViewerProps {
    sequence_id: string;
}