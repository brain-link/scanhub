import * as React from 'react'
import Input from '@mui/joy/Input'
import Modal from '@mui/joy/Modal'
import ModalClose from '@mui/joy/ModalClose'
import ModalDialog from '@mui/joy/ModalDialog'
import Stack from '@mui/joy/Stack'
import Typography from '@mui/joy/Typography'
import Button from '@mui/joy/Button'
import FormLabel from '@mui/joy/FormLabel'
import Grid from '@mui/joy/Grid'

import { useMutation } from 'react-query'
import { patientApi } from "../Api"
import { BasePatient, PatientOut } from "../generated-client/patient";
import { ModalComponentProps } from '../interfaces/components.interface'


// Patient form items, order is row wise
const createPatientFormContent = [
  { key: 'name', label: 'Patient Name', placeholder: 'Last name, first name' },
  { key: 'issuer', label: 'Issuer', placeholder: 'Last name, first name' },
  { key: 'sex', label: 'Patient Gender', placeholder: 'M/F/D' },
  { key: 'status', label: 'Status', placeholder: 'Patient created' },
  { key: 'birth_date', label: 'Patient Birth Date', placeholder: '01.01.1995' },
  { key: 'comment', label: 'Comment', placeholder: '' },
]


export default function PatientCreateModal(props: ModalComponentProps<PatientOut>) {

  const [patient, setPatient] = React.useState<BasePatient>({sex: '', name: '', issuer: '', status: '', comment: '', birth_date: ''})

  // Post a new record and refetch records table
  const mutation = useMutation(async () => {
    await patientApi.createPatientPost(patient).then((response) => { props.onSubmit(response.data) }).catch((err) => { console.log(err) })
  })

  return (
    <Modal
      keepMounted
      open={props.isOpen}
      color='neutral'
      onClose={() => props.setOpen(false)}
      sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}
    >
      <ModalDialog
        aria-labelledby='basic-modal-dialog-title'
        aria-describedby='basic-modal-dialog-description'
        size='sm'
        sx={{
          width: '50vw', 
          borderRadius: 'md', 
          p: 5
        }}
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
          Create New Patient
        </Typography>

        <form
          onSubmit={(event) => {
            event.preventDefault()
            mutation.mutate()
            props.setOpen(false)
          }}
        >
          <Stack spacing={5}>
            <Grid container rowSpacing={1.5} columnSpacing={5}>
              {createPatientFormContent.map((item, index) => (
                <Grid key={index} md={6}>
                  <FormLabel>{item.label}</FormLabel>
                  <Input
                    name={item.key}
                    onChange={(e) => setPatient({ ...patient, [e.target.name]: e.target.value })}
                    placeholder={item.placeholder}
                    required
                  />
                </Grid>
              ))}
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