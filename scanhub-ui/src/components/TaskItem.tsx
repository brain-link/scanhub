/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * TaskItem.tsx is responsible for rendering a single task item.
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
import ExpandMoreIcon from '@mui/icons-material/ExpandMore'

import { TaskOut } from '../generated-client/exam'
import { ItemInterface } from '../interfaces/components.interface'
import TaskInfo from './TaskInfo'
import { taskApi } from '../api'
import LoginContext from '../LoginContext'


export default function TaskItem({ data: task, refetchParentData }: ItemInterface<TaskOut>) {
  return (
    <Tooltip
      placement='right'
      variant='outlined'
      arrow
      title={<TaskInfo data={task} refetchParentData={refetchParentData}/>}
    >
      <Box
        sx={{ 
          width: '100%', 
          display: 'flex',
          justifyContent: 'space-between',
        }}
      >
        <Box 
          display='flex'
          alignItems='center'
          p='0.5'
        >
          <AssignmentIcon fontSize='small' />
          <Box 
            sx={{
              marginLeft: 0.5,
              p: 0.5, 
              display: 'flex',
              flexDirection: 'column',
            }}
          >
            <Typography level='title-sm'>{task.description ? task.description : 'Task'}</Typography>
            
            <Typography level='body-xs' textColor='text.tertiary'>
              {`Created: ${new Date(task.datetime_created).toDateString()}`}
            </Typography>
          </Box>
        </Box>
        <Box
          display='flex'
          alignItems='center'
        >
          <TaskMenu data={task} refetchParentData={refetchParentData} />
          <IconButton sx={{visibility: 'hidden'}} >
            <ExpandMoreIcon />
          </IconButton>
        </Box>
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