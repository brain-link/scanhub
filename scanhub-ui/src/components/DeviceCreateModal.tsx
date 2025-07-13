/**
 * Copyright (C) 2025, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * DeviceCreateModal.tsx is responsible for rendering a modal with an interface
 * to create a new device.
 */
import * as React from 'react'
import { useMutation } from '@tanstack/react-query'

import Button from '@mui/joy/Button'
import FormLabel from '@mui/joy/FormLabel'
import Textarea from '@mui/joy/Textarea'
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


function DeviceForm(props: ModalProps) {
  const [, showNotification] = React.useContext(NotificationContext)
  const [device, setDevice] = React.useState<DeviceCreationRequest>({
    name: '',
    description: ''
  })

  // Make device creation request and refetch devices table
  const mutation = useMutation({
    mutationFn: async () => {
      const response = await deviceApi.createDeviceApiV1DeviceCreatedevicePost(device, {
        responseType: 'blob'
      })
      // Create blob URL
      const blob = new Blob([response.data], { type: 'application/json' });
      const url = window.URL.createObjectURL(blob);

      // Create a link and click it to trigger download
      const a = document.createElement('a');
      a.href = url;
      a.download = 'device_credentials.json'; // Desired filename
      a.style.display = 'none';

      // Append, click, and clean up
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);

      props.onSubmit()
      showNotification({message: 'Device created.', type: 'success'})
    }
  })

  return (
    <>
      <Typography id='basic-modal-dialog-title' component='h2' level='inherit' fontSize='1.25em' mb='0.25em'>
        Create new device connection
      </Typography>

      <form
        onSubmit={(event) => {
          event.preventDefault()
            mutation.mutate()
        }}
      >
        <Grid container rowSpacing={3} columnSpacing={5}>
          <Grid md={6}>
            <FormLabel sx={{marginBottom: 1}}>Device connection name</FormLabel>
            <Input
              onChange={(e) => setDevice({ ...device, name: e.target.value })}
              placeholder='Connection name'
              required
            />
          </Grid>
          <Grid md={6}>
            <FormLabel sx={{marginBottom: 1}}>Description</FormLabel>
            <Textarea 
              placeholder="Add a description..."
              minRows={3}
              onChange={(e) => setDevice({ ...device, description: e.target.value })}
            />
          </Grid>

          <Grid md={12}>
            <Button size='sm' type='submit' sx={{ maxWidth: 120 }}>
              Create
            </Button>
          </Grid>
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