/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * ExamModifyModal.tsx is responsible for rendering a modal with an interface
 * to modify an existing exam.
 */
import Button from '@mui/joy/Button'
import FormLabel from '@mui/joy/FormLabel'
import Grid from '@mui/joy/Grid'
import Input from '@mui/joy/Input'
import Modal from '@mui/joy/Modal'
import ModalClose from '@mui/joy/ModalClose'
import ModalDialog from '@mui/joy/ModalDialog'
import Stack from '@mui/joy/Stack'
import Typography from '@mui/joy/Typography'
import * as React from 'react'
import { useMutation } from 'react-query'

import LoginContext from '../LoginContext'
import { examApi } from '../api'
import { BaseExam, ExamOut } from '../generated-client/exam'
import { ModalPropsModify } from '../interfaces/components.interface'
import NotificationContext from '../NotificationContext'


const formContent: {key: keyof BaseExam, label: string}[] = [
  { key: 'name', label: 'Exam Name' },
  { key: 'country', label: 'Country' },
  { key: 'site', label: 'Site' },
  { key: 'address', label: 'Site Address' },
]

export default function ExamCreateModal(props: ModalPropsModify<ExamOut>) {
  const [user] = React.useContext(LoginContext)
  const [, showNotification] = React.useContext(NotificationContext)
  
  const [exam, setExam] = React.useState<BaseExam>({
    patient_id: props.item.patient_id,          // eslint-disable-line camelcase
    name: props.item.name,
    country: props.item.country,
    site: props.item.site,
    address: props.item.address,
    creator: props.item.creator,
    status: 'UPDATED',
    is_template: props.item.is_template,        // eslint-disable-line camelcase
    is_frozen: props.item.is_frozen,            // eslint-disable-line camelcase
  })


  const mutation = useMutation(async () => {
    await examApi
    .updateExamApiV1ExamExamIdPut(props.item.id, 
                                  exam, 
                                  { headers: { Authorization: 'Bearer ' + user?.access_token } })
    .then(() => {
      props.onSubmit()
    })
    .catch(() => {
      showNotification({message: 'Could not update exam', type: 'warning'})
    })
  })

  
  return (
    <Modal
      open={props.isOpen}
      color='neutral'
      onClose={() => props.setOpen(false)}
      sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}
    >
      <ModalDialog
        aria-labelledby='basic-modal-dialog-title'
        aria-describedby='basic-modal-dialog-description'
        sx={{ width: '50vw', borderRadius: 'md', p: 5 }}
      >
        <ModalClose
          sx={{
            top: '10px',
            right: '10px',
            borderRadius: '50%',
            bgcolor: 'background.body',
          }}
        />

        <Typography id='basic-modal-dialog-title' component='h2' level='inherit' fontSize='1.25em' mb='0.25em'>
          Create New Exam Template
        </Typography>

        <Stack spacing={1}>
          <Grid container rowSpacing={1.5} columnSpacing={5}>
            {formContent.map((item, index) => (
              <Grid key={index} md={6}>
                <FormLabel>{item.label}</FormLabel>
                <Input
                  name={item.key}
                  onChange={(e) => setExam({ ...exam, [e.target.name]: e.target.value })}
                  value={exam[item.key]?.toString()}
                  required
                />
              </Grid>
            ))}
          </Grid>

          <Button
            size='sm'
            sx={{ maxWidth: 120 }}
            onClick={(event) => {
              event.preventDefault()
              mutation.mutate()
              props.setOpen(false)
            }}
          >
            Save
          </Button>
        </Stack>
      </ModalDialog>
    </Modal>
  )
}
