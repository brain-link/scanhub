/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * TaskInstanceItem.tsx is responsible for rendering a single task instance item
 * in the task instance list of a workflow.
 */
import * as React from 'react'
import { useMutation } from 'react-query'

import AssignmentIcon from '@mui/icons-material/Assignment'
import Typography from '@mui/joy/Typography'
import Tooltip from '@mui/joy/Tooltip'
import Box from '@mui/joy/Box'
import Dropdown from '@mui/joy/Dropdown'
import Menu from '@mui/joy/Menu'
import MenuButton from '@mui/joy/MenuButton'
import IconButton from '@mui/joy/IconButton'
import MenuItem from '@mui/joy/MenuItem'
import MoreHorizIcon from '@mui/icons-material/MoreHoriz'

import { TaskOut } from '../generated-client/exam'
import { ItemInterface } from '../interfaces/components.interface'
import TaskInstanceInfo from './TaskInstanceInfo'
import { taskApi } from '../api'
import LoginContext from '../LoginContext'


export default function TaskItem({ data: task, refetchParentData }: ItemInterface<TaskOut>) {
  return (
    <Tooltip
      placement='right'
      variant='outlined'
      arrow
      title={<TaskInstanceInfo data={task} refetchParentData={refetchParentData}/>}
    >
      <Box
        sx={{ 
          width: '100%', 
          p: 0.5, 
          display: 'flex',
          alignItems: 'center',
        }}
      >
        <AssignmentIcon fontSize='small' />
        <Box 
          sx={{
            marginLeft: 0.5,
            p: 0.5, 
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'start',
          }}
        >
          <Typography level='title-sm'>{task.description ? task.description : 'Task'}</Typography>
          
          <Typography level='body-xs' textColor='text.tertiary'>
            {`Created: ${new Date(task.datetime_created).toDateString()}`}
          </Typography>
        </Box>
        <TaskMenu data={task} refetchParentData={refetchParentData} />
      </Box>
    </Tooltip>
  )
}


function TaskMenu({ data: task, refetchParentData }: ItemInterface<TaskOut>) {
  const [user] = React.useContext(LoginContext)

  const deleteTask = useMutation(async () => {
    await taskApi
      .deleteTaskApiV1ExamTaskTaskIdDelete(task.id, { headers: { Authorization: 'Bearer ' + user?.access_token } })
      .then(() => {
        refetchParentData()
      })
  })

  return (
    <Dropdown>
      <MenuButton variant='plain' sx={{ size: 'xs' }} slots={{ root: IconButton }}>
        <MoreHorizIcon fontSize='small' />
      </MenuButton>
      <Menu id='context-menu' variant='plain' sx={{ zIndex: 'snackbar' }}>
        <MenuItem key='edit' onClick={() => {}}>
          Edit
        </MenuItem>
        <MenuItem
          key='delete'
          onClick={() => {
            deleteTask.mutate()
          }}
        >
          Delete
        </MenuItem>
      </Menu>
    </Dropdown>
  )
}