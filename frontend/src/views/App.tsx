// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
// App.tsx is the main view of the react app. It is responsible for rendering the navigation bar and the main content.
import Box from '@mui/joy/Box'
import CssBaseline from '@mui/joy/CssBaseline'
import { CssVarsProvider } from '@mui/joy/styles'
import { GlobalStyles } from '@mui/system'
import * as React from 'react'
import { Outlet } from 'react-router-dom'

import Navigation from '../components/Navigation'

export default function App() {
  return (
    <CssVarsProvider
      // defaultMode="dark"
      disableTransitionOnChange
    >
      <CssBaseline />
      <GlobalStyles
        styles={{
          ':root': {
            '--Collapsed-breakpoint': '769px', // form will stretch when viewport is below `769px`
            '--Cover-width': '40vw', // must be `vw` only
            '--Form-maxWidth': '700px',
            '--Transition-duration': '0.4s', // set to `none` to disable transition
            // '--Navigation-height': '64px',  // set height of navigation bar
            // '--PatientView-toolbarHeight': '54px',
            // '--PatientView-drawerWidth': '300px',
            // '--PatientView-recordWidth': '300px',
          },
        }}
      />
      <Navigation />

      {/* Main content */}
      <Box
        sx={{
          m: 0,
          p: 0,
          gap: 2,
          justifyContent: 'start',
          display: 'flex',
          flexDirection: 'row',
          maxHeight: '100vh',
        }}
      >
        <Outlet />
      </Box>
    </CssVarsProvider>
  )
}
