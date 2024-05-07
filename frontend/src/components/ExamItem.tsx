// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
// ExamItem.tsx is responsible for rendering a single exam item in the exam list of the patient view.
import MoreHorizIcon from '@mui/icons-material/MoreHoriz'
import SnippetFolderSharpIcon from '@mui/icons-material/SnippetFolderSharp'
// Mui joy components
import Box from '@mui/joy/Box'
import IconButton from '@mui/joy/IconButton'
import ListItem from '@mui/joy/ListItem'
import ListItemButton from '@mui/joy/ListItemButton'
import ListItemDecorator from '@mui/joy/ListItemDecorator'
import Menu from '@mui/joy/Menu'
import MenuItem from '@mui/joy/MenuItem'
import Typography from '@mui/joy/Typography'
import * as React from 'react'
import { useMutation } from 'react-query'
import { Link as RouterLink } from 'react-router-dom'
import { useParams } from 'react-router-dom'
import { useNavigate } from 'react-router-dom'

import client from '../client/exam-tree-queries'
import ExamModal from '../components/ExamModal'
import { ComponentProps } from '../interfaces/components.interface'
// Interfaces and api service
// import { Exam } from '../interfaces/data.interface'
import { ExamOut } from '../generated-client/exam'
import { examApi } from '../api'


function ExamItem({ data: exam, refetchParentData, isSelected }: ComponentProps<ExamOut>) {
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
    await examApi.examDeleteApiV1ExamExamIdDelete(exam.id, {headers: {Authorization: "Bearer Bitte"}}).then(() => {
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
    <ListItem>
      <ListItemButton
        id='exam-item'
        component={RouterLink}
        to={`/${params.patientId}/${exam.id}`}
        relative='path'
        selected={isSelected}
        variant={isSelected || exam.id === contextOpen ? 'soft' : 'plain'}
      >
        <ListItemDecorator sx={{ align: 'center', justify: 'center' }}>
          <SnippetFolderSharpIcon />
        </ListItemDecorator>

        <Box sx={{ display: 'flex', flexDirection: 'column', width: '100%' }}>
          <Box sx={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-between' }}>
            <Typography>{exam.name}</Typography>
            <IconButton
              variant='plain'
              sx={{ '--IconButton-size': '25px' }}
              onClick={(e) => handleContextOpen(e, exam.id)}
            >
              <MoreHorizIcon />
            </IconButton>
          </Box>

          <Typography level='body-sm' textColor='text.tertiary'>{`Issuer: ${exam.creator}, ${exam.site}`}</Typography>
          <Typography level='body-sm' textColor='text.tertiary'>
            {exam.status}
          </Typography>
          <Typography level='body-sm' textColor='text.tertiary'>{`Created: ${new Date(
            exam.datetime_created,
          ).toDateString()}`}</Typography>
          <Typography level='body-sm' textColor='text.tertiary'>{`Updated: ${
            exam.datetime_updated ? new Date(exam.datetime_updated).toDateString() : '-'
          }`}</Typography>
        </Box>

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
      </ListItemButton>
    </ListItem>
  )
}

export default ExamItem
