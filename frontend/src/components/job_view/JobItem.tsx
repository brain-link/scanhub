import * as React from 'react';
import { useMutation } from 'react-query';
import { Link as RouterLink } from 'react-router-dom';
import { useParams } from 'react-router-dom';

import Card from '@mui/joy/Card';
import Box from '@mui/joy/Box';
import Stack from '@mui/joy/Stack';
import CardContent from '@mui/joy/CardContent';
import CardOverflow from '@mui/joy/CardOverflow';
import Typography from '@mui/joy/Typography';
import Divider from '@mui/joy/Divider';
import Select from '@mui/joy/Select';
import Option from '@mui/joy/Option';
import IconButton from '@mui/joy/IconButton';
import Input from '@mui/joy/Input';
import FormControl from '@mui/joy/FormControl';

// Icons
import PendingActionsSharpIcon from '@mui/icons-material/PendingActionsSharp';
import PlayCircleFilledSharpIcon from '@mui/icons-material/PlayCircleFilledSharp';
import GraphicEqSharpIcon from '@mui/icons-material/GraphicEqSharp';
import MoreHorizIcon from '@mui/icons-material/MoreHoriz';

import { Job } from '../../interfaces/data.interface'; 
import { JobComponentProps } from '../../interfaces/components.interface';
import { JobApiService } from '../../client/queries';



function JobItem ({job, devices, workflows, refetchParentData}: JobComponentProps) {

    const params = useParams();
    const jobClient = new JobApiService();

    const updateJob = useMutation( async (jobUpdate: Job) => {
        await jobClient.update(job.id, jobUpdate)
        .then( () => { refetchParentData() } )
        .catch( (err) => { console.log("Error on job update: ", err) })
    })

    // TODO: Use update function to update job, deep clone by newJob = { ...job }
    // What is the fastest way? Update db on every change or create a deep copy, work on deep copy (update values here)
    // and modify db only when focus changed to different component?

    // TODO: Add controls

    // TODO: Implementation of sequence upload

    return (
        <Card
            orientation="horizontal"
            variant="outlined"
            sx={{ display: 'flex', bgcolor: 'background.body' }}
        >
            <CardOverflow sx={{ p: 2, display: 'flex', alignItems: 'center' }}>
                <PendingActionsSharpIcon/>
            </CardOverflow>
            <Divider />
            <CardContent sx={{ px: 2, gap: 1 }}>

                {/* Card header */}
                <Box sx={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' }}>

                    <FormControl
                        onChange={ () => {} }
                    >
                        <Input 
                            type="string"
                            variant="plain"
                            value={ job.type === "" ? "Enter type..." : job.type }
                            disabled={ job.is_acquired }
                        />
                    </FormControl>
                    
                    {/* Job interactions */}
                    <Stack direction='row'>
                        <IconButton 
                            aria-label='Options'
                            variant='plain' 
                            color='neutral'
                            sx={{ "--IconButton-size": "40px" }}
                            onClick={ () => {} }
                        >
                            <MoreHorizIcon/>
                        </IconButton>
                        <IconButton 
                            aria-label='Show sequence'
                            variant='plain' 
                            color='neutral'
                            sx={{ "--IconButton-size": "40px" }}
                            onClick={ () => {} }
                        >
                            <GraphicEqSharpIcon/>
                        </IconButton>
                        <IconButton
                            aria-label='Acquire'
                            variant='plain' 
                            color='neutral'
                            sx={{ "--IconButton-size": "40px" }}
                            onClick={ () => {} }
                        >
                            <PlayCircleFilledSharpIcon/>
                        </IconButton>
                    </Stack>
                    

                </Box>
            
                
                <FormControl
                    onChange={ () => {} }
                >
                    <Input 
                        type="string"
                        variant="plain"
                        value={ !job.comment || job.comment === "" ? "Enter comment..." : job.comment }
                        disabled={ job.is_acquired }
                    />
                </FormControl>

                {/* Configuration: Device, Workflow, Sequence */}
                <Stack direction='row' spacing={2}>
                    <Select placeholder="Device">
                        <Option>Device 1</Option>
                    </Select>
                    <Select placeholder="Sequence">
                        <Option>Sequence 1</Option>
                    </Select>
                    <Select placeholder="Workflow">
                        <Option>Workflow 1</Option>
                    </Select>
                </Stack>

            </CardContent>
            <Divider />
            <CardOverflow
                variant="soft"
                color={ job.is_acquired ? "success" :  "info" }
                sx={{
                    px: 0.2,
                    writingMode: 'vertical-rl',
                    textAlign: 'center',
                    fontSize: 'xs2',
                    fontWeight: 'xl2',
                    letterSpacing: '1px',
                    textTransform: 'uppercase',
                  }}
            >
                { job.is_acquired ? "Done" : "Pending" }
            </CardOverflow>
        </Card>
    );
}

export default JobItem;