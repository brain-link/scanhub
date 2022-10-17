import { Routes, Route } from "react-router-dom";
import { Suspense } from 'react'
import React from 'react';

import Dashboard from './Dashboard'
import DeviceTable from "./DeviceTable";
import PatientTable from "./PatientTable";
import { App } from './App'
import { PatientIndex } from './Patient'
import { Procedure, ProcedureMainContentSwitcher, ProcedureMainContent } from "./Procedure";
import TestPage from './TestPage';

export function RouteConfiguration () {
    return (
        <Routes>
            <Route path='/' element={<App />}>
                <Route path="/" element={<Dashboard />} />
                <Route path="/patients">
                    <Route index element={
                        <Suspense fallback={<div>Loading...</div>}>
                            <PatientTable />
                        </Suspense>
                    } />
                    <Route path=':patientId'>
                        <Route index element={<PatientIndex />} />
                        <Route path=':procedureId' element={<Procedure />} >
                            <Route path=':recordingId' element={<ProcedureMainContentSwitcher />}>
                                <Route index element={<ProcedureMainContent />} />
                                <Route path=':content' element={<ProcedureMainContent />} />
                            </Route>
                        </Route>
                    </Route>
                </Route>
                <Route path="/devices">
                    <Route index element={
                    <Suspense fallback={<div>Loading...</div>}>
                        <DeviceTable />
                    </Suspense>
                    } />
                </Route> 

                {/* Testing */}
                <Route path="/test" element={<TestPage />} />
                
            </Route>
      </Routes>
    )
}
