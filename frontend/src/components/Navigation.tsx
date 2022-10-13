import * as React from 'react';

import { Link as RouterLink } from 'react-router-dom';

import IconButton from '@mui/material/IconButton';
import AppBar from '@mui/material/AppBar';
import Typography from '@mui/material/Typography';
import Toolbar from '@mui/material/Toolbar';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';

function isActive(status) {
    return !status ? "outlined" : "contained"
}

export function Navigation() {

    const [activeElement, setActiveElement] = React.useState(0)

    const updateActiveElement = (id) => {
        setActiveElement(activeElement !== id ? id : -1)
    }

    return (
        <Box sx={{ display: 'flex', flexDirection: 'row', position: 'sticky', zIndex: 'snackbar' }}>
            <AppBar position="fixed" color="transparent">
                <Toolbar sx={{ gap: 1.5 }}>

                    <IconButton href="https://www.brain-link.de/" sx={{ height: 40 }}>
                        <img
                            src='https://avatars.githubusercontent.com/u/27105562?s=200&v=4'
                            alt=""
                            height="40"
                            className="d-inline-block"
                        />
                    </IconButton>

                    <Typography variant="h4" sx={{ mr: 5 }}>
                        ScanHub
                    </Typography>    
                    

                    <Button 
                        component={RouterLink} 
                        to="/" color="primary" 
                        variant={isActive(0 === activeElement)} 
                        onClick={0 !== activeElement ? () => updateActiveElement(0) : () => {}}
                    >
                        Dashboard
                    </Button>

                    <Button 
                        component={RouterLink} 
                        to="/patients" 
                        variant={isActive(1 === activeElement)} 
                        onClick={1 !== activeElement ? () => updateActiveElement(1) : () => {}}
                    >
                        Patients
                    </Button>

                    <Button 
                        component={RouterLink} 
                        to="/devices" 
                        variant={isActive(2 === activeElement)} 
                        onClick={2 !== activeElement ? () => updateActiveElement(2) : () => {}}
                    >
                        Devices
                    </Button>

                    <Button 
                        component={RouterLink} 
                        to="/patient" 
                        variant={isActive(3 === activeElement)} 
                        onClick={3 !== activeElement ? () => updateActiveElement(3) : () => {}}
                    >
                        Patient
                    </Button>
                    
                </Toolbar>
            </AppBar>
        </Box>
    );
}
