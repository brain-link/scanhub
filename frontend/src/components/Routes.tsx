import { Routes, Route } from "react-router-dom";
import React from 'react';

import Dashboard from './Dashboard'
import DeviceTable from "./DeviceTable";
import PatientTable from "./PatientTable";
import App from './App'
import PatientIndex from './exam-mainview/PatientIndex'
import Procedures from "./exam-mainview/procedures";

import ExamViewController from "./exam-mainview/ExamViewController";

export function RouteConfiguration () {
    return (
        <Routes>
            <Route path='/' element={<App />}>
                <Route path="/" element={<Dashboard />} />
                <Route path="/patients">
                    <Route index element={<PatientTable />} />
                    <Route path=':patientId' element={<PatientIndex/>} >
                        <Route path=':examId' element={<Procedures/>}>
                            <Route path=':procedureId' element={<ExamViewController/>}>
                                <Route path=':examViewId'/>
                            </Route>
                        </Route>
                    </Route>
                </Route>
                <Route path="/devices">
                    <Route index element={ <DeviceTable /> } />
                </Route> 
            </Route>
      </Routes>
    )
}
