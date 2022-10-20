import * as React from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import Divider from '@mui/material/Divider';
import Typography from '@mui/joy/Typography';
import Box from '@mui/joy/Box';
import config from '../utils/config';
import { format_date } from '../utils/formatter';
import { Patient } from './Interfaces';

export default function PatientInfo() {

    const params = useParams();
    const [patient, setPatient] = React.useState<Patient | undefined>(undefined);

    async function fetchPatient() {
        await axios.get( `${config["baseURL"]}/patients/${params.patientId}` )
        .then((response) => { setPatient(response.data) })
    }

    // fetch patient
    React.useEffect(() => {
        fetchPatient();
    }, []);

    return (
        <Box>
            <Typography level="h5" sx={{ p:2 }}>Patient Info</Typography>
            <Divider />
            <Box
                sx={{
                    gap: 2,
                    p: 2,
                    display: 'grid',
                    gridTemplateColumns: 'auto 1fr',
                    '& > *:nth-child(odd)': { 
                        color: 'text.secondary' 
                    },
                }}
            >

                <Typography level="body2">ID</Typography>
                <Typography level="body2" textColor="text.primary">
                    {patient?.id}
                </Typography>

                <Typography level="body2">Sex</Typography>
                <Typography level="body2" textColor="text.primary">
                    {patient?.sex}
                </Typography>

                <Typography level="body2">Birthday</Typography>
                <Typography level="body2" textColor="text.primary">
                    {patient?.birthday}
                </Typography>

                <Typography level="body2">Admission</Typography>
                <Typography level="body2" textColor="text.primary">
                    { patient ? format_date(patient.admission_date) : "" }
                </Typography>

                <Typography level="body2">Status</Typography>
                <Typography level="body2" textColor="text.primary">
                    {patient?.status}
                </Typography>

                <Typography level="body2">Concern</Typography>
                <Typography level="body2" textColor="text.primary">
                    {patient?.concern}
                </Typography>

            </Box>
        </Box>
    )
};