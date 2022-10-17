import React from "react";

// import Card from '@mui/joy/Card';

// import {
//     Card,
//     Container,
//     IconButton,
//     Box,
//     CardMedia,
//     Typography,
//     Grid
// } from "@mui/material"
import Container from '@mui/material/Container';
import Card from '@mui/material/Card';
import CardMedia from '@mui/material/CardMedia'
import IconButton from '@mui/joy/IconButton';
import Box from '@mui/joy/Box';
import Typography from "@mui/joy/Typography";
import Grid from '@mui/joy/Grid';
import AddSharpIcon from '@mui/icons-material/AddSharp';

import { DeviceTable } from "./DeviceTable";
import { PatientTable } from "./PatientTable";

export function Dashboard() {
    return (
        // <Container maxWidth={false} sx={{ display: 'flex', justifyContent: 'center'}}>
        //     <Card sx={{ maxWidth: 600, p: 10}}>
        //         <CardMedia
        //             component="img"
        //             width="200"
        //             src="https://brain-link.de/wp-content/uploads/2022/03/ScanHub.svg"
        //             sx={{ m: 2 }}
        //         />

        //         <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', mt: 5, gap: 1}}>

        //             <Typography>ScanHub &copy; 2022, Powered by BRAIN-LINK</Typography>
        //             <IconButton href="https://www.brain-link.de/">
        //                 <img
        //                     src='https://avatars.githubusercontent.com/u/27105562?s=200&v=4'
        //                     alt=""
        //                     height="30"
        //                     className="d-inline-block"
        //                 />
        //             </IconButton>

        //         </Box>
                        
        //     </Card>       
        // </Container>

        <Box sx={{ display: 'flex', flexGrow: 1, alignContent: 'flex-start', minHeight: '92vh', bgcolor: 'background.componentBg' }}>

            <Box sx={{ width: '40%', borderRight: '1px solid', borderColor: 'divider' }}>
                <Box sx={{ p: 2, display: 'flex', flexDirection:'row', justifyContent:'space-between', flexWrap: 'wrap', alignItems: 'center' }}>
                    <Typography level="h5"> Devices </Typography>
                    <IconButton size='sm' variant='outlined'>
                        <AddSharpIcon />
                    </IconButton>
                </Box>
                <DeviceTable />
            </Box>

            <Box sx={{ flexGrow: 1 }}>
                <Box sx={{ p: 2, display: 'flex', flexDirection:'row', justifyContent:'space-between', flexWrap: 'wrap', alignItems: 'center' }}>
                    <Typography level="h5"> Patients </Typography>
                    <IconButton size='sm' variant='outlined'>
                        <AddSharpIcon />
                    </IconButton>
                </Box>
                <PatientTable />
            </Box>

        </Box>
             
    );
}