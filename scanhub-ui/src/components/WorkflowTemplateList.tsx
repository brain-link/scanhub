/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * WorkflowTemplateList.tsx is responsible for rendering a list of workflow template items.
 */
import Add from '@mui/icons-material/Add'
import Button from '@mui/joy/Button'
import Stack from '@mui/joy/Stack'
import * as React from 'react'
import { useContext } from 'react'
// import { Alerts } from '../interfaces/components.interface'
import { useQuery } from 'react-query'

import LoginContext from '../LoginContext'
import { workflowsApi } from '../api'
import { WorkflowOut } from '../generated-client/exam'
// import AlertItem from '../components/AlertItem'
import WorkflowTemplateCreateModal from './WorkflowTemplateCreateModal'
import WorkflowTemplateItem from './WorkflowTemplateItem'

export default function WorkflowTemplateList() {
  const [modalOpen, setModalOpen] = React.useState(false)

  const [user] = useContext(LoginContext)

  // const {data: workflows, isLoading, isError, refetch} = useQuery<WorkflowOut[]>({
  const { data: workflows, refetch } = useQuery<WorkflowOut[]>({
    queryKey: ['workflows'],
    queryFn: async () => {
      return await workflowsApi
        .getAllWorkflowTemplatesApiV1ExamWorkflowTemplatesAllGet({
          headers: { Authorization: 'Bearer ' + user?.access_token },
        })
        .then((result) => {
          return result.data
        })
    },
  })

  return (
    <Stack direction='column' alignItems='flex-start' spacing={2} sx={{ p: 2 }}>
      <Button startDecorator={<Add />} onClick={() => setModalOpen(true)}>
        Create Workflow Template
      </Button>

      <WorkflowTemplateCreateModal
        isOpen={modalOpen}
        setOpen={setModalOpen}
        onSubmit={() => {
          refetch()
        }}
        onClose={() => {}}
      />

      {workflows?.map((workflow, index) => (
        <WorkflowTemplateItem
          key={index}
          data={workflow}
          onClicked={() => {}}
          onDeleted={() => {
            refetch()
          }}
        />
      ))}
    </Stack>
  )
}
