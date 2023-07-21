// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

// ExamCreateModal.tsx is responsible for rendering the modal for creating a new exam.

import * as React from 'react';
import { useParams } from 'react-router-dom';
import { useMutation } from 'react-query';

// Import mui joy components
import Typography from '@mui/joy/Typography';
import Button from '@mui/joy/Button';
import Input from '@mui/joy/Input';
import FormLabel from '@mui/joy/FormLabel';
import Stack from '@mui/joy/Stack';
import Grid from '@mui/joy/Grid';
import Modal from '@mui/joy/Modal';
import ModalClose from '@mui/joy/ModalClose';
import ModalDialog from '@mui/joy/ModalDialog';

// Import api service and interfaces
import client from '../../client/exam-tree-queries';
import { Job } from '../../interfaces/data.interface';
import { ModalProps } from '../../interfaces/components.interface';


function ExamList({data, dialogOpen, setDialogOpen, onCreated}: ModalProps<Job>) {

    const params = useParams();

    const [job, setJob] = data ? React.useState<Job>(data) : 
        React.useState<Job>({
            id: 0, 
            procedure_id: Number(params.procedure_id),
            type: '',
            comment: '',
            is_acquired: false,
            sequence_id: '',
            device_id: 0,
            workflow_id: null, 
            records: [], 
            datetime_created: new Date(),
            datetime_updated: new Date(),
        })
    

    const createExam = useMutation( async() => {
        await client.jobService.create(job)
        .then( () => { onCreated() })
        .catch((err) => { console.log("Error during job creation: ", err) }) 
    })

    return (
        <Modal 
            keepMounted
            open={dialogOpen}
            color='neutral'
            onClose={() => setDialogOpen(false)}
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
                    Create new exam
                </Typography>
                
                <form
                    onSubmit={(event) => {
                        event.preventDefault();
                        createExam.mutate();
                        setDialogOpen(false);
                    }}
                >
                    <Stack direction="column" spacing={5}>
                        
                        <Stack direction="row">

                            <FormLabel>Type</FormLabel>
                            <Input 
                                name="type"
                                onChange={(e) => setJob({...job, [e.target.name]: e.target.value})} 
                                placeholder="Job type"
                                required 
                            />

                            <FormLabel>Comment</FormLabel>
                            <Input 
                                name="comment"
                                onChange={(e) => setJob({...job, [e.target.name]: e.target.value})} 
                                placeholder="Job description"
                                required 
                            />

                            <FormLabel>Sequence</FormLabel>


                        </Stack>

                        <Button size='sm' type="submit" sx={{ maxWidth: 100 }}>Save</Button>

                    </Stack>

                </form>
            </ModalDialog>
        </Modal>
    );  
}

export default ExamList;