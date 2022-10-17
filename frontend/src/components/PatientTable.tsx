import { Link as RouterLink } from 'react-router-dom';
import { Patient } from './Interfaces'
import { useQuery } from "react-query";
import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from "@mui/material/TableHead";
import TableFooter from '@mui/material/TableFooter';
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import LinearProgress from '@mui/material/LinearProgress';
import Typography from '@mui/material/Typography';
import Container from '@mui/system/Container';
import Box from '@mui/joy/Box'

export function PatientTable() {

    // Syncing our data
    const { data: patients, isSuccess } = useQuery<Patient[]>("patients/");

    if (!isSuccess) {
        return (
            <Container maxWidth={false} sx={{ width: '50%', mt: 5, }}>
                <Typography align='center'>Loading patients...</Typography>
                <LinearProgress />
            </Container>
    )}

    return (
        <Box sx={{ flexGrow: 1, justifyContent: 'center', p: 2, pt: 0 }}>
            <Paper sx={{ overflow: 'scroll', maxHeight: '82vh'}}>
                
                <TableContainer>
                    <Table stickyHeader aria-label="Device Table">
                        <TableHead>
                            <TableRow>
                                <TableCell><Typography variant="button">ID</Typography></TableCell>
                                <TableCell><Typography variant="button">Sex</Typography></TableCell>
                                <TableCell><Typography variant="button">Birthday</Typography></TableCell>
                                <TableCell><Typography variant="button">Status</Typography></TableCell>
                                <TableCell><Typography variant="button">Concern</Typography></TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {patients?.map(patient => (
                                <TableRow component={RouterLink} to="/test" key={patient.id} color='primary' >
                                    <TableCell>{ patient.id }</TableCell>
                                    <TableCell>{ patient.sex }</TableCell>
                                    <TableCell>{ patient.birthday }</TableCell>
                                    <TableCell>{ patient.status }</TableCell>
                                    <TableCell>{ patient.concern }</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            {/* <TablePagination
                rowsPerPageOptions={[10, 25, 100]}
                component="div"
                count={devices.length}
                rowsPerPage={rowsPerPage}
                page={page}
                onPageChange={handleChangePage}
                onRowsPerPageChange={handleChangeRowsPerPage}
            /> */}
            </Paper>
        </Box>
    );

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





