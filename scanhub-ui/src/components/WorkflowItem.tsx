/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * WorkflowItem.tsx is responsible for rendering additional information
 * of a workflow item.
 */
import * as React from 'react'
import { useMutation } from 'react-query'

import Typography from '@mui/joy/Typography'
import Tooltip from '@mui/joy/Tooltip'
import Box from '@mui/joy/Box'
import Dropdown from '@mui/joy/Dropdown'
import Menu from '@mui/joy/Menu'
import MenuButton from '@mui/joy/MenuButton'
import IconButton from '@mui/joy/IconButton'
import MenuItem from '@mui/joy/MenuItem'
import MoreHorizIcon from '@mui/icons-material/MoreHoriz'
import SchemaIcon from '@mui/icons-material/Schema'
import Button from '@mui/joy/Button'

import { WorkflowOut } from '../generated-client/exam'
import { RefetchableItemInterface, SelectableItemInterface } from '../interfaces/components.interface'
import WorkflowInfo from './WorkflowInfo'
import { workflowsApi } from '../api'
import TaskFromTemplateModal from './TaskFromTemplateModal'
import TaskModal from './TaskModal'
import WorkflowModal from './WorkflowModal'


export default function WorkflowItem({ item: workflow, selection, onClick }: SelectableItemInterface<WorkflowOut>) {
  return (
    <Tooltip
      placement='right'
      variant='outlined'
      describeChild={false}
      arrow
      title={<WorkflowInfo workflow={workflow} />}
    >
      <Button
        sx={{ 
          width: '100%', 
          p: 0.5, 
          display: 'flex',
          justifyContent: 'flex-start'
        }}
        variant={(selection.type == 'workflow' && selection.itemId == workflow.id) ? 'outlined' : 'plain'}
        onClick={onClick}
      >
        <SchemaIcon fontSize='small' />
        <Box 
          sx={{
            marginLeft: 0.5,
            p: 0.5, 
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'start',
          }}
        >
          <Typography level='title-sm'>{workflow.name}</Typography>

          <Typography level='body-xs' textColor='text.tertiary'>
            {`Created: ${new Date(workflow.datetime_created).toDateString()}`}
          </Typography>
        </Box>
      </Button>
    </Tooltip>
  )
}


export function WorkflowMenu({ item: workflow, refetchParentData }: RefetchableItemInterface<WorkflowOut>) {

  const [taskFromTemplateModalOpen, setTaskFromTemplateModalOpen] = React.useState(false)
  const [taskCreateNewModalOpen, setTaskCreateNewModalOpen] = React.useState(false)
  const [workflowModalOpen, setWorkflowModalOpen] = React.useState(false)

  const deleteWorkflow = useMutation(async () => {
    await workflowsApi
      .deleteWorkflowApiV1ExamWorkflowWorkflowIdDelete(workflow.id)
      .then(() => {
        refetchParentData()
      })
  })

  return (
    <>
      <Dropdown>
        <MenuButton variant='plain' sx={{ size: 'xs' }} slots={{ root: IconButton }}>
          <MoreHorizIcon fontSize='small' />
        </MenuButton>
        <Menu id='context-menu' variant='plain' sx={{ zIndex: 'snackbar' }}>
          <MenuItem key='edit' onClick={() => {setWorkflowModalOpen(true)}}>
            Edit
          </MenuItem>
          <MenuItem
            key='delete'
            onClick={() => {
              deleteWorkflow.mutate()
            }}
          >
            Delete
          </MenuItem>
          <MenuItem
            key='addFromTemplate'
            onClick={() => {
              setTaskFromTemplateModalOpen(true)
            }}
          >
            Add Task from Template
          </MenuItem>
          {
            workflow.is_template ?
              <MenuItem
                key='addNew'
                onClick={() => {
                  setTaskCreateNewModalOpen(true)
                }}
              >
                Add new Task
              </MenuItem>
            : undefined
          }
        </Menu>
      </Dropdown>

      <TaskFromTemplateModal
        isOpen={taskFromTemplateModalOpen}
        setOpen={setTaskFromTemplateModalOpen}
        parentId={workflow.id}
        onSubmit={refetchParentData}
        createTemplate={workflow.is_template}
        modalType={'create'}
      />

      {
        workflow.is_template ?
          <TaskModal
            isOpen={taskCreateNewModalOpen}
            setOpen={setTaskCreateNewModalOpen}
            parentId={workflow.id}
            onSubmit={refetchParentData}
            createTemplate={workflow.is_template}
            modalType={'create'}
          />
        : undefined
      }

      <WorkflowModal 
        onSubmit={refetchParentData}
        isOpen={workflowModalOpen}
        setOpen={setWorkflowModalOpen}
        item={workflow}
        modalType={'modify'}
      />    
    </>
  )
}