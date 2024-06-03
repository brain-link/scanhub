// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
// ExamItem.tsx is responsible for rendering a single exam item in the exam list of the patient view.

import * as React from 'react'
import { useMutation } from 'react-query'
import { useParams } from 'react-router-dom'
import { useNavigate } from 'react-router-dom'

// Mui joy components
import IconButton from '@mui/joy/IconButton'
import ListItem from '@mui/joy/ListItem'
import ListItemDecorator from '@mui/joy/ListItemDecorator'
import ListItemContent from '@mui/joy/ListItemContent'
import Menu from '@mui/joy/Menu'
import MenuItem from '@mui/joy/MenuItem'
import Typography from '@mui/joy/Typography'

// Icons
import MoreHorizIcon from '@mui/icons-material/MoreHoriz'
import SnippetFolderSharpIcon from '@mui/icons-material/SnippetFolderSharp'

// Sub-components, interfaces, client
import { ComponentProps } from '../interfaces/components.interface'
import { WorkflowOut } from '../generated-client/exam'
import { workflowsApi } from '../api'


function WorkflowInstanceItem({ data: workflow, refetchParentData, isSelected }: ComponentProps<WorkflowOut>) {

  // Context: Delete and edit options, anchor for context location
  const [contextOpen, setContextOpen] = React.useState<string | null>(null)
  const [anchorEl, setAnchorEl] = React.useState<HTMLElement | null>(null)
  // const [workflowModalOpen, setWorkflowModalOpen] = React.useState(false)

  const handleContextClose = () => {
    setAnchorEl(null)
    setContextOpen(null)
  }

  const handleContextOpen = (e: React.MouseEvent<HTMLAnchorElement, MouseEvent>, examId: string) => {
    e.preventDefault()
    setAnchorEl(e.currentTarget)
    setContextOpen(examId)
  }

  const deleteExam = useMutation(async () => {
    await workflowsApi.deleteWorkflowApiV1ExamWorkflowWorkflowIdDelete(workflow.id).then(() => {
      refetchParentData()
    })
  })

  // TODO: Mutation to edit workflow instance

  return (

    <ListItem sx={{width: "100%"}}>

      <ListItemDecorator sx={{ align: 'center', justify: 'center' }}>
        <SnippetFolderSharpIcon />
      </ListItemDecorator>

      <ListItemContent>
        
        <Typography>{workflow.comment}</Typography>

        <Typography level='body-sm' textColor='text.tertiary'>
          {
            `Created: ${new Date(workflow.datetime_created).toDateString()}`
          }
        </Typography>

      </ListItemContent>

      <IconButton
        variant='plain'
        sx={{ '--IconButton-size': '25px' }}
        onClick={(e) => handleContextOpen(e, workflow.id)}
      >
        <MoreHorizIcon />
      </IconButton>

      <Menu
        id='context-menu'
        variant='plain'
        anchorEl={anchorEl}
        open={workflow.id === contextOpen}
        onClose={() => handleContextClose()}
        sx={{ zIndex: 'snackbar' }}
      >
        <MenuItem
          key='edit'
          onClick={() => {
            // setWorkflowModel(true)
          }}
        >
          Edit
        </MenuItem>

        <MenuItem
          key='delete'
          onClick={() => {
            deleteExam.mutate()
          }}
        >
          Delete
        </MenuItem>
      </Menu>

      {/* TODO: Model to edit workflow instance comes here */}

    </ListItem>

  )
}

export default WorkflowInstanceItem
