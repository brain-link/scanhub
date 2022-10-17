import { Link as RouterLink } from 'react-router-dom';
import { Patient } from './Interfaces'
import { useQuery } from "react-query";
import * as React from 'react';
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

export default function PatientTable() {

    // Syncing our data
    const { data: patients, isSuccess } = useQuery<Patient[]>("patients/");

    if (!isSuccess) {
        return (
            <Container maxWidth={false} sx={{ width: '50%', mt: 5, justifyContent: 'center' }}>
                <Typography>Loading patients...</Typography>
                <LinearProgress />
            </Container>
    )}

    return (
        // <Box sx={{ flexGrow: 1, justifyContent: 'center', p: 2, pt: 0 }}>
        //     <Paper sx={{ overflow: 'scroll', maxHeight: '82vh'}}>
        
        <Box sx={{ flexGrow: 1, justifyContent: 'center', p: 2 }}> 
            <TableContainer component={Paper} sx={{ overflow: 'scroll', maxHeight: '90vh' }}>
                <Table stickyHeader aria-label="Device Table">
                    <TableHead>
                        <TableRow>
                            <TableCell><Typography level="h5">ID</Typography></TableCell>
                            <TableCell><Typography level="h5">Sex</Typography></TableCell>
                            <TableCell><Typography level="h5">Birthday</Typography></TableCell>
                            <TableCell><Typography level="h5">Status</Typography></TableCell>
                            <TableCell><Typography level="h5">Concern</Typography></TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {patients?.map(patient => (
                            <TableRow hover={true} component={RouterLink} to={`/patients/${patient.id}`} key={patient.id} sx={{ textDecoration: 'none' }}>
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
        </Box>
    );
}





