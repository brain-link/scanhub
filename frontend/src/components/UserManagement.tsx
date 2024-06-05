// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
// UserManagement.tsx is responsible for rendering the user table and for adding, modifying and removing users.
import AddSharpIcon from '@mui/icons-material/AddSharp'
import Box from '@mui/joy/Box'
import IconButton from '@mui/joy/IconButton'
import LinearProgress from '@mui/joy/LinearProgress'
import Stack from '@mui/joy/Stack'
import Typography from '@mui/joy/Typography'
import Container from '@mui/system/Container'
import * as React from 'react'
import { useQuery } from 'react-query'
import { User } from '../generated-client/userlogin';
import { userApi } from '../api'
import PatientCreateModal from '../components/PatientCreateModal'
import Sheet from '@mui/joy/Sheet'
import Table from '@mui/joy/Table'
import AlertItem from '../components/AlertItem'
import { Alerts } from '../interfaces/components.interface'
import LoginContext from '../LoginContext'

export default function UserManagement() {

  const [currentuser, ] = React.useContext(LoginContext)
  const [dialogOpen, setDialogOpen] = React.useState<boolean>(false)

  const {data: users, isLoading, isError} = useQuery<User[]>({
    queryKey: ['patients'],
    queryFn: async () => { 
      return await userApi.getUserListApiV1UserloginGetallusersGet(
        {headers: {Authorization: 'Bearer ' + currentuser?.access_token}}
      ).then(
        (result) => {return result.data}
      )}
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


  return (

    <Box sx={{ m: 3 }}>
      
      {/* 
      <PatientCreateModal
        isOpen={dialogOpen}
        setOpen={setDialogOpen}
        onSubmit={(newPatient: PatientOut) => {patients?.push(newPatient)}}
        onClose={() => {}}
      />

      <Stack direction='row' sx={{ justifyContent: 'space-between', mb: 2 }}>
        <Typography level='title-md'>List of Users</Typography>
        <IconButton size='sm' variant='outlined'>
          <AddSharpIcon onClick={() => setDialogOpen(true)} />
        </IconButton>
      </Stack>
      */}

      <Sheet variant='outlined' sx={{ p: 1, borderRadius: 'sm' }}>
        <Table hoverRow borderAxis='xBetween' color='neutral' size='sm' stickyHeader variant='plain'>
          <thead>
            <tr>
              <th>Username</th>
              <th>First Name</th>
              <th>Last Name</th>
              <th>e-Mail</th>
              <th>Last Activity [Unixtime]</th>
            </tr>
          </thead>

          <tbody>
            {users?.map((user) => (
              <tr key={user.username} onClick={() => {}}>
                <td>{user.username}</td>
                <td>{user.first_name}</td>
                <td>{user.last_name}</td>
                <td>{user.email}</td>
                <td></td>
              </tr>
            ))}
          </tbody>
        </Table>
      </Sheet>

    </Box>
  )
}



