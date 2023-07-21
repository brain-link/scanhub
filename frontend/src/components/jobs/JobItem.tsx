// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

// JobItem.tsx is responsible for rendering a single job item in the job table.

import * as React from 'react';
import { useMutation } from 'react-query';
import { useParams, useNavigate, useLocation } from 'react-router-dom';

import Card from '@mui/joy/Card';
import Box from '@mui/joy/Box';
import Stack from '@mui/joy/Stack';
import CardContent from '@mui/joy/CardContent';
import CardOverflow from '@mui/joy/CardOverflow';
import ListItem from '@mui/joy/ListItem';
import ListItemButton from '@mui/joy/ListItemButton';
import ListItemDecorator from '@mui/joy/ListItemDecorator';
import Typography from '@mui/joy/Typography';
import Menu from '@mui/joy/Menu';
import MenuItem from '@mui/joy/MenuItem';
import Divider from '@mui/joy/Divider';
import Select from '@mui/joy/Select';
import Option from '@mui/joy/Option';
import IconButton from '@mui/joy/IconButton';
import Badge from '@mui/joy/Badge';
import FormControl from '@mui/joy/FormControl';

// Icons
import PendingActionsSharpIcon from '@mui/icons-material/PendingActionsSharp';
import PlayCircleFilledSharpIcon from '@mui/icons-material/PlayCircleFilledSharp';
import GraphicEqSharpIcon from '@mui/icons-material/GraphicEqSharp';
import MoreHorizIcon from '@mui/icons-material/MoreHoriz';

import { Job } from '../../interfaces/data.interface'; 
import { JobComponentProps } from '../../interfaces/components.interface';
import client from '../../client/exam-tree-queries';



function JobItem ({job, devices, sequences, refetchParentData}: JobComponentProps) {

    // Context: Delete and edit options, anchor for context location
    const [contextOpen, setContextOpen] = React.useState<boolean>(false);
    const [anchorEl, setAnchorEl] = React.useState<HTMLElement | null>(null);
    const navigate = useNavigate();
    const location = useLocation();

    const [jobUpdate, setJobUpdate] = React.useState<Job>(job);
    
    // TODO: Use update function to update job, deep clone by newJob = { ...job }
    // What is the fastest way? Update db on every change or create a deep copy, work on deep copy (update values here)
    // and modify db only when focus changed to different component?

    const updateJob = useMutation( async () => {
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

    React.useEffect(() => {
        updateJob.mutate();
    }, [jobUpdate])

    // TODO: Add controls

    // TODO: Implementation of sequence upload

    // TODO: Use devices and workflows in selectors 

    return (
        <ListItem>
            <ListItemButton 
                id="job-item"
                variant="plain"
                sx={{
                    alignItems: 'center',
                    gap: 3,
                }}
            >
                {/* <ListItemDecorator sx={{ align: 'center', justify: 'center'}}>
                    <PendingActionsSharpIcon />
                </ListItemDecorator> */}

                <Badge color="success"  sx={{ml: 3}} />

                <IconButton
                    aria-label='Acquire'
                    variant='plain' 
                    color='neutral'
                    sx={{ "--IconButton-size": "40px" }}
                    onClick={ () => {} }
                >
                    <PlayCircleFilledSharpIcon/>
                </IconButton>

                {/* Card header */}
                {/* <Box sx={{ display: 'flex', flexDirection: 'row', gap: 4, justifyContent: 'space-between', align: 'center' }}> */}

                    {/* <Input 
                        type="string"
                        variant="plain"
                        name="type"
                        defaultValue={ job.type === "" ? "Enter type..." : job.type }
                        disabled={ job.is_acquired }
                        onChange={ (e) => setJobUpdate({...jobUpdate, [e.target.name]: e.target.value}) }
                        onBlur={ () => updateJob.mutate() }
                    /> */}



                    {/* <Input 
                        type="string"
                        variant="plain"
                        name="comment"
                        defaultValue={ !job.comment || job.comment === "" ? "Enter comment..." : job.comment }
                        disabled={ job.is_acquired }
                        onChange={ (e) => setJobUpdate({...jobUpdate, [e.target.name]: e.target.value}) }
                        onBlur={ () => updateJob.mutate() }
                    /> */}
                
                {/* <Stack direction='row' spacing={4} sx={{alignItems: 'center'}}> */}

                <Stack direction='column'>
                    <Typography level="body1" textColor="text.primary">{job.type}</Typography>
                    <Typography level="body1" textColor="text.secondary">{job.comment}</Typography>
                </Stack>

                <Stack direction='column'>
                    <Typography level="body2" textColor="text.tertiary">{ `Created: ${new Date(job.datetime_created).toDateString()}` }</Typography>
                    <Typography level="body2" textColor="text.tertiary">{ `Updated: ${job.datetime_updated ? new Date(job.datetime_updated).toDateString() : '-'}` }</Typography>
                </Stack>

                {/* Job interactions */}
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
                        onClick={ () => { 
                            console.log(`${location.pathname}/${job.id}/seq`); 
                            // navigate(`${location.pathname}/${job.id}/seq`);
                            navigate(`${job.id}/seq`)
                        }}
                    >
                        <GraphicEqSharpIcon/>
                    </IconButton>

                    {/* </Stack> */}
                    
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

                {/* </Box> */}
            
                
                {/* Configuration: Device, Workflow, Sequence */}

                <Select placeholder="Device">
                    <Option value="device" >
                        Scanner 1: ULF-MRI
                    </Option>
                </Select>
                <Select
                    placeholder="Sequence"
                    onChange={(
                        event: React.SyntheticEvent | null,
                        newValue: string | null
                    ) => { setJobUpdate({...jobUpdate, ["sequence_id"]: newValue ? newValue : "" }) }}
                >
                    {
                        sequences?.map( (sequence, index) => (
                            <Option key={index} value={sequence._id}>
                                { sequence.name }
                            </Option>
                        ))
                    }
                </Select>
                <Select placeholder="Workflow">
                    <Option value="workflow">
                        Reco-Cartesian
                    </Option>
                </Select>

            </ListItemButton>   
        </ListItem>
    );
}

export default JobItem;