/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * TaskInstanceItem.tsx is responsible for rendering a single task instance item
 * in the task instance list of a workflow.
 */
import AssignmentIcon from '@mui/icons-material/Assignment'
// Icons
// Mui joy components
import ListItem from '@mui/joy/ListItem'
import ListItemContent from '@mui/joy/ListItemContent'
import ListItemDecorator from '@mui/joy/ListItemDecorator'
import Typography from '@mui/joy/Typography'
import * as React from 'react'

// Sub-components, interfaces, client
import { TaskOut } from '../generated-client/exam'
import { InstanceInterface } from '../interfaces/components.interface'

// function ExamInstanceItem({ data: exam, refetchParentData, isSelected }: ComponentProps<ExamOut>) {
function TaskInstanceItem({ data: task }: InstanceInterface<TaskOut>) {

  return (
    <ListItem sx={{ width: '100%', p: 0.5 }}>
      <ListItemDecorator sx={{ align: 'center', justify: 'center' }}>
        <AssignmentIcon fontSize='small' />
      </ListItemDecorator>

      <ListItemContent>
        <Typography level='title-sm'>{task.description ? task.description : 'Task'}</Typography>

        <Typography level='body-xs' textColor='text.tertiary'>
          {`Created: ${new Date(task.datetime_created).toDateString()}`}
        </Typography>
      </ListItemContent>
    </ListItem>
  )
}

export default TaskInstanceItem
