import * as React from 'react';
import { useQuery } from "react-query";
import { Device } from './Interfaces'
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from "@mui/material/TableHead";
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import LinearProgress from '@mui/material/LinearProgress';
import Typography from '@mui/joy/Typography';
import Container from '@mui/system/Container';
import Box from '@mui/joy/Box'


export default function DeviceTable() {
  
    const { data: devices, isSuccess } = useQuery<Device[]>("devices/");

    if (!isSuccess) {
        return (
            <Container maxWidth={false} sx={{ width: '50%', mt: 5, justifyContent: 'center' }}>
                <Typography>Loading devices...</Typography>
                <LinearProgress />
            </Container>
        )
    }

    return (
        <Box sx={{ flexGrow: 1, justifyContent: 'center', p: 2 }}>
            {/* <Paper sx={{ overflow: 'scroll', maxHeight: '82vh'}}> */}

            <TableContainer component={Paper} sx={{ overflow: 'scroll', maxHeight: '90vh' }}>
                <Table stickyHeader aria-label="Device Table">
                    <TableHead>
                        <TableRow>
                            <TableCell><Typography level="h5">ID</Typography></TableCell>
                            <TableCell><Typography level="h5">Modality</Typography></TableCell>
                            <TableCell><Typography level="h5">Location</Typography></TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {devices?.map(device => (
                            <TableRow hover={true} key={device.id}>
                                <TableCell>{ device.id }</TableCell>
                                <TableCell>{ device.modality }</TableCell>
                                <TableCell>{ device.address }</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </Box>
    );
}
