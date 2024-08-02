/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * AcquisitionView.tsx is responsible for rendering the acquisition view.
 * The acquisition view is the main interaction point and contains instances of
 * exams, workflows and tasks of a certain patients.
 * It allows to execute them and view results, i.e. dicom images.
 */
import AddSharpIcon from '@mui/icons-material/AddSharp'
import Badge from '@mui/joy/Badge'
import Box from '@mui/joy/Box'
import Divider from '@mui/joy/Divider'
import IconButton from '@mui/joy/IconButton'
import Sheet from '@mui/joy/Sheet'
import Typography from '@mui/joy/Typography'
import * as React from 'react'
import { useQuery } from 'react-query'
import { useParams } from 'react-router-dom'

import { examApi, patientApi } from '../api'
import AcquisitionControl from '../components/AcquisitionControl'
import DicomViewer from '../components/DicomViewer'
import PatientInfo from '../components/PatientInfo'
import { PatientOut } from '../generated-client/patient'
import { ExamOut } from '../generated-client/exam'
import ExamFromTemplateModal from '../components/ExamFromTemplateModal'
import AccordionWithMenu from '../components/AccordionWithMenu'
import ExamItem, { ExamMenu } from '../components/ExamItem'
import WorkflowItem, { WorkflowMenu } from '../components/WorkflowItem'
import TaskItem from '../components/TaskItem'
import { ITEM_UNSELECTED, ItemSelection } from '../interfaces/components.interface'


function PatientIndex() {
  const params = useParams()

  const [examModalOpen, setExamModalOpen] = React.useState(false)
  const [itemSelection, setItemSelection] = React.useState<ItemSelection>(ITEM_UNSELECTED)

  // useQuery for caching the fetched data
  const {
    data: patient,
    // refetch: refetchPatient,
    isLoading: patientLoading,
    isError: patientError,
  } = useQuery<PatientOut, Error>({
    queryKey: ['patient', params.patientId],
    queryFn: async () => {
      return await patientApi.getPatientApiV1PatientPatientIdGet(Number(params.patientId)).then((result) => {
        return result.data
      })
    },
  })

  // Query all exams of the patient
  const {
    data: exams,
    refetch: refetchExams,
    // isLoading: examsLoading,
    // isError: examsError,
  } = useQuery<ExamOut[], Error>({
    queryKey: ['allExams', params.patientId],
    queryFn: async () => {
      return await examApi
        .getAllPatientExamsApiV1ExamAllPatientIdGet(Number(params.patientId))
        .then((result) => {
          return result.data
        })
    },
  })

  return (
    <Box
      sx={{
        flex: 1,
        display: 'flex',
        flexDirection: 'row',
        width: '100dvh',
      }}
    >
      <Sheet
        className='Sidebar'
        sx={{
          position: { xs: 'fixed', md: 'sticky' },
          height: 'calc(100dvh - var(--Navigation-height))',
          width: 'var(--Sidebar-width)',
          top: 0,
          p: 2,
          flexShrink: 0,
          display: 'flex',
          flexDirection: 'column',
          gap: 1.5,
          borderRight: '1px solid',
          borderColor: 'divider',
        }}
      >
        <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
          <Typography level='title-md'>Patient Info</Typography>
        </Box>
        <Divider />
        <PatientInfo patient={patient} isLoading={patientLoading} isError={patientError} />

        {/* <ListDivider /> */}
        <Divider />

        {/* Exam header */}
        <Box sx={{ display: 'flex', gap: 1, alignItems: 'center', justifyContent: 'space-between' }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 3 }}>
            <Typography level='title-md'>Exams</Typography>
            <Badge badgeContent={exams?.length} color='primary' />
          </Box>

          <IconButton size='sm' variant='plain' color='neutral' onClick={() => setExamModalOpen(true)}>
            <AddSharpIcon />
          </IconButton>
        </Box>

        <Divider />

        <Box
          sx={{
            minHeight: 0,
            overflow: 'hidden auto',
            flexGrow: 1,
            display: 'flex',
            flexDirection: 'column',
          }}
        >
          {exams?.map((exam) => (
            <AccordionWithMenu 
              key={`exam-${exam.id}`}
              accordionSummary={
                <ExamItem 
                  item={exam} 
                  onClick={() => {setItemSelection({type: 'exam', itemId: exam.id})}} 
                  selection={itemSelection}
                />
              }
              accordionMenu={
                <ExamMenu item={exam} refetchParentData={refetchExams} />
              }
            >
              {exam.workflows?.map((workflow) => (
                <AccordionWithMenu 
                  key={`workflow-${workflow.id}`}
                  accordionSummary={
                    <WorkflowItem 
                      item={workflow} 
                      onClick={() => {setItemSelection({type: 'workflow', itemId: workflow.id})}}
                      selection={itemSelection}
                    />
                  }
                  accordionMenu={<WorkflowMenu item={workflow} refetchParentData={refetchExams} />}
                >
                  {workflow.tasks?.map((task) => (
                    <TaskItem 
                      key={`task-${task.id}`} 
                      item={task} 
                      refetchParentData={refetchExams}
                      onClick={() => {setItemSelection({type: 'task', itemId: task.id})}}
                      selection={itemSelection}
                    />
                  ))}
                </AccordionWithMenu>
              ))}
            </AccordionWithMenu>
          ))}
        </Box>

        <Divider />
        <AcquisitionControl itemSelection={itemSelection}/>
      </Sheet>

      <ExamFromTemplateModal
        isOpen={examModalOpen}
        setOpen={setExamModalOpen}
        parentId={String(params.patientId)}
        onSubmit={refetchExams}
        createTemplate={false}
      />

      <DicomViewer />
    </Box>
  )
}

export default PatientIndex
