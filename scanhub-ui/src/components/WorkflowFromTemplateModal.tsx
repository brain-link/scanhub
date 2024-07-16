/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * WorkflowFromTemplateModal.tsx is responsible for rendering a
 * workflow template selection interface to generate a new workflow instance.
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
import { CreateInstanceModalInterface } from '../interfaces/components.interface'
import WorkflowTemplateItem from './WorkflowTemplateItem'

export default function WorkflowFromTemplateModal(props: CreateInstanceModalInterface) {
  const [user] = useContext(LoginContext)

  // const {data: exams, isLoading, isError} = useQuery<ExamOut[]>({
  const { data: workflows } = useQuery<WorkflowOut[]>({
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

  const mutation = useMutation(async (id: string) => {
    await workflowsApi
      .createWorkflowFromTemplateApiV1ExamWorkflowPost(String(props.parentId), id, {
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
      {/* <IconButton 
        variant='soft'
        onClick={() => {setModalOpen(true)}}
      >
        <AddSharpIcon />
      </IconButton> */}

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
                  <WorkflowTemplateItem data={workflow} onClicked={() => {}} onDeleted={() => {}} />
                </ListItemButton>
              ))}
          </List>
        </ModalDialog>
      </Modal>
    </>
  )
}
