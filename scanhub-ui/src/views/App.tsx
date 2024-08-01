/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * App.tsx is the main view of the react app. It is responsible for rendering the navigation bar and the main content.
 */
import * as React from 'react'
import axios from 'axios'
import { Outlet } from 'react-router-dom'
import Box from '@mui/joy/Box'
import Snackbar from '@mui/joy/Snackbar'

import NotificationContext from '../NotificationContext'
import Navigation from '../components/Navigation'
import LoginContext from '../LoginContext'


export default function App() {

  const [messageObj, setMessageObject] = React.useContext(NotificationContext)
  const [, showNotification] = React.useContext(NotificationContext)
  const [user] = React.useContext(LoginContext)

  React.useEffect(() => {
    // globally set authorization header
    axios.defaults.headers.common['Authorization'] = 'Bearer ' + user?.access_token;
    // reset authorization after logout
    return () => axios.defaults.headers.common['Authorization'] = undefined
  }, [user])

  React.useEffect(() => {
    const interceptor = axios.interceptors.response.use(function (response) {
        // Any status code that lie within the range of 2xx cause this function to trigger
        // Do something with response data
        return response;
      }, function (error) {
        // Any status codes that falls outside the range of 2xx cause this function to trigger
        // Do something with response error
        showNotification({message: 'A problem with the connection to the server occurred!', type: 'warning'})
        return Promise.reject(error);
    });
    return () => {
      // clean up of the effect (reset the interceptor)
      axios.interceptors.response.eject(interceptor);
    }
  }, [])

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
          {messageObj.message.toString()}
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
