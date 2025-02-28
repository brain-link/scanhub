/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * TaskModal.tsx is responsible for rendering a modal with an interface to create a new task or to modify an existing task.
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
import { useMutation, useQuery } from 'react-query'

import { deviceApi, sequenceApi, taskApi } from '../api'
import { BaseTask, TaskOut, TaskType } from '../generated-client/exam'
import { MRISequence } from '../generated-client/sequence/api'
import { DeviceOut } from '../generated-client/device/api'
import { ModalPropsCreate, ModalPropsModify } from '../interfaces/components.interface'
import NotificationContext from '../NotificationContext'


function TaskForm(props: ModalPropsCreate | ModalPropsModify<TaskOut>) {
  // The form is in this separate component to make sure that the state is reset after closing the modal

  const [, showNotification] = React.useContext(NotificationContext)

  const initialTask: BaseTask = props.modalType == 'modify' ?
    {...props.item, status: 'UPDATED'}
  :
    {
      workflow_id: props.parentId,              // eslint-disable-line camelcase
      name: '',
      description: '',
      comment: undefined,
      type: TaskType.ProcessingTask,
      status: 'NEW',
      args: {},
      artifacts: {},
      destinations: {},
      is_template: props.createTemplate,        // eslint-disable-line camelcase
    }

  const [task, setTask] = React.useState<BaseTask>(initialTask);

  let sequenceParametersJson: {fov: {[key: string]: number}, fov_offset: {[key: string]: number}};
  try {
    sequenceParametersJson = JSON.parse(task.args.sequence_parameters);
    if (sequenceParametersJson == undefined
      || sequenceParametersJson.fov == undefined
      || sequenceParametersJson.fov.X == undefined
      || sequenceParametersJson.fov.Y == undefined
      || sequenceParametersJson.fov.Z == undefined
      || sequenceParametersJson.fov_offset == undefined
      || sequenceParametersJson.fov_offset.X == undefined
      || sequenceParametersJson.fov_offset.Y == undefined
      || sequenceParametersJson.fov_offset.Z == undefined) {
        throw Error()
      }
  } catch {
    sequenceParametersJson = {
      'fov': {
        'X': 0,
        'Y': 0,
        'Z': 0
      },
      'fov_offset': {
        'X': 0,
        'Y': 0,
        'Z': 0
      }
    }
  }

  // New argument
  const [argKey, setArgKey] = React.useState<string>('')
  const [argVal, setArgVal] = React.useState<string>('')

  // New Destination
  const [destinationKey, setDestinationKey] = React.useState<string>('')
  const [destinationVal, setDestinationVal] = React.useState<string>('')

  // New Artifact
  const [artifactKey, setArtifactKey] = React.useState<string>('')
  const [artifactVal, setArtifactVal] = React.useState<string>('')

  // Post a new/modified task and reset
  const mutation = 
    props.modalType == 'modify' ?
      useMutation(async () => {
        await taskApi
          .updateTaskApiV1ExamTaskTaskIdPut(props.item.id, task)
          .then(() => {
            props.onSubmit()
            showNotification({message: 'Updated Task.', type: 'success'})
          })
      })
    :
      useMutation(async () => {
        await taskApi
          .createTaskApiV1ExamTaskNewPost(task)
          .then(() => {
            props.onSubmit()
            showNotification({message: 'Created Task.', type: 'success'})
          })
      })

  const {
    data: sequences,
    // isLoading: isLoadingSequences,
    // isError: isErrorSequences,
    // refetch: refetchSequences,
  } = useQuery<MRISequence[]>({
    queryKey: ['sequences'],
    queryFn: async () => {
      return await sequenceApi
        .getMriSequencesEndpointApiV1MriSequencesGet()
        .then((result) => {
          return result.data
        })
    },
  })

  const {
    data: devices,
    // isLoading: isLoadingDevices,
    // isError: isErrorDevices,
    // refetch: refetchDevices,
  } = useQuery<DeviceOut[]>({
    queryKey: ['devices'],
    queryFn: async () => {
      return await deviceApi
        .getDevicesApiV1DeviceGet()
        .then((result) => {
          return result.data
        })
    },
  })

  const title = props.modalType == 'modify' ? 'Update Task' : 'Create New Task'

  return (
    <>
      <Typography id='basic-modal-dialog-title' component='h2' level='inherit' fontSize='1.25em' mb='0.25em'>
        {title}
      </Typography>

      <Stack direction='row' spacing={4} useFlexGap sx={{ flexWrap: 'wrap' }}>
        <Stack spacing={1}>
          <FormLabel>Name</FormLabel>
          <Input
            name={'name'}
            onChange={(e) => setTask({ ...task, [e.target.name]: e.target.value })}
            value={task.name}
          />
        </Stack>
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
        </Stack>
        <Stack spacing={1}>
          <FormLabel>Description</FormLabel>
          <Textarea
            minRows={2}
            name={'description'}
            onChange={(e) => setTask({ ...task, [e.target.name]: e.target.value })}
            defaultValue={task.description}
          />
        </Stack>
        {
          !task.is_template ?
            <Stack spacing={1}>
              <FormLabel>Comment</FormLabel>
              <Textarea
                minRows={2}
                name={'comment'}
                onChange={(e) => setTask({ ...task, [e.target.name]: e.target.value })}
                defaultValue={task.comment}
              />
            </Stack>
          :
            undefined
        }
      </Stack>

      {
        (task.type == TaskType.DeviceTaskSimulator || task.type == TaskType.DeviceTaskSdk) ?
          <Stack direction='row' spacing={4} useFlexGap sx={{ flexWrap: 'wrap' }}>
            <Stack spacing={1}>
              <FormLabel>Sequence</FormLabel>
              <Select
                value={task.args.sequence_id ? task.args.sequence_id : null}
                placeholder={'Select a sequence...'}
                size='sm'
                onChange={(event, value) => {
                  if (value) {
                    setTask({ ...task, args: { ...task.args, 'sequence_id': value.toString() } })
                  }
                }}
              >
                {sequences?.map((sequence) => {
                  return (
                    <Option key={sequence.name + ' (' + sequence._id + ')'} value={sequence._id}>
                      {sequence.name}
                    </Option>
                  )
                })}
              </Select>
            </Stack>
            <Stack spacing={1}>
              <FormLabel>Device</FormLabel>
              <Select
                value={task.args.device_id ? task.args.device_id : null}
                placeholder={'Select a device...'}
                size='sm'
                onChange={(event, value) => {
                  if (value) {
                    setTask({ ...task, args: { ...task.args, 'device_id': value.toString() } })
                  }
                }}
              >
                {devices?.map((device) => {
                  return (
                    <Option key={device.id} value={device.id}>
                      {device.name}
                    </Option>
                  )
                })}
              </Select>
            </Stack>
            <Stack spacing={1}>
              <FormLabel>Field of View</FormLabel>
              <Stack spacing={1} direction={'row'}>
                {['X', 'Y', 'Z'].map((index) => [
                  <FormLabel key={'FormLabelFov' + index}>{index}</FormLabel>,
                  <Input
                    key={'InputFov' + index}
                    type="number"
                    size='sm'
                    slotProps={ {input: {min: 0, max: 30000}} }
                    value={sequenceParametersJson.fov[index]}
                    endDecorator="px"
                    onChange={(event) => {
                      sequenceParametersJson.fov[index] = event.target.valueAsNumber
                      setTask({...task, args: { ...task.args, 'sequence_parameters': JSON.stringify(sequenceParametersJson) } })
                    }}
                  />
                  ])}
              </Stack>
            </Stack>
            <Stack spacing={1}>
              <FormLabel>Field of View Offset</FormLabel>
              <Stack spacing={1} direction={'row'}>
                {['X', 'Y', 'Z'].map((index) => [
                  <FormLabel key={'FormLabelFovOffset' + index}>{index}</FormLabel>,
                  <Input
                    key={'InputFovOffset' + index}
                    type="number"
                    size='sm'
                    slotProps={ {input: {min: 0, max: 30000}} }
                    value={sequenceParametersJson.fov_offset[index]}
                    endDecorator="px"
                    onChange={(event) => {
                      sequenceParametersJson.fov_offset[index] = event.target.valueAsNumber
                      setTask({...task, args: { ...task.args, 'sequence_parameters': JSON.stringify(sequenceParametersJson) } })
                    }}
                  />
                  ])}
              </Stack>
            </Stack>
          </Stack>
        : undefined
      }

      <Stack direction='row' spacing={4} useFlexGap sx={{ flexWrap: 'wrap' }}>

        <Stack spacing={1}>
          <FormLabel>Arguments</FormLabel>
          <Stack direction='row' spacing={1}>
            <FormControl>
              <FormLabel>Key</FormLabel>
              <Input onChange={(e) => setArgKey(e.target.value)} size='sm' value={argKey} />
            </FormControl>

            <FormControl>
              <FormLabel>Value</FormLabel>
              <Stack direction='row' spacing={1}>
                <Input onChange={(e) => setArgVal(e.target.value)} size='sm' value={argVal} />
                <IconButton
                  onClick={() => {
                    setTask({ ...task, args: { ...task.args, [argKey]: argVal } })
                    setArgKey('')
                    setArgVal('')
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
              <Input onChange={(e) => setDestinationKey(e.target.value)} size='sm' value={destinationKey} />
            </FormControl>

            <FormControl>
              <FormLabel>Value</FormLabel>
              <Stack direction='row' spacing={1}>
                <Input onChange={(e) => setDestinationVal(e.target.value)} size='sm' value={destinationVal} />
                <IconButton
                  onClick={() => {
                    setTask({ ...task, destinations: { ...task.destinations, [destinationKey]: destinationVal } })
                    setDestinationKey('')
                    setDestinationVal('')
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
              <Input onChange={(e) => setArtifactKey(e.target.value)} size='sm' value={artifactKey} />
            </FormControl>

            <FormControl>
              <FormLabel>Value</FormLabel>
              <Stack direction='row' spacing={1}>
                <Input onChange={(e) => setArtifactVal(e.target.value)} size='sm' value={artifactVal} />
                <IconButton
                  onClick={() => {
                    setTask({ ...task, artifacts: { ...task.artifacts, [artifactKey]: artifactVal } })
                    setArtifactKey('')
                    setArtifactVal('')
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
                      const tmpArtifacts = { ...prevTask.artifacts }
                      delete tmpArtifacts[artifact[0]]
                      return { ...prevTask, artifacts: tmpArtifacts }
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
          if (task.name == '') {
            showNotification({message: 'Task name must not be empty.', type: 'warning'})
          }
          else if (task.description == '') {
            showNotification({message: 'Task description must not be empty.', type: 'warning'})
          }
          else {
            mutation.mutate()
            props.setOpen(false)
          }
        }}
      >
        Save
      </Button>
    </>
  )
}


export default function TaskModal(props: ModalPropsCreate | ModalPropsModify<TaskOut>) {


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
        sx={{ width: '75vw', maxHeight: 'calc(100vh - 2 * var(--Navigation-height))', borderRadius: 'md', p: 5, overflow: 'auto'}}
      >
        <ModalClose
          sx={{
            top: '10px',
            right: '10px',
            borderRadius: '50%',
            bgcolor: 'background.body',
          }}
        />
        <TaskForm {...props} />
      </ModalDialog>
    </Modal>
  )
}
