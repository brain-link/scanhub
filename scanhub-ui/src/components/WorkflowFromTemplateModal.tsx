/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * WorkflowFromTemplateModal.tsx is responsible for rendering a
 * workflow template selection interface to generate a new workflow.
 */
import Modal from '@mui/joy/Modal'
import ModalClose from '@mui/joy/ModalClose'
import ModalDialog from '@mui/joy/ModalDialog'
import DialogTitle from '@mui/material/DialogTitle'
import * as React from 'react'
import { useMutation } from 'react-query'
import { useQuery } from 'react-query'

import { workflowsApi } from '../api'
import { WorkflowOut } from '../generated-client/exam'
import { ITEM_UNSELECTED, ModalPropsCreate } from '../interfaces/components.interface'
import WorkflowItem from './WorkflowItem'
import { Stack } from '@mui/material'

export default function WorkflowFromTemplateModal(props: ModalPropsCreate) {

  const { data: workflows } = useQuery<WorkflowOut[]>({
    queryKey: ['allWorkflowTemplates'],
    queryFn: async () => {
      return await workflowsApi
        .getAllWorkflowTemplatesApiV1ExamWorkflowTemplatesAllGet()
        .then((result) => {
          return result.data
        })
    },
  })

  const mutation = useMutation(async (id: string) => {
    await workflowsApi
      .createWorkflowFromTemplateApiV1ExamWorkflowPost(String(props.parentId), id, props.createTemplate)
      .then(() => {
        props.onSubmit()
      })
      .catch((err) => {
        console.log(err)
      })
  })

  return (
    <>
      <Modal
        open={props.isOpen}
        onClose={() => {
          props.setOpen(false)
        }}
      >
        <ModalDialog sx={{ width: '50vw', p: 5 }}>
          <ModalClose />
          <DialogTitle>Add Workflow from Template</DialogTitle>
          <Stack
            sx={{
              overflow: 'scroll',
              mx: 'calc(-1 * var(--ModalDialog-padding))',
              px: 'var(--ModalDialog-padding)',
            }}
          >
            {workflows &&
              workflows.map((workflow, idx) => (
                <WorkflowItem 
                  key={idx}
                  item={workflow} 
                  onClick={() => {
                    mutation.mutate(workflow.id)
                    props.setOpen(false)
                  }}
                  selection={ITEM_UNSELECTED}
                />
              ))}
          </Stack>
        </ModalDialog>
      </Modal>
    </>
  )
}
