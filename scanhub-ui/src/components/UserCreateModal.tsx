/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * UserCreateModal.tsx is responsible for rendering a modal with an interface
 * to create a new user.
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
import Stack from '@mui/joy/Stack'
import Typography from '@mui/joy/Typography'
import Select from '@mui/joy/Select'
import Option from '@mui/joy/Option';

import { userApi } from '../api'
import { UserRole, User } from '../generated-client/userlogin'
import { ModalProps } from '../interfaces/components.interface'
import NotificationContext from '../NotificationContext'


interface BaseFormEntry {
  key: string,
  label: string
}

interface TextFormEntry extends BaseFormEntry {
  type: 'text'
  required?: boolean
  placeholder?: string
};

interface PasswordFormEntry extends BaseFormEntry {
  type: 'password'
  required?: boolean
  placeholder?: string
};

interface SelectFormEntry extends BaseFormEntry {
  type: 'select'
  options: string[]
};

type FormEntry = TextFormEntry | SelectFormEntry | PasswordFormEntry;

// User form items, order is row wise
const createUserFormContent: FormEntry[] = [
  { type: 'text', key: 'username', label: 'Username', placeholder: 'Username', required: true },
  { type: 'text', key: 'first_name', label: 'First name', placeholder: 'First name', required: true },
  { type: 'text', key: 'last_name', label: 'Last name', placeholder: 'Last name', required: true },
  { type: 'text', key: 'email', label: 'e-Mail', placeholder: 'e-Mail', required: false },
  { type: 'select', key: 'role', label: 'Role', options: Object.values(UserRole) },
  { type: 'password', key: 'access_token', label: 'Password', placeholder: 'At least 12 characters.', required: true },
]


function UserForm(props: ModalProps) {
  // The form is in this separate component to make sure that the state is reset after closing the modal

  const [, showNotification] = React.useContext(NotificationContext)
  // eslint-disable-next-line camelcase

  const [user, setUser] = React.useState<User>({
    username: '',
    first_name: '',   // eslint-disable-line camelcase
    last_name: '',    // eslint-disable-line camelcase
    email: '',
    role: UserRole.Medical, // eslint-disable-next-line camelcase
    token_type: 'password',   // eslint-disable-line camelcase
    access_token: '',         // eslint-disable-line camelcase
  })

  // Post a new record and refetch records table
  const mutation = useMutation({
    mutationKey: ['users'],
    mutationFn: async () => {
      await userApi
        .createUserApiV1UserloginCreateuserPost(user)
        .then(() => {
          props.onSubmit()
          showNotification({message: 'Created user ' + user.username, type: 'success'})
        })
        .catch((err) => {
          let errorMessage = null
          if (err?.response?.data?.detail?.[0]?.msg) {
            errorMessage = 'Error at creating new user. Detail: ' + err.response.data.detail[0].msg
          } else if (err?.response?.data?.detail) {
            errorMessage = 'Error at creating new user. Detail: ' + err.response.data.detail
          } else {
            errorMessage = 'Error at creating new user.'
          }
          showNotification({message: errorMessage, type: 'warning'})
        })
    },
  })

  function renderFormEntry(item: FormEntry, index: number) {
    if (item.type == 'text') {
      return (
        <Grid key={index} md={6}>
          <FormLabel sx={{marginBottom: 1}}>{item.label}</FormLabel>
          <Input
            name={item.key}
            onChange={(e) => setUser({ ...user, [e.target.name]: e.target.value })}
            placeholder={item.placeholder}
            required={item.required}
          />
        </Grid>
      )
    }
    else if (item.type == 'password') {
      return (
        <Grid key={index} md={6}>
          <FormLabel sx={{marginBottom: 1}}>{item.label}</FormLabel>
          <Input
            name={item.key}
            onChange={(e) => setUser({ ...user, [e.target.name]: e.target.value })}
            placeholder={item.placeholder}
            required={item.required}
            type={'password'}
          />
        </Grid>
      )
    }
    else if (item.type == 'select') {
      return (
        <Grid key={index} md={6}>
          <FormLabel sx={{marginBottom: 1}}>{item.label}</FormLabel>
          <Select 
            onChange={(event, value) => setUser({ ...user, [item.key]: value })}
            required
          >
            {item.options.map((option) => 
              <Option key={option} value={option}>{option}</Option>
            )}
          </Select>
        </Grid>
      )
    }
  }

  return (
    <>
      <Typography id='basic-modal-dialog-title' component='h2' level='inherit' fontSize='1.25em' mb='0.25em'>
        Create New User
      </Typography>

      <form
        onSubmit={(event) => {
          event.preventDefault()
          if (user.access_token.length < 12) {
            showNotification({message: 'Password must have at least 12 characters!', type: 'warning'})
          }
          else {
            mutation.mutate()
            props.setOpen(false)
          }
        }}
      >
        <Stack spacing={5}>
          <Grid container rowSpacing={1.5} columnSpacing={5}>
            {createUserFormContent.map(renderFormEntry)}
          </Grid>
          <Button size='sm' type='submit' sx={{ maxWidth: 100 }}>
            Submit
          </Button>
        </Stack>
      </form>
    </>
  )
}


export default function UserCreateModal(props: ModalProps) {
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
            bgcolor: 'background.body',
          }}
        />
        <UserForm {...props} />
      </ModalDialog>
    </Modal>
  )
}
