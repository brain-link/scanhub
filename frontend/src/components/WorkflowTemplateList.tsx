// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
// PatientTable.tsx is responsible for rendering the patient table view.
import * as React from 'react'
import Stack from '@mui/joy/Stack'
import Add from '@mui/icons-material/Add'
import Button from '@mui/joy/Button'

import WorkflowTemplateItem from './WorkflowTemplateItem'
import AlertItem from '../components/AlertItem'
import WorkflowTemplateCreateModal from './WorkflowTemplateCreateModal'

import { Alerts } from '../interfaces/components.interface'
import { useQuery } from 'react-query'
import { WorkflowOut } from "../generated-client/exam";
import { workflowsApi } from '../Api'


export default function WorkflowTemplateList() {

  const [modalOpen, setModalOpen] = React.useState(false)

  const {data: workflows, isLoading, isError, refetch} = useQuery<WorkflowOut[]>({
    queryKey: ['workflows'],
    queryFn: async () => { return await workflowsApi.getAllWorkflowTemplatesApiV1ExamWorkflowTemplatesAllGet().then((result) => {return result.data})}
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
        Create Workflow Template
      </Button>

      <WorkflowTemplateCreateModal
        isOpen={modalOpen}
        setOpen={setModalOpen}
        onSubmit={
          () => { refetch() }
        }
        onClose={() => {}}
      />

      {
        workflows?.map((workflow) => (
          <WorkflowTemplateItem
            item={workflow}
            onClicked={() => {}}
          />
        ))
      }
    </Stack>
  )
}
