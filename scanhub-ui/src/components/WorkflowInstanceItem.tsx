/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * WorkflowInstanceItem.tsx is responsible for rendering additional information
 * of a workflow instance item.
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

import { WorkflowOut } from '../generated-client/exam'
import { InstanceInterface } from '../interfaces/components.interface'
import WorkflowInstanceInfo from '../components/WorkflowInstanceInfo'
import { workflowsApi } from '../api'
import LoginContext from '../LoginContext'
import TaskFromTemplateModal from '../components/TaskFromTemplateModal'


export default function WorkflowInstanceItem({ data: workflow, refetchParentData }: InstanceInterface<WorkflowOut>) {
  return (
    <Tooltip
      placement='right'
      variant='outlined'
      describeChild={false}
      arrow
      title={<WorkflowInstanceInfo data={workflow} refetchParentData={refetchParentData} />}
    >
      <Box
        sx={{ 
          width: '100%', 
          p: 0.5, 
          display: 'flex',
          alignItems: 'center',
        }}
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
          <Typography level='title-sm'>{workflow.comment}</Typography>

          <Typography level='body-xs' textColor='text.tertiary'>
            {`Created: ${new Date(workflow.datetime_created).toDateString()}`}
          </Typography>
        </Box>
      </Box>
    </Tooltip>
  )
}


export function WorkflowInstanceMenu({ data: workflow, refetchParentData }: InstanceInterface<WorkflowOut>) {

  const [taskFromTemplateModalOpen, setTaskFromTemplateModalOpen] = React.useState(false)
  // const [examModalOpen, setExamModalOpen] = React.useState(false)

  const [user] = React.useContext(LoginContext)

  const deleteWorkflow = useMutation(async () => {
    await workflowsApi
      .deleteWorkflowApiV1ExamWorkflowWorkflowIdDelete(workflow.id, { headers: { Authorization: 'Bearer ' + user?.access_token } })
      .then(() => {
        refetchParentData()
      })
  })

  return (
    <>
      <Dropdown>
        <MenuButton variant='plain' sx={{ zIndex: 'snackbar', size: 'xs' }} slots={{ root: IconButton }}>
          <MoreHorizIcon fontSize='small' />
        </MenuButton>
        <Menu id='context-menu' variant='plain' sx={{ zIndex: 'snackbar' }}>
          <MenuItem key='edit' onClick={() => {}}>
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
            key='add'
            onClick={() => {
              setTaskFromTemplateModalOpen(true)
            }}
          >
            Add Task
          </MenuItem>
        </Menu>
      </Dropdown>

      <TaskFromTemplateModal
        isOpen={taskFromTemplateModalOpen}
        setOpen={setTaskFromTemplateModalOpen}
        parentId={workflow.id}
        onSubmit={refetchParentData}
      />
    </>
  )
}