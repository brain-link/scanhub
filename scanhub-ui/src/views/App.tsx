/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * App.tsx is the main view of the react app. It is responsible for rendering the navigation bar and the main content.
 */
import * as React from 'react'
import { Outlet } from 'react-router-dom'
import Box from '@mui/joy/Box'
import Snackbar from '@mui/joy/Snackbar'

import NotificationContext from '../NotificationContext'
import Navigation from '../components/Navigation'


export default function App() {

  const [messageObj, setMessageObject] = React.useContext(NotificationContext)
  
  return (
    <>
      <Navigation />

      <Snackbar 
        open={messageObj.visible === true || messageObj.visible === undefined} 
        variant={'soft'} 
        color={messageObj.type}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
        onClose={() => setMessageObject({ ...messageObj, visible: false})}
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
    </>
  )
}
