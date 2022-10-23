import * as React from 'react';
import { Outlet, useParams, Link as RouterLink } from 'react-router-dom';
import Box from '@mui/joy/Box';
import Typography from '@mui/joy/Typography';
import config from '../utils/config';
import { MRIView } from './MRIView';
import { SequenceForm } from './SequenceHandler';

export default function PatientPageMainView() {

    const params = useParams();

    switch(params.toolId) {
        case config.tools.dataview: 
            return (
                <Box sx={{ display: 'flex', width: '100%', height: '100%', bgcolor: '#000', alignItems: 'center' }}>
                    <MRIView />
                </Box>
            )
        case config.tools.configuration: 
            return <SequenceForm />
        default: 
            return <></>
    }
}