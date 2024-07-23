/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * ExamItem.tsx is responsible for rendering a single exam item.
 */
import ListAltIcon from '@mui/icons-material/ListAlt'
import Typography from '@mui/joy/Typography'
import * as React from 'react'
import { useMutation } from 'react-query'
import MoreHorizIcon from '@mui/icons-material/MoreHoriz'
import Dropdown from '@mui/joy/Dropdown'
import Menu from '@mui/joy/Menu'
import MenuButton from '@mui/joy/MenuButton'
import IconButton from '@mui/joy/IconButton'
import MenuItem from '@mui/joy/MenuItem'
import Tooltip from '@mui/joy/Tooltip'

// Sub-components, interfaces, client
import { ExamOut } from '../generated-client/exam'
import { ItemInterface } from '../interfaces/components.interface'
import Box from '@mui/joy/Box'
import { examApi } from '../api'
import LoginContext from '../LoginContext'
import WorkflowFromTemplateModal from './WorkflowFromTemplateModal'
import ExamInfo from './ExamInfo'
import WorkflowModal from './WorkflowModal'
// import ExamModal from './ExamModal'


export default function ExamItem({ exam }: { exam: ExamOut }) {

  return (
    <Tooltip
      placement='right'
      variant='outlined'
      describeChild={false}
      arrow
      title={<ExamInfo exam={exam} />}
    >
      <Box
        sx={{ 
          width: '100%', 
          p: 0.5, 
          display: 'flex',
          alignItems: 'center',
        }}
      >
        <ListAltIcon fontSize='small' />
        <Box 
          sx={{
            marginLeft: 0.5,
            p: 0.5, 
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'start',
          }}
        >
          <Typography level='title-sm'>
            {exam.name}
          </Typography>

          <Typography level='body-xs' textColor='text.tertiary'>
            {`Created: ${new Date(exam.datetime_created).toDateString()}`}
          </Typography>
        </Box>
      </Box>
    </Tooltip>
  )
}


export function ExamMenu({ data: exam, refetchParentData }: ItemInterface<ExamOut>) {

  const [workflowFromTemplateModalOpen, setWorkflowFromTemplateModalOpen] = React.useState(false)
  const [workflowCreateNewModalOpen, setWorkflowCreateNewModalOpen] = React.useState(false)
  // const [examModalOpen, setExamModalOpen] = React.useState(false)

  const [user] = React.useContext(LoginContext)

  // const updateExam = useMutation(async (data: Exam) => {
  //   await client.examService
  //     .update(data.id, data)
  //     .then(() => {
  //       refetchParentData()
  //     })
  //     .catch((err) => {
  //       console.log('Error on exam update: ', err)
  //     })
  // })

  const deleteExam = useMutation(async () => {
    await examApi
      .examDeleteApiV1ExamExamIdDelete(exam.id, { headers: { Authorization: 'Bearer ' + user?.access_token } })
      .then(() => {
        refetchParentData()
      })
  })

  return (
    <>
      <Dropdown>
        <MenuButton variant='plain' sx={{ size: 'xs' }} slots={{ root: IconButton }}>
          <MoreHorizIcon fontSize='small' />
        </MenuButton>
        <Menu id='context-menu' variant='plain' sx={{ zIndex: 'snackbar' }}>
          <MenuItem key='edit' onClick={() => {}}>
            Edit
          </MenuItem>
          <MenuItem
            key='delete'
            onClick={() => {
              deleteExam.mutate()
            }}
          >
            Delete
          </MenuItem>
          <MenuItem
            key='addFromTemplate'
            onClick={() => {
              setWorkflowFromTemplateModalOpen(true)
            }}
          >
            Add Workflow from Template
          </MenuItem>
          {
            exam.is_template ?
              <MenuItem
                key='addNew'
                onClick={() => {
                  setWorkflowCreateNewModalOpen(true)
                }}
              >
                Add new Workflow
              </MenuItem>
            : undefined
          }
        </Menu>
      </Dropdown>

      {/* <ExamModal   // TODO use ExamOut instead of Exam type
        data={exam}
        dialogOpen={examModalOpen}
        setDialogOpen={setExamModalOpen}
        handleModalSubmit={(data: Exam) => {
          updateExam.mutate(data)
        }}
      /> */}

      <WorkflowFromTemplateModal
        isOpen={workflowFromTemplateModalOpen}
        setOpen={setWorkflowFromTemplateModalOpen}
        parentId={exam.id}
        onSubmit={refetchParentData}
        createTemplate={exam.is_template}
      />
      {
        exam.is_template ?
          <WorkflowModal
            isOpen={workflowCreateNewModalOpen}
            setOpen={setWorkflowCreateNewModalOpen}
            parentId={exam.id}
            onSubmit={refetchParentData}
            createTemplate={exam.is_template}
          />
        : undefined
      }

    </>
  )
}
