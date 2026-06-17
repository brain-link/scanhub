/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * TemplatesView.tsx is responsible for rendering all existing template items
 * and allows to add new templates or edit existing templates.
 */
import Add from '@mui/icons-material/Add'
import Box from '@mui/joy/Box'
import Button from '@mui/joy/Button'
import Stack from '@mui/joy/Stack'
import React from 'react'
import { useQuery } from '@tanstack/react-query'

import { protocolApi, taskApi } from '../api'
import { ProtocolOut } from '../openapi/generated-client/protocol'
import ExamModal from '../components/ExamModal'
import ExamItem, { ExamMenu } from '../components/ExamItem'
import Typography from '@mui/joy/Typography'
import TaskItem from '../components/TaskItem'
import { ITEM_UNSELECTED } from '../interfaces/components.interface'
import TaskModal from '../components/TaskModal'


export default function TemplatesView() {
  const [examModalOpen, setExamModalOpen] = React.useState(false)
  const [taskModalOpen, setTaskModalOpen] = React.useState(false)

  const [selectedProtocol, setSelectedProtocol] = React.useState<undefined | number>(undefined)
  const [draggingTaskIndex, setDraggingTaskIndex] = React.useState<number | undefined>(undefined)

  const handleDragStart = (index: number) => {
    setDraggingTaskIndex(index)
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
  }

  const handleDrop = async (index: number) => {
    if (
      draggingTaskIndex === undefined ||
      draggingTaskIndex === index ||
      selectedProtocol === undefined ||
      !exams
    )
      return

    const tasks = [...exams[selectedProtocol].tasks]
    const [draggedTask] = tasks.splice(draggingTaskIndex, 1)
    tasks.splice(index, 0, draggedTask)

    const taskIds = tasks.map((t) => t.id)
    await taskApi.reorderTasks({ task_ids: taskIds })
    refetchExams()
    setDraggingTaskIndex(undefined)
  }

  const { data: exams, refetch: refetchExams } = useQuery<ProtocolOut[]>({
    queryKey: ['allExamTemplates'],
    queryFn: async () => {
      return await protocolApi
        .getAllProtocolTemplates()
        .then((result) => {
          return result.data
        })
    },
  })

  return (
    <Stack direction="row" alignItems="flex-start" width='100vw'>

      <Stack direction='column' alignContent='center' flex={1} spacing={2} sx={{ p: 2 }}>
        <Stack direction='row' sx={{ justifyContent: 'space-between', mb: 1, alignItems: 'center' }}>
          <Typography level='title-md'>Protocol Templates</Typography>
          <Button
            variant='outlined'
            startDecorator={<Add sx={{ fontSize: 'var(--IconFontSize)' }} />}
            onClick={() => setExamModalOpen(true)}>
            Create Protocol
          </Button>
        </Stack>

        <ExamModal
          isOpen={examModalOpen}
          setOpen={setExamModalOpen}
          onSubmit={() => refetchExams()}
          modalType='create'
          createTemplate={true}
          parentId={undefined}
        />
        {
          exams?.map((protocol, index) => (
            <Stack direction="row" key={`protocol-${protocol.id}`} gap={1}>
              <ExamItem
                item={protocol}
                onClick={() => { selectedProtocol === index ? setSelectedProtocol(undefined) : setSelectedProtocol(index) }}
                selection={selectedProtocol === index ? {
                  type: 'protocol',
                  name: exams[index].name,
                  itemId: exams[index].id,
                  status: exams[index].status
                } : ITEM_UNSELECTED}
              />
              <ExamMenu item={protocol} refetchParentData={refetchExams} />
            </Stack>
          ))
        }
      </Stack>

      <Stack direction='column' alignContent='center' flex={1} spacing={2} sx={{ p: 2 }}>
        <Stack direction='row' sx={{ justifyContent: 'space-between', mb: 1, alignItems: 'center' }}>
          <Typography level='title-md'>Task Templates</Typography>
          <Button
            variant='outlined'
            startDecorator={<Add sx={{ fontSize: 'var(--IconFontSize)' }} />}
            onClick={() => setTaskModalOpen(true)}
            disabled={selectedProtocol === undefined}
          >
            Create Task
          </Button>
        </Stack>

        <TaskModal
          isOpen={taskModalOpen}
          setOpen={setTaskModalOpen}
          onSubmit={() => refetchExams()}
          modalType='create'
          createTemplate={true}
          parentId={exams && selectedProtocol !== undefined ? exams[selectedProtocol].id : undefined}
        />
        {
          exams && selectedProtocol !== undefined && exams[selectedProtocol]?.tasks?.map((task, index) => (
            <Box
              key={`task-${task.id}`}
              draggable
              onDragStart={() => handleDragStart(index)}
              onDragOver={handleDragOver}
              onDrop={() => handleDrop(index)}
              sx={{
                cursor: 'grab',
                '&:active': { cursor: 'grabbing' },
                opacity: draggingTaskIndex === index ? 0.5 : 1,
              }}
            >
              <TaskItem
                item={task}
                refetchParentData={refetchExams}
                onClick={() => { }}
                selection={ITEM_UNSELECTED}
              />
            </Box>
          ))
        }
      </Stack>

    </Stack>
  )
}
