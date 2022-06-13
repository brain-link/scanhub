import { Link } from 'react-router-dom'
import React from 'react'

import { Patient } from './Interfaces'

import {
    CCard,
    CCardBody,
    CCardSubtitle,
    CCardTitle,
    CTable,
    CTableBody,
    CTableDataCell,
    CTableHead,
    CTableRow,
    CTableHeaderCell,
    CBadge,
    CNavLink,
} from '@coreui/react'


export function PatientTable() {

    let [loading, setLoading] = React.useState(true);
    let [patients, setPatients] = React.useState<Patient[]>([]);

    React.useEffect(() => {
        setLoading(true);
        const fetchData = async () => {
            const response = await fetch("http://localhost:8000/patients/");
            const data = await response.json();
            setPatients(data);
            setLoading(false);
        };

        fetchData();
    }, []);

    return (
        <CCard className='m-4'>
            <CCardBody className='m-2'>
                <CCardTitle>List of all Patients</CCardTitle>
                <CCardSubtitle className="mb-4 text-medium-emphasis">
                    Patients
                </CCardSubtitle>
                <CTable hover borderless>
                    <CTableHead color='dark'>
                        <CTableRow>
                            <CTableHeaderCell scope="col">ID</CTableHeaderCell>
                            <CTableHeaderCell scope="col">Sex <span className='fa fa-arrow-down' /></CTableHeaderCell>
                            <CTableHeaderCell scope="col">Birthday</CTableHeaderCell>
                            <CTableHeaderCell scope="col">Status</CTableHeaderCell>
                            <CTableHeaderCell scope="col">Concern</CTableHeaderCell>
                            <CTableHeaderCell scope="col"><input type='checkbox' /></CTableHeaderCell>
                        </CTableRow>
                    </CTableHead>
                    <CTableBody>
                        {
                            !loading ? patients.map(patient => (    
                                <CTableRow key={patient.id}>
                                    <CTableHeaderCell scope="row">
                                        <CNavLink to={`/patients/${patient.id}`} component={Link}>{patient.id}</CNavLink>
                                    </CTableHeaderCell>
                                    <CTableDataCell>{patient.sex}</CTableDataCell>
                                    <CTableDataCell>{patient.birthday}</CTableDataCell>
                                    <CTableDataCell>{patient.status}</CTableDataCell>
                                    <CTableDataCell>{patient.concern}</CTableDataCell>
                                    <CTableDataCell><input type='checkbox' /></CTableDataCell>
                                </CTableRow>
                            )) : null
                        }
                    </CTableBody>
                </CTable>
            </CCardBody>
        </CCard>
    );
}





