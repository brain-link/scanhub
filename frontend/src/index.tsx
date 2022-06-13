import './index.scss'

import React from 'react'
import ReactDOM from 'react-dom'
import { BrowserRouter } from "react-router-dom";
import { Suspense } from 'react'
import { RouteConfiguration } from './components/Routes'

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
root.render(<App />);
