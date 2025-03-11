/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * PatientListView.tsx is responsible for rendering the patient table view.
 */
import * as React from 'react'
import { useContext } from 'react'
import { useQuery, useMutation } from 'react-query'
import { useNavigate } from 'react-router-dom'

import AddSharpIcon from '@mui/icons-material/AddSharp'
import Box from '@mui/joy/Box'
import IconButton from '@mui/joy/IconButton'
import DeleteIcon from '@mui/icons-material/DeleteOutlined'
import ImportContactsIcon from '@mui/icons-material/ImportContacts';
import Stack from '@mui/joy/Stack'
import Typography from '@mui/joy/Typography'
import Container from '@mui/system/Container'
import Sheet from '@mui/joy/Sheet'
import { DataGrid, GridColDef, GridCellParams, GridActionsCellItem } from '@mui/x-data-grid'

import { patientApi } from '../api'
import AlertItem from '../components/AlertItem'
import PatientCreateModal from '../components/PatientCreateModal'
import { PatientOut, Gender } from '../generated-client/patient'
import { Alerts } from '../interfaces/components.interface'
import NotificationContext from '../NotificationContext'
import ConfirmDeleteModal from '../components/ConfirmDelteModal'


export default function PatientListView() {
  const navigate = useNavigate()
  const [, showNotification] = useContext(NotificationContext)
  const [patientCreateDialogOpen, setPatientCreateDialogOpen] = React.useState<boolean>(false)
  const [patientToDelete, setPatientToDelete] = React.useState<PatientOut | undefined>(undefined)
  const [isUpdating, setIsUpdating] = React.useState<boolean>(false)

  const {
    data: patients,
    refetch,
    isLoading,
    isError,
  } = useQuery<PatientOut[]>({
    queryKey: ['patients'],
    queryFn: async () => {
      return await patientApi.getPatientListApiV1PatientGet()
      .then((result) => {
        return result.data
      })
    },
  })

  const delteMutation = useMutation<unknown, unknown, PatientOut>(async (patient) => {
    await patientApi
      .deletePatientApiV1PatientPatientIdDelete(patient.id)
      .then(() => {
        showNotification({message: 'Deleted patient ' + patient.first_name + ' ' + patient.last_name + ' (' + patient.id + ')', type: 'success'})
        refetch()
      })
      .catch((err) => {
        let errorMessage = null
        if (err?.response?.data?.detail) {
          errorMessage = 'Could not delete patient. Detail: ' + err.response.data.detail
        } else {
          errorMessage = 'Could not delete patient.'
        }
        showNotification({message: errorMessage, type: 'warning'})
      })
  })

  const updateMutation = useMutation<unknown, unknown, PatientOut>(async (patient) => {
    await patientApi
      .updatePatientApiV1PatientPatientIdPut(patient.id, patient)
      .then(() => {
        showNotification({message: 'Modified patient ' + patient.first_name + ' ' + 
                                   patient.last_name + ' (' + patient.id + ')', 
                          type: 'success'})
        setIsUpdating(false)
        refetch()
      })
      .catch((err) => {
        let errorMessage = null
        if (err?.response?.data?.detail?.[0]?.msg) {
          errorMessage = 'Could not update user. Detail: ' + err.response.data.detail[0].msg
        }
        else if (err?.response?.data?.detail) {
          errorMessage = 'Could not update user. Detail: ' + err.response.data.detail
        } else {
          errorMessage = 'Could not update user.'
        }
        setIsUpdating(false)
        refetch()
        showNotification({message: errorMessage, type: 'warning'})
      })
      // don't catch error here to make sure it propagates to onRowUpdate
  })

  if (isError) {
    return (
      <Container maxWidth={false} sx={{ width: '50%', mt: 5, justifyContent: 'center' }}>
        <AlertItem title='Error Loading Patients' type={Alerts.Error} />
      </Container>
    )
  }

  const columns: GridColDef<PatientOut>[] = [
    {
      field: 'open',
      type: 'actions',
      headerName: 'Open',
      width: 80,
      cellClassName: 'actions',
      getActions: (row) => {
        return [
          <GridActionsCellItem
            key='1'
            icon={<ImportContactsIcon />}
            label='Show'
            color='inherit'
            onClick={() => {
              navigate(`/${row.id}`)
            }}
          />
        ]
      },
    },
    { field: 'id', headerName: 'ID', width: 300, editable: false },
    { field: 'first_name', headerName: 'First Name', width: 200, editable: true },
    { field: 'last_name', headerName: 'Last Name', width: 200, editable: true },
    { field: 'birth_date', headerName: 'Birthday', width: 150, editable: true },
    {
      field: 'sex',
      type: 'singleSelect',
      headerName: 'Sex',
      width: 100,
      editable: true,
      valueOptions: Object.values(Gender),
    },
    { field: 'datetime_created', headerName: 'Added (date/time)', width: 200, editable: false },
    { field: 'datetime_updated', headerName: 'Last updated (date/time)', width: 200, editable: false },
    { field: 'comment', headerName: 'Comment', width: 300, editable: true },
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
              setPatientToDelete(row.row)
            }}
          />
        ]
      },
    },
  ]

  return (
    <Box sx={{ p: 3, width: '100%' }}>
      <PatientCreateModal
        isOpen={patientCreateDialogOpen}
        setOpen={setPatientCreateDialogOpen}
        onSubmit={() => {
          refetch()
        }}
      />

      <Stack direction='row' sx={{ justifyContent: 'space-between', mb: 2 }}>
        <Typography level='title-md'>List of Patients</Typography>
        <IconButton size='sm' variant='outlined'>
          <AddSharpIcon onClick={() => setPatientCreateDialogOpen(true)} />
        </IconButton>
      </Stack>

      <Sheet variant='outlined' sx={{ p: 1, borderRadius: 'sm' }}>
        <DataGrid
          rows={patients ? patients : []}
          columns={columns}
          hideFooterSelectedRowCount
          editMode={'row'}
          rowHeight={40}  // MUI default is 52
          loading={isUpdating || isLoading}
          processRowUpdate={(updatedPatient, oldPatient) => {
            if (isNaN(Date.parse(updatedPatient.birth_date))) {
              showNotification({message: 'Invalid date format for birth-date.', type: 'warning'})
              // TODO the 30th of february is not handled correct yet
              return oldPatient
            }
            else {
              setIsUpdating(true)
              updateMutation.mutate(updatedPatient)
              return updatedPatient
            }
          }}
          onCellClick={(params: GridCellParams) => {
            if (params.field == 'id') {
              navigate(`/${params.row.id}`)
            }
          }}
        />
      </Sheet>

      <ConfirmDeleteModal 
        onSubmit={() => {
          if (patientToDelete != undefined) delteMutation.mutate(patientToDelete)
        }}
        isOpen={patientToDelete != undefined ? true : false} 
        setOpen={(status) => {
          if (status == false) setPatientToDelete(undefined)
        }}
        modalType={'modify'}
        item={patientToDelete != undefined ? 
                'patient ' + patientToDelete.first_name + ' ' + 
                 patientToDelete.last_name + ' (' + patientToDelete.id + ')'
              : ''}
      />
    </Box>
  )
}
