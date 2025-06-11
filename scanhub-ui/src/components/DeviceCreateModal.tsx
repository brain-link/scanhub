/**
 * Copyright (C) 2025, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * DeviceCreateModal.tsx is responsible for rendering a modal with an interface
 * to create a new device.
 */
import * as React from 'react'
import { useMutation } from 'react-query'

import Button from '@mui/joy/Button'
import FormLabel from '@mui/joy/FormLabel'
import Grid from '@mui/joy/Grid'
import Input from '@mui/joy/Input'
import Modal from '@mui/joy/Modal'
import ModalClose from '@mui/joy/ModalClose'
import ModalDialog from '@mui/joy/ModalDialog'
import Typography from '@mui/joy/Typography'

import { DeviceCreationRequest } from '../generated-client/device'
import { ModalProps } from '../interfaces/components.interface'
import NotificationContext from '../NotificationContext'
import { deviceApi } from '../api'


interface BaseFormEntry {
  key: string,
  label: string
}

interface TextFormEntry extends BaseFormEntry {
  type: 'text'
  required?: boolean
  placeholder?: string
};

// Patient form items, order is row wise
const createPatientFormContent: TextFormEntry[] = [
  { type: 'text', key: 'title', label: 'Title', required: true },
  { type: 'text', key: 'description', label: 'Description', placeholder: '', required: true },
]


function DeviceForm(props: ModalProps) {
  const [, showNotification] = React.useContext(NotificationContext)

  const [deviceToken, setDeviceToken] = React.useState<string | undefined>(undefined);
  const [deviceId, setDeviceId] = React.useState<string | undefined>(undefined);

  const [device, setDevice] = React.useState<DeviceCreationRequest>({
    title: '',
    description: ''
  })

  // Post a new record and refetch records table
  const mutation = useMutation(async () => {
    await deviceApi
      .createDeviceApiV1DeviceCreatedevicePost(device)
      .then((response) => {
        props.onSubmit()
        setDeviceToken(response.data.device_token)
        setDeviceId(response.data.device_id)
        showNotification({message: 'Device created.', type: 'success'})
      })
  })

  function renderFormEntry(item: TextFormEntry, index: number) {
    if (item.type == 'text') {
      return (
        <Grid key={index} md={6}>
          <FormLabel sx={{marginBottom: 1}}>{item.label}</FormLabel>
          <Input
            name={item.key}
            onChange={(e) => setDevice({ ...device, [e.target.name]: e.target.value })}
            placeholder={item.placeholder}
            required={item.required}
            disabled={deviceId != undefined}
          />
        </Grid>
      )
    }
  }

  return (
    <>
      <Typography id='basic-modal-dialog-title' component='h2' level='inherit' fontSize='1.25em' mb='0.25em'>
        Create New Device
      </Typography>

      <form
        onSubmit={(event) => {
          event.preventDefault()
            mutation.mutate()
        }}
      >
        <Grid container rowSpacing={3} columnSpacing={5}>
          {createPatientFormContent.map((item, index) => renderFormEntry(item, index))}
          <Grid md={12}>
            <Button size='sm' type='submit' sx={{ maxWidth: 100 }} disabled={deviceId != undefined}>
              Create
            </Button>
          </Grid>
          {deviceId ?
            <>
              <Grid md={12}>
                <Typography color='primary' variant='soft'>
                  Copy the new device ID and token to that device, such that it can connect to Scanhub.
                </Typography>
                <Typography color='warning' variant='soft'>
                  The token will not be accessible later!
                </Typography>
              </Grid>
              <Grid md={12}>
                <Typography level='title-md'>
                  Device ID
                </Typography>
                <Typography>
                  {deviceId}
                </Typography>
              </Grid>
              <Grid md={12}>
                <Typography level='title-md'>
                  Device Token
                </Typography>
                <Typography level='body-sm' sx={{overflowWrap: 'break-word'}}>
                  {deviceToken}
                </Typography>
              </Grid>
            </>
            : undefined}
        </Grid>
      </form>
    </>
  )
}


export default function DeviceCreateModal(props: ModalProps) {
  return (
    <Modal
      open={props.isOpen}
      color='neutral'
      onClose={() => {
        props.setOpen(false)
      }}
      sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}
    >
      <ModalDialog
        aria-labelledby='basic-modal-dialog-title'
        aria-describedby='basic-modal-dialog-description'
        size='sm'
        sx={{
          width: '70vw',
          borderRadius: 'md',
          p: 5,
        }}
      >
        <ModalClose
          sx={{
            top: '10px',
            right: '10px',
            borderRadius: '50%',
          }}
        />
        <DeviceForm {...props} />
      </ModalDialog>
    </Modal>
  )
}