// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
// PatientTable.tsx is responsible for rendering the patient table view.
import AddSharpIcon from '@mui/icons-material/AddSharp'
import Box from '@mui/joy/Box'
import IconButton from '@mui/joy/IconButton'
import LinearProgress from '@mui/joy/LinearProgress'
import Stack from '@mui/joy/Stack'
import Typography from '@mui/joy/Typography'
import Container from '@mui/system/Container'
import * as React from 'react'
import { useQuery } from 'react-query'
import { PatientOut } from '../generated-client/patient';
import { patientApi } from '../api'
import PatientCreateModal from '../components/PatientCreateModal'
import PatientTable from '../components/PatientTable'
import AlertItem from '../components/AlertItem'
import { Alerts } from '../interfaces/components.interface'

export default function PatientListView() {

  // const [patients, setPatients] = React.useState<Patient[]>([]);
  const [dialogOpen, setDialogOpen] = React.useState<boolean>(false)

  const {data: patients, isLoading, isError} = useQuery<PatientOut[]>({
    queryKey: ['patients'],
    queryFn: async () => { return await patientApi.getPatientListGet().then((result) => {return result.data})}
  })

  if (isLoading) {
    return (
      <Container maxWidth={false} sx={{ width: '50%', mt: 5, justifyContent: 'center' }}>
        <Typography>Loading patients...</Typography>
        <LinearProgress variant='plain' />
      </Container>
    )
  }

  if (isError) {
    return (
      <Container maxWidth={false} sx={{ width: '50%', mt: 5, justifyContent: 'center' }}>
        <AlertItem
          title="Error Loading Patients"
          type={Alerts.Error}
        />
      </Container>
    )
  }

  // TODO: Healthcheck exam service
  // const isReady = useHealthCheck(baseUrls.examService)

  // if (!isReady) {
  //   return (
  //     <Box
  //       sx={{
  //         m: 10,
  //         gap: 2,
  //         display: 'flex',
  //         flexDirection: 'column',
  //         width: '100%',
  //         alignItems: 'center',
  //       }}
  //     >
  //       {/* <CircularProgress size="md" value={10} variant="soft" /> */}
  //       <LinearProgress determinate={false} size='sm' value={20} sx={{ width: '100px' }} />
  //       <Typography>Connecting to ScanHub...</Typography>
  //     </Box>
  //   )
  // }

  return (
    <Box sx={{ m: 3 }}>
      
      <PatientCreateModal
        isOpen={dialogOpen}
        setOpen={setDialogOpen}
        onSubmit={(newPatient: PatientOut) => {patients?.push(newPatient)}}
        onClose={() => {}}
      />

      <Stack direction='row' sx={{ justifyContent: 'space-between', mb: 2 }}>
        <Typography level='title-md'>List of Patients</Typography>
        <IconButton size='sm' variant='outlined'>
          <AddSharpIcon onClick={() => setDialogOpen(true)} />
        </IconButton>
      </Stack>

      <PatientTable
        patients={patients ? patients : []}
      />

    </Box>
  )
}
