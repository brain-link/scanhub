import * as React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from "react-router-dom";
import { QueryClient, QueryClientProvider } from 'react-query';

import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';

import { RouteConfiguration } from './components/Routes'

const queryClient = new QueryClient();
const root = ReactDOM.createRoot(document.getElementById("root")!);

root.render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <RouteConfiguration />
      </BrowserRouter>
    </QueryClientProvider>
    
  </React.StrictMode>
);
