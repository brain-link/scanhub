// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
// PatientTable.tsx is responsible for rendering the patient table view.
import * as React from 'react'
import Grid from '@mui/joy/Grid'

import ExamTemplateList from '../components/ExamTemplateList'
import WorkflowTemplateList from '../components/WorkflowTemplateList'
import TaskTemplateList from '../components/TaskTemplateList'

import { navigation } from '../utils/size_vars'

export default function Templates() {

  return (
    <Grid 
      container 
      spacing={2} 
      sx={{ 
        flexGrow: 1,
        m: 0,
        height: `calc(100vh - ${navigation.height})`,
        '--Grid-borderWidth': '1px',
        '& > div': {
          borderRight: 'var(--Grid-borderWidth) solid',
          borderColor: 'divider',
        },
      }}
    >

      <Grid xs={4}>
        <ExamTemplateList/>
      </Grid>

      <Grid xs={4}>
        <WorkflowTemplateList/>
      </Grid>

      <Grid xs={4}>
        <TaskTemplateList/>
      </Grid>

    </Grid>
  )
}
