/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * ExamTemplateList.tsx is responsible for rendering a list of template item.
 */
import Add from '@mui/icons-material/Add'
import Button from '@mui/joy/Button'
import Stack from '@mui/joy/Stack'
import * as React from 'react'
import { useContext } from 'react'
// import { Alerts } from '../interfaces/components.interface'
import { useQuery } from 'react-query'

import LoginContext from '../LoginContext'
import { examApi } from '../api'
// import AlertItem from '../components/AlertItem'
import ExamTemplateCreateModal from '../components/ExamTemplateCreateModal'
import ExamTemplateItem from '../components/ExamTemplateItem'
import { ExamOut } from '../generated-client/exam'

export default function ExamTemplateList() {
  const [modalOpen, setModalOpen] = React.useState(false)
  const [user] = useContext(LoginContext)

  // const {data: exams, isLoading, isError, refetch} = useQuery<ExamOut[]>({
  const { data: exams, refetch } = useQuery<ExamOut[]>({
    queryKey: ['exams'],
    queryFn: async () => {
      return await examApi
        .getAllExamTemplatesApiV1ExamTemplatesAllGet({ headers: { Authorization: 'Bearer ' + user?.access_token } })
        .then((result) => {
          return result.data
        })
    },
  })

  return (
    <Stack direction='column' alignItems='flex-start' spacing={2} sx={{ p: 2 }}>
      <Button startDecorator={<Add />} onClick={() => setModalOpen(true)}>
        Create Exam Template
      </Button>

      <ExamTemplateCreateModal
        isOpen={modalOpen}
        setOpen={setModalOpen}
        onSubmit={
          // (newExam: ExamOut) => { exams?.push(newExam) }
          () => {
            refetch()
          }
        }
        onClose={() => {}}
      />

      {exams?.map((exam, idx) => (
        <ExamTemplateItem
          key={idx}
          item={exam}
          onClicked={() => {}}
          onDeleted={() => {
            refetch()
          }}
        />
      ))}
    </Stack>
  )
}
