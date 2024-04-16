// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
// PatientTable.tsx is responsible for rendering the patient table view.
import * as React from 'react'
import Stack from '@mui/joy/Stack'
import Add from '@mui/icons-material/Add'
import Button from '@mui/joy/Button'

import TaskTemplateItem from './TaskTemplateItem'
import AlertItem from '../components/AlertItem'

import { Alerts } from '../interfaces/components.interface'
import { useQuery } from 'react-query'
import { TaskOut } from "../generated-client/exam";
import { taskApi } from '../Api'


export default function TaskTemplateList() {

  const [modalOpen, setModalOpen] = React.useState(false)

  const {data: tasks, isLoading, isError, refetch} = useQuery<TaskOut[]>({
    queryKey: ['tasks'],
    queryFn: async () => { return await taskApi.getAllTaskTemplatesApiV1ExamTaskTemplatesAllGet().then((result) => {return result.data})}
  })

  return (
    <Stack
      direction="column"
      alignItems="flex-start"
      spacing={2}
    >
      <Button
        startDecorator={<Add />}
        onClick={() => setModalOpen(true)}
      >
        Create Task Template
      </Button>

      {/* <WorkflowTemplateCreateModal
        isOpen={modalOpen}
        setOpen={setModalOpen}
        onSubmit={
          () => { refetch() }
        }
        onClose={() => {}}
      /> */}

      {
        tasks?.map((task) => (
          <TaskTemplateItem
            item={task}
            onClicked={() => {}}
          />
        ))
      }
    </Stack>
  )
}
