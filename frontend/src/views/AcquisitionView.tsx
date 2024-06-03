// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
// PatientIndex.tsx is responsible for rendering the patient view. It is the entry point for the patient view.

import * as React from 'react'
import AddSharpIcon from '@mui/icons-material/AddSharp'
// import KeyboardArrowLeftSharpIcon from '@mui/icons-material/KeyboardArrowLeftSharp'
// import KeyboardArrowRightSharpIcon from '@mui/icons-material/KeyboardArrowRightSharp'
import Badge from '@mui/joy/Badge'
// Mui Joy
import Box from '@mui/joy/Box'
import IconButton from '@mui/joy/IconButton'
import ListItemButton from '@mui/joy/ListItemButton'
import List from '@mui/joy/List'
import ListDivider from '@mui/joy/ListDivider'
import Stack from '@mui/joy/Stack'
import Typography from '@mui/joy/Typography'
import Accordion from '@mui/joy/Accordion'
import Tooltip from '@mui/joy/Tooltip'
import AccordionDetails from '@mui/joy/AccordionDetails'
import AccordionSummary from '@mui/joy/AccordionSummary'

import { useQuery } from 'react-query'
// import { useMutation } from 'react-query'
import { useParams } from 'react-router-dom'

import ExamItem from '../components/ExamInstanceItem'
import WorkflowItem from '../components/WorkflowInstanceItem'
import TaskItem from '../components/TaskInstanceItem'

import PatientInfo from '../components/PatientInfo'
import ExamInstanceInfo from '../components/ExamInstanceInfo'
import WorkflowInstanceInfo from '../components/WorkflowInstanceInfo'
import TaskInstanceInfo from '../components/TaskInstanceInfo'

import ExamFromTemplateModal from '../components/ExamFromTemplateModal'


// Import interfaces, api services and global variables
import { navigation, patientView } from '../utils/size_vars'

import { examApi, patientApi } from '../api'
import { ExamOut } from '../generated-client/exam'
import { PatientOut } from '../generated-client/patient'
// import { WorkflowOut } from '../generated-client/exam'
import LoginContext from '../LoginContext'


function PatientIndex() {

  const params = useParams()

  // Visibility of side panel containing patient info and exam list
  // const [sidePanelOpen, setSidePanelOpen] = React.useState(true)
  // Modal states for exam
  const [examModalOpen, setExamModalOpen] = React.useState(false)
  // List of jobs
  // const [workflows, setWorkflows] = React.useState<WorkflowOut[] | undefined>(undefined)

  const [user, ] = React.useContext(LoginContext);

  // useQuery for caching the fetched data
  const {
    data: patient,
    // refetch: refetchPatient,
    isLoading: patientLoading,
    isError: patientError,
  } = useQuery<PatientOut, Error>({
    queryKey: ['patient', params.patientId],
    queryFn: async () => { return await patientApi.getPatientPatientIdGet(Number(params.patientId)).then((result) => {return result.data})}
  })


  // Query all exams of the patient
  const {
    data: exams,
    refetch: refetchExams,
    // isLoading: examsLoading,
    // isError: examsError,
  } = useQuery<ExamOut[], Error>({
    queryKey: ['exam', params.patientId],
    queryFn: async () => {
      return await examApi.getAllPatientExamsApiV1ExamAllPatientIdGet(
        Number(
          params.patientId),
          {headers: {Authorization: 'Bearer ' + user?.access_token}}
        ).then((result) => {return result.data}
      )
    }
  })


  return (
    <Stack 
      direction='row' 
      sx={{
        height: `calc(100vh - ${navigation.height})`,
        width: '100%',
        overflow: 'clip'
      }}
    >
      <Box
        sx={{
          width: patientView.drawerWidth,
          overflow: 'clip',
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
            overflow: 'scroll'
          }}
        >
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 3 }}>
            <Typography level='title-md'> Exams </Typography>
            <Badge badgeContent={exams?.length} color='primary' />
          </Box>

          <IconButton
            variant='soft'
            sx={{ '--IconButton-size': patientView.iconButtonSize }}
            onClick={() => setExamModalOpen(true)}
          >
            <AddSharpIcon />
          </IconButton>

          <ExamFromTemplateModal isOpen={examModalOpen} setOpen={setExamModalOpen} parentId={String(params.patientId)} onSubmit={refetchExams}/>

        </Box>

        <ListDivider />

        {/* List of exams */}
        <List sx={{ pt: 0 }}>
          {
            exams?.map(exam => (

              <Accordion key={`exam-${exam.id}`}>

                <Tooltip
                  placement="right"
                  variant="outlined"
                  describeChild={false}
                  arrow
                  title={<ExamInstanceInfo exam={exam} />}
                >
                  <AccordionSummary>
                    <ExamItem data={exam} refetchParentData={refetchExams}/>
                  </AccordionSummary>

                </Tooltip>
                
                <AccordionDetails>
                  {
                    exam.workflows?.map(workflow => (

                      <Accordion key={`workflow-${workflow.id}`}>

                        <Tooltip
                          placement="right"
                          variant="outlined"
                          describeChild={false}
                          arrow
                          title={<WorkflowInstanceInfo workflow={workflow} />}
                        >
                          <AccordionSummary>
                            <WorkflowItem data={workflow} refetchParentData={refetchExams} />
                          </AccordionSummary>
                        </Tooltip>

                        <AccordionDetails>
                          <List>
                            {
                              workflow.tasks?.map(task => (
                                <Tooltip
                                  key={`task-${task.id}`}
                                  placement="right"
                                  variant="outlined"
                                  arrow
                                  title={<TaskInstanceInfo task={task} />}
                                >
                                  <ListItemButton>
                                    <TaskItem data={task} refetchParentData={refetchExams}/>
                                  </ListItemButton>
                                </Tooltip>
                              ))
                            }
                          </List>
                        </AccordionDetails>

                      </Accordion>

                    ))
                  }
                </AccordionDetails>
              </Accordion>
            ))
          }

        </List>
      </Box>

      {/* job view controller */}
      <Box sx={{ width: '100%', bgcolor: 'background.componentBg' }}>
        {/* <JobList
          // Implementation of new interface may be required
          data={workflows ? workflows : []}
          refetchParentData={refetchExams}
          isSelected={params.examId ? true : false}
        /> */}
      </Box>

    </Stack>
  )
}

export default PatientIndex
