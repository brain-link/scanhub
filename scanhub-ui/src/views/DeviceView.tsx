/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * DeviceView.tsx is responsible for rendering the devices table and for managing the device registration.
 */
import * as React from 'react'
import { useMutation, useQuery } from 'react-query'

import Box from '@mui/joy/Box'
import IconButton from '@mui/joy/IconButton'
import AddSharpIcon from '@mui/icons-material/AddSharp'
import DeleteIcon from '@mui/icons-material/DeleteOutlined'
import LinearProgress from '@mui/joy/LinearProgress'
import Sheet from '@mui/joy/Sheet'
import Stack from '@mui/joy/Stack'
import Typography from '@mui/joy/Typography'
import Container from '@mui/system/Container'
import { DataGrid, GridActionsCellItem, GridColDef } from '@mui/x-data-grid'

import NotificationContext from '../NotificationContext'
import { deviceApi } from '../api'
import AlertItem from '../components/AlertItem'
import { Alerts } from '../interfaces/components.interface'
import { DeviceOut } from '../generated-client/device/api'
import DeviceCreateModal from '../components/DeviceCreateModal'
import ConfirmDeleteModal from '../components/ConfirmDelteModal'


export default function DeviceView() {
  const [, showNotification] = React.useContext(NotificationContext)
  const [deviceCreateModalOpen, setDeviceCreateModalOpen] = React.useState<boolean>(false)
  // const [isUpdating, setIsUpdating] = React.useState<boolean>(false)
  const [deviceToDelete, setDeviceToDelete] = React.useState<DeviceOut | undefined>(undefined)

  const {
    data: devices,
    isLoading,
    isError,
    refetch,
  } = useQuery<DeviceOut[]>({
    queryKey: ['devices'],
    queryFn: async () => {
      return await deviceApi
        .getDevicesApiV1DeviceGet()
        .then((result) => {
          return result.data
        })
    },
  })

  const delteMutation = useMutation<unknown, unknown, string>(async (deviceId) => {
    await deviceApi
      .deleteDeviceApiV1DeviceDeviceIdDelete(deviceId)
      .then(() => {
        showNotification({message: 'Deleted device.', type: 'success'})
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
        <Typography>Loading devices...</Typography>
        <LinearProgress variant='plain' />
      </Container>
    )
  }

  if (isError) {
    return (
      <Container maxWidth={false} sx={{ width: '50%', mt: 5, justifyContent: 'center' }}>
        <AlertItem title='Error loading devices' type={Alerts.Error} />
      </Container>
    )
  }

  const columns: GridColDef<DeviceOut>[] = [
    { field: 'id', headerName: 'ID', width: 200, editable: false },
    { field: 'title', headerName: 'Title', width: 200, editable: false },
    { field: 'description', headerName: 'Description', width: 200, editable: false },
    { field: 'status', headerName: 'Status', width: 200, editable: false },

    { field: 'name', headerName: 'Device Name', width: 200, editable: false },
    { field: 'manufacturer', headerName: 'Manufacturer', width: 200, editable: false },
    { field: 'modality', headerName: 'Modality', width: 200, editable: false },
    { field: 'site', headerName: 'Site', width: 200, editable: false },
    { field: 'ip_address', headerName: 'IP Address', width: 200, editable: false },
    {
      field: 'datetime_created',
      headerName: 'Added (date/time)',
      width: 200,
      editable: false,
      filterable: false,
      valueFormatter: (value) => (value ? new Date(value).toLocaleString() : ''),
    },
    {
      field: 'datetime_updated',
      headerName: 'Last updated (date/time)',
      width: 200,
      editable: false,
      filterable: false,
      valueFormatter: (value) => (value ? new Date(value).toLocaleString() : ''),
    },
    {
      field: 'actions',
      type: 'actions',
      headerName: 'Delete',
      width: 150,
      cellClassName: 'actions',
      getActions: (row) => {
        return [
          <GridActionsCellItem
            key='1'
            icon={<DeleteIcon />}
            label='Delete'
            color='inherit'
            onClick={() => {
              setDeviceToDelete(row.row)
            }}
          />,
        ]
      },
    },
  ]

  return (
    <Box sx={{ p: 3, width: '100%'}}>
      <DeviceCreateModal
        isOpen={deviceCreateModalOpen}
        setOpen={setDeviceCreateModalOpen}
        onSubmit={() => {
          refetch()
        }}
      />

      <Stack direction='row' sx={{ justifyContent: 'space-between', mb: 2 }}> 
        <Typography level='title-md'>List of Devices</Typography> 
        <IconButton size='sm' variant='outlined'>
          <AddSharpIcon onClick={() => setDeviceCreateModalOpen(true)} />
        </IconButton>
      </Stack>

      <Sheet variant='outlined' sx={{ p: 1, borderRadius: 'sm' }}>
        <DataGrid
          rows={devices}
          columns={columns}
          // getRowId={(user) => user.username}
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
      <ConfirmDeleteModal 
        onSubmit={() => {if (deviceToDelete) delteMutation.mutate(deviceToDelete.id)}}
        isOpen={deviceToDelete != undefined}
        setOpen={(status) => {
          if (status == false) setDeviceToDelete(undefined)
        }}
        item={deviceToDelete ? 'Device \'' + deviceToDelete.title + '\' with ID \'' + deviceToDelete.id + '\'' : ''}
        modalType={'modify'}
      />
    </Box>
  )
}
