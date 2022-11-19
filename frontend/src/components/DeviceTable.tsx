import * as React from 'react';
import { useMutation } from "react-query";
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
import AddSharpIcon from '@mui/icons-material/AddSharp';
import IconButton from '@mui/joy/IconButton';
import axios from 'axios';
import config from '../utils/config';

import { format_date } from '../utils/formatter';


export default function DeviceTable() {
  
    // const { data: devices, isSuccess } = useQuery<Device[]>("/devices");
    const [devices, setDevices] = React.useState<Device[] | undefined>(undefined);

    async function fetchDevices() {
        await axios.get(`${config["baseURL"]}/devices`)
        .then((response) => {setDevices(response.data)})
    }

    React.useEffect(() => {
        fetchDevices();
    }, [])

    const mutation = useMutation(async() => {
        await axios.post(`${config["baseURL"]}/devices/new`)
        .then(() => {
            fetchDevices();
        })
    })

    if (!devices) {
        return (
            <Container maxWidth={false} sx={{ width: '50%', mt: 5, justifyContent: 'center' }}>
                <Typography>Loading devices...</Typography>
                <LinearProgress />
            </Container>
        )
    }

    return (
        <TableContainer component={Paper} sx={{ m: 2, overflow: 'auto' }}>
            <Table stickyHeader aria-label="Device Table">

                <TableHead>
                    <TableRow>
                        <TableCell><Typography level="h5">ID</Typography></TableCell>
                        <TableCell><Typography level="h5">Modality</Typography></TableCell>
                        <TableCell><Typography level="h5">Location</Typography></TableCell>
                        <TableCell><Typography level="h5">Created at</Typography></TableCell>
                        <TableCell>
                            <IconButton size='sm' variant='outlined'>
                                <AddSharpIcon onClick={() => mutation.mutate()}/>
                            </IconButton>
                        </TableCell>
                    </TableRow>
                </TableHead>

                <TableBody>
                    {/* Map elements in devices to table cells */}
                    { devices?.map(device => (
                        <TableRow 
                            hover={true} 
                            key={device.id}
                        >
                            <TableCell>{ device.id }</TableCell>
                            <TableCell>{ device.modality }</TableCell>
                            <TableCell>{ device.address }</TableCell>
                            <TableCell>{ format_date(device.created_at) }</TableCell>
                        </TableRow>
                    )) }
                </TableBody>
            </Table>
        </TableContainer>
    );
}
