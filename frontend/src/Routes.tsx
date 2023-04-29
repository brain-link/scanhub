import { Routes, Route } from "react-router-dom";
import React from 'react';

// Import views
import App from './views/App';
import Dashboard from './views/Dashboard';
import DeviceTable from './views/DeviceTable';
import PatientTable from './views/PatientTable';
import PatientIndex from './views/PatientIndex';

export function RouteConfiguration () {
    return (
        <Routes>
            <Route path='/' element={<App />}>
                <Route path="/" element={<Dashboard />} />
                <Route path="/patients">
                    <Route index element={<PatientTable />} />
                    {/* Using multiple optional parameters in patient path, denoted by the question mark */}
                    <Route path=':patientId' element={<PatientIndex/>} />
                    <Route path=':patientId/:examId' element={<PatientIndex/>} />
                    <Route path=':patientId/:examId/:procedureId' element={<PatientIndex/>} />
                    <Route path=':patientId/:examId/:procedureId/:examViewId' element={<PatientIndex/>} />
                </Route>
                <Route path="/devices">
                    <Route index element={ <DeviceTable /> } />
                </Route> 
            </Route>
      </Routes>
    )
}
