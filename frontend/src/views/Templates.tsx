// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
// PatientTable.tsx is responsible for rendering the patient table view.
import * as React from 'react'
import Box from '@mui/joy/Box'
import Divider from '@mui/joy/Divider'

import Stack from '@mui/joy/Stack'

import ExamTemplateList from '../components/ExamTemplateList'
import WorkflowTemplateList from '../components/WorkflowTemplateList'
import TaskTemplateList from '../components/TaskTemplateList'

export default function Templates() {

  

  return (
    <Stack
      direction="row"
      divider={<Divider orientation="vertical" />}
      spacing={2}
      justifyContent="center"
    >

      <Box sx={{ p: 3 }}>
        <ExamTemplateList/>
      </Box>

      <Box sx={{ p: 3 }}>
        <WorkflowTemplateList/>
      </Box>

      <Box sx={{ p: 3 }}>
        <TaskTemplateList/>
      </Box>


    </Stack>
    
  )
}
