/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * Routes.tsx is responsible for defining the routes of the react app.
 */
import React from 'react'
import { useContext } from 'react'
import { Navigate, Route, Routes, useNavigate } from 'react-router-dom'
import CssBaseline from '@mui/joy/CssBaseline';
import { GlobalStyles } from '@mui/system'
import { CssVarsProvider as JoyCssVarsProvider } from '@mui/joy/styles'
import {
  THEME_ID as MATERIAL_THEME_ID,
  Experimental_CssVarsProvider as MaterialCssVarsProvider,
  experimental_extendTheme as materialExtendTheme,
} from '@mui/material/styles'
const materialTheme = materialExtendTheme()

// import Context
import LoginContext from './LoginContext'
import UserManagement from './components/UserManagement'
import PatientIndex from './views/AcquisitionView'
// Import views
import App from './views/App'
import Login from './views/LoginView'
import PatientListView from './views/PatientListView'
// import RecordViewer from './views/RecordViewer'
import Templates from './views/TemplatesView'

// import models

export function RouteConfiguration() {
  const navigate = useNavigate()
  const [user, setUser] = useContext(LoginContext)

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
              '--Sidebar-width': '330px',
              '--Navigation-height': '60px',
              // '--Navigation-height': '64px',  // set height of navigation bar
              // '--PatientView-toolbarHeight': '54px',
              // '--PatientView-drawerWidth': '300px',
              // '--PatientView-recordWidth': '300px',
            },
          }}
        />

        <Routes>
          <Route path='/' element={user ? <App /> : <Navigate to='/login' />}>
            <Route index element={<PatientListView />} />
            <Route path=':patientId' element={<PatientIndex />}>
              <Route path=':examId' element={<PatientIndex />} />
            </Route>
            <Route path='/templates' element={<Templates />} />
            <Route path='/users' element={<UserManagement />} />
          </Route>

          <Route
            path='/login'
            element={
              <Login
                onLogin={(newuser) => {
                  console.log('Login confirmed.')
                  setUser(newuser)
                  navigate('/')
                }}
              />
            }
          />
        </Routes>
      </JoyCssVarsProvider>
    </MaterialCssVarsProvider>
  )
}
