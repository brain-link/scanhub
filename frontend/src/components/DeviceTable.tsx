// import { Link } from 'react-router-dom'

import { useQuery } from "react-query";
import { Device } from './Interfaces'

// import {
//     CCard,
//     CCardTitle,
//     CCardSubtitle,
//     CSpinner,
//     CCardHeader,
//     CCardBody,
//     CTable,
//     CTableBody,
//     CTableDataCell,
//     CTableHead,
//     CTableRow,
//     CTableHeaderCell,
//     CNavLink,
//     CContainer,
// } from '@coreui/react'

import * as React from 'react';
// import { useTheme } from '@mui/material/styles';
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

// import TablePaginationActions from './TablePagination'

export function DeviceTable() {
  
    const { data: devices, isSuccess } = useQuery<Device[]>("devices/");

    if (!isSuccess) {
        return (
            <Container maxWidth={false} sx={{ width: '50%', mt: 5, }}>
                <Typography align='center'>Loading devices...</Typography>
                <LinearProgress />
            </Container>
        )
    }

    // const [page, setPage] = React.useState(0);
    // const [rowsPerPage, setRowsPerPage] = React.useState(10);

    // const handleChangePage = (event: unknown, newPage: number) => {
    //     setPage(newPage);
    // };

    // const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    //     setRowsPerPage(+event.target.value);
    //     setPage(0);
    // };
      
    return (
        <Container sx={{ display: 'flex', justifyContent: 'center'}}>
            <Paper sx={{ width: 0.8, overflow: 'hidden' }}>
                <TableContainer sx={{ maxHeight: '90vh'}}>
                    <Table stickyHeader aria-label="Device Table">
                        <TableHead>
                            <TableRow>
                                <TableCell><Typography variant="button">ID</Typography></TableCell>
                                <TableCell><Typography variant="button">Modality</Typography></TableCell>
                                <TableCell><Typography variant="button">Location</Typography></TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {devices?.map(device => (
                                <TableRow key={device.id}>
                                    <TableCell>{ device.id }</TableCell>
                                    <TableCell>{ device.modality }</TableCell>
                                    <TableCell>{ device.address }</TableCell>
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
        </Container>
    );
}

    // return (
    //     <CCard className='m-4'>
    //         <CCardHeader className="h5">Devices</CCardHeader>
    //         <CCardBody className='m-2'>

    //             {/* <CCardTitle>List of all Devices</CCardTitle>
    //             <CCardSubtitle className="mb-4 text-medium-emphasis">
    //                 Devices
    //             </CCardSubtitle> */}

    //             <CTable hover>
    //                 <CTableHead color='secondary'>
    //                     <CTableRow>
    //                         <CTableHeaderCell scope="col">ID</CTableHeaderCell>
    //                         <CTableHeaderCell scope="col">Modality</CTableHeaderCell>
    //                         <CTableHeaderCell scope="col">Address</CTableHeaderCell>
    //                         <CTableHeaderCell scope="col">Site</CTableHeaderCell>
    //                     </CTableRow>
    //                 </CTableHead>
    //                 <CTableBody>
    //                     {
    //                         devices?.map(device => (
    //                             <CTableRow align="middle" key={device.id}>
    //                                 <CTableHeaderCell scope="row">
    //                                     <CNavLink to={`/devices/${device.id}`} component={Link}>{device.id}</CNavLink>
    //                                 </CTableHeaderCell>
    //                                 <CTableDataCell>{device.modality}</CTableDataCell>
    //                                 <CTableDataCell>{device.address}</CTableDataCell>
    //                                 <CTableDataCell>{device.site}</CTableDataCell>
    //                             </CTableRow>
    //                         ))
    //                     }
    //                 </CTableBody>
    //             </CTable>
    //         </CCardBody>
    //     </CCard>
    //     );
    // }
