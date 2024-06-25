/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * ExamInstanceItem.tsx is responsible for rendering a single exam instance item
 * in the exam instance list of a patient.
 */
import ListAltIcon from '@mui/icons-material/ListAlt'
// Icons
// import MoreHorizIcon from '@mui/icons-material/MoreHoriz'
// import Dropdown from '@mui/joy/Dropdown'
// Mui joy components
// import IconButton from '@mui/joy/IconButton'
import ListItem from '@mui/joy/ListItem'
// import ListItemDecorator from '@mui/joy/ListItemDecorator'
import ListItemContent from '@mui/joy/ListItemContent'
// import Menu from '@mui/joy/Menu'
// import MenuButton from '@mui/joy/MenuButton'
// import MenuItem from '@mui/joy/MenuItem'
import Typography from '@mui/joy/Typography'
import * as React from 'react'
// import { useMutation } from 'react-query'

// Sub-components, interfaces, client
// import ExamModal from './ExamModal'
// import LoginContext from '../LoginContext'
// import { examApi } from '../api'
import { ExamOut } from '../generated-client/exam'
import { InstanceInterface } from '../interfaces/components.interface'
import WorkflowFromTemplateModal from './WorkflowFromTemplateModal'

// function ExamInstanceItem({ data: exam, refetchParentData, isSelected }: ComponentProps<ExamOut>) {
function ExamInstanceItem({ data: exam, refetchParentData }: InstanceInterface<ExamOut>) {
  // const [user] = React.useContext(LoginContext)
  // const [examModalOpen, setExamModalOpen] = React.useState(false)
  const [modalOpen, setModalOpen] = React.useState(false)

  // const deleteExam = useMutation(async () => {
  //   await examApi
  //     .examDeleteApiV1ExamExamIdDelete(exam.id, { headers: { Authorization: 'Bearer ' + user?.access_token } })
  //     .then(() => {
  //       refetchParentData()
  //     })
  // })

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

  return (
    <ListItem sx={{ width: '100%', p: 0.5 }}>
      {/* <ListItemDecorator sx={{ align: 'center', justify: 'center' }}>
          <SnippetFolderSharpIcon />
        </ListItemDecorator> */}
        <ListAltIcon fontSize='small' />

        <ListItemContent>
          <Typography level='title-sm'>{exam.name}</Typography>

          <Typography level='body-xs' textColor='text.tertiary'>
            {`Created: ${new Date(exam.datetime_created).toDateString()}`}
          </Typography>
        </ListItemContent>

        {/* <Dropdown>
          <MenuButton variant='plain' sx={{ zIndex: 'snackbar', size: 'xs' }} slots={{ root: IconButton }}>
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
              key='add'
              onClick={() => {
                setModalOpen(true)
              }}
            >
              Add Workflow
            </MenuItem>
          </Menu>
        </Dropdown> */}

        <WorkflowFromTemplateModal
          isOpen={modalOpen}
          setOpen={setModalOpen}
          parentId={exam.id}
          onSubmit={refetchParentData}
        />

        {/* <ExamModal
          data={exam}
          dialogOpen={examModalOpen}
          setDialogOpen={setExamModalOpen}
          handleModalSubmit={(data: Exam) => {
            updateExam.mutate(data)
          }}
        /> */}
    </ListItem>
  )
}

export default ExamInstanceItem