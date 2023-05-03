import * as React from 'react';
import { useParams } from 'react-router-dom';
import { useMutation } from 'react-query';
import { useQuery } from 'react-query';
import Box from '@mui/joy/Box';
import Stack from '@mui/joy/Stack';
import Typography from '@mui/joy/Typography';
import IconButton from '@mui/joy/IconButton';
import AddCircleOutlineSharpIcon from '@mui/icons-material/AddCircleOutlineSharp';

import MRIView from '../viewer/dicom-view/DicomViewer';
import JobItem from './JobItem';
import { SequenceForm } from '../viewer/sequence-view/SequenceViewer';


import { Job } from '../../interfaces/data.interface';
import { ComponentProps } from '../../interfaces/components.interface';

import { DeviceApiService } from '../../client/queries';
import { WorkflowApiService } from '../../client/queries';
import { JobApiService } from '../../client/queries';

import { Device } from '../../interfaces/data.interface';
import { Workflow } from '../../interfaces/data.interface';


function JobViewController({data: jobs, refetchParentData, isSelected}: ComponentProps<Job[]>) {

    const params = useParams();

    const jobClient = new JobApiService();
    const deviceClient = new DeviceApiService();
    const workflowClient = new WorkflowApiService();

    const [newJob, setNewJob] = React.useState<Job>({
        id: 0,
        type: "Enter job type...",
        comment: "Comment",
        procedure_id: Number(params.procedureId),
        sequence_id: "",
        workflow_id: null,
        device_id: 0,
        datetime_created: new Date(),
    });

    // const { data: devices, isLoading: devicesLoading, isError: devicesError } = useQuery<Device[], Error>({
    //     queryKey: ['devices'],
    //     queryFn: () => deviceClient.getAll()
    // });

    const { data: workflows, isLoading: workflowLoading, isError: workflowError } = useQuery<Workflow[], Error>({
        queryKey: ['workflows'],
        queryFn: () => workflowClient.getAll()
    });

    const createJob = useMutation( async () => {
        // Add a new empty job, editable in job-item component
        // setNewJob({...newJob, ["procedure_id"]: Number(params.procedureId)});
        console.log("New job: ", newJob)
        await jobClient.create(newJob)
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

    switch(params.examViewId) {
        default:

            if (workflowLoading) {
                return (
                    <div> Loading workflows and devices...</div>
                )
            }

            if (workflowError) {
                return (
                    <div>Error loading devices/workflows...</div>
                )
            }

            return (
                <Stack sx={{
                    display: 'flex',
                    p: 2,
                    rowGap: 2,
                    width: '100%',
                    height: '100%',
                    bgcolor: 'background.componentBg',
                    alignItems: 'center',
                    justifyContent: 'flex-start',
                    overflow: 'auto',
                }}>
                    <Typography>Jobs</Typography>
                    {
                        jobs.map((job, index) => (
                            <JobItem
                                key={ index }
                                job={ job }
                                devices={ [] }
                                workflows={ workflows ? workflows : [] }
                                // Forward onDelete function which refetches the records
                                refetchParentData={ refetchParentData }
                            />
                        ))
                    }
                    <IconButton
                        variant='soft'
                        onClick={ () => createJob.mutate() }
                    >
                        <AddCircleOutlineSharpIcon/>
                    </IconButton>
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