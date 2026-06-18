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
import Select from '@mui/joy/Select'
import Option from '@mui/joy/Option'

import MenuItem from '@mui/joy/MenuItem'
import MoreHorizIcon from '@mui/icons-material/MoreHoriz'
import Button from '@mui/joy/Button'

import { AcquisitionTaskOut, ResultOut } from '../openapi/generated-client/protocol'
import TaskInfo from './TaskInfo'
import { taskApi } from '../api'
import TaskModal from './TaskModal'
import { RefetchableItemInterface, SelectableItemInterface } from '../interfaces/components.interface'
import DagsterUIModal from './DagsterUIModal'
import { extractRunId, getLatestResult } from '../utils/ProtocolTree'


interface TaskItemExtraProps {
  results?: ResultOut[];
  selectedResultId?: string;
  onResultSelect?: (id: string) => void;
}

export default function TaskItem(
  {
    item: task,
    refetchParentData,
    selection,
    onClick,
    icon = <></>,
    results,
    selectedResultId,
    onResultSelect,
  }: RefetchableItemInterface<AcquisitionTaskOut> & SelectableItemInterface<AcquisitionTaskOut> & TaskItemExtraProps
) {
  const isSelected = selection.type === 'ACQUISITION' && selection.itemId === task.id
  const showResultSelect = isSelected && !!results && results.length > 0

  return (
    <Box sx={{ display: 'grid', gridTemplateColumns: '1fr auto', pl: 2 }}>
      <Tooltip
        placement='right'
        variant='outlined'
        arrow
        title={<TaskInfo data={task} />}
        modifiers={[
          { name: 'offset', options: { offset: [0, 64] } },
        ]}
      >
        <Button
          sx={{ p: 0.5, minWidth: 0, justifyContent: 'flex-start', gap: 0.5 }}
          variant={isSelected ? 'outlined' : 'plain'}
          onClick={onClick}
        >
          {icon}
          <Box sx={{ marginLeft: 0.5, p: 0.5, display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
            <Typography level='body-xs' textColor='text.tertiary'>
              {task.task_type}
            </Typography>
            <Typography level='title-sm' textAlign='left' sx={{ overflowWrap: 'anywhere' }}>
              {task.name}
            </Typography>
            <Typography level='body-xs' textColor='text.tertiary' textAlign='left'>
              {`Created: ${new Date(task.datetime_created).toDateString()}`}
            </Typography>
          </Box>
        </Button>
      </Tooltip>

      <Box sx={{ display: 'flex', alignItems: 'center' }}>
        <TaskMenu item={task} refetchParentData={refetchParentData} />
      </Box>

      {showResultSelect && (
        <Select
          size='sm'
          value={selectedResultId ?? null}
          onChange={(_, v) => v && onResultSelect?.(v)}
          sx={{ mt: 0.75, mb: 0.75, minWidth: 0 }}
          slotProps={{ listbox: { placement: 'bottom-start' } }}
        >
          {results!.map(result => {
            const dt = new Date(result.datetime_created)
            const label = (result.files?.[0] ? result.files[0] + ' | ' : '') +
              dt.toLocaleDateString() + ', ' + dt.toLocaleTimeString()
            return <Option key={result.id} value={result.id}>{label}</Option>
          })}
        </Select>
      )}
    </Box>
  )
}


function TaskMenu({ item: task, refetchParentData }: RefetchableItemInterface<AcquisitionTaskOut>) {

  const [taskModalOpen, setTaskModalOpen] = React.useState<boolean>(false);
  const [dagsterOpen, setDagsterOpen] = React.useState<boolean>(false);

  const runId = React.useMemo(() => {
    return extractRunId(getLatestResult(task.results)?.meta as unknown)
  }, [task.results]);

  const deleteTask = useMutation({
    mutationFn: async () => {
      await taskApi.deleteTask(task.id)
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
            runId &&
            <MenuItem key='open-dagster' onClick={() => { setDagsterOpen(true) }}>
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