/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * App.tsx is the main view of the react app. It is responsible for rendering the navigation bar and the main content.
 */
import Box from '@mui/joy/Box'
import { CssVarsProvider as JoyCssVarsProvider } from '@mui/joy/styles'
import CssBaseline from '@mui/material/CssBaseline'
import {
  THEME_ID as MATERIAL_THEME_ID,
  Experimental_CssVarsProvider as MaterialCssVarsProvider,
  experimental_extendTheme as materialExtendTheme,
} from '@mui/material/styles'
import { GlobalStyles } from '@mui/system'
import * as React from 'react'
import { Outlet } from 'react-router-dom'

import Snackbar from '@mui/joy/Snackbar'
import NotificationContext from '../NotificationContext'

import Navigation from '../components/Navigation'

const materialTheme = materialExtendTheme()

export default function App() {

  const [messageObj, setMessageObject] = React.useContext(NotificationContext)
  

  return (
    <MaterialCssVarsProvider defaultMode='system' theme={{ [MATERIAL_THEME_ID]: materialTheme }}>
      <JoyCssVarsProvider defaultMode='system' disableTransitionOnChange>
        <CssBaseline />
        <GlobalStyles
          styles={{
            ':root': {
              '--Collapsed-breakpoint': '769px', // form will stretch when viewport is below `769px`
              '--Cover-width': '40vw', // must be `vw` only
              '--Form-maxWidth': '700px',
              '--Transition-duration': '0.4s', // set to `none` to disable transition
              '--Sidebar-width': '300px',
              '--Navigation-height': '60px',
              // '--Navigation-height': '64px',  // set height of navigation bar
              // '--PatientView-toolbarHeight': '54px',
              // '--PatientView-drawerWidth': '300px',
              // '--PatientView-recordWidth': '300px',
            },
          }}
        />
        <Navigation />

        <Snackbar 
          open={messageObj.open} 
          variant={'soft'} 
          color={messageObj.type}
          anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
          onClose={() => setMessageObject({ ...messageObj, open: false})}
        >
          {messageObj.message}
        </Snackbar>

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
      </JoyCssVarsProvider>
    </MaterialCssVarsProvider>
  )
}
