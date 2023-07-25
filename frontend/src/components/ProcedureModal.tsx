// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

// ProcedureCreateModal.tsx is responsible for rendering the modal for creating a new procedure.

import * as React from 'react';
import { useParams } from 'react-router-dom';
import { useMutation } from 'react-query';

// Import mui joy components
import Button from '@mui/joy/Button';
import Typography from '@mui/joy/Typography';
import Input from '@mui/joy/Input';
import FormLabel from '@mui/joy/FormLabel';
import Modal from '@mui/joy/Modal';
import ModalClose from '@mui/joy/ModalClose';
import ModalDialog from '@mui/joy/ModalDialog';
import Stack from '@mui/joy/Stack';
import Grid from '@mui/joy/Grid';

// Import procedure api service and interfaces 
import client from '../client/exam-tree-queries';
import { Procedure } from '../interfaces/data.interface';
import { ModalProps } from '../interfaces/components.interface';


// Procedure form template
const createProcedureForm = [
    {key: 'name', label: 'Procedure Name', placeholder: 'MRI examination'},
    {key: 'status', label: 'Status', placeholder: 'Procedure created'},
]

function ProcedureModal(props: ModalProps<Procedure>) {

    const params = useParams();

    const [procedure, setProcedure] = props.data ? React.useState<Procedure>(props.data) :
        React.useState<Procedure>({
            id: NaN,
            exam_id: Number(params.examId),
            name: "",
            status: "",
            // jobs: [],
            datetime_created: new Date(),
        });

    const title = props.data ? "Update Procedure" : "Create Procedure"

    return (
        <Modal 
            keepMounted
            open={ props.dialogOpen }
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
                            createProcedureForm.map((item, index) => (
                                <Grid key={ index } md={12}
                                >
                                    <FormLabel>{ item.label }</FormLabel>
                                    <Input 
                                        name={ item.key }
                                        onChange={(e) => setProcedure({...procedure, [e.target.name]: e.target.value})} 
                                        placeholder={ item.placeholder }
                                        defaultValue={ procedure[item.key] }
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
                                props.handleModalSubmit(procedure);
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

export default ProcedureModal;