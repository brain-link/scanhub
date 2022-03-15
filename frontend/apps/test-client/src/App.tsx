import 'scanhub-ui/css/index.css'
import { RelayEnvironmentProvider } from 'react-relay'
import { ThemeProvider } from 'styled-components'

import { environment } from './env'
import { RouteConfig } from './components/Routes'
import { DialogSystem, ErrorBoundary, theme } from 'scanhub-ui'
import { HashRouter } from 'react-router-dom'
import { Suspense } from 'react'

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
