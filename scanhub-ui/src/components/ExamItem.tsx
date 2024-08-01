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
import { RefetchableItemInterface, SelectableItemInterface } from '../interfaces/components.interface'
import Box from '@mui/joy/Box'
import { examApi } from '../api'
import WorkflowFromTemplateModal from './WorkflowFromTemplateModal'
import ExamInfo from './ExamInfo'
import WorkflowCreateModal from './WorkflowCreateModal'
import NotificationContext from '../NotificationContext'
import ExamModifyModal from './ExamModifyModal'
import Button from '@mui/joy/Button'


export default function ExamItem({ item: exam, selection, onClick }: SelectableItemInterface<ExamOut>) {

  return (
    <Tooltip
      placement='right'
      variant='outlined'
      describeChild={false}
      arrow
      title={<ExamInfo exam={exam} />}
    >
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
      </Button>
    </Tooltip>
  )
}


export function ExamMenu({ item: exam, refetchParentData }: RefetchableItemInterface<ExamOut>) {

  const [workflowFromTemplateModalOpen, setWorkflowFromTemplateModalOpen] = React.useState(false)
  const [workflowCreateNewModalOpen, setWorkflowCreateNewModalOpen] = React.useState(false)
  const [examModalOpen, setExamModalOpen] = React.useState(false)
  const [, showNotification] = React.useContext(NotificationContext)

  const deleteExam = useMutation(async () => {
    await examApi
      .examDeleteApiV1ExamExamIdDelete(exam.id)
      .then(() => {
        refetchParentData()
      })
      .catch(() => {
        showNotification({message: 'Could not delete exam', type: 'warning'})
      })
  })

  return (
    <>
      <Dropdown>
        <MenuButton variant='plain' sx={{ size: 'xs' }} slots={{ root: IconButton }}>
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

      <ExamModifyModal
        item={exam}
        isOpen={examModalOpen}
        setOpen={setExamModalOpen}
        onSubmit={refetchParentData}
      />

      <WorkflowFromTemplateModal
        isOpen={workflowFromTemplateModalOpen}
        setOpen={setWorkflowFromTemplateModalOpen}
        parentId={exam.id}
        onSubmit={refetchParentData}
        createTemplate={exam.is_template}
      />
      {
        exam.is_template ?
          <WorkflowCreateModal
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
