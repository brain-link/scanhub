// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
// ExamItem.tsx is responsible for rendering a single exam item in the exam list of the patient view.

import * as React from 'react'
import { useMutation } from 'react-query'
import { useParams } from 'react-router-dom'
import { useNavigate } from 'react-router-dom'

// Mui joy components
import IconButton from '@mui/joy/IconButton'
import ListItem from '@mui/joy/ListItem'
import ListItemDecorator from '@mui/joy/ListItemDecorator'
import ListItemContent from '@mui/joy/ListItemContent'
import Menu from '@mui/joy/Menu'
import MenuItem from '@mui/joy/MenuItem'
import Typography from '@mui/joy/Typography'

// Icons
import MoreHorizIcon from '@mui/icons-material/MoreHoriz'
import SnippetFolderSharpIcon from '@mui/icons-material/SnippetFolderSharp'

// Sub-components, interfaces, client
import ExamModal from './ExamModal'
import { ComponentProps } from '../interfaces/components.interface'
import { ExamOut } from '../generated-client/exam'
import { examApi } from '../api'


function ExamInstanceItem({ data: exam, refetchParentData, isSelected }: ComponentProps<ExamOut>) {
  const params = useParams()
  const navigate = useNavigate()

  // Context: Delete and edit options, anchor for context location
  const [contextOpen, setContextOpen] = React.useState<string | null>(null)
  const [anchorEl, setAnchorEl] = React.useState<HTMLElement | null>(null)
  const [examModalOpen, setExamModalOpen] = React.useState(false)

  const handleContextClose = () => {
    setAnchorEl(null)
    setContextOpen(null)
  }

  const handleContextOpen = (e: React.MouseEvent<HTMLAnchorElement, MouseEvent>, examId: string) => {
    e.preventDefault()
    setAnchorEl(e.currentTarget)
    setContextOpen(examId)
  }

  const deleteExam = useMutation(async () => {
    await examApi.examDeleteApiV1ExamExamIdDelete(exam.id).then(() => {
      if (String(params.examId) === exam.id) {
        // Reset router path if this exam id is in the path
        navigate(`/${params.patientId}`)
      }
      refetchParentData()
    })
  })

  // const updateExam = useMutation(async (data: Exam) => {
  //   console.log('Updating exam data... ', data)
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

    <ListItem sx={{width: "100%"}}>

      <ListItemDecorator sx={{ align: 'center', justify: 'center' }}>
        <SnippetFolderSharpIcon />
      </ListItemDecorator>

      <ListItemContent>
        
        <Typography>{exam.name}</Typography>

        <Typography level='body-sm' textColor='text.tertiary'>
          {
            `Created: ${new Date(exam.datetime_created).toDateString()}`
          }
        </Typography>

      </ListItemContent>

      <IconButton
        variant='plain'
        sx={{ '--IconButton-size': '25px' }}
        onClick={(e) => handleContextOpen(e, exam.id)}
      >
        <MoreHorizIcon />
      </IconButton>

      <Menu
        id='context-menu'
        variant='plain'
        anchorEl={anchorEl}
        open={exam.id === contextOpen}
        onClose={() => handleContextClose()}
        sx={{ zIndex: 'snackbar' }}
      >
        <MenuItem
          key='edit'
          onClick={() => {
            // setExamModalOpen(true)
          }}
        >
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
      </Menu>

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
