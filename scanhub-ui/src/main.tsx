/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * main.tsx is the entry point for the react app. It is responsible for rendering the app into the DOM.
 */
import '@fontsource/roboto/300.css'
import '@fontsource/roboto/400.css'
import '@fontsource/roboto/500.css'
import '@fontsource/roboto/700.css'
import { StyledEngineProvider } from '@mui/joy/styles'
import * as React from 'react'
import ReactDOM from 'react-dom/client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { BrowserRouter } from 'react-router-dom'

import LoginContextProvider from './LoginContextProvider'
import NotificationContextProvider from './NotificationContextProvider'
import { RouteConfiguration } from './Routes'

const queryClient = new QueryClient()

ReactDOM.createRoot(document.querySelector('#root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <StyledEngineProvider injectFirst>
          <LoginContextProvider>
            <NotificationContextProvider>
              <RouteConfiguration />
            </NotificationContextProvider>
          </LoginContextProvider>
        </StyledEngineProvider>
      </BrowserRouter>
    </QueryClientProvider>
  </React.StrictMode>,
)
