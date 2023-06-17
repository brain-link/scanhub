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

// import MRIView from '../viewer/dicom-view/DicomViewer';
import JobItem from './JobItem';
// import { SequenceForm } from '../viewer/sequence-view/SequenceViewer';


import { Job } from '../../interfaces/data.interface';
import { ComponentProps } from '../../interfaces/components.interface';

import client from '../../client/exam-tree-queries';
import sequenceClient from '../../client/mri-queries';

import { Device } from '../../interfaces/data.interface';
// import { Workflow } from '../../interfaces/data.interface';
import { MRISequence } from '../../interfaces/mri-data.interface';
import { patientView } from '../../utils/size_vars';


function JobView({data: jobs, refetchParentData, isSelected}: ComponentProps<Job[]>) {

    const params = useParams();

    const newJob: Job = {
        id: 0,
        type: "Enter job type...",
        comment: "Comment",
        procedure_id: Number(params.procedureId),
        sequence_id: "",
        workflow_id: null,
        device_id: 0,
        datetime_created: new Date(),
    };

    // const { data: devices, isLoading: devicesLoading, isError: devicesError } = useQuery<Device[], Error>({
    //     queryKey: ['devices'],
    //     queryFn: () => deviceClient.getAll()
    // });

    const { data: sequences, isLoading: sequencesLoading, isError: sequencesError } = useQuery<MRISequence[], Error>({
        queryKey: ['sequences'],
        queryFn: () => sequenceClient.getAll()
    });


    React.useEffect( () => {
        console.log(jobs)
    }, [jobs])



    // const { data: workflows, isLoading: workflowLoading, isError: workflowError } = useQuery<Workflow[], Error>({
    //     queryKey: ['workflows'],
    //     queryFn: () => client.workflowService.getAll()
    // });

    const createJob = useMutation( async () => {
        // Add a new empty job, editable in job-item component
        // setNewJob({...newJob, ["procedure_id"]: Number(params.procedureId)});
        console.log("New job: ", newJob)
        console.log("New job procedure id: ", newJob.procedure_id)
        await client.jobService.create(newJob)
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

    if (sequencesLoading) {
        return (
            <div> Loading workflows and devices...</div>
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
                    <Typography level="h5"> Jobs </Typography>
                    {/* <Badge badgeContent={exams?.length} color="primary"/> */}
                </Box>
    
                <Box sx={{ display: 'flex', gap: 1 }}>
                    <IconButton 
                        variant='soft'
                        sx={{ "--IconButton-size": patientView.iconButtonSize }}
                        onClick={() => createJob.mutate()}
                    >
                        <AddSharpIcon/>
                    </IconButton>
                </Box>

                {/* <ExamCreateModal 
                    dialogOpen={ newExamDialogOpen }
                    setDialogOpen={ setNewExamDialogOpen }
                    onCreated={ refetchExams }
                /> */}

            </Box>
    
            <ListDivider />  
    
            {/* List of exams */}
            <List sx={{ pt: 0 }}>
                {
                    // Check if exams are loading
                    jobs.map((job, index) => (
                        <React.Fragment key={index}>
                            <JobItem
                                key={ index }
                                job={ job }
                                devices={ [] }
                                sequences={ sequences ? sequences : [] }
                                // Forward onDelete function which refetches the records
                                refetchParentData={ refetchParentData }
                            />
                            <ListDivider sx={{ m: 0 }} />
                        </React.Fragment>
                    ))
                }
            </List>

            {/* {
                jobs.map((job, index) => (
                    <JobItem
                        key={ index }
                        job={ job }
                        devices={ [] }
                        sequences={ sequences ? sequences : [] }
                        // Forward onDelete function which refetches the records
                        refetchParentData={ refetchParentData }
                    />
                ))
            } */}
            {/* <IconButton
                variant='soft'
                onClick={ () => createJob.mutate() }
            >
                <AddCircleOutlineSharpIcon/>
            </IconButton> */}
        </Stack>
    )
}

export default JobView;