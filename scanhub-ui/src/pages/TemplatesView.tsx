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
import { useQuery } from '@tanstack/react-query'

import { examApi } from '../api'
import { ExamOut, WorkflowOut} from '../openapi/generated-client/exam'
import ExamModal from '../components/ExamModal'
import ExamItem, {ExamMenu} from '../components/ExamItem'
import WorkflowItem, {WorkflowMenu} from '../components/WorkflowItem'
import TaskItem from '../components/TaskItem'
import { ITEM_UNSELECTED } from '../interfaces/components.interface'
import WorkflowModal from '../components/WorkflowModal'
import TaskModal from '../components/TaskModal'


export default function TemplatesView() {
  const [examModalOpen, setExamModalOpen] = React.useState(false)
  const [workflowModalOpen, setWorkflowModalOpen] = React.useState(false)
  const [taskModalOpen, setTaskModalOpen] = React.useState(false)

  const [selectedExam, setSelectedExam] = React.useState<undefined | number>(undefined)
  const [selectedWorkflow, setSelectedWorkflow] = React.useState<undefined | number>(undefined)

  // Reset selectedWorkflow and selectedTask when selectedExam changes to undefined
  React.useEffect(() => {
    if (!selectedExam) {
      setSelectedWorkflow(undefined)
    }
  }, [selectedExam])


  const { data: exams, refetch: refetchExams } = useQuery<ExamOut[]>({
    queryKey: ['allExamTemplates'],
    queryFn: async () => {
      return await examApi
        .getAllExamTemplatesApiV1ExamTemplatesAllGet()
        .then((result) => {
          return result.data
        })
    },
  })

  return (
    <Stack direction="row" alignItems="flex-start" width='100vw'>

      <Stack direction='column' alignContent='center' flex={1} spacing={2} sx={{ p: 2 }}>
        <Button startDecorator={<Add />} onClick={() => setExamModalOpen(true)}>
          Create Exam Template
        </Button>

        <ExamModal
          isOpen={examModalOpen}
          setOpen={setExamModalOpen}
          onSubmit={() => refetchExams()}
          modalType='create'
          createTemplate={true}
          parentId={undefined}
        />
        {
          exams?.map((exam, index) => (
            <Stack direction="row" key={`exam-${exam.id}`}>
              <ExamItem 
                item={exam}
                onClick={() => {selectedExam === index ? setSelectedExam(undefined) : setSelectedExam(index)}}
                selection={selectedExam === index ? {
                  type: 'exam',
                  name: exams[index].name,
                  itemId: exams[index].id,
                  status: exams[index].status
                } : ITEM_UNSELECTED}
              />
              <ExamMenu item={exam} refetchParentData={refetchExams} />
            </Stack>
          ))
        }
      </Stack>

      <Stack direction='column' alignContent='center' flex={1} spacing={2} sx={{ p: 2 }}>
        <Button startDecorator={<Add />} onClick={() => setWorkflowModalOpen(true)} disabled={selectedExam === undefined}>
          Create Workflow Template
        </Button>

        <WorkflowModal
          isOpen={workflowModalOpen}
          setOpen={setWorkflowModalOpen}
          onSubmit={() => refetchExams()}
          modalType='create'
          createTemplate={true}
          parentId={exams && selectedExam !== undefined ? exams[selectedExam].id : undefined}
        />
        {
          exams && selectedExam !== undefined && exams[selectedExam]?.workflows?.map((workflow: WorkflowOut, index: number) => (
            <Stack direction="row" key={`workflow-${workflow.id}`}>
              <WorkflowItem 
                item={workflow}
                onClick={() => {selectedWorkflow === index ? setSelectedWorkflow(undefined) : setSelectedWorkflow(index)}}
                selection={ selectedWorkflow === index ? {
                  type: 'workflow',
                  name: exams[selectedExam].workflows[index].name,
                  itemId: exams[selectedExam].workflows[index].id,
                  status: exams[selectedExam].workflows[index].status
                } : ITEM_UNSELECTED }
              />
              <WorkflowMenu item={workflow} refetchParentData={refetchExams} />
            </Stack>
          ))
        }
      </Stack>

      <Stack direction='column' alignContent='center' flex={1} spacing={2} sx={{ p: 2 }}>
        <Button startDecorator={<Add />} onClick={() => setTaskModalOpen(true)} disabled={selectedWorkflow === undefined}>
          Create Task Template
        </Button>

        <TaskModal
          isOpen={taskModalOpen}
          setOpen={setTaskModalOpen}
          onSubmit={() => refetchExams()}
          modalType='create'
          createTemplate={true}
          parentId={exams && selectedExam !== undefined && selectedWorkflow !== undefined ? exams[selectedExam].workflows[selectedWorkflow].id : undefined}
        />
        {
          exams && selectedExam !== undefined && selectedWorkflow !== undefined && exams[selectedExam].workflows[selectedWorkflow]?.tasks?.map((task) => (
            <TaskItem 
              key={`task-${task.id}`}
              item={task}
              refetchParentData={refetchExams}
              onClick={() => {}}
              selection={ITEM_UNSELECTED}
            />
          ))
        }
      </Stack>

    </Stack>
  )
}