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
import Stack from '@mui/joy/Stack';
import Dropdown from '@mui/joy/Dropdown'
import Menu from '@mui/joy/Menu'
import MenuButton from '@mui/joy/MenuButton'
import IconButton from '@mui/joy/IconButton'
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import CircularProgress from '@mui/joy/CircularProgress';
import HighlightOffIcon from '@mui/icons-material/HighlightOff';
import RadioButtonUncheckedIcon from '@mui/icons-material/RadioButtonUnchecked';
import MenuItem from '@mui/joy/MenuItem'
import MoreHorizIcon from '@mui/icons-material/MoreHoriz'
import Button from '@mui/joy/Button'

import { AcquisitionTaskOut, DAGTaskOut, ItemStatus, TaskType } from '../openapi/generated-client/exam'
import TaskInfo from './TaskInfo'
import { taskApi } from '../api'
import TaskModal from './TaskModal'
import { RefetchableItemInterface, SelectableItemInterface } from '../interfaces/components.interface'
import DagsterUIModal from './DagsterUIModal'
import { extractRunId, getLatestResult } from '../utils/ExamTree'


export default function TaskItem(
  {
    item: task, 
    refetchParentData, 
    selection, 
    onClick
  }: RefetchableItemInterface<AcquisitionTaskOut | DAGTaskOut> & SelectableItemInterface<AcquisitionTaskOut | DAGTaskOut>
) {
  return (
    <Stack direction='row' width='100%' alignItems='center' sx={{paddingLeft: 2}}>
      <Tooltip
        placement='right'
        variant='outlined'
        arrow
        title={<TaskInfo data={task} />}
        modifiers={[
          { name: 'offset', options: { offset: [0, 64] } }, // skidding=8 (down), distance=20 (further right)
        ]}
      >
        <Button 
          sx={{
            p: 0.5,
            flexGrow: 1,
            justifyContent: 'flex-start',
            gap: 0.5,
          }}
          variant={((selection.type == 'DAG' || selection.type == 'ACQUISITION') && selection.itemId == task.id) ? 'outlined' : 'plain'}
          onClick={onClick}
        >
          {
            task.status === ItemStatus.Finished ? <CheckCircleIcon fontSize='small' /> : (
              task.status === ItemStatus.Inprogress ? <CircularProgress variant='plain' size="sm" /> : (
                task.status === ItemStatus.Error ? <HighlightOffIcon fontSize='small' /> : <RadioButtonUncheckedIcon fontSize='small' />
              )
            )
          }
          <Box sx={{ marginLeft: 0.5, p: 0.5,  display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }} >
            <Typography level='body-xs' textColor='text.tertiary'>
              {task.task_type}
            </Typography>
            
            <Typography level='title-sm' textAlign='left' sx={{overflowWrap: 'anywhere'}}>
              {task.name}
            </Typography>
            
            <Typography level='body-xs' textColor='text.tertiary' textAlign='left'>
              {`Created: ${new Date(task.datetime_created).toDateString()}`}
            </Typography>
          </Box>
        </Button>
      </Tooltip>

      <TaskMenu item={task} refetchParentData={refetchParentData} />

    </Stack>
  )
}


function TaskMenu({ item: task, refetchParentData }: RefetchableItemInterface<AcquisitionTaskOut | DAGTaskOut>) {

  const [taskModalOpen, setTaskModalOpen] = React.useState<boolean>(false);
  const [dagsterOpen, setDagsterOpen] = React.useState<boolean>(false);

  const runId = React.useMemo(() => {
    return extractRunId(getLatestResult(task.results)?.meta as unknown)
  }, [task.results]);

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
          <MenuItem key='delete' onClick={() => { deleteTask.mutate() }}>
            Delete
          </MenuItem>
          {
            task.task_type === TaskType.Dag &&
            <MenuItem key='open-dagster' onClick={() => { setDagsterOpen(true) }} disabled={!runId}>
              Open DagsterUI
            </MenuItem>
          }
        </Menu>
      </Dropdown>

      <TaskModal 
        isOpen={taskModalOpen}
        setOpen={setTaskModalOpen}
        onSubmit={refetchParentData}
        item={task}
        modalType={'modify'}
      />

      <DagsterUIModal 
        isOpen={dagsterOpen}
        setOpen={setDagsterOpen}
        onSubmit={() => {}}
        item={runId ? `/dagster/runs/${ runId }` : '/dagster/runs'}
      />
    </>
  )
}