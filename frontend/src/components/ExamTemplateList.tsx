// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
// PatientTable.tsx is responsible for rendering the patient table view.
import * as React from 'react'
import Stack from '@mui/joy/Stack'
import Add from '@mui/icons-material/Add'
import Button from '@mui/joy/Button'

import ExamTemplateItem from '../components/ExamTemplateItem'
import AlertItem from '../components/AlertItem'
import ExamTemplateCreateModal from '../components/ExamTemplateCreateModal'

import { Alerts } from '../interfaces/components.interface'
import { useQuery } from 'react-query'
import { ExamOut } from "../generated-client/exam";
import { examApi } from '../api'


export default function ExamTemplateList() {

  const [modalOpen, setModalOpen] = React.useState(false)

  const {data: exams, isLoading, isError, refetch} = useQuery<ExamOut[]>({
    queryKey: ['exams'],
    queryFn: async () => { return await examApi.getAllExamTemplatesApiV1ExamTemplatesAllGet().then((result) => {return result.data})}
  })

  return (
    <Stack
      direction="column"
      alignItems="flex-start"
      spacing={2}
      sx={{p: 2}}
    >
      <Button
        startDecorator={<Add />}
        onClick={() => setModalOpen(true)}
      >
        Create Exam Template
      </Button>

      <ExamTemplateCreateModal
        isOpen={modalOpen}
        setOpen={setModalOpen}
        onSubmit={
          // (newExam: ExamOut) => { exams?.push(newExam) }
          () => { refetch() }
        }
        onClose={() => {}}
      />

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
