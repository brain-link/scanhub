// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
// PatientIndex.tsx is responsible for rendering the patient view. It is the entry point for the patient view.
import AddSharpIcon from '@mui/icons-material/AddSharp'
import KeyboardArrowLeftSharpIcon from '@mui/icons-material/KeyboardArrowLeftSharp'
import KeyboardArrowRightSharpIcon from '@mui/icons-material/KeyboardArrowRightSharp'
import Badge from '@mui/joy/Badge'
// Mui Joy
import Box from '@mui/joy/Box'
import IconButton from '@mui/joy/IconButton'
import List from '@mui/joy/List'
import ListDivider from '@mui/joy/ListDivider'
import Stack from '@mui/joy/Stack'
import Typography from '@mui/joy/Typography'
import * as React from 'react'
import { useQuery } from 'react-query'
import { useMutation } from 'react-query'
import { useParams } from 'react-router-dom'

import client from '../client/exam-tree-queries'
import ExamItem from '../components/ExamItem'
import ExamModal from '../components/ExamModal'
import JobList from '../components/JobList'
// Import sub components
import PatientInfo from '../components/PatientInfo'
import ProcedureItem from '../components/ProcedureItem'
import ProcedureModal from '../components/ProcedureModal'
// Import interfaces, api services and global variables
import { Patient } from '../interfaces/data.interface'
import { Exam } from '../interfaces/data.interface'
import { Job } from '../interfaces/data.interface'
import { navigation, patientView } from '../utils/size_vars'

function PatientIndex() {
  const params = useParams()
  // Visibility of side panel containing patient info and exam list
  // const [sidePanelOpen, setSidePanelOpen] = React.useState(true)
  // Modal states for exam
  const [examModalOpen, setExamModalOpen] = React.useState(false)
  // List of jobs
  const [jobs, setJobs] = React.useState<Job[] | undefined>(undefined)

  // useQuery for caching the fetched data
  const {
    data: patient,
    // refetch: refetchPatient,
    isLoading: patientLoading,
    isError: patientError,
  } = useQuery<Patient, Error>({
    queryKey: ['patient', params.patientId],
    queryFn: () => client.patientService.get(Number(params.patientId)),
  })

  // Query all exams of the patient
  const {
    data: exams,
    refetch: refetchExams,
    // isLoading: examsLoading,
    // isError: examsError,
  } = useQuery<Exam[], Error>({
    queryKey: ['exam', params.patientId],
    queryFn: () => client.examService.getAll(Number(params.patientId)),
  })

  // This useEffect hook is executed when either exams or params.examId change
  React.useEffect(() => {
    if (params.examId && exams) {
      // Get the selected exam
      const exam = exams.filter((exam) => exam.id === String(params.examId))[0]
      // Set jobs if exam exists
      if (exam) {
        setJobs(exam.jobs)
      }
    }
  }, [exams, params.examId])

  // Mutations to create a new exam
  const createExam = useMutation(async (data: Exam) => {
    await client.examService
      .create(data)
      .then(() => {
        refetchExams()
      })
      .catch((err) => {
        console.log('Error on exam creation: ', err)
      })
  })

  return (
    <Stack direction='row' sx={{ height: `calc(100vh - ${navigation.height})`, width: '100%' }}>
      <Box
        sx={{
          // minWidth: sidePanelOpen ? patientView.drawerWidth : 0,
          // width: sidePanelOpen ? patientView.drawerWidth : 0,
          overflow: 'auto',
          bgcolor: 'background.componentBg',
          borderRight: '1px solid',
          borderColor: 'divider',
        }}
      >
        {/* Conditional rendering: Only rendered if patient exists */}
        {patient && <PatientInfo patient={patient} isLoading={patientLoading} isError={patientError} />}

        <ListDivider />

        {/* Exam list header */}
        <Box
          sx={{
            p: 1.5,
            display: 'flex',
            flexDirection: 'row',
            justifyContent: 'space-between',
            flexWrap: 'wrap',
            alignItems: 'center',
          }}
        >
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 3 }}>
            <Typography level='title-md'> Exams </Typography>
            <Badge badgeContent={exams?.length} color='primary' />
          </Box>

          <Box sx={{ display: 'flex', gap: 1 }}>
            <IconButton
              variant='soft'
              sx={{ '--IconButton-size': patientView.iconButtonSize }}
              onClick={() => setExamModalOpen(true)}
            >
              <AddSharpIcon />
            </IconButton>
          </Box>

          <ExamModal
            // When data is null, modal fills data in new empty procedure
            data={null}
            dialogOpen={examModalOpen}
            setDialogOpen={setExamModalOpen}
            handleModalSubmit={(data: Exam) => {
              createExam.mutate(data)
            }}
          />
        </Box>

        <ListDivider />

        {/* List of exams */}
        <List sx={{ pt: 0 }}>
          {// Check if exams are loading
          exams?.map((exam, index) => (
            <React.Fragment key={index}>
              <ExamItem data={exam} refetchParentData={refetchExams} isSelected={exam.id === String(params.examId)} />
              <ListDivider sx={{ m: 0 }} />
            </React.Fragment>
          ))}
        </List>
      </Box>

      {/* job view controller */}
      <Box sx={{ width: '100%', bgcolor: 'background.componentBg' }}>
        <JobList
          // Implementation of new interface may be required
          data={jobs ? jobs : []}
          refetchParentData={refetchExams}
          isSelected={params.examId ? true : false}
        />
      </Box>

    </Stack>
  )
}

export default PatientIndex
