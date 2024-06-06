// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
// UserManagement.tsx is responsible for rendering the user table and for adding, modifying and removing users.
import AddSharpIcon from '@mui/icons-material/AddSharp'
import Box from '@mui/joy/Box'
import IconButton from '@mui/joy/IconButton'
import DeleteIcon from '@mui/icons-material/DeleteOutlined';
import CloseIcon from '@mui/icons-material/Close';
import LinearProgress from '@mui/joy/LinearProgress'
import Stack from '@mui/joy/Stack'
import Typography from '@mui/joy/Typography'
import Container from '@mui/system/Container'
import * as React from 'react'
import { useMutation, useQuery } from 'react-query'
import { User } from '../generated-client/userlogin';
import { userApi } from '../api'
import Sheet from '@mui/joy/Sheet'
import { DataGrid, GridActionsCellItem, GridColDef } from '@mui/x-data-grid';
import AlertItem from '../components/AlertItem'
import { Alerts } from '../interfaces/components.interface'
import Alert from '@mui/joy/Alert';
import LoginContext from '../LoginContext'
import UserCreateModal from './UserCreateModal'

export default function UserManagement() {

  const [currentuser, ] = React.useContext(LoginContext)
  const [dialogOpen, setDialogOpen] = React.useState<boolean>(false)
  const [alert, setAlert] = React.useState<string | null>(null)

  const {data: users, isLoading, isError, refetch} = useQuery<User[]>({
    queryKey: ['users'],
    queryFn: async () => { 
      return await userApi.getUserListApiV1UserloginGetallusersGet(
        {headers: {Authorization: 'Bearer ' + currentuser?.access_token}}
      ).then(
        (result) => {return result.data}
      )}
  })

  const delte_mutation = useMutation<unknown, unknown, string>(async (username) => {
    await userApi.userDeleteApiV1UserloginDeleteuserDelete(username, {headers: {Authorization: 'Bearer ' + currentuser?.access_token}})
    .then((_) => {
      console.log("Deleted user:", username)
      setAlert(null);
      refetch();
    })
    .catch((err) => { 
      let error_message = null;
      if (err?.response?.data?.detail) {
        error_message = "Could not delete user. Detail: " + err.response.data.detail
      }
      else {
        error_message = "Could not delete user."
      }
      console.log(error_message)
      setAlert(error_message)
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
        <AlertItem
          title="Error Loading Patients"
          type={Alerts.Error}
        />
      </Container>
    )
  }


  const columns: GridColDef<User>[] = [
    { field: 'username',    headerName: 'Username',     width: 200,   editable: true },
    { field: 'first_name',  headerName: 'First name',   width: 200,   editable: true },
    { field: 'last_name',   headerName: 'Last name',    width: 200,   editable: true },
    { field: 'email',       headerName: 'e-Mail',       width: 200,   editable: true },
    { 
      field: 'last_activity_unixtime', headerName: 'Last Activity Time', width: 200, editable: false, 
      filterable: false, valueFormatter: (value) => value ? new Date(value * 1000).toLocaleString() : ""
    },
    { field: 'actions', type: 'actions', headerName: 'Delete', width: 100, cellClassName: 'actions', getActions: (row) => {
      return [<GridActionsCellItem icon={<DeleteIcon />} label="Delete" color="inherit" onClick={() => {
        delte_mutation.mutate(row.id.toString())
      }}/>];
    }}
  ];

  return (

    <Box sx={{ m: 3 }}>

      <UserCreateModal
        isOpen={dialogOpen}
        setOpen={setDialogOpen}
        onSubmit={(_: User) => { refetch() }}
        onClose={() => {}}
        setAlert={setAlert}
      />

      <Stack direction='row' sx={{ justifyContent: 'space-between', mb: 2 }}>
        <Typography level='title-md'>List of Users</Typography>
        {alert ? 
          <Alert 
            variant="soft"
            color="warning"
            endDecorator={
              <IconButton variant="soft" size="sm" color="warning" onClick={() => setAlert(null)}>
                <CloseIcon />
              </IconButton>
            }
          >
            {alert}
          </Alert>
          : null}
        <IconButton size='sm' variant='outlined'>
          <AddSharpIcon onClick={() => setDialogOpen(true)} />
        </IconButton>
      </Stack>


      <Sheet variant='outlined' sx={{ p: 1, borderRadius: 'sm' }}>
        <DataGrid 
          rows={users} 
          columns={columns} 
          getRowId={(user) => user.username} 
          style={{width: 1100}} 
          hideFooterSelectedRowCount
          editMode={"row"}
        />
      </Sheet>

    </Box>
  )
}



