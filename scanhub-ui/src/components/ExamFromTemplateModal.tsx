/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * ExamFromTemplateModal.tsx is responsible for rendering a
 * exam template selection interface to generate a new exam.
 */
import List from '@mui/joy/List'
import ListItemButton from '@mui/joy/ListItemButton'
import Modal from '@mui/joy/Modal'
import ModalClose from '@mui/joy/ModalClose'
import ModalDialog from '@mui/joy/ModalDialog'
import DialogTitle from '@mui/material/DialogTitle'
import * as React from 'react'
import { useContext } from 'react'
import { useMutation } from 'react-query'
import { useQuery } from 'react-query'

import LoginContext from '../LoginContext'
import { examApi } from '../api'
import { ExamOut } from '../generated-client/exam'
import { ModalPropsCreate } from '../interfaces/components.interface'
import ExamItem from './ExamItem'

export default function ExamFromTemplateModal(props: ModalPropsCreate) {
  const [user] = useContext(LoginContext)

  const { data: exams } = useQuery<ExamOut[]>({
    queryKey: ['exams'],
    queryFn: async () => {
      return await examApi
        .getAllExamTemplatesApiV1ExamTemplatesAllGet({ headers: { Authorization: 'Bearer ' + user?.access_token } })
        .then((result) => {
          return result.data
        })
    },
  })

  const mutation = useMutation(async (id: string) => {
    await examApi
      .createExamFromTemplateApiV1ExamPost(Number(props.parentId), id, props.createTemplate, {
        headers: { Authorization: 'Bearer ' + user?.access_token },
      })
      .then(() => {
        props.onSubmit()
      })
      .catch((err) => {
        console.log(err)
      })
  })

  return (
    <>
      <Modal
        open={props.isOpen}
        onClose={() => {
          props.setOpen(false)
        }}
      >
        <ModalDialog sx={{ width: '50vw', p: 5 }}>
          <ModalClose />
          <DialogTitle>Exam Templates</DialogTitle>
          <List
            sx={{
              overflow: 'scroll',
              mx: 'calc(-1 * var(--ModalDialog-padding))',
              px: 'var(--ModalDialog-padding)',
            }}
          >
            {exams &&
              exams.map((exam, idx) => (
                <ListItemButton
                  key={idx}
                  onClick={() => {
                    mutation.mutate(exam.id)
                    props.setOpen(false)
                  }}
                >
                  <ExamItem exam={exam} />
                </ListItemButton>
              ))}
          </List>
        </ModalDialog>
      </Modal>
    </>
  )
}
