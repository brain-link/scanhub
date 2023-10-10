// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
// Dashboard.tsx is responsible for rendering the dashboard view. It is the default view of the app.
import Box from '@mui/joy/Box'
import Card from '@mui/joy/Card'
import CardContent from '@mui/joy/CardContent'
import IconButton from '@mui/joy/IconButton'
// import CircularProgress from '@mui/joy/CircularProgress';
import LinearProgress from '@mui/joy/LinearProgress'
import Typography from '@mui/joy/Typography'
import Container from '@mui/system/Container'
import React from 'react'

import useHealthCheck from '../client/healthcheck'
import baseUrls from '../client/urls'

// import DeviceTable from "./DeviceTable";
// import PatientTable from "./PatientTable";

export default function Dashboard() {
  const isReady = useHealthCheck(baseUrls.examService)

  if (!isReady) {
    return (
      <Box
        sx={{
          m: 10,
          gap: 2,
          display: 'flex',
          flexDirection: 'column',
          width: '100%',
          alignItems: 'center',
        }}
      >
        {/* <CircularProgress size="md" value={10} variant="soft" /> */}
        <LinearProgress determinate={false} size='sm' value={20} sx={{ width: '100px' }} />
        <Typography>Connecting to ScanHub...</Typography>
      </Box>
    )
  }

  return (
    <Box sx={{ p: 5, display: 'flex', width: '100vw', justifyContent: 'center' }}>
      <Card sx={{ width: 600, height: 400, p: 10, m: 5 }}>
        <CardContent
          component='img'
          src='https://brain-link.de/wp-content/uploads/2022/03/ScanHub.svg'
          sx={{ m: 2, justifyContent: 'center', height: '60%' }}
        />

        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', mt: 5, gap: 1 }}>
          <Typography>ScanHub &copy; 2022, Powered by BRAIN-LINK</Typography>
          <IconButton variant='plain' href='https://www.brain-link.de/'>
            <img
              src='https://avatars.githubusercontent.com/u/27105562?s=200&v=4'
              alt=''
              height='30'
              className='d-inline-block'
            />
          </IconButton>
        </Box>
      </Card>
    </Box>
  )
}
