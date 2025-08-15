/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * PatientCreateModal.tsx is responsible for rendering a modal with an interface
 * to create a new patient.
 */
import React from 'react'
import { useMutation } from '@tanstack/react-query'
import dayjs from 'dayjs'

import Button from '@mui/joy/Button'
import FormLabel from '@mui/joy/FormLabel'
import Textarea from '@mui/joy/Textarea'
import Grid from '@mui/joy/Grid'
import Input from '@mui/joy/Input'
import Modal from '@mui/joy/Modal'
import ModalClose from '@mui/joy/ModalClose'
import ModalDialog from '@mui/joy/ModalDialog'
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import Select from '@mui/joy/Select'
import Option from '@mui/joy/Option';
import Stack from '@mui/joy/Stack'
import Typography from '@mui/joy/Typography'

import LoginContext from '../LoginContext'
import { BasePatient, Gender } from '../openapi/generated-client/patient'
import { ModalProps } from '../interfaces/components.interface'
import NotificationContext from '../NotificationContext'
import { patientApi } from '../api'


function PatientForm(props: ModalProps) {
  const [user, ] = React.useContext(LoginContext)
  const [, showNotification] = React.useContext(NotificationContext)

  const [patient, setPatient] = React.useState<BasePatient>({
    first_name: '',     // eslint-disable-line camelcase
    last_name: '',      // eslint-disable-line camelcase
    birth_date: '',     // eslint-disable-line camelcase
    sex: Gender.NotGiven,
    height: 0,
    weight: 0,
    issuer: user ? user.username : '',
    status: 'NEW',
    comment: undefined,
  })

  // Post a new record and refetch records table
  const mutation = useMutation({
    mutationFn: async () => {
      await patientApi
        .createPatientApiV1PatientPost(patient)
        .then((response) => {
          props.onSubmit()
          showNotification({message: 'Created patient ' + response.data.first_name + ' ' + response.data.last_name, type: 'success'})
        }
      )
    }
  })

  return (
    <>
      <Typography id='basic-modal-dialog-title' component='h2' level='inherit' fontSize='1.25em' mb='0.25em'>
        Create New Patient
      </Typography>

      <form
        onSubmit={(event) => {
          event.preventDefault()
          if (patient.birth_date == '') {
            showNotification({message: 'Please select a birth date', type: 'warning'})
          } else {
            mutation.mutate()
            props.setOpen(false)
          }
        }}
      >
        <Stack spacing={5}>
          <Grid container rowSpacing={1.5} columnSpacing={5}>
            
            <Grid md={6}>
              <FormLabel sx={{marginBottom: 1}}>First name</FormLabel>
              <Input
                onChange={(e) => setPatient({ ...patient, first_name: e.target.value })}
                placeholder='patient first name'
                required
              />
            </Grid>

            <Grid md={6}>
              <FormLabel sx={{marginBottom: 1}}>Last name</FormLabel>
              <Input
                onChange={(e) => setPatient({ ...patient, last_name: e.target.value })}
                placeholder='Patient last name'
                required
              />
            </Grid>

            <Grid md={6}>
              <FormLabel sx={{marginBottom: 1}}>Birth date</FormLabel>
              <LocalizationProvider dateAdapter={AdapterDayjs}>
                <DatePicker 
                  sx={{width: '100%'}} 
                  label="MM/DD/YYYY"
                  maxDate={dayjs()}
                  onAccept={(value) => setPatient({ ...patient, birth_date: value ? value.format('YYYY-MM-DD') : '' })}
                />
              </LocalizationProvider>
            </Grid>

            <Grid md={6}>
              <FormLabel sx={{marginBottom: 1}}>Gender</FormLabel>
              <Select
                defaultValue={patient.sex}
                onChange={(_, value) => setPatient({ ...patient, sex: value ? value : Gender.NotGiven})}
                required
              >
                {Object.values(Gender).map((option: Gender) => 
                  <Option key={option} value={option}>{option}</Option>
                )}
              </Select>
            </Grid>

            <Grid md={6}>
              <FormLabel sx={{marginBottom: 1}}>{'Height (cm)'}</FormLabel>
              <Input
                type="number"
                placeholder='Patient height / cm'
                slotProps={{ input: {min: 0, max: 999, step: 5} }}
                onChange={(e) => setPatient({ ...patient, height: parseFloat(e.target.value) })}
              />
            </Grid>

            <Grid md={6}>
              <FormLabel sx={{marginBottom: 1}}>{'Weight (kg)'}</FormLabel>
              <Input
                type="number"
                placeholder='Patient weight / kg'
                slotProps={{ input: {min: 0, max: 999, step: 5} }}
                onChange={(e) => setPatient({ ...patient, weight: parseFloat(e.target.value) })}
              />
            </Grid>

            <Grid md={12}>
              <FormLabel sx={{marginBottom: 1}}>Comment</FormLabel>
              <Textarea 
                placeholder="Add a comment..."
                minRows={3}
                onChange={(e) => setPatient({ ...patient, comment: e.target.value })}
              />
            </Grid>
            
            <Grid md={12} display="flex" justifyContent="flex-end">
              <Button size='sm' type='submit' sx={{ width: 120 }}>
              Save
              </Button>
            </Grid>

          </Grid>
        </Stack>
      </form>
    </>
  )
}


export default function PatientCreateModal(props: ModalProps) {
  return (
    <Modal
      open={props.isOpen}
      color='neutral'
      onClose={() => {
        props.setOpen(false)
      }}
      sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}
    >
      <ModalDialog
        aria-labelledby='basic-modal-dialog-title'
        aria-describedby='basic-modal-dialog-description'
        size='sm'
        sx={{
          width: '70vw',
          borderRadius: 'md',
          p: 5,
        }}
      >
        <ModalClose
          sx={{
            top: '10px',
            right: '10px',
            borderRadius: '50%',
          }}
        />
        <PatientForm {...props} />
      </ModalDialog>
    </Modal>
  )
}