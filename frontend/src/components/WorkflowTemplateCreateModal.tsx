// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
// PatientTable.tsx is responsible for rendering the patient table view.
import Typography from '@mui/joy/Typography'

import Button from '@mui/joy/Button'
import ModalDialog from '@mui/joy/ModalDialog'
import ModalClose from '@mui/joy/ModalClose'
import Input from '@mui/joy/Input'
import FormLabel from '@mui/joy/FormLabel'
import Modal from '@mui/joy/Modal'
import Stack from '@mui/joy/Stack'
import * as React from 'react'
import { useContext } from 'react'

import { useMutation } from 'react-query'
import { BaseWorkflow, WorkflowOut } from '../generated-client/exam';
import { workflowsApi } from '../api';
import { ModalComponentProps } from '../interfaces/components.interface'
import LoginContext from '../LoginContext'


export default function WorkflowTemplateCreateModal(props: ModalComponentProps<WorkflowOut>) {

  const [workflow, setWorkflow] = React.useState<BaseWorkflow>({comment: '', exam_id: undefined, is_finished: false, is_template: true, is_frozen: false})
  const [user, ] = useContext(LoginContext);

  // Post a new exam template and refetch exam table
  const mutation = useMutation(async () => {
    await workflowsApi.createWorkflowTemplateApiV1ExamWorkflowTemplatesPost(
      workflow,
      {headers: {Authorization: 'Bearer ' + user?.access_token}}
    )
    .then((response) => { props.onSubmit(response.data) })
    .catch((err) => { console.log(err) })
  })

  return (
    <Modal
      open={props.isOpen}
      color='neutral'
      onClose={() => props.setOpen(false)}
      sx={{display: 'flex', justifyContent: 'center', alignItems: 'center'}}
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
            defaultValue={ workflow.comment }
          />

          {/* TODO: Drop-down menu to select exam template */}
          <FormLabel>Exam ID</FormLabel>
          <Input
            name={'exam_id'}
            onChange={(e) => setWorkflow({ ...workflow, [e.target.name]: e.target.value })}
            defaultValue={ workflow.exam_id }
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
