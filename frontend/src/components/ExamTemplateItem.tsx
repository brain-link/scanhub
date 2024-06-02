// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
// PatientTable.tsx is responsible for rendering the patient table view.
import Typography from '@mui/joy/Typography'
import Card from '@mui/joy/Card'
import CardContent from '@mui/joy/CardContent'
import * as React from 'react'
import { ExamOut } from '../generated-client/exam';
import { TemplateItemInterface } from '../interfaces/components.interface'


export default function ExamTemplateItem(prop: TemplateItemInterface<ExamOut>) {

  return (
    <Card variant="outlined" sx={{ width: '100%' }}>
        <CardContent>
        <Typography level="title-md">Exam: { prop.item.name }</Typography>
        
        <Typography level='body-sm' textColor='text.tertiary'>ID: { prop.item.id }</Typography>
        <Typography level='body-sm' textColor='text.tertiary'>Site: { prop.item.site }</Typography>
        <Typography level='body-sm' textColor='text.tertiary'>Address: { prop.item.address }</Typography>
        <Typography level='body-sm' textColor='text.tertiary'>Creator: { prop.item.creator }</Typography>
        <Typography level='body-sm' textColor='text.tertiary'>Created: { new Date(prop.item.datetime_created).toDateString() }</Typography>
        <Typography level='body-sm' textColor='text.tertiary'>Updated: { prop.item.datetime_updated ? new Date(prop.item.datetime_updated).toDateString() : '-'}</Typography>

        </CardContent>
    </Card>
  )
}
