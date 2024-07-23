/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * TemplatesView.tsx is responsible for rendering all existing template items
 * and allows to add new templates or edit existing templates.
 */
import Add from '@mui/icons-material/Add'
import Button from '@mui/joy/Button'
import Stack from '@mui/joy/Stack'
import * as React from 'react'
import { useContext } from 'react'
import { useQuery } from 'react-query'

import LoginContext from '../LoginContext'
import { examApi } from '../api'
import { ExamOut } from '../generated-client/exam'
import ExamModal from '../components/ExamModal'
import AccordionWithMenu from '../components/AccordionWithMenu'
import ExamItem, {ExamMenu} from '../components/ExamItem'
import WorkflowItem, {WorkflowMenu} from '../components/WorkflowItem'
import TaskItem from '../components/TaskItem'

export default function Templates() {
  const [modalOpen, setModalOpen] = React.useState(false)
  const [user] = useContext(LoginContext)

  // const {data: exams, isLoading, isError, refetch} = useQuery<ExamOut[]>({
  const { data: exams, refetch } = useQuery<ExamOut[]>({
    queryKey: ['allExamTemplates'],
    queryFn: async () => {
      return await examApi
        .getAllExamTemplatesApiV1ExamTemplatesAllGet({ headers: { Authorization: 'Bearer ' + user?.access_token } })
        .then((result) => {
          return result.data
        })
    },
  })

  return (
    <Stack direction='column' alignContent='center' width='20%' margin='auto' spacing={2} sx={{ p: 2 }}>
      <Button startDecorator={<Add />} onClick={() => setModalOpen(true)}>
        Create Exam Template
      </Button>

      <ExamModal
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

      {exams?.map((exam) => (
        <AccordionWithMenu 
          key={`exam-${exam.id}`}
          accordionSummary={<ExamItem exam={exam} />}
          accordionMenu={<ExamMenu data={exam} refetchParentData={refetch} />}
        >
          {exam.workflows?.map((workflow) => (
            <AccordionWithMenu 
              key={`workflow-${workflow.id}`}
              accordionSummary={<WorkflowItem data={workflow} refetchParentData={refetch} />}
              accordionMenu={<WorkflowMenu data={workflow} refetchParentData={refetch} />}
            >
              {workflow.tasks?.map((task) => (
                <TaskItem key={`task-${task.id}`} data={task} refetchParentData={refetch} />
              ))}
            </AccordionWithMenu>
          ))}
        </AccordionWithMenu>
      ))}

      {/* {exams?.map((exam, idx) => (
        <ExamTemplateItem
          key={idx}
          data={exam}
          onClicked={() => {}}
          onDeleted={() => {
            refetch()
          }}
        />
      ))} */}
    </Stack>
  )
}