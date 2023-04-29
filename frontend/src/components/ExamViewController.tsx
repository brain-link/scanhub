import * as React from 'react';
import { useParams } from 'react-router-dom';
import Box from '@mui/joy/Box';


import MRIView from '../viewer/DicomViewer';
import { SequenceForm } from '../viewer/SequenceViewer';
import JobList from './JobList';


function ExamViewController() {

    const params = useParams();

    switch(params.examViewId) {
        case 'dicom-view': 
            return (
                <Box sx={{ display: 'flex', width: '100%', height: '100%', bgcolor: '#000', alignItems: 'center' }}>
                    <MRIView procedureId={params.procedureId ? params.procedureId : ""}/>
                </Box>
            )
        case 'sequence-view': 
            return (
                <Box sx={{ display: 'flex', width: '100%', height: '100%', alignItems: 'center', justifyContent: 'center' }}>
                    <SequenceForm />
                </Box>
            )
        default: 
            return (
                <JobList />
            )
    }
}

export default ExamViewController;