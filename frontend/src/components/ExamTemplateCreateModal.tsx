// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
// PatientTable.tsx is responsible for rendering the patient table view.
import * as React from 'react'

import Typography from '@mui/joy/Typography'
import Button from '@mui/joy/Button'
import ModalDialog from '@mui/joy/ModalDialog'
import ModalClose from '@mui/joy/ModalClose'
import Grid from '@mui/joy/Grid'
import Input from '@mui/joy/Input'
import FormLabel from '@mui/joy/FormLabel'
import Modal from '@mui/joy/Modal'
import Stack from '@mui/joy/Stack'

import { useMutation } from 'react-query'
import { BaseExam, ExamOut } from '../generated-client/exam';
import { examApi } from '../api';
import { ModalComponentProps } from '../interfaces/components.interface'
import LoginContext from '../LoginContext'

const formContent = [
  { key: 'name', label: 'Exam Name', placeholder: 'Knee complaints' },
  { key: 'site', label: 'Site', placeholder: 'Berlin' },
  { key: 'address', label: 'Site Address', placeholder: 'Street name, number' },
  { key: 'creator', label: 'Name of Exam Creater', placeholder: 'Last name, first name' },
  { key: 'status', label: 'Status', placeholder: 'Exam created' },
]

export default function ExamTemplateCreateModal(props: ModalComponentProps<ExamOut>) {

  const [exam, setExam] = React.useState<BaseExam>({patient_id: undefined, name: '', country: 'germany', site: '', address: '', creator: '', status: '', is_template: true, is_frozen: false})
  const [user, setUser] = React.useContext(LoginContext);

  // Post a new exam template and refetch exam table
  const mutation = useMutation(async () => {

    await examApi.createExamTemplateApiV1ExamTemplatesPost(
      exam, {headers: {Authorization: 'Bearer ' + user?.access_token}}
    )
    .then((response) => { props.onSubmit(response.data) })
    .catch((err) => { console.log(err) })
  })

  return (
    <Modal
      open={props.isOpen}
      color='neutral'
      onClose={() => props.setOpen(false)}
      sx={{display: 'flex', justifyContent: 'center', alignItems: 'center'}}
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
