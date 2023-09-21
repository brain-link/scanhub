// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

// JobModal.tsx is responsible for rendering the modal for creating or updating a job.

import * as React from 'react';
import { useParams } from 'react-router-dom';

// Import mui joy components
import Typography from '@mui/joy/Typography';
import Button from '@mui/joy/Button';
import Input from '@mui/joy/Input';
import FormLabel from '@mui/joy/FormLabel';
import Stack from '@mui/joy/Stack';
import Modal from '@mui/joy/Modal';
import ModalClose from '@mui/joy/ModalClose';
import ModalDialog from '@mui/joy/ModalDialog';
import Select from '@mui/joy/Select';
import Option from '@mui/joy/Option';

// Import api service and interfaces
import { Job } from '../interfaces/data.interface';
import { JobModalProps } from '../interfaces/components.interface';


function JobModal(props: JobModalProps) {

    const params = useParams();

    const [job, setJob] = props.data ? React.useState<Job>(props.data) : 
        React.useState<Job>({
            id: 0,
            type: "",
            comment: "",
            procedure_id: Number(params.procedureId),
            sequence_id: "",
            workflow_id: null,
            device_id: "",
            datetime_created: new Date(),
        })

    React.useEffect(() => {
        setJob({...job, procedure_id: Number(params.procedureId)})
    }, [params.procedureId])
    
    // To be replaced by devices and workflows from database
    // const devices = [{"id": 1, "name": "MRI Simulator"}]
    const workflows = [{"id": 0, "name": "2d FFT"}]

    const title = props.data ? "Update Job" : "Create Job"

    return (
        <Modal 
            keepMounted
            open={props.dialogOpen}
            color='neutral'
            onClose={() => props.setDialogOpen(false)}
            sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}
        >
            <ModalDialog
                aria-labelledby="basic-modal-dialog-title"
                aria-describedby="basic-modal-dialog-description"
                sx={{ width: '50vw', borderRadius: 'md', p: 5 }}
            >
                <ModalClose
                    sx={{
                        top: '10px',
                        right: '10px',
                        borderRadius: '50%',
                        bgcolor: 'background.body',
                    }}
                />
                <Typography
                    id="basic-modal-dialog-title"
                    component="h2"
                    level="inherit"
                    fontSize="1.25em"
                    mb="0.25em"
                >
                    { title }
                </Typography>
                
                <Stack direction="column" spacing={3}>
                    <Stack direction="column" spacing={1.5}>

                        <FormLabel>Type</FormLabel>
                        <Input 
                            name="type"
                            onChange={(e) => setJob({...job, [e.target.name]: e.target.value})} 
                            placeholder="Job type"
                            defaultValue={ job.type }
                            required 
                        />

                        <FormLabel>Comment</FormLabel>
                        <Input 
                            name="comment"
                            onChange={(e) => setJob({...job, [e.target.name]: e.target.value})} 
                            placeholder="Job description"
                            defaultValue={ job.type }
                            required 
                        />

                        <FormLabel>Device</FormLabel>
                        <Select 
                            placeholder="Select..."
                            onChange={(
                                event: React.SyntheticEvent | null,
                                newValue: string | null
                            ) => {
                                // Only set new device if newValue is not null
                                newValue ? setJob({...job, ["device_id"]: newValue}) : () => {} 
                            }}
                            defaultValue={
                                // Device value cannot be null -> check if device id is contained in device list
                                props.devices.find(x => x.id === job.device_id) ? job.device_id : null 
                            }
                        >
                            {
                                props.devices.map((device, index) => (
                                    <Option key={index} value={device.id}>
                                        { device.name }
                                    </Option>
                                ))
                            }
                        </Select>

                        <FormLabel>Sequence</FormLabel>
                        <Select
                            placeholder="Select..."
                            onChange={(
                                event: React.SyntheticEvent | null,
                                newValue: string | null
                            ) => { 
                                // Only set sequence id if newValue is not null
                                newValue ? setJob({...job, ["sequence_id"]: newValue}) : () => {}
                            }}
                            defaultValue={ job.sequence_id }
                        >
                            {
                                props.sequences?.map( (sequence, index) => (
                                    <Option key={index} value={sequence._id}>
                                        { sequence.name }
                                    </Option>
                                ))
                            }
                        </Select>

                        <FormLabel>Workflow</FormLabel>
                        <Select 
                            placeholder="Select..."
                            onChange={(
                                event: React.SyntheticEvent | null,
                                newValue: Number | null
                            ) => {
                                // Workflow id can be null, no checks needed
                                setJob({...job, ["workflow_id"]: newValue});
                            }}
                            defaultValue={ job.workflow_id }
                        >
                            {
                                workflows.map( (workflow, index) => (
                                    <Option key={index} value={workflow.id}>
                                        { workflow.name }
                                    </Option>
                                ))
                            }
                        </Select>

                    </Stack>

                    <Button 
                        size='sm'
                        sx={{ maxWidth: 120 }}
                        onClick={
                            (event) => {
                                event.preventDefault();
                                props.handleModalSubmit(job);
                                props.setDialogOpen(false);
                            }
                        }
                    >
                        Save    
                    </Button>

                </Stack>

            </ModalDialog>
        </Modal>
    );  
}

export default JobModal;