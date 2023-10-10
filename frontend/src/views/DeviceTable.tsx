// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
// DeviceTable.tsx is responsible for rendering the device table view.
import AddSharpIcon from '@mui/icons-material/AddSharp'
import ExpandMoreIcon from '@mui/icons-material/ExpandMore'
import Box from '@mui/joy/Box'
import IconButton from '@mui/joy/IconButton'
import Typography from '@mui/joy/Typography'
import Accordion from '@mui/material/Accordion'
import AccordionDetails from '@mui/material/AccordionDetails'
import AccordionSummary from '@mui/material/AccordionSummary'
import LinearProgress from '@mui/material/LinearProgress'
import Paper from '@mui/material/Paper'
import Table from '@mui/material/Table'
import TableBody from '@mui/material/TableBody'
import TableCell from '@mui/material/TableCell'
import TableContainer from '@mui/material/TableContainer'
import TableHead from '@mui/material/TableHead'
import TableRow from '@mui/material/TableRow'
import Container from '@mui/system/Container'
import axios from 'axios'
import * as React from 'react'
import { useMutation } from 'react-query'

import { Device } from '../interfaces/data.interface'
import config from '../utils/config'

export default function DeviceTable() {
  // const { data: devices, isSuccess } = useQuery<Device[]>("/devices");
  const [devices, setDevices] = React.useState<Device[] | undefined>(undefined)
  const [expanded, setExpanded] = React.useState<string | false>(false)

  const handleExpandChange = (panel: string) => (event: React.SyntheticEvent, isExpanded: boolean) => {
    setExpanded(isExpanded ? panel : false)
  }

  async function fetchDevices() {
    await axios.get(`${config['baseURL']}/devices`).then((response) => {
      setDevices(response.data)
    })
  }

  React.useEffect(() => {
    fetchDevices()
  }, [])

  const mutation = useMutation(async () => {
    await axios.post(`${config['baseURL']}/devices/new`).then(() => {
      fetchDevices()
    })
  })

  if (!devices) {
    return (
      <Container maxWidth={false} sx={{ width: '50%', mt: 5, justifyContent: 'center' }}>
        <Typography>Loading devices...</Typography>
        <LinearProgress />
      </Container>
    )
  }

  return (
    <div style={{ width: '100%' }}>
      <Box sx={{ m: 2, display: 'flex', flexDirection: 'row-reverse' }}>
        <IconButton size='sm' variant='outlined'>
          <AddSharpIcon onClick={() => mutation.mutate()} />
        </IconButton>
      </Box>
      <Box sx={{ m: 2 }}>
        {devices?.map((device) => (
          <Accordion expanded={expanded === device.id} onChange={handleExpandChange(device.id)}>
            <AccordionSummary expandIcon={<ExpandMoreIcon />} aria-controls='panel1bh-content' id='panel1bh-header'>
              <Typography sx={{ width: '33%', flexShrink: 0 }}>Device ID: {device.id}</Typography>
              <Typography sx={{ color: 'text.secondary' }}>Modality: {device.modality}</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Typography> Created at: {new Date(device.datetime_created).toDateString()} </Typography>
              <Typography>
                {' '}
                Address: {device.datetime_updated ? new Date(device.datetime_updated).toDateString() : '-'}{' '}
              </Typography>
            </AccordionDetails>
          </Accordion>
        ))}
      </Box>
    </div>

    // <TableContainer component={Paper} sx={{ m: 2, overflow: 'auto' }}>
    //     <Table stickyHeader aria-label="Device Table">

    //         <TableHead>
    //             <TableRow>
    //                 <TableCell><Typography level="h5">ID</Typography></TableCell>
    //                 <TableCell><Typography level="h5">Modality</Typography></TableCell>
    //                 <TableCell><Typography level="h5">Location</Typography></TableCell>
    //                 <TableCell><Typography level="h5">Created at</Typography></TableCell>
    //                 <TableCell>
    //                     <IconButton size='sm' variant='outlined'>
    //                         <AddSharpIcon onClick={() => mutation.mutate()}/>
    //                     </IconButton>
    //                 </TableCell>
    //             </TableRow>
    //         </TableHead>

    //         <TableBody>
    //             {/* Map elements in devices to table cells */}
    //             { devices?.map(device => (
    //                 <TableRow
    //                     hover={true}
    //                     key={device.id}
    //                 >
    //                     <TableCell>{ device.id }</TableCell>
    //                     <TableCell>{ device.modality }</TableCell>
    //                     <TableCell>{ device.address }</TableCell>
    //                     <TableCell>{ format_date(device.created_at) }</TableCell>
    //                 </TableRow>
    //             )) }
    //         </TableBody>
    //     </Table>
    // </TableContainer>
  )
}
