/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * TaskFromTemplateModal.tsx is responsible for rendering a
 * task template selection interface to generate a new task.
 */
import * as React from 'react'
import { useMutation } from 'react-query'
import { useQuery } from 'react-query'
import Modal from '@mui/joy/Modal'
import ModalClose from '@mui/joy/ModalClose'
import ModalDialog from '@mui/joy/ModalDialog'
import DialogTitle from '@mui/material/DialogTitle'
import Stack from '@mui/joy/Stack'

import { taskApi } from '../api'
import { TaskOut } from '../generated-client/exam'
import { ITEM_UNSELECTED, ModalPropsCreate } from '../interfaces/components.interface'
import TaskTemplateItem from './TaskItem'

export default function TaskFromTemplateModal(props: ModalPropsCreate) {
  const { data: tasks } = useQuery<TaskOut[]>({
    queryKey: ['allTaskTemplates'],
    queryFn: async () => {
      return await taskApi
        .getAllTaskTemplatesApiV1ExamTaskTemplatesAllGet()
        .then((result) => {
          return result.data
        })
    },
  })

  const mutation = useMutation(async (id: string) => {
    await taskApi
      .createTaskFromTemplateApiV1ExamTaskPost(String(props.parentId), id, props.createTemplate)
      .then(() => {
        props.onSubmit()
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
          <DialogTitle>Add Task from Template</DialogTitle>
          <Stack
            sx={{
              overflow: 'scroll',
              mx: 'calc(-1 * var(--ModalDialog-padding))',
              px: 'var(--ModalDialog-padding)',
            }}
          >
            {tasks &&
              tasks.map((task, idx) => (
                <TaskTemplateItem 
                  key={idx} 
                  item={task} 
                  refetchParentData={() => {}} 
                  onClick={() => {
                    mutation.mutate(task.id)
                    props.setOpen(false)
                  }} 
                  selection={ITEM_UNSELECTED} 
                />
              ))}
          </Stack>
        </ModalDialog>
      </Modal>
    </>
  )
}
