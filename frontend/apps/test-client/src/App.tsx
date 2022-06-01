// import 'scanhub-ui/css/index.css'
import './style.scss'

import { RelayEnvironmentProvider } from 'react-relay'
import { HashRouter } from 'react-router-dom'
import { Suspense } from 'react'
import { environment } from './env'
import { RouteConfig } from './components/Routes'

import { ThemeProvider } from 'styled-components'
import { DialogSystem, ErrorBoundary, theme } from 'scanhub-ui'

export function App() {
  return (
    <RelayEnvironmentProvider environment={environment}>
      <ErrorBoundary>
        <Suspense fallback={<div>Loading...</div>}>
          <ThemeProvider theme={theme}>
            <HashRouter>
              <DialogSystem>
                <RouteConfig />
              </DialogSystem>
            </HashRouter>
          </ThemeProvider>
        </Suspense>
      </ErrorBoundary>
    </RelayEnvironmentProvider>
  )
}
