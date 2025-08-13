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

import { DeviceCreationRequest } from '../openapi/generated-client/device'
import { ModalProps } from '../interfaces/components.interface'
import NotificationContext from '../NotificationContext'
import { deviceApi } from '../api'


function DeviceForm(props: ModalProps) {
  const [, showNotification] = React.useContext(NotificationContext)
  const [device, setDevice] = React.useState<DeviceCreationRequest>({ name: '', description: '' })
  const [credentialsUrl, setCredentialsUrl] = React.useState<string | null>(null)

  // Make device creation request and refetch devices table
  const mutation = useMutation({
    // Return the Blob so we can enable the download button after success
    mutationFn: async () => {
      const response = await deviceApi.createDeviceApiV1DeviceCreatedevicePost(device, {
        responseType: 'blob'
      })
      // Some clients already give you a Blob in response.data when responseType='blob'
      // Wrap in Blob to be safe if type is unknown/ArrayBuffer
      const blob = response?.data instanceof Blob
        ? response.data
        : new Blob([response.data], { type: 'application/json' })

      return blob
    },
    onSuccess: (blob: Blob) => {
      // Create object URL and enable the download button
      const url = URL.createObjectURL(blob)
      setCredentialsUrl(url)
      showNotification({ message: 'Device created. Credentials are ready to download.', type: 'success' })
    },
    onError: () => {
      showNotification({ message: 'Failed to create device.', type: 'warning' })
    }
  })

  const handleDownload = () => {
    if (!credentialsUrl) return
    const a = document.createElement('a')
    a.href = credentialsUrl
    a.download = 'device_credentials.json'
    a.style.display = 'none'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    // Keep URL alive in case the user wants to click again.
    // If you want to revoke right after download, call URL.revokeObjectURL(credentialsUrl) and setCredentialsUrl(null)
    props.setOpen(false) // Close modal after download
  }

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
          <Grid md={12}>
            <FormLabel sx={{marginBottom: 1}}>Device connection name</FormLabel>
            <Input
              onChange={(e) => setDevice({ ...device, name: e.target.value })}
              placeholder='Connection name'
              required
            />
          </Grid>
          <Grid md={12}>
            <FormLabel sx={{marginBottom: 1}}>Description</FormLabel>
            <Textarea 
              placeholder="Add a description..."
              minRows={3}
              onChange={(e) => setDevice({ ...device, description: e.target.value })}
            />
          </Grid>

          <Grid md={12} sx={{ display: 'flex', gap: 1 }}>
            {/* Buttons */}
            <Button
              size='sm'
              type='submit'
              loading={mutation.isPending}
              disabled={mutation.isPending || !device.name || !device.description || credentialsUrl !== null}
              sx={{ maxWidth: 200 }}
            >
              Create
            </Button>

            <Button
              size='sm'
              disabled={!credentialsUrl}
              onClick={handleDownload}
              sx={{ maxWidth: 200 }}
            >
              Download credentials
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
          width: '50vw',
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