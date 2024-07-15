/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * PatientTable.tsx is responsible for rendering the patient table view.
 */
import Sheet from '@mui/joy/Sheet'
import * as React from 'react'
import { useNavigate } from 'react-router-dom'
import { DataGrid, GridColDef, GridRowParams } from '@mui/x-data-grid'
import { PatientTableInterface } from '../interfaces/components.interface'
import { PatientOut } from '../generated-client/patient'


export default function PatientTable(props: PatientTableInterface) {

  const navigate = useNavigate()

  const columns: GridColDef<PatientOut>[] = [
    { field: 'id', headerName: 'ID', width: 200, editable: false },
    { field: 'name', headerName: 'Name', width: 200, editable: false },
    {
      field: 'sex',
      type: 'singleSelect',
      headerName: 'Sex',
      width: 200,
      editable: false,
      valueOptions: ['m', 'w', 'o'],
    },
    { field: 'birth_date', headerName: 'Birthday', width: 200, editable: false },
    { field: 'status', headerName: 'Status', width: 200, editable: false },
  ]

  return (
    <Sheet variant='outlined' sx={{ p: 1, borderRadius: 'sm' }}>
      <DataGrid
        rows={props.patients}
        columns={columns}
        hideFooterSelectedRowCount
        editMode={'row'}
        rowHeight={40}  // MUI default is 52
        // loading={isUpdating}
        processRowUpdate={(updatedUser) => {    // TODO enable udpates
          // setIsUpdating(true)
          // updateMutation.mutate(updatedUser)
          return updatedUser
        }}
        onRowClick={(params: GridRowParams<PatientOut>) => navigate(`/${params.row.id}`)}
      />
    </Sheet>
  )
}
