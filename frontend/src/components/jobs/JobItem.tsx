// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

// JobItem.tsx is responsible for rendering a single job item in the job table.

import * as React from 'react';
import { useMutation } from 'react-query';
import { useNavigate } from 'react-router-dom';

import Stack from '@mui/joy/Stack';
import ListItem from '@mui/joy/ListItem';
import ListItemButton from '@mui/joy/ListItemButton';
import Typography from '@mui/joy/Typography';
import Menu from '@mui/joy/Menu';
import MenuItem from '@mui/joy/MenuItem';
import IconButton from '@mui/joy/IconButton';
import Badge from '@mui/joy/Badge';
import Button from '@mui/joy/Button';

import PlayCircleFilledSharpIcon from '@mui/icons-material/PlayCircleFilledSharp';
import MoreHorizIcon from '@mui/icons-material/MoreHoriz';

import JobModal from './JobModal'
import { Job } from '../../interfaces/data.interface'; 
import { JobComponentProps } from '../../interfaces/components.interface';
import client from '../../client/exam-tree-queries';


function JobItem ({data: job, devices, sequences, refetchParentData}: JobComponentProps) {

    // Context: Delete and edit options, anchor for context location
    const navigate = useNavigate();
    const [contextOpen, setContextOpen] = React.useState<boolean>(false);
    const [anchorEl, setAnchorEl] = React.useState<HTMLElement | null>(null);
    const [jobModalOpen, setJobModalOpen] = React.useState(false);

    const updateJob = useMutation( async (data: Job) => {
        await client.jobService.update(data.id, data)
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
                    
                    <Menu   
                        id='context-menu'
                        variant='plain'
                        anchorEl={anchorEl}
                        open={ contextOpen }
                        onClose={() => { setAnchorEl(null); setContextOpen(false); }}
                        sx={{ zIndex: 'snackbar' }}
                    >
                        <MenuItem key='edit' onClick={() => { setJobModalOpen(true); }}>
                            Edit
                        </MenuItem>
                        <MenuItem key='delete' onClick={() => { deleteThisJob.mutate() }}>
                            Delete
                        </MenuItem>
                    </Menu>

                    <JobModal 
                        data={ job }
                        dialogOpen={ jobModalOpen }
                        setDialogOpen={ setJobModalOpen }
                        devices={ devices }
                        sequences={ sequences }
                        refetchParentData={ () => {} } // unused
                        handleModalSubmit={ (data: Job) => { updateJob.mutate(data) }}
                    />

                <Button
                    variant="outlined"
                    color="neutral"
                    disabled={ job.sequence_id === "" }   // no sequence id
                    onClick={ () => { navigate(`${job.id}/seq`) }}
                >
                    { !job.sequence_id || job.sequence_id === "" ? "No sequence..." : `View ${sequences.find(x => x._id === job.sequence_id)?.name}` }
                </Button>
                
            </ListItemButton>   
        </ListItem>
    );
}

export default JobItem;