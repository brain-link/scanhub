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
import client from '../client/queries';
import { Exam } from '../interfaces/data.interface';
import { CreateModalProps } from '../interfaces/components.interface';


// Exam form template, order is row wise
const createExamFormContent = [
    {key: 'name', label: 'Exam Name', placeholder: 'Knee complaints'},
    {key: 'site', label: 'Site', placeholder: 'Berlin'},
    {key: 'address', label: 'Site Address', placeholder: ''},
    {key: 'creator', label: 'Name of Exam Creater', placeholder: 'Last name, first name'},
    {key: 'status', label: 'Status', placeholder: 'Exam created'},
]


function ExamList({dialogOpen, setDialogOpen, onCreated}: CreateModalProps) {

    const params = useParams();

    const [exam, setExam] = React.useState<Exam>({
        id: 0, 
        patient_id: Number(params.patientId),
        name: '',
        procedures: [],
        country: 'D',
        site: '',
        address: '',
        creator: '', 
        status: '', 
        datetime_created: new Date(), 
        datetime_updated: new Date(),
    })

    const createExam = useMutation( async() => {
        await client.examService.create(exam)
        .then( () => { onCreated() })
        .catch((err) => { console.log("Error during exam creation: ", err) }) 
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
                    <Stack spacing={5}>
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
                                            required 
                                        />
                                    </Grid>
                                ))
                            }
                        </Grid>
                        <Button size='sm' type="submit" sx={{ maxWidth: 100 }}>Submit</Button>
                    </Stack>

                </form>
            </ModalDialog>
        </Modal>
    );  
}

export default ExamList;