/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * TaskModal.tsx is responsible for rendering a modal with an interface to create a new task or to modify an existing task.
 */

import Button from '@mui/joy/Button'
import FormLabel from '@mui/joy/FormLabel'
import Input from '@mui/joy/Input'

import Stack from '@mui/joy/Stack'
import Textarea from '@mui/joy/Textarea'
import Typography from '@mui/joy/Typography'
import * as React from 'react'
import { useMutation } from '@tanstack/react-query'

import { patientApi } from '../api'
import { AcquisitionLimits } from '../generated-client/exam'
import { PatientOut } from '../generated-client/patient'

import { ModalPropsModify } from '../interfaces/components.interface'
import NotificationContext from '../NotificationContext'


function AcquisitionLimitForm(props: ModalPropsModify<PatientOut>)
{

  const [, showNotification] = React.useContext(NotificationContext)
  const [limits, setLimits] = React.useState<AcquisitionLimits>(props.item.acquisition_limits as AcquisitionLimits);

  const mutation = useMutation<unknown, unknown, PatientOut>({
    mutationFn: async () => {
      await patientApi.updatePatientApiV1PatientPatientIdPut(props.item.id, {acquisition_limits: limits})
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

      <Stack direction='column' spacing={4} useFlexGap sx={{ flexWrap: 'wrap' }}>

        <Stack spacing={1}>
          <FormLabel>Height</FormLabel>
          <Input
            name={'patient_height'}
            onChange={(e) => setLimits({ ...limits, [e.target.name]: e.target.value })}
            value={limits.patient_height}
          />
        </Stack>
        
        <Stack spacing={1}>
          <FormLabel>Weight</FormLabel>
          <Textarea
            minRows={2}
            name={'patient_weight'}
            onChange={(e) => setLimits({ ...limits, [e.target.name]: e.target.value })}
            defaultValue={limits.patient_weight}
          />
        </Stack>

        <Button
          size='sm'
          sx={{ maxWidth: 120 }}
          onClick={(event) => {
            event.preventDefault()
            mutation.mutate()
            props.setOpen(false)
            }
          }
        >
          Confirm
        </Button>
      </Stack>
    </>
  )
}
