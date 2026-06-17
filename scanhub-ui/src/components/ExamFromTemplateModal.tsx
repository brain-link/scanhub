/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * ExamFromTemplateModal.tsx is responsible for rendering a
 * exam template selection interface to generate a new exam.
 */
import React from 'react'
import { useQuery } from '@tanstack/react-query'
import Modal from '@mui/joy/Modal'
import ModalClose from '@mui/joy/ModalClose'
import ModalDialog from '@mui/joy/ModalDialog'
import DialogTitle from '@mui/joy/DialogTitle';
import Stack from '@mui/joy/Stack'

import { protocolApi } from '../api'
import { ProtocolOut } from '../openapi/generated-client/protocol'
import { ITEM_UNSELECTED, ModalPropsCreate } from '../interfaces/components.interface'
import ExamItem from './ExamItem'
import ExamModal from './ExamModal'


export default function ExamFromTemplateModal(props: ModalPropsCreate) {

  const [selectedProtocol, setSelectedProtocol] = React.useState<ProtocolOut | undefined>(undefined);

  const { data: protocols } = useQuery<ProtocolOut[]>({
    queryKey: ['exams'],
    queryFn: async () => {
      return await protocolApi
        .getAllProtocolTemplates()
        .then((result) => {
          return result.data
        })
    },
  })

  function returnProtocolFromTemplateModal() {
    return <Modal
      open={props.isOpen}
      onClose={() => {
        props.setOpen(false)
      }}
    >
      <ModalDialog sx={{ width: '50vw', p: 5 }}>
        <ModalClose />
        <DialogTitle>Add Protocol from Template</DialogTitle>
        <Stack
          sx={{
            overflow: 'scroll',
            mx: 'calc(-1 * var(--ModalDialog-padding))',
            px: 'var(--ModalDialog-padding)',
          }}
        >
          {protocols &&
            protocols.map((exam, idx) => (
              <ExamItem
                key={idx}
                item={exam}
                onClick={() => {
                  setSelectedProtocol({ ...exam, 'patient_id': props.parentId, 'is_template': props.createTemplate })
                }}
                selection={ITEM_UNSELECTED} 
              />
            ))}
        </Stack>
      </ModalDialog>
    </Modal>
  }

  return (
    selectedProtocol ? 
      <ExamModal
        item={selectedProtocol}
        isOpen={true}
        setOpen={(status) => {
          if (status == false) {
            setSelectedProtocol(undefined)  // reset state
          }
          props.setOpen(status)
        }}
        onSubmit={props.onSubmit}
        modalType={'createModifyFromTemplate'}
      />
    :
      returnProtocolFromTemplateModal()
  )
}
