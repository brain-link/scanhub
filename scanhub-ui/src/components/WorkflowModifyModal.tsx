/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * WorkflowModifyModal.tsx is responsible for rendering a modal with an interface
 * to modify an existing workflow.
 */
import Button from '@mui/joy/Button'
import FormLabel from '@mui/joy/FormLabel'
import Input from '@mui/joy/Input'
import Modal from '@mui/joy/Modal'
import ModalClose from '@mui/joy/ModalClose'
import ModalDialog from '@mui/joy/ModalDialog'
import Stack from '@mui/joy/Stack'
import Typography from '@mui/joy/Typography'
import * as React from 'react'
import { useMutation } from 'react-query'

import { workflowsApi } from '../api'
import { BaseWorkflow, WorkflowOut } from '../generated-client/exam'
import { ModalPropsModify } from '../interfaces/components.interface'
import NotificationContext from '../NotificationContext'

export default function WorkflowModifyModal(props: ModalPropsModify<WorkflowOut>) {
  const [, showNotification] = React.useContext(NotificationContext)
  
  const [workflow, setWorkflow] = React.useState<BaseWorkflow>({
    name: props.item.name,
    comment: props.item.comment,
    exam_id: props.item.exam_id,              // eslint-disable-line camelcase
    is_finished: props.item.is_finished,      // eslint-disable-line camelcase
    is_template: props.item.is_template,      // eslint-disable-line camelcase
    is_frozen: props.item.is_frozen,          // eslint-disable-line camelcase
  })

  // Post a new exam template and refetch exam table
  const mutation = useMutation(async () => {
    await workflowsApi
      .updateWorkflowApiV1ExamWorkflowWorkflowIdPut(props.item.id, workflow)
      .then(() => {
        props.onSubmit()
      })
      .catch(() => {
        showNotification({message: 'Could not update Workflow!', type: 'warning'})
      })
  })

  return (
    <Modal
      open={props.isOpen}
      color='neutral'
      onClose={() => props.setOpen(false)}
      sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}
    >
      <ModalDialog
        aria-labelledby='basic-modal-dialog-title'
        aria-describedby='basic-modal-dialog-description'
        sx={{ width: '50vw', borderRadius: 'md', p: 5 }}
      >
        <ModalClose
          sx={{
            top: '10px',
            right: '10px',
            borderRadius: '50%',
            bgcolor: 'background.body',
          }}
        />

        <Typography id='basic-modal-dialog-title' component='h2' level='inherit' fontSize='1.25em' mb='0.25em'>
          Update Workflow
        </Typography>

        <Stack spacing={1}>
          <FormLabel>Name</FormLabel>
          <Input
            name={'name'}
            onChange={(e) => setWorkflow({ ...workflow, [e.target.name]: e.target.value })}
            defaultValue={workflow.name}
          />

          <FormLabel>Comment</FormLabel>
          <Input
            name={'comment'}
            onChange={(e) => setWorkflow({ ...workflow, [e.target.name]: e.target.value })}
            defaultValue={workflow.comment}
          />

          <Button
            size='sm'
            sx={{ maxWidth: 120 }}
            onClick={(event) => {
              event.preventDefault()
              if (workflow.name == '') {
                showNotification({message: 'Workflow name must not be empty.', type: 'warning'})
              }
              else {
                mutation.mutate()
                props.setOpen(false)
              }
            }}
          >
            Save
          </Button>
        </Stack>
      </ModalDialog>
    </Modal>
  )
}
