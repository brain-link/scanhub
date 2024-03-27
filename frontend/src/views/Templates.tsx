// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
// PatientTable.tsx is responsible for rendering the patient table view.
import * as React from 'react'
import Box from '@mui/joy/Box'
import ExamTemplateList from '../components/ExamTemplateList'


export default function Templates() {

  return (
    <Box sx={{ m: 3 }}>
      <ExamTemplateList/>
    </Box>
  )
}
