/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * ExamModal.tsx is responsible for rendering a modal with an interface
 * to create a new exam or modify an existing exam.
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

import { examApi } from '../api'
import { BaseExam, ExamOut } from '../generated-client/exam'
import { ModalPropsModify } from '../interfaces/components.interface'
import NotificationContext from '../NotificationContext'


const formContent: {key: keyof BaseExam, label: string, placeholder: string}[] = [
  { key: 'name', label: 'Exam Name', placeholder: 'Knee complaints' },
  { key: 'country', label: 'Country', placeholder: '' },
  { key: 'site', label: 'Site', placeholder: 'Berlin' },
  { key: 'address', label: 'Site Address', placeholder: 'Street name, number' },
]

export default function ExamModal(props: ModalPropsModify<ExamOut | undefined>) {
  const [, showNotification] = React.useContext(NotificationContext)
  
	const [exam, setExam] = React.useState<BaseExam>(
		props.item ? 
			{
				patient_id: props.item.patient_id,          // eslint-disable-line camelcase
				name: props.item.name,
				country: props.item.country,
				site: props.item.site,
				address: props.item.address,
				status: 'UPDATED',
				is_template: props.item.is_template,        // eslint-disable-line camelcase
				is_frozen: props.item.is_frozen,            // eslint-disable-line camelcase
			}
		:
			{
				patient_id: undefined,    // eslint-disable-line camelcase
				name: '',
				country: '',
				site: '',
				address: '',
				status: 'NEW',
				is_template: true,        // eslint-disable-line camelcase
				is_frozen: false,         // eslint-disable-line camelcase
			}
  )

  const mutation = 
		props.item ?
			useMutation(async () => {
				await examApi
				.updateExamApiV1ExamExamIdPut(props.item!.id, exam)   // props.item most not be and is not undefined here
				.then(() => {
				  props.onSubmit()
				})
			})
		:
			useMutation(async () => {
				await examApi
				.createExamApiV1ExamNewPost(exam)
				.then(() => {
				  props.onSubmit()
				})
			})

	const title = 
		props.item ?
			'Update Exam'
		:
			'Create New Exam'
  
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
          {title}
        </Typography>

        <Stack spacing={1}>
          <Grid container rowSpacing={1.5} columnSpacing={5}>
            {formContent.map((entry, index) => (
              <Grid key={index} md={6}>
                <FormLabel>{entry.label}</FormLabel>
                <Input
                  name={entry.key}
                  onChange={(e) => setExam({ ...exam, [e.target.name]: e.target.value })}
                  placeholder={entry.placeholder}
									value={props.item ? exam[entry.key]?.toString() : undefined}
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
              if (exam.name == '') {
                showNotification({message: 'Name must not be empty.', type: 'warning'})
              } else {
                mutation.mutate()
                props.setOpen(false)
              }
            }}
          >
            Save
          </Button>
        </Stack>
      </ModalDialog>
    </Modal>
  )
}
