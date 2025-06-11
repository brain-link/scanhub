/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * ExamFromTemplateModal.tsx is responsible for rendering a
 * exam template selection interface to generate a new exam.
 */
import * as React from 'react'
import { useQuery } from '@tanstack/react-query'
import Modal from '@mui/joy/Modal'
import ModalClose from '@mui/joy/ModalClose'
import ModalDialog from '@mui/joy/ModalDialog'
import DialogTitle from '@mui/material/DialogTitle'
import Stack from '@mui/joy/Stack'

import { examApi } from '../api'
import { ExamOut } from '../generated-client/exam'
import { ITEM_UNSELECTED, ModalPropsCreate } from '../interfaces/components.interface'
import ExamItem from './ExamItem'
import ExamModal from './ExamModal'


export default function ExamFromTemplateModal(props: ModalPropsCreate) {

  const [examForModification, setExamForModification] = React.useState<ExamOut | undefined>(undefined);

  const { data: exams } = useQuery<ExamOut[]>({
    queryKey: ['exams'],
    queryFn: async () => {
      return await examApi
        .getAllExamTemplatesApiV1ExamTemplatesAllGet()
        .then((result) => {
          return result.data
        })
    },
  })

  function returnExamFromTemplateModal() {
    return <Modal
      open={props.isOpen}
      onClose={() => {
        props.setOpen(false)
      }}
    >
      <ModalDialog sx={{ width: '50vw', p: 5 }}>
        <ModalClose />
        <DialogTitle>Add Exam from Template</DialogTitle>
        <Stack
          sx={{
            overflow: 'scroll',
            mx: 'calc(-1 * var(--ModalDialog-padding))',
            px: 'var(--ModalDialog-padding)',
          }}
        >
          {exams &&
            exams.map((exam, idx) => (
              <ExamItem
                key={idx}
                item={exam}
                onClick={() => {
                  setExamForModification({ ...exam, 'patient_id': props.parentId, 'is_template': props.createTemplate })
                }}
                selection={ITEM_UNSELECTED} 
              />
            ))}
        </Stack>
      </ModalDialog>
    </Modal>
  }

  return (
    examForModification ? 
      <ExamModal
        item={examForModification}
        isOpen={true}
        setOpen={(status) => {
          if (status == false) {
            setExamForModification(undefined)  // reset state
          }
          props.setOpen(status)
        }}
        onSubmit={props.onSubmit}
        modalType={'createModifyFromTemplate'}
      />
    :
      returnExamFromTemplateModal()
  )
}
