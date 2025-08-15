/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * DeviceView.tsx is responsible for rendering the devices table and for managing the device registration.
 */
import React from 'react'
import { useMutation, useQuery } from '@tanstack/react-query'

import Box from '@mui/joy/Box'
import IconButton from '@mui/joy/IconButton'
import AddSharpIcon from '@mui/icons-material/AddSharp'
import DeleteIcon from '@mui/icons-material/DeleteOutlined'
import LinearProgress from '@mui/joy/LinearProgress'
import Stack from '@mui/joy/Stack'
import Typography from '@mui/joy/Typography'
import Container from '@mui/system/Container'
import { DataGrid, GridActionsCellItem, GridColDef } from '@mui/x-data-grid'

import NotificationContext from '../NotificationContext'
import { deviceApi } from '../api'
import AlertItem from '../components/AlertItem'
import { Alerts } from '../interfaces/components.interface'
import { DeviceOut } from '../openapi/generated-client/device/api'
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

  const delteMutation = useMutation<unknown, unknown, string>({
    mutationFn: async (deviceId) => {
      await deviceApi.deleteDeviceApiV1DeviceDeviceIdDelete(deviceId)
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
    }
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
    { field: 'id', headerName: 'ID', width: 100, editable: false },
    { field: 'name', headerName: 'Connection name', width: 150, editable: false },
    { field: 'description', headerName: 'Description', width: 150, editable: false },
    { field: 'status', headerName: 'Status', width: 100, editable: false },
    { field: 'device_name', headerName: 'Device name', width: 150, editable: false },
    { field: 'serial_number', headerName: 'Serial No.', width: 100, editable: false },
    { field: 'manufacturer', headerName: 'Manufacturer', width: 100, editable: false },
    { field: 'modality', headerName: 'Modality', width: 100, editable: false },
    { field: 'site', headerName: 'Site', width: 100, editable: false },
    {
      field: 'datetime_created', headerName: 'Added (date/time)', width: 100, editable: false,
      valueFormatter: (value) => (value ? new Date(value).toLocaleString() : ''),
    },
    {
      field: 'datetime_updated', headerName: 'Last updated (date/time)', width: 100, editable: false,
      valueFormatter: (value) => (value ? new Date(value).toLocaleString() : ''),
    },
    {
      field: 'actions', type: 'actions', width: 100, cellClassName: 'actions',
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

      <div style={{ height:'80vh', width: '100%'}}>
        <DataGrid
          rows={devices}
          columns={columns}
          // getRowId={(user) => user.username}
          hideFooterSelectedRowCount 
          editMode={'row'}
          rowHeight={45}  // MUI default is 52
          // loading={isUpdating}
          autoPageSize= {true}
          processRowUpdate={(updatedUser) => {
            // setIsUpdating(true)
            // updateMutation.mutate(updatedUser)
            return updatedUser
          }}
          sx={{
            '&.MuiDataGrid-root .MuiDataGrid-cell:focus-within': {
              outline: 'none !important',
            },
          }}
        />
      </div>
      <ConfirmDeleteModal 
        onSubmit={() => {if (deviceToDelete) delteMutation.mutate(deviceToDelete.id)}}
        isOpen={deviceToDelete != undefined}
        setOpen={(status) => {
          if (status == false) setDeviceToDelete(undefined)
        }}
        item={deviceToDelete ? 'Device \'' + deviceToDelete.name + '\' with ID \'' + deviceToDelete.id + '\'' : ''}
        modalType={'modify'}
      />
    </Box>
  )
}
