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
import Accordion from '@mui/joy/Accordion'
import AccordionDetails from '@mui/joy/AccordionDetails'
import AccordionSummary from '@mui/joy/AccordionSummary'
// import KeyboardArrowLeftSharpIcon from '@mui/icons-material/KeyboardArrowLeftSharp'
// import KeyboardArrowRightSharpIcon from '@mui/icons-material/KeyboardArrowRightSharp'
import Badge from '@mui/joy/Badge'
// Mui Joy
import Box from '@mui/joy/Box'
// import ListDivider from '@mui/joy/ListDivider'
import Divider from '@mui/joy/Divider'
import IconButton from '@mui/joy/IconButton'
import List from '@mui/joy/List'
import ListItemButton from '@mui/joy/ListItemButton'
import Sheet from '@mui/joy/Sheet'
import Tooltip from '@mui/joy/Tooltip'
import Typography from '@mui/joy/Typography'
import * as React from 'react'
import { useQuery } from 'react-query'
// import { useMutation } from 'react-query'
import { useParams } from 'react-router-dom'

// import { WorkflowOut } from '../generated-client/exam'
import LoginContext from '../LoginContext'
import { examApi, patientApi } from '../api'
import AcquisitionControl from '../components/AcquisitionControl'
import DicomViewer from '../components/DicomViewer'
import ExamFromTemplateModal from '../components/ExamFromTemplateModal'
import ExamInstanceInfo from '../components/ExamInstanceInfo'
import ExamItem from '../components/ExamInstanceItem'
import PatientInfo from '../components/PatientInfo'
import TaskInstanceInfo from '../components/TaskInstanceInfo'
import TaskItem from '../components/TaskInstanceItem'
import WorkflowInstanceInfo from '../components/WorkflowInstanceInfo'
import WorkflowItem from '../components/WorkflowInstanceItem'
import { ExamOut } from '../generated-client/exam'
import { PatientOut } from '../generated-client/patient'

function PatientIndex() {
  const params = useParams()

  // Visibility of side panel containing patient info and exam list
  // const [sidePanelOpen, setSidePanelOpen] = React.useState(true)
  // Modal states for exam
  const [examModalOpen, setExamModalOpen] = React.useState(false)
  // List of jobs
  // const [workflows, setWorkflows] = React.useState<WorkflowOut[] | undefined>(undefined)

  const [user] = React.useContext(LoginContext)

  // useQuery for caching the fetched data
  const {
    data: patient,
    // refetch: refetchPatient,
    isLoading: patientLoading,
    isError: patientError,
  } = useQuery<PatientOut, Error>({
    queryKey: ['patient', params.patientId],
    queryFn: async () => {
      return await patientApi.getPatientPatientIdGet(Number(params.patientId)).then((result) => {
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
    queryKey: ['exam', params.patientId],
    queryFn: async () => {
      return await examApi
        .getAllPatientExamsApiV1ExamAllPatientIdGet(Number(params.patientId), {
          headers: { Authorization: 'Bearer ' + user?.access_token },
        })
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

          <ExamFromTemplateModal
            isOpen={examModalOpen}
            setOpen={setExamModalOpen}
            parentId={String(params.patientId)}
            onSubmit={refetchExams}
          />
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
          <List size='sm' sx={{ pt: 0, overflow: 'scroll', '--ListItem-radius': (theme) => theme.vars.radius.sm }}>
            {exams?.map((exam) => (
              <Accordion key={`exam-${exam.id}`}>
                <Tooltip
                  placement='right'
                  variant='outlined'
                  describeChild={false}
                  arrow
                  title={<ExamInstanceInfo exam={exam} />}
                >
                  <AccordionSummary>
                    <ExamItem data={exam} refetchParentData={refetchExams} />
                  </AccordionSummary>
                </Tooltip>

                <AccordionDetails>
                  {exam.workflows?.map((workflow) => (
                    <Accordion key={`workflow-${workflow.id}`}>
                      <Tooltip
                        placement='right'
                        variant='outlined'
                        describeChild={false}
                        arrow
                        title={<WorkflowInstanceInfo workflow={workflow} />}
                      >
                        <AccordionSummary>
                          <WorkflowItem data={workflow} refetchParentData={refetchExams} />
                        </AccordionSummary>
                      </Tooltip>

                      <AccordionDetails>
                        <List size='sm' sx={{ pt: 0, '--ListItem-radius': (theme) => theme.vars.radius.sm }}>
                          {workflow.tasks?.map((task) => (
                            <Tooltip
                              key={`task-${task.id}`}
                              placement='right'
                              variant='outlined'
                              arrow
                              title={<TaskInstanceInfo task={task} />}
                            >
                              <ListItemButton>
                                <TaskItem data={task} refetchParentData={refetchExams} />
                              </ListItemButton>
                            </Tooltip>
                          ))}
                        </List>
                      </AccordionDetails>
                    </Accordion>
                  ))}
                </AccordionDetails>
              </Accordion>
            ))}
          </List>
        </Box>

        {/* Trigger workflow engine */}
        <Divider />
        <AcquisitionControl />
      </Sheet>

      <DicomViewer />
    </Box>
  )
}

export default PatientIndex
