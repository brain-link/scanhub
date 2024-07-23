/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * ExamTemplateCreateModal.tsx is responsible for rendering a modal with an interface
 * to create a new exam template.
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
import { ModalComponentProps } from '../interfaces/components.interface'

const formContent = [
  { key: 'name', label: 'Exam Name', placeholder: 'Knee complaints' },
  { key: 'site', label: 'Site', placeholder: 'Berlin' },
  { key: 'address', label: 'Site Address', placeholder: 'Street name, number' },
  { key: 'status', label: 'Status', placeholder: 'Exam created' },
]

export default function ExamModal(props: ModalComponentProps<ExamOut>) {
  const [user] = React.useContext(LoginContext)

  const [exam, setExam] = React.useState<BaseExam>({
    patient_id: undefined,    // eslint-disable-line camelcase
    name: '',
    country: 'germany',
    site: '',
    address: '',
    creator: user?.username != undefined ? user.username : '',
    status: '',
    is_template: true,        // eslint-disable-line camelcase
    is_frozen: false,         // eslint-disable-line camelcase
  })

  // Post a new exam template and refetch exam table
  const mutation = useMutation(async () => {
    await examApi
      .createExamApiV1ExamNewPost(exam, { headers: { Authorization: 'Bearer ' + user?.access_token } })
      .then((response) => {
        props.onSubmit(response.data)
      })
      .catch((err) => {
        console.log(err)
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
                  placeholder={item.placeholder}
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
