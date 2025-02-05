/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * SequenceView.tsx is responsible for rendering the sequence table and for adding, modifying and removing sequences.
 */
import * as React from 'react'
// import { useContext } from 'react'
import { useQuery } from 'react-query'

import IconButton from '@mui/joy/IconButton'
import AddSharpIcon from '@mui/icons-material/AddSharp'
// import DeleteIcon from '@mui/icons-material/DeleteOutlined'
import Box from '@mui/joy/Box'
import LinearProgress from '@mui/joy/LinearProgress'
import Sheet from '@mui/joy/Sheet'
import Stack from '@mui/joy/Stack'
import Typography from '@mui/joy/Typography'
import Container from '@mui/system/Container'
import { DataGrid, GridColDef } from '@mui/x-data-grid'

// import NotificationContext from '../NotificationContext'
import { sequenceApi } from '../api'
import { MRISequence } from '../generated-client/sequence'
import { Alerts } from '../interfaces/components.interface'
import AlertItem from '../components/AlertItem'
import SequenceUpload from '../components/SequenceUpload'


export default function SequenceView() {
  // const [, showNotification] = useContext(NotificationContext)
  const [dialogOpen, setDialogOpen] = React.useState<boolean>(false)
  // const [isUpdating, setIsUpdating] = React.useState<boolean>(false)

  const {
    data: sequences,
    isLoading,
    isError,
    refetch,
  } = useQuery<MRISequence[]>({
    queryKey: ['sequences'],
    queryFn: async () => {
      return await sequenceApi
        .getMriSequencesEndpointApiV1MriSequencesGet()
        .then((result) => {
          return result.data
        })
    },
  })

  // const delteMutation = useMutation<unknown, unknown, string>(async (username) => {
  //   await userApi
  //     .userDeleteApiV1UserloginDeleteuserDelete(username)
  //     .then(() => {
  //       showNotification({message: 'Deleted user ' + username, type: 'success'})
  //       refetch()
  //     })
  //     .catch((err) => {
  //       let errorMessage = null
  //       if (err?.response?.data?.detail) {
  //         errorMessage = 'Could not delete user. Detail: ' + err.response.data.detail
  //       } else {
  //         errorMessage = 'Could not delete user.'
  //       }
  //       showNotification({message: errorMessage, type: 'warning'})
  //     })
  // })

  // const updateMutation = useMutation<unknown, unknown, User>(async (user) => {
  //   await userApi
  //     .updateUserApiV1UserloginUpdateuserPut(user)
  //     .then(() => {
  //       console.log('Modified user:', user.username)
  //       setIsUpdating(false)
  //       refetch()
  //     })
  //     .catch((err) => {
  //       let errorMessage = null
  //       if (err?.response?.data?.detail) {
  //         errorMessage = 'Could not update user. Detail: ' + err.response.data.detail
  //       } else {
  //         errorMessage = 'Could not update user.'
  //       }
  //       setIsUpdating(false)
  //       refetch()
  //       showNotification({message: errorMessage, type: 'warning'})
  //     })
  // })

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

  const columns: GridColDef<MRISequence>[] = [
    { field: '_id', headerName: 'ID', width: 250, editable: false },
    { field: 'name', headerName: 'Name', width: 200, editable: false },
    { field: 'description', headerName: 'Description', width: 300, editable: false },
    { field: 'sequence_type', headerName: 'Type', width: 200, editable: false },
    {
      field: 'created_at',
      headerName: 'Added (date/time)',
      width: 200,
      editable: false,
      filterable: false,
      valueFormatter: (value) => (value ? new Date(value).toLocaleString() : ''),
    },
    {
      field: 'updated_at',
      headerName: 'Last updated (date/time)',
      width: 200,
      editable: false,
      filterable: false,
      valueFormatter: (value) => (value ? new Date(value).toLocaleString() : ''),
    },
    {
      field: 'tags',
      headerName: 'Tags',
      width: 200,
      editable: false,
      filterable: false,
    },
    { field: 'file', headerName: 'File', width: 200, editable: false },
    { field: 'file_extension', headerName: 'File extension', width: 100, editable: false },
  ]

  return (
    <Box sx={{ p: 3, width: '100%'}}>
      <SequenceUpload
        isOpen={dialogOpen}
        setOpen={setDialogOpen}
        onSubmit={() => {
          refetch()
        }}
      />

      <Stack direction='row' sx={{ justifyContent: 'space-between', mb: 2 }}> 
        <Typography level='title-md'>List of Sequences</Typography>
        <IconButton size='sm' variant='outlined'>
          <AddSharpIcon onClick={() => setDialogOpen(true)} />
        </IconButton>
      </Stack>

      <Sheet variant='outlined' sx={{ p: 1, borderRadius: 'sm' }}>
        <DataGrid
          rows={sequences}
          columns={columns}
          getRowId={(sequence) => sequence._id ? sequence._id : ''}
          hideFooterSelectedRowCount 
          editMode={'row'}
          rowHeight={40}  // MUI default is 52
          // loading={isUpdating}
          processRowUpdate={(updatedUser) => {
            // setIsUpdating(true)
            // updateMutation.mutate(updatedUser)
            return updatedUser
          }}
        />
      </Sheet>
    </Box>
  )
}
