import './index.scss'

import React from 'react'
import ReactDOM from 'react-dom'
import { BrowserRouter } from "react-router-dom";
import { Suspense } from 'react'
import { RouteConfiguration } from './components/Routes'

import { QueryClient, QueryClientProvider } from "react-query";
import { query } from "./utils/query";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      queryFn: query,
    },
  },
});

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <BrowserRouter>
        <RouteConfiguration />
      </BrowserRouter>
    </Suspense>
  );
}

const root = ReactDOM.createRoot(document.getElementById("root")!);
root.render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </React.StrictMode>,
);
