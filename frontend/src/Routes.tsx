// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
// Routes.tsx is responsible for defining the routes of the react app.
import React from 'react'
import { Route, Routes } from 'react-router-dom'

// Import views
import App from './views/App'
import PatientIndex from './views/PatientIndex'
import PatientListView from './views/PatientListView'
import RecordViewer from './views/RecordViewer'
import Templates from './views/Templates'

export function RouteConfiguration() {
  return (
    // <Routes>
    //   <Route path='/' element={<App />}>
    //     <Route path='/' element={<Dashboard />} />

    //     <Route path='/patients'>
    //       <Route index element={<PatientTable />} />
    //       {/* Using multiple optional parameters in patient path, denoted by the question mark */}
    //       <Route path=':patientId' element={<PatientIndex />}>
    //         <Route path=':examId' element={<PatientIndex />}>
    //           <Route path=':procedureId' element={<PatientIndex />} />
    //         </Route>
    //       </Route>

    //       <Route path='dcmview/:patientId' element={<RecordViewer />} />
    //     </Route>
    //   </Route>
    // </Routes>

    <Routes>
      <Route path='/' element={<App />}>
        <Route index element={<PatientListView />} />
        {/* Using multiple optional parameters in patient path, denoted by the question mark */}
        <Route path=':patientId' element={<PatientIndex />}>
          <Route path=':examId' element={<PatientIndex />} />
        </Route>
        
        <Route path='/templates' element={<Templates />} />

      </Route>
    </Routes>
  )
}
