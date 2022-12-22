import * as React from 'react';
import { Outlet, useParams, Link as RouterLink } from 'react-router-dom';
// MUI
import { styled, useTheme } from '@mui/material/styles';
import Drawer from '@mui/material/Drawer';
import Divider from '@mui/material/Divider';
import Box from '@mui/joy/Box';
import IconButton from '@mui/joy/IconButton';
// Icons import
import KeyboardArrowRightSharpIcon from '@mui/icons-material/KeyboardArrowRightSharp';
import KeyboardArrowLeftSharpIcon from '@mui/icons-material/KeyboardArrowLeftSharp';
import TuneSharpIcon from '@mui/icons-material/TuneSharp';
import PreviewSharpIcon from '@mui/icons-material/PreviewSharp';
import PlayArrowSharpIcon from '@mui/icons-material/PlayArrowSharp';
// Import sub components
import Procedures from './Procedures';
import PatientInfo from './PatientInfo';
import PatientPageMainView from './PatientPageMainView';
import config from '../utils/config';


const Main = styled('div', { shouldForwardProp: (prop) => prop !== 'open' }) <{ open?: boolean }>
(
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
                marginLeft: theme.patientView.drawerWidth
            })
        }
    )
);

export default function PatientIndex() {

    const theme = useTheme();
    const params = useParams();
    const recordRef = React.useRef<any>(null);
    const [activeTool, setActiveTool] = React.useState<string | undefined>(undefined);
    const [sidePanelOpen, setSidePanelOpen] = React.useState(true);

    // Set active tool if component is rendered
    if (params.toolId && params.toolId.toString() !== activeTool) {
        setActiveTool(params.toolId.toString())
    }

    return (    
        <div id="page-container" style={{ width: '100%', position: 'relative', height: `calc(100vh - ${theme.navigation.height})` }}>
            <Drawer
                sx={{
                    width: theme.patientView.drawerWidth,
                    flexShrink: 0,
                    '& .MuiDrawer-paper': {
                        width: theme.patientView.drawerWidth,
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
                <Box sx={{ overflow: 'auto', bgcolor: 'background.componentBg' }}>

                    <PatientInfo />
                    <Divider />
                    <Procedures />

                </Box>
                

            </Drawer>

            <Main open={sidePanelOpen}>
                <Box sx={{ display: 'grid', gridTemplateRows: `${theme.patientView.toolbarHeight} auto`, gridTemplateColumns: '1fr', bgcolor: 'background.componentBg'}}>
                    
                    {/* Toolbar */}
                    <Box sx={{ 
                        p: 1.5,
                        gap: 1,
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
                            {/* <MenuIcon /> */}
                            { sidePanelOpen ? <KeyboardArrowLeftSharpIcon /> : <KeyboardArrowRightSharpIcon/> }
                        </IconButton>

                        <Box sx={{ pr: 1.5, gap: 1, display: 'flex', flexDirection: 'row', justifyContent: 'right', width: '100%' }}>

                            {/* Start Record */}
                            <IconButton
                                id="toggle-sequence"
                                size="sm"
                                variant="outlined"
                                color="danger"
                                disabled={!params.recordId}
                                component={RouterLink}
                                to={`http://localhost:8080/api/v1/workflow/control/MEAS_START/`}
                            >
                                <PlayArrowSharpIcon />
                            </IconButton>
                            {/* Open sequence handler */}
                            <IconButton
                                id="toggle-sequence"
                                size="sm"
                                variant={activeTool == config.tools.configuration ? "soft" : "outlined"}
                                color="primary"
                                disabled={!params.recordId}
                                component={RouterLink}
                                to={`${params.procedureId}/${params.recordId}/${config.tools.configuration}`}
                                onClick={() => setActiveTool(config.tools.configuration)}
                            >
                                <TuneSharpIcon />
                            </IconButton>
                            {/* Open data viewer */}
                            <IconButton
                                id="toggle-dataview"
                                size="sm"
                                variant={activeTool == config.tools.dataview ? "soft" : "outlined"}
                                color="primary"
                                disabled={!params.recordId}
                                component={RouterLink}
                                to={`${params.procedureId}/${params.recordId}/${config.tools.dataview}`}
                                onClick={() => setActiveTool(config.tools.dataview)}
                            >
                                <PreviewSharpIcon />
                            </IconButton>
                            
                        </Box>

                        {/* TODO: Insert Breadcrumbs here */}

                    </Box>

                    {/* Main Content */}
                    <Box sx={{ display: 'flex', height: `calc(100vh - ${theme.patientView.toolbarHeight} - ${theme.navigation.height})` }}>
                        <Box sx={{ 
                            overflow: 'auto', 
                            width: theme.patientView.recordsWidth, 
                            bgcolor: 'background.componentBg',
                            borderRight: '1px solid',
                            borderColor: 'divider',
                        }}> 
                            <Outlet context={{ ref: recordRef }} />
                        </Box>

                        <Box sx={{ display: 'flex', flexGrow: 1, alignItems: 'center', justifyContent: 'center', bgcolor: 'background.componentBg' }}>
                            <PatientPageMainView/>
                        </Box>
                        
                    </Box>
                </Box>
            </Main>
        </div>
    );      
}
