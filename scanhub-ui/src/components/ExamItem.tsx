/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * ExamItem.tsx is responsible for rendering a single exam item.
 */
import Typography from '@mui/joy/Typography'
import React from 'react'
import { useMutation } from '@tanstack/react-query'
import MoreHorizIcon from '@mui/icons-material/MoreHoriz'
import FolderIcon from '@mui/icons-material/Folder';
import Dropdown from '@mui/joy/Dropdown'
import Menu from '@mui/joy/Menu'
import MenuButton from '@mui/joy/MenuButton'
import IconButton from '@mui/joy/IconButton'
import MenuItem from '@mui/joy/MenuItem'

// Sub-components, interfaces, client
import { ExamOut } from '../openapi/generated-client/exam'
import { RefetchableItemInterface, SelectableItemInterface } from '../interfaces/components.interface'
import Box from '@mui/joy/Box'
import { examApi } from '../api'
import WorkflowFromTemplateModal from './WorkflowFromTemplateModal'
import WorkflowModal from './WorkflowModal'
import ExamModal from './ExamModal'
import Button from '@mui/joy/Button'


export default function ExamItem({ item: exam, selection, onClick }: SelectableItemInterface<ExamOut>) {

  return (
    <Button
      sx={{ 
        width: '100%', 
        p: 0.5, 
        display: 'flex',
        justifyContent: 'flex-start'
      }}
      variant={(selection.type == 'exam' && selection.itemId == exam.id) ? 'outlined' : 'plain'}
      onClick={onClick}
    >
      <FolderIcon fontSize='small' />
      <Box 
        sx={{
          marginLeft: 0.5,
          p: 0.5, 
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'start',
        }}
      >
        <Typography level='body-xs' textColor='text.tertiary'>
          EXAM
        </Typography>

        <Typography level='title-sm'>
          {exam.name}
        </Typography>

        <Typography level='body-xs' textColor='text.tertiary'>
          {`Created: ${new Date(exam.datetime_created).toDateString()}`}
        </Typography>
      </Box>
    </Button>
  )
}


export function ExamMenu({ item: exam, refetchParentData }: RefetchableItemInterface<ExamOut>) {

  const [workflowFromTemplateModalOpen, setWorkflowFromTemplateModalOpen] = React.useState(false)
  const [workflowCreateNewModalOpen, setWorkflowCreateNewModalOpen] = React.useState(false)
  const [examModalOpen, setExamModalOpen] = React.useState(false)

  const deleteExam = useMutation({
    mutationFn: async () => {
      await examApi
        .examDeleteApiV1ExamExamIdDelete(exam.id)
        .then(() => {
          refetchParentData()
        })
    }
  })

  return (
    <>
      <Dropdown>
        <MenuButton slotProps={{ root: { size: 'sm', variant: 'plain' } }} sx={{ aspectRatio: '1 / 1', minWidth: 0, p: 0.5 }} slots={{ root: IconButton }}>
          <MoreHorizIcon fontSize='small' />
        </MenuButton>
        <Menu id='context-menu' variant='plain' sx={{ zIndex: 'snackbar' }}>
          <MenuItem key='edit' onClick={() => setExamModalOpen(true)}>
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

      <ExamModal
        item={exam}
        isOpen={examModalOpen}
        setOpen={setExamModalOpen}
        onSubmit={refetchParentData}
        modalType='modify'
      />

      <WorkflowFromTemplateModal
        isOpen={workflowFromTemplateModalOpen}
        setOpen={setWorkflowFromTemplateModalOpen}
        parentId={exam.id}
        onSubmit={refetchParentData}
        createTemplate={exam.is_template}
        modalType={'create'}
      />
      {
        exam.is_template ?
          <WorkflowModal
            isOpen={workflowCreateNewModalOpen}
            setOpen={setWorkflowCreateNewModalOpen}
            parentId={exam.id}
            onSubmit={refetchParentData}
            createTemplate={exam.is_template}
            modalType={'create'}
          />
        : undefined
      }

    </>
  )
}
