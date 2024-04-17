// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
// PatientTable.tsx is responsible for rendering the patient table view.
import * as React from 'react'
import Typography from '@mui/joy/Typography'
import Button from '@mui/joy/Button'
import ModalDialog from '@mui/joy/ModalDialog'
import ModalClose from '@mui/joy/ModalClose'
import Input from '@mui/joy/Input'
import FormLabel from '@mui/joy/FormLabel'
import Modal from '@mui/joy/Modal'
import Stack from '@mui/joy/Stack'
import Select from '@mui/joy/Select';
import Option from '@mui/joy/Option';


import { useMutation } from 'react-query'
import { BaseTask, TaskOut, TaskType } from "../generated-client/exam";
import { taskApi } from '../Api';
import { ModalComponentProps } from '../interfaces/components.interface'


export default function TaskTemplateCreateModal(props: ModalComponentProps<TaskOut>) {

  const [task, setTask] = React.useState<BaseTask>({
    workflow_id: undefined, description: '', type: TaskType.ProcessingTask, status: {}, args: {}, artifacts: {}, task_destinations: [], is_template: true, is_frozen: false
  })

  // Post a new exam template and refetch exam table
  const mutation = useMutation(async () => {
    await taskApi.createTaskTemplateApiV1ExamTaskTemplatePost(task).then((response) => { props.onSubmit(response.data) }).catch((err) => { console.log(err) })
  })

  const getType = (str: keyof typeof TaskType) => {
    return TaskType[str]
  }

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
            name={'description'}
            onChange={(e) => setTask({ ...task, [e.target.name]: e.target.value })}
            defaultValue={ task.description }
          />

          {/* TODO: Drop-down menu to select exam template */}
          <FormLabel>Workflow ID</FormLabel>
          <Input
            name={'workflow_id'}
            onChange={(e) => setTask({ ...task, [e.target.name]: e.target.value })}
            defaultValue={ task.workflow_id }
          />

          <FormLabel>Type</FormLabel>
          <Select defaultValue={task.type} placeholder={task.type}>
            {
              Object.keys(TaskType).map((key) => (
                <Option key={key} value={key}>
                  { TaskType[key] }
                </Option>
              ))
            }
          </Select>

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
