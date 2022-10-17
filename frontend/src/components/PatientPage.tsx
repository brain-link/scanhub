import * as React from 'react';
import { useParams, Link as RouterLink } from 'react-router-dom';
// import { useMutation } from 'react-query';
// import axios from 'axios';
// MUI
import { styled } from '@mui/material/styles';
import Drawer from '@mui/material/Drawer';
import Divider from '@mui/material/Divider';
import Box from '@mui/joy/Box';
import Typography from '@mui/joy/Typography';
import IconButton from '@mui/joy/IconButton';
// Icons import
import MenuIcon from '@mui/icons-material/Menu';
// Import sub components
import Procedures from './ProcedureComponent';
import PatientInfo from './PatientInfo';

// Constants
const baseURL = "http://localhost:8000/";
const drawerWidth = 300;

const Main = styled('div', { shouldForwardProp: (prop) => prop !== 'open' }) <{ open?: boolean }>(
    ({ theme, open }) => (
        {
            flexGrow: 1,
            display: 'flex',
            flexDirection: 'column',
            minHeight: '100%',
            transition: theme.transitions.create('margin', {
                    easing: theme.transitions.easing.sharp,
                    duration: theme.transitions.duration.leavingScreen,
            }),
            marginLeft: 0,
            ...(open && {
                transition: theme.transitions.create('margin', {
                    easing: theme.transitions.easing.easeOut,
                    duration: theme.transitions.duration.enteringScreen,
                }),
                marginLeft: drawerWidth
            })
        }
    )
);

export default function PatientIndex() {

    let params = useParams()

    const [sidePanelOpen, setSidePanelOpen] = React.useState(true);

    return (    
        // TODO: Find better solution for minHeigh property (fully expand div in vertical direction)
        <div id="page-container" style={{ width: '100%', position: 'relative', minHeight:'92vh' }}>
            <Drawer
                sx={{
                    width: drawerWidth,
                    flexShrink: 0,
                    '& .MuiDrawer-paper': {
                        width: drawerWidth,
                    }
                }}
                PaperProps={{ style: { position: 'absolute' } }}
                BackdropProps={{ style: { position: 'absolute' } }}
                ModalProps={{
                    container: document.getElementById('page-container'),
                    style: { position: 'absolute' }
                }}
                variant="persistent"
                anchor="left"
                open={sidePanelOpen}
            >
                <Box sx={{ bgcolor: 'background.componentBg' }}>

                    <PatientInfo url={`${baseURL}patients/${params.patientId}/`} />
                    <Divider />
                    <Procedures procedureURL={`${baseURL}patients/${params.patientId}/procedures/`}/>

                </Box>
                

            </Drawer>

            <Main open={sidePanelOpen}>
                <Box sx={{ display: 'grid', gridTemplateRows: '54px auto', gridTemplateColumns: '1fr', bgcolor: 'background.componentBg'}}>
                    
                    {/* Toolbar */}
                    <Box sx={{ 
                        p: 1.5,
                        display: 'flex', 
                        flexDirection: 'row', 
                        bgcolor: 'background.componentBg',
                        justifyContent: 'space-between',
                        alignItem: 'center', 
                        borderBottom: '1px solid',
                        borderColor: 'divider',
                        top: 0,
                        position: 'sticky',
                    }}>
                        <IconButton
                            id="toggle-mode"
                            size="sm"
                            variant="outlined"
                            color="primary"
                            onClick={() => { setSidePanelOpen(!sidePanelOpen) }}
                        >
                            <MenuIcon />
                        </IconButton>

                        {/* TODO: Insert Breadcrumbs here */}

                    </Box>

                    {/* Main Content */}
                    <Box sx={{ display: 'flex', height: '100%' }}>
                        <Box sx={{ width: '300px', bgcolor: 'background.componentBg'}}> 

                            <Procedures procedureURL={`${baseURL}patients/${params.patientId}/procedures/`}/>

                        </Box>
                        <Box sx={{ flexGrow: 1, bgcolor: '#eee' }}>

                            <Typography sx={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}> View </Typography>
                        
                        </Box>
                    </Box>
                </Box>
            </Main>
        </div>
    );      
}
