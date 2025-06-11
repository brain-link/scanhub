/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * UserManagementView.tsx is responsible for rendering the user table and for adding, modifying and removing users.
 */
import * as React from 'react'
import { useMutation, useQuery } from 'react-query'

import Container from '@mui/system/Container'
import { DataGrid, GridActionsCellItem, GridColDef } from '@mui/x-data-grid'
import AddSharpIcon from '@mui/icons-material/AddSharp'
import DeleteIcon from '@mui/icons-material/DeleteOutlined'
import AdminPanelSettingsSharpIcon from '@mui/icons-material/AdminPanelSettingsSharp'
import Box from '@mui/joy/Box'
import IconButton from '@mui/joy/IconButton'
import Sheet from '@mui/joy/Sheet'
import Stack from '@mui/joy/Stack'
import Typography from '@mui/joy/Typography'

import NotificationContext from '../NotificationContext'
import { useContext } from 'react'
import { userApi } from '../api'
import AlertItem from '../components/AlertItem'
import { User, UserRole } from '../generated-client/userlogin'
import { Alerts } from '../interfaces/components.interface'
import UserCreateModal from '../components/UserCreateModal'
import PasswordModal from '../components/PasswordModal'
import ConfirmDeleteModal from '../components/ConfirmDelteModal'


export default function UserManagementView() {
  const [, showNotification] = useContext(NotificationContext)
  const [userCreateModalOpen, setUserCreateModalOpen] = React.useState<boolean>(false)
  const [usernameToResetPasswordFor, setUsernameToResetPasswordFor] = React.useState('')
  const [userToDelete, setUserToDelete] = React.useState('')
  const [isUpdating, setIsUpdating] = React.useState<boolean>(false)

  const {
    data: users,
    isLoading,
    isError,
    refetch,
  } = useQuery<User[]>({
    queryKey: ['users'],
    queryFn: async () => {
      return await userApi
        .getUserListApiV1UserloginGetallusersGet()
        .then((result) => {
          return result.data
        })
    },
  })

  const delteMutation = useMutation<unknown, unknown, string>(async (username) => {
    await userApi
      .userDeleteApiV1UserloginDeleteuserDelete(username)
      .then(() => {
        showNotification({message: 'Deleted user ' + username, type: 'success'})
        refetch()
      })
      .catch((err) => {
        let errorMessage = null
        if (err?.response?.data?.detail) {
          errorMessage = 'Could not delete user. Detail: ' + err.response.data.detail
        } else {
          errorMessage = 'Could not delete user.'
        }
        showNotification({message: errorMessage, type: 'warning'})
      })
  })

  const updateMutation = useMutation<unknown, unknown, User>(async (user) => {
    await userApi
      .updateUserApiV1UserloginUpdateuserPut(user)
      .then(() => {
        showNotification({message: 'Modified user ' + user.username, type: 'success'})
        setIsUpdating(false)
        refetch()
      })
      .catch((err) => {
        let errorMessage = null
        if (err?.response?.data?.detail) {
          errorMessage = 'Could not update user. Detail: ' + err.response.data.detail
        } else {
          errorMessage = 'Could not update user.'
        }
        setIsUpdating(false)
        refetch()
        showNotification({message: errorMessage, type: 'warning'})
      })
  })

  if (isError) {
    return (
      <Container maxWidth={false} sx={{ width: '50%', mt: 5, justifyContent: 'center' }}>
        <AlertItem title='Error Loading Users' type={Alerts.Error} />
      </Container>
    )
  }

  const columns: GridColDef<User>[] = [
    { field: 'username', headerName: 'Username', width: 200, editable: false }, // username is primary key, if you want to change it, use delete and create
    { field: 'first_name', headerName: 'First name', width: 200, editable: true },
    { field: 'last_name', headerName: 'Last name', width: 200, editable: true },
    { field: 'email', headerName: 'e-Mail', width: 200, editable: true },
    {
      field: 'role',
      type: 'singleSelect',
      headerName: 'Role',
      width: 200,
      editable: true,
      valueOptions: Object.values(UserRole),
    },
    {
      field: 'last_activity_unixtime',
      headerName: 'Last Activity Time',
      width: 200,
      editable: false,
      filterable: false,
      valueFormatter: (value) => (value ? new Date(value * 1000).toLocaleString() : ''),
    },
    {
      field: 'last_login_unixtime',
      headerName: 'Last Login Time',
      width: 200,
      editable: false,
      filterable: false,
      valueFormatter: (value) => (value ? new Date(value * 1000).toLocaleString() : ''),
    },
    {
      field: 'actions',
      type: 'actions',
      headerName: 'Delete / Set Password',
      width: 200,
      cellClassName: 'actions',
      getActions: (row) => {
        return [
          <GridActionsCellItem
            key='1'
            icon={<DeleteIcon />}
            label='Delete'
            color='inherit'
            onClick={() => {
              setUserToDelete(row.row.username)
            }}
          />,
          <GridActionsCellItem
            key='2'
            icon={<AdminPanelSettingsSharpIcon />}
            label='setpassword'
            color='inherit'
            onClick={() => {
              setUsernameToResetPasswordFor(row.row.username)
            }}
          />,
        ]
      },
    },
  ]

  return (
    <Box sx={{ p: 3, width: '100%'}}>
      <UserCreateModal
        isOpen={userCreateModalOpen}
        setOpen={setUserCreateModalOpen}
        onSubmit={() => {
          refetch()
        }}
      />

      <Stack direction='row' sx={{ justifyContent: 'space-between', mb: 2 }}> 
        <Typography level='title-md'>List of Users</Typography> 
        <IconButton size='sm' variant='outlined'>
          <AddSharpIcon onClick={() => setUserCreateModalOpen(true)} />
        </IconButton>
      </Stack>

      <Sheet variant='outlined' sx={{ p: 1, borderRadius: 'sm' }}>
        <DataGrid
          rows={users ? users : []}
          columns={columns}
          getRowId={(user) => user.username}
          hideFooterSelectedRowCount 
          editMode={'row'}
          rowHeight={40}  // MUI default is 52
          loading={isUpdating || isLoading}
          processRowUpdate={(updatedUser) => {
            setIsUpdating(true)
            updateMutation.mutate(updatedUser)
            return updatedUser
          }}
        />
      </Sheet>

      <PasswordModal 
        onSubmit={() => {}} 
        isOpen={usernameToResetPasswordFor != '' ? true : false} 
        setOpen={(status) => {
          if (status == false) setUsernameToResetPasswordFor('')
        }}
        modalType={'modify'}
        item={usernameToResetPasswordFor}
      />

      <ConfirmDeleteModal 
        onSubmit={() => delteMutation.mutate(userToDelete)}
        isOpen={userToDelete != '' ? true : false} 
        setOpen={(status) => {
          if (status == false) setUserToDelete('')
        }}
        modalType={'modify'}
        item={'User \'' + userToDelete + '\''}
      />
    </Box>
  )
}
