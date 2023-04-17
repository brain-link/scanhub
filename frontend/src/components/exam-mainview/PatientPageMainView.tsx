import * as React from 'react';
import { useParams } from 'react-router-dom';
import Box from '@mui/joy/Box';
import config from '../../utils/config';
import MRIView from '../viewer/DicomViewer';
import { SequenceForm } from '../SequenceHandler';


export default function PatientPageMainView() {

    const params = useParams();

    switch(params.toolId) {
        case config.tools.dataview: 
            return (
                <Box sx={{ display: 'flex', width: '100%', height: '100%', bgcolor: '#000', alignItems: 'center' }}>
                    <MRIView recordId={params.recordId ? params.recordId : ""}/>
                </Box>
            )
        case config.tools.configuration: 
            return (
                <Box sx={{ display: 'flex', width: '100%', height: '100%', alignItems: 'center', justifyContent: 'center' }}>
                    <SequenceForm />
                </Box>
            )
        default: 
            return <></>
    }
}