/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * PatientInfo.tsx is responsible for displaying patient information in the patient view.
 */
import Box from '@mui/joy/Box'
import Typography from '@mui/joy/Typography'
// import { useParams } from 'react-router-dom';
import React from 'react'

// import client from '../client/queries';
// import { Patient } from '../interfaces/data.interface'
import { PatientOut } from '../openapi/generated-client/patient'
import { getAgeFromDate } from '../utils/Calc'

function PatientInfo({ patient, isLoading, isError }: { patient: PatientOut | undefined; isLoading: boolean; isError: boolean }) {

  if (isLoading) {
    // TODO: Beautify
    return <div>Loading...</div>
  }

  if (isError) {
    // TODO: Beautify
    return <div>Error loading patient data</div>
  }

  if (patient) {

    const patient_birth_date = new Date(patient.birth_date)
    const datetime_create = new Date(patient.datetime_created)
    const datetime_updated = patient.datetime_updated ? new Date(String(patient.datetime_updated)) : undefined

    return (
      <Box
        sx={{
          rowGap: 0.4,
          columnGap: 2,
          display: 'grid',
          gridTemplateColumns: 'auto 1fr',
          '& > *:nth-of-type(odd)': {
            color: 'text.secondary',
          },
        }}
      >
        {/* <Typography level='body-sm'>ID</Typography>
        <Typography level='body-sm' textColor='text.primary' sx={{overflow: 'auto'}}>
          {patient.id}
        </Typography> */}

        <Typography level='body-sm'>Name</Typography>
        <Typography level='body-sm' textColor='text.primary' sx={{overflow: 'auto'}}>
          {patient.last_name + ', ' + patient.first_name}
        </Typography>

        <Typography level='body-sm'>Birthday</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {patient_birth_date.toLocaleDateString() + ` (${getAgeFromDate(patient_birth_date)})`}
        </Typography>

        <Typography level='body-sm'>Gender</Typography>
        <Typography level='body-sm' textColor='text.primary' sx={{overflow: 'auto'}}>
          {patient.sex}
        </Typography>

        <Typography level='body-sm'>Height</Typography>
        <Typography level='body-sm' textColor='text.primary' sx={{overflow: 'auto'}}>
          {patient.height + ' cm'}
        </Typography>

        <Typography level='body-sm'>Weight</Typography>
        <Typography level='body-sm' textColor='text.primary' sx={{overflow: 'auto'}}>
          {patient.weight + ' kg'}
        </Typography>

        <Typography level='body-sm'>Last update</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {
            datetime_updated ? datetime_updated.toLocaleDateString() + ', ' + datetime_updated.toLocaleTimeString()
            : datetime_create.toLocaleDateString() + ', ' + datetime_create.toLocaleTimeString()
          }
        </Typography>
      </Box>
    )
  }
  return null;
}

export default PatientInfo
