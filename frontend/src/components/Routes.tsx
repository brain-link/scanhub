import { Routes, Route } from "react-router-dom";
import { Suspense } from 'react'

import { Dashboard } from './Dashboard'
import { PatientTable } from './PatientTable'
import { DeviceTable } from './DeviceTable'
import { Navigation } from './Navigation'
import { PatientIndex } from './Patient'
import { Procedure, ProcedureMainContentSwitcher, ProcedureMainContent } from "./Procedure";

export function RouteConfiguration () {
    return (
        <Routes>
            <Route path='/' element={<Navigation />}>
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
            </Route>
      </Routes>
    )
}
