// import { Link } from 'react-router-dom'

import { useQuery } from "react-query";
import { Device } from './Interfaces'

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
        <Box sx={{ flexGrow: 1, justifyContent: 'center', p: 2, pt: 0 }}>
            <Paper sx={{ overflow: 'scroll', maxHeight: '82vh'}}>
                
                <TableContainer>
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
        </Box>
    );
}
