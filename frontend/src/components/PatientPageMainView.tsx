import * as React from 'react';
import { Outlet, useParams, Link as RouterLink } from 'react-router-dom';
import Box from '@mui/joy/Box';
import Typography from '@mui/joy/Typography';
import config from '../utils/config';
import { MRIView } from './MRIView';

export default function PatientPageMainView() {

    const params = useParams();

    switch(params.toolId) {
        case config.tools.dataview: 
            return <MRIView />
        case config.tools.configuration: 
            // return <SequenceForm />
            return <Typography level='h5'> Sequence Configuration </Typography>
        default: 
            return <></>
    }
}