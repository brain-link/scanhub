import * as React from 'react';
import { useParams } from 'react-router-dom';
import Box from '@mui/joy/Box';
import Stack from '@mui/joy/Stack';
import Typography from '@mui/joy/Typography';

import MRIView from '../viewer/dicom-view/DicomViewer';
import JobItem from './JobItem';
import { SequenceForm } from '../viewer/sequence-view/SequenceViewer';
// import JobList from '../JobList';

import { Job } from '../../interfaces/data.interface';
import { ItemComponentProps } from '../../interfaces/components.interface';



function JobViewController({data: jobs, onDelete, isSelected}: ItemComponentProps<Job[]>) {

    const params = useParams();

    if (!isSelected) {
        // isSelected indicates if procedure is selected
        // To do: Add indicator, if no procedure is selected
        return (
            <div>
                Noting to view...
            </div>
        )
    }

    switch(params.examViewId) {
        default:
            
            return (
                <Stack>
                    <Typography>Jobs</Typography>
                    {
                        jobs.map((job, index) => (
                            <JobItem
                                key={ index }
                                data={ job }
                                onDelete={ () => {} }
                                isSelected={ false }
                            />
                        ))
                    }
                </Stack>
            )

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
    }
}

export default JobViewController;