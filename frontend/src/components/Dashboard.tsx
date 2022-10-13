import React from "react";

// import Card from '@mui/joy/Card';

import {
    Card,
    Container,
    IconButton,
    Box,
    CardMedia,
    Typography
} from "@mui/material"

export function Dashboard() {
    return (
        <Container maxWidth={false} sx={{ display: 'flex', justifyContent: 'center'}}>
            <Card sx={{ maxWidth: 600, p: 10}}>
                <CardMedia
                    component="img"
                    width="200"
                    src="https://brain-link.de/wp-content/uploads/2022/03/ScanHub.svg"
                    sx={{ m: 2 }}
                />

                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', mt: 5, gap: 1}}>

                    <Typography>ScanHub &copy; 2022, Powered by BRAIN-LINK</Typography>
                    <IconButton href="https://www.brain-link.de/">
                        <img
                            src='https://avatars.githubusercontent.com/u/27105562?s=200&v=4'
                            alt=""
                            height="30"
                            className="d-inline-block"
                        />
                    </IconButton>

                </Box>
                        
            </Card>       
        </Container>
             
    );
}