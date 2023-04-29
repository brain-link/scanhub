import * as React from 'react';
// import { useParams } from 'react-router-dom';
import Divider from '@mui/material/Divider';
import Typography from '@mui/joy/Typography';
import Box from '@mui/joy/Box';


// import client from '../client/queries';
import { Patient } from '../interfaces/data.interface';


function PatientInfo(props: { patient: Patient, isLoading: Boolean, isError: Boolean }) {

    const { patient, isLoading, isError } = props;

    if (isLoading) {
        // TODO: Beautify
        return <div>Loading...</div>;
    }

    if (isError) {
        // TODO: Beautify
        return <div>Error loading patient data</div>;
    }

    return (
        <Box>
            <Typography level="h5" sx={{ p: 1.5 }}>Patient Info</Typography>
            <Divider />
            {
                patient &&
                <Box
                    sx={{
                        rowGap: 0.4,
                        columnGap: 4,
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
                        {patient.id}
                    </Typography>

                    <Typography level="body2">Sex</Typography>
                    <Typography level="body2" textColor="text.primary">
                        {patient.sex}
                    </Typography>

                    <Typography level="body2">Birthday</Typography>
                    <Typography level="body2" textColor="text.primary">
                        { patient.birth_date }
                    </Typography>

                    <Typography level="body2">Admission</Typography>
                    <Typography level="body2" textColor="text.primary">
                        { new Date(patient.datetime_created).toDateString() }
                    </Typography>

                    <Typography level="body2">Updated</Typography>
                    <Typography level="body2" textColor="text.primary">
                        { patient.datetime_updated ? new Date(patient.datetime_updated).toDateString() : '-' }
                    </Typography>

                    <Typography level="body2">Status</Typography>
                    <Typography level="body2" textColor="text.primary">
                        {patient.status}
                    </Typography>

                    <Typography level="body2">Concern</Typography>
                    <Typography level="body2" textColor="text.primary">
                        {patient.issuer}
                    </Typography>

                </Box>
            }
        </Box>
    )
};

export default PatientInfo;
