import { Link as RouterLink, useNavigate } from 'react-router-dom';
import { Patient } from './Interfaces'
import { useMutation } from "react-query";
import axios from 'axios';
import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from "@mui/material/TableHead";
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import LinearProgress from '@mui/material/LinearProgress';
import Typography from '@mui/joy/Typography';
import Container from '@mui/system/Container';
import AddSharpIcon from '@mui/icons-material/AddSharp';
import IconButton from '@mui/joy/IconButton';

import Modal from '@mui/joy/Modal';
import ModalClose from '@mui/joy/ModalClose';
import ModalDialog from '@mui/joy/ModalDialog';
import Stack from '@mui/joy/Stack';
import TextField from '@mui/joy/TextField';
import Button from '@mui/joy/Button';

import config from '../utils/config';
import { format_date } from '../utils/formatter';

export default function PatientTable() {

    // Syncing our data
    // const { data: patients, isSuccess } = useQuery<Patient[]>("/patients");
    const [patients, setPatients] = React.useState<Patient[] | undefined >(undefined);
    const [patient, setPatient] = React.useState<Patient>({id: 0, admission_date: "", status: 0, sex: 0, concern: "", birthday: ""});
    const [dialogOpen, setDialogOpen] = React.useState<boolean>(false);

    const navigate = useNavigate();

    async function fetchPatients() {
        await axios.get(`${config["baseURL"]}/patients`)
        .then((response) => {setPatients(response.data)})
    }

    // Fetch all patients
    React.useEffect(() => {
        fetchPatients()
        // patients?.sort((a, b) => {return b.id - a.id})
        console.log("fetched patients...")
    }, [!dialogOpen]);

    // Post a new record and refetch records table
    const mutation = useMutation(async() => {
        await axios.post(`${config["baseURL"]}/patients/new`, patient)
        .then((response) => {
            // setPatient(response.data)
            console.log(response.data)
        })
        .catch((err) => { console.log(err) })
    })

    if (!patients) {
        return (
            <Container maxWidth={false} sx={{ width: '50%', mt: 5, justifyContent: 'center' }}>
                <Typography>Loading patients...</Typography>
                <LinearProgress />
            </Container>
    )}

    return (
        <TableContainer component={Paper} sx={{ m: 2, overflow: 'auto' }}>

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
                    sx={{
                        width: '50vh', 
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
                        Create new record
                    </Typography>
                    
                    <form
                        onSubmit={(event) => {
                            event.preventDefault();
                            mutation.mutate();
                            setDialogOpen(false);
                        }}
                    >
                        <Stack spacing={2}>
                            <TextField 
                                label='Sex' 
                                name='sex'
                                onChange={(e) => setPatient({...patient, [e.target.name]: e.target.value})} 
                                autoFocus 
                                required 
                            />
                            <TextField 
                                label='Concern'
                                name='concern'
                                onChange={(e) => setPatient({...patient, [e.target.name]: e.target.value})} 
                                required 
                            />
                            <TextField 
                                label='Date of birth'
                                name='birthday'
                                onChange={(e) => setPatient({...patient, [e.target.name]: e.target.value})} 
                                required 
                            />
                            <Button type="submit">Submit</Button>
                        </Stack>
                    </form>
                </ModalDialog>
            </Modal>

            <Table stickyHeader aria-label="Device Table">
                <TableHead>
                    <TableRow>
                        <TableCell><Typography level="h5">ID</Typography></TableCell>
                        <TableCell><Typography level="h5">Sex</Typography></TableCell>
                        <TableCell><Typography level="h5">Birthday</Typography></TableCell>
                        <TableCell><Typography level="h5">Status</Typography></TableCell>
                        <TableCell><Typography level="h5">Concern</Typography></TableCell>
                        <TableCell><Typography level="h5">Admission</Typography></TableCell>
                        <TableCell>
                            <IconButton size='sm' variant='outlined'>
                                <AddSharpIcon onClick={() => setDialogOpen(true)}/>
                            </IconButton>
                        </TableCell>
                    </TableRow>
                </TableHead>

                <TableBody>
                    {/* Map elements in patients to table cells */}
                    { patients?.map(patient => (
                        <TableRow 
                            hover={true} 
                            key={patient.id} 
                            sx={{ textDecoration: 'none' }}
                            onClick={() => {navigate(`/patients/${patient.id}`)}}
                        >
                            <TableCell>{ patient.id }</TableCell>
                            <TableCell>{ patient.sex }</TableCell>
                            <TableCell>{ patient.birthday }</TableCell>
                            <TableCell>{ patient.status }</TableCell>
                            <TableCell>{ patient.concern }</TableCell>
                            <TableCell>{ format_date(patient.admission_date) }</TableCell>
                        </TableRow>
                    )) }
                </TableBody>
            </Table>
        </TableContainer>
    );
}





