import * as React from 'react';
import axios from 'axios';

import Typography from '@mui/joy/Typography';
import Box from '@mui/joy/Box';

import { Patient } from './Interfaces';

export default function PatientInfo(patientURL: any) {

    const [patient, setPatient] = React.useState<Patient | undefined>(undefined);

    // fetch patient
    React.useEffect(() => {
        axios.get(patientURL.url).then((response) => { setPatient(response.data) })
    }, []);

    return (
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
                {patient?.admission_date}
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
    )
};