// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
// PatientTable.tsx is responsible for rendering the patient table view.
import Stack from '@mui/joy/Stack'
import * as React from 'react'
import { useQuery } from 'react-query'
import { ExamOut } from "../generated-client/exam";
import { examApi } from '../Api'
import AlertItem from '../components/AlertItem'
import { Alerts } from '../interfaces/components.interface'
import ExamTemplateItem from '../components/ExamTemplateItem'


export default function ExamTemplateList() {

  const {data: exams, isLoading, isError} = useQuery<ExamOut[]>({
    queryKey: ['exams'],
    queryFn: async () => { return await examApi.getAllExamTemplatesApiV1ExamTemplatesAllGet().then((result) => {return result.data})}
  })

  return (
    <Stack
      direction="column"
      alignItems="flex-start"
      spacing={2}
    >
      {
        exams?.map((exam) => (
          <ExamTemplateItem
            item={exam}
            onClicked={() => {}}
          />
        ))
      }
    </Stack>
  )
}
