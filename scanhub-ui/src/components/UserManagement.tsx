/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * UserManagement.tsx is responsible for rendering the user table and for adding, modifying and removing users.
 */
import AddSharpIcon from '@mui/icons-material/AddSharp'
import DeleteIcon from '@mui/icons-material/DeleteOutlined'
import Box from '@mui/joy/Box'
import IconButton from '@mui/joy/IconButton'
import LinearProgress from '@mui/joy/LinearProgress'
import Sheet from '@mui/joy/Sheet'
import Stack from '@mui/joy/Stack'
import Typography from '@mui/joy/Typography'
import Container from '@mui/system/Container'
import { DataGrid, GridActionsCellItem, GridColDef } from '@mui/x-data-grid'
import * as React from 'react'
import { useMutation, useQuery } from 'react-query'

import LoginContext from '../LoginContext'
import NotificationContext from '../NotificationContext'
import { useContext } from 'react'
import { userApi } from '../api'
import AlertItem from '../components/AlertItem'
import { User, UserRole } from '../generated-client/userlogin'
import { Alerts } from '../interfaces/components.interface'
import UserCreateModal from './UserCreateModal'

export default function UserManagement() {
  const [currentuser] = React.useContext(LoginContext)
  const [, setMessageObject] = useContext(NotificationContext)
  const [dialogOpen, setDialogOpen] = React.useState<boolean>(false)
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
        .getUserListApiV1UserloginGetallusersGet({ headers: { Authorization: 'Bearer ' + currentuser?.access_token } })
        .then((result) => {
          return result.data
        })
    },
  })

  const delteMutation = useMutation<unknown, unknown, string>(async (username) => {
    await userApi
      .userDeleteApiV1UserloginDeleteuserDelete(username, {
        headers: { Authorization: 'Bearer ' + currentuser?.access_token },
      })
      .then(() => {
        console.log('Deleted user:', username)
        setMessageObject({message: 'Deleted user ' + username, type: 'success', open: true})
        refetch()
      })
      .catch((err) => {
        let errorMessage = null
        if (err?.response?.data?.detail) {
          errorMessage = 'Could not delete user. Detail: ' + err.response.data.detail
        } else {
          errorMessage = 'Could not delete user.'
        }
        console.log(errorMessage)
        setMessageObject({message: errorMessage, type: 'warning', open: true})
      })
  })

  const updateMutation = useMutation<unknown, unknown, User>(async (user) => {
    await userApi
      .updateUserApiV1UserloginUpdateuserPut(user, {
        headers: { Authorization: 'Bearer ' + currentuser?.access_token },
      })
      .then(() => {
        console.log('Modified user:', user.username)
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
        console.log(errorMessage)
        setMessageObject({message: errorMessage, type: 'warning', open: true})
      })
  })

  if (isLoading) {
    return (
      <Container maxWidth={false} sx={{ width: '50%', mt: 5, justifyContent: 'center' }}>
        <Typography>Loading patients...</Typography>
        <LinearProgress variant='plain' />
      </Container>
    )
  }

  if (isError) {
    return (
      <Container maxWidth={false} sx={{ width: '50%', mt: 5, justifyContent: 'center' }}>
        <AlertItem title='Error Loading Patients' type={Alerts.Error} />
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
      field: 'actions',
      type: 'actions',
      headerName: 'Delete',
      width: 100,
      cellClassName: 'actions',
      getActions: (row) => {
        return [
          <GridActionsCellItem
            key='1'
            icon={<DeleteIcon />}
            label='Delete'
            color='inherit'
            onClick={() => {
              delteMutation.mutate(row.id.toString())
            }}
          />,
        ]
      },
    },
  ]

  return (
    <Box sx={{ m: 3 }}>
      <UserCreateModal
        isOpen={dialogOpen}
        setOpen={setDialogOpen}
        onSubmit={() => {
          refetch()
        }}
        onClose={() => {}}
      />

      <Stack direction='row' sx={{ justifyContent: 'space-between', mb: 2 }}>
        <Typography level='title-md'>List of Users</Typography>
        <IconButton size='sm' variant='outlined'>
          <AddSharpIcon onClick={() => setDialogOpen(true)} />
        </IconButton>
      </Stack>

      <Sheet variant='outlined' sx={{ p: 1, borderRadius: 'sm' }}>
        <DataGrid
          rows={users}
          columns={columns}
          getRowId={(user) => user.username}
          style={{ width: 1300 }}
          hideFooterSelectedRowCount
          editMode={'row'}
          loading={isUpdating}
          processRowUpdate={(updatedUser) => {
            setIsUpdating(true)
            updateMutation.mutate(updatedUser)
            return updatedUser
          }}
        />
      </Sheet>
    </Box>
  )
}
