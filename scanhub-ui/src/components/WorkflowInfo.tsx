/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * WorkflowInfo.tsx is responsible for rendering additional information of a workflow item.
 */
import Box from '@mui/joy/Box'
import Typography from '@mui/joy/Typography'
import * as React from 'react'

import { WorkflowOut } from '../generated-client/exam'


function WorkflowInfo({ workflow }: { workflow: WorkflowOut }) {

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
          {workflow.name}
        </Typography>

        <Typography fontSize='sm'>Description</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {workflow.description}
        </Typography>

        <Typography fontSize='sm'>Comment</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {workflow.comment}
        </Typography>

        <Typography fontSize='sm'>Status</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {workflow.status}
        </Typography>

        <Typography fontSize='sm'>Is Template</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {workflow.is_template ? 'True' : 'False'}
        </Typography>

        <Typography fontSize='sm'>ID</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {workflow.id}
        </Typography>

        <Typography fontSize='sm'>Creator</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {workflow.creator}
        </Typography>

        <Typography fontSize='sm'>Created</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {new Date(workflow.datetime_created).toLocaleString()}
        </Typography>

        <Typography fontSize='sm'>Updated</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {workflow.datetime_updated ? new Date(workflow.datetime_updated).toLocaleString() : '-'}
        </Typography>
      </Box>
    </Box>
  )
}

export default WorkflowInfo
