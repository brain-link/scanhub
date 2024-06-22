/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * WorkflowInstanceItem.tsx is responsible for rendering additional information
 * of a workflow instance item.
 */
// Icons
import MoreHorizIcon from '@mui/icons-material/MoreHoriz'
import SchemaIcon from '@mui/icons-material/Schema'
import Dropdown from '@mui/joy/Dropdown'
// Mui joy components
import IconButton from '@mui/joy/IconButton'
import ListItem from '@mui/joy/ListItem'
import ListItemContent from '@mui/joy/ListItemContent'
import ListItemDecorator from '@mui/joy/ListItemDecorator'
import Menu from '@mui/joy/Menu'
import MenuButton from '@mui/joy/MenuButton'
import MenuItem from '@mui/joy/MenuItem'
import Typography from '@mui/joy/Typography'
import * as React from 'react'
import { useMutation } from 'react-query'

// Sub-components, interfaces, client
import LoginContext from '../LoginContext'
import { workflowsApi } from '../api'
import { WorkflowOut } from '../generated-client/exam'
import { InstanceInterface } from '../interfaces/components.interface'
import TaskFromTemplateModal from './TaskFromTemplateModal'

function WorkflowInstanceItem({ data: workflow, refetchParentData }: InstanceInterface<WorkflowOut>) {
  const [user] = React.useContext(LoginContext)
  const [modalOpen, setModalOpen] = React.useState(false)

  const deleteExam = useMutation(async () => {
    await workflowsApi
      .deleteWorkflowApiV1ExamWorkflowWorkflowIdDelete(workflow.id, {
        headers: { Authorization: 'Bearer ' + user?.access_token },
      })
      .then(() => {
        refetchParentData()
      })
  })

  // TODO: Mutation to edit workflow instance

  return (
    <ListItem sx={{ width: '100%', p: 0.5 }}>
      <ListItemDecorator sx={{ align: 'center', justify: 'center' }}>
        <SchemaIcon fontSize='small' />
      </ListItemDecorator>

      <ListItemContent>
        <Typography level='title-sm'>{workflow.comment}</Typography>

        <Typography level='body-xs' textColor='text.tertiary'>
          {`Created: ${new Date(workflow.datetime_created).toDateString()}`}
        </Typography>
      </ListItemContent>

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
              deleteExam.mutate()
            }}
          >
            Delete
          </MenuItem>
          <MenuItem
            key='add'
            onClick={() => {
              setModalOpen(true)
            }}
          >
            Add Task
          </MenuItem>
        </Menu>
      </Dropdown>

      <TaskFromTemplateModal
        isOpen={modalOpen}
        setOpen={setModalOpen}
        parentId={workflow.id}
        onSubmit={refetchParentData}
      />

      {/* TODO: Model to edit workflow instance comes here */}
    </ListItem>
  )
}

export default WorkflowInstanceItem
