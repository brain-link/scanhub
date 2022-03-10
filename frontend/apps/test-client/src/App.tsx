import './App.css'
import { RelayEnvironmentProvider } from 'react-relay'
import { environment } from './env'
import { Client } from './Client'
import { Suspense } from 'react'
import { ErrorBoundary } from 'error-boundary'

function App() {
  return (
    <RelayEnvironmentProvider environment={environment}>
      <ErrorBoundary>
        <Suspense fallback={<div>Loading...</div>}>
          <Client />
        </Suspense>
      </ErrorBoundary>
    </RelayEnvironmentProvider>
  )
}

export default App
