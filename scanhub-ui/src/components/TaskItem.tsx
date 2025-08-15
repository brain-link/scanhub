/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * TaskItem.tsx is responsible for rendering a single task item.
 */
import React from 'react'
import { useMutation } from '@tanstack/react-query'

import Typography from '@mui/joy/Typography'
import Tooltip from '@mui/joy/Tooltip'
import Box from '@mui/joy/Box'
import Dropdown from '@mui/joy/Dropdown'
import Menu from '@mui/joy/Menu'
import MenuButton from '@mui/joy/MenuButton'
import IconButton from '@mui/joy/IconButton'
import DatasetRoundedIcon from '@mui/icons-material/DatasetRounded';
import AccountTreeRoundedIcon from '@mui/icons-material/AccountTreeRounded';
import MenuItem from '@mui/joy/MenuItem'
import MoreHorizIcon from '@mui/icons-material/MoreHoriz'
import ExpandMoreIcon from '@mui/icons-material/ExpandMore'
import Button from '@mui/joy/Button'

import { AcquisitionTaskOut, DAGTaskOut, ItemStatus, TaskType } from '../openapi/generated-client/exam'
import TaskInfo from './TaskInfo'
import { taskApi } from '../api'
import TaskModal from './TaskModal'
import { RefetchableItemInterface, SelectableItemInterface } from '../interfaces/components.interface'


export default function TaskItem(
  {
    item: task, 
    refetchParentData, 
    selection, 
    onClick
  }: RefetchableItemInterface<AcquisitionTaskOut | DAGTaskOut> & SelectableItemInterface<AcquisitionTaskOut | DAGTaskOut>
) {
  return (
    <Box
      sx={{ 
        width: '100%', 
        display: 'flex',
        justifyContent: 'space-between',
      }}
    >
      <Tooltip
        placement='right'
        variant='outlined'
        arrow
        title={<TaskInfo data={task} />}
      >
        <Button 
          sx={{
            width: '100%', 
            display: 'flex',
            justifyContent: 'flex-start',
            p: 0.5,
          }}
          color={task.status == ItemStatus.Finished ? 'success' : 'primary'}
          variant={((selection.type == 'DAG' || selection.type == 'ACQUISITION') && selection.itemId == task.id) ? 'outlined' : 'plain'}
          onClick={onClick}
        >
          {
            task.task_type === TaskType.Acquisition ? <DatasetRoundedIcon fontSize='small' /> : <AccountTreeRoundedIcon fontSize='small' />
          }
          <Box 
            sx={{
              marginLeft: 0.5,
              p: 0.5, 
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'flex-start'
            }}
          >
            <Typography level='title-sm' textAlign='left' sx={{overflowWrap: 'anywhere'}}>
              {task.name}
            </Typography>
            
            <Typography level='body-xs' textColor='text.tertiary' textAlign='left'>
              {`Created: ${new Date(task.datetime_created).toDateString()}`}
            </Typography>
          </Box>
        </Button>
      </Tooltip>
      <Box
        display='flex'
        alignItems='center'
      >
        <TaskMenu item={task} refetchParentData={refetchParentData} />
        <IconButton sx={{visibility: 'hidden'}} >
          <ExpandMoreIcon />
        </IconButton>
      </Box>
    </Box>
  )
}


function TaskMenu({ item: task, refetchParentData }: RefetchableItemInterface<AcquisitionTaskOut | DAGTaskOut>) {

  const [taskModalOpen, setTaskModalOpen] = React.useState<boolean>(false);

  const deleteTask = useMutation({
    mutationFn: async () => {
      await taskApi.deleteTaskApiV1ExamTaskTaskIdDelete(task.id)
      .then(() => {
        refetchParentData()
      })
    }
  })

  return (
    <>
      <Dropdown>
        <MenuButton variant='plain' sx={{ size: 'xs' }} slots={{ root: IconButton }}>
          <MoreHorizIcon fontSize='small' />
        </MenuButton>
        <Menu id='context-menu' variant='plain' sx={{ zIndex: 'snackbar' }}>
          <MenuItem key='edit' onClick={() => setTaskModalOpen(true)}>
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

      <TaskModal 
        isOpen={taskModalOpen}
        setOpen={setTaskModalOpen}
        onSubmit={refetchParentData}
        item={task}
        modalType={'modify'}
      />
    </>
  )
}