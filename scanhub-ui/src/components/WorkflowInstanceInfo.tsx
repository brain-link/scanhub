/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * WorkflowInstanceInfo.tsx is responsible for rendering additional information
 * of a workflow instance item.
 */
import Box from '@mui/joy/Box'
import Chip from '@mui/joy/Chip'
import Stack from '@mui/joy/Stack'
import Typography from '@mui/joy/Typography'
import * as React from 'react'

import { WorkflowOut } from '../generated-client/exam'

function WorkflowInstanceInfo(props: { workflow: WorkflowOut }) {
  return (
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
      <Typography fontSize='sm'>ID</Typography>
      <Typography level='body-sm' textColor='text.primary'>
        {props.workflow.id}
      </Typography>

      <Typography fontSize='sm'>Comment</Typography>
      <Typography level='body-sm' textColor='text.primary'>
        {props.workflow.comment}
      </Typography>

      <Typography fontSize='sm'>Created</Typography>
      <Typography level='body-sm' textColor='text.primary'>
        {new Date(props.workflow.datetime_created).toDateString()}
      </Typography>

      <Typography fontSize='sm'>Updated</Typography>
      <Typography level='body-sm' textColor='text.primary'>
        {props.workflow.datetime_updated ? new Date(props.workflow.datetime_updated).toDateString() : '-'}
      </Typography>

      <Typography fontSize='sm'>Status</Typography>
      <Stack direction='row' spacing={0.5}>
        <Chip size='sm' color={props.workflow.is_template ? 'success' : 'danger'} sx={{ fontWeight: 'lg' }}>
          Template
        </Chip>
        <Chip size='sm' color={props.workflow.is_frozen ? 'success' : 'danger'} sx={{ fontWeight: 'lg' }}>
          Frozen
        </Chip>
        <Chip size='sm' color={props.workflow.is_finished ? 'success' : 'danger'} sx={{ fontWeight: 'lg' }}>
          Finished
        </Chip>
      </Stack>
    </Box>
  )
}

export default WorkflowInstanceInfo
