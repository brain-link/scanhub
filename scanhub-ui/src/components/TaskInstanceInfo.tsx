/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * TaskInstanceInfo.tsx is responsible for rendering additional information
 * of a task instance item.
 */
import * as React from 'react'

import Box from '@mui/joy/Box'
import Chip from '@mui/joy/Chip'
import Stack from '@mui/joy/Stack'
import Typography from '@mui/joy/Typography'

import { TaskOut } from '../generated-client/exam'
import { InstanceInterface } from '../interfaces/components.interface'


function TaskInstanceInfo({ data: task }: InstanceInterface<TaskOut>) {
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
        <Typography fontSize='sm'>Description</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {task.description}
        </Typography>

        <Typography fontSize='sm'>ID</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {task.id}
        </Typography>

        <Typography fontSize='sm'>Type</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {task.type}
        </Typography>

        <Typography fontSize='sm'>Arguments</Typography>
        <Stack direction='column'>
          {task.args &&
            Object.entries(task.args).map((arg, index) => (
              <Typography key={index} level='body-sm' textColor='text.primary'>
                {arg[0]}: {arg[1]}
              </Typography>
            ))}
        </Stack>

        <Typography fontSize='sm'>Artifacts</Typography>
        <Stack direction='column'>
          {task.artifacts &&
            Object.entries(task.artifacts).map((artifact, index) => (
              <Typography key={index} level='body-sm' textColor='text.primary'>
                {artifact[0]}: {artifact[1]}
              </Typography>
            ))}
        </Stack>

        <Typography fontSize='sm'>Destinations</Typography>
        <Stack direction='column'>
          {task.destinations &&
            Object.entries(task.destinations).map((destination, index) => (
              <Typography key={index} level='body-sm' textColor='text.primary'>
                {destination[0]}: {destination[1]}
              </Typography>
            ))}
        </Stack>

        <Typography fontSize='sm'>Created</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {new Date(task.datetime_created).toDateString()}
        </Typography>

        <Typography fontSize='sm'>Status</Typography>
        <Stack direction='row' spacing={0.5}>
          <Chip size='sm' color={task.is_template ? 'success' : 'danger'} sx={{ fontWeight: 'lg' }}>
            Template
          </Chip>
          <Chip size='sm' color={task.is_frozen ? 'success' : 'danger'} sx={{ fontWeight: 'lg' }}>
            Frozen
          </Chip>
        </Stack>
      </Box>
    </Box>
  )
}

export default TaskInstanceInfo
