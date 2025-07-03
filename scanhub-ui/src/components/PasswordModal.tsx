/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * PasswordModal.tsx is responsible for rendering a modal with an interface
 * to change the password of a user.
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
import { useMutation } from '@tanstack/react-query'

import { userApi } from '../api'
import { ModalPropsModify } from '../interfaces/components.interface'
import LoginContext from '../LoginContext'
import NotificationContext from '../NotificationContext'


function PasswordForm(props: ModalPropsModify<string>) {
  // The form is in this separate component to make sure that the state is reset after closing the modal

  const [passwordOfRequester, setPasswordOfRequester] = React.useState('');
  const [newPassword1, setNewPassword1] = React.useState('');
  const [newPassword2, setNewPassword2] = React.useState('');

  const [, showNotification] = React.useContext(NotificationContext)
  const [user, ] = React.useContext(LoginContext)

  const mutation = useMutation({
    mutationFn: async () => {
      await userApi.changePasswordApiV1UserloginChangepasswordPut(
        {
          password_of_requester: passwordOfRequester,   // eslint-disable-line camelcase
          username_to_change_password_for: props.item,  // eslint-disable-line camelcase
          newpassword: newPassword1
        }
      ).then(() => {
          props.onSubmit()
          showNotification({message: 'Updated password sucessfully.', type: 'success'})
        }
      ).catch(() => {
          showNotification({message: 'Error at updating password! Maybe your password was wrong.', type: 'warning'})
        }
      )
    }
  })

  return (
    <>
      <Typography id='basic-modal-dialog-title' component='h2' level='inherit' fontSize='1.25em' mb='0.25em'>
        {'Change Password for user ' + props.item}
      </Typography>

      <Stack spacing={1}>
        <FormLabel>Password of user {user?.username}</FormLabel>
        <Input
          name={'password'}
          type={'password'}
          onChange={(e) => setPasswordOfRequester(e.target.value)}
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
            if (passwordOfRequester == '') {
              showNotification({message: 'Password must not be empty.', type: 'warning'})
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


export default function PasswordModal(props: ModalPropsModify<string>) {
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
