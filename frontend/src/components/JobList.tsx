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
import UploadFileSharpIcon from '@mui/icons-material/UploadFileSharp';

import JobModal from './JobModal'
import JobItem from './JobItem';
import SequenceUpload from './SequenceUpload';
import AlertItem from './AlertItem';

import { Job } from '../interfaces/data.interface';
import { ComponentProps, Alerts } from '../interfaces/components.interface';
import { MRISequence } from '../interfaces/mri-data.interface';
import { patientView } from '../utils/size_vars';
import { Device } from '../interfaces/data.interface';
// import { Workflow } from '../interfaces/data.interface';

import client from '../client/exam-tree-queries';
import deviceClient from '../client/device-api';
import sequenceClient from '../client/sequence-api';


function JobList({data: jobs, refetchParentData, isSelected: isVisible}: ComponentProps<Job[]>) {

    const params = useParams();
    const [jobModalOpen, setJobModalOpen] = React.useState(false);
    const [sequenceModalOpen, setSequenceModalOpen] = React.useState(false);

    const { data: devices, isLoading: devicesLoading, isError: devicesError } = useQuery<Device[], Error>({
        queryKey: ['devices'],
        queryFn: () => deviceClient.getAll()
    });

    // const { data: workflows, isLoading: workflowsLoading, isError: workflowsError } = useQuery<Workflow[], Error>({
    //     queryKey: ['workflows'],
    //     queryFn: () => deviceClient.getAll()
    // });

    const { data: sequences, refetch: refetchSequences, isLoading: sequencesLoading, isError: sequencesError } = useQuery<MRISequence[], Error>({
        queryKey: ['sequences'],
        queryFn: () => sequenceClient.getAll()
    });

    const createJob = useMutation( async (data: Job) => {
        await client.jobService.create(data)
        .then(() => { refetchParentData() })
        .catch((err) => { console.log("Error during job creation: ", err) })
    })

    React.useEffect(() => {
        console.log("DEVICES: ", devices)
    }, [devices])

    if (sequencesError) {
        return (
            <Stack sx={{ p: 10, display: 'flex', width: '100%', height: '100%', bgcolor: 'background.componentBg', justifyContent: 'center'}}>
                <AlertItem 
                    title="Error loading sequences"
                    info="Sequences could not be loaded, an error occured."
                    type={ Alerts.Danger }
                />
            </Stack>
        )
    }

    if (devicesError) {
        return (
            <Stack sx={{ p: 10, display: 'flex', width: '100%', height: '100%', bgcolor: 'background.componentBg', justifyContent: 'center'}}>
                <AlertItem 
                    title="Error: No devices"
                    info="Devices could not be loaded, an error occured."
                    type={ Alerts.Danger }
                />
            </Stack>
        )
    }

    return (
        <Stack sx={{
            display: 'flex',
            width: '100%',
            height: '100%',
            bgcolor: 'background.componentBg',
            overflow: 'auto'
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
                    <Typography level="title-md"> Jobs </Typography>
                    {/* <Badge badgeContent={exams?.length} color="primary"/> */}
                </Box>
    
                <Box sx={{ display: 'flex', gap: 1 }}>

                    {/* Sequence upload */}
                    <IconButton 
                        variant='soft'
                        sx={{ "--IconButton-size": patientView.iconButtonSize }}
                        onClick={ () => { setSequenceModalOpen(true) }}
                    >
                        <UploadFileSharpIcon />
                    </IconButton>

                    {/* Add job */}
                    <IconButton 
                        variant='soft'
                        sx={{ "--IconButton-size": patientView.iconButtonSize }}
                        onClick={ () => { setJobModalOpen(true) }}
                        disabled={ params.procedureId === undefined }
                    >
                        <AddSharpIcon/>
                    </IconButton>
                </Box>

                <SequenceUpload
                    fetchSequences={ () => refetchSequences() }
                    dialogOpen={ sequenceModalOpen }
                    setDialogOpen={ setSequenceModalOpen }
                />

                <JobModal 
                    data={ null }
                    dialogOpen={ jobModalOpen }
                    setDialogOpen={ setJobModalOpen }
                    devices={ devices ? devices : [] }    // TODO: Fetch devices and pass them to modal
                    sequences={ sequences ? sequences : [] }
                    refetchParentData={ () => {} } // unused
                    handleModalSubmit={ (data: Job) => { createJob.mutate(data) }}
                />

            </Box>
    
            <ListDivider />  

    
            {/* List of exams */}
            <List sx={{ pt: 0 }}>

                {
                    // Notification to display when no jobs are present
                    !isVisible && <Stack sx={{ p: 10, pt: 2, pb: 0, display: 'flex', bgcolor: 'background.componentBg', justifyContent: 'center'}}>
                        <AlertItem 
                            title="Nothing to show..."
                            info="Please select an exam and a procedure to view the jobs."
                            type={ Alerts.Neutral }
                        />
                    </Stack>
                }

                {
                    // Check device list
                    !(devices && devices.length > 0) && 
                    <Stack sx={{ p: 10, pt: 2, pb: 0, display: 'flex', width: '100%', bgcolor: 'background.componentBg', justifyContent: 'center'}}>
                        <AlertItem 
                            title={devicesLoading ? "Loading devices..." : "No device found"}
                            info={!devicesLoading ? "Could not find any registered device, please register a device first." : undefined}
                            type={ Alerts.Warning }
                        />
                    </Stack>
                }

                {
                    // Check sequence list
                    !(sequences && sequences.length > 0) && 
                    <Stack sx={{ p: 10, pt: 2, pb: 0, display: 'flex', width: '100%', bgcolor: 'background.componentBg', justifyContent: 'center'}}>
                        <AlertItem 
                            title={sequencesLoading ? "Loading sequences..." : "No sequence found"}
                            info={!sequencesLoading ? "Could not find any sequence, please upload a sequence first." : undefined}
                            type={ Alerts.Warning }
                        />
                    </Stack>
                }

                {
                    // Check if exams are loading
                    !sequencesLoading && jobs.map((job, index) => (
                        <React.Fragment key={index}>
                            <JobItem
                                key={ index }
                                data={ job }
                                devices={ devices ? devices : [] }
                                sequences={ sequences ? sequences : [] }
                                refetchParentData={ refetchParentData }
                            />

                            {/* When not using card items, divided is required to separate jobs */}
                            {/* <ListDivider sx={{ m: 0 }} /> */}
                        </React.Fragment>
                    ))
                }
            </List>

        </Stack>
    )
}

export default JobList;