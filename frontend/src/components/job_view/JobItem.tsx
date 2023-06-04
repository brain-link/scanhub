// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

// JobItem.tsx is responsible for rendering a single job item in the job table.

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
import Menu from '@mui/joy/Menu';
import MenuItem from '@mui/joy/MenuItem';
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
import client from '../../client/queries';



function JobItem ({job, devices, workflows, refetchParentData}: JobComponentProps) {

    // Context: Delete and edit options, anchor for context location
    const [contextOpen, setContextOpen] = React.useState<boolean>(false);
    const [anchorEl, setAnchorEl] = React.useState<HTMLElement | null>(null);

    const [jobUpdate, setJobUpdate] = React.useState<Job>(job);
    
    // TODO: Use update function to update job, deep clone by newJob = { ...job }
    // What is the fastest way? Update db on every change or create a deep copy, work on deep copy (update values here)
    // and modify db only when focus changed to different component?

    const updateJob = useMutation( async () => {
        console.log("JOB UPDATE", jobUpdate)
        console.log("Procedure id: ", job.procedure_id)
        await client.jobService.update(job.id, jobUpdate)
        .then( () => { refetchParentData() } )
        .catch( (err) => { console.log("Error on job update: ", err) })
    })


    const deleteThisJob = useMutation(async () => {
        await client.jobService.delete(job.id)
        .then(() => { 
            setContextOpen(false); 
            refetchParentData(); 
        })
    })

    // TODO: Add controls

    // TODO: Implementation of sequence upload

    // TODO: Use devices and workflows in selectors 

    return (
        <Card
            orientation="horizontal"
            variant="outlined"
            sx={{ display: 'flex', bgcolor: 'background.body' }}
        >
            <CardOverflow sx={{ p: 2, display: 'flex', alignItems: 'center' }}>
                <PendingActionsSharpIcon/>
            </CardOverflow>

            <CardContent sx={{ px: 2, gap: 1 }}>

                {/* Card header */}
                <Box sx={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' }}>

                    <Input 
                        type="string"
                        variant="plain"
                        name="type"
                        defaultValue={ job.type === "" ? "Enter type..." : job.type }
                        disabled={ job.is_acquired }
                        onChange={ (e) => setJobUpdate({...jobUpdate, [e.target.name]: e.target.value}) }
                        onBlur={ () => updateJob.mutate() }
                    />
                    
                    {/* Job interactions */}
                    <Stack direction='row'>
                        <IconButton 
                            aria-label='Options'
                            variant='plain' 
                            color='neutral'
                            sx={{ "--IconButton-size": "40px" }}
                            onClick={ (e) => { e.preventDefault(); setAnchorEl(e.currentTarget); setContextOpen(true); } }
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
                    
                    <Menu   
                        id='context-menu'
                        variant='plain'
                        anchorEl={anchorEl}
                        open={ contextOpen }
                        onClose={() => { setAnchorEl(null); setContextOpen(false); }}
                        sx={{ zIndex: 'snackbar' }}
                    >
                        <MenuItem key='edit' onClick={() => { console.log('To be implemented...') }}>
                            Edit
                        </MenuItem>
                        <MenuItem key='delete' onClick={() => { deleteThisJob.mutate() }}>
                            Delete
                        </MenuItem>
                    </Menu>

                </Box>
            
                <Box sx={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' }}>

                    <Input 
                        type="string"
                        variant="plain"
                        name="comment"
                        defaultValue={ !job.comment || job.comment === "" ? "Enter comment..." : job.comment }
                        disabled={ job.is_acquired }
                        onChange={ (e) => setJobUpdate({...jobUpdate, [e.target.name]: e.target.value}) }
                        onBlur={ () => updateJob.mutate() }
                    />

                    <Stack>
                        <Typography level="body2" textColor="text.tertiary">{ `Created: ${new Date(job.datetime_created).toDateString()}` }</Typography>
                        <Typography level="body2" textColor="text.tertiary">{ `Updated: ${job.datetime_updated ? new Date(job.datetime_updated).toDateString() : '-'}` }</Typography>
                    </Stack>

                </Box>
                

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

            <CardOverflow
                variant="soft"
                color={ job.is_acquired ? "success" :  "primary" }
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