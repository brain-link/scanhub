/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * TaskModifyModal.tsx is responsible for rendering a modal with an interface to modify an existing task.
 */
import AddSharpIcon from '@mui/icons-material/AddSharp'
import ClearIcon from '@mui/icons-material/Clear'
import Button from '@mui/joy/Button'
import FormControl from '@mui/joy/FormControl'
import FormLabel from '@mui/joy/FormLabel'
import IconButton from '@mui/joy/IconButton'
import Input from '@mui/joy/Input'
import Modal from '@mui/joy/Modal'
import ModalClose from '@mui/joy/ModalClose'
import ModalDialog from '@mui/joy/ModalDialog'
import Option from '@mui/joy/Option'
import Select from '@mui/joy/Select'
import Stack from '@mui/joy/Stack'
import Textarea from '@mui/joy/Textarea'
import Typography from '@mui/joy/Typography'
import * as React from 'react'
import { useMutation } from 'react-query'

import LoginContext from '../LoginContext'
import { taskApi } from '../api'
import { BaseTask, TaskOut, TaskType } from '../generated-client/exam'
import { ModalPropsModify } from '../interfaces/components.interface'
import NotificationContext from '../NotificationContext'


export default function TaskModifyModal(props: ModalPropsModify<TaskOut>) {
  const [, showNotification] = React.useContext(NotificationContext)

  const [task, setTask] = React.useState<BaseTask>({
    workflow_id: props.item.workflow_id,              // eslint-disable-line camelcase
    description: props.item.description,
    type: props.item.type,
    status: props.item.status,
    args: props.item.args,
    artifacts: props.item.artifacts,
    destinations: props.item.destinations,
    is_template: props.item.is_template,              // eslint-disable-line camelcase
    is_frozen: props.item.is_frozen,                  // eslint-disable-line camelcase
  })

  // New argument
  const [argKey, setArgKey] = React.useState<string>('')
  const [argVal, setArgVal] = React.useState<string>('')

  // New Destination
  const [destinationKey, setDestinationKey] = React.useState<string>('')
  const [destinationVal, setDestinationVal] = React.useState<string>('')

  // New Artifact
  const [artifactKey, setArtifactKey] = React.useState<string>('')
  const [artifactVal, setArtifactVal] = React.useState<string>('')

  const [user] = React.useContext(LoginContext)

  // Post a new exam template and refetch exam table
  const mutation = useMutation(async () => {
    await taskApi
      .updateTaskApiV1ExamTaskTaskIdPut(
        props.item.id, 
        task, 
        {headers: { Authorization: 'Bearer ' + user?.access_token }}
      )
      .then(() => {
        props.onSubmit()
      })
      .catch(() => {
        showNotification({message: 'Could not update the Task!', type: 'warning'})
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
        sx={{ borderRadius: 'md', p: 5 }}
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

        <Stack direction='row' spacing={4}>
          <Stack spacing={1}>
            <FormLabel>Type</FormLabel>
            <Select
              defaultValue={task.type}
              placeholder={task.type}
              size='sm'
              onChange={(e: React.SyntheticEvent | null, key: TaskType | null) => {
                // Only set type if key is not null
                key ? setTask({ ...task, ['type']: TaskType[key as keyof typeof TaskType] }) : () => {}
              }}
            >
              {Object.keys(TaskType).map((key) => (
                <Option key={key} value={key}>
                  {TaskType[key as keyof typeof TaskType]}
                </Option>
              ))}
            </Select>

            <FormLabel>Comment</FormLabel>
            <Textarea
              minRows={2}
              name={'description'}
              onChange={(e) => setTask({ ...task, [e.target.name]: e.target.value })}
              defaultValue={task.description}
            />
          </Stack>

          <Stack spacing={1}>
            <FormLabel>Arguments</FormLabel>

            <Stack direction='row' spacing={1}>
              <FormControl>
                <FormLabel>Key</FormLabel>
                <Input onChange={(e) => setArgKey(e.target.value)} size='sm' />
              </FormControl>

              <FormControl>
                <FormLabel>Value</FormLabel>
                <Stack direction='row' spacing={1}>
                  <Input onChange={(e) => setArgVal(e.target.value)} size='sm' />
                  <IconButton
                    onClick={() => {
                      setTask({ ...task, args: { ...task.args, [argKey]: argVal } })
                    }}
                    size='sm'
                  >
                    <AddSharpIcon />
                  </IconButton>
                </Stack>
              </FormControl>
            </Stack>

            {task &&
              Object.entries(task.args).map((arg, index) => (
                <Stack direction='row' spacing={2} alignItems='center' key={index}>
                  <Typography level='body-sm' textColor='text.tertiary'>
                    {arg[0]}: {arg[1]}
                  </Typography>
                  <IconButton
                    size='sm'
                    onClick={() => {
                      setTask((prevTask) => {
                        const tmpArgs = { ...prevTask.args }
                        delete tmpArgs[arg[0]]
                        return { ...prevTask, args: tmpArgs }
                      })
                    }}
                  >
                    <ClearIcon />
                  </IconButton>
                </Stack>
              ))}
          </Stack>

          <Stack spacing={1}>
            <FormLabel>Destinations</FormLabel>

            <Stack direction='row' spacing={1}>
              <FormControl>
                <FormLabel>Key</FormLabel>
                <Input onChange={(e) => setDestinationKey(e.target.value)} size='sm' />
              </FormControl>

              <FormControl>
                <FormLabel>Value</FormLabel>
                <Stack direction='row' spacing={1}>
                  <Input onChange={(e) => setDestinationVal(e.target.value)} size='sm' />
                  <IconButton
                    onClick={() => {
                      setTask({ ...task, destinations: { ...task.destinations, [destinationKey]: destinationVal } })
                    }}
                    size='sm'
                  >
                    <AddSharpIcon />
                  </IconButton>
                </Stack>
              </FormControl>
            </Stack>

            {task &&
              Object.entries(task.destinations).map((destination, index) => (
                <Stack direction='row' spacing={2} alignItems='center' key={index}>
                  <Typography level='body-sm' textColor='text.tertiary'>
                    {destination[0]}: {destination[1]}
                  </Typography>
                  <IconButton
                    size='sm'
                    onClick={() => {
                      setTask((prevTask) => {
                        const tmpDestinations = { ...prevTask.destinations }
                        delete tmpDestinations[destination[0]]
                        return { ...prevTask, destinations: tmpDestinations }
                      })
                    }}
                  >
                    <ClearIcon />
                  </IconButton>
                </Stack>
              ))}
          </Stack>

          <Stack spacing={1}>
            <FormLabel>Artifacts</FormLabel>

            <Stack direction='row' spacing={1}>
              <FormControl>
                <FormLabel>Key</FormLabel>
                <Input onChange={(e) => setArtifactKey(e.target.value)} size='sm' />
              </FormControl>

              <FormControl>
                <FormLabel>Value</FormLabel>
                <Stack direction='row' spacing={1}>
                  <Input onChange={(e) => setArtifactVal(e.target.value)} size='sm' />
                  <IconButton
                    onClick={() => {
                      setTask({ ...task, artifacts: { ...task.artifacts, [artifactKey]: artifactVal } })
                    }}
                    size='sm'
                  >
                    <AddSharpIcon />
                  </IconButton>
                </Stack>
              </FormControl>
            </Stack>

            {task &&
              Object.entries(task.artifacts).map((artifact, index) => (
                <Stack direction='row' spacing={2} alignItems='center' key={index}>
                  <Typography level='body-sm' textColor='text.tertiary'>
                    {artifact[0]}: {artifact[1]}
                  </Typography>
                  <IconButton
                    size='sm'
                    onClick={() => {
                      setTask((prevTask) => {
                        const tmpArtifacts = { ...prevTask.args }
                        delete tmpArtifacts[artifact[0]]
                        return { ...prevTask, args: tmpArtifacts }
                      })
                    }}
                  >
                    <ClearIcon />
                  </IconButton>
                </Stack>
              ))}
          </Stack>
        </Stack>

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
      </ModalDialog>
    </Modal>
  )
}
