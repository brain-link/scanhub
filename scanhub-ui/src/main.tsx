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
import * as React from 'react'
import ReactDOM from 'react-dom/client'
import { QueryClient, QueryClientProvider } from 'react-query'
import { BrowserRouter } from 'react-router-dom'
import { StyledEngineProvider } from '@mui/joy/styles';

import { RouteConfiguration } from './Routes'
import LoginContextProvider from './LoginContextProvider'


const queryClient = new QueryClient()
// const root = ReactDOM.createRoot(document.getElementById('root')!)

// root.render(
//   <React.StrictMode>
//     <QueryClientProvider client={queryClient}>
//       <BrowserRouter>
//         <LoginContextProvider>
//           <RouteConfiguration />
//         </LoginContextProvider>
//       </BrowserRouter>
//     </QueryClientProvider>
//   </React.StrictMode>,
// )

ReactDOM.createRoot(document.querySelector('#root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <StyledEngineProvider injectFirst>
          <LoginContextProvider>
            <RouteConfiguration />
          </LoginContextProvider>
        </StyledEngineProvider>
      </BrowserRouter>
    </QueryClientProvider>
  </React.StrictMode>
)
