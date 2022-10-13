import { Link } from 'react-router-dom'
import React from 'react'
import { useQuery } from "react-query";
import { Patient } from './Interfaces'

// import {
//     CCard,
//     CCardBody,
//     CContainer,
//     CSpinner,
//     CCardSubtitle,
//     CCardTitle,
//     CTable,
//     CTableBody,
//     CTableDataCell,
//     CTableHead,
//     CTableRow,
//     CTableHeaderCell,
//     CBadge,
//     CNavLink,
//     CCardHeader,
// } from '@coreui/react'

import Container from '@mui/material/Container';
import LinearProgress from '@mui/material/LinearProgress';
import Box from '@mui/material/Box'
import { Typography } from '@mui/material';

export function PatientTable() {

    // Syncing our data
    const { data: patients, isSuccess } = useQuery<Patient[]>("patients/");

    // if (!isSuccess) {
    //     return (
    //         <Container maxWidth={false} sx={{ width: '50%', mt: 5, }}>
    //             <Typography align='center'>Loading patients...</Typography>
    //             <LinearProgress />
    //         </Container>
    // )


    return (
        <Container maxWidth={false} sx={{ width: '50%', mt: 5, }}>
            <Typography align='center'>Under construction...</Typography>
            <LinearProgress />
        </Container>
    )

    // return (
    //     <CCard className='m-4'>
    //         <CCardHeader className="h5">Patients</CCardHeader>
    //         <CCardBody className='m-2'>
    //             {/* <CCardTitle className="mb-4">List of all Patients</CCardTitle> */}
    //             <CTable hover>
    //                 <CTableHead color='secondary'>
    //                     <CTableRow>
    //                         <CTableHeaderCell scope="col">ID</CTableHeaderCell>
    //                         <CTableHeaderCell scope="col">Sex <span className='fa fa-arrow-down' /></CTableHeaderCell>
    //                         <CTableHeaderCell scope="col">Birthday</CTableHeaderCell>
    //                         <CTableHeaderCell scope="col">Status</CTableHeaderCell>
    //                         <CTableHeaderCell scope="col">Concern</CTableHeaderCell>
    //                         <CTableHeaderCell scope="col"><input type='checkbox' /></CTableHeaderCell>
    //                     </CTableRow>
    //                 </CTableHead>
    //                 <CTableBody>
    //                     {
    //                         // !loading ? patients.map(patient => (    
    //                         patients?.map(patient => (    
    //                             <CTableRow align="middle" key={patient.id}>
    //                                 <CTableHeaderCell scope="row">
    //                                     <CNavLink to={`/patients/${patient.id}`} component={Link}>{patient.id}</CNavLink>
    //                                 </CTableHeaderCell>
    //                                 <CTableDataCell>{patient.sex}</CTableDataCell>
    //                                 <CTableDataCell>{patient.birthday}</CTableDataCell>
    //                                 <CTableDataCell>{patient.status}</CTableDataCell>
    //                                 <CTableDataCell>{patient.concern}</CTableDataCell>
    //                                 <CTableDataCell><input type='checkbox' /></CTableDataCell>
    //                             </CTableRow>
    //                         ))
    //                     }
    //                 </CTableBody>
    //             </CTable>
    //         </CCardBody>
    //     </CCard>
    // );
}





