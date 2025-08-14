/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * TaskModal.tsx is responsible for rendering a modal with an interface to create a new task or to modify an existing task.
 */

import Button from '@mui/joy/Button'
import FormLabel from '@mui/joy/FormLabel'
import Input from '@mui/joy/Input'

import Modal from '@mui/joy/Modal'
import Grid from '@mui/joy/Grid'
import ModalClose from '@mui/joy/ModalClose'
import ModalDialog from '@mui/joy/ModalDialog'
import Typography from '@mui/joy/Typography'
import React from 'react'
import { useMutation } from '@tanstack/react-query'

import { patientApi } from '../api'
import { BasePatient, PatientOut } from '../openapi/generated-client/patient'

import { ModalProps } from '../interfaces/components.interface'
import NotificationContext from '../NotificationContext'


function ConfirmAcquisitionLimitsForm(props: ModalProps & { item: PatientOut })
{

  const [, showNotification] = React.useContext(NotificationContext)
  const [patient, setPatient] = React.useState<BasePatient>({...props.item, status: 'UPDATED'})

  const mutation = useMutation({
    mutationFn: async () => {
      await patientApi.updatePatientApiV1PatientPatientIdPut(props.item.id, patient)
      .then(() => {
        showNotification({message: 'Updated patient acquisition limits.', type: 'success'})
        props.onSubmit()
      })
      .catch((err) => {
        let errorMessage = null
        if (err?.response?.data?.detail?.[0]?.msg) {
          errorMessage = 'Could not update patient. Detail: ' + err.response.data.detail[0].msg
        }
        else if (err?.response?.data?.detail) {
          errorMessage = 'Could not update patient. Detail: ' + err.response.data.detail
        } else {
          errorMessage = 'Could not update patient.'
        }
        showNotification({message: errorMessage, type: 'warning'})
      })
      // don't catch error here to make sure it propagates to onRowUpdate
    }
  })

  return (
    <>
      <Typography id='basic-modal-dialog-title' component='h2' level='inherit' fontSize='1.25em' mb='0.25em'>
        Confirm Acquisition Limits
      </Typography>

      <Grid container rowSpacing={1.5} columnSpacing={5}>

        <Grid md={6}>
          <FormLabel sx={{ mb: 1 }}>Patient height / cm</FormLabel>
          <Input
            type="number"
            defaultValue={patient.height}
            slotProps={{ input: {min: 0, max: 999, step: 5} }}
            onChange={(e) => setPatient({ ...patient, height: parseFloat(e.target.value) })}
          />
        </Grid>
        
        <Grid md={6}>
          <FormLabel sx={{ mb: 1 }}>Patient weight / kg</FormLabel>
          <Input
            type="number"
            defaultValue={patient.weight}
            slotProps={{ input: {min: 0, max: 999, step: 5} }}
            onChange={(e) => setPatient({ ...patient, weight: parseFloat(e.target.value) })}
          />
        </Grid>

        <Grid md={12} display="flex" justifyContent="flex-end">
          <Button
            size='sm'
            sx={{ maxWidth: 120 }}
            onClick={(event) => {
              event.preventDefault()
              mutation.mutate()
              props.onSubmit()
              props.setOpen(false)
            }}
          >
            Confirm
          </Button>
        </Grid>
      </Grid>
    </>
  )
}


export default function ConfirmAcquisitionLimitsModal(props: ModalProps & { item: PatientOut }) {
  return (
    <Modal
      open={props.isOpen}   // open=False unmounts children, resetting the state of the form
      color='neutral'
      onClose={() => props.setOpen(false)}
      sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}
    >
      <ModalDialog
        aria-labelledby='basic-modal-dialog-title'
        aria-describedby='basic-modal-dialog-description'
        sx={{ width: '70vw', borderRadius: 'md', p: 5 }}
      >
        <ModalClose
          sx={{
            top: '10px',
            right: '10px',
            borderRadius: '50%',
            bgcolor: 'background.body',
          }}
        />
        <ConfirmAcquisitionLimitsForm {...props} />
      </ModalDialog>
    </Modal>
  )
}