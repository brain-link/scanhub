// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
// PatientInfo.tsx is responsible for displaying patient information in the patient view.
import Box from '@mui/joy/Box'
import Typography from '@mui/joy/Typography'
// import { useParams } from 'react-router-dom';
import Divider from '@mui/material/Divider'
import * as React from 'react'

// import client from '../client/queries';
// import { Patient } from '../interfaces/data.interface'
import { PatientOut } from '../generated-client/patient'

function PatientInfo(props: { patient: PatientOut | undefined; isLoading: boolean; isError: boolean }) {
  const { patient, isLoading, isError } = props

  if (isLoading) {
    // TODO: Beautify
    return <div>Loading...</div>
  }

  if (isError) {
    // TODO: Beautify
    return <div>Error loading patient data</div>
  }

  if (patient) {
    return (
      <Box
        sx={{
          rowGap: 0.4,
          columnGap: 2,
          // p: 1,
          display: 'grid',
          gridTemplateColumns: 'auto 1fr',
          '& > *:nth-of-type(odd)': {
            color: 'text.secondary',
          },
        }}
      >
        <Typography level='body-sm'>ID</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {patient.id}
        </Typography>
  
        <Typography level='body-sm'>Sex</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {patient.sex}
        </Typography>
  
        <Typography level='body-sm'>Birthday</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {patient.birth_date}
        </Typography>
  
        <Typography level='body-sm'>Admission</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {new Date(patient.datetime_created).toDateString()}
        </Typography>
  
        <Typography level='body-sm'>Updated</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {patient.datetime_updated ? new Date(patient.datetime_updated).toDateString() : '-'}
        </Typography>
  
        <Typography level='body-sm'>Status</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {patient.status}
        </Typography>
  
        <Typography level='body-sm'>Concern</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {patient.issuer}
        </Typography>
      </Box>
    )
  }
}

export default PatientInfo
