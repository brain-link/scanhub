// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
// JobItem.tsx is responsible for rendering a single job item in the job table.
import MoreHorizIcon from '@mui/icons-material/MoreHoriz'
import PlayCircleFilledSharpIcon from '@mui/icons-material/PlayCircleFilledSharp'
import Box from '@mui/joy/Box'
import Button from '@mui/joy/Button'
// import Badge from '@mui/joy/Badge';
import Card from '@mui/joy/Card'
import IconButton from '@mui/joy/IconButton'
import ListItem from '@mui/joy/ListItem'
import ListItemContent from '@mui/joy/ListItemContent'
import Menu from '@mui/joy/Menu'
import MenuItem from '@mui/joy/MenuItem'
import Modal from '@mui/joy/Modal'
import ModalClose from '@mui/joy/ModalClose'
import ModalDialog from '@mui/joy/ModalDialog'
import Stack from '@mui/joy/Stack'
import Typography from '@mui/joy/Typography'
import * as React from 'react'
import { useMutation } from 'react-query'

import acquisitionControl from '../client/acquisition-api'
import client from '../client/exam-tree-queries'
import { JobComponentProps } from '../interfaces/components.interface'
import { Job } from '../interfaces/data.interface'
import { navigation } from '../utils/size_vars'
import DeviceItem from './_Device'
import JobModal from './_JobModal'
import SequenceViewer from './SequencePlot'

function JobItem({ data: job, devices, sequences, refetchParentData }: JobComponentProps) {
  // Context: Delete and edit options, anchor for context location
  const [contextOpen, setContextOpen] = React.useState<boolean>(false)
  const [anchorEl, setAnchorEl] = React.useState<HTMLElement | null>(null)
  const [jobModalOpen, setJobModalOpen] = React.useState(false)
  const [seqModalOpen, setSeqModalOpen] = React.useState(false)

  const updateJob = useMutation(async (data: Job) => {
    await client.jobService
      .update(data.id, data)
      .then(() => {
        refetchParentData()
      })
      .catch((err) => {
        console.log('Error on job update: ', err)
      })
  })

  const deleteThisJob = useMutation(async () => {
    await client.jobService.delete(job.id).then(() => {
      setContextOpen(false)
      refetchParentData()
    })
  })

  const handleAcquire = async () => {
    console.log('Starting acquisition...')
    await acquisitionControl.post(job).then((response) => {
      // Debug...
      console.log('Acquisition control response... ', response)
    })
  }

  return (
    <Card variant='soft' sx={{ m: 1, p: 0.5 }}>
      <ListItem
        startAction={
          <IconButton
            aria-label='Acquire'
            variant='plain'
            color='neutral'
            sx={{ '--IconButton-size': '40px' }}
            onClick={handleAcquire}
          >
            <PlayCircleFilledSharpIcon />
          </IconButton>
        }
      >
        <ListItemContent sx={{ overflow: 'auto' }}>
          <Stack gap={3} direction='row' sx={{ ml: 8, alignItems: 'center' }}>
            {/* <Badge color="success"  sx={{ml: 3}} /> */}

            <Stack direction='column'>
              <Typography noWrap level='body-md'>
                {job.type}
              </Typography>
              <Typography noWrap level='body-md'>
                {job.comment}
              </Typography>
              {/* <Typography noWrap level="body-md">{`Records: ${job.records ? job.records.length : "-"}`}</Typography> */}
              {/* </Stack>

                    <Stack direction='column'> */}
              <Typography noWrap level='body-md' textColor='text.tertiary'>{`Created: ${new Date(
                job.datetime_created,
              ).toDateString()}`}</Typography>
              {/* <Typography noWrap level="body-md" textColor="text.tertiary">{ `Updated: ${job.datetime_updated ? new Date(job.datetime_updated).toDateString() : '-'}` }</Typography> */}
              <Typography noWrap level='body-md' textColor='text.tertiary'>
                {`Last record: ${
                  job.records && job.records.length > 0
                    ? new Date(job.records[job.records.length - 1].datetime_created).toDateString() +
                      ` (${job.records ? job.records.length : '-'})`
                    : '-'
                }`}
              </Typography>
            </Stack>

            <DeviceItem device={devices.find((x) => x.id === job.device_id)} />

            <Button
              variant='outlined'
              color='neutral'
              disabled={job.sequence_id === ''} // no sequence id
              onClick={() => setSeqModalOpen(true)}
            >
              <Stack>
                <Typography level='body-md'>Sequence</Typography>
                <Typography level='body-md'>
                  {job.sequence_id ? sequences.find((x) => x._id === job.sequence_id)?.name : '-'}
                </Typography>
              </Stack>
            </Button>

            <Box sx={{ display: 'flex', flexGrow: 1, justifyContent: 'flex-end' }}>
              <IconButton
                aria-label='Options'
                variant='plain'
                color='neutral'
                sx={{ '--IconButton-size': '40px' }}
                onClick={(e) => {
                  e.preventDefault()
                  setAnchorEl(e.currentTarget)
                  setContextOpen(true)
                }}
              >
                <MoreHorizIcon />
              </IconButton>
            </Box>
          </Stack>
        </ListItemContent>

        {/* Job interaction menu */}
        <Menu
          id='context-menu'
          variant='plain'
          anchorEl={anchorEl}
          open={contextOpen}
          onClose={() => {
            setAnchorEl(null)
            setContextOpen(false)
          }}
          sx={{ zIndex: 'snackbar' }}
        >
          <MenuItem
            key='edit'
            onClick={() => {
              setJobModalOpen(true)
            }}
          >
            Edit
          </MenuItem>
          <MenuItem
            key='delete'
            onClick={() => {
              deleteThisJob.mutate()
            }}
          >
            Delete
          </MenuItem>
        </Menu>

        {/* Job create/edit modaal */}
        <JobModal
          data={job}
          dialogOpen={jobModalOpen}
          setDialogOpen={setJobModalOpen}
          devices={devices}
          sequences={sequences}
          refetchParentData={() => {}} // unused
          handleModalSubmit={(data: Job) => {
            updateJob.mutate(data)
          }}
        />

        {/* Sequence viewer modal */}
        <Modal open={seqModalOpen} onClose={() => setSeqModalOpen(false)} sx={{ mt: navigation.height }}>
          <ModalDialog layout='fullscreen' variant='plain'>
            <ModalClose />
            <SequenceViewer sequence_id={job.sequence_id} />
          </ModalDialog>
        </Modal>
      </ListItem>
    </Card>
  )
}

export default JobItem
