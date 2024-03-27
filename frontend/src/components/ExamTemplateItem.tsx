// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
// PatientTable.tsx is responsible for rendering the patient table view.
import Typography from '@mui/joy/Typography'
import Card from '@mui/joy/Card'
import CardContent from '@mui/joy/CardContent'
import * as React from 'react'
import { ExamOut } from "../generated-client/exam";
import { TemplateItemInterface } from '../interfaces/components.interface'


export default function ExamTemplateItem(prop: TemplateItemInterface<ExamOut>) {

  return (
    <Card variant="outlined">
        <CardContent>
        <Typography level="title-md">Exam</Typography>
        <Typography>{ prop.item.id }</Typography>
        </CardContent>
    </Card>
  )
}
