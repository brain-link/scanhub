/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * TaskTemplateList.tsx is responsible for rendering a list of task template items.
 */
import Add from '@mui/icons-material/Add'
import Button from '@mui/joy/Button'
import Stack from '@mui/joy/Stack'
import * as React from 'react'
// import AlertItem from '../components/AlertItem'
// import { Alerts } from '../interfaces/components.interface'
import { useQuery } from 'react-query'

import LoginContext from '../LoginContext'
import { taskApi } from '../api'
import { TaskOut } from '../generated-client/exam'
import TaskTemplateCreateModal from './TaskTemplateCreateModal'
import TaskTemplateItem from './TaskTemplateItem'

export default function TaskTemplateList() {
  const [modalOpen, setModalOpen] = React.useState(false)
  const [user] = React.useContext(LoginContext)

  // const {data: tasks, isLoading, isError, refetch} = useQuery<TaskOut[]>({
  const { data: tasks, refetch } = useQuery<TaskOut[]>({
    queryKey: ['tasks'],
    queryFn: async () => {
      return await taskApi
        .getAllTaskTemplatesApiV1ExamTaskTemplatesAllGet({ headers: { Authorization: 'Bearer ' + user?.access_token } })
        .then((result) => {
          return result.data
        })
    },
  })

  return (
    <Stack direction='column' alignItems='flex-start' spacing={2} sx={{ p: 2 }}>
      <Button startDecorator={<Add />} onClick={() => setModalOpen(true)}>
        Create Task Template
      </Button>

      <TaskTemplateCreateModal
        isOpen={modalOpen}
        setOpen={setModalOpen}
        onSubmit={() => {
          refetch()
        }}
        onClose={() => {}}
      />

      {tasks?.map((task, index) => (
        <TaskTemplateItem
          key={index}
          item={task}
          onClicked={() => {}}
          onDeleted={() => {
            refetch()
          }}
        />
      ))}
    </Stack>
  )
}
