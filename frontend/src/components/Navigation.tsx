import React from 'react';
import IconButton from '@mui/joy/IconButton';
import AppBar from '@mui/material/AppBar';
import Typography from '@mui/material/Typography';
import Toolbar from '@mui/material/Toolbar';
import Box from '@mui/joy/Box';
import Button from '@mui/material/Button';
import { Link as RouterLink } from 'react-router-dom';
import HomeRoundedIcon from '@mui/icons-material/HomeRounded';

function isActive(status) {
    return !status ? "outlined" : "contained"
}

interface NavItem {
    id: number;
    text: string;
    link: string;
}

const menuItems = [
    {id: 0, text: "Dashboard", link: "/"},
    {id: 1, text: "Patients", link: "/patients"},
    {id: 2, text: "Devices", link: "/devices"},
];

export function Navigation() {

    const [activeElement, setActiveElement] = React.useState(0)

    // To prevent bugs in visualization:
    // Make button highlighting dependent on route/path
    const updateActiveElement = (id) => {
        setActiveElement(activeElement !== id ? id : -1)
    }

    return (
        <Box sx={{ display: 'flex', flexDirection: 'row', position: 'sticky', zIndex: 'snackbar' }}>
            <AppBar position="fixed" color="transparent">
                <Toolbar sx={{ gap: 1.5 }}>

                    <IconButton variant="plain" href="https://www.brain-link.de/" sx={{ height: 40 }}>
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

                    <>
                    {
                        menuItems?.map( item => (
                            <Button
                                component={RouterLink}
                                to={item.link}
                                color='primary'
                                variant={isActive(item.id === activeElement)}
                                onClick={item.id !== activeElement ? () => updateActiveElement(item.id) : () => {}}
                            >
                                {item.text}
                            </Button>
                        ))
                    }
                    </>
                    
                    {/* <IconButton variant="plain" component={RouterLink} to="/">
                        <HomeRoundedIcon />
                    </IconButton> */}
                    
                </Toolbar>
            </AppBar>
        </Box>
    );
}
