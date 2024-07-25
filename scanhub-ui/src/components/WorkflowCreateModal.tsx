/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * WorkflowCreateModal.tsx is responsible for rendering a modal with an interface
 * to create a new workflow.
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
import { useContext } from 'react'
import { useMutation } from 'react-query'

import LoginContext from '../LoginContext'
import { workflowsApi } from '../api'
import { BaseWorkflow } from '../generated-client/exam'
import { ModalPropsCreate } from '../interfaces/components.interface'

export default function WorkflowCreateModal(props: ModalPropsCreate) {
  const [workflow, setWorkflow] = React.useState<BaseWorkflow>({
    comment: '',
    exam_id: props.parentId,                // eslint-disable-line camelcase
    is_finished: false,                     // eslint-disable-line camelcase
    is_template: props.createTemplate,      // eslint-disable-line camelcase
    is_frozen: false,                       // eslint-disable-line camelcase
  })
  const [user] = useContext(LoginContext)

  // Post a new exam template and refetch exam table
  const mutation = useMutation(async () => {
    await workflowsApi
      .createWorkflowApiV1ExamWorkflowNewPost(workflow, {
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
          Create New Workflow Template
        </Typography>

        <Stack spacing={1}>
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
              mutation.mutate()
              props.setOpen(false)
            }}
          >
            Save
          </Button>
        </Stack>
      </ModalDialog>
    </Modal>
  )
}
