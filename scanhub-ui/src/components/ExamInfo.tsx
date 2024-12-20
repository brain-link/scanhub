/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * ExamInfo.tsx is responsible for rendering additional information of an exam item.
 */
import Box from '@mui/joy/Box'
import Typography from '@mui/joy/Typography'
import * as React from 'react'

import { ExamOut } from '../generated-client/exam'


function ExamInfo({ exam }: { exam: ExamOut }) {

  return (
    <Box sx={{display: 'flex', alignItems: 'stretch'}}>
      <Box
        sx={{
          rowGap: 0.4,
          columnGap: 4,
          p: 2,
          display: 'grid',
          gridTemplateColumns: 'auto 1fr',
          '& > *:nth-of-type(odd)': {
            color: 'text.secondary',
          },
        }}
      >
        <Typography fontSize='sm'>Name</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {exam.name}
        </Typography>

        <Typography fontSize='sm'>Description</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {exam.description}
        </Typography>

        <Typography fontSize='sm'>Indication</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {exam.indication}
        </Typography>

        <Typography fontSize='sm'>Patient height [cm]</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {exam.patient_height_cm}
        </Typography>

        <Typography fontSize='sm'>Patient weight [kg]</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {exam.patient_weight_kg}
        </Typography>

        <Typography fontSize='sm'>Comment</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {exam.comment}
        </Typography>

        <Typography fontSize='sm'>Status</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {exam.status}
        </Typography>

        <Typography fontSize='sm'>Is Template</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {exam.is_template ? 'True' : 'False'}
        </Typography>

        <Typography fontSize='sm'>ID</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {exam.id}
        </Typography>

        <Typography fontSize='sm'>Creator</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {exam.creator}
        </Typography>

        <Typography fontSize='sm'>Created</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {new Date(exam.datetime_created).toLocaleString()}
        </Typography>

        <Typography fontSize='sm'>Updated</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {exam.datetime_updated ? new Date(exam.datetime_updated).toLocaleString() : '-'}
        </Typography>
      </Box>
    </Box>
  )
}

export default ExamInfo
