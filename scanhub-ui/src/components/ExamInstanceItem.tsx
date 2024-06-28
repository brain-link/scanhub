/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * ExamInstanceItem.tsx is responsible for rendering a single exam instance item
 * in the exam instance list of a patient.
 */
import ListAltIcon from '@mui/icons-material/ListAlt'
// Mui joy components
import ListItem from '@mui/joy/ListItem'
// import ListItemDecorator from '@mui/joy/ListItemDecorator'
import ListItemContent from '@mui/joy/ListItemContent'
import Typography from '@mui/joy/Typography'
import * as React from 'react'

// Sub-components, interfaces, client
import { ExamOut } from '../generated-client/exam'
import { InstanceInterface } from '../interfaces/components.interface'
import WorkflowFromTemplateModal from './WorkflowFromTemplateModal'

// function ExamInstanceItem({ data: exam, refetchParentData, isSelected }: ComponentProps<ExamOut>) {
function ExamInstanceItem({ data: exam, refetchParentData }: InstanceInterface<ExamOut>) {
  const [modalOpen, setModalOpen] = React.useState(false)

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

        <WorkflowFromTemplateModal
          isOpen={modalOpen}
          setOpen={setModalOpen}
          parentId={exam.id}
          onSubmit={refetchParentData}
        />
    </ListItem>
  )
}

export default ExamInstanceItem
