// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
// ExamItem.tsx is responsible for rendering a single exam item in the exam list of the patient view.

import * as React from 'react'
import { useMutation } from 'react-query'

// Mui joy components
import IconButton from '@mui/joy/IconButton'
import ListItem from '@mui/joy/ListItem'
import ListItemDecorator from '@mui/joy/ListItemDecorator'
import ListItemContent from '@mui/joy/ListItemContent'
import Typography from '@mui/joy/Typography'
import Dropdown from '@mui/joy/Dropdown';
import MenuButton from '@mui/joy/MenuButton';
import MenuItem from '@mui/joy/MenuItem';
import Menu from '@mui/joy/Menu'

// Icons
import MoreHorizIcon from '@mui/icons-material/MoreHoriz'
import AssignmentIcon from '@mui/icons-material/Assignment'

// Sub-components, interfaces, client
import LoginContext from '../LoginContext';
import { InstanceInterface } from '../interfaces/components.interface'
import { TaskOut } from '../generated-client/exam'
import { taskApi } from '../api'

// function ExamInstanceItem({ data: exam, refetchParentData, isSelected }: ComponentProps<ExamOut>) {
function TaskInstanceItem({data: task, refetchParentData}: InstanceInterface<TaskOut>) {

  const [user, ] = React.useContext(LoginContext);
  
  const deleteTask = useMutation(async () => {
    await taskApi.deleteTaskApiV1ExamTaskTaskIdDelete(
      task.id, {headers: {Authorization: 'Bearer ' + user?.access_token}}
    ).then(() => {
      refetchParentData()
    })
  })

  return (

    <ListItem sx={{width: '100%', p: 0.5}}>

      <ListItemDecorator sx={{ align: 'center', justify: 'center' }}>
        <AssignmentIcon fontSize='small' />
      </ListItemDecorator>

      <ListItemContent>
        
        <Typography level="title-sm">{task.description ? task.description : 'Task'}</Typography>

        <Typography level='body-xs' textColor='text.tertiary'>
          { `Created: ${new Date(task.datetime_created).toDateString()}` }
        </Typography>

      </ListItemContent>

      <Dropdown>
        <MenuButton variant='plain' sx={{zIndex: 'snackbar', size: 'xs'}} slots={{root: IconButton}}>
          <MoreHorizIcon fontSize='small'/>
        </MenuButton>
        <Menu
          id='context-menu'
          variant='plain'
          sx={{ zIndex: 'snackbar' }}
        >
          <MenuItem key='edit' onClick={() => {}}>Edit</MenuItem>
          <MenuItem key='delete' onClick={() => {deleteTask.mutate()}}>Delete</MenuItem>
        </Menu>
      </Dropdown>

    </ListItem>

  )
}

export default TaskInstanceItem
