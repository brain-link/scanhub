/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * TaskFromTemplateModal.tsx is responsible for rendering a
 * task template selection interface to generate a new task instance.
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
import { taskApi } from '../api'
import { TaskOut } from '../generated-client/exam'
import { CreateInstanceModalInterface } from '../interfaces/components.interface'
import TaskTemplateItem from './TaskTemplateItem'

export default function TaskFromTemplateModal(props: CreateInstanceModalInterface) {
  const [user] = useContext(LoginContext)

  const { data: tasks } = useQuery<TaskOut[]>({
    queryKey: ['exams'],
    queryFn: async () => {
      return await taskApi
        .getAllTaskTemplatesApiV1ExamTaskTemplatesAllGet({ headers: { Authorization: 'Bearer ' + user?.access_token } })
        .then((result) => {
          return result.data
        })
    },
  })

  const mutation = useMutation(async (id: string) => {
    await taskApi
      .createTaskFromTemplateApiV1ExamTaskPost(String(props.parentId), id, {
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
            {tasks &&
              tasks.map((task, idx) => (
                <ListItemButton
                  key={idx}
                  onClick={() => {
                    mutation.mutate(task.id)
                    props.setOpen(false)
                  }}
                >
                  <TaskTemplateItem item={task} onClicked={() => {}} onDeleted={() => {}} />
                </ListItemButton>
              ))}
          </List>
        </ModalDialog>
      </Modal>
    </>
  )
}
