import { useNavigate } from 'react-router-dom';
import { useMutation } from "react-query";
import * as React from 'react';

import Typography from '@mui/joy/Typography';
import Container from '@mui/system/Container';
import AddSharpIcon from '@mui/icons-material/AddSharp';
import IconButton from '@mui/joy/IconButton';
import LinearProgress from '@mui/joy/LinearProgress';
import Modal from '@mui/joy/Modal';
import ModalClose from '@mui/joy/ModalClose';
import ModalDialog from '@mui/joy/ModalDialog';
import Stack from '@mui/joy/Stack';
import Grid from '@mui/joy/Grid';
import Input from '@mui/joy/Input';
import FormLabel from '@mui/joy/FormLabel';
import Button from '@mui/joy/Button';
import Table from '@mui/joy/Table';
import Box from '@mui/joy/Box';

import client from '../client/queries';
import { Patient } from '../client/interfaces';


// Patient form items, order is row wise
const createPatientFormContent = [
    {key: 'name', label: 'Patient Name', placeholder: 'Last name, first name'},
    {key: 'issuer', label: 'Issuer', placeholder: 'Last name, first name'},
    {key: 'sex', label: 'Patient Gender', placeholder: 'M/F/D'},
    {key: 'status', label: 'Status', placeholder: 'Patient created'},
    {key: 'birth_date', label: 'Patient Birth Date', placeholder: '01.01.1995'},
    {key: 'comment', label: 'Comment', placeholder: ''},
]


export default function PatientTable() {

    // Create raw patient
    const [patient, setPatient] = React.useState<Patient>({
        id: 0, sex: "", name: "", issuer: "", status: "", comment: "", 
        birth_date: "", datetime_created: new Date(), datetime_updated: new Date()
    });
    const [patients, setPatients] = React.useState<Patient[]>([]);
    const [dialogOpen, setDialogOpen] = React.useState<boolean>(false);

    const navigate = useNavigate();

    async function fetchPatients() {
        await client.patients.getAll().then((data) => { setPatients(data) })
    }

    // Fetch all patients
    React.useEffect(() => {
        fetchPatients();
    }, []);

    // Post a new record and refetch records table
    const mutation = useMutation(async() => {
        await client.patients.create(patient).then( (response) => { patients?.push(response) })
        .catch((err) => { console.log(err) })
    })

    if (!patients) {
        return (
            <Container maxWidth={false} sx={{ width: '50%', mt: 5, justifyContent: 'center' }}>
                <Typography>Loading patients...</Typography>
                <LinearProgress variant="plain" />
            </Container>
    )}

    return (
        <Box sx={{ m: 5 }}>

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
                    size='sm'
                    sx={{
                        width: '50vw', 
                        // height: '50vh',
                        borderRadius: 'md',
                        p: 5,
                        // boxShadow: 'lg',
                    }}
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
                        Create New Patient
                    </Typography>
                    
                    <form
                        onSubmit={(event) => {
                            event.preventDefault();
                            mutation.mutate();
                            setDialogOpen(false);
                        }}
                    >
                        <Stack spacing={5}>
                            <Grid container rowSpacing={1.5} columnSpacing={5}>
                                {
                                    createPatientFormContent.map((item, index) => (
                                        <Grid key={ index } md={6}
                                        >
                                            <FormLabel>{ item.label }</FormLabel>
                                            <Input 
                                                name={ item.key }
                                                onChange={(e) => setPatient({...patient, [e.target.name]: e.target.value})} 
                                                placeholder={ item.placeholder }
                                                required 
                                            />
                                        </Grid>
                                    ))
                                }
                            </Grid>
                            <Button type="submit">Submit</Button>
                        </Stack>
                    </form>
                </ModalDialog>
            </Modal>

            
            <IconButton size='sm' variant='outlined'>
                <AddSharpIcon onClick={() => setDialogOpen(true)}/>
            </IconButton>

            <Table
                hoverRow
                borderAxis="xBetween"
                color="neutral"
                size="sm"
                stickyHeader
                variant="plain"
            >
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Sex</th>
                        <th>Birthday</th>
                        <th>Issuer</th>
                        <th>Status</th>
                        <th>Comment</th>
                        <th>Admission</th>
                        <th>Updated</th>
                    </tr>
                </thead>

                <tbody>
                    { patients?.map(patient => (
                        <tr
                            onClick={() => {navigate(`/patients/${patient.id}`)}}
                            key={ patient.id }
                        >
                            <td>{ patient.id }</td>
                            <td>{ patient.name }</td>
                            <td>{ patient.sex }</td>
                            <td>{ patient.issuer }</td>
                            <td>{ patient.status }</td>
                            <td>{ patient.comment }</td>
                            <td>{ new Date(patient.datetime_created).toDateString() }</td>
                            <td>{ patient.datetime_updated ? new Date(patient.datetime_updated).toDateString() : '-' }</td>
                        </tr>
                    )) }
                </tbody>

            </Table>
        </Box>
    );
}





