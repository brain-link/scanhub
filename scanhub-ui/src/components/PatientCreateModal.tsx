/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * PatientCreateModal.tsx is responsible for rendering a modal with an interface
 * to create a new patient.
 */
import Button from '@mui/joy/Button'
import FormLabel from '@mui/joy/FormLabel'
import Grid from '@mui/joy/Grid'
import Input from '@mui/joy/Input'
import Modal from '@mui/joy/Modal'
import ModalClose from '@mui/joy/ModalClose'
import ModalDialog from '@mui/joy/ModalDialog'
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import dayjs from 'dayjs'
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import Select from '@mui/joy/Select'
import Option from '@mui/joy/Option';
import Stack from '@mui/joy/Stack'
import Typography from '@mui/joy/Typography'
import * as React from 'react'
import { useMutation } from 'react-query'

import { getPatientApi } from '../api'
import LoginContext from '../LoginContext'
import { BasePatient, Gender } from '../generated-client/patient'
import { ModalProps } from '../interfaces/components.interface'
import NotificationContext from '../NotificationContext'


interface BaseFormEntry {
  key: string,
  label: string
}

interface TextFormEntry extends BaseFormEntry {
  type: 'text'
  required?: boolean
  placeholder?: string
};

interface SelectFormEntry extends BaseFormEntry {
  type: 'select'
  options: string[]
};

interface DateFormEntry extends BaseFormEntry {
  type: 'date'
};

type FormEntry = TextFormEntry | SelectFormEntry | DateFormEntry;


// Patient form items, order is row wise
const createPatientFormContent: FormEntry[] = [
  { type: 'text', key: 'first_name', label: 'First Name', required: true },
  { type: 'text', key: 'last_name', label: 'Last Name', placeholder: '', required: true },
  { type: 'date', key: 'birth_date', label: 'Patient Birth Date' },
  { type: 'select', key: 'sex', label: 'Patient Gender', options: Object.values(Gender) },
  { type: 'text', key: 'comment', label: 'Comment'},
]

export default function PatientCreateModal(props: ModalProps) {
  const [user, ] = React.useContext(LoginContext)
  const [, showNotification] = React.useContext(NotificationContext)
  const patientApi = getPatientApi(user ? user.access_token : '')

  const initialPatient: BasePatient = {
    first_name: '',     // eslint-disable-line camelcase
    last_name: '',      // eslint-disable-line camelcase
    birth_date: '',     // eslint-disable-line camelcase
    sex: Gender.NotGiven,
    issuer: user ? user.username : '',
    status: 'NEW',
    comment: undefined,
  }

  const [patient, setPatient] = React.useState<BasePatient>(initialPatient)

  // Post a new record and refetch records table
  const mutation = useMutation(async () => {
    await patientApi
      .createPatientPost(patient)
      .then((response) => {
        props.onSubmit()
        showNotification({message: 'Created patient ' + response.data.first_name + ' ' + response.data.last_name, type: 'success'})
      })
      .catch((err) => {
        showNotification({message: 'Error at creating patient: ' + err.toString(), type: 'warning'})
      })
  })

  function renderFormEntry(item: FormEntry, index: number) {
    if (item.type == 'date') {
      return (
        <Grid key={index} md={6}>
          <FormLabel sx={{marginBottom: 1}}>{item.label}</FormLabel>
          <LocalizationProvider dateAdapter={AdapterDayjs}>
            <DatePicker 
              sx={{width: '100%'}} 
              label="MM/DD/YYYY"
              maxDate={dayjs()}
              onAccept={(value) => setPatient({ ...patient, [item.key]: value?.format('YYYY-MM-DD') })}
            />
          </LocalizationProvider>
        </Grid>
      )    
    }
    else if (item.type == 'text') {
      return (
        <Grid key={index} md={6}>
          <FormLabel sx={{marginBottom: 1}}>{item.label}</FormLabel>
          <Input
            name={item.key}
            onChange={(e) => setPatient({ ...patient, [e.target.name]: e.target.value })}
            placeholder={item.placeholder}
            required={item.required}
          />
        </Grid>
      )
    }
    else if (item.type == 'select') {
      return (
        <Grid key={index} md={6}>
          <FormLabel sx={{marginBottom: 1}}>{item.label}</FormLabel>
          <Select 
            onChange={(event, value) => setPatient({ ...patient, [item.key]: value })}
            required
          >
            {item.options.map((option) => 
              <Option key={option} value={option}>{option}</Option>
            )}
          </Select>
        </Grid>
      )
    }
  }

  return (
    <Modal
      open={props.isOpen}
      color='neutral'
      onClose={() => {
        props.setOpen(false)
        setPatient(initialPatient)
      }}
      sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}
    >
      <ModalDialog
        aria-labelledby='basic-modal-dialog-title'
        aria-describedby='basic-modal-dialog-description'
        size='sm'
        sx={{
          width: '50vw',
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
              setPatient(initialPatient)
            }
          }}
        >
          <Stack spacing={5}>
            <Grid container rowSpacing={1.5} columnSpacing={5}>
              {createPatientFormContent.map((item, index) => renderFormEntry(item, index))}
            </Grid>
            <Button size='sm' type='submit' sx={{ maxWidth: 100 }}>
              Submit
            </Button>
          </Stack>
        </form>
      </ModalDialog>
    </Modal>
  )
}