// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

// JobList.tsx is responsible for rendering a list of jobs to be executed.

import * as React from 'react';
import { useParams } from 'react-router-dom';
import { useMutation } from 'react-query';
import { useQuery } from 'react-query';
import Box from '@mui/joy/Box';
import Stack from '@mui/joy/Stack';
import List from '@mui/joy/List';
import ListDivider from '@mui/joy/ListDivider';
import Typography from '@mui/joy/Typography';
import IconButton from '@mui/joy/IconButton';
import AddSharpIcon from '@mui/icons-material/AddSharp';
import PlayCircleFilledSharpIcon from '@mui/icons-material/PlayCircleFilledSharp';

import JobModal from './JobModal'
import JobItem from './JobItem';

import { Job } from '../../interfaces/data.interface';
import { ComponentProps } from '../../interfaces/components.interface';
import { MRISequence } from '../../interfaces/mri-data.interface';
import { patientView } from '../../utils/size_vars';
// import { Device } from '../../interfaces/data.interface';
// import { Workflow } from '../../interfaces/data.interface';

import client from '../../client/exam-tree-queries';
import sequenceClient from '../../client/sequence-api';


function JobList({data: jobs, refetchParentData, isSelected}: ComponentProps<Job[]>) {

    const params = useParams();
    const [jobModalOpen, setJobModalOpen] = React.useState(false);

    // const { data: devices, isLoading: devicesLoading, isError: devicesError } = useQuery<Device[], Error>({
    //     queryKey: ['devices'],
    //     queryFn: () => deviceClient.getAll()
    // });

    const { data: sequences, isLoading: sequencesLoading, isError: sequencesError } = useQuery<MRISequence[], Error>({
        queryKey: ['sequences'],
        queryFn: () => sequenceClient.getAll()
    });

    const createJob = useMutation( async (data: Job) => {
        await client.jobService.create(data)
        .then(() => { refetchParentData() })
        .catch((err) => { console.log("Error during job creation: ", err) })
    })

    if (!isSelected) {
        // isSelected indicates if procedure is selected
        // To do: Add indicator, if no procedure is selected
        return (
            <div>
                Noting to view...
            </div>
        )
    }

    return (
        <Stack sx={{
            display: 'flex',
            width: '100%',
            height: '100%',
            bgcolor: 'background.componentBg',
            overflow: 'auto',
        }}>

            {/* Exam list header */}
            <Box sx={{ p: 1.5, display: 'flex', flexDirection:'row', justifyContent:'space-between', flexWrap: 'wrap', alignItems: 'center' }}>
                            
                <Box sx={{display: 'flex', alignItems: 'center', gap: 3}}>
                    <IconButton
                        aria-label='Acquire'
                        variant='plain' 
                        color='neutral'
                        sx={{ "--IconButton-size": "40px" }}
                        onClick={ () => {} }
                    >
                        <PlayCircleFilledSharpIcon/>
                    </IconButton>
                    <Typography level="h5"> Jobs </Typography>
                    {/* <Badge badgeContent={exams?.length} color="primary"/> */}
                </Box>
    
                <Box sx={{ display: 'flex', gap: 1 }}>
                    <IconButton 
                        variant='soft'
                        sx={{ "--IconButton-size": patientView.iconButtonSize }}
                        onClick={ () => { setJobModalOpen(true) }}
                        disabled={ sequences ? sequences.length === 0 : true }
                    >
                        <AddSharpIcon/>
                    </IconButton>
                </Box>

                <JobModal 
                    data={ null }
                    dialogOpen={ jobModalOpen }
                    setDialogOpen={ setJobModalOpen }
                    devices={[]}    // TODO: Fetch devices and pass them to modal
                    sequences={ sequences ? sequences : [] }
                    refetchParentData={ () => {} } // unused
                    handleModalSubmit={ (data: Job) => { createJob.mutate(data) }}
                />

            </Box>
    
            <ListDivider />  
    
            {/* List of exams */}
            <List sx={{ pt: 0 }}>
                {
                    // Check if exams are loading
                    !sequencesLoading && jobs.map((job, index) => (
                        <React.Fragment key={index}>
                            <JobItem
                                key={ index }
                                data={ job }
                                devices={ [] }
                                sequences={ sequences ? sequences : [] }
                                refetchParentData={ refetchParentData }
                            />
                            <ListDivider sx={{ m: 0 }} />
                        </React.Fragment>
                    ))
                }
            </List>

        </Stack>
    )
}

export default JobList;