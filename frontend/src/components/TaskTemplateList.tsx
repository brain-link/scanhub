// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
// PatientTable.tsx is responsible for rendering the patient table view.
import * as React from 'react'
import Stack from '@mui/joy/Stack'
import Add from '@mui/icons-material/Add'
import Button from '@mui/joy/Button'

import TaskTemplateItem from './TaskTemplateItem'
import TaskTemplateCreateModal from './TaskTemplateCreateModal'
// import AlertItem from '../components/AlertItem'

// import { Alerts } from '../interfaces/components.interface'
import { useQuery } from 'react-query'
import { TaskOut } from '../generated-client/exam';
import { taskApi } from '../api'
import LoginContext from '../LoginContext'


export default function TaskTemplateList() {

  const [modalOpen, setModalOpen] = React.useState(false)
  const [user, ] = React.useContext(LoginContext);

  // const {data: tasks, isLoading, isError, refetch} = useQuery<TaskOut[]>({
  const {data: tasks, refetch} = useQuery<TaskOut[]>({
    queryKey: ['tasks'],
    queryFn: async () => {
      return await taskApi.getAllTaskTemplatesApiV1ExamTaskTemplatesAllGet(
        {headers: {Authorization: 'Bearer ' + user?.access_token}}
      )
      .then((result) => {return result.data})
    }
  })

  return (
    <Stack
      direction="column"
      alignItems="flex-start"
      spacing={2}
      sx={{p: 2}}
    >
      <Button
        startDecorator={<Add />}
        onClick={() => setModalOpen(true)}
      >
        Create Task Template
      </Button>

      <TaskTemplateCreateModal
        isOpen={modalOpen}
        setOpen={setModalOpen}
        onSubmit={
          () => { refetch() }
        }
        onClose={() => {}}
      />

      {
        tasks?.map((task, index) => (
          <TaskTemplateItem
            key={index}
            item={task}
            onClicked={() => {}}
            onDeleted={() => {refetch()}}
          />
        ))
      }
    </Stack>
  )
}
