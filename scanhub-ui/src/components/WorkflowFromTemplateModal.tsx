/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * WorkflowFromTemplateModal.tsx is responsible for rendering a
 * workflow template selection interface to generate a new workflow.
 */
import List from '@mui/joy/List'
import ListItemButton from '@mui/joy/ListItemButton'
import Modal from '@mui/joy/Modal'
import ModalClose from '@mui/joy/ModalClose'
import ModalDialog from '@mui/joy/ModalDialog'
import DialogTitle from '@mui/material/DialogTitle'
import * as React from 'react'
import { useContext } from 'react'
import { useMutation } from 'react-query'
import { useQuery } from 'react-query'

import LoginContext from '../LoginContext'
import { workflowsApi } from '../api'
import { WorkflowOut } from '../generated-client/exam'
import { ModalPropsCreate } from '../interfaces/components.interface'
import WorkflowItem from './WorkflowItem'

export default function WorkflowFromTemplateModal(props: ModalPropsCreate) {
  const [user] = useContext(LoginContext)

  const { data: workflows } = useQuery<WorkflowOut[]>({
    queryKey: ['allWorkflowTemplates'],
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

  const mutation = useMutation(async (id: string) => {
    await workflowsApi
      .createWorkflowFromTemplateApiV1ExamWorkflowPost(String(props.parentId), id, props.createTemplate, {
        headers: { Authorization: 'Bearer ' + user?.access_token },
      })
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
          <DialogTitle>Exam Templates</DialogTitle>
          <List
            sx={{
              overflow: 'scroll',
              mx: 'calc(-1 * var(--ModalDialog-padding))',
              px: 'var(--ModalDialog-padding)',
            }}
          >
            {workflows &&
              workflows.map((workflow, idx) => (
                <ListItemButton
                  key={idx}
                  onClick={() => {
                    mutation.mutate(workflow.id)
                    props.setOpen(false)
                  }}
                >
                  <WorkflowItem data={workflow} refetchParentData={() => {}} />
                </ListItemButton>
              ))}
          </List>
        </ModalDialog>
      </Modal>
    </>
  )
}
