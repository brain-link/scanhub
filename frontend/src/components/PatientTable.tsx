// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
// PatientTable.tsx is responsible for rendering the patient table view.
import KeyboardArrowRight from '@mui/icons-material/KeyboardArrowRight'
import Box from '@mui/joy/Box'
import Button from '@mui/joy/Button'
import Sheet from '@mui/joy/Sheet'
import Table from '@mui/joy/Table'
import * as React from 'react'
import { useNavigate } from 'react-router-dom'
import { PatientTableInterface } from '../interfaces/components.interface'


export default function PatientTable(props: PatientTableInterface) {

  const navigate = useNavigate()

  return (
    <Sheet variant='outlined' sx={{ p: 1, borderRadius: 'sm' }}>
      <Table hoverRow borderAxis='xBetween' color='neutral' size='sm' stickyHeader variant='plain'>
        <thead>
          <tr>
            <th style={{ width: '4%' }}>ID</th>
            <th>Name</th>
            <th style={{ width: '4%' }}>Sex</th>
            <th style={{ width: '8%' }}>Birthday</th>
            <th>Issuer</th>
            <th>Status</th>
            <th>Comment</th>
            <th style={{ width: '8%' }}>Admission</th>
            <th style={{ width: '8%' }}>Updated</th>
          </tr>
        </thead>

        <tbody>
          {props.patients.map((patient) => (
            <tr key={patient.id} onClick={() => {navigate(`/${patient.id}`)}}>
              <td>{patient.id}</td>
              <td>{patient.name}</td>
              <td>{patient.sex}</td>
              <td>{patient.birth_date}</td>
              <td>{patient.issuer}</td>
              <td>{patient.status}</td>
              <td>{patient.comment}</td>
              <td>{new Date(patient.datetime_created).toDateString()}</td>
              <td>{patient.datetime_updated ? new Date(patient.datetime_updated).toDateString() : '-'}</td>

              {/* <td>
                <Box sx={{ display: 'flex', gap: 1 }}>
                  <Button
                    size='sm'
                    sx={{ zIndex: 'snackbar' }}
                    variant='soft'
                    endDecorator={<KeyboardArrowRight />}
                    color='neutral'
                    onClick={() => {
                      navigate(`/patients/dcmview/${patient.id}`)
                    }}
                  >
                    View
                  </Button>
                  <Button
                    size='sm'
                    sx={{ zIndex: 'snackbar' }}
                    variant='soft'
                    endDecorator={<KeyboardArrowRight />}
                    color='neutral'
                    onClick={() => {
                      navigate(`/patients/${patient.id}`)
                    }}
                  >
                    Acquire
                  </Button>
                </Box>
              </td> */}
            </tr>
          ))}
        </tbody>
      </Table>
    </Sheet>
  )
}
