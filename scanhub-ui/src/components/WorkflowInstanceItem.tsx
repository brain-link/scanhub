/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * WorkflowInstanceItem.tsx is responsible for rendering additional information
 * of a workflow instance item.
 */
import SchemaIcon from '@mui/icons-material/Schema'
import ListItem from '@mui/joy/ListItem'
import ListItemContent from '@mui/joy/ListItemContent'
import ListItemDecorator from '@mui/joy/ListItemDecorator'
import Typography from '@mui/joy/Typography'
import * as React from 'react'

import { WorkflowOut } from '../generated-client/exam'
import { InstanceInterface } from '../interfaces/components.interface'


function WorkflowInstanceItem({ data: workflow }: InstanceInterface<WorkflowOut>) {
  return (
    <ListItem sx={{ width: '100%', p: 0.5 }}>
      <ListItemDecorator sx={{ align: 'center', justify: 'center' }}>
        <SchemaIcon fontSize='small' />
      </ListItemDecorator>

      <ListItemContent>
        <Typography level='title-sm'>{workflow.comment}</Typography>

        <Typography level='body-xs' textColor='text.tertiary'>
          {`Created: ${new Date(workflow.datetime_created).toDateString()}`}
        </Typography>
      </ListItemContent>
    </ListItem>
  )
}

export default WorkflowInstanceItem
