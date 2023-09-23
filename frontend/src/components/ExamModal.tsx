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
import { Exam } from '../interfaces/data.interface';
import { ModalProps } from '../interfaces/components.interface';

// Exam form template, order is row wise, used to map the exam fields
const createExamFormContent = [
    {key: 'name', label: 'Exam Name', placeholder: 'Knee complaints'},
    {key: 'site', label: 'Site', placeholder: 'Berlin'},
    {key: 'address', label: 'Site Address', placeholder: 'Street name, number'},
    {key: 'creator', label: 'Name of Exam Creater', placeholder: 'Last name, first name'},
    {key: 'status', label: 'Status', placeholder: 'Exam created'},
]

function ExamModal(props: ModalProps<Exam>) {

    const params = useParams();

    const [exam, setExam] = props.data ? React.useState<Exam>(props.data) :
        React.useState<Exam>({
            id: NaN, 
            patient_id: Number(params.patientId),
            name: '',
            procedures: [],
            country: 'D',
            site: '',
            address: '',
            creator: '', 
            status: '', 
            datetime_created: new Date(), 
        })

    const title = props.data ? 'Update Exam' : 'Create Exam'

    return (
        <Modal 
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
                
                <Stack spacing={3}>
                    <Grid container rowSpacing={1.5} columnSpacing={5}>
                        {
                            createExamFormContent.map((item, index) => (
                                <Grid key={ index } md={6}
                                >
                                    <FormLabel>{ item.label }</FormLabel>
                                    <Input 
                                        name={ item.key }
                                        onChange={(e) => setExam({...exam, [e.target.name]: e.target.value})} 
                                        placeholder={ item.placeholder }
                                        defaultValue={ exam[item.key] }
                                        required 
                                    />
                                </Grid>
                            ))
                        }
                    </Grid>
                    
                    <Button 
                        size='sm'
                        sx={{ maxWidth: 120 }}
                        onClick={
                            (event) => {
                                event.preventDefault();
                                props.handleModalSubmit(exam);
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

export default ExamModal;