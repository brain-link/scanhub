/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 * 
 * ExamInstanceInfo.tsx is responsible for rendering additional information#
 * of an exam instance item.
 */

import * as React from 'react'
import Box from '@mui/joy/Box'
import Typography from '@mui/joy/Typography'
import Chip from '@mui/joy/Chip'
import Stack from '@mui/joy/Stack'

import { ExamOut } from '../generated-client/exam'

function ExamInstanceInfo(props: {exam: ExamOut}) {

  return (
    <Box
      sx={{
        rowGap: 0.4,
        columnGap: 4,
        p: 2,
        display: 'grid',
        gridTemplateColumns: 'auto 1fr',
        '& > *:nth-child(odd)': {
          color: 'text.secondary',
        },
      }}
    >

      <Typography fontSize="sm">Name</Typography>
      <Typography level='body-sm' textColor='text.primary'>
        {props.exam.name}
      </Typography>

      <Typography fontSize="sm">ID</Typography>
      <Typography level='body-sm' textColor='text.primary'>
        {props.exam.id}
      </Typography>

      <Typography fontSize="sm">Note</Typography>
      <Typography level='body-sm' textColor='text.primary'>
        {props.exam.status}
      </Typography>

      <Typography fontSize="sm">Issuer</Typography>
      <Typography level='body-sm' textColor='text.primary'>
        {props.exam.creator}
      </Typography>

      <Typography fontSize="sm">Site</Typography>
      <Typography level='body-sm' textColor='text.primary'>
        {props.exam.site}
      </Typography>

      <Typography fontSize="sm">Created</Typography>
      <Typography level='body-sm' textColor='text.primary'>
        { new Date(props.exam.datetime_created).toDateString() }
      </Typography>

      <Typography fontSize="sm">Updated</Typography>
      <Typography level='body-sm' textColor='text.primary'>
        { props.exam.datetime_updated ? new Date(props.exam.datetime_updated).toDateString() : '-' }
      </Typography>

      <Typography fontSize="sm">Status</Typography>
      <Stack direction="row" spacing={0.5}>
        <Chip size="sm" color={props.exam.is_template ? 'success' : 'danger'} sx={{ fontWeight: 'lg' }}>Template</Chip>
        <Chip size="sm" color={props.exam.is_frozen ? 'success' : 'danger'} sx={{ fontWeight: 'lg' }}>Frozen</Chip>
      </Stack>

    </Box>
  )
}

export default ExamInstanceInfo