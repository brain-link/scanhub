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
import Typography from '@mui/joy/Typography'
import React from 'react'
import { useQuery } from '@tanstack/react-query'

import { protocolApi, taskApi } from '../api'
import { ProtocolOut } from '../openapi/generated-client/protocol'
import ProtocolModal from '../components/ProtocolModal'
import ProtocolItem from '../components/ProtocolItem'
import TaskItem from '../components/TaskItem'
import { ITEM_UNSELECTED } from '../interfaces/components.interface'
import TaskModal from '../components/TaskModal'


export default function TemplatesView() {
  const [protocolModalOpen, setProtocolModalOpen] = React.useState(false)
  const [taskModalOpen, setTaskModalOpen] = React.useState(false)
  const [expandedProtocolIds, setExpandedProtocolIds] = React.useState<Set<string>>(new Set())
  const [taskParentId, setTaskParentId] = React.useState<string | undefined>(undefined)
  const [draggingTaskIndex, setDraggingTaskIndex] = React.useState<{ protocolId: string; index: number } | undefined>(undefined)

  const handleDragStart = (protocolId: string, index: number) => setDraggingTaskIndex({ protocolId, index })
  const handleDragOver = (e: React.DragEvent) => e.preventDefault()

  const toggleProtocol = (id: string) => {
    setTaskParentId(id)
    setExpandedProtocolIds(prev => {
      const next = new Set(prev)
      next.has(id) ? next.delete(id) : next.add(id)
      return next
    })
  }

  const handleDrop = async (protocolId: string, dropIndex: number) => {
    if (
      draggingTaskIndex === undefined ||
      draggingTaskIndex.protocolId !== protocolId ||
      draggingTaskIndex.index === dropIndex ||
      !protocols
    )
      return

    const protocol = protocols.find(p => p.id === protocolId)
    if (!protocol) return

    const tasks = [...protocol.tasks]
    const [draggedTask] = tasks.splice(draggingTaskIndex.index, 1)
    tasks.splice(dropIndex, 0, draggedTask)

    await taskApi.reorderTasks({ task_ids: tasks.map(t => t.id) })
    refetchProtocols()
    setDraggingTaskIndex(undefined)
  }

  const { data: protocols, refetch: refetchProtocols } = useQuery<ProtocolOut[]>({
    queryKey: ['allProtocolTemplates'],
    queryFn: async () => protocolApi.getAllProtocolTemplates().then(r => r.data),
  })

  return (
    <Stack direction='column' sx={{ height: '100%', overflow: 'hidden' }}>

      {/* Header with action buttons */}
      <Stack
        direction='row'
        alignItems='center'
        justifyContent='space-between'
        sx={{ p: 2, borderBottom: '1px solid', borderColor: 'divider', flexShrink: 0 }}
      >
        <Typography level='title-md'>Protocol Templates</Typography>
        <Stack direction='row' gap={1}>
          <Button
            size='sm'
            variant='outlined'
            startDecorator={<Add sx={{ fontSize: 'var(--IconFontSize)' }} />}
            onClick={() => setProtocolModalOpen(true)}
          >
            Create Protocol
          </Button>
          <Button
            size='sm'
            variant='outlined'
            startDecorator={<Add sx={{ fontSize: 'var(--IconFontSize)' }} />}
            onClick={() => setTaskModalOpen(true)}
            disabled={expandedProtocolIds.size === 0}
          >
            Create Task
          </Button>
        </Stack>
      </Stack>

      {/* Protocol list with inline task expansion */}
      <Stack direction='column' spacing={0.5} sx={{ p: 2, overflow: 'auto', flex: 1 }}>
        {protocols?.map((protocol) => (
          <React.Fragment key={`protocol-${protocol.id}`}>
            <ProtocolItem
              item={protocol}
              onClick={() => toggleProtocol(protocol.id)}
              selection={
                taskParentId === protocol.id ? {
                  type: 'protocol',
                  name: protocol.name,
                  itemId: protocol.id,
                  status: protocol.status,
                } : ITEM_UNSELECTED
              }
              refetchParentData={refetchProtocols}
            />

            {expandedProtocolIds.has(protocol.id) && protocol.tasks?.map((task, taskIndex) => (
              <Box
                key={`task-${task.id}`}
                draggable
                onDragStart={() => handleDragStart(protocol.id, taskIndex)}
                onDragOver={handleDragOver}
                onDrop={() => handleDrop(protocol.id, taskIndex)}
                sx={{
                  ml: 3,
                  cursor: 'grab',
                  '&:active': { cursor: 'grabbing' },
                  opacity: draggingTaskIndex?.protocolId === protocol.id && draggingTaskIndex.index === taskIndex ? 0.5 : 1,
                }}
              >
                <TaskItem
                  item={task}
                  refetchParentData={refetchProtocols}
                  onClick={() => {}}
                  selection={ITEM_UNSELECTED}
                />
              </Box>
            ))}
          </React.Fragment>
        ))}
      </Stack>

      <ProtocolModal
        isOpen={protocolModalOpen}
        setOpen={setProtocolModalOpen}
        onSubmit={refetchProtocols}
        modalType='create'
        createTemplate={true}
        parentId={undefined}
      />
      <TaskModal
        isOpen={taskModalOpen}
        setOpen={setTaskModalOpen}
        onSubmit={refetchProtocols}
        modalType='create'
        createTemplate={true}
        parentId={taskParentId}
      />

    </Stack>
  )
}
