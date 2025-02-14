/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * PasswordModal.tsx is responsible for rendering a modal with an interface
 * to change the users own password.
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

import { userApi } from '../api'
import { ModalProps } from '../interfaces/components.interface'
import NotificationContext from '../NotificationContext'


function PasswordForm(props: ModalProps) {
  // The form is in this separate component to make sure that the state is reset after closing the modal

  const [oldPassword, setOldPassword] = React.useState('');
  const [newPassword1, setNewPassword1] = React.useState('');
  const [newPassword2, setNewPassword2] = React.useState('');

  const [, showNotification] = React.useContext(NotificationContext)

  const mutation = useMutation(async () => {
    await userApi.changeOwnPasswordApiV1UserloginChangeownpasswordPut({ oldpassword: oldPassword, newpassword: newPassword1 })
      .then(() => {
        props.onSubmit()
        showNotification({message: 'Updated password sucessfully.', type: 'success'})
      })
      .catch(() => {
        showNotification({message: 'Error at updating password! Maybe the old password was wrong.', type: 'warning'})
      })
  })


  return (
    <>
      <Typography id='basic-modal-dialog-title' component='h2' level='inherit' fontSize='1.25em' mb='0.25em'>
        Change Password
      </Typography>

      <Stack spacing={1}>
        <FormLabel>Old Password</FormLabel>
        <Input
          name={'oldpassword'}
          type={'password'}
          onChange={(e) => setOldPassword(e.target.value)}
        />

        <FormLabel>New Password</FormLabel>
        <Input
          name={'newpassword1'}
          type={'password'}
          onChange={(e) => setNewPassword1(e.target.value)}
        />

        <FormLabel>Repeat New Password</FormLabel>
        <Input
          name={'newpassword2'}
          type={'password'}
          onChange={(e) => setNewPassword2(e.target.value)}
        />

        <Button
          size='sm'
          sx={{ maxWidth: 120 }}
          onClick={(event) => {
            event.preventDefault()
            if (oldPassword == '') {
              showNotification({message: 'Old password must not be empty.', type: 'warning'})
            }
            else if (newPassword1.length < 12) {
              showNotification({message: 'The new password must at least have 12 characters.', type: 'warning'})
            }
            else if (newPassword1 != newPassword2) {
              showNotification({message: 'The new passwords do not match, please enter them again.', type: 'warning'})
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
    </>
  )
}


export default function PasswordModal(props: ModalProps) {
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
        <PasswordForm {...props} />
      </ModalDialog>
    </Modal>
  )
}
