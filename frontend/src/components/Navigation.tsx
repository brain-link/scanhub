import React from 'react';
import { Link as RouterLink, useLocation} from 'react-router-dom';

import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';

import { useColorScheme } from '@mui/joy/styles';
import IconButton from '@mui/joy/IconButton';
import Button from '@mui/joy/Button';
import Box from '@mui/joy/Box';

// Icons
import HomeRoundedIcon from '@mui/icons-material/HomeRounded';
import DarkModeRoundedIcon from '@mui/icons-material/DarkModeRounded';
import LightModeRoundedIcon from '@mui/icons-material/LightModeRounded';

// Menu elements
const menuItems = [
    {id: 0, text: "Home", link: "/"},
    {id: 1, text: "Patients", link: "/patients"},
    {id: 2, text: "Devices", link: "/devices"},
];

function ColorSchemeToggle() {
    const { mode, setMode } = useColorScheme();
    const [mounted, setMounted] = React.useState(true);
    React.useEffect(() => {
        setMounted(true);
    }, []);

    if (!mounted) {
        return <IconButton size="sm" variant="outlined" color="primary" />;
    }

    return (
        <IconButton
            id="toggle-mode"
            variant="outlined"
            color="primary"
            size="sm"
            onClick={() => {
                if (mode === 'light') {
                    setMode('dark');
                } else {
                    setMode('light');
                }
            }}
        >
            {mode === 'light' ? <DarkModeRoundedIcon /> : <LightModeRoundedIcon />}
        </IconButton>
    );
}

export default function Navigation() {

    const loc = useLocation();

    return (
        <Box sx={{ display: 'flex', flexDirection: 'row', position: 'sticky', zIndex: 'snackbar' }}>
            <AppBar position="fixed" color="inherit">
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
                                color="primary"
                                startDecorator={ item.link === "/" ? <HomeRoundedIcon/> : <></> }
                                disabled={ loc.pathname === item.link }
                                variant={ loc.pathname === item.link ? 'soft' : 'plain' }
                            >
                                {item.text}
                            </Button>
                        ))
                    }
                    </>

                    <Box sx={{ display: 'flex', flexDirection: 'row-reverse', width: '100%' }}>
                        <ColorSchemeToggle />
                    </Box>
                    
                </Toolbar>
            </AppBar>
        </Box>
    );
}
